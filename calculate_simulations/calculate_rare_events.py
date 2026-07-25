import math
import numpy as np

def estimate_tail_probability_naive(threshold, n_samples, dim=1, seed=None):
    if seed is not None:
        rng = np.random.default_rng(seed)
        samples = rng.normal(0.0, 1.0, size=(n_samples, dim))
    else:
        samples = np.random.normal(0.0, 1.0, size=(n_samples, dim))
    sums = samples.sum(axis=1)
    indicators = (sums > threshold).astype(float)
    estimate = indicators.mean()
    std_error = indicators.std(ddof=1) / math.sqrt(n_samples)
    return float(estimate), float(std_error)

def importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=None, seed=None):
    if tilt is None:
        tilt = max(0.0, threshold / max(1, dim))
    if seed is not None:
        rng = np.random.default_rng(seed)
        samples = rng.normal(tilt, 1.0, size=(n_samples, dim))
    else:
        samples = np.random.normal(tilt, 1.0, size=(n_samples, dim))
    sums = samples.sum(axis=1)
    indicators = (sums > threshold).astype(float)
    weights = np.exp(-tilt * sums + 0.5 * dim * tilt * tilt)
    weighted = weights * indicators
    estimate = weighted.mean()
    std_error = weighted.std(ddof=1) / math.sqrt(n_samples)
    return float(estimate), float(std_error)

def cross_entropy_importance_sampling(threshold, n_samples_ce, n_samples_final, dim=1, n_iters=10, rho=0.01, seed=None):
    tilt = max(0.0, threshold / max(1, dim))
    rng = np.random.default_rng(seed)
    for _ in range(int(n_iters)):
        samples = rng.normal(tilt, 1.0, size=(n_samples_ce, dim))
        sums = samples.sum(axis=1)
        gamma = np.quantile(sums, 1.0 - rho)
        elites = sums[sums >= gamma]
        if elites.size > 0:
            tilt = float(elites.mean() / dim)
        else:
            tilt = tilt + 0.1
    prob, se = importance_sampling_normal_tail(threshold, n_samples_final, dim=dim, tilt=tilt, seed=seed)
    return float(prob), float(se), float(tilt)

def estimate_rare_event_probability(initial_condition, x0, time_horizon, n_paths, threshold, sigma=1.0, seed=None, method='importance'):
    n_samples = int(n_paths)
    if method == 'naive':
        return estimate_tail_probability_naive(threshold, n_samples, dim=1, seed=seed)
    if method == 'importance':
        return importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=threshold, seed=seed)
    if method == 'cross_entropy':
        prob, se, tilt = cross_entropy_importance_sampling(threshold, n_samples, n_samples, dim=1, seed=seed)
        return prob, se
    return importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=threshold, seed=seed)

