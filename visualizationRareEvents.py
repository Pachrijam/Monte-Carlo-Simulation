import math
import numpy as np
import matplotlib.pyplot as plt

#TODO: add estimates graph, error graph, and combined subplot for rare event probability estimation

def visualize_rare_event_probability(initial_condition, x0, time_horizon, n_paths, threshold, sigma=1.0, seed=None, show=True):
    plt.style.use("dark_background")
    estimates = []
    errors = []
    x_values = np.linspace(-2.0, 2.0, 9)
    
    for x_value in x_values:
        estimate, std_error = estimate_rare_event_probability(initial_condition, x_value, time_horizon, n_paths, threshold, sigma=sigma, seed=seed)
        estimates.append(estimate)
        errors.append(std_error)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_values, estimates, marker="o", color="orange", label="Rare Event Probability Estimate")
    ax.fill_between(x_values, np.array(estimates) - np.array(errors), np.array(estimates) + np.array(errors), alpha=0.2, color="orange")
    ax.set_title("Rare Event Probability Estimation", fontsize=16, fontweight='bold')
    ax.set_xlabel("x", fontsize=14)
    ax.set_ylabel("Probability", fontsize=14)
    ax.legend()
    
    if show:
        plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
        plt.tight_layout()
        plt.show()
    
    return fig, ax