import numpy as np
import matplotlib.pyplot as plt
from calculators.calculate_pde_sde import monte_carlo_pde_solution, simulate_sde_paths


def visualize_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=1.0, x_values=None, seed=None, show=True):
    plt.style.use("dark_background")
    if x_values is None:
        x_values = np.linspace(-2.0, 2.0, 9)

    estimates = []
    errors = []
    for x_value in x_values:
        estimate, std_error = monte_carlo_pde_solution(initial_condition, x_value, time_horizon, n_paths, sigma=sigma, seed=seed)
        estimates.append(estimate)
        errors.append(std_error)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_values, estimates, marker="o", color="royalblue", label="Monte Carlo estimate")
    ax.fill_between(x_values, np.array(estimates) - np.array(errors), np.array(estimates) + np.array(errors), alpha=0.2, color="royalblue")
    ax.set_title("PDE Monte Carlo solution", fontsize=16, fontweight='bold')
    ax.set_xlabel("x", fontsize=14)
    ax.set_ylabel("u(x, t)", fontsize=14)
    ax.legend()
    if show:
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
        plt.tight_layout()
        plt.show()
    return fig, ax


def visualize_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=None, show=True):
    plt.style.use("dark_background")
    paths, time_grid = simulate_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)

    fig, ax = plt.subplots(figsize=(8, 4))
    for path in paths[: min(10, n_paths)]:
        ax.plot(time_grid, path, alpha=0.6, color="steelblue")
    ax.plot(time_grid, paths.mean(axis=0), color="crimson", linewidth=2, label="Mean path")
    ax.set_title("SDE Monte Carlo sample paths", fontsize=16, fontweight='bold')
    ax.set_xlabel("time", fontsize=14)
    ax.set_ylabel("X_t", fontsize=14)
    ax.legend()
    if show:
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
        plt.tight_layout()
        plt.show()
    return fig, ax


def visualize_pde_sde_subplot(initial_condition, x0, time_horizon, n_paths, sigma=1.0, initial_value=0.0, drift=0.0, diffusion=1.0, n_steps=50, seed=None, show=True):
    plt.style.use("dark_background")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    x_values = np.linspace(-2.0, 2.0, 9)
    estimates = []
    errors = []
    for x_value in x_values:
        estimate, std_error = monte_carlo_pde_solution(initial_condition, x_value, time_horizon, n_paths, sigma=sigma, seed=seed)
        estimates.append(estimate)
        errors.append(std_error)

    axes[0].plot(x_values, estimates, marker="o", color="royalblue")
    axes[0].fill_between(x_values, np.array(estimates) - np.array(errors), np.array(estimates) + np.array(errors), alpha=0.2, color="royalblue")
    axes[0].set_title("PDE estimate", fontsize=16, fontweight='bold')
    axes[0].set_xlabel("x", fontsize=14)
    axes[0].set_ylabel("u(x, t)", fontsize=14)
    axes[0].grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    paths, time_grid = simulate_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
    for path in paths[: min(10, n_paths)]:
        axes[1].plot(time_grid, path, alpha=0.5, color="steelblue")
    axes[1].plot(time_grid, paths.mean(axis=0), color="crimson", linewidth=2, label="Mean path")
    axes[1].set_title("SDE sample paths", fontsize=16, fontweight='bold')
    axes[1].set_xlabel("time", fontsize=14)
    axes[1].set_ylabel("X_t", fontsize=14)
    axes[1].legend()
    axes[1].grid(True, color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    if show:
        plt.tight_layout()
        plt.show()
    return fig, axes