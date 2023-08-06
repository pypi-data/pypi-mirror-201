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
This module defines the LogNormal distribution class and related functions.
"""

import numpy as np
from scipy.stats import norm
from scipy.special import erf


class LogNormal:
    r"""
    This class defines the LogNormal distribution.

    X ~ LogNormal(:math:`\mu`, :math:`\sigma`) is often written as :math:`X \sim \exp(\mu + \sigma * Z)`,
    where Z ~ N(0, 1) is a standard normal distribution.

    :param mu: float, the mean of the distribution.
    :param sigma: float, the standard deviation of the distribution.
    """

    def __init__(self, mu: float, sigma: float):
        """
        Initialize the LogNormal distribution.

        X ~ LogNormal(mu, sigma) is often written as X ~ exp(mu + sigma * Z), where Z ~ N(0, 1).

        mu (float): The mean of the distribution.
        sigma (float): The standard deviation of the distribution.
        """
        self.mu_ = mu
        self.sigma_ = sigma
        self.num_sample_qubits_ = None
        self.num_grid_points_ = 0
        self.cutoff_min_ = np.maximum(0.0, self.mean - 3 * self.stddev)
        self.cutoff_max_ = self.mean + 3 * self.stddev

    def set_num_sample_qubits(self, num_sample_qubits):
        """
        Set the number of sample qubits.
        """
        self.num_sample_qubits_ = num_sample_qubits
        self.num_grid_points_ = 2 ** num_sample_qubits

    def sample(self, num_samples: int=10000) -> np.ndarray:
        """
        Sample from the LogNormal distribution.

        :param num_samples: int, the number of samples.

        :return: the samples.
        """
        return np.exp(self.mu_ + self.sigma_ * np.random.randn(num_samples))

    @property
    def cutoff_min(self) -> float:
        """
        The minimum value used in discrete probability distribution.
        """
        return self.cutoff_min_

    @cutoff_min.setter
    def cutoff_min(self, cutoff_min: float):
        """
        Set the minimum value used in discrete probability distribution.
        """
        self.cutoff_min_ = cutoff_min

    @property
    def cutoff_max(self) -> float:
        """
        The maximum value used in discrete probability distribution.
        """
        return self.cutoff_max_

    @cutoff_max.setter
    def cutoff_max(self, cutoff_max: float):
        """
        Set the maximum value used in discrete probability distribution.
        """
        self.cutoff_max_ = cutoff_max

    def discrete_pdf(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Calculate the discrete probability distribution.

        :return: the grid and the probability distribution.
        """
        grid = np.linspace(self.cutoff_min, self.cutoff_max, self.num_grid_points_)
        prob = self.pdf(grid)
        # Normalize the probability distribution, so that the sum of the probabilities is 1.
        prob /= np.sum(prob)
        return grid, prob

    def discrete_pdf_slanted(self, K: float) -> tuple[np.ndarray, np.ndarray]:
        r"""
        Calculate the discrete pdf function customized for :math:`\max\{S-K, 0\}`.

        Accumulate the probability mass of the grid points that are smaller than K.

        :param K: float, the strike price.
        :return: the grid and the probability distribution.
        """
        self.cutoff_min = max(K - self.stddev, 0)
        self.cutoff_max = self.cutoff_min + 6 * self.stddev
        grid = np.linspace(self.cutoff_min, self.cutoff_max, self.num_grid_points_)
        prob = [0] * self.num_grid_points_

        prob[0] = self.cdf(self.cutoff_min)
        # Calculate the probability of the grid points that are larger than K.
        for i in range(1, self.num_grid_points_):
            prob[i] = self.cdf(grid[i]) - self.cdf(grid[i - 1])

        # Normalize the probability distribution, so that the sum of the probabilities is 1.
        prob /= np.sum(prob)
        return grid, prob

    def pdf(self, x: float) -> float:
        """
        Calculate the probability density function of the distribution.

        :param x: The value of the random variable.
        :return: The probability density function of the distribution.
        """
        return np.exp(-0.5 * ((np.log(x) - self.mu_) / self.sigma_) ** 2) / (x * self.sigma_ * np.sqrt(2 * np.pi))

    def cdf(self, x: float) -> float:
        """
        Calculate the cumulative density function of the distribution.

        :param x: The value of the random variable.
        :return: The cumulative density function of the distribution.
        """
        return norm.cdf((np.log(x) - self.mu_) / self.sigma_)

    def inv_cdf(self, p: float) -> float:
        """
        Calculate the inverse cumulative density function of the distribution.

        :param p: float, the probability.

        :return: the inverse cumulative density function of the distribution.
        """
        return np.exp(self.mu_ + self.sigma_ * norm.ppf(p))

    def int_1st_moment(self, a: float, b: float) -> float:
        r"""
        Return the integration :math:`\int_a^b x p(x) dx`.

        :param a: float, The lower bound of the integration.
        :param b: float, The upper bound of the integration.

        :return: the integration function of x * pdf(x).
        """
        def orig(x):
            factor = -1 / 2 * np.exp(self.mu_ + self.sigma_ ** 2)
            return factor * erf(1 / (2 ** 0.5 * self.sigma_) * (self.mu_ + self.sigma_ ** 2 - np.log(x)))
        return orig(b) - orig(a)

    @property
    def mean(self) -> float:
        """
        Calculate the mean of the distribution.

        :return: The mean of the distribution.
        """
        return np.exp(self.mu_ + 0.5 * self.sigma_ ** 2)

    @property
    def variance(self) -> float:
        """
        Calculate the variance of the distribution.

        :return: The variance of the distribution.
        """
        return (np.exp(self.sigma_ ** 2) - 1) * np.exp(2 * self.mu_ + self.sigma_ ** 2)

    @property
    def stddev(self) -> float:
        """
        Calculate the standard deviation of the distribution.

        :return: The standard deviation of the distribution.
        """
        return np.sqrt(self.variance)

    @property
    def skewness(self) -> float:
        """
        Calculate the skewness of the distribution.

        :return: The skewness of the distribution.
        """
        return (np.exp(self.sigma_ ** 2) + 2) * np.sqrt(np.exp(self.sigma_ ** 2) - 1)
