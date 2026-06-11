import math
import numpy as np
import matplotlib.pyplot as plt

def generatePiData(samples):
    x = np.random.rand(samples)
    y = np.random.rand(samples)

    inside = x**2 + y**2 <= 1
    hits = np.cumsum(inside)
    n = np.arange(1, samples + 1)
    
    pi_estimates = 4 * hits / n
    errors = np.abs(pi_estimates - math.pi) / math.pi * 100
    return n, pi_estimates, errors

def visualizePiEstimates(samples):
    xValues, yValues, _ = generatePiData(samples)
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    plt.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')

    y_min = min(np.min(yValues), math.pi)
    y_max = max(np.max(yValues), math.pi)
    y_span = y_max - y_min
    if y_span < 0.1:
        y_span = 0.1
    margin = y_span * 0.1
    plt.ylim(max(0, y_min - margin), y_max + margin)

    plt.xlim(0, samples)
    plt.xlabel('Number of Samples', fontsize=14)
    plt.ylabel('Estimated Value of Pi', fontsize=14)
    plt.title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()
    plt.show()

def visualizePiPercentError(samples):
    xValues, _, yValues = generatePiData(samples)
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)

    top_value = max(np.nanmax(yValues), np.nanpercentile(yValues, 95), 1.0)
    plt.ylim(0, top_value * 1.1)

    plt.xlim(0, samples)
    plt.xlabel('Number of Samples', fontsize=14)
    plt.ylabel('Percent Error (%)', fontsize=14)
    plt.title('Percent Error of Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def visualizePiSubplot(samples):
    xValues, yValues, errorValues = generatePiData(samples)
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    y_min = min(np.min(yValues), math.pi)
    y_max = max(np.max(yValues), math.pi)
    y_span = y_max - y_min
    if y_span < 0.1:
        y_span = 0.1
    margin = y_span * 1.1
    ax1.set_ylim(max(0, y_min - margin), y_max + margin)
    ax1.set_xlim(0, samples)
    ax1.set_xlabel('Number of Samples', fontsize=14)
    ax1.set_ylabel('Estimated Value of Pi', fontsize=14)
    ax1.set_title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    ax1.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')
    ax1.legend()
    ax1.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    ax2.plot(xValues, errorValues, color='red', linestyle='-', linewidth=2, markersize=3)
    top_value = max(np.nanmax(errorValues), np.nanpercentile(errorValues, 95), 1.0)
    ax2.set_ylim(0, top_value * 1.1)
    ax2.set_xlim(0, samples)
    ax2.set_xlabel('Number of Samples', fontsize=14)
    ax2.set_ylabel('Percent Error (%)', fontsize=14)
    ax2.set_title('Percent Error of Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    ax2.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    plt.tight_layout()
    plt.show()