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
This module contains functions that deal with the measurement results.
"""


def parse_bit_string(bit_string: str) -> int:
    r"""
    Parse the bit string to an integer.

    + Step 1: reverse the bit string
    + Step 2: convert the reversed bit string to an integer

    QCompute uses big-endian, if the measument of `MeasureZ([q[0], q[1], q[2]], [0, 1, 2])` is '110',
    this means `q[0]=0, q[1]=1, q[2]=1`.
    Use the convention that `q[0]` is the most significant bit, `q[2]` is the least significant bit.
    Return an integer.

    :param bit_string: a string of `0` s and `1` s, e.g., '110'

    :return: Integer

    **Example**
    
        >>> parse_bit_string('110')
    """
    reversed_bit_string = bit_string[::-1]
    return int(reversed_bit_string, 2)


def parse_counts_dict_to_int(counts_dict: dict) -> dict:
    r"""
    Parse the counts dict to obtain a new dict, where the key is an integer.

    For each item in the count_dict, the key is the bit string, the value is the number of occurrences.
    This function converts the key of count_dict to an integer.

    :param counts_dict: dict, the counts dict where the key is the bit string, the value is the number of occurrences.

    :return: dict, the parsed counts dict where the key is an integer.

    **Example**

        >>> task_result = env.commit(shots)
        >>> counts_dict = task_result['counts']
        >>> parse_counts_dict_to_int(counts_dict)
    """
    new_count_dict = {}
    for k, v in counts_dict.items():
        new_count_dict[parse_bit_string(k)] = v
    return new_count_dict


def parse_counts_dict_to_float(counts_dict: dict, n: int) -> dict:
    r"""
    Parse the counts dict to obtain a new dict, where the key is a float.

    The argument count_dict is obtained from the measured result as follows:

    >>> task_result = env.commit(shots)
    >>> count_dict = task_result['counts']

    For each item in the count_dict, the key is the bit string, the value is the number of occurrences.
    This function converts the key of count_dict to an integer, and then divides it by :math:`2^n`.

    :param counts_dict: dict, the counts dict where the key is the bit string, the value is the number of occurrences.
    :param n: int, the number of qubits

    :return: dict, the parsed counts dict where the key is a float.

    **Example**

        >>> task_result = env.commit(shots)
        >>> counts_dict = task_result['counts']
        >>> parse_counts_dict_to_float(counts_dict, n)
    """
    new_count_dict = {}
    for k, v in counts_dict.items():
        new_count_dict[parse_bit_string(k) / (2 ** n)] = v
    return new_count_dict


def parse_counts_dict_to_freq_list(counts_dict: dict, num_qubits: int, shots: int) -> list:
    r"""
    Parse the counts dict to obtain a list of frequencies.

    For each item in the count_dict, the key is the bit string, the value is the number of occurrences.
    This function converts the count of each bit string to the frequency: count/shots.
    The frequency is placed in the list according to the integer corresponding to the bit string.

    :param counts_dict: dict, the counts dict where the key is the bit string, the value is the number of occurrences.
    :param num_qubits: int, the number of qubits
    :param shots: int, the number of shots

    :return: list, the frequency list
    
    **Example**

        >>> task_result = env.commit(shots)
        >>> counts_dict = task_result['counts']
        >>> parse_counts_dict_to_freq_list(counts_dict, num_qubits, shots)
    """
    freq_list = [0.0] * (2 ** num_qubits)
    for k, v in counts_dict.items():
        freq_list[parse_bit_string(k)] = v / shots
    return freq_list


def extract_to_int_by_max(counts_dict: dict) -> int:
    r"""
    Extract the key for which the number of occurrences is the greatest.

    First  parse the counts_dict to a discrete distribution, where the key is an integer.
    Then extract the key for which the number of occurrences is the greatest.

    :param counts_dict: dict, the counts dict where the key is the bit string, the value is the number of occurrences.

    :return: int, the key for which the number of occurrences is the greatest, converted to an integer.

    **Example**

        >>> task_result = env.commit(shots)
        >>> counts_dict = task_result['counts']
        >>> extract_to_int_by_max(counts_dict)
    """
    new_count_dict = parse_counts_dict_to_int(counts_dict)
    k_max = 0
    v_max = 1
    for k, v in new_count_dict.items():
        if v > v_max:
            v_max = v
            k_max = k
    return k_max


def extract_to_float_by_max(counts_dict: dict, n: int) -> float:
    r"""
    Extract the key for which the number of occurrences is the greatest.

    First  parse the counts_dict to a discrete distribution, where the key is a float = integer/:math:`2^n`.
    Then extract the key for which the number of occurrences is the greatest.

    :param counts_dict: dict, the counts dict where the key is the bit string, the value is the number of occurrences.
    :param n: int, the number of qubits

    :return: float, the key for which the number of occurrences is the greatest, converted to a float.

    **Example**

        >>> task_result = env.commit(shots)
        >>> counts_dict = task_result['counts']
        >>> extract_to_float_by_max(counts_dict, n)
    """
    new_count_dict = parse_counts_dict_to_float(counts_dict, n)
    k_max = 0.0
    v_max = 1
    for k, v in new_count_dict.items():
        if v > v_max:
            v_max = v
            k_max = k
    return k_max
