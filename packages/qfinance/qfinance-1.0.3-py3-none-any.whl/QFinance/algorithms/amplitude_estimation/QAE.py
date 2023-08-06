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
This module implements the canonical QAE algorithm.

Reference: http://arxiv.org/abs/quant-ph/0005055
"""

import numpy

from QCompute import *
from copy import deepcopy

from QFinance.utils import sub_qreg, full_qreg
from QFinance.utils import parse_counts_dict_to_float
from QFinance.utils import extract_to_float_by_max

from QFinance.algorithms.amplitude_estimation.AE_problem import AEProblem
from QFinance.algorithms.QFT import QFT


class CanonicalQAE:
    """
    The Canonical quantum amplitude estimation class.

    :param problem: The amplitude estimation problem.
    """

    def __init__(self, problem: AEProblem):
        """
        Initialize the class.

        num_qubits: The number of qubits that Q acts on.
        num_ancillas: The number of ancillary qubits, used to control the precision of estimation
        num_total: The total number of qubits, equal to num_qubits + num_ancillas

        :param problem: The amplitude estimation problem.
        """
        self.problem = problem
        self.num_qubits_ = problem.num_qubits
        self.num_ancillas_ = None
        self.num_total_ = None
        self.q = None
        self.op_A = None
        self.op_CQ = None
        self.estimated_amplitude = None
        self.shots = 1

    @property
    def num_qubits(self) -> int:
        """
        Return the number of qubits.
        """
        return self.num_qubits_

    @property
    def num_ancillas(self) -> int:
        """
        Return the number of ancillary qubits.
        """
        return self.num_ancillas_

    @property
    def num_total(self) -> int:
        """
        Return the total number of qubits.
        """
        return self.num_total_

    @num_ancillas.setter
    def num_ancillas(self, num_ancillas: int) -> None:
        """
        Set the number of ancillary qubits.

        :param num_ancillas: The number of ancillary qubits.
        """
        self.num_ancillas_ = num_ancillas
        self.num_total_ = self.num_qubits_ + self.num_ancillas_

    def init_env(self) -> None:
        """
        Setup the initial environment.

        Create the quantum register used by the algorithm.
        """
        self.env = QEnv()
        self.env.backend(BackendName.LocalBaiduSim2)
        self.q = self.env.Q
        self.q.createList(self.num_total)

    def inherit_env(self, env: QEnv) -> None:
        """
        Inherit the environment from the input env.

        :param env: The environment to inherit.
        """
        self.env = env
        self.q = env.Q

    def check_env(self) -> None:
        """
        Check if the environment is valid.
        """
        if self.q is None:
            raise ValueError("The environment is not initialized.")
        if len(self.q.registerMap) != self.num_total:
            raise ValueError("The number of qubits in the environment is not equal to the total number of qubits.")
        if self.num_ancillas_ is None:
            raise ValueError("The number of ancillary qubits is not set.")

    def setup_qreg(self) -> None:
        r"""
        Setup the working and ancillary quantum registers.

        The working and ancillary qubits are all initialized to :math:`\left|0\right>`.
        The ancillary qubits are the qubits with indices [0, num_ancillas).
        The working qubits are the qubits with indices [num_ancillas, num_total).
        """
        self.ancilla_qreg = sub_qreg(self.q, 0, self.num_ancillas_)
        self.working_qreg = sub_qreg(self.q, self.num_ancillas_, self.num_qubits_)
        self.total_qreg = full_qreg(self.q)

    def prepare_A(self) -> None:
        """
        Prepare the amplitude estimation problem.
        """
        self.envA = deepcopy(self.problem.envA)
        self.op_A = self.envA.convertToProcedure("procA", self.env)()

    def prepare_ctrlQ(self) -> None:
        """
        Prepare the controlled-:math:`Q` gate.

        `ctrlQ` acts on the working qubits and is controlled by one of the ancillary qubits.
        `ctrlQ` is a gate with (`num_qubits_ + 1`) qubits.

        Attention: in QCompute, the controlling qubit is the last qubit, e.g.,
        use `ctrlQ(working, ancilla)` if :math:`Q` acts on working qubits.
        """
        self.envQ = deepcopy(self.problem.envQ)
        self.envQ.convertToProcedure("procQ", self.env)
        self.proc_CQ, _ = self.env.controlProcedure("procQ")
        self.op_CQ = self.proc_CQ()

    def check_status(self) -> None:
        """
        Check that the environment is valid.

        Also check that the amplitude estimation problem and the controlled Q gate are prepared.
        """
        self.check_env()
        if self.ancilla_qreg is None:
            raise ValueError("The ancillary qubits are not prepared.")
        if self.working_qreg is None:
            raise ValueError("The working qubits are not prepared.")
        if self.total_qreg is None:
            raise ValueError("The total qubits are not prepared.")
        if self.op_A is None:
            raise ValueError("The amplitude estimation problem is not prepared.")
        if self.op_CQ is None:
            raise ValueError("The controlled Q gate is not prepared.")

    def estimate(self) -> None:
        """
        Run the canonical QAE algorithm.
        """
        self.check_status()

        # step 1. apply the Hadamard gate to the ancillary qubits
        for ancilla_qubit in self.ancilla_qreg:
            H(ancilla_qubit)

        # step 2. apply the operator A to the working qubits
        self.op_A(*self.working_qreg)

        # step 3. apply the controlled Q^(2^j) gate to the working qubits and ancillary qubits
        count = 0
        for ancilla_qubit in reversed(self.ancilla_qreg):
            for _ in range(2 ** count):
                self.op_CQ(*self.working_qreg, ancilla_qubit)
            count += 1

        # step 4. apply the inverse QFT to the ancillary qubits
        qft_env = QFT(self.num_ancillas_, True).qft_env
        qft_op = qft_env.convertToProcedure("procQFT", self.env)()
        qft_op(*self.ancilla_qreg)

        # step 5. measure the ancillary qubits and calculate the estimated amplitude
        counts_dict = self.measure_ancillas()
        self.get_estimated_amp_by_max(counts_dict)

    def measure_ancillas(self) -> dict:
        """
        Measure the ancillary qubits in the last step of the canonical QAE algorithm.

        :return: the counts_dict of the measurement.
        """
        if self.env.backendName is None:
            raise ValueError("The backend of the environment is not set.")

        MeasureZ(self.ancilla_qreg, range(self.num_ancillas_))
        taskResult = self.env.commit(self.shots)
        counts_dict = taskResult['counts']
        return counts_dict

    def get_estimated_amp_by_max(self, counts_dict: dict) -> None:
        """
        Calculate the estimated amplitude from the counts_dict of the measurement.
        
        The estimated amplitude is the one which corresponds to the maximum counts.

        :param counts_dict: The counts_dict obtained from the measurement result.
        """
        estimated_theta = numpy.pi * extract_to_float_by_max(counts_dict, self.num_ancillas_)
        self.estimated_amplitude = numpy.sin(estimated_theta) ** 2
