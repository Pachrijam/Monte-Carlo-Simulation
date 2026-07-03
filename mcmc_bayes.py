import numpy as np
import math
from typing import Callable, Iterable, List, Tuple, Optional


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


def trace_plot(samples: np.ndarray, var_idx: int = 0, ax=None, show: bool = True, savepath: Optional[str] = None):
    import matplotlib.pyplot as plt
    s = np.asarray(samples)
    y = s[:, var_idx]
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(y, color="C0")
    ax.set_xlabel("Iteration")
    ax.set_ylabel(f"x[{var_idx}]")
    if savepath:
        ax.figure.savefig(savepath, bbox_inches="tight")
    if show:
        plt.show()


def acf_plot(samples: np.ndarray, var_idx: int = 0, max_lag: int = 50, ax=None, show: bool = True, savepath: Optional[str] = None):
    import matplotlib.pyplot as plt
    s = np.asarray(samples)
    acf = autocorrelation(s[:, var_idx], max_lag)
    lags = np.arange(acf.size)
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 3))
    ax.stem(lags, acf, use_line_collection=True)
    ax.set_xlabel("Lag")
    ax.set_ylabel("Autocorrelation")
    if savepath:
        ax.figure.savefig(savepath, bbox_inches="tight")
    if show:
        plt.show()


def summarize_chain(samples: np.ndarray, var_names: Optional[List[str]] = None, cred: float = 0.95) -> None:
    mean, lower, upper = posterior_summary(samples, cred)
    if var_names is None:
        var_names = [f"x[{i}]" for i in range(mean.size)]
    for i, name in enumerate(var_names):
        ess = effective_sample_size(samples[:, i])
        print(f"{name}: mean={mean[i]:.4f}  {int(100*cred)}% CI=({lower[i]:.4f}, {upper[i]:.4f})  ESS={ess:.1f}")
