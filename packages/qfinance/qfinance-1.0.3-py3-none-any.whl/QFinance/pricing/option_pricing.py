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
This module defines the class for European call problem.

The class EuropeanCallQMC is defined in this module.
"""


import numpy as np
from scipy.stats import norm


from QFinance.pricing.lognormal import LogNormal
from QFinance.algorithms import SimpleQMC


class EuropeanCallQMC:
    r"""
    This is a conceptual class representation of European pricing problem using Quantum Monte Carlo method.

    The European call option pricing problem is defined by various parameters related to the option.
    The Quantum Monte Carlo method is controlled by the number of qubits and the scaling factor.

    :param s0: float, initial stock price
    :param k: float, strike price
    :param t: float, time to maturity (in years)
    :param r: float, risk-free interest rate
    :param sigma: float, volatility
    """

    def __init__(self, s0: float, k: float, t: float, r: float, sigma: float) -> None:
        """
        Construct the class.
        """
        self.s0_ = s0
        self.k_ = k
        self.t_ = t
        self.r_ = r
        self.sigma_ = sigma
        self.lognormal = None
        self.price_grid = None
        self.probs = None
        self.sqrt_probs = None
        self.numq = 3  # number of qubits to use
        self.qmc = None
        self.ae_problem = None
        self.method = "MLAE"
        self.accepted_methods = ["MLAE", "IQAE"]
        self.mlae_config = None
        self.iqae_config = None

        self.scaling_ = 0.04
        self.exact_price_ = None

    def init_check(self) -> None:
        """
        Check that the parameters are valid.
        """
        if self.s0_ <= 0:
            raise ValueError(f'The initial stock price must be positive, but {self.s0_} is given.')
        if self.k_ <= 0:
            raise ValueError(f'The strike price must be positive, but {self.k_} is given.')
        if self.t_ <= 0:
            raise ValueError(f'The time to maturity must be positive, but {self.t_} is given.')
        if self.r_ <= 0:
            raise ValueError(f'The risk-free interest rate must be positive, but {self.r_} is given.')
        if self.sigma_ <= 0:
            raise ValueError(f'The volatility must be positive, but {self.sigma_} is given.')

    def check_method(self) -> None:
        """
        Check that the method is valid.
        """
        if self.method not in self.accepted_methods:
            raise ValueError(f'The method must be in {self.accepted_methods}, but {self.method} is given.')

    def show_info(self):
        """
        Print the relevant information for the option pricing problem.
        """
        print("\nEuropean call option pricing with the following parameters:")
        print(f"current stock price: \t\ts0 = {self.s0}")
        print(f"strike price: \t\t\tk = {self.k}")
        print(f"time to maturity (in years): \tt = {self.t}")
        print(f"risk-free interest rate: \tr = {self.r}")
        print(f"volatility: \t\t\tsigma = {self.sigma}\n")

    @property
    def exact_price(self) -> float:
        """
        Return the exact price of the option.
        """
        if self.exact_price_ is None:
            self.exact_price_ = self.calc_exact_price()
        return self.exact_price_

    @property
    def s0(self) -> float:
        """
        Return the initial stock price.
        """
        return self.s0_

    @s0.setter
    def s0(self, s0: float) -> None:
        """
        Set the initial stock price.

        :param s0: initial stock price.
        """
        if s0 <= 0:
            raise ValueError(f'The initial stock price must be positive, but {s0} is given.')
        self.s0_ = s0

    @property
    def k(self) -> float:
        """
        Return the strike price.
        """
        return self.k_

    @k.setter
    def k(self, k: float) -> None:
        """
        Set the strike price.

        :param k: strike price
        """
        if k <= 0:
            raise ValueError(f'The strike price must be positive, but {k} is given.')
        self.k_ = k

    @property
    def t(self) -> float:
        """
        Return the time to maturity (in years).
        """
        return self.t_

    @t.setter
    def t(self, t: float) -> None:
        """
        Set the time to maturity (in years).

        :param t: time to maturity
        """
        if t <= 0:
            raise ValueError(f'The time to maturity must be positive, but {t} is given.')
        self.t_ = t

    @property
    def r(self) -> float:
        """
        Return the risk-free interest rate.
        """
        return self.r_

    @r.setter
    def r(self, r: float) -> None:
        """
        Set the risk-free interest rate.

        :param r: risk-free interest rate.
        """
        if r <= 0:
            raise ValueError(f'The risk-free interest rate must be positive, but {r} is given.')
        self.r_ = r

    @property
    def sigma(self) -> float:
        """
        Return the volatility.
        """
        return self.sigma_

    @sigma.setter
    def sigma(self, sigma: float) -> None:
        """
        Set the volatility.

        :param sigma: volatility
        """
        if sigma <= 0:
            raise ValueError(f'The volatility must be positive, but {sigma} is given.')
        self.sigma_ = sigma

    def set_num_qubits(self, num_qubits: int) -> None:
        """
        Set the number of qubits to use.

        :param num_qubits: int, number of qubits to use
        """
        self.numq = num_qubits
        # update price_grid and sqrt_probs
        self.get_log_normal()

    def set_scaling(self, scaling: float) -> None:
        """
        Set the scaling factor for the payoff function.

        :param scaling: float, the scaling factor
        """
        # check that scaling is in appropriate range
        if scaling <= 1E-3:
            raise ValueError(f'The scaling factor must be greater than 1E-3, but {scaling} is given.')
        if scaling >= 0.5:
            raise ValueError(f'The scaling factor is too large, {scaling} is given.')
        self.scaling_ = scaling

    def calc_exact_price(self) -> float:
        """
        Calculate the exact price of the option.

        The exact price is calculated using the Black-Scholes-Merton formula.

        :return: the exact price of the option
        """
        d1 = (np.log(self.s0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))
        d2 = d1 - self.sigma * np.sqrt(self.t)
        return self.s0 * norm.cdf(d1) - self.k * np.exp(-1 * self.r * self.t) * norm.cdf(d2)

    def get_log_normal(self) -> LogNormal:
        r"""
        Get the desired log-normal distribution, which is the distribution of the stock price.

        The price of the stock at maturity is log-normally distributed.

        .. math::
            s_T = s_0 \exp\left((r - \frac{1}{2}\sigma^2)t + \sigma\sqrt{t}Z\right) \\
            s_T \sim \text{LogNormal}\left((r - \frac{1}{2}\sigma^2)t, \quad \sigma\sqrt{t}\right)

        :return: the desired log-normal distribution
        """
        LNmu = (self.r_ - 0.5 * self.sigma_ ** 2) * self.t_ + np.log(self.s0_)
        LNsigma = self.sigma_ * np.sqrt(self.t_)
        self.lognormal = LogNormal(LNmu, LNsigma)
        self.lognormal.set_num_sample_qubits(self.numq)

        price_grid, self.probs = self.lognormal.discrete_pdf()

        self.price_grid = price_grid
        self.sqrt_probs = np.sqrt(self.probs)
        return self.lognormal

    def calc_grid_expectation(self) -> float:
        """
        Calculate the theoretical expectation of the payoff function.

        The theoretical expectation value is coarse-grained by the price grid.

        :return: the grid expectation.
        """
        payoff = np.maximum(self.price_grid - self.k_, 0)
        grid_expectation = np.sum(payoff * self.probs)
        return grid_expectation

    def calc_grid_P1(self) -> float:
        r"""
        Calculate the theoretical probability :math:`P_1`.
        
        :math:`P_1` is the probability of measuring :math:`1` in the last qubit.
        The grid :math:`P_1` is the obtained from the grid expectation.
        The grid :math:`P_1` will be compared against the measured amplitude.

        :return: the grid probability.
        """
        s = self.qmc.pwl.scaling_
        ymin = self.qmc.pwl.ymin
        ymax = self.qmc.pwl.ymax
        grid_expectation = self.calc_grid_expectation()
        slope = 2 * s / (ymax - ymin)
        intercept = 1 / 2 - s * (2 * ymin / (ymax - ymin) + 1)
        grid_P1 = slope * grid_expectation + intercept
        print(f"The linear transform is P1 = {slope:.5e} * Exp + {intercept:.5e}.\n")
        return grid_P1

    def reduce_to_aep(self) -> None:
        """
        Reduce the European call problem to amplitude estimation problem.
        """
        # step1: create the QMC object
        self.qmc = SimpleQMC(self.numq)

        # step2: load the LogNormal distribution
        dist = self.sqrt_probs
        self.qmc.load_dist(dist)

        # step3: set the payoff function
        price_min = self.price_grid[0]
        price_max = self.price_grid[-1]
        domain = (price_min, price_max)
        # check that the strike price is within the domain of the price grid
        assert self.k_ >= price_min and self.k_ <= price_max, "The strike price is out of the domain of the price grid."
        self.qmc.set_linear(domain, self.k_)
        if self.scaling_ is not None:
            self.qmc.set_scaling(self.scaling_)

    def get_price(self) -> float:
        r"""
        Obtain the option price.

        The option price is given by :math:`e^{-rT} E[\max\{0, sT - k\}]`.

        :return: the option price
        """
        if self.ae_problem is None:
            self.reduce_to_aep()

        if self.method == "MLAE":
            self.measured_expectation = self.qmc.run_mlae_demo()
        elif self.method == "IQAE":
            self.measured_expectation = self.qmc.run_iqae()
        self.measured_P1 = self.qmc.measured_P1
        self.measured_price = np.exp(-self.r_ * self.t_) * self.measured_expectation

        return self.measured_price

    def get_price_mlae(self, 
                       Q_powers: list[int], 
                       shots: list[int], 
                       precision: float=1E-4) -> float:
        """
        Obtain the option price using MLAE method in the amplitude estimation.

        :param Q_powers: A list of the powers of Q.
        :param shots: The number of shots for each power of Q.
        :param precision: The precision of the expectation value, default is 1E-4.

        :return: The option price.
        """
        if self.ae_problem is None:
            self.reduce_to_aep()

        self.measured_expectation = self.qmc.run_mlae(Q_powers, shots, precision)

        self.measured_P1 = self.qmc.measured_P1
        self.measured_price = np.exp(-self.r_ * self.t_) * self.measured_expectation

        return self.measured_price
