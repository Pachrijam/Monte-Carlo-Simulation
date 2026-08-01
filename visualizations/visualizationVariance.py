import matplotlib.pyplot as plt
import numpy as np

def plot_variance(samples, bins=50):
	arr = np.asarray(samples)
	var = float(np.var(arr, ddof=1))
	fig, ax = plt.subplots()
	ax.hist(arr, bins=bins, density=True, alpha=0.7)
	ax.set_title("Sample Distribution")
	ax.set_xlabel("Value")
	ax.set_ylabel("Density")
	ax.text(0.95, 0.95, f"Sample variance: {var:.6g}", transform=ax.transAxes, ha="right", va="top")
	plt.tight_layout()
	plt.show()