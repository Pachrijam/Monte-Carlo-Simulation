import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def trace_plot(samples: np.ndarray, var_idx: int = 0, ax=None, show: bool = True, savepath: Optional[str] = None):
    plt.style.use('dark_background')
    s = np.asarray(samples)
    y = s[:, var_idx]
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    ax.plot(y, color="C0")
    ax.set_xlabel("Iteration", fontsize=14)
    ax.set_ylabel(f"x[{var_idx}]", fontsize=14)
    if savepath:
        ax.figure.savefig(savepath, bbox_inches="tight")
    if show:
        plt.title("Trace Plot", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()


def acf_plot(samples: np.ndarray, var_idx: int = 0, max_lag: int = 50, ax=None, show: bool = True, savepath: Optional[str] = None):
    plt.style.use('dark_background')
    s = np.asarray(samples)
    from calculators.calculate_mcmc_bayes import autocorrelation
    acf = autocorrelation(s[:, var_idx], max_lag)
    lags = np.arange(acf.size)
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    try:
        ax.stem(lags, acf, use_line_collection=True)
    except TypeError:
        ax.stem(lags, acf)
    ax.set_xlabel("Lag", fontsize=14)
    ax.set_ylabel("Autocorrelation", fontsize=14)
    if savepath:
        ax.figure.savefig(savepath, bbox_inches="tight")
    if show:
        plt.title(f"Autocorrelation Function (Variable {var_idx})", fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()


def acf_trace_subplot(samples: np.ndarray, var_idx: int = 0, max_lag: int = 50, ax=None, show: bool = True, savepath: Optional[str] = None):
    plt.style.use('dark_background')
    s = np.asarray(samples)
    y = s[:, var_idx]
    from calculators.calculate_mcmc_bayes import autocorrelation
    acf = autocorrelation(y, max_lag)
    lags = np.arange(acf.size)
    if ax is None:
        fig, ax = plt.subplots(2, 1, figsize=(12, 10))
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    ax[0].plot(y, color="C0")
    ax[0].set_xlabel("Iteration", fontsize=14)
    ax[0].set_ylabel(f"x[{var_idx}]", fontsize=14)
    ax[0].set_title("Trace Plot", fontsize=16, fontweight='bold')
    ax[0].grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    try:
        ax[1].stem(lags, acf, use_line_collection=True)
    except TypeError:
        ax[1].stem(lags, acf)
    ax[1].set_xlabel("Lag", fontsize=14)
    ax[1].set_ylabel("Autocorrelation", fontsize=14)
    ax[1].set_title(f"Autocorrelation Function (Variable {var_idx})", fontsize=16, fontweight='bold')

    if savepath:
        fig.savefig(savepath, bbox_inches="tight")
    if show:
        plt.tight_layout()
        plt.show()
