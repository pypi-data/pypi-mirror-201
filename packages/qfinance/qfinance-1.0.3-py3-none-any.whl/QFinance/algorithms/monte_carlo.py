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
This module implements the Quantum Monte Carlo Integration algorithm.
Reference: http://arxiv.org/abs/1905.02666
"""

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegStorage

from QFinance.algorithms import MultiQubitState
from QFinance.algorithms import QuantumComparatorOP
from QFinance.algorithms.linear_function import SimplePiecewiseLinear
from QFinance.algorithms.amplitude_estimation import AEProblem
from QFinance.algorithms.amplitude_estimation import IQAE, MLAE

from QFinance.utils import sub_qreg, full_qreg

import numpy


class SimpleQMC:
    r"""
    This class implements the Quantum Monte Carlo Integration algorithm for the simple function:

    .. math::
        f(x) = \max\{0, x - x_k\} 
    
    where :math:`x_k` is a constant.

    The goal is to calculate the expectation value of :math:`f(x)`,
    with respect to a given distribution on :math:`[x_{min}, x_{max}]`.

    :param qubit_num: int, number of qubits used in the prepare state function.
    """

    def __init__(self, qubit_num: int):
        self.qnum = qubit_num
        self.qtotal = 2 * qubit_num + 1 + 1
        self.env = QEnv()
        self.qregL = self.env.Q.createList(self.qtotal)

        self.xmin = None
        self.xmax = None
        self.xk = None

        self.distribution = None

        self.working_qregL = []
        self.ancilla_qregL = [] 
        self.comp_qreg = None
        self.angle_qreg = None

        self.scaling_ = None

        self.pwl = None
        self.aep = None

    def load_dist(self, dist: numpy.ndarray) -> None:
        r"""
        Load distribution.
        
        The parameter `dist` should be a normalized vector, i.e., 
        
        .. math::
            \sum_{i=0}^{2^n-1} |v_i|^2 = 1.

        :param dist: The distribution on :math:`[x_{min}, x_{max}]`
        """
        self.distribution = dist
        assert len(self.distribution) == 2 ** self.qnum, "The length of distribution is not equal to 2 ** qnum."

    def set_linear(self, domain: tuple[float, float], xk: float) -> None:
        r"""
        Set the linear function which will be loaded after the quantum comparator.

        The linear function is :math:`f(x) = \max\{0, x - x_k\}` where :math:`x_k` is a constant.
        The piecewise linear function will be \max\{0, x - x_k\} defined on the interval :math:`[x_{min}, x_{max}]`.

        :param domain: The domain of the piecewise linear function.
        :param xk: The constant :math:`x_k`.
        """
        self.xmin, self.xmax = domain
        self.xk = xk
        assert self.xmin < self.xmax
        assert self.xk >= self.xmin and self.xk <= self.xmax

    def set_scaling(self, scaling: float) -> None:
        """
        Set the scaling factor for the linear function.

        :param scaling: The target scaling factor.
        """
        self.scaling_ = scaling

    def __print__(self) -> None:
        """
        Print the information of the problem.
        """
        print("xmin: ", self.xmin)
        print("xmax: ", self.xmax)
        print("xk: ", self.xk)
        print("function:", f"f(x) = max{{0, x - {self.xk}}} on [{self.xmin}, {self.xmax}]")
        print("qnum: ", self.qnum)
        print("qtotal: ", self.qtotal)

    def create_AEProblem(self) -> AEProblem:
        """
        Prepare state and load function f(x) into the quantum register.

        :return: The `AEProblem` object.
        """

        # set the qregL
        self.working_qregL = self.qregL[0: self.qnum]
        self.ancilla_qregL = self.qregL[self.qnum: 2 * self.qnum]
        self.comp_qreg = self.qregL[2 * self.qnum]
        self.angle_qreg = self.qregL[2 * self.qnum + 1]

        # prepare state
        self.state = MultiQubitState(self.distribution)
        self.state.load_to(self.working_qregL)

        # load the piecewise linear function
        self.pwl = SimplePiecewiseLinear((self.xmin, self.xmax), self.qnum, self.xk)
        ymax = self.pwl.ymax
        ymin = self.pwl.ymin
        beta = 1 / 2 - self.pwl.scaling * (ymax + ymin) / (ymax - ymin)

        if self.scaling_ is not None:
            self.pwl.scaling = self.scaling_
        self.pwl.apply_to(self.working_qregL, self.ancilla_qregL, self.comp_qreg, self.angle_qreg)

        # create the AE problem
        self.aep = AEProblem(self.env, self.qtotal)
        return self.aep

    def run_iqae(self) -> float:
        r"""
        Run the QMC algorithm, use IQAE to estimate the expectation value of :math:`f(x)`
        with respect to given distribution on :math:`[x_{min}, x_{max}]`.

        :return: The expectation value of :math:`f(x)` wrt. given distribution on :math:`[x_{min}, x_{max}]`.
        """
        aep = self.create_AEProblem()
        self.iqae = IQAE(aep)
        self.iqae.epsilon = 0.001
        self.iqae.alpha = 0.05
        self.iqae.num_shots = 10000
        self.iqae.run()
        self.measured_P1 = self.iqae.estimated_amp
        self.expectation = self.recover_amp(self.measured_P1)
        return self.expectation

    def run_mlae(self, Q_powers: list[int], shots: list[int], precision: float = 1E-4) -> float:
        """
        Run the algorithm, use MLAE to estimate the expectation value of :math:`f(x)` 
        wrt. given distribution on :math:`[x_{min}, x_{max}]`.

        :param Q_powers: The list of :math:`Q` powers.
        :param shots: The list of shots for each :math:`Q` power.
        :param precision: The precision of the grid, default is 1E-4.
        :return: The measured expectation value of :math:`f(x)` wrt. given distribution on :math:`[x_{min}, x_{max}]`.
        """
        aep = self.create_AEProblem()
        self.mlae = MLAE(aep)
        self.mlae.set_grid_precision(precision)

        error = None

        self.mlae.setup_arbitrary_scheme(Q_powers, shots)
        error = self.mlae.estimated_error()

        self.mlae.run()
        self.measured_P1 = self.mlae.estimated_amp
        self.measured_expectation = self.recover_amp(self.measured_P1)

        # recover the lower and upper bound of the expectation
        measured_expectation_lower_bound = self.recover_amp(self.measured_P1 - error)
        measured_expectation_upper_bound = self.recover_amp(self.measured_P1 + error)
        self.expectation_random_error = abs(measured_expectation_upper_bound - measured_expectation_lower_bound) / 2
        return self.measured_expectation

    def run_mlae_demo(self) -> float:
        r"""
        run the algorithm, use MLAE to estimate the expectation value of :math:`f(x)` with respect to 
        given distribution on :math:`[x_{min}, x_{max}]`.

        :return: The measured expectation value of :math:`f(x)` on :math:`[x_{min}, x_{max}]`.
        """
        aep = self.create_AEProblem()
        self.mlae = MLAE(aep)
        self.mlae.set_grid_precision(1E-4)

        scheme = "arbitrary"
        error = None

        if scheme == "linear":
            shots = 100000
            self.mlae.num_terms = 15
            # 12 is large enough
            self.mlae.setup_linear_scheme(shots)
            error = self.mlae.estimated_error()
            print(f"estimated error of MLAE linear scheme: {error:.4e}")

        elif scheme == "exponential":
            shots = 100000
            self.mlae.num_terms = 7
            self.mlae.setup_exponential_scheme(shots)
            error = self.mlae.estimated_error()
            print(f"estimated error of MLAE exponential scheme: {error:.4e}")

        elif scheme == "arbitrary":
            Q_power_list = [2, 3, 5, 10]
            shots_list = [100000] * len(Q_power_list)
            self.mlae.setup_arbitrary_scheme(Q_power_list, shots_list)
            error = self.mlae.estimated_error()
            # display error as scientific notation
            print(f"estimated error of MLAE arbitrary scheme: {error:.4e}")

        self.mlae.run()
        self.measured_P1 = self.mlae.estimated_amp
        self.measured_expectation = self.recover_amp(self.measured_P1)

        # recover the lower and upper bound of the expectation
        measured_expectation_lower_bound = self.recover_amp(self.measured_P1 - error)
        measured_expectation_upper_bound = self.recover_amp(self.measured_P1 + error)
        self.expectation_random_error = (measured_expectation_upper_bound - measured_expectation_lower_bound) / 2
        return self.measured_expectation

    def recover_amp(self, measured_P1: float) -> float:
        """
        Recover the desired expectation from the measured probability of :math:`\left|1\\right>` state.

        The measured P1 is equal to the return value from amplitude estimation.

        :param measured_P1: The measured probability of :math:`\left|1\\right>` state.
        """
        measured_expectation = self.pwl.measured_exp_from_P1(measured_P1)
        return measured_expectation
