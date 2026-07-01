from __future__ import annotations

import math
import random
from typing import Tuple

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
    if seed is not None:
        random.seed(seed)

    drift = (r - 0.5 * sigma * sigma) * T
    vol = sigma * math.sqrt(max(T, 0.0))

    payoffs = []
    controls = []

    if antithetic:
        half = (n_sim + 1) // 2
        for _ in range(half):
            z = random.gauss(0.0, 1.0)
            st1 = S0 * math.exp(drift + vol * z)
            st2 = S0 * math.exp(drift - vol * z)
            if option == "call":
                p1 = max(st1 - K, 0.0)
                p2 = max(st2 - K, 0.0)
            else:
                p1 = max(K - st1, 0.0)
                p2 = max(K - st2, 0.0)
            payoffs.append((p1 + p2) / 2.0)
            if control_variate:
                controls.append((st1 + st2) / 2.0)
    else:
        for _ in range(n_sim):
            z = random.gauss(0.0, 1.0)
            st = S0 * math.exp(drift + vol * z)
            if option == "call":
                p = max(st - K, 0.0)
            else:
                p = max(K - st, 0.0)
            payoffs.append(p)
            if control_variate:
                controls.append(st)

    m = float(len(payoffs))
    avg_payoff = sum(payoffs) / m
    discount = math.exp(-r * T)

    if control_variate and len(controls) == m:
        EX = S0 * math.exp(r * T)
        X = controls
        Y = payoffs
        meanX = sum(X) / m
        meanY = sum(Y) / m
        cov = sum((xi - meanX) * (yi - meanY) for xi, yi in zip(X, Y)) / (m - 1 if m > 1 else 1)
        varX = sum((xi - meanX) ** 2 for xi in X) / (m - 1 if m > 1 else 1)
        b = cov / varX if varX > 0 else 0.0
        adjusted = [yi - b * (xi - EX) for xi, yi in zip(X, Y)]
        avg_payoff = sum(adjusted) / m
        var_adj = sum((z - avg_payoff) ** 2 for z in adjusted) / (m - 1 if m > 1 else 1)
        stderr = math.sqrt(var_adj / m) * discount
    else:
        var_pay = sum((z - avg_payoff) ** 2 for z in payoffs) / (m - 1 if m > 1 else 1)
        stderr = math.sqrt(var_pay / m) * discount

    price = discount * avg_payoff
    return price, stderr
