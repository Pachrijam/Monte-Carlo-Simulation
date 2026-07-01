```python
from simulations.european_options import monte_carlo_european, black_scholes_price

S0 = 100.0
K = 100.0
T = 1.0
r = 0.01
sigma = 0.2

mc_price, mc_se = monte_carlo_european(S0, K, T, r, sigma, option='call', n_sim=20000, seed=0)
print('MC price:', mc_price, 'SE:', mc_se)

mc_a, se_a = monte_carlo_european(S0, K, T, r, sigma, option='call', n_sim=20000, antithetic=True, seed=0)
print('Antithetic price:', mc_a, 'SE:', se_a)

mc_cv, se_cv = monte_carlo_european(S0, K, T, r, sigma, option='call', n_sim=20000, control_variate=True, seed=0)
print('Control variate price:', mc_cv, 'SE:', se_cv)

bs = black_scholes_price(S0, K, T, r, sigma, 'call')
print('Black-Scholes:', bs)
```
