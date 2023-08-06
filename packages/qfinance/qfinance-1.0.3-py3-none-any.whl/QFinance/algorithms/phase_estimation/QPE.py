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


import pprint
import numpy as np
import sys

from traitlets import List


from QCompute import *

from QCompute.QPlatform.QRegPool import QRegPool, QRegStorage
from QCompute.QPlatform.QOperation.QProcedure import QProcedure, QProcedureOP

from QFinance.algorithms.QFT import QFT


def subQreg(q: QRegPool, start: int, num: int) -> list[QRegStorage]:
    """
    Return a list of QRegStorage with the qubits in the given slice.

    :param q: the quantum register from which the qubits are taken
    :param start: the start index of the slice
    :param num: the number of qubits in the slice

    :return: a list of QRegStorage
    """
    if start is None:
        start = 0
    dic = q.registerMap

    return [v for k, v in dic.items() if start <= k < start + num]


class QPE:
    r"""
    This is a conceptual class representation of Quantum Phase Estimation algorithm.

    The input of the algorithm is an operator ctrl-U, which acts on :math:`n + 1` qubits.
    The oracle in QPE algorithm is the black box composed of sequential ctrl-:math:`U^{2^k}` gates.
    The eigenvalue of U is :math:`e^{2*\pi*i*\phi}`.

    :param num_qubits: int, number of qubits that U acts on
    :param num_ancillas: int, number of ancilla qubits, on which the final inverse QFT is applied
    :param ctrlU_env: QEnv, the environment correspondind to the controlled unitary operator
    """

    def __init__(self, num_qubits: int, num_ancillas: int, ctrlU_env: QEnv):
        """
        Initialize the QPE class.

        :param num_qubits: int, number of qubits that U acts on
        :param num_ancillas: int, number of ancilla qubits, on which the final inverse QFT is applied
        :param ctrlU_env: QEnv, the environment correspondind to the controlled unitary operator
        """
        self.num_qubits = num_qubits
        self.num_ancillas = num_ancillas
        self.num_total = num_qubits + num_ancillas
        self.ctrlU_env = ctrlU_env
        # self.oracle = oracle
        self.env = QEnv()
        self.q = self.env.Q
        self.q.createList(self.num_total)
        self.ancilla_qubits = subQreg(self.q, 0, self.num_ancillas)
        self.operating_qubits = subQreg(self.q, self.num_ancillas, self.num_qubits)
        self.total_qubits = subQreg(self.q, 0, self.num_total)
        self.eigenstate: QEnv = None
        # self.oracle = self.get_oracle(ctrlU)
        self.oracle: QProcedureOP = None
        self.oracle_constructed = False
        self.oracle_applied = False
        self.estimated_phase = 0
        self.estimated_eigenvalue = 1
        self.shots = 1024

    def select_backend(self, backendName: str):
        """
        Select backend.

        :param backendName: the target backend name.
        """
        self.env.backend(backendName)

    def apply_oracle(self) -> None:
        """
        Apply the oracle ctrl-U^{2^k} to the ancilla qubits.
        """
        # convert QEnv ctrlU to an QProcedureOP on the current environment
        self.ctrlU = self.ctrlU_env.convertToProcedure('ctrlU', self.env)()

        for i in range(self.num_ancillas):
            # ctrl-U^{2^(n-i-1)}
            for _ in range(2 ** (self.num_ancillas - i - 1)):
                self.ctrlU(self.q[i], *self.operating_qubits)

        self.oracle_applied = True

    def estimate_phase(self) -> None:
        """
        Estimate the phase of U operator using the Quantum Phase Estimation algorithm.

        The estimated phase is stored in self.estimated_phase.
        The estimated eigenvalue is stored in self.estimated_eigenvalue.
        """

        if not self.env.backendName:
            raise RuntimeError("backend not selected")

        if not self.eigenstate:
            raise RuntimeError("eigenstate not prepared")

        # Apply Hadamard gates to the ancilla qubits
        for i in range(self.num_ancillas):
            H(self.q[i])

        # Apply the oracle
        # if not self.oracle_constructed:
        #     self.get_oracle()
        # self.oracle(*self.total_qubits)

        # Apply the oracle
        if not self.oracle_applied:
            self.apply_oracle()

        # Apply inverse QFT
        iqft = QFT(self.num_ancillas, True)
        iqft_subroutine = iqft.qft_env.convertToProcedure('iqft', self.env)()
        iqft_subroutine(*self.ancilla_qubits)

        # Measure the ancilla qubits
        MeasureZ(subQreg(self.q, 0, self.num_ancillas), range(self.num_ancillas))

        task_result = self.env.commit(self.shots, fetchMeasure=True)
        counts_dict = task_result['counts']
        self.estimated_phase = self.get_phase_by_mean(counts_dict)
        # self.estimated_phase = self.get_phase_by_max(counts_dict)
        self.estimated_eigenvalue = np.exp(2 * np.pi * 1j * self.estimated_phase)
        # return self.estimated_phase

    def get_phase_by_max(self, counts_dict: dict) -> float:
        """
        Extract the estimated phase, use the result with maximum likelihood in the measurement.

        :param counts_dict: dict, the counts dictionary, which looks like {'000': 512, '001': 512}
            QCompute uses big-endian, so the order is like '(n-1),(n-2),...,0'

        :return: the estimated phase
        """
        def parse_bits_string(bits_string: str) -> int:
            """
            parse the bits string to integer
            :param bits_string: bits string, like '110'
            :return: integer, like 0
            QCompute uses big-endian
            """
            reversed_bits_string = bits_string[::-1]
            return int(reversed_bits_string, 2)

        phase = 0
        kmax = None
        vmax = 0
        for k, v in counts_dict.items():
            if v > vmax:
                kmax = k
                vmax = v

        if kmax is not None:
            phase = parse_bits_string(kmax) / 2 ** self.num_ancillas
        return phase

    def get_phase_by_mean(self, counts_dict: dict) -> float:
        """
        Extract the estimated phase, use the average result in the measurement with corresponding weight.

        :param counts_dict: counts dictionary, looks like {'000': 512, '001': 512}
            QCompute uses big-endian, so the order is like '(n-1),(n-2),...,0'
            
        :return: estimated phase
        """
        def parse_bits_string(bits_string: str) -> int:
            """
            parse the bits string to integer
            :param bits_string: bits string, like '110'
            :return: integer, like 0
            QCompute uses big-endian
            """
            reversed_bits_string = bits_string[::-1]
            return int(reversed_bits_string, 2)

        phase = 0
        v_total = 0

        for k, v in counts_dict.items():
            v_total += v

        for k, v in counts_dict.items():
            phase += parse_bits_string(k) * v / v_total

        phase /= 2 ** self.num_ancillas

        return phase
