import math
import numpy as np
from utils.export_csv import rare_event_results_csv
from utils.export_json import rare_event_results_json
from visualizations.visualizationRareEvents import visualize_rare_event_probability
from calculators.calculate_confidence import confidence_interval


def run_rare() -> None:
    print("You have selected option 9: Rare event and Tail Risk Simulation.")
    print("1. Naive Monte Carlo tail probability")
    print("2. Importance sampling with fixed tilt")
    print("3. Cross-entropy to find tilt + importance sampling")
    choice = input("Enter choice (1-3) or 'b' to go back: ").strip().lower()
    if choice == 'b':
        return
    try:
        threshold = float(input("Enter threshold for the sum of standard normals: ").strip())
    except Exception:
        print("Invalid threshold")
        return
    try:
        dim = int(input("Enter number of components (dim) [1]: ").strip() or "1")
    except Exception:
        dim = 1
    try:
        n_samples = int(input("Enter number of samples [100000]: ").strip() or "100000")
    except Exception:
        n_samples = 100000
    seed_input = input("Enter random seed (integer) or leave blank: ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None
    method = "naive"
    tilt = None
    n_paths_for_export = n_samples
    if choice == '1':
        prob, se, confidence_intervals = estimate_tail_probability_naive(threshold, n_samples, dim=dim, seed=seed)
        method = "naive"
        print(f"Naive Monte Carlo estimate: {prob} (SE: {se})")
        for ci in confidence_intervals:
            print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']}, lower={ci['lower']}, upper={ci['upper']}, ME={ci['margin_of_error']}")
    elif choice == '2':
        try:
            tilt = float(input("Enter tilt (positive shift) for importance sampling [threshold/dim]: ").strip() or str(max(0.0, threshold / max(1, dim))))
        except Exception:
            tilt = max(0.0, threshold / max(1, dim))
        prob, se, confidence_intervals = importance_sampling_normal_tail(threshold, n_samples, dim=dim, tilt=tilt, seed=seed)
        method = "importance"
        print(f"Importance sampling estimate (tilt={tilt}): {prob} (SE: {se})")
        for ci in confidence_intervals:
            print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']}, lower={ci['lower']}, upper={ci['upper']}, ME={ci['margin_of_error']}")
    elif choice == '3':
        try:
            n_samples_ce = int(input("Enter samples for CE iterations [20000]: ").strip() or "20000")
        except Exception:
            n_samples_ce = 20000
        try:
            n_samples_final = int(input("Enter final importance sampling samples [100000]: ").strip() or "100000")
        except Exception:
            n_samples_final = 100000
        try:
            n_iters = int(input("Enter number of CE iterations [10]: ").strip() or "10")
        except Exception:
            n_iters = 10
        try:
            rho = float(input("Enter elite fraction rho (0.0-1.0) [0.01]: ").strip() or "0.01")
        except Exception:
            rho = 0.01
        prob, se, tilt, confidence_intervals = cross_entropy_importance_sampling(threshold, n_samples_ce, n_samples_final, dim=dim, n_iters=n_iters, rho=rho, seed=seed)
        method = "cross_entropy"
        n_paths_for_export = n_samples_final
        print(f"Cross-entropy found tilt: {tilt}")
        print(f"CE+Importance sampling estimate: {prob} (SE: {se})")
        for ci in confidence_intervals:
            print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']}, lower={ci['lower']}, upper={ci['upper']}, ME={ci['margin_of_error']}")
    else:
        print("Invalid selection")
        return
    export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the rare event results? (yes/no): ")).lower()
    while export_choice not in ['yes', 'y', 'no', 'n']:
        export_choice = str(input("Please enter 'yes' or 'no': ")).lower()
    if export_choice in ['yes', 'y']:
        rare_event_results_json(0.0, 0.0, 1.0, n_paths_for_export, threshold, prob, confidence_intervals)
        rare_event_results_csv(0.0, 0.0, 1.0, n_paths_for_export, threshold, prob, confidence_intervals)
    visualization_choice = str(input("Would you like to visualize the rare event probability estimate? (yes/no): ")).lower()
    while visualization_choice not in ['yes', 'y', 'no', 'n']:
        visualization_choice = str(input("Please enter 'yes' or 'no': ")).lower()
    if visualization_choice in ['yes', 'y']:
        visualize_rare_event_probability(0.0, 0.0, 1.0, n_paths_for_export, threshold, sigma=1.0, seed=seed)


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
    per_sample = (sums > threshold).astype(float)
    confidence_intervals = [confidence_interval(per_sample, confidence=conf) for conf in (0.90, 0.95, 0.99)]
    return float(estimate), float(std_error), confidence_intervals


def importance_sampling_normal_tail(threshold, n_samples, dim=1, tilt=None, seed=None, rng=None):
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
    confidence_intervals = [confidence_interval(weighted, confidence=conf) for conf in (0.90, 0.95, 0.99)]
    return float(estimate), float(std_error), confidence_intervals


def cross_entropy_importance_sampling(threshold, n_samples_ce, n_samples_final, dim=1, n_iters=10, rho=0.01, seed=None):
    tilt = max(0.0, threshold / max(1, dim))
    rng = np.random.default_rng(seed)
    n_elite = max(1,math.ceil(rho * n_samples_ce))
    
    for _ in range(int(n_iters)):
        sums = draw_gaussian_sum(rng, n_samples_ce, dim, tilt)
        elite_sums = np.partition(sums, n_samples_ce - n_elite)[n_samples_ce - n_elite:]
        tilt = float(elite_sums.mean()/dim)
    
    prob, se, confidence_intervals = importance_sampling_normal_tail(threshold, n_samples_final, dim=dim, tilt=tilt, rng=rng)
    return float(prob), float(se), float(tilt), confidence_intervals


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

