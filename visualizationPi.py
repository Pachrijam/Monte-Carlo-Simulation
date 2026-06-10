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
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    plt.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')
    if(samples >= 50 and samples < 100):
        plt.ylim(2.5, 3.5)
    elif(samples >= 100 and samples < 1000):
        plt.ylim(2.6, 4)
    elif(samples >= 1000 and samples < 100000):
        plt.ylim(3, 3.3)
    elif(samples >= 100000 and samples < 1000000):
        plt.ylim(3.1, 3.2)
    elif(samples >= 1000000):
        plt.ylim(3.12, 3.15)
    else:
        plt.ylim(0, 6)
    plt.xlim(0, samples)
    plt.xlabel('Number of Samples', fontsize=14)
    plt.ylabel('Estimated Value of Pi', fontsize=14)
    plt.title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.legend()
    plt.show()

def visualizePiPercentError(samples):
    xValues, _, yValues = generatePiData(samples)
    plt.style.use('dark_background')
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    if(samples >= 100 and samples < 400):
        plt.ylim(0, 40)
    elif(samples >= 400 and samples < 600):
        plt.ylim(0, 30)
    elif(samples >= 600 and samples < 1000):
        plt.ylim(0, 20)
    elif(samples >= 1000 and samples < 10000):
        plt.ylim(0, 10)
    elif(samples >= 10000 and samples < 100000):
        plt.ylim(0, 5)
    else:        
        plt.ylim(0, 100)
    plt.xlim(0, samples)
    plt.xlabel('Number of Samples', fontsize=14)
    plt.ylabel('Percent Error (%)', fontsize=14)
    plt.title('Percent Error of Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.show()

def visualizePiSubplot(samples):
    xValues, yValues, errorValues = generatePiData(samples)
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    if(samples >= 50 and samples < 100):
        ax1.set_ylim(2.5, 3.5)
    elif(samples >= 100 and samples < 1000):
        ax1.set_ylim(2.6, 4)
    elif(samples >= 1000 and samples < 100000):
        ax1.set_ylim(3, 3.3)
    elif(samples >= 100000 and samples < 1000000):
        ax1.set_ylim(3.1, 3.2)
    elif(samples >= 1000000):
        ax1.set_ylim(3.12, 3.15)
    else:
        ax1.set_ylim(0, 6)
    ax1.set_xlim(0, samples)
    ax1.set_xlabel('Number of Samples', fontsize=14)
    ax1.set_ylabel('Estimated Value of Pi', fontsize=14)
    ax1.set_title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    ax1.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')
    ax1.legend()
    ax1.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    ax2.plot(xValues, errorValues, color='red', linestyle='-', linewidth=2, markersize=3)
    if(samples >= 100 and samples < 400):
        ax2.set_ylim(0, 40)
    elif(samples >= 400 and samples < 600):
        ax2.set_ylim(0, 30)
    elif(samples >= 600 and samples < 1000):
        ax2.set_ylim(0, 20)
    elif(samples >= 1000 and samples < 10000):
        ax2.set_ylim(0, 10)
    elif(samples >= 10000 and samples < 100000):
        ax2.set_ylim(0, 5)
    elif(samples >= 100000):
        ax2.set_ylim(0, 1)
    ax2.set_xlim(0, samples)
    ax2.set_xlabel('Number of Samples', fontsize=14)
    ax2.set_ylabel('Percent Error (%)', fontsize=14)
    ax2.set_title('Percent Error of Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    ax2.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    plt.tight_layout()
    plt.show()