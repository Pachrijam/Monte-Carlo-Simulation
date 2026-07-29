from __future__ import annotations
import math
import numpy as np
from typing import Tuple
from utils.export_csv import european_option_results_csv
from utils.export_json import european_option_results_json


def run_european() -> None:
    print("You have selected option 10: European Option Pricing (Black-Scholes Monte Carlo).\n------------------------------------------------------------------------")

    def _read_float(prompt: str, positive: bool = False) -> float:
        while True:
            try:
                v = float(input(prompt))
                if positive and v <= 0:
                    print("Please enter a positive value.")
                    continue
                return v
            except ValueError:
                print("Invalid number, please try again.")

    S0 = _read_float("Enter initial stock price S0 (e.g., 100): ", positive=True)
    K = _read_float("Enter strike price K (e.g., 100): ", positive=True)
    T = _read_float("Enter time to maturity T in years (e.g., 1): ", positive=True)
    r = _read_float("Enter risk-free rate r as decimal (e.g., 0.01): ")
    sigma = _read_float("Enter volatility sigma as decimal (e.g., 0.2): ", positive=True)

    option: str = "call"
    opt_input = input("Enter option type ('call' or 'put') [call]: ").strip().lower()
    if opt_input in ['call', 'put']:
        option = opt_input

    try:
        n_sim = int(input("Enter number of Monte Carlo simulations (n_sim) [20000]: "))
    except Exception:
        n_sim = 20000
    if n_sim <= 0:
        n_sim = 20000

    antithetic = input("Use antithetic variates? (yes/no) [no]: ").strip().lower() in ['yes', 'y']
    control_variate = input("Use control variate? (yes/no) [no]: ").strip().lower() in ['yes', 'y']
    seed_input = input("Enter random seed (integer) or leave blank for random: ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None

    mc_price, mc_se = monte_carlo_european(S0, K, T, r, sigma, option=option, n_sim=n_sim, antithetic=antithetic, control_variate=control_variate, seed=seed)
    bs_price = black_scholes_price(S0, K, T, r, sigma, option)

    print(f"------------------------------------------------------\nMonte Carlo estimated price: {mc_price} (SE: {mc_se})")
    print(f"Black-Scholes closed-form price: {bs_price}")
    export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the European option results? (yes/no): ")).lower()
    if export_choice in ['yes', 'y']:
        european_option_results_json(S0, K, T, r, sigma, n_sim, mc_price)
        european_option_results_csv(S0, K, T, r, sigma, n_sim, mc_price)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black_scholes_price(S: float, K: float, T: float, r: float, sigma: float, option: str = "call") -> float:
    if T <= 0:
        if option == "call":
            return max(S - K, 0.0)
        return max(K - S, 0.0)

    if sigma <= 0:
        F = S * math.exp(r * T)
        disc = math.exp(-r * T)
        if option == "call":
            return disc * max(F - K, 0.0)
        return disc * max(K - F, 0.0)

    sqrtT = math.sqrt(T)
    d1 = (math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT

    if option == "call":
        return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)
    else:
        return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def monte_carlo_european(
    S0: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option: str = "call",
    n_sim: int = 20000,
    antithetic: bool = False,
    control_variate: bool = False,
    seed: int | None = None,
) -> Tuple[float, float]:
    
    rng = np.random.default_rng(seed)
    
    drift = (r - 0.5 * sigma * sigma) * T
    vol = sigma * math.sqrt(max(T, 0.0))
    discount = math.exp(-r * T)

    if antithetic:
        half = (n_sim + 1) // 2
        z = rng.standard_normal(half)
        st1 = S0 * np.exp(drift + vol * z)
        st2 = S0 * np.exp(drift - vol * z)
        if option == "call":
            p1 = np.maximum(st1 - K, 0.0)
            p2 = np.maximum(st2 - K, 0.0)
        else:
            p1 = np.maximum(K - st1, 0.0)
            p2 = np.maximum(K - st2, 0.0)
        payoffs = (p1 + p2) * 0.5
        controls = (st1 + st2) * 0.5 if control_variate else None
    else:
        z = rng.standard_normal(n_sim)
        st = S0 * np.exp(drift + vol * z)
        if option == "call":
            payoffs = np.maximum(st - K, 0.0)
        else:
            payoffs = np.maximum(K - st, 0.0)
        controls = st if control_variate else None
 
    m = payoffs.size
    denom = (m - 1) if m > 1 else 1

    if control_variate and controls is not None:
        EX = S0 * math.exp(r * T)
        meanX = controls.mean()
        meanY = payoffs.mean()
        cov = np.sum((controls-meanX) * (payoffs - meanY)) / denom
        varX = np.sum((controls-meanX) **2) / denom
        b = cov / varX if varX > 0 else 0.0
        adjusted = payoffs - b * (controls - EX)
        avg_payoff = adjusted.mean()
        var_adj = np.sum((adjusted - avg_payoff) ** 2) / denom
        stderr = math.sqrt(var_adj / m) * discount
    else:
        avg_payoff = payoffs.mean()
        var_pay = np.sum((payoffs - avg_payoff) ** 2) / denom
        stderr = math.sqrt(var_pay / m) * discount

    price = discount * avg_payoff
    return float(price), float(stderr)
