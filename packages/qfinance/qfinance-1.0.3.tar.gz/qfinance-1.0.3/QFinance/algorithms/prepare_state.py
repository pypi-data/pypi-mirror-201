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
This module implements the algorithm to prepare an arbitrary state.

Reference: http://arxiv.org/abs/quant-ph/0406176
"""

import numpy as np
from copy import deepcopy

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegPool, QRegStorage
from QFinance.utils import sub_qreg, full_qreg, sub_qreg_slice, parse_counts_dict_to_freq_list


class SingleQubitState:
    r"""
    This class implements the algorithm to prepare an arbitrary single qubit state.

    The input state is a 2-dim vector :math:`\left|\psi\right> = \alpha\left|0\right> + \beta\left|1\right>`.

    The state :math:`\left|\psi\right>` is expected to be normalized, i.e., 
    :math:`|\alpha|^2 + |\beta|^2 = 1`.
    However, this class will normalize the input state if it is not.

    In the most general case, the state |psi> can be written as

    .. math::
        \left|\psi\right> &= \alpha \left|0\right> + \beta \left|1\right> \\
        &= r e^{it/2} (e^{-i \phi/2} \cos(\theta/2) \left|0\right> + 
        e^{i\phi/2} \sin(\theta/2) \left|1\right>)

    where 
    
    .. math::
        r &= \sqrt{|\alpha|^2 + |\beta|^2}, \\
        t &= arg(\alpha) + arg(\beta), \\
        \phi &= arg(\beta) - arg(\alpha), \\
        \theta &= 2\arccos(|\alpha|/r).

    The single qubit state can be rotated back to the state :math:`\left|0\right>` by applying `Rz` and `Ry` gate:

    .. math::
        R_y(-\theta) R_z(-\phi) \left|\psi\right> = r e^{i t/2} \left|0\right>

    :param state: The target state. It should be a 2-dim ndarray.
    """

    def __init__(self, state: np.ndarray) -> None:
        """
        Initialize the algorithm.

        :param state: The target state.
        """
        if not isinstance(state, np.ndarray):
            raise TypeError('state should be a numpy array')
        if state.shape != (2,):
            raise ValueError('state should be a 2-dim vector')
        # self._state = state
        self.alpha = state[0]
        self.beta = state[1]
        # self.r = np.sqrt(abs(self.alpha) ** 2 + abs(self.beta) ** 2)
        self.r = np.linalg.norm(state)
        self.theta = 2 * np.arccos(abs(self.alpha) / self.r)
        self.t = np.angle(self.alpha) + np.angle(self.beta)
        self.phi = np.angle(self.beta) - np.angle(self.alpha)
        # record the normalization factor r * exp(i * t / 2)
        self.norm_factor = self.r * np.exp(1j * self.t / 2)


class MultiQubitState:
    r"""
    This class prepares the multi qubit state.

    The input state is a :math:`2^n`-dim vector:

    .. math::
        \left|\psi\right> = \sum_{i=0}^{2^n-1} \alpha_i \left|i\right>

    The state :math:`\left|\psi\right>` is expected to be normalized, i.e., 
    
    .. math::
        \sum_{i=0}^{2^n-1} |\alpha_i|^2 = 1,

    however, this class will normalize the input state if it is not.

    :param state: The target state. It should be a :math:`2^n`-dim numpy array.
    """

    def __init__(self, state: np.ndarray) -> None:
        if not isinstance(state, np.ndarray):
            raise TypeError('state should be a numpy array')
        if not np.log2(state.shape[0]).is_integer():
            raise ValueError('state should be a 2^n-dim vector')

        self.num_qubits = int(np.log2(state.shape[0]))

        self.state = state
        self.current_num_qubits = self.num_qubits
        # self.partitiond_single_qubit_states = None
        # self.thetas = None
        # self.phis = None
        # self.residual = None
        # self.partition_state(self.state)

        self.qreg_list = None

        self.shots = 1000

    def partition_state(self, state: np.ndarray) -> tuple:
        r"""
        Partition the multi qubit state into single qubit states.

        :param state: The target state, should be a :math:`2^n`-dim ndarray.
        :return: the tuple (residual, thetas, phis)
        """
        if not isinstance(state, np.ndarray):
            raise TypeError('state should be a numpy array')
        if not np.log2(state.shape[0]).is_integer():
            raise ValueError('state should be a 2^n-dim vector')

        num_qubits = int(np.log2(state.shape[0]))

        # partition the state to contiguous 2-dim vectors
        num_partitiond = 2 ** (num_qubits - 1)
        state = np.reshape(state, (num_partitiond, 2))

        partitiond_single_qubit_states = []
        thetas = []
        phis = []
        residual = []

        for i in range(num_partitiond):
            single_qubit_state = SingleQubitState(state[i])
            partitiond_single_qubit_states.append(single_qubit_state)
            thetas.append(single_qubit_state.theta)
            phis.append(single_qubit_state.phi)
            residual.append(single_qubit_state.norm_factor)

        # convert the list to numpy array
        thetas = np.array(thetas)
        phis = np.array(phis)
        residual = np.array(residual)

        return (residual, thetas, phis)

    def load_to(self, qreg_list: list[QRegStorage]) -> None:
        """
        Prepare the the state by "peeling off" single qubits.

        :param qreg_list: The list of qregs.
        """
        # check that num_qubits is equal to the length of qreg
        if self.num_qubits != len(qreg_list):
            raise ValueError('The length of qreg should be equal to the number of qubits')

        self.qreg_list = qreg_list

        current_state = self.state
        self.current_num_qubits = self.num_qubits

        thetas_list = []
        phis_list = []

        # the main recursion
        while self.current_num_qubits >= 1:
            # partition the current state
            residual, thetas, phis = self.partition_state(current_state)
            # store the thetas and phis
            thetas_list.append(thetas)
            phis_list.append(phis)
            # # prepare the current state
            # self.multiplexor(RZ, -phis, self.current_num_qubits - 1)
            # self.multiplexor(RY, -thetas, self.current_num_qubits - 1)
            # update the current state
            current_state = residual
            self.current_num_qubits -= 1

        # construct the state from the thetas and phis
        # by inverting the recursion
        thetas_list.reverse()
        phis_list.reverse()
        self.current_num_qubits = 0
        while self.current_num_qubits < self.num_qubits:
            self.current_num_qubits += 1
            # prepare the current state
            self.multiplexor(RY, thetas_list[self.current_num_qubits - 1], self.current_num_qubits - 1)
            self.multiplexor(RZ, phis_list[self.current_num_qubits - 1], self.current_num_qubits - 1)

    def measure_state(self) -> np.ndarray:
        r"""
        Measure the final state of self.env and return the prob vector.

        The prob vector is to be compared with :math:`|\text{target_state}|^2`.
        This function is used for testing purpose.

        :return: np.ndarray, the frequency vector.
        """
        env = self.qreg_list[0].env
        env.backend(BackendName.LocalBaiduSim2)
        MeasureZ(self.qreg_list, range(self.num_qubits))
        task_result = env.commit(self.shots)
        counts_dict = task_result['counts']
        freq_list = parse_counts_dict_to_freq_list(counts_dict, self.num_qubits, self.shots)
        freq_array = np.array(freq_list)
        return freq_array

    def multiplexor(self, rot_gate, angles: list, numq: int) -> None:
        r"""
        Implement the multiplexor recursion.

        In the "outermost" recursion, the environment is the original environment, current env has `numq + 1` qubits,
        and `numq = self.num_qubits - 1`.
        The number of angles is halved in each recursion.

        :param rot_gate: The rotation gate, can be either `RZ` or `RY`.
        :param angles: An array of angles, is a list with :math:`2^{\text{numq}}` rotation angles.
        :param numq: The number of qubits in the current multiplexor.
        """
        # number of qubits should be non-negative
        if numq < 0:
            raise ValueError('The number of qubits should be non-negative')

        # check the length of angles
        if len(angles) != 2 ** numq:
            raise ValueError('The length of angles should be 2^numq')

        # check the type of angles
        # angles should be a ndarray
        if not isinstance(angles, np.ndarray):
            raise TypeError('angles should be a ndarray')

        # "shift" the environment wrt. two factors
        # shift by the current "peeling off" step, dictated by self.current_num_qubits
        # shift by the current multiplexor recursion, dictated by numq
        # working_qreg = sub_qreg_slice(self.q, self.current_num_qubits - 1 - numq, self.current_num_qubits)
        working_qreg = self.qreg_list[self.current_num_qubits - 1 - numq: self.current_num_qubits]

        # base case
        if numq == 0:
            # check that the angles list and the working_qreg has length 1
            if len(angles) != 1:
                raise ValueError('The length of angles should be 1')
            if len(working_qreg) != 1:
                raise ValueError('The length of working_qreg should be 1')

            # apply the rotation gate
            rot_gate(angles[0])(working_qreg[0])

        # recursion
        else:
            # check that the angles list and the working_qreg has matching length
            if len(angles) != 2 ** (len(working_qreg) - 1):
                raise ValueError('The length of angles should match the length of working_qreg')

            # generate the plus and minus angles list
            num_angles = len(angles)
            num_new_angles = num_angles // 2
            angles_first_half = angles[0:num_new_angles]
            angles_second_half = angles[num_new_angles:num_angles]
            angles_plus = (angles_first_half + angles_second_half) / 2
            angles_minus = (angles_first_half - angles_second_half) / 2

            # apply the part corresponding to the plus angles
            self.multiplexor(rot_gate, angles_plus, numq - 1)

            # apply the CNOT gate
            CX(working_qreg[0], working_qreg[-1])

            # apply the part corresponding to the minus angles
            self.multiplexor(rot_gate, angles_minus, numq - 1)

            # apply the CNOT gate
            CX(working_qreg[0], working_qreg[-1])
