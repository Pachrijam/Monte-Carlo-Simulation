import math
import numpy as np
import matplotlib.pyplot as plt

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

	ref_integral = np.trapz(ref_fx, ref_x)

	if abs(ref_integral) < 1e-12:
		errors = np.abs(integral_estimates - ref_integral) * 100
	else:
		errors = np.abs(integral_estimates - ref_integral) / abs(ref_integral) * 100

	return n, integral_estimates, errors, ref_integral


def visualizeIntEstimates(samples, func, a, b):
	xValues, yValues, _, ref_integral = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
	plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
	plt.axhline(y=ref_integral, color='blue', linestyle='--', label='Reference integral')

	# Automatic y-limits heuristic (based on interval and samples)
	span = abs(b - a)
	if samples < 50:
		plt.ylim(ref_integral - span * 1.5, ref_integral + span * 1.5)
	elif samples < 1000:
		plt.ylim(ref_integral - span * 1.0, ref_integral + span * 1.0)
	else:
		plt.ylim(ref_integral - span * 0.3, ref_integral + span * 0.3)

	plt.xlim(0, samples)
	plt.xlabel('Number of Samples', fontsize=14)
	plt.ylabel('Estimated Integral', fontsize=14)
	plt.title('Monte Carlo Estimation of an Integral', fontsize=14, fontweight='bold')
	plt.legend()
	plt.show()


def visualizeIntPercentError(samples, func, a, b):
	xValues, _, yValues, _ = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
	plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)

	# Adaptive y-limits for percent error
	if samples < 100:
		plt.ylim(0, max(10, np.nanpercentile(yValues, 95)))
	elif samples < 1000:
		plt.ylim(0, max(5, np.nanpercentile(yValues, 95)))
	elif samples < 10000:
		plt.ylim(0, max(1, np.nanpercentile(yValues, 95)))
	else:
		plt.ylim(0, max(0.5, np.nanpercentile(yValues, 95)))

	plt.xlim(0, samples)
	plt.xlabel('Number of Samples', fontsize=14)
	plt.ylabel('Percent Error (%)', fontsize=14)
	plt.title('Percent Error of Monte Carlo Integral Estimate', fontsize=14, fontweight='bold')
	plt.show()


def visualizeIntSubplot(samples, func, a, b):
	xValues, yValues, errorValues, ref_integral = generateIntData(samples, func, a, b)
	plt.style.use('dark_background')
	fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

	ax1.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
	ax1.axhline(y=ref_integral, color='blue', linestyle='--', label='Reference integral')
	span = abs(b - a)
	if samples < 50:
		ax1.set_ylim(ref_integral - span * 1.5, ref_integral + span * 1.5)
	elif samples < 1000:
		ax1.set_ylim(ref_integral - span * 1.0, ref_integral + span * 1.0)
	else:
		ax1.set_ylim(ref_integral - span * 0.3, ref_integral + span * 0.3)
	ax1.set_xlim(0, samples)
	ax1.set_xlabel('Number of Samples', fontsize=14)
	ax1.set_ylabel('Estimated Integral', fontsize=14)
	ax1.set_title('Monte Carlo Estimation of an Integral', fontsize=14, fontweight='bold')
	ax1.legend()
	ax1.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

	ax2.plot(xValues, errorValues, color='red', linestyle='-', linewidth=2, markersize=3)
	if samples < 100:
		ax2.set_ylim(0, max(10, np.nanpercentile(errorValues, 95)))
	elif samples < 1000:
		ax2.set_ylim(0, max(5, np.nanpercentile(errorValues, 95)))
	else:
		ax2.set_ylim(0, max(1, np.nanpercentile(errorValues, 95)))
	ax2.set_xlim(0, samples)
	ax2.set_xlabel('Number of Samples', fontsize=14)
	ax2.set_ylabel('Percent Error (%)', fontsize=14)
	ax2.set_title('Percent Error of Monte Carlo Integral Estimate', fontsize=14, fontweight='bold')
	ax2.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

	plt.tight_layout()
	plt.show()