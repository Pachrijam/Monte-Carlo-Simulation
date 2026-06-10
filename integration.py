import numpy as np

def monte_carlo_integration(func, a, b, n):
    # Generate n random samples between a and b
    x = np.random.uniform(a, b, n)

    # Evaluate the function at the random samples.
    # If func only accepts scalars, fall back to elementwise evaluation.
    try:
        fx = func(x)
    except TypeError:
        fx = np.array([func(xi) for xi in x], dtype=float)

    # Calculate the average value of the function at the random samples
    average_fx = np.mean(fx)

    # Estimate the integral as the average value times the width of the interval
    integral_estimate = (b - a) * average_fx

    return integral_estimate