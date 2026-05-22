import math
import matplotlib.pyplot as plt
from calculate import monte_carlo_pi

def visualizeOverTime(samples):
    xValues = []
    yValues = []

    # start at 1 to avoid zero-sample calls; match x-axis limit
    for num_samples in range(1, samples + 1):
        pi_estimate = monte_carlo_pi(num_samples)
        xValues.append(num_samples)
        yValues.append(pi_estimate)

    plt.style.use('dark_background')
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    plt.xlim(0, samples)
    plt.ylim(1, 5)
    plt.xlabel('Number of Samples')
    plt.ylabel('Estimated Value of Pi')
    plt.title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')
    plt.legend()
    plt.show()
