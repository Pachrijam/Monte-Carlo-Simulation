import math
import numpy as np

def draw_gaussian_sum(rng,n_samples,dim,mean_per_dim):
    return rng.normal(dim*mean_per_dim,math.sqrt(dim),size=n_samples)


def estimate_tail_probability_naive(threshold, n_samples, dim=1, seed=None):
    rng = np.random.default_rng(seed)
    sums = draw_gaussian_sum(rng, n_samples, dim, 0.0)
    
    n_exceed = np.count_nonzero(sums > threshold)
    estimate = n_exceed / n_samples
    if n_samples > 1:
        std_error = math.sqrt(estimate * (1 - estimate) / (n_samples - 1))
    else:
        std_error = float("nan")
    return float(estimate), float(std_error)


def importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=None, seed=None):
    if tilt is None:
        tilt = max(0.0, threshold / max(1, dim))
    if rng is None:
        rng = np.random.default_rng(seed)
    
    sums = draw_gaussian_sum(rng,n_samples,dim,tilt)
    mask = sums > threshold
    exceeded_sums = sums[mask]
    weighted = np.zeros(n_samples,dtype=np.float64)
    if exceeded_sums.size:
        weighted[mask] = np.exp(-tilt * exceeded_sums + 0.5 * dim * (tilt ** 2))
    estimate = np.mean(weighted)
    std_error = weighted.std(ddof=1) / math.sqrt(n_samples) if n_samples > 1 else float ("nan")
    
    return float(estimate), float(std_error)

def cross_entropy_importance_sampling(threshold, n_samples_ce, n_samples_final, dim=1, n_iters=10, rho=0.01, seed=None):
    tilt = max(0.0, threshold / max(1, dim))
    rng = np.random.default_rng(seed)
    n_elite = max(1,math.ceil(rho * n_samples_ce))
    
    for _ in range(int(n_iters)):
        sums = draw_gaussian_sum(rng, n_samples_ce, dim, tilt)
        elite_sums = np.partition(sums, n_samples_ce - n_elite)[n_samples_ce - n_elite:]
        tilt = float(elite_sums.mean()/dim)
    
    prob, se = importance_sampling_normal_tail(threshold, n_samples_final, dim=dim, tilt=tilt, rng=rng)
    return float(prob), float(se), float(tilt)

def estimate_rare_event_probability(initial_condition, x0, time_horizon, n_paths, threshold, sigma=1.0, seed=None, method='importance', n_samples_ce=None):
    n_samples = int(n_paths)
    if method == 'naive':
        return estimate_tail_probability_naive(threshold, n_samples, dim=1, seed=seed)
    if method == 'importance':
        return importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=threshold, seed=seed)
    if method == 'cross_entropy':
        ce_samples = n_samples_ce if n_samples_ce is not None else min(n_samples,5000)
        prob, se, tilt = cross_entropy_importance_sampling(threshold, ce_samples, n_samples, dim=1, seed=seed)
        return prob, se
    return importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=threshold, seed=seed)

