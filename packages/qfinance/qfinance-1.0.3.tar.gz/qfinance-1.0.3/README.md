# QFinance

*Copyright (c) 2023 Institute for Quantum Computing, Baidu Inc. All Rights Reserved.*

## About QFinance

**QFinance** is a Quantum Finance library based on the [QCompute](https://github.com/baidu/QCompute) SDK. It provides a set of tools for building quantum algorithms for finance. Currently, it supports the following features:
* Pricing European options using Quantum Monte Carlo method
* Pricing European options using classical methods, including
    + Black-Scholes-Merton method
    + Classical Monte Carlo method

The following quantum algorithms are implemented in **QFinance**:
* Quantum Monte Carlo algorithm for simple piecewise linear payoff function
* Arbitrary quantum state preparation
* Quantum Fourier transform
* Quantum phase estimation
* Quantum amplitude estimation algorithms:
    + Canonical Quantum Amplitude Estimation [[Brassard 2002](http://arxiv.org/abs/quant-ph/0005055)]
    + Maximum Likelihood Amplitude Estimation [[Suzuki 2019](http://arxiv.org/abs/1904.10246)]
    + Iterative Quantum Amplitude Estimation [[Grinko 2019](http://arxiv.org/abs/1912.05559)]


## Installation
QFinance is available on PyPI. To install the latest release, run:

```bash
pip install qfinance
```
**pip** will handle all dependencies automatically.

## Examples

### Option Pricing

```python
import QCompute
QCompute.Define.Settings.outputInfo = False
from QFinance.pricing import EuropeanOptionPricingClassical, EuropeanCallQMC

# set parameters
# s0 is the current price of the underlying asset
# k is the strike price
# t is the time to maturity (in years)
# r is the risk-free interest rate
# sigma is the volatility of the underlying asset
s0 = 100
k = 90
t = 1
r = 0.05
sigma = 0.1

########################################################################################

option_classical = EuropeanOptionPricingClassical(s0, k, t, r, sigma, "call", "long")

# option price calculated by Black-Scholes-Merton model
bsm_price = option_classical.bsm_price()

option_classical.set_CMC_sample_size(1000000)
# option price calculated by Classical Monte Carlo method
cmc_price = option_classical.cmc_price()

option_classical.show_info()

########################################################################################

option = EuropeanCallQMC(s0, k, t, r, sigma)
option.set_num_qubits(3)
option.set_scaling(0.04)

# set MLAE configuration
option.method = "MLAE"
Q_powers = [2, 3, 5, 10]
shots = [100000] * len(Q_powers)
price_qmc = option.get_price_mlae(Q_powers, shots)

print(f"BSM price: \t{bsm_price:.5f}")
print(f"CMC price: \t{cmc_price:.5f}")
print(f"QMC price: \t{price_qmc:.5f}")

```

The typical output is as follows:

```bash
European option pricing with the following parameters:
option type:                    call, long
current stock price:            s0 = 100  
strike price:                   k = 90    
time to maturity (in years):    t = 1
risk-free interest rate:        r = 0.05
volatility:                     sigma = 0.1


=================== Running MLAE algorithm ======================
powers of Q are: [2, 3, 5, 10]
number of shots are: [100000, 100000, 100000, 100000]

Applying Q^2 to the state A|0>^8...
Time elapsed: 0.2348 seconds.

Applying Q^3 to the state A|0>^8...
Time elapsed: 0.3460 seconds.

Applying Q^5 to the state A|0>^8...
Time elapsed: 0.5540 seconds.

Applying Q^10 to the state A|0>^8...
Time elapsed: 1.0420 seconds.
===================== MLAE algorithm finished. ====================

BSM price:      14.62884
CMC price:      14.62937
QMC price:      14.62056

```

## License

QFinance uses the [Apache License 2.0](https://github.com/Qiskit/qiskit-finance/blob/main/LICENSE.txt).