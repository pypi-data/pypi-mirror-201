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
This module defines the help functions associated to QRegPool class.

The functions defined in this module are used to help the user to get the qubits in a given slice of a QRegPool.
"""

from QCompute.QPlatform.QRegPool import QRegPool


def sub_qreg(qreg: QRegPool, start: int, num: int):
    r"""
    Obtain a list of qubits in a given slice of :class:`QRegPool`.

    For a given slice, return a list of :class:`QRegStorage` with the qubits in the given slice.
    
    :param qreg: QRegPool, the quantum register
    :param start: int, the start index of the slice
    :param num: int, the number of qubits contained in the slice

    :return: list, a list of QRegStorage with the qubits in the given slice

    **Example**

        >>> sub_qreg(qreg, 0, 2)
    """
    if start is None:
        start = 0

    dic = qreg.registerMap

    sublist = []
    for k, v in dic.items():
        if start <= k < start + num:
            sublist.append(v)
    return sublist


def sub_qreg_slice(qreg: QRegPool, start: int, end: int):
    r"""
    Obtain a list of qubits in a given slice of :class:`QRegPool`.

    For a given slice, return a list of :class:`QRegStorage` with the qubits in the given slice.
    
    :param qreg: QRegPool, the quantum register
    :param start: int, the start index of the slice
    :param end: int, the end index of the slice

    :return: list, a list of QRegStorage with the qubits in the given slice

    **Example**

        >>> sub_qreg(qreg, 0, 2)
    """
    dic = qreg.registerMap

    sublist = []
    for k, v in dic.items():
        if start <= k < end:
            sublist.append(v)
    return sublist


def full_qreg(qreg: QRegPool) -> list:
    r"""
    Obtain the list of all the qubits in a given :class:`QRegPool`.

    For a given :class:`QRegPool`, return a list of :class:`QRegStorage` with all the qubits in the :class:`QRegPool`.

    :param qreg: QRegPool, the quantum register

    :return: list, a list of QRegStorage with all the qubits in the :class:`QRegPool`
    """
    return list(qreg.registerMap.values())
