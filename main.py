import random
from calculate import monte_carlo_pi, percent_error
from visualization import visualizeEstimates, visualizePercentError, visualizeSubplot
from confidence import confidence_interval

print("Estimating the value of pi using the Monte Carlo method...\nHow many random samples would you like to use?")
num_samples = int(input())

while num_samples > 10000000 or num_samples <= 0:
    print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
    num_samples = int(input())
else:
    monte_carlo_result = monte_carlo_pi(num_samples)
    error_percentage = percent_error(num_samples)
    
    runs = 50
    samples_per_run = 100000
    estimates = [monte_carlo_pi(samples_per_run) for _ in range(runs)]
    for conf in [0.90, 0.95, 0.99]:
        ci = confidence_interval(estimates, confidence=conf)
        print(f"------------------------------------------------------\n{int(conf*100)}% Confidence Interval:")
        print(f"Mean: {ci['mean']}")
        print(f"Range: ({ci['lower']}, {ci['upper']})")

print(f"------------------------------------------------------\nEstimated value of π: {monte_carlo_result}\nPercent error: {error_percentage}%")
print("------------------------------------------------------\nWould you like a visualization of the estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot')")

visualization_choice = input().lower()
while visualization_choice not in ['estimates', 'error', 'subplot']:
    print("Please enter 'estimates', 'error', or 'subplot' to choose a visualization.")
    visualization_choice = input().lower()

if visualization_choice == 'estimates':
    visualizeEstimates(num_samples)
elif visualization_choice == 'error':
    visualizePercentError(num_samples)
elif visualization_choice == 'subplot':
    visualizeSubplot(num_samples)