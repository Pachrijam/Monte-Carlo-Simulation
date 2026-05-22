import math
import matplotlib.pyplot as plt
from calculate import monte_carlo_pi

def visualizeOverTime(samples):
    xValues = []
    yValues = []

    # start at 1 to avoid zero-sample calls; match x-axis limit
    hits = 0
    for num_samples in range(1, samples + 1):
        x, y = __import__('random').random(), __import__('random').random()
        hits += 1 if x**2 + y**2 <= 1 else 0
        pi_estimate = 4 * hits / num_samples
        xValues.append(num_samples)
        yValues.append(pi_estimate)

    
    plt.style.use('dark_background')
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    plt.plot(xValues, yValues, color='red', linestyle='-', linewidth=2, markersize=3)
    # Automatically adjust y-axis limits based on the number of samples
    if(samples >= 50 and samples < 100):
        plt.ylim(2.5,3.5)
    elif(samples >= 100 and samples < 1000):
        plt.ylim(2.6,4)
    elif(samples >= 1000 and samples < 100000):
        plt.ylim(3,3.3)
    elif(samples >= 100000 and samples < 1000000):
        plt.ylim(3.1,3.2)
    elif(samples >= 1000000):
        plt.ylim(3.12,3.15)
    else:
        plt.ylim(0,6)
    plt.xlim(0, samples)
    plt.xlabel('Number of Samples')
    plt.ylabel('Estimated Value of Pi')
    plt.title('Monte Carlo Estimation of Pi', fontsize=14, fontweight='bold')
    plt.axhline(y=math.pi, color='blue', linestyle='--', label='Actual value of Pi')
    plt.legend()
    plt.show()
