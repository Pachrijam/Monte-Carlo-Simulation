import random
import math
from calculatePi import monte_carlo_pi, percent_error
from visualizationPi import visualizePiEstimates, visualizePiPercentError, visualizePiSubplot
from confidence import confidence_interval
from calculateInt import monte_carlo_integration as calculate_int
from visualizationInt import visualizeIntEstimates, visualizeIntPercentError, visualizeIntSubplot
from export import export_pi_results, export_integration_results
from european_options import monte_carlo_european, black_scholes_price
from mcmc_bayes import metropolis_hastings, gibbs_sampler, autocorrelation, effective_sample_size, posterior_summary, trace_plot, acf_plot, summarize_chain


def get_menu_choice() -> int:
    """
    Display menu and get user's simulation choice.
    
    Returns:
        int: User's menu selection (1-11)
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
10. European Option Pricing (Black-Scholes Monte Carlo)
11. Exit
------------------------------------------------------------------------"""
    )
    
    sim_choice = int(input("Enter the number of the simulation you would like to run (1-11): "))
    return sim_choice


def monte_carlo_integration() -> None:
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
    function_choice = input("Enter the number of the function: ").strip()
    
    while function_choice not in integrand_functions:
        print("Please enter a valid function number.")
        function_choice = input("Enter the number of the function: ").strip()
    
    function_name: str
    integrand: callable
    function_name, integrand = integrand_functions[function_choice]
    
    lower_bound = float(input("Enter the lower bound of the integral: "))
    upper_bound = float(input("Enter the upper bound of the integral: "))
    while upper_bound <= lower_bound:
        upper_bound = float(input("Upper bound must be greater than lower bound. Enter the upper bound: "))
    
    integration_samples = int(input("Enter the number of samples for the integral estimate: "))
    while integration_samples > 10000000 or integration_samples <= 0:
        integration_samples = int(input("Please enter a number of samples less than or equal to 10,000,000 and greater than 0."))
        
    integral_estimate: float = calculate_int(integrand, lower_bound, upper_bound, integration_samples)
    print(f"------------------------------------------------------\nEstimated integral of {function_name} from {lower_bound} to {upper_bound}: {integral_estimate}")
    
    export_int_choice = str(input("------------------------------------------------------\nWould you like to export the integration results? (yes/no): ")).lower()
    while export_int_choice not in ['yes', 'y', 'no', 'n']:
        export_int_choice = str(input("Please enter 'yes' or 'no'.")).lower()
    if export_int_choice in ['yes', 'y']:
        export_integration_results(function_name, lower_bound, upper_bound, integration_samples, integral_estimate)
    
    int_vis_choice = str(input("------------------------------------------------------\nWould you like a visualization of the integral estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot'): ")).lower()
    while int_vis_choice not in ['estimates', 'error', 'subplot', 'no', 'n']:
        int_vis_choice = str(input("Please enter 'estimates', 'error', 'subplot' or 'no'.")).lower()
    
    if int_vis_choice in ['estimates', 'error', 'subplot']:
        if int_vis_choice == 'estimates':
            visualizeIntEstimates(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'error':
            visualizeIntPercentError(integration_samples, integrand, lower_bound, upper_bound)
        elif int_vis_choice == 'subplot':
            visualizeIntSubplot(integration_samples, integrand, lower_bound, upper_bound)


def pi_estimation() -> None:
    print("You have selected option 2: Estimate the value of π using the Monte Carlo method.")
    num_samples = int(input("------------------------------------------------------------------------\nEnter the number of samples to estimate π: "))
    
    while num_samples > 10000000 or num_samples <= 0:
        num_samples = int(input("Please enter a number of samples less than or equal to 10,000,000 and greater than 0: "))
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
    
    export_pi_choice = str(input("------------------------------------------------------\nWould you like to export the Pi estimation results? (yes/no): ")).lower()
    while export_pi_choice not in ['yes', 'y', 'no', 'n']:
        export_pi_choice = str(input("Please enter 'yes' or 'no'.")).lower()
    if export_pi_choice in ['yes', 'y']:
        export_pi_results(num_samples, monte_carlo_result, error_percentage, confidence_intervals)
    
    visualization_choice = str(input("------------------------------------------------------\nWould you like a visualization of the estimates, error, or a combined subplot? (Enter 'estimates', 'error', or 'subplot'): ")).lower()
    while visualization_choice not in ['estimates', 'error', 'subplot', 'no', 'n']:
        visualization_choice = str(input("Please enter 'estimates', 'error', 'subplot' or 'no': ")).lower()
    
    if visualization_choice in ['estimates', 'error', 'subplot']:
        if visualization_choice == 'estimates':
            visualizePiEstimates(num_samples)
        elif visualization_choice == 'error':
            visualizePiPercentError(num_samples)
        elif visualization_choice == 'subplot':
            visualizePiSubplot(num_samples)


def confidence_intervals() -> None:
    """
    Handle Confidence Intervals and Statistical Analysis.
    """
    print("You have selected option 3: Confidence Intervals and Statistical Analysis.")


def visualizations() -> None:
    print("You have selected option 4: Visualizations. Please select a specific visualization type from the menu.\n------------------------------------------------------------------------")
    print("""1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of π using the Monte Carlo method
3. Confidence Intervals and Statistical Analysis
4. Visualizations
5. Variance Reduction Techniques
6. Markov Chain Monte Carlo (MCMC) Methods
7. PDE and SDE Solvers
8. Sequential Monte Carlo Analysis (particle filters)
9. Rare event and Tail Risk Simulation
10. European Option Pricing (Black-Scholes Monte Carlo)
------------------------------------------------------------------------"""
    )
    visualizations_choice = int(input("Enter the number of the visualization you would like to run (1-10): "))


def variance_reduction() -> None:
    """
    Handle Variance Reduction Techniques.
    """
    print("You have selected option 5: Variance Reduction Techniques.")
    print("This feature is under development.")


def mcmc() -> None:
    print("You have selected option 6: Markov Chain Monte Carlo (MCMC) Methods.")
    


def pde_sde() -> None:
    """
    Handle PDE and SDE Solvers.
    """
    print("You have selected option 7: PDE and SDE Solvers.")
    print("This feature is under development.")


def sequential_monte_carlo() -> None:
    """
    Handle Sequential Monte Carlo Analysis (particle filters).
    """
    print("You have selected option 8: Sequential Monte Carlo Analysis (particle filters).")
    print("This feature is under development.")


def rare_event() -> None:
    """
    Handle Rare event and Tail Risk Simulation.
    """
    print("You have selected option 9: Rare event and Tail Risk Simulation.")
    print("This feature is under development.")


def european_options() -> None:
    print("You have selected option 10: European Option Pricing (Black-Scholes Monte Carlo).\n------------------------------------------------------------------------")

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
    opt_input = input("Enter option type ('call' or 'put') [call]: ").strip().lower()
    if opt_input in ['call', 'put']:
        option = opt_input

    try:
        n_sim = int(input("Enter number of Monte Carlo simulations (n_sim) [20000]: "))
    except Exception:
        n_sim = 20000
    if n_sim <= 0:
        n_sim = 20000

    antithetic = input("Use antithetic variates? (yes/no) [no]: ").strip().lower() in ['yes', 'y']
    control_variate = input("Use control variate? (yes/no) [no]: ").strip().lower() in ['yes', 'y']
    seed_input = input("Enter random seed (integer) or leave blank for random: ").strip()
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
        
        if sim_choice == 11:
            print("------------------------------------------------------------------------\nExiting the program. Thank you!")
            break
        elif sim_choice == 1:
            monte_carlo_integration()
        elif sim_choice == 2:
            pi_estimation()
        elif sim_choice == 3:
            confidence_intervals()
        elif sim_choice == 4:
            visualizations()
        elif sim_choice == 5:
            variance_reduction()
        elif sim_choice == 6:
            mcmc()
        elif sim_choice == 7:
            pde_sde()
        elif sim_choice == 8:
            sequential_monte_carlo()
        elif sim_choice == 9:
            rare_event()
        elif sim_choice == 10:
            european_options()
        else:
            print("Invalid choice. Please select a number between 1 and 11.")


if __name__ == "__main__":
    main()
