import random
import matplotlib.pyplot as plt
from calculatePI import monte_carlo_pi, percent_error
from visualization import visualize_data


#Main
print("How many samples to use for Monte Carlo estimation of Pi?")
num_samples = int(input())
print("Estimated value of pi: {:.6f}".format(monte_carlo_pi(num_samples)))
print("Simulation Percentage Error: {:.2f}%".format(percent_error(num_samples)))