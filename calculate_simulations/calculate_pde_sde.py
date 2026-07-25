import numpy as np


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
    return estimate, std_error


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
    return estimate, std_error