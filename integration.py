import numpy as np
def monte_carlo_integration(func, a, b, n):
    # Generate n random samples between a and b
    x = np.random.uniform(a, b, n)
    
    # Evaluate the function at the random samples
    fx = func(x)
    
    # Calculate the average value of the function at the random samples
    average_fx = np.mean(fx)
    
    # Estimate the integral as the average value times the width of the interval
    integral_estimate = (b - a) * average_fx
    
    return integral_estimate