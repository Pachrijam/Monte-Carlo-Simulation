import numpy as np
from utils.exceptions import safe_int, safe_float, safe_choice, safe_seed_input
from visualizations.visualizationVariance import plot_variance

def run_variance():
    n = safe_int("Enter number of samples: ", min_val=1)
    dist = safe_choice("Choose distribution (normal/uniform/exponential): ", ["normal", "uniform", "exponential"])
    seed = safe_seed_input("Optional seed (press Enter to skip): ")
    rng = np.random.default_rng(seed)
    if dist == "normal":
        mu = safe_float("Enter mean (mu): ")
        sigma = safe_float("Enter std dev (sigma, >0): ", min_val=0.0)
        samples = rng.normal(mu, sigma, size=n)
    elif dist == "uniform":
        low = safe_float("Enter lower bound: ")
        high = safe_float("Enter upper bound: ")
        samples = rng.uniform(low, high, size=n)
    else:
        scale = safe_float("Enter scale (lambda^-1): ", min_val=0.0)
        samples = rng.exponential(scale, size=n)
    sample_var = float(np.var(samples, ddof=1))
    print(f"Estimated variance (sample, ddof=1): {sample_var}")
    try:
        plot_variance(samples)
    except Exception:
        pass
    return {"n": n, "distribution": dist, "variance_estimate": sample_var}