#!/usr/bin/python3
# -*- coding: utf8 -*-

# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
This module implements the Iterative Quantum Amplitude Estimation algorithm.

Reference: http://arxiv.org/abs/1912.05559
"""

import numpy as np
import scipy.special

from QCompute import *
from copy import deepcopy

from QFinance.utils import sub_qreg, full_qreg
from QFinance.algorithms.amplitude_estimation.AE_problem import AEProblem


def inv_beta(alpha: float, x: float, y: float):
    r"""
    Calculate inverse of regularized incomplete beta function.
    
    This function corresponds to :math:`I^{-1}(\alpha;x,y)` in the reference.
    
    :param alpha: value of the incomplete beta function.
    :param x: the left end of the integration interval
    :param y: the right end of the integration interval
    """
    return scipy.special.betaincinv(x, y, alpha)


class IQAE:
    r"""
    The Iterative Quantum Amplitude Estimation class.

    In the methods of this class, we assume that every angular parameter is already scaled by :math:`1/2 \pi`,
    namely, mapped from a unit circle to [0, 1] interval.

    :param problem: the `AEProblem` instance
    """

    def __init__(self, problem: AEProblem) -> None:
        """
        Initialize the IQAE class.

        :param problem: the AEProblem instance

        num_qubits is the number of qubits that Q acts on.
        """
        self.problem = problem
        self.num_qubits = problem.num_qubits

        # epsilon is the error tolerance, or the accuracy of the estimation
        # the algorithm will stop when the width of confidence interval is less than 2*epsilon
        self.epsilon_ = 1E-4
        # maximum number of iterations
        self.max_iter_ = 100
        # confidence level is 1 - alpha
        self.alpha_ = 0.05
        # number of shots
        self.num_shots_ = 100
        # decide whether to group measurement results with the same k in the main loop
        self.group_same_k = True
        # confidence interval method, default is "CP" the Clopper-Pearson method
        self.confidence_interval_method = "CP"
        # accepted confidence interval methods are "CP" and "CH"
        # "CP" is the Clopper-Pearson method
        # "CH" is the Chernoff-Hoeffding method
        self.accepted_methods = ["CP", "CH"]
        # max number of rounds
        self.T = np.log2(np.pi / (8 * self.epsilon_))
        # L_max
        self.L_max = 1
        # the final confidence interval
        self.amplitude_ci = [0, 1]
        # the final amplitude
        self.estimated_amp = None

    @property
    def estimated_amplitude(self) -> float:
        """
        Return the estimated amplitude.
        """
        return (self.amplitude_ci[0] + self.amplitude_ci[1]) / 2

    @property
    def amplitude_interval(self) -> list:
        """
        Return the amplitude interval.
        """
        return self.amplitude_ci

    @property
    def epsilon(self) -> float:
        """
        Return the error tolerance.
        """
        return self.epsilon_

    @epsilon.setter
    def epsilon(self, epsilon):
        """
        Set the error tolerance.

        :param epsilon: the error tolerance.
        """
        self.epsilon_ = epsilon
        self.T = np.log2(np.pi / (8 * self.epsilon_))

    @property
    def max_iter(self):
        """
        Return the maximum number of iterations.
        """
        return self.max_iter_

    @max_iter.setter
    def max_iter(self, max_iter):
        """
        Set the maximum number of iterations.

        :param max_iter: the maximum number of iterations.
        """
        self.max_iter_ = max_iter

    @property
    def alpha(self):
        """
        Return the confidence level.
        """
        return self.alpha_

    @property
    def success_prob(self):
        """
        Return the success probability.
        """
        return 1 - self.alpha_

    @property
    def confidence_level(self):
        """
        Return the confidence level.
        """
        return 1 - self.alpha_

    @alpha.setter
    def alpha(self, alpha):
        """
        Set the value of alpha.

        :param alpha: the value of alpha.
        """
        self.alpha_ = alpha

    @property
    def num_shots(self):
        """
        Return the maximum number of shots.
        """
        return self.num_shots_

    @num_shots.setter
    def num_shots(self, num_shots):
        """
        Set the maximum number of shots.

        :param num_shots: the maximum number of shots.
        """
        self.num_shots_ = num_shots

    def set_confidence_interval_method(self, method) -> None:
        """
        Set the confidence interval method.

        :param method: the confidence interval method, can be "CP" or "CH".
        """
        if method not in self.accepted_methods:
            raise ValueError(f"Accepted confidence interval methods are 'CP' and 'CH', but {method} is given.")
        self.confidence_interval_method = method

    def max_shots(self) -> int:
        """
        Return the N_max in the reference.
        """
        factor = 32 / (1 - 2 * np.sin(np.pi / 14)) ** 2
        N_max = factor * np.log(2 / self.alpha_ * np.log2(np.pi / (4 * self.epsilon_)))
        return int(N_max)

    def max_num_oracle_calls(self) -> int:
        r"""
        Return the maximum number of oracle calls, :math:`N_{oracle}` in the reference.
        """
        N_oracle = 50 / self.epsilon_ * np.log(2 / self.alpha_ * np.log2(np.pi / (4 * self.epsilon_)))
        return int(N_oracle)

    def get_T(self) -> None:
        """
        Return the maximum number of rounds, :math:`T` in the reference.
        """
        self.T = np.ceil(np.log2(np.pi / (8 * self.epsilon_)))

    def calc_L_max(self) -> None:
        r"""
        Calculate :math:`L_{\max}`.
        """
        if self.confidence_interval_method == "CH":
            inner = 2 / self.num_shots_ * np.log(2 * self.T / self.alpha_)
            self.L_max = np.arcsin(np.power(inner, 1/4))
        elif self.confidence_interval_method == "CP":
            self.L_max = 1

    def confidence_interval_CH(self, a: float, num: int):
        """
        Return the confidence interval using Chernoff-Hoeffding method.

        :param a: the amplitude.
        :param num: the number of shots.
        """
        inner = 1 / (2 * num) * np.log(2 * self.T / self.alpha_)
        epsilon_a = np.sqrt(inner)
        a_max = min(a + epsilon_a, 1)
        a_min = max(a - epsilon_a, 0)
        return a_min, a_max

    def confidence_interval_CP(self, a: float, num: int):
        """
        Return the confidence interval using Clopper-Pearson method.

        Attention: the a_min and a_max in the reference is incorrect.

        :param a: the amplitude.
        :param num: the number of shots.
        """
        a_min = inv_beta(self.alpha / (2 * self.T), num * a, num * (1 - a) + 1)
        a_max = inv_beta(1 - self.alpha / (2 * self.T), num * a + 1, num * (1 - a))
        return a_min, a_max

    def measure_Qk(self, k: int, num: int) -> float:
        r"""
        Apply operator :math:`Q^k` to the state :math:`\left|0^n\right>` and measure the last qubit.

        Return the proportion of 1s in the sample, as an estimate of a for the current round.

        :param k: the power of :math:`Q`. Note that :math:`k` must be non-negative integer.
        :param num: the number of shots.
        """
        print(f"Measure Q^k with k = {k} and num = {num}")

        if k < 0:
            raise ValueError(f"Power k must be non-negative integer, but {k} is given.")
        if num <= 0:
            raise ValueError(f"Number of shots num must be positive integer, but {num} is given.")

        # intialize the environment
        env = QEnv()
        env.backend(BackendName.LocalBaiduSim2)
        q = env.Q
        q.createList(self.num_qubits)
        envA = deepcopy(self.problem.envA)
        opA = envA.convertToProcedure("opA", env)()
        envQ = deepcopy(self.problem.envQ)
        opQ = envQ.convertToProcedure("opQ", env)()

        # apply Q^k to the state |psi> = A |0>^num_qubits
        opA(*full_qreg(q))
        for _ in range(k):
            opQ(*full_qreg(q))

        # measure the last qubit
        MeasureZ([q[self.num_qubits - 1]], [0])
        taskResult = env.commit(num)
        counts_dict = taskResult['counts']

        # the estimated a is the number of 1s divided by the number of shots
        # get the number of 0s and 1s from the counts dictionary directly
        # because only one qubit is measured
        num_0 = counts_dict.get("0", 0)
        num_1 = counts_dict.get("1", 0)

        a_est = num_1 / num
        # check if the number of shots is correct
        if num_0 + num_1 != num:
            print("The number of shots do not match, use the measured number of shots.")
            a_est = num_1 / (num_0 + num_1)
        return a_est

    def run(self) -> None:
        """
        Run the main body of the IQAE algorithm.
        """
        # initialize iteration count
        iter_count = 0
        # initial power of Q
        k_i = 0
        # initial interval is on the upper half plane
        up_i = True

        # initial interval is [0, pi/2]
        # theta_{in the reference} = 2pi * theta_{in this function}
        theta_l = 0
        theta_u = 1/4

        # the number of measurements in each iteration, N in the reference
        num = self.num_shots_

        k_list = [k_i]
        a_list = []
        theta_lu_list = [[theta_l, theta_u]]

        self.get_T()
        self.calc_L_max()

        # the main loop
        while theta_u - theta_l > self.epsilon_ / np.pi:
            # increment the iteration count
            iter_count += 1
            print(f"\nIteration {iter_count}...")

            if iter_count > self.max_iter_:
                raise ValueError(f"The algorithm did not converge in {iter_count} iterations, \
                                 theta_u - theta_l = {theta_u - theta_l}")
            # calculate the next power of Q
            k_i, up_i = self.find_next_K(k_i, theta_l, theta_u, up_i)
            k_list.append(k_i)
            K_i = 4 * k_i + 2

            if K_i > np.ceil(self.L_max / self.epsilon_):
                # no overshooting condition
                num = np.ceil(self.num_shots_ * self.L_max / (K_i * self.epsilon_ * 10))
                num = int(num)
            else:
                num = self.num_shots_

            # measure the state, and return the approximate amplitude a_i
            a_i = self.measure_Qk(k_i, num)
            a_list.append(a_i)

            # combine results of the previous iterations with the same k_i
            # thus creating effective num and a_i
            # for each iteration with the same k_i, the number of shots is the same, i.e. num
            # the updated_num = num*j, where j is the number of consecutive iterations with the same k_i
            # the updated a_i is just the average of the a_i's
            # TODO: this part should be modified if shots are lost during measurement
            #
            if self.group_same_k:
                j = 1
                a_list_part = [a_list[-1]]
                if iter_count == 1:
                    pass
                else:
                    while (k_list[-1] == k_list[-j-1]):
                        # a_i = (a_i * j + a_list[-j]) / (j + 1)
                        a_list_part.append(a_list[-j])
                        j += 1
                        if j == iter_count:
                            break
                    a_i = np.mean(a_list_part)
                    num = num * j

            # calculate the interval of the approximate amplitude
            # from the measured approximate a_i
            if self.confidence_interval_method == "CH":
                a_min, a_max = self.confidence_interval_CH(a_i, num)
            elif self.confidence_interval_method == "CP":
                a_min, a_max = self.confidence_interval_CP(a_i, num)

            # calculate the confidence interval [theta_l, theta_u]
            theta_l, theta_u = self.calc_theta_from_a(a_min, a_max, up_i, K_i, theta_l, theta_u)
            theta_lu_list.append([theta_l, theta_u])

        # calculate the confidence interval [a_l, a_u] of the amplitude
        # from the confidence interval [theta_l, theta_u]
        # first restore the 2*pi factor in theta, then
        # [a_l, a_u] = [sin^2(theta_l), sin^2(theta_u)]
        a_l = np.sin(2 * np.pi * theta_l)**2
        a_u = np.sin(2 * np.pi * theta_u)**2
        self.amplitude_ci = [a_l, a_u]
        self.estimated_amp = (a_l + a_u) / 2

        print(f"The IQAE algorithm converged in {iter_count} iterations.\n \
        The confidence interval of the amplitude is [{self.amplitude_ci[0]}, {self.amplitude_ci[1]}].")

    def calc_theta_from_a(self, a_min: float, a_max: float, up: bool, K: int, theta_l: float, theta_u: float):
        r"""
        Calculate the confidence interval :math:`[\theta_l, \theta_u]`.

        The confidence interval of :math:`\theta` is calculated from the confidence interval
        :math:`[a_{min}, a_{max}]` of the approximate amplitude.

        :param a_min: the lower bound of the confidence interval of the approximate amplitude
        :param a_max: the upper bound of the confidence interval of the approximate amplitude
        :param up: a boolean flag indicating whether the interval is in the upper half plane
        :param K: the power of Q
        :param theta_l: the lower bound of the confidence interval of theta
        :param theta_u: the upper bound of the confidence interval of theta
        """
        # step 1. calculate the confidence interval [theta_min, theta_max]
        # from [a_min, a_max] and the boolean flag up
        # by inverting a = (1 - cos(K_i theta))/2
        #
        # a = P[|1>] = sin^2((2k+1) * theta)
        # = (1 - cos((4k+2) * theta))/2
        # = (1 - cos(K * theta))/2
        theta_min = 0
        theta_max = 0
        if up:
            # [theta_min, theta_max] is in the upper half plane
            # angle is scaled by 1/2pi as usual
            # [theta_min, theta_max] \subset [0, 1/2]
            theta_min = np.arccos(1 - 2 * a_min) / (2 * np.pi)
            theta_max = np.arccos(1 - 2 * a_max) / (2 * np.pi)
        else:
            theta_min = 1 - np.arccos(1 - 2 * a_max) / (2 * np.pi)
            theta_max = 1 - np.arccos(1 - 2 * a_min) / (2 * np.pi)

        # step 2. determine the integer M, which satisfies
        # K*theta_l = 2pi * M + theta_min
        # K*theta_u = 2pi * M + theta_max
        # angle is scaled by 1/2pi as usual
        M_l = np.floor(K * theta_l)
        M_u = np.floor(K * theta_u)
        # M calculated from theta_l and theta_u should be the same
        # this is guaranteed by the find_next_K subroutine
        # TODO: sometimes M_l and M_u differ by 1, which is not expected

        # step 3. calculate the final interval [theta_l, theta_u]
        new_theta_l = (M_l + theta_min) / K
        new_theta_u = (M_l + theta_max) / K

        return new_theta_l, new_theta_u

    def find_next_K(self, k: int, theta_l: float, theta_u: float, up: bool, r: int = 2):
        r"""
        Implement the *FindNextK* subroutine in the reference.

        Find the largest :math:`k` such that the interval :math:`[(4k+2)\theta_l, (4k+2)\theta_u]` is fully contained
        in either :math:`[0, \pi]` or :math:`[\pi, 2\pi]`.

        In this function, we assume that every angular parameter is already scaled by :math:`1/2\pi`.
        
        :math:`\theta_l` and :math:`\theta_u` are in the interval :math:`[0, 1]`.

        :math:`\theta_{\text{in the reference}} = 2\pi\times\theta_{\text{in this function}}`

        :math:`r` is the ratio.

        :param k: the current :math:`k`
        :param theta_l: the lower bound of the confidence interval of :math:`theta`
        :param theta_u: the upper bound of the confidence interval of :math:`theta`
        :param up: the boolean flag indicating whether the interval is in the upper half plane
        :param r: the ratio
        """
        Ki = 4 * k + 2
        theta_min = Ki * theta_l
        theta_max = Ki * theta_u
        K_max = int(np.floor(0.5 / (theta_u - theta_l)))

        # largest potential candidate, of the form 4k + 2, and <= K_max
        # K_candidate = K_max - (K_max - 2) % 4
        K_candidate = K_max
        while (K_candidate - 2) % 4 != 0:
            K_candidate -= 1

        while K_candidate >= r * Ki:
            # factor to scale the angle
            q = K_candidate / Ki
            if (q * theta_max) % 1 <= 0.5 and (q * theta_min) % 1 <= 0.5:
                # the next interval [theta_min, theta_max] is in upper half plane
                K_i1 = K_candidate
                up_i1 = True
                k_i1 = (K_i1 - 2) // 4
                return k_i1, up_i1
            elif (q * theta_max) % 1 > 0.5 and (q * theta_min) % 1 > 0.5:
                # the next interval [theta_min, theta_max] is in lower half plane
                K_i1 = K_candidate
                up_i1 = False
                k_i1 = (K_i1 - 2) // 4
                return k_i1, up_i1
            else:
                K_candidate -= 4

        # if we reach here, then we cannot find a valid K, return the old value
        return k, up
