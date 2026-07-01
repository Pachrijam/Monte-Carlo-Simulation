import math
from european_options import black_scholes_price, monte_carlo_european

def test_mc_close_to_bs_plain():
    S0 = 100.0
    K = 100.0
    T = 1.0
    r = 0.01
    sigma = 0.2
    seed = 12345
    bs_call = black_scholes_price(S0, K, T, r, sigma, "call")
    mc_price, mc_se = monte_carlo_european(S0, K, T, r, sigma, option="call", n_sim=20000, antithetic=False, control_variate=False, seed=seed)
    assert abs(mc_price - bs_call) < 4 * mc_se + 1e-8

def test_control_variate_improves_variance():
    S0 = 100.0
    K = 110.0
    T = 0.5
    r = 0.02
    sigma = 0.3
    seed = 54321
    bs_call = black_scholes_price(S0, K, T, r, sigma, "call")
    mc_plain, se_plain = monte_carlo_european(S0, K, T, r, sigma, option="call", n_sim=20000, antithetic=False, control_variate=False, seed=seed)
    mc_cv, se_cv = monte_carlo_european(S0, K, T, r, sigma, option="call", n_sim=20000, antithetic=False, control_variate=True, seed=seed)
    assert se_cv <= se_plain + 1e-12
    assert abs(mc_cv - bs_call) <= abs(mc_plain - bs_call) + 1e-12
