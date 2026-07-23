import math
import numpy as np
from calculate_pi import monte_carlo_pi, percent_error
from visualizationPi import visualizePiEstimates, visualizePiPercentError, visualizePiSubplot
from calculate_confidence import confidence_interval
from calculate_int import calculate_monte_carlo_integration
from visualizationInt import visualizeIntEstimates, visualizeIntPercentError, visualizeIntSubplot
from export_json import pi_results_json, integration_results_json, mcmc_results_json, european_option_results_json, pde_sde_results_json, rare_event_results_json
from export_csv import pi_results_csv, integration_results_csv, mcmc_results_csv, european_option_results_csv, pde_sde_results_csv, rare_event_results_csv
from calculate_european_options import monte_carlo_european, black_scholes_price
from calculate_mcmc_bayes import metropolis_hastings, posterior_summary
from calculate_pde_sde import monte_carlo_pde_solution, monte_carlo_sde_expectation
from visualizationMCMC import trace_plot, acf_plot, acf_trace_subplot
from visualizationPDE_SDE import visualize_pde_solution, visualize_sde_paths, visualize_pde_sde_subplot
from calculate_rare_events import estimate_tail_probability_naive, importance_sampling_normal_tail, cross_entropy_importance_sampling
from visualizationRareEvents import visualize_rare_event_probability
from calculate_sequential import linear_gaussian_filter, nonlinear_tracking_filter, state_estimate, state_variance
from visualizationSequential import visualize_particle_trajectories, visualize_particle_weights, visualize_effective_sample_size, visualize_sequential_subplot


def get_menu_choice() -> int:
    print("--------------------------------<<MENU>>--------------------------------\nSELECT AN OPTION FROM BELOW:\n------------------------------------------------------------------------")
    print("""1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of pi using the Monte Carlo method
3. Variance Reduction Techniques
4. Markov Chain Monte Carlo (MCMC) Methods
5. PDE and SDE Solvers
6. Sequential Monte Carlo Analysis (particle filters)
7. Rare event and Tail Risk Simulation
8. European Option Pricing (Black-Scholes Monte Carlo)
9. Exit
------------------------------------------------------------------------""")
    
    sim_choice = int(input("Enter the number of the simulation you would like to run (1-9): "))
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
        
    integral_estimate: float = calculate_monte_carlo_integration(integrand, lower_bound, upper_bound, integration_samples)
    print(f"------------------------------------------------------\nEstimated integral of {function_name} from {lower_bound} to {upper_bound}: {integral_estimate}")
    
    export_int_choice = str(input("------------------------------------------------------\nWould you like to export the integration results? (yes/no): ")).lower()
    while export_int_choice not in ['yes', 'y', 'no', 'n']:
        export_int_choice = str(input("Please enter 'yes' or 'no'.")).lower()
    if export_int_choice in ['yes', 'y']:
        integration_results_json(function_name, lower_bound, upper_bound, integration_samples, integral_estimate)
        integration_results_csv(function_name, lower_bound, upper_bound, integration_samples, integral_estimate)
    
    int_vis_choice = str(input("------------------------------------------------------\nWould you like a visualization of the integral estimates, error, or a combined subplot? (Enter 'estimates', 'error', 'subplot', or 'no'): ")).lower()
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
    print("You have selected option 2: Estimate the value of pi using the Monte Carlo method.")
    num_samples = int(input("------------------------------------------------------------------------\nEnter the number of samples to estimate pi: "))
    
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
    
    print(f"------------------------------------------------------\nEstimated value of pi: {monte_carlo_result}\nPercent error: {error_percentage}%")
    
    export_pi_choice = str(input("------------------------------------------------------\nWould you like to export the Pi estimation results? (yes/no): ")).lower()
    while export_pi_choice not in ['yes', 'y', 'no', 'n']:
        export_pi_choice = str(input("Please enter 'yes' or 'no'.")).lower()
    if export_pi_choice in ['yes', 'y']:
        pi_results_json(num_samples, monte_carlo_result, error_percentage, confidence_intervals)
        pi_results_csv(num_samples, monte_carlo_result, error_percentage, confidence_intervals)
    
    visualization_choice = str(input("------------------------------------------------------\nWould you like a visualization of the estimates, error, or a combined subplot? (Enter 'estimates', 'error', 'subplot', or 'no'): ")).lower()
    while visualization_choice not in ['estimates', 'error', 'subplot', 'no', 'n']:
        visualization_choice = str(input("Please enter 'estimates', 'error', 'subplot' or 'no': ")).lower()
    
    if visualization_choice in ['estimates', 'error', 'subplot']:
        if visualization_choice == 'estimates':
            visualizePiEstimates(num_samples)
        elif visualization_choice == 'error':
            visualizePiPercentError(num_samples)
        elif visualization_choice == 'subplot':
            visualizePiSubplot(num_samples)


def variance_reduction() -> None:
    print("You have selected option 5: Variance Reduction Techniques.")
    print("This feature is under development.")


def mcmc() -> None:
    print("You have selected option 6: Markov Chain Monte Carlo (MCMC) Methods.")
    print("------------------------------------------------------------------------\nSelect an MCMC method to run:")
    print("""1. Metropolis-Hastings
2. Gibbs Sampling
3. Exit""")
    mcmc_choice = int(input("Enter the number of the MCMC method you would like to run (1-3): "))
    if mcmc_choice == 1:
        print("------------------------------------------------------------------------\nYou have selected Metropolis-Hastings.")
        def log_normal(x: np.ndarray) -> float:
            return -0.5 * np.sum(x ** 2) - (len(x) / 2) * np.log(2 * np.pi)
        dim = int(input("Enter the dimension of the target distribution (e.g., 2): "))
        while dim <= 0:
            dim = int(input("Please enter a positive integer for the dimension: "))
        num_samples = int(input("Enter the number of samples to generate (e.g., 1000): "))
        while num_samples <= 0 or num_samples > 1000000:
            num_samples = int(input("Please enter a positive integer less than or equal to 1,000,000 for the number of samples: "))
        proposal_std = float(input("Enter the standard deviation for the proposal distribution (e.g., 1.0): "))
        while proposal_std <= 0:
            proposal_std = float(input("Please enter a positive value for the standard deviation: "))
        burn_in = int(input("Enter the number of burn-in samples (e.g., 100): "))
        while burn_in < 0 or burn_in >= num_samples:
            burn_in = int(input("Please enter a non-negative integer less than the number of samples for burn-in: "))
        thin = int(input("Enter the thinning interval (e.g., 1 for no thinning): "))
        while thin <= 0:
            thin = int(input("Please enter a positive integer for the thinning interval: "))
        
        inital = np.zeros(dim)
        samples, acceptance_rate = metropolis_hastings(log_normal, inital, num_samples, proposal_std=proposal_std, burn_in=burn_in, thin=thin)
        
        print(f"------------------------------------------------------------------------\nMetropolis-Hastings completed. Acceptance rate: {acceptance_rate:.4f}")
        mean, lower, upper = posterior_summary(samples, cred=0.95)
        print(f"95% credible intervals for each dimension:")
        for i in range(dim):
            print(f"Dimension {i}: Mean={mean[i]:.4f},95% CI=({lower[i]:.4f}, {upper[i]:.4f})")

        trace_vis = str(input("------------------------------------------------------------------------\nWould you like to visualize the samples? (acf/trace/subplot/no): ")).lower()
        while trace_vis not in ['acf', 'trace', 'subplot', 'no', 'n']:
            trace_vis = str(input("Please enter 'acf', 'trace', 'subplot', or 'no'.")).lower()
        if trace_vis in ['acf'] and dim > 0:
            acf_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['trace'] and dim > 0:
            trace_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['subplot'] and dim > 0:
            acf_trace_subplot(samples, var_idx=0, show=True)
        export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the MCMC results? (yes/no): ")).lower()
        if export_choice in ['yes', 'y']:
            parameters = {
                "dimension": dim,
                "proposal_std": proposal_std,
                "burn_in": burn_in,
                "thin": thin
            }
            posterior_summary_data = []
            for i in range(dim):
                posterior_summary_data.append({
                    "parameter": f"Dimension {i}",
                    "mean": mean[i],
                    "median": np.median(samples[:, i]),
                    "lower": lower[i],
                    "upper": upper[i],
                    "std_dev": np.std(samples[:, i]),
                    "ci_lower": lower[i],
                    "ci_upper": upper[i],
                    "95% CI Lower": lower[i],
                    "95% CI Upper": lower[i]
                })
            mcmc_results_json("Metropolis-Hastings", parameters, num_samples, posterior_summary_data)
            mcmc_results_csv("Metropolis-Hastings", parameters, num_samples, posterior_summary_data)
    elif mcmc_choice == 2:    
        print("------------------------------------------------------------------------\nYou have selected Gibbs Sampling.")
        dim = int(input("Enter the dimension of the target distribution (e.g., 2): "))
        while dim <= 0:
            dim = int(input("Please enter a positive integer for the dimension: "))
        num_samples = int(input("Enter the number of samples to generate (e.g., 1000): "))
        while num_samples <= 0 or num_samples > 1000000:
            num_samples = int(input("Please enter a positive integer less than or equal to 1,000,000 for the number of samples: "))
        burn_in = int(input("Enter the number of burn-in samples (e.g., 100): "))
        while burn_in < 0 or burn_in >= num_samples:
            burn_in = int(input("Please enter a non-negative integer less than the number of samples for burn-in: "))
        thin = int(input("Enter the thinning interval (e.g., 1 for no thinning): "))
        while thin <= 0:
            thin = int(input("Please enter a positive integer for the thinning interval: "))

        def gibbs_standard_normal(dim: int, n_samples: int, burn_in: int = 0, thin: int = 1) -> np.ndarray:
            total = burn_in + n_samples * thin
            x = np.zeros(dim)
            samples = []
            for t in range(total):
                for i in range(dim):
                    x[i] = np.random.randn()
                if t >= burn_in and ((t - burn_in) % thin == 0):
                    samples.append(x.copy())
            return np.array(samples)

        samples = gibbs_standard_normal(dim, num_samples - burn_in if burn_in < num_samples else num_samples, burn_in=burn_in, thin=thin)
        print(f"------------------------------------------------------------------------\nGibbs sampling completed. Generated {samples.shape[0]} samples.")
        mean, lower, upper = posterior_summary(samples, cred=0.95)
        print(f"95% credible intervals for each dimension:")
        for i in range(dim):
            print(f"Dimension {i}: Mean={mean[i]:.4f},95% CI=({lower[i]:.4f}, {upper[i]:.4f})")
        trace_vis = str(input("------------------------------------------------------------------------\nWould you like to visualize the samples? (acf/trace/subplot/no): ")).lower()
        while trace_vis not in ['acf', 'trace', 'subplot', 'no', 'n']:
            trace_vis = str(input("Please enter 'acf', 'trace', 'subplot', or 'no'.")).lower()
        if trace_vis in ['acf'] and dim > 0:
            acf_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['trace'] and dim > 0:
            trace_plot(samples, var_idx=0, show=True)
        elif trace_vis in ['subplot'] and dim > 0:
            acf_trace_subplot(samples, var_idx=0, show=True)
        export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the MCMC results? (yes/no): ")).lower()
        if export_choice in ['yes', 'y']:
            parameters = {
                "dimension": dim,
                "burn_in": burn_in,
                "thin": thin
            }
            posterior_summary_data = []
            for i in range(dim):
                posterior_summary_data.append({
                    "parameter": f"Dimension {i}",
                    "mean": mean[i],
                    "median": np.median(samples[:, i]),
                    "lower": lower[i],
                    "upper": upper[i],
                    "std_dev": np.std(samples[:, i]),
                    "ci_lower": lower[i],
                    "ci_upper": upper[i],
                    "95% CI Lower": lower[i],
                    "95% CI Upper": lower[i]
                })
            mcmc_results_json("Gibbs Sampling", parameters, num_samples, posterior_summary_data)
            mcmc_results_csv("Gibbs Sampling", parameters, num_samples, posterior_summary_data)
    elif mcmc_choice == 3:
        print("------------------------------------------------------------------------\nExiting MCMC methods.")


def pde_sde() -> None:
    print("You have selected option 7: PDE and SDE Solvers.")
    solver_type = input("------------------------------------------------------------------------\nSelect a solver type [PDE/SDE]: ").strip().lower()
    if solver_type not in ['pde', 'sde']:
        print("Invalid solver type. Please enter 'PDE' or 'SDE'.")
        return

    if solver_type == 'pde':
        pde_functions = {
            '1': ("exp(-x^2)", lambda x: np.exp(-(x ** 2))),
            '2': ("x^2", lambda x: x ** 2),
            '3': ("sin(x)", lambda x: np.sin(x)),
            '4': ("cos(x)", lambda x: np.cos(x)),
        }
        print("Choose an initial condition:")
        for key, (name, _) in pde_functions.items():
            print(f"{key}. {name}")
        function_choice = input("Enter the number of the function: ").strip()
        while function_choice not in pde_functions:
            function_choice = input("Please enter a valid function number: ").strip()
        function_name, initial_condition = pde_functions[function_choice]
        x0 = float(input("Enter the spatial point x0: "))
        time_horizon = float(input("Enter the time horizon T: "))
        while time_horizon <= 0:
            time_horizon = float(input("Please enter a positive time horizon: "))
        sigma = float(input("Enter the diffusion coefficient sigma [1.0]: ") or "1.0")
        while sigma <= 0:
            sigma = float(input("Please enter a positive diffusion coefficient: "))
        n_paths = int(input("Enter the number of Monte Carlo paths [20000]: ") or "20000")
        while n_paths <= 0:
            n_paths = int(input("Please enter a positive number of Monte Carlo paths: "))
        seed_input = input("Enter random seed or leave blank for random: ").strip()
        seed = int(seed_input) if seed_input.isdigit() else None

        estimate, std_error = monte_carlo_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        print(f"------------------------------------------------------\nPDE Monte Carlo estimate for {function_name} at x={x0}, T={time_horizon}: {estimate:.6f} (SE: {std_error:.6f})")
        visualization_choice = input("Would you like to visualize the PDE result? (pde/subplot/no): ").strip().lower()
        while visualization_choice not in ['pde', 'subplot', 'no', 'n']:
            visualization_choice = input("Please enter 'pde', 'subplot', or 'no': ").strip().lower()
        if visualization_choice == 'pde':
            visualize_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        elif visualization_choice == 'subplot':
            visualize_pde_sde_subplot(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the PDE results? (yes/no): ")).lower()
        if export_choice in ['yes', 'y']:
            pde_sde_results_json("PDE", {"function": function_name, "x0": x0, "time_horizon": time_horizon, "n_paths": n_paths, "sigma": sigma}, n_paths, {"estimate": estimate, "std_error": std_error})
            pde_sde_results_csv("PDE", {"function": function_name, "x0": x0, "time_horizon": time_horizon, "n_paths": n_paths, "sigma": sigma}, n_paths, {"estimate": estimate, "std_error": std_error})
    
    elif solver_type == 'sde':
        initial_value = float(input("Enter the initial value X0: "))
        drift = float(input("Enter the drift coefficient mu [0.0]: ") or "0.0")
        diffusion = float(input("Enter the diffusion coefficient sigma [1.0]: ") or "1.0")
        while diffusion <= 0:
            diffusion = float(input("Please enter a positive diffusion coefficient: "))
        time_horizon = float(input("Enter the time horizon T: "))
        while time_horizon <= 0:
            time_horizon = float(input("Please enter a positive time horizon: "))
        n_steps = int(input("Enter the number of time steps [100]: ") or "100")
        while n_steps <= 0:
            n_steps = int(input("Please enter a positive number of time steps: "))
        n_paths = int(input("Enter the number of Monte Carlo paths [20000]: ") or "20000")
        while n_paths <= 0:
            n_paths = int(input("Please enter a positive number of Monte Carlo paths: "))
        seed_input = input("Enter random seed or leave blank for random: ").strip()
        seed = int(seed_input) if seed_input.isdigit() else None

        estimate, std_error = monte_carlo_sde_expectation(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
        print(f"------------------------------------------------------\nSDE Monte Carlo estimate at T={time_horizon}: {estimate:.6f} (SE: {std_error:.6f})")
        visualization_choice = input("Would you like to visualize the SDE result? (sde/subplot/no): ").strip().lower()
        while visualization_choice not in ['sde', 'subplot', 'no', 'n']:
            visualization_choice = input("Please enter 'sde', 'subplot', or 'no': ").strip().lower()
        if visualization_choice == 'sde':
            visualize_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
        elif visualization_choice == 'subplot':
            visualize_pde_sde_subplot(lambda x: np.exp(-(x ** 2)), 0.0, time_horizon, n_paths, sigma=diffusion, seed=seed)
        export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the SDE results? (yes/no): ")).lower()
        if export_choice in ['yes', 'y']:
            pde_sde_results_json("SDE", {"initial_value": initial_value, "drift": drift, "diffusion": diffusion, "time_horizon": time_horizon, "n_steps": n_steps, "n_paths": n_paths}, n_paths, {"estimate": estimate, "std_error": std_error})
            pde_sde_results_csv("SDE", {"initial_value": initial_value, "drift": drift, "diffusion": diffusion, "time_horizon": time_horizon, "n_steps": n_steps, "n_paths": n_paths}, n_paths, {"estimate": estimate, "std_error": std_error})


def sequential_monte_carlo() -> None:
    print("You have selected option 6: Sequential Monte Carlo Analysis (particle filters).")
    print("------------------------------------------------------------------------\nSelect a filter model to run:")
    print("""1. Linear Gaussian Filter
2. Nonlinear Tracking Filter
3. Exit""")
    smc_choice = int(input("Enter the number of the filter model (1-3): "))
    
    if smc_choice == 1:
        print("------------------------------------------------------------------------\nYou have selected Linear Gaussian Filter.")
        n_particles = int(input("Enter the number of particles [1000]: ") or "1000")
        while n_particles <= 0:
            n_particles = int(input("Please enter a positive number of particles: "))
        n_steps = int(input("Enter the number of time steps [50]: ") or "50")
        while n_steps <= 0:
            n_steps = int(input("Please enter a positive number of time steps: "))
        F = float(input("Enter the state transition coefficient F [1.0]: ") or "1.0")
        Q = float(input("Enter the process noise variance Q [1.0]: ") or "1.0")
        while Q <= 0:
            Q = float(input("Please enter a positive process noise variance: "))
        R = float(input("Enter the measurement noise variance R [1.0]: ") or "1.0")
        while R <= 0:
            R = float(input("Please enter a positive measurement noise variance: "))
        seed_input = input("Enter random seed or leave blank for random: ").strip()
        seed = int(seed_input) if seed_input.isdigit() else None
        
        true_state = 1.0
        observations = [true_state + np.sqrt(R) * np.random.randn() for _ in range(n_steps)]
        
        particle_history, weight_history = linear_gaussian_filter(observations, n_particles, F=F, Q=Q, R=R, seed=seed)
        
        print(f"------------------------------------------------------------------------\nLinear Gaussian Filter completed.")
        final_estimate = state_estimate(particle_history[-1], weight_history[-1])
        final_variance = state_variance(particle_history[-1], weight_history[-1], final_estimate)
        print(f"Final state estimate: {final_estimate:.6f}")
        print(f"Final state variance: {final_variance:.6f}")
        
        vis_choice = str(input("------------------------------------------------------------------------\nWould you like to visualize the filter results? (trajectories/weights/ess/subplot/no): ")).lower()
        while vis_choice not in ['trajectories', 'weights', 'ess', 'subplot', 'no', 'n']:
            vis_choice = str(input("Please enter 'trajectories', 'weights', 'ess', 'subplot', or 'no': ")).lower()
        if vis_choice == 'trajectories':
            visualize_particle_trajectories(particle_history, weight_history, observations)
        elif vis_choice == 'weights':
            visualize_particle_weights(weight_history)
        elif vis_choice == 'ess':
            visualize_effective_sample_size(weight_history)
        elif vis_choice == 'subplot':
            visualize_sequential_subplot(particle_history, weight_history, observations)
    
    elif smc_choice == 2:
        print("------------------------------------------------------------------------\nYou have selected Nonlinear Tracking Filter.")
        n_particles = int(input("Enter the number of particles [1000]: ") or "1000")
        while n_particles <= 0:
            n_particles = int(input("Please enter a positive number of particles: "))
        n_steps = int(input("Enter the number of time steps [50]: ") or "50")
        while n_steps <= 0:
            n_steps = int(input("Please enter a positive number of time steps: "))
        seed_input = input("Enter random seed or leave blank for random: ").strip()
        seed = int(seed_input) if seed_input.isdigit() else None
        
        true_states = np.zeros(n_steps)
        observations = np.zeros(n_steps)
        x = 0.1
        for t in range(n_steps):
            x = 0.5 * x + 25.0 * x / (1.0 + x ** 2) + 8.0 * np.cos(1.2 * (t + 1)) + np.sqrt(10) * np.random.randn()
            true_states[t] = x
            observations[t] = x ** 2 / 20.0 + np.random.randn()
        
        particle_history, weight_history = nonlinear_tracking_filter(observations, n_particles, seed=seed)
        
        print(f"------------------------------------------------------------------------\nNonlinear Tracking Filter completed.")
        final_estimate = state_estimate(particle_history[-1], weight_history[-1])
        final_variance = state_variance(particle_history[-1], weight_history[-1], final_estimate)
        print(f"Final state estimate: {final_estimate:.6f}")
        print(f"Final state variance: {final_variance:.6f}")
        
        vis_choice = str(input("------------------------------------------------------------------------\nWould you like to visualize the filter results? (trajectories/weights/ess/subplot/no): ")).lower()
        while vis_choice not in ['trajectories', 'weights', 'ess', 'subplot', 'no', 'n']:
            vis_choice = str(input("Please enter 'trajectories', 'weights', 'ess', 'subplot', or 'no': ")).lower()
        if vis_choice == 'trajectories':
            visualize_particle_trajectories(particle_history, weight_history, observations)
        elif vis_choice == 'weights':
            visualize_particle_weights(weight_history)
        elif vis_choice == 'ess':
            visualize_effective_sample_size(weight_history)
        elif vis_choice == 'subplot':
            visualize_sequential_subplot(particle_history, weight_history, observations)
    
    elif smc_choice == 3:
        print("------------------------------------------------------------------------\nExiting Sequential Monte Carlo analysis.")


def rare_event() -> None:
    print("You have selected option 9: Rare event and Tail Risk Simulation.")
    print("1. Naive Monte Carlo tail probability")
    print("2. Importance sampling with fixed tilt")
    print("3. Cross-entropy to find tilt + importance sampling")
    choice = input("Enter choice (1-3) or 'b' to go back: ").strip().lower()
    if choice == 'b':
        return
    try:
        threshold = float(input("Enter threshold for the sum of standard normals: ").strip())
    except Exception:
        print("Invalid threshold")
        return
    try:
        dim = int(input("Enter number of components (dim) [1]: ").strip() or "1")
    except Exception:
        dim = 1
    try:
        n_samples = int(input("Enter number of samples [100000]: ").strip() or "100000")
    except Exception:
        n_samples = 100000
    seed_input = input("Enter random seed (integer) or leave blank: ").strip()
    seed = int(seed_input) if seed_input.isdigit() else None
    method = "naive"
    tilt = None
    n_paths_for_export = n_samples
    if choice == '1':
        prob, se = estimate_tail_probability_naive(threshold, n_samples, dim=dim, seed=seed)
        method = "naive"
        print(f"Naive Monte Carlo estimate: {prob} (SE: {se})")
    elif choice == '2':
        try:
            tilt = float(input("Enter tilt (positive shift) for importance sampling [threshold/dim]: ").strip() or str(max(0.0, threshold / max(1, dim))))
        except Exception:
            tilt = max(0.0, threshold / max(1, dim))
        prob, se = importance_sampling_normal_tail(threshold, n_samples, dim=dim, tilt=tilt, seed=seed)
        method = "importance"
        print(f"Importance sampling estimate (tilt={tilt}): {prob} (SE: {se})")
    elif choice == '3':
        try:
            n_samples_ce = int(input("Enter samples for CE iterations [20000]: ").strip() or "20000")
        except Exception:
            n_samples_ce = 20000
        try:
            n_samples_final = int(input("Enter final importance sampling samples [100000]: ").strip() or "100000")
        except Exception:
            n_samples_final = 100000
        try:
            n_iters = int(input("Enter number of CE iterations [10]: ").strip() or "10")
        except Exception:
            n_iters = 10
        try:
            rho = float(input("Enter elite fraction rho (0.0-1.0) [0.01]: ").strip() or "0.01")
        except Exception:
            rho = 0.01
        prob, se, tilt = cross_entropy_importance_sampling(threshold, n_samples_ce, n_samples_final, dim=dim, n_iters=n_iters, rho=rho, seed=seed)
        method = "cross_entropy"
        n_paths_for_export = n_samples_final
        print(f"Cross-entropy found tilt: {tilt}")
        print(f"CE+Importance sampling estimate: {prob} (SE: {se})")
    else:
        print("Invalid selection")
        return
    export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the rare event results? (yes/no): ")).lower()
    while export_choice not in ['yes', 'y', 'no', 'n']:
        export_choice = str(input("Please enter 'yes' or 'no': ")).lower()
    if export_choice in ['yes', 'y']:
        rare_event_results_json(0.0, 0.0, 1.0, n_paths_for_export, threshold, prob)
        rare_event_results_csv(0.0, 0.0, 1.0, n_paths_for_export, threshold, prob)
    visualization_choice = str(input("Would you like to visualize the rare event probability estimate? (yes/no): ")).lower()
    while visualization_choice not in ['yes', 'y', 'no', 'n']:
        visualization_choice = str(input("Please enter 'yes' or 'no': ")).lower()
    if visualization_choice in ['yes', 'y']:
        visualize_rare_event_probability(0.0, 0.0, 1.0, n_paths_for_export, threshold, sigma=1.0, seed=seed)


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
    export_choice = str(input("------------------------------------------------------------------------\nWould you like to export the European option results? (yes/no): ")).lower()
    if export_choice in ['yes', 'y']:
        european_option_results_json(S0, K, T, r, sigma, n_sim, mc_price)
        european_option_results_csv(S0, K, T, r, sigma, n_sim, mc_price)


def main() -> None:
    while True:
        sim_choice: int = get_menu_choice()
        if sim_choice == 9:
            print("------------------------------------------------------------------------\nExiting the program. Thank you!")
            break
        elif sim_choice == 1:
            monte_carlo_integration()
        elif sim_choice == 2:
            pi_estimation()
        elif sim_choice == 3:
            variance_reduction()
        elif sim_choice == 4:
            mcmc()
        elif sim_choice == 5:
            pde_sde()
        elif sim_choice == 6:
            sequential_monte_carlo()
        elif sim_choice == 7:
            rare_event()
        elif sim_choice == 8:
            european_options()
        else:
            print("Invalid choice. Please select a number between 1 and 9.")


if __name__ == "__main__":
    main()
