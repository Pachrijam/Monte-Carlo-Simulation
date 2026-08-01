import matplotlib.pyplot as plt
import numpy as np

def plot_variance(samples, bins=50):
    plt.style.use("dark_background")
    arr = np.asarray(samples)
    var = float(np.var(arr, ddof=1))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(arr, bins=bins, density=True, alpha=0.7)
    ax.set_title("Sample Distribution", fontsize=14)
    ax.set_xlabel("Value", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.text(0.95, 0.95, f"Sample variance: {var:.6g}", transform=ax.transAxes, ha="right", va="top")
    plt.tight_layout()
    plt.show()