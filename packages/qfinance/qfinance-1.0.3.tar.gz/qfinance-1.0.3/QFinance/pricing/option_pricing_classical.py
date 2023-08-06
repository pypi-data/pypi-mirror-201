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
This module include the classical methods to solve option pricing problems.
"""

import numpy as np
from scipy.stats import norm


class EuropeanOptionPricingClassical:
    """
    This is a conceptual class representing the European call/put option pricing problem.

    This class provides the classical methods to solve option pricing problems.
    The classical solver includes the Black-Scholes-Merton (BSM) model and classical Monte Carlo (CMC) method.

    :param s0: float, initial stock price
    :param k: float, strike price
    :param t: float, time to maturity (in years)
    :param r: float, risk-free interest rate
    :param sigma: float, volatility
    """

    def __init__(self,
                 s0: float = 1.0,
                 k: float = 1.0,
                 t: float = 1,
                 r: float = 0.05,
                 sigma: float = 0.2,
                 cp: str = 'call',
                 ls: str = 'long') -> None:
        """
        Construct the class.
        """
        self.s0_ = s0
        self.k_ = k
        self.t_ = t
        self.r_ = r
        self.sigma_ = sigma
        self.cp_ = cp
        self.ls_ = ls
        self.pricing_method_ = 'BSM'
        self.accepted_methods_ = ['BSM', 'CMC']
        self.CMC_sample_size_ = 100000
        self.confidence_radius_ = None
        self.init_check()

    def init_check(self) -> None:
        """
        Check that the parameters are valid.
        """
        self.check_call_put()
        self.check_long_short()
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

    def show_info(self):
        """
        Print the relevant information for the option pricing problem.
        """
        print("\nEuropean option pricing with the following parameters:")
        print(f"option type: \t\t\t{self.cp_}, {self.ls_}")
        print(f"current stock price: \t\ts0 = {self.s0}")
        print(f"strike price: \t\t\tk = {self.k}")
        print(f"time to maturity (in years): \tt = {self.t}")
        print(f"risk-free interest rate: \tr = {self.r}")
        print(f"volatility: \t\t\tsigma = {self.sigma}\n")

    def set_long_short(self, ls: str) -> None:
        """
        Set the option to long or short.

        :param ls: str, 'long' or 'short'
        """
        self.ls_ = ls
        self.check_long_short()

    def set_call_put(self, cp: str) -> None:
        """
        Set the option to call or put.

        :param cp: str, 'call' or 'put'
        """
        self.cp_ = cp
        self.check_call_put()

    def check_call_put(self) -> None:
        """
        Check if the option is 'call' or 'put'.
        """
        if self.cp_ != 'call' and self.cp_ != 'put':
            raise ValueError(f'The option must be call or put, but {self.cp_} is given.')

    def check_long_short(self) -> None:
        """
        Check if the option is long or short.
        """
        if self.ls_ != 'long' and self.ls_ != 'short':
            raise ValueError(f'The option must be long or short, but {self.ls_} is given.')

    def check_method(self) -> None:
        """
        Check if the method is BSM or CMC.
        """
        if self.pricing_method_ not in self.accepted_methods_:
            raise ValueError(f'The method must be BSM or CMC, but {self.pricing_method_} is given.')

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

        :param k: strike price of the option.
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

        :param t: time to maturity (in years).
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
        Return the volatility of the stock price.
        """
        return self.sigma_

    @sigma.setter
    def sigma(self, sigma: float) -> None:
        """
        Set the volatility of the stock price.

        :param sigma: volatility.
        """
        if sigma <= 0:
            raise ValueError(f'The volatility must be positive, but {sigma} is given.')
        self.sigma_ = sigma

    def set_pricing_method(self, method: str) -> None:
        """
        Set the method to solve the option pricing problem.

        The method can be either BSM or CMC.
        
        :param method: str, the method to solve the option pricing problem.
        """
        self.pricing_method_ = method
        self.check_method()

    def set_CMC_sample_size(self, sample_size: int) -> None:
        """
        Set the sample size of the classical Monte Carlo method.

        :param sample_size: int, the sample size of the classical Monte Carlo method.
        """
        if sample_size <= 0:
            raise ValueError(f'The sample size must be positive, but {sample_size} is given.')
        self.CMC_sample_size_ = sample_size

    @property
    def confidence_radius(self) -> float:
        """
        Return the confidence radius of the option price.

        The confidence radius is calculated by the classical Monte Carlo method.
        """
        if self.confidence_radius_ is None:
            raise ValueError('The confidence radius is not calculated yet.')
        return self.confidence_radius_

    def long_call_price_CMC(self) -> float:
        r"""
        Calculate the price of the European long call option, using classical Monte Carlo method.

        First, generate a sample of stock prices at maturity, then calculate the average of the discounted payoffs.
        The stock price at maturity :math:`s_T` is generated by the geometric Brownian motion,
        and follows a LogNormal distribution.
        The payoff is :math:`\max\{sT - k, 0\}`, where :math:`k` is the strike price.
        The discounted payoff is :math:`\exp(-r t) \max\{sT - k, 0\}`.
        """
        z = np.random.normal(0, 1, self.CMC_sample_size_)
        sT = self.s0 * np.exp((self.r - 0.5 * self.sigma ** 2) * self.t + self.sigma * np.sqrt(self.t) * z)
        sample = np.maximum(sT - self.k, 0)
        # calculate the standard deviation of the sample
        std = np.std(sample)
        self.confidence_radius_ = np.exp(-1 * self.r * self.t) * 1.96 * std / np.sqrt(self.CMC_sample_size_)
        return np.exp(-1 * self.r * self.t) * np.mean(sample)

    def long_call_price_BSM(self) -> float:
        """
        Calculate the price of the European long call option, using Black-Scholes-Merton formula directly.

        Reference: Section 15.8 of John Hull's book "Options, Futures, and Other Derivatives".
        """
        d1 = (np.log(self.s0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))
        d2 = d1 - self.sigma * np.sqrt(self.t)
        return self.s0 * norm.cdf(d1) - self.k * np.exp(-1 * self.r * self.t) * norm.cdf(d2)

    def long_call_price(self) -> float:
        """
        Return the price of the European long call option.
        """
        self.check_method()
        if self.pricing_method_ == 'BSM':
            return self.long_call_price_BSM()
        elif self.pricing_method_ == 'CMC':
            return self.long_call_price_CMC()

    def short_call_price(self) -> float:
        """
        Return the price of the European short call option.
        """
        return -self.long_call_price()

    def long_put_price(self) -> float:
        """
        Return the price of the European long put option.
        """
        return -self.long_call_price()

    def short_put_price(self) -> float:
        """
        Return the price of the European short put option.
        """
        return -self.long_put_price()

    def price(self) -> float:
        """
        Return the price of the European call/put option.
        """
        self.check_call_put()
        self.check_long_short()
        if self.cp_ == 'call':
            if self.ls_ == 'long':
                return self.long_call_price()
            else:
                return self.short_call_price()
        else:
            if self.ls_ == 'long':
                return self.long_put_price()
            else:
                return self.short_put_price()

    def bsm_price(self) -> float:
        """
        Obtain the price of the European call/put option, using BSM formula directly.
        """
        method_backup = self.pricing_method_
        self.pricing_method_ = 'BSM'
        price = self.price()
        self.pricing_method_ = method_backup
        return price

    def cmc_price(self) -> float:
        """
        Obtain the price of the European call/put option, using Classical Monte Carlo method.
        """
        method_backup = self.pricing_method_
        self.pricing_method_ = 'CMC'
        price = self.price()
        self.pricing_method_ = method_backup
        return price

    def compare_prices(self) -> None:
        """
        Compare the prices of the European call/put option, as obtained from BSM and CMC.
        """
        method_backup = self.pricing_method_
        self.pricing_method_ = 'BSM'
        print(f'BSM price: {self.price():.5f}')
        self.pricing_method_ = 'CMC'
        print(f"CMC price: {self.price():.5f}",  u"\u00B1", f"{self.confidence_radius:.5f}")
        self.pricing_method_ = method_backup

    def long_call_delta_BSM(self) -> float:
        r"""
        Calculate the delta of the European long call option, using Black-Scholes-Merton formula directly.

        The delta of an option is the sensitivity of the option price to a change in the price of the underlying stock.
        
        .. math::

            \delta = \frac{\partial C}{\partial s} = N(d_1), \\
            d_1 = \frac{ln(s_0 / k) + (r + \sigma^2 / 2) t}{\sigma \sqrt{t}}
        """
        d1 = (np.log(self.s0 / self.k) + (self.r + 0.5 * self.sigma ** 2) * self.t) / (self.sigma * np.sqrt(self.t))
        return norm.cdf(d1)
