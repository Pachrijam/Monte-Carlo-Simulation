import math
import numpy as np
import matplotlib.pyplot as plt


def trapz(y, x):
    """Simple trapezoidal integration fallback if numpy.trapz is unavailable."""
    dx = np.diff(x)
    return np.sum((y[:-1] + y[1:]) * dx / 2)


def generateIntData(samples, func, a, b, reference_grid=100000):
	x = np.random.rand(samples)
	x = a + (b - a) * x

	try:
		fx = func(x)
	except Exception:
		fx = np.array([func(xi) for xi in x], dtype=float)

	cumulative_sum = np.cumsum(fx)
	n = np.arange(1, samples + 1)
	mean_fx = cumulative_sum / n
	integral_estimates = (b - a) * mean_fx

	grid_size = int(min(max(1000, samples * 10), reference_grid))
	ref_x = np.linspace(a, b, grid_size)
	try:
		ref_fx = func(ref_x)
	except Exception:
		ref_fx = np.array([func(xi) for xi in ref_x], dtype=float)

	ref_integral = trapz(ref_fx, ref_x)

	if abs(ref_integral) < 1e-12:
		errors = np.abs(integral_estimates - ref_integral) * 100
	else:
		errors = np.abs(integral_estimates - ref_integral) / abs(ref_integral) * 100

	return n, integral_estimates, errors, ref_integral


def visualizeIntEstimates(samples, func, a, b):
	xValues, yValues, _, ref_integral = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	plt.figure(figsize=(10, 6))
	plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
	plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
	plt.axhline(y=ref_integral, color='blue', linestyle='--', label='Reference integral')

	y_min = min(np.min(yValues), ref_integral)
	y_max = max(np.max(yValues), ref_integral)
	y_span = y_max - y_min
	if y_span <= 0:
		y_span = max(abs(ref_integral), 1.0)
	margin = max(y_span * 0.1, 0.1)
	plt.ylim(y_min - margin, y_max + margin)

	plt.xlim(0, samples)
	plt.xlabel('Number of Samples', fontsize=14)
	plt.ylabel('Estimated Integral', fontsize=14)
	plt.title('Monte Carlo Estimation of an Integral', fontsize=14, fontweight='bold')
	plt.legend()
	plt.tight_layout()
	plt.show()


def visualizeIntPercentError(samples, func, a, b):
	xValues, _, yValues, _ = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	plt.figure(figsize=(10, 6))
	plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
	plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)

	top_value = max(np.nanmax(yValues), np.nanpercentile(yValues, 95), 1.0)
	plt.ylim(0, top_value * 1.1)

	plt.xlim(0, samples)
	plt.xlabel('Number of Samples', fontsize=14)
	plt.ylabel('Percent Error (%)', fontsize=14)
	plt.title('Percent Error of Monte Carlo Integral Estimate', fontsize=14, fontweight='bold')
	plt.tight_layout()
	plt.show()


def visualizeIntSubplot(samples, func, a, b):
	xValues, yValues, errorValues, ref_integral = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

	ax1.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
	ax1.axhline(y=ref_integral, color='blue', linestyle='--', label='Reference integral')
	y_min = min(np.min(yValues), ref_integral)
	y_max = max(np.max(yValues), ref_integral)
	y_span = y_max - y_min
	if y_span <= 0:
		y_span = max(abs(ref_integral), 1.0)
	margin = max(y_span * 0.1, 0.1)
	ax1.set_ylim(y_min - margin, y_max + margin)
	ax1.set_xlim(0, samples)
	ax1.set_xlabel('Number of Samples', fontsize=14)
	ax1.set_ylabel('Estimated Integral', fontsize=14)
	ax1.set_title('Monte Carlo Estimation of an Integral', fontsize=14, fontweight='bold')
	ax1.legend()
	ax1.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

	ax2.plot(xValues, errorValues, color='red', linestyle='-', linewidth=2, markersize=3)
	top_value = max(np.nanmax(errorValues), np.nanpercentile(errorValues, 95), 1.0)
	ax2.set_ylim(0, top_value * 1.1)
	ax2.set_xlim(0, samples)
	ax2.set_xlabel('Number of Samples', fontsize=14)
	ax2.set_ylabel('Percent Error (%)', fontsize=14)
	ax2.set_title('Percent Error of Monte Carlo Integral Estimate', fontsize=14, fontweight='bold')
	ax2.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

	plt.tight_layout()
	plt.show()