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
This module implements the piecewise linear function operator.

Reference: http://arxiv.org/abs/1905.02666
"""

from QCompute import *
from QCompute.QPlatform.QRegPool import QRegStorage
from QFinance.algorithms import QuantumComparatorOP

import numpy


def CCRY(c1: QRegStorage, c2: QRegStorage, t: QRegStorage, theta: float) -> None:
    """
    Apply the controlled-controlled-RY gate.

    Decomposition details can be found in figure 4.8 of Nielsen-Chuang.

    :param c1: the control qubit 1
    :param c2: the control qubit 2
    :param t: the target qubit
    :param theta: the rotation angle
    """
    CRY(theta / 2)(c2, t)
    CX(c1, c2)
    CRY(-theta / 2)(c2, t)
    CX(c1, c2)
    CRY(theta / 2)(c1, t)


class SimplePiecewiseLinear:
    r"""
    This class implements the ad hoc piecewise linear function operator.

    This specific piecewise linear function has the form of 
    
    .. math::
        f(x) = \max\{0, x - x_k\}.
    
    The domain is :math:`[x_{min}, x_{max}]`, discretized into math:`2^n` grid points, and
    :math:`x_k` is the value corresponding to the k-th grid point.

    :param domain: the domain :math:`[x_{min}, x_{max}]` of the function
    :param num: the number of qubits, i.e., there're :math:`2^{\text{num}}` grid points
    :param xk: the value corresponding to the :math:`k`-th grid point
    """

    def __init__(self, domain: tuple[float, float], num: int, xk: float):
        """
        Define the piecewise linear function f(x) = max{0, x - xk}.

        :param domain: the domain [xmin, xmax] of the function
        :param num: the number of qubits, i.e., there're 2^num grid points
        :param xk: the value corresponding to the k-th grid point
        """
        self.domain = domain
        self.xmin, self.xmax = domain
        self.num = num
        self.xk = xk
        self.ymin = self.xmin - self.xk
        self.ymax = self.xmax - self.xk
        self.K = self.findK()
        self.scaling_ = 0.1

        self.working_qregL = None
        self.ancillary_qregL = None
        self.compare_qreg = None
        self.angle_qreg = None

    @property
    def scaling(self) -> float:
        r"""
        The scaling factor :math:`s`.
        """
        return self.scaling_

    @scaling.setter
    def scaling(self, s: float) -> None:
        """
        Set the scaling factor :math:`s`.

        :param s: the scaling factor :math:`s`.
        """
        self.scaling_ = s

    def fhat(self, i: int) -> float:
        r"""
        Return the rescaled linear function :math:`\hat{f}`.
         
        The function :math:`\hat{f}` is obtained from the original
        linear function :math:`f(x) = x - x_k`.

        Transform the domain from :math:`x` to :math:`i`:

        .. math::
            \hat{f} = 2 (f(x(i)) - c)/(d-c) - 1

        :param i: int, the i-th grid point.
        
        :return: float, the slope of the piecewise linear function.
        """
        def i_to_x(i):
            return self.xmin + (self.xmax - self.xmin) / (2 ** self.num - 1) * i

        def f(x):
            return x - self.xk

        def image_rescale(y):
            return 2 * (y - self.ymin) / (self.ymax - self.ymin) - 1

        return image_rescale(f(i_to_x(i)))

    def angle_g0(self) -> float:
        r"""
        Return the angle :math:`g_0` in the reference.

        .. math::
            g_0 = \pi/4 - s * (2c/(d-c) + 1)
        """
        return numpy.pi / 4 - self.scaling_ * (2 * self.ymin / (self.ymax - self.ymin) + 1)

    def angle_h(self, i: int) -> float:
        r"""
        Return the angle :math:`h(i)`.

        h(i) = s*\hat{f}(i) + \pi/4 - g_0

        :param i: int, the :math:`i`-th grid point.
        """
        return self.scaling_ * self.fhat(i) + numpy.pi / 4 - self.angle_g0()

    def angle_h_slope_intersect(self) -> tuple[float, float]:
        r"""
        Return the slope and intersect of the function :math:`h(i)`.
        """
        # 1.0 is the slope of f(x) = x - xk
        h1 = 2 * self.scaling_ / (self.ymax - self.ymin) * 1.0 * (self.xmax - self.xmin) / (2 ** self.num - 1)
        h0 = 2 * self.scaling_ / (self.ymax - self.ymin) * (self.xmin * 1.0 - self.xk)
        return h1, h0

    def findK(self) -> int:
        r"""
        Find the :math:`k`-th grid point corresponding to :math:`x_k`.

        The :math:`0`-th grid point corresponds to :math:`x_{min}`,
        and the :math:`(2^{num}-1)`-th grid point corresponds to :math:`x_{max}`.

        The returned :math:`k` will be the classical value to be compared in the quantum comparator.

        :return: int, the value :math:`k` where the :math:`k`-th grid point corresponding to :math:`x_k`.
        """
        xmin, xmax = self.domain
        K = numpy.ceil((self.xk - xmin) / (xmax - xmin) * (2 ** self.num - 1))
        return int(K)

    def measured_exp_from_P1(self, measured_P1: float) -> float:
        r"""
        Return the original expectation `p_orig`.

        The original exectation
        :math:`p_{orig} = sum_{i=0}^{2^n-1} p(i) * f(x(i))`
        is related to the measured probability :math:` p_{measured}` by

        .. math::
            p_{measured} = 2s/(d-c) * p_{orig} + 1/2 -s(2c/(d-c) + 1))

        :param measured_P1: float, the measured probability of the qubit being in the :math:`\left|1\right>` state.
        :return: the expectation of the original function.
        """
        numerator = measured_P1 - 1 / 2 + self.scaling_ * (2 * self.ymin / (self.ymax - self.ymin) + 1)
        denominator = 2 * self.scaling_ / (self.ymax - self.ymin)
        return numerator / denominator

    def apply_to(self,
                 working_qregL: list[QRegStorage],
                 ancillary_qregL: list[QRegStorage],
                 comp: QRegStorage, angle: QRegStorage):
        """
        Apply the quantum piecewise linear function to the working qubits.
        
        :param working_qregL: the working qubits
        :param ancillary_qregL: the ancillary qubits, used in quantum parator
        :param comp: the qubit used to store the comparison result
        :param angle: the angle qubit, whose amplitude will be measured
        """
        self.working_qregL = working_qregL
        self.ancillary_qregL = ancillary_qregL
        self.compare_qreg = comp
        self.angle_qreg = angle

        # check that num_working is equal to num_ancillary, and is equal to self.num
        if len(self.working_qregL) != self.num:
            raise ValueError("The number of working qubits is not equal to num")

        if len(self.ancillary_qregL) != self.num:
            raise ValueError("The number of ancillary qubits is not equal to num")

        # apply the quantum comparator
        comparator = QuantumComparatorOP(self.num, self.K)
        comparator(self.working_qregL, self.ancillary_qregL, self.compare_qreg, True)
        # TODO: set self.angle_qreg to any of the ancillary qubits
        # if one wants to save 1 qubit

        # apply RY(2 g0) to the angle qubit
        g0 = self.angle_g0()
        g0_eff = 2 * g0
        RY(g0_eff)(self.angle_qreg)

        # implement effective CRY(2 h(i))
        h1, h0 = self.angle_h_slope_intersect()
        h0_eff = 2 * h0
        h1_eff = 2 * h1

        CRY(h0_eff)(self.compare_qreg, self.angle_qreg)

        for i in range(self.num):
            angle_i = 2 ** (self.num - 1 - i) * h1_eff
            CCRY(self.working_qregL[i], self.compare_qreg, self.angle_qreg, angle_i)
