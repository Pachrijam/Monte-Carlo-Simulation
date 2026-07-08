import math
import numpy as np

# TODO: validate these functions and ensure they are correct for rare event probability estimation


def estimate_tail_probability_naive():
    # Number of samples for naive Monte Carlo
    n_samples = 1000000
    # Generate samples from standard normal distribution
    samples = np.random.normal(0, 1, n_samples)
    # Count how many samples are greater than 3 (tail event)
    tail_count = np.sum(samples > 3)
    # Estimate the tail probability
    tail_probability = tail_count / n_samples
    return tail_probability

def importance_sampling_normal_tail():
    # Number of samples for importance sampling
    n_samples = 1000000
    # Generate samples from the importance distribution (shifted normal)
    samples = np.random.normal(3, 1, n_samples)
    # Evaluate the importance weights
    weights = np.exp(-0.5 * (samples - 3)**2) / np.exp(-0.5 * samples**2)
    # Estimate the tail probability
    tail_probability = np.sum(weights * (samples > 3)) / np.sum(weights)
    return tail_probability

def cross_entropy_importance_sampling():
    # Number of samples for cross-entropy importance sampling
    n_samples = 1000000
    # Generate samples from the cross-entropy distribution
    samples = np.random.normal(3, 1, n_samples)
    # Evaluate the cross-entropy weights
    weights = np.exp(-0.5 * (samples - 3)**2) / np.exp(-0.5 * samples**2)
    # Estimate the tail probability
    tail_probability = np.sum(weights * (samples > 3)) / np.sum(weights)
    return tail_probability