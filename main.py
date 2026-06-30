import random
import math
from calculatePi import monte_carlo_pi, percent_error
from visualizationPi import visualizePiEstimates, visualizePiPercentError, visualizePiSubplot
from confidence import confidence_interval
from calculateInt import monte_carlo_integration
from visualizationInt import visualizeIntEstimates, visualizeIntPercentError, visualizeIntSubplot
from export import export_pi_results, export_integration_results

print("--------------------------------<<MENU>>--------------------------------\nSELECT AN OPTION FROM BELOW:")
print("""
1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of π using the Monte Carlo method
3. Confidence Intervals and Statistical Analysis
4. Visualizations
5. Variance Reduction Techniques
6. Markov Chain Monte Carlo (MCMC) Methods
7. PDE and SDE Solvers
8. Sequential Monte Carlo Analysis (particle filters)
9. Rare event and Tail Risk Simulation
10. Exit
"""
    )

integrate_choice = int(input())


### fix the code below to handle new menu selection

integrate_choice = input().lower()
while integrate_choice not in ['yes', 'y', 'no', 'n']:
    print("Please enter 'yes' or 'no'.")
    integrate_choice = input().lower()

if integrate_choice in ['yes', 'y']:
    integrand_functions = {
        '1': ("x^2", lambda x: x ** 2),
        '2': ("sin(x)", math.sin),
        '3': ("exp(-x^2)", lambda x: math.exp(-x ** 2)),
        '4': ("1 / (1 + x^2)", lambda x: 1 / (1 + x ** 2)),
        '5': ("cos(x)", math.cos),
        '6': ("log(abs(x) + 1)", lambda x: math.log(abs(x) + 1)),
    }
    print("Choose a function to integrate:")
    for key, (name, _) in integrand_functions.items():
        print(f"{key}. {name}")
    print("Enter the number of the function:")
    function_choice = input()
    while function_choice not in integrand_functions:
        print("Please enter a valid function number.")
        function_choice = input()
    function_name, integrand = integrand_functions[function_choice]
    print("Enter the lower bound of the integral:")
    lower_bound = float(input())
    print("Enter the upper bound of the integral:")
    upper_bound = float(input())
    while float(upper_bound) <= float(lower_bound):
        print("Upper bound must be greater than lower bound. Enter the upper bound:")
        upper_bound = float(input())
    print("Enter the number of samples for the integral estimate:")
    integration_samples = int(input())
    while integration_samples > 10000000 or integration_samples <= 0:
        print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
        integration_samples = int(input())
    integral_estimate = monte_carlo_integration(integrand, lower_bound, upper_bound, integration_samples)
    print(f"------------------------------------------------------\nEstimated integral of {function_name} from {lower_bound} to {upper_bound}: {integral_estimate}")

    print("------------------------------------------------------\nWould you like to export the integration results? (yes/no)")
    export_int_choice = input().lower()
    if export_int_choice in ['yes', 'y']:
        export_integration_results(function_name, lower_bound, upper_bound, integration_samples, integral_estimate)
    while(export_int_choice not in ['yes', 'y', 'no', 'n']):
        print("Please enter 'yes' or 'no'.")
        export_int_choice = input().lower()
    print("------------------------------------------------------\nWould you like a visualization of the integral estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot')")
    int_vis_choice = input().lower()
    while int_vis_choice not in ['estimates', 'error', 'subplot', 'no', 'n']:
        print("Please enter 'estimates', 'error', 'subplot' or 'no'.")
        int_vis_choice = input().lower()

    if int_vis_choice in ['estimates', 'error', 'subplot']:
        if int_vis_choice == 'estimates':
            visualizeIntEstimates(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'error':
            visualizeIntPercentError(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'subplot':
            visualizeIntSubplot(integration_samples, integrand, lower_bound, upper_bound)


print("------------------------------------------------------\nWould you like to estimate π using the Monte Carlo method? (yes/no)")
pi_choice = input().lower()
if pi_choice not in ['yes', 'y']:
    print("------------------------------------------------------\nExiting the program. Thank you!")
    exit()

print("How many random samples would you like to use to estimate π?")
num_samples = int(input())

while num_samples > 10000000 or num_samples <= 0:
    print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
    num_samples = int(input())

monte_carlo_result = monte_carlo_pi(num_samples)
error_percentage = percent_error(num_samples)

runs = 50
samples_per_run = 100000
estimates = [monte_carlo_pi(samples_per_run) for _ in range(runs)]
confidence_intervals = []
for conf in [0.90, 0.95, 0.99]:
    ci = confidence_interval(estimates, confidence=conf)
    confidence_intervals.append(ci)
    print(f"------------------------------------------------------\n{int(conf*100)}% Confidence Interval:")
    print(f"Mean: {ci['mean']}")
    print(f"Range: ({ci['lower']}, {ci['upper']})")

print(f"------------------------------------------------------\nEstimated value of π: {monte_carlo_result}\nPercent error: {error_percentage}%")

print("------------------------------------------------------\nWould you like to export the Pi estimation results? (yes/no)")
export_pi_choice = input().lower()
if export_pi_choice in ['yes', 'y']:
    export_pi_results(num_samples, monte_carlo_result, error_percentage, confidence_intervals)
print("------------------------------------------------------\nWould you like a visualization of the estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot')")

visualization_choice = input().lower()
while visualization_choice not in ['estimates', 'error', 'subplot']:
    print("Please enter 'estimates', 'error', or 'subplot' to choose a visualization.")
    visualization_choice = input().lower()

if visualization_choice == 'estimates':
    visualizePiEstimates(num_samples)
elif visualization_choice == 'error':
    visualizePiPercentError(num_samples)
elif visualization_choice == 'subplot':
    visualizePiSubplot(num_samples)