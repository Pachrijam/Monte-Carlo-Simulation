import numpy as np

def calculate_monte_carlo_integration(func, a, b, n):
    x = np.random.uniform(a, b, n)

    try:
        fx = func(x)
    except TypeError:
        fx = np.array([func(xi) for xi in x], dtype=float)

    average_fx = np.mean(fx)

    integral_estimate = (b - a) * average_fx

    return integral_estimate
