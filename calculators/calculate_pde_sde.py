import numpy as np
from utils.exceptions import safe_choice, safe_float, safe_optional_float, safe_optional_int, safe_seed_input, safe_int
from visualizations.visualizationPDE_SDE import visualize_pde_sde_subplot, visualize_pde_solution, visualize_sde_paths
from utils.export_csv import pde_sde_results_csv
from utils.export_json import pde_sde_results_json
from calculators.calculate_confidence import confidence_interval

def run_pde_sde() -> None:
    print("You have selected option 7: PDE and SDE Solvers.")
    solver_type = safe_choice("------------------------------------------------------------------------\nSelect a solver type [PDE/SDE]: ", ['pde', 'sde'])

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
        function_choice = safe_choice("Enter the number of the function: ", list(pde_functions.keys()))
        function_name, initial_condition = pde_functions[function_choice]
        x0 = safe_float("Enter the spatial point x0: ")
        time_horizon = safe_float("Enter the time horizon T: ", min_val=0.0001)
        sigma = safe_optional_float("Enter the diffusion coefficient sigma [1.0]: ", default=1.0)
        while sigma <= 0:
            print("Diffusion coefficient must be positive.")
            sigma = safe_float("Enter the diffusion coefficient sigma: ", min_val=0.0001)
        n_paths = safe_optional_int("Enter the number of Monte Carlo paths [20000]: ", default=20000)
        while n_paths <= 0:
            print("Number of paths must be positive.")
            n_paths = safe_int("Enter the number of Monte Carlo paths: ", min_val=1)
        seed = safe_seed_input("Enter random seed or leave blank for random: ")

        estimate, std_error, confidence_intervals = monte_carlo_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        print(f"------------------------------------------------------\nPDE Monte Carlo estimate for {function_name} at x={x0}, T={time_horizon}: {estimate:.6f} (SE: {std_error:.6f})")
        for ci in confidence_intervals:
            print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']:.6f}, lower={ci['lower']:.6f}, upper={ci['upper']:.6f}, ME={ci['margin_of_error']:.6f}")
        visualization_choice = safe_choice("Would you like to visualize the PDE result? (pde/subplot/no): ", ['pde', 'subplot', 'no', 'n'])
        if visualization_choice == 'pde':
            visualize_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        elif visualization_choice == 'subplot':
            visualize_pde_sde_subplot(initial_condition, x0, time_horizon, n_paths, sigma=sigma, seed=seed)
        export_choice = safe_choice("------------------------------------------------------------------------\nWould you like to export the PDE results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_choice in ['yes', 'y']:
            pde_sde_results_json("PDE", {"function": function_name, "x0": x0, "time_horizon": time_horizon, "n_paths": n_paths, "sigma": sigma}, n_paths, {"estimate": estimate, "std_error": std_error}, confidence_intervals)
            pde_sde_results_csv("PDE", {"function": function_name, "x0": x0, "time_horizon": time_horizon, "n_paths": n_paths, "sigma": sigma}, n_paths, {"estimate": estimate, "std_error": std_error}, confidence_intervals)
    
    elif solver_type == 'sde':
        initial_value = safe_float("Enter the initial value X0: ")
        drift = safe_optional_float("Enter the drift coefficient mu [0.0]: ", default=0.0)
        diffusion = safe_optional_float("Enter the diffusion coefficient sigma [1.0]: ", default=1.0)
        while diffusion <= 0:
            print("Diffusion coefficient must be positive.")
            diffusion = safe_float("Enter the diffusion coefficient sigma: ", min_val=0.0001)
        time_horizon = safe_float("Enter the time horizon T: ", min_val=0.0001)
        n_steps = safe_optional_int("Enter the number of time steps [100]: ", default=100)
        while n_steps <= 0:
            print("Number of steps must be positive.")
            n_steps = safe_int("Enter the number of time steps: ", min_val=1)
        n_paths = safe_optional_int("Enter the number of Monte Carlo paths [20000]: ", default=20000)
        while n_paths <= 0:
            print("Number of paths must be positive.")
            n_paths = safe_int("Enter the number of Monte Carlo paths: ", min_val=1)
        seed = safe_seed_input("Enter random seed or leave blank for random: ")

        estimate, std_error, confidence_intervals = monte_carlo_sde_expectation(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
        print(f"------------------------------------------------------\nSDE Monte Carlo estimate at T={time_horizon}: {estimate:.6f} (SE: {std_error:.6f})")
        for ci in confidence_intervals:
            print(f"{int(ci['confidence_level']*100)}% CI: mean={ci['mean']:.6f}, lower={ci['lower']:.6f}, upper={ci['upper']:.6f}, ME={ci['margin_of_error']:.6f}")
        visualization_choice = safe_choice("Would you like to visualize the SDE result? (sde/subplot/no): ", ['sde', 'subplot', 'no', 'n'])
        if visualization_choice == 'sde':
            visualize_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
        elif visualization_choice == 'subplot':
            visualize_pde_sde_subplot(lambda x: np.exp(-(x ** 2)), 0.0, time_horizon, n_paths, sigma=diffusion, seed=seed)
        export_choice = safe_choice("------------------------------------------------------------------------\nWould you like to export the SDE results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_choice in ['yes', 'y']:
            pde_sde_results_json("SDE", {"initial_value": initial_value, "drift": drift, "diffusion": diffusion, "time_horizon": time_horizon, "n_steps": n_steps, "n_paths": n_paths}, n_paths, {"estimate": estimate, "std_error": std_error}, confidence_intervals)
            pde_sde_results_csv("SDE", {"initial_value": initial_value, "drift": drift, "diffusion": diffusion, "time_horizon": time_horizon, "n_steps": n_steps, "n_paths": n_paths}, n_paths, {"estimate": estimate, "std_error": std_error}, confidence_intervals)


def monte_carlo_pde_solution(initial_condition, x0, time_horizon, n_paths, sigma=1.0, seed=None):
    if time_horizon < 0:
        raise ValueError("time_horizon must be non-negative")
    if n_paths <= 0:
        raise ValueError("n_paths must be positive")

    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, np.sqrt(time_horizon), size=n_paths)
    terminal_values = np.asarray(initial_condition(x0 + sigma * noise), dtype=float)
    estimate = float(np.mean(terminal_values))
    std_error = float(np.std(terminal_values, ddof=1) / np.sqrt(n_paths))
    confidence_intervals = [confidence_interval(terminal_values, confidence=conf) for conf in (0.90, 0.95, 0.99)]
    return estimate, std_error, confidence_intervals


def simulate_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=None):
    if time_horizon < 0:
        raise ValueError("time_horizon must be non-negative")
    if n_steps <= 0:
        raise ValueError("n_steps must be positive")
    if n_paths <= 0:
        raise ValueError("n_paths must be positive")

    rng = np.random.default_rng(seed)
    dt = time_horizon / n_steps
    time_grid = np.linspace(0.0, time_horizon, n_steps + 1)
    paths = np.empty((n_paths, n_steps + 1), dtype=float)
    paths[:, 0] = initial_value

    for step in range(n_steps):
        noise = rng.normal(0.0, 1.0, size=n_paths)
        paths[:, step + 1] = paths[:, step] + drift * dt + diffusion * np.sqrt(dt) * noise

    return paths, time_grid


def monte_carlo_sde_expectation(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=None):
    paths, _ = simulate_sde_paths(initial_value, drift, diffusion, time_horizon, n_steps, n_paths, seed=seed)
    terminal_values = paths[:, -1]
    estimate = float(np.mean(terminal_values))
    std_error = float(np.std(terminal_values, ddof=1) / np.sqrt(n_paths))
    confidence_intervals = [confidence_interval(terminal_values, confidence=conf) for conf in (0.90, 0.95, 0.99)]
    return estimate, std_error, confidence_intervals