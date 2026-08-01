import math
import numpy as np
from utils.exceptions import safe_float, safe_choice, safe_int
from utils.export_csv import integration_results_csv
from utils.export_json import integration_results_json
from visualizations.visualizationInt import visualizeIntEstimates, visualizeIntPercentError, visualizeIntSubplot
from calculators.calculate_confidence import confidence_interval

def run_int() -> None:
    print("You have selected option 1: Estimate the integral of a function using Monte Carlo integration.")
    
    integrand_functions: dict = {
        '1': ("x^2", lambda x: x ** 2),
        '2': ("sin(x)", math.sin),
        '3': ("exp(-x^2)", lambda x: math.exp(-x ** 2)),
        '4': ("1 / (1 + x^2)", lambda x: 1 / (1 + x ** 2)),
        '5': ("cos(x)", math.cos),
        '6': ("log(abs(x) + 1)", lambda x: math.log(abs(x) + 1)),
    }
    
    print("------------------------------------------------------------------------\nChoose a function to integrate:")
    for key, (name, _) in integrand_functions.items():
        print(f"{key}. {name}")
    function_choice = safe_choice("Enter the number of the function: ", list(integrand_functions.keys()))
    
    function_name: str
    integrand: callable
    function_name, integrand = integrand_functions[function_choice]
    
    lower_bound = safe_float("Enter the lower bound of the integral: ")
    upper_bound = safe_float("Enter the upper bound of the integral: ")
    while upper_bound <= lower_bound:
        print("Upper bound must be greater than lower bound.")
        upper_bound = safe_float("Enter the upper bound: ")
    
    integration_samples = safe_int("Enter the number of samples for the integral estimate: ", min_val=1, max_val=10000000)
        
    integral_estimate, confidence_intervals = calculate_monte_carlo_integration(integrand, lower_bound, upper_bound, integration_samples)
    print(f"------------------------------------------------------\nEstimated integral of {function_name} from {lower_bound} to {upper_bound}: {integral_estimate}")
    for ci in confidence_intervals:
        print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']}, lower={ci['lower']}, upper={ci['upper']}, ME={ci['margin_of_error']}")
    
    export_int_choice = safe_choice("------------------------------------------------------\nWould you like to export the integration results? (yes/no): ", ['yes', 'y', 'no', 'n'])
    if export_int_choice in ['yes', 'y']:
        integration_results_json(function_name, lower_bound, upper_bound, integration_samples, integral_estimate, confidence_intervals)
        integration_results_csv(function_name, lower_bound, upper_bound, integration_samples, integral_estimate, confidence_intervals)
    
    int_vis_choice = safe_choice("------------------------------------------------------\nWould you like a visualization of the integral estimates, error, or a combined subplot? (Enter 'estimates', 'error', 'subplot', or 'no'): ", ['estimates', 'error', 'subplot', 'no', 'n'])
    
    if int_vis_choice in ['estimates', 'error', 'subplot']:
        if int_vis_choice == 'estimates':
            visualizeIntEstimates(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'error':
            visualizeIntPercentError(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'subplot':
            visualizeIntSubplot(integration_samples, integrand, lower_bound, upper_bound)


def calculate_monte_carlo_integration(func, a, b, n):
    x = np.random.uniform(a, b, n)

    try:
        fx = func(x)
    except TypeError:
        fx = np.array([func(xi) for xi in x], dtype=float)

    average_fx = np.mean(fx)

    integral_estimate = (b - a) * average_fx
    per_sample = (b - a) * fx
    confidence_intervals = [confidence_interval(per_sample, confidence=conf) for conf in (0.90, 0.95, 0.99)]
    return integral_estimate, confidence_intervals
