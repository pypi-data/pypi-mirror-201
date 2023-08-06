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
This module defines a general amplitude estimation problem.
"""

from QCompute import *
from copy import deepcopy

from QFinance.utils import sub_qreg, full_qreg
from QFinance.utils import cnx, cnz


class AEProblem:
    r"""
    Amplitude estimation problem class.

    The operator A satisfies

    .. math::
        A\left|0\right> = \sqrt{1-a} \left|\psi_0\right> \left|0\right> + \sqrt{a} \left|\psi_1\right>\left|0\right>,

    where :math:`a` is the probability of measuring :math:`\left|1\right>` in the ancilla qubit.

    Equivalently, 
    
    .. math::
        A\left|0\right> = \cos(\theta_a) \left|\psi_0\right> \left|0\right> + 
        \sin(\theta_a) \left|\psi_1\right>\left|0\right>.
    
    On the left hand side, :math:`\left|\psi_0\right>` represesnts an array of num_qubits zero states.

    The environment `envQ` carries the operator :math:`Q`, which is the main unitary operator
    in the amplitude estimation algorithm:

    .. math::
        Q = A S_0 A^{\dagger} S_{\psi_0}

    :param num_qubits: int, number of qubits that operator :math:`A` acts on.
    :param envA: QEnv, the environment which carries operator :math:`A`.
    """

    def __init__(self, envA: QEnv, num_qubits: int) -> None:
        self.envA_ = envA
        self.num_qubits_ = num_qubits
        self.envQ_ = None

    @property
    def envA(self) -> QEnv:
        """
        Get the operator A.
        """
        return self.envA_

    @envA.setter
    def envA(self, envA: QEnv) -> None:
        """
        Set the operator A.

        :param envA: QEnv, the environment which carries operator A.
        """
        self.envA_ = envA

    @property
    def num_qubits(self) -> int:
        """
        Get the number of qubits that operator A acts on.
        """
        return self.num_qubits_

    @num_qubits.setter
    def num_qubits(self, num_qubits: int) -> None:
        """
        Set the number of qubits that operator A acts on.

        :param num_qubits: int, number of qubits that operator A acts on.
        """
        self.num_qubits_ = num_qubits

    @property
    def envQ(self) -> QEnv:
        """
        Get the operator Q.
        """
        if self.envQ_ is None:
            self.assemble_Q()
        return self.envQ_

    @envQ.setter
    def envQ(self, envQ: QEnv) -> None:
        """
        Set the operator Q.

        :param envQ: QEnv, the environment which carries operator Q.
        """
        self.envQ_ = envQ

    def reflection_S_psi0(self) -> QEnv:
        r"""
        Construct the reflection operator :math:`S_{\psi_0}`.

        The operator :math:`S_{\psi_0} = I \otimes Z` is a reflection about the bad state :math:`|\psi_0>|0>`.
        
        :math:`S_{\psi_0}` acts as follows:

        .. math::
            \left|\psi_0\right> \left|0\right> &\rightarrow - \left|\psi_0\right> \left|0\right> \\
            \left|\psi_1\right> \left|1\right> &\rightarrow \left|\psi_1\right> \left|1\right>
        """
        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        Z(q[self.num_qubits_ - 1])
        return env

    def reflection_S0(self) -> QEnv:
        r"""
        Construct the reflection operator :math:`S_0`.

        :math:`S_0` is the reflection about the state :math:`\left|0^n\right>`, 
        where :math:`n` = `self.num_qubits`.

        .. math::
            S_0 &= 2 \left|0^n\right> \left<0^n\right| - I \\
            S_0 &= X^n C^{n-1}Z X^n
        """
        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        qreglist = full_qreg(q)
        for i in range(self.num_qubits_):
            X(q[i])
        cnz(self.num_qubits_ - 1, env)
        for i in range(self.num_qubits_):
            X(q[i])
        return env

    def assemble_Q(self) -> None:
        r"""
        Assemble the Grover operator :math:`Q`.
        
        .. math::
            Q = A S_0 A^{\dagger} S_{\psi_0}

        The circuit of :math:`Q` has the same size as the circuit of :math:`A`.
        """
        # this is the main env associated to opQ

        env = QEnv()
        q = env.Q
        q.createList(self.num_qubits_)
        qreglist = full_qreg(q)

        # in case where an instance of AEProblem calls assemble_Q() multiple times
        envA = deepcopy(self.envA_)

        # construct A and A^dagger operators
        # the inverseCircuit() method already uses the deepcopy, so we don't need to deepcopy self.envA_ here
        opA_dagger = envA.inverseCircuit().convertToProcedure('opA_dagger', env)()
        opA = envA.convertToProcedure('opA', env)()

        # construct S0 and S_{psi0} operators
        opS0 = self.reflection_S0().convertToProcedure('opS0', env)()
        opS_psi0 = self.reflection_S_psi0().convertToProcedure('opS_psi0', env)()

        # assemble Q operator: Q = A S0 A^dagger S_{psi0}
        opS_psi0(*qreglist)
        opA_dagger(*qreglist)
        opS0(*qreglist)
        opA(*qreglist)

        self.envQ_ = env
