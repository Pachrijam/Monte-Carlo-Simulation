import random
import math
from calculatePi import monte_carlo_pi, percent_error
from visualizationPi import visualizePiEstimates, visualizePiPercentError, visualizePiSubplot
from confidence import confidence_interval
from calculateInt import monte_carlo_integration
from visualizationInt import visualizeIntEstimates, visualizeIntPercentError, visualizeIntSubplot
from export import export_pi_results, export_integration_results

# European options (Black-Scholes Monte Carlo)
# This import is optional during development if the module is not yet present.
try:
    from european_options import monte_carlo_european, black_scholes_price
    _HAS_EUROPEAN = True
except Exception:
    _HAS_EUROPEAN = False


def get_menu_choice() -> int:
    """
    Display menu and get user's simulation choice.
    
    Returns:
        int: User's menu selection (1-12)
    """
    print("--------------------------------<<MENU>>--------------------------------\nSELECT AN OPTION FROM BELOW:\n------------------------------------------------------------------------")
    print("""1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of π using the Monte Carlo method
3. Confidence Intervals and Statistical Analysis
4. Visualizations
5. Variance Reduction Techniques
6. Markov Chain Monte Carlo (MCMC) Methods
7. PDE and SDE Solvers
8. Sequential Monte Carlo Analysis (particle filters)
9. Rare event and Tail Risk Simulation
10. (reserved)
11. European Option Pricing (Black-Scholes Monte Carlo)
12. Exit
------------------------------------------------------------------------"""
    )
    
    print("Enter the number of the simulation you would like to run (1-12):") 
    sim_choice: int = int(input())
    return sim_choice


def handle_monte_carlo_integration() -> None:
    """
    Handle Monte Carlo integration simulation.
    Prompts user at start and end of method.
    """
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
    print("Enter the number of the function:")
    function_choice: str = input()
    while function_choice not in integrand_functions:
        print("Please enter a valid function number.")
        function_choice = input()
    
    function_name: str
    integrand: callable
    function_name, integrand = integrand_functions[function_choice]
    
    print("Enter the lower bound of the integral:")
    lower_bound: float = float(input())
    print("Enter the upper bound of the integral:")
    upper_bound: float = float(input())
    while float(upper_bound) <= float(lower_bound):
        print("Upper bound must be greater than lower bound. Enter the upper bound:")
        upper_bound = float(input())
    
    print("Enter the number of samples for the integral estimate:")
    integration_samples: int = int(input())
    while integration_samples > 10000000 or integration_samples <= 0:
        print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
        integration_samples = int(input())
    
    integral_estimate: float = monte_carlo_integration(integrand, lower_bound, upper_bound, integration_samples)
    print(f"------------------------------------------------------\nEstimated integral of {function_name} from {lower_bound} to {upper_bound}: {integral_estimate}")
    
    # Prompt at end of method
    print("------------------------------------------------------\nWould you like to export the integration results? (yes/no)")
    export_int_choice: str = input().lower()
    while export_int_choice not in ['yes', 'y', 'no', 'n']:
        print("Please enter 'yes' or 'no'.")
        export_int_choice = input().lower()
    if export_int_choice in ['yes', 'y']:
        export_integration_results(function_name, lower_bound, upper_bound, integration_samples, integral_estimate)
    
    print("------------------------------------------------------\nWould you like a visualization of the integral estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot'[...")
    int_vis_choice: str = input().lower()
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


def handle_pi_estimation() -> None:
    """
    Handle Pi estimation simulation.
    Prompts user at start and end of method.
    """
    print("You have selected option 2: Estimate the value of π using the Monte Carlo method.")
    
    print("------------------------------------------------------------------------\nHow many random samples would you like to use to estimate π?")
    num_samples: int = int(input())
    
    while num_samples > 10000000 or num_samples <= 0:
        print("Please enter a number of samples less than or equal to 10,000,000 and greater than 0.")
        num_samples = int(input())
    
    monte_carlo_result: float = monte_carlo_pi(num_samples)
    error_percentage: float = percent_error(num_samples)
    
    runs: int = 50
    samples_per_run: int = 100000
    estimates: list = [monte_carlo_pi(samples_per_run) for _ in range(runs)]
    confidence_intervals: list = []
    for conf in [0.90, 0.95, 0.99]:
        ci: dict = confidence_interval(estimates, confidence=conf)
        confidence_intervals.append(ci)
        print(f"------------------------------------------------------\n{int(conf*100)}% Confidence Interval:")
        print(f"Mean: {ci['mean']}")
        print(f"Range: ({ci['lower']}, {ci['upper']})")
    
    print(f"------------------------------------------------------\nEstimated value of π: {monte_carlo_result}\nPercent error: {error_percentage}%")
    
    # Prompt at end of method
    print("------------------------------------------------------\nWould you like to export the Pi estimation results? (yes/no)")
    export_pi_choice: str = input().lower()
    while export_pi_choice not in ['yes', 'y', 'no', 'n']:
        print("Please enter 'yes' or 'no'.")
        export_pi_choice = input().lower()
    if export_pi_choice in ['yes', 'y']:
        export_pi_results(num_samples, monte_carlo_result, error_percentage, confidence_intervals)
    
    print("------------------------------------------------------\nWould you like a visualization of the estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot')")
    visualization_choice: str = input().lower()
    while visualization_choice not in ['estimates', 'error', 'subplot', 'no', 'n']:
        print("Please enter 'estimates', 'error', 'subplot' or 'no'.")
        visualization_choice = input().lower()
    
    if visualization_choice in ['estimates', 'error', 'subplot']:
        if visualization_choice == 'estimates':
            visualizePiEstimates(num_samples)
        elif visualization_choice == 'error':
            visualizePiPercentError(num_samples)
        elif visualization_choice == 'subplot':
            visualizePiSubplot(num_samples)


def handle_confidence_intervals() -> None:
    """
    Handle Confidence Intervals and Statistical Analysis.
    """
    print("You have selected option 3: Confidence Intervals and Statistical Analysis.")
    print("This feature is under development.")


def handle_visualizations() -> None:
    """
    Handle Visualizations option.
    """
    print("You have selected option 4: Visualizations.")
    print("This feature is under development.")


def handle_variance_reduction() -> None:
    """
    Handle Variance Reduction Techniques.
    """
    print("You have selected option 5: Variance Reduction Techniques.")
    print("This feature is under development.")


def handle_mcmc() -> None:
    """
    Handle Markov Chain Monte Carlo (MCMC) Methods.
    """
    print("You have selected option 6: Markov Chain Monte Carlo (MCMC) Methods.")
    print("This feature is under development.")


def handle_pde_sde() -> None:
    """
    Handle PDE and SDE Solvers.
    """
    print("You have selected option 7: PDE and SDE Solvers.")
    print("This feature is under development.")


def handle_sequential_monte_carlo() -> None:
    """
    Handle Sequential Monte Carlo Analysis (particle filters).
    """
    print("You have selected option 8: Sequential Monte Carlo Analysis (particle filters).")
    print("This feature is under development.")


def handle_rare_event() -> None:
    """
    Handle Rare event and Tail Risk Simulation.
    """
    print("You have selected option 9: Rare event and Tail Risk Simulation.")
    print("This feature is under development.")


def handle_european_options() -> None:
    """
    Handle European Option Pricing using Monte Carlo under Black-Scholes.
    """
    if not _HAS_EUROPEAN:
        print("European option pricing module not available (simulations.european_options). Please add it to the project to use this feature.")
        return

    print("You have selected option 11: European Option Pricing (Black-Scholes Monte Carlo).")

    def _read_float(prompt: str, positive: bool = False) -> float:
        while True:
            try:
                v = float(input(prompt))
                if positive and v <= 0:
                    print("Please enter a positive value.")
                    continue
                return v
            except ValueError:
                print("Invalid number, please try again.")

    S0 = _read_float("Enter initial stock price S0 (e.g., 100): ", positive=True)
    K = _read_float("Enter strike price K (e.g., 100): ", positive=True)
    T = _read_float("Enter time to maturity T in years (e.g., 1): ", positive=True)
    r = _read_float("Enter risk-free rate r as decimal (e.g., 0.01): ")
    sigma = _read_float("Enter volatility sigma as decimal (e.g., 0.2): ", positive=True)

    option: str = "call"
    print("Enter option type ('call' or 'put') [call]: ")
    opt_input = input().strip().lower()
    if opt_input in ['call', 'put']:
        option = opt_input

    print("Enter number of Monte Carlo simulations (n_sim) [20000]: ")
    try:
        n_sim = int(input())
    except Exception:
        n_sim = 20000
    if n_sim <= 0:
        n_sim = 20000

    print("Use antithetic variates? (yes/no) [no]: ")
    antithetic = input().strip().lower() in ['yes', 'y']
    print("Use control variate? (yes/no) [no]: ")
    control_variate = input().strip().lower() in ['yes', 'y']

    print("Enter random seed (integer) or leave blank for random: ")
    seed_input = input().strip()
    seed = int(seed_input) if seed_input.isdigit() else None

    mc_price, mc_se = monte_carlo_european(S0, K, T, r, sigma, option=option, n_sim=n_sim, antithetic=antithetic, control_variate=control_variate, seed=seed)
    bs_price = black_scholes_price(S0, K, T, r, sigma, option)

    print(f"------------------------------------------------------\nMonte Carlo estimated price: {mc_price} (SE: {mc_se})")
    print(f"Black-Scholes closed-form price: {bs_price}")


def main() -> None:
    """
    Main application loop.
    Handles menu selection and routing to appropriate simulation methods.
    """
    while True:
        sim_choice: int = get_menu_choice()
        
        if sim_choice == 12:
            print("------------------------------------------------------------------------\nExiting the program. Thank you!")
            break
        elif sim_choice == 1:
            handle_monte_carlo_integration()
        elif sim_choice == 2:
            handle_pi_estimation()
        elif sim_choice == 3:
            handle_confidence_intervals()
        elif sim_choice == 4:
            handle_visualizations()
        elif sim_choice == 5:
            handle_variance_reduction()
        elif sim_choice == 6:
            handle_mcmc()
        elif sim_choice == 7:
            handle_pde_sde()
        elif sim_choice == 8:
            handle_sequential_monte_carlo()
        elif sim_choice == 9:
            handle_rare_event()
        elif sim_choice == 11:
            handle_european_options()
        else:
            print("Invalid choice. Please select a number between 1 and 12.")


if __name__ == "__main__":
    main()
