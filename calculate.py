import random

def percent_error(num_samples):
    pi_estimate = monte_carlo_pi(num_samples)
    error = abs(pi_estimate - 3.141592653589793)
    return (error / 3.141592653589793) * 100

def monte_carlo_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate