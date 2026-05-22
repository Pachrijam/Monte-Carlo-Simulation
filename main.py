import random
from calculate import monte_carlo_pi
from calculate import percent_error
from visualization import visualizeOverTime

print("Estimating the value of pi using the Monte Carlo method...\nHow many random samples would you like to use?")
num_samples = int(input())

while num_samples > 10000000 or num_samples <= 0:
    print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
    num_samples = int(input())
else:
    monte_carlo_result = monte_carlo_pi(num_samples)
    error_percentage = percent_error(num_samples)

print(f"Estimated value of π: {monte_carlo_result}\nPercent error: {error_percentage}%")
visualizeOverTime(num_samples)