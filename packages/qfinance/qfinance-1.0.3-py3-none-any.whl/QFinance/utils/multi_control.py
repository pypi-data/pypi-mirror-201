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
This module defines the multi-control gates CnX and CnZ.

The multi-control gates CnX and CnZ are defined in this module. However, the decomposition method is not optimized.
"""


from QCompute import *
import numpy as np


def cnx(n: int, env: QEnv) -> QEnv:
    r"""
    Apply multi-controlled-NOT gate to env.

    The circuit has :math:`n + 1` qubits in total.
    The first :math:`n` qubits are controlling qubits, the last qubit is the target qubit.

    Attention! This decomposition method requires exponential number of gates and is for test only:

    .. math::
        f(n) = 2 \times f(n-1) + C  \rightarrow f(n) = 2^n * C

    :param n: int, the number of controlling qubits, the circuit has :math:`n+1` qubits in total.
    :param env: QEnv, the environment to apply the CnX gate.

    :return: QEnv, the environment after applying the CnX gate.

    :raise ValueError: if n is not a nonnegative integer.

    **Example**

        >>> cnx(2)
    """
    q = env.Q

    if n == 0:
        X(q[0])
    elif n == 1:
        CX(q[0], q[1])
    elif n == 2:
        CCX(q[0], q[1], q[2])
    elif n >= 2:
        SWAP(q[n-1], q[n])
        CRZ(np.pi/2)(q[n], q[n-1])
        CU(np.pi/2, 0, 0)(q[n], q[n-1])
        env = cnx(n-1, env)
        CU(-np.pi/2, 0, 0)(q[n], q[n-1])
        env = cnx(n-1, env)
        CRZ(-np.pi/2)(q[n], q[n-1])
        SWAP(q[n-1], q[n])
    else:
        raise ValueError("n must be a nonnegative integer")
    return env


def cnz(n: int, env: QEnv) -> QEnv:
    r"""
    Apply multi-Controlled-Z gate to env.

    The circuit has :math:`n + 1` qubits in total.
    The first :math:`n` qubits are controlling qubits, the last qubit is the target qubit.

    :param n: int, the number of controlling qubits, the circuit has :math:`n+1` qubits in total.
    :param env: QEnv, the environment to apply the CnX gate.

    :return: QEnv, the environment after applying the CnX gate.

    :raise ValueError: if n is not a nonnegative integer.

    **Example**

        >>> cnz(2)
    """
    q = env.Q

    if n == 0:
        Z(q[0])
    elif n == 1:
        CZ(q[0], q[1])
    elif n >= 2:
        H(q[n])
        env = cnx(n, env)
        H(q[n])
    else:
        raise ValueError("n must be a nonnegative integer")
    return env

    # TODO: change to an optimized version of CnX and CnZ
