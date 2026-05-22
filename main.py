import random
from calculate import monte_carlo_pi
from calculate import percent_error


print("Estimating the value of pi using the Monte Carlo method.\nHow many random samples would you like to use?")
num_samples = int(input())
monte_carlo_result = monte_carlo_pi(num_samples)
error_percentage = percent_error(num_samples)

print("Estimated value of π: " + str(monte_carlo_result))
print("Percent error: " + str(error_percentage) + "%")