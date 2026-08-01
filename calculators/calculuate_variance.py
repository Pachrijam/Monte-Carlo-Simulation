import numpy as np
from utils.exceptions import safe_int, safe_float, safe_choice, safe_seed_input
from visualizations.visualizationVariance import plot_variance
from utils.export_csv import variance_results_csv
from utils.export_json import variance_results_json

def run_variance():
    n = safe_int("Enter number of samples: ", min_val=1)
    dist = safe_choice("Choose distribution (normal/uniform/exponential): ", ["normal", "uniform", "exponential"])
    seed = safe_seed_input("Optional seed (press Enter to skip): ")
    rng = np.random.default_rng(seed)
    params = {}
    if dist == "normal":
        mu = safe_float("Enter mean (mu): ")
        sigma = safe_float("Enter std dev (sigma, >0): ", min_val=0.0)
        samples = rng.normal(mu, sigma, size=n)
        params = {"mu": mu, "sigma": sigma}
    elif dist == "uniform":
        low = safe_float("Enter lower bound: ")
        high = safe_float("Enter upper bound: ")
        samples = rng.uniform(low, high, size=n)
        params = {"low": low, "high": high}
    else:
        scale = safe_float("Enter scale (lambda^-1): ", min_val=0.0)
        samples = rng.exponential(scale, size=n)
        params = {"scale": scale}
    sample_var = float(np.var(samples, ddof=1))
    print(f"Estimated variance (sample, ddof=1): {sample_var}")
    try:
        plot_variance(samples)
    except Exception:
        pass
    export_choice = safe_choice("Export results? (none/csv/json/both): ", ["none", "csv", "json", "both"])
    filename = input("Optional filename (without extension, press Enter to auto): ").strip()
    method_name = "Monte Carlo Variance"
    if export_choice in ("csv", "both"):
        variance_results_csv(method_name, params, n, sample_var, filename or None)
    if export_choice in ("json", "both"):
        variance_results_json(method_name, params, n, sample_var, filename or None)
    return {"n": n, "distribution": dist, "parameters": params, "variance_estimate": sample_var}