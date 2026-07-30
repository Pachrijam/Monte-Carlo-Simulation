import numpy as np
import math
from typing import Callable, Iterable, List, Tuple, Optional
from utils.exceptions import safe_int, safe_float, safe_choice
from visualizations.visualizationMCMC import acf_plot, trace_plot, acf_trace_subplot
from utils.export_json import mcmc_results_json
from utils.export_csv import mcmc_results_csv


def run_mcmc() -> None:
    print("You have selected option 6: Markov Chain Monte Carlo (MCMC) Methods.")
    print("------------------------------------------------------------------------\nSelect an MCMC method to run:")
    print("""1. Metropolis-Hastings
2. Gibbs Sampling
3. Exit""")
    mcmc_choice = safe_int("Enter the number of the MCMC method you would like to run (1-3): ", min_val=1, max_val=3)
    if mcmc_choice == 1:
        print("------------------------------------------------------------------------\nYou have selected Metropolis-Hastings.")
        def log_normal(x: np.ndarray) -> float:
            return -0.5 * np.sum(x ** 2) - (len(x) / 2) * np.log(2 * np.pi)
        dim = safe_int("Enter the dimension of the target distribution (e.g., 2): ", min_val=1)
        num_samples = safe_int("Enter the number of samples to generate (e.g., 1000): ", min_val=1, max_val=1000000)
        proposal_std = safe_float("Enter the standard deviation for the proposal distribution (e.g., 1.0): ", min_val=0.0001)
        burn_in = safe_int("Enter the number of burn-in samples (e.g., 100): ", min_val=0)
        while burn_in >= num_samples:
            print("Burn-in must be less than number of samples.")
            burn_in = safe_int("Enter the number of burn-in samples: ", min_val=0)
        thin = safe_int("Enter the thinning interval (e.g., 1 for no thinning): ", min_val=1)
        
        initial = np.zeros(dim)
        samples, acceptance_rate = metropolis_hastings(log_normal, initial, num_samples, proposal_std=proposal_std, burn_in=burn_in, thin=thin)
        
        print(f"------------------------------------------------------------------------\nMetropolis-Hastings completed. Acceptance rate: {acceptance_rate:.4f}")
        mean, lower, upper = posterior_summary(samples, cred=0.95)
        print(f"95% credible intervals for each dimension:")
        for i in range(dim):
            print(f"Dimension {i}: Mean={mean[i]:.4f},95% CI=({lower[i]:.4f}, {upper[i]:.4f})")

        trace_vis = safe_choice("------------------------------------------------------------------------\nWould you like to visualize the samples? (acf/trace/subplot/no): ", ['acf', 'trace', 'subplot', 'no', 'n'])
        if trace_vis in ['acf'] and dim > 0:
            acf_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['trace'] and dim > 0:
            trace_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['subplot'] and dim > 0:
            acf_trace_subplot(samples, var_idx=0, show=True)
        export_choice = safe_choice("------------------------------------------------------------------------\nWould you like to export the MCMC results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_choice in ['yes', 'y']:
            parameters = {
                "dimension": dim,
                "proposal_std": proposal_std,
                "burn_in": burn_in,
                "thin": thin
            }
            posterior_summary_data = []
            for i in range(dim):
                posterior_summary_data.append({
                    "parameter": f"Dimension {i}",
                    "mean": mean[i],
                    "median": np.median(samples[:, i]),
                    "lower": lower[i],
                    "upper": upper[i],
                    "std_dev": np.std(samples[:, i]),
                    "ci_lower": lower[i],
                    "ci_upper": upper[i],
                    "95% CI Lower": lower[i],
                    "95% CI Upper": upper[i]
                })
            mcmc_results_json("Metropolis-Hastings", parameters, num_samples, posterior_summary_data)
            mcmc_results_csv("Metropolis-Hastings", parameters, num_samples, posterior_summary_data)
    elif mcmc_choice == 2:    
        print("------------------------------------------------------------------------\nYou have selected Gibbs Sampling.")
        dim = safe_int("Enter the dimension of the target distribution (e.g., 2): ", min_val=1)
        num_samples = safe_int("Enter the number of samples to generate (e.g., 1000): ", min_val=1, max_val=1000000)
        burn_in = safe_int("Enter the number of burn-in samples (e.g., 100): ", min_val=0)
        while burn_in >= num_samples:
            print("Burn-in must be less than number of samples.")
            burn_in = safe_int("Enter the number of burn-in samples: ", min_val=0)
        thin = safe_int("Enter the thinning interval (e.g., 1 for no thinning): ", min_val=1)

        def gibbs_standard_normal(dim: int, n_samples: int, burn_in: int = 0, thin: int = 1) -> np.ndarray:
            total = burn_in + n_samples * thin
            x = np.zeros(dim)
            samples = []
            for t in range(total):
                for i in range(dim):
                    x[i] = np.random.randn()
                if t >= burn_in and ((t - burn_in) % thin == 0):
                    samples.append(x.copy())
            return np.array(samples)

        samples = gibbs_standard_normal(dim, num_samples, burn_in=burn_in, thin=thin)
        print(f"------------------------------------------------------------------------\nGibbs sampling completed. Generated {samples.shape[0]} samples.")
        mean, lower, upper = posterior_summary(samples, cred=0.95)
        print(f"95% credible intervals for each dimension:")
        for i in range(dim):
            print(f"Dimension {i}: Mean={mean[i]:.4f},95% CI=({lower[i]:.4f}, {upper[i]:.4f})")
        trace_vis = safe_choice("------------------------------------------------------------------------\nWould you like to visualize the samples? (acf/trace/subplot/no): ", ['acf', 'trace', 'subplot', 'no', 'n'])
        if trace_vis in ['acf'] and dim > 0:
            acf_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['trace'] and dim > 0:
            trace_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['subplot'] and dim > 0:
            acf_trace_subplot(samples, var_idx=0, show=True)
        export_choice = safe_choice("------------------------------------------------------------------------\nWould you like to export the MCMC results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_choice in ['yes', 'y']:
            parameters = {
                "dimension": dim,
                "burn_in": burn_in,
                "thin": thin
            }
            posterior_summary_data = []
            for i in range(dim):
                posterior_summary_data.append({
                    "parameter": f"Dimension {i}",
                    "mean": mean[i],
                    "median": np.median(samples[:, i]),
                    "lower": lower[i],
                    "upper": upper[i],
                    "std_dev": np.std(samples[:, i]),
                    "ci_lower": lower[i],
                    "ci_upper": upper[i],
                    "95% CI Lower": lower[i],
                    "95% CI Upper": upper[i]
                })
            mcmc_results_json("Gibbs Sampling", parameters, num_samples, posterior_summary_data)
            mcmc_results_csv("Gibbs Sampling", parameters, num_samples, posterior_summary_data)
    elif mcmc_choice == 3:
        print("------------------------------------------------------------------------\nExiting MCMC methods.")


def metropolis_hastings(log_prob: Callable[[np.ndarray], float], initial: np.ndarray, n_samples: int, proposal_std: float = 1.0, burn_in: int = 0, thin: int = 1, rng: Optional[np.random.Generator] = None) -> Tuple[np.ndarray, float]:
    if rng is None:
        rng = np.random.default_rng()
    dim = np.atleast_1d(initial).shape[0]
    total_iters = burn_in + n_samples * thin
    samples = np.zeros((n_samples, dim))
    current = np.atleast_1d(initial).astype(float)
    current_logp = log_prob(current)
    accepted = 0
    out_i = 0
    for it in range(total_iters):
        proposal = current + rng.normal(scale=proposal_std, size=dim)
        prop_logp = log_prob(proposal)
        log_accept_ratio = prop_logp - current_logp
        if math.log(rng.random()) < log_accept_ratio:
            current = proposal
            current_logp = prop_logp
            accepted += 1
        if it >= burn_in and ((it - burn_in) % thin == 0):
            samples[out_i] = current
            out_i += 1
    acc_rate = accepted / total_iters
    return samples, acc_rate


def gibbs_sampler(conditional_samplers: Iterable[Callable[[np.ndarray, np.random.Generator], float]], initial: Iterable[float], n_samples: int, burn_in: int = 0, thin: int = 1, rng: Optional[np.random.Generator] = None) -> np.ndarray:
    if rng is None:
        rng = np.random.default_rng()
    conds = list(conditional_samplers)
    dim = len(conds)
    state = np.array(list(initial), dtype=float)
    total_iters = burn_in + n_samples * thin
    samples = np.zeros((n_samples, dim))
    out_i = 0
    for it in range(total_iters):
        for i, sampler in enumerate(conds):
            state[i] = sampler(state, rng)
        if it >= burn_in and ((it - burn_in) % thin == 0):
            samples[out_i] = state
            out_i += 1
    return samples


def autocorrelation(x: np.ndarray, max_lag: int = 100) -> np.ndarray:
    x = np.asarray(x)
    n = x.shape[0]
    x = x - x.mean()
    acf = np.zeros(min(max_lag, n - 1) + 1)
    var = (x * x).sum() / n
    if var == 0:
        return acf
    for lag in range(acf.size):
        acf[lag] = (x[:n - lag] * x[lag:]).sum() / n / var
    return acf


def effective_sample_size(x: np.ndarray, max_lag: int = 100) -> float:
    acf = autocorrelation(x, max_lag)
    rho = acf[1:]
    positive_seq = rho[rho > 0]
    if positive_seq.size == 0:
        return x.size
    s = 0.0
    for r in positive_seq:
        s += 2 * r
    ess = x.size / (1 + s)
    return ess


def posterior_summary(samples: np.ndarray, cred: float = 0.95) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    samples = np.asarray(samples)
    mean = samples.mean(axis=0)
    lower = np.percentile(samples, 100 * (1 - cred) / 2, axis=0)
    upper = np.percentile(samples, 100 * (1 + cred) / 2, axis=0)
    return mean, lower, upper


def summarize_chain(samples: np.ndarray, var_names: Optional[List[str]] = None, cred: float = 0.95) -> None:
    mean, lower, upper = posterior_summary(samples, cred)
    if var_names is None:
        var_names = [f"x[{i}]" for i in range(mean.size)]
    for i, name in enumerate(var_names):
        ess = effective_sample_size(samples[:, i])
        print(f"{name}: mean={mean[i]:.4f}  {int(100*cred)}% CI=({lower[i]:.4f}, {upper[i]:.4f})  ESS={ess:.1f}")
