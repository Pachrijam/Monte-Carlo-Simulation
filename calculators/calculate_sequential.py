import numpy as np
from utils.exceptions import safe_int, safe_optional_float, safe_optional_int, safe_float, safe_seed_input, safe_choice
from visualizations.visualizationSequential import visualize_particle_trajectories, visualize_particle_weights, visualize_effective_sample_size, visualize_sequential_subplot
from utils.export_csv import sequential_results_csv
from utils.export_json import sequential_results_json


def run_sequential() -> None:
    print("You have selected option 6: Sequential Monte Carlo Analysis (particle filters).")
    print("------------------------------------------------------------------------\nSelect a filter model to run:")
    print("""1. Linear Gaussian Filter
2. Nonlinear Tracking Filter""")
    smc_choice = safe_int("Enter the number of the filter model (1-2): ", min_val=1, max_val=2)
    
    if smc_choice == 1:
        print("------------------------------------------------------------------------\nYou have selected Linear Gaussian Filter.")
        n_particles = safe_optional_int("Enter the number of particles [1000]: ", default=1000)
        while n_particles <= 0:
            print("Number of particles must be positive.")
            n_particles = safe_int("Enter the number of particles: ", min_val=1)
        n_steps = safe_optional_int("Enter the number of time steps [50]: ", default=50)
        while n_steps <= 0:
            print("Number of steps must be positive.")
            n_steps = safe_int("Enter the number of time steps: ", min_val=1)
        F = safe_optional_float("Enter the state transition coefficient F [1.0]: ", default=1.0)
        Q = safe_optional_float("Enter the process noise variance Q [1.0]: ", default=1.0)
        while Q <= 0:
            print("Process noise variance must be positive.")
            Q = safe_float("Enter the process noise variance Q: ", min_val=0.0001)
        R = safe_optional_float("Enter the measurement noise variance R [1.0]: ", default=1.0)
        while R <= 0:
            print("Measurement noise variance must be positive.")
            R = safe_float("Enter the measurement noise variance R: ", min_val=0.0001)
        seed = safe_seed_input("Enter random seed or leave blank for random: ")
        
        true_state = 1.0
        observations = [true_state + np.sqrt(R) * np.random.randn() for _ in range(n_steps)]
        
        particle_history, weight_history = linear_gaussian_filter(observations, n_particles, F=F, Q=Q, R=R, seed=seed)
        
        print(f"------------------------------------------------------------------------\nLinear Gaussian Filter completed.")
        final_estimate = state_estimate(particle_history[-1], weight_history[-1])
        final_variance = state_variance(particle_history[-1], weight_history[-1], final_estimate)
        print(f"Final state estimate: {final_estimate:.6f}")
        print(f"Final state variance: {final_variance:.6f}")
        
        vis_choice = safe_choice("------------------------------------------------------------------------\nWould you like to visualize the filter results? (trajectories/weights/ess/subplot/no): ", ['trajectories', 'weights', 'ess', 'subplot', 'no', 'n'])
        if vis_choice == 'trajectories':
            visualize_particle_trajectories(particle_history, weight_history, observations)
        elif vis_choice == 'weights':
            visualize_particle_weights(weight_history)
        elif vis_choice == 'ess':
            visualize_effective_sample_size(weight_history)
        elif vis_choice == 'subplot':
            visualize_sequential_subplot(particle_history, weight_history, observations)
        export_option = safe_choice("------------------------------------------------------------------------\nWould you like to export the filter results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_option in ['yes', 'y']:
            sequential_results_json("Nonlinear Tracking Filter", {"n_particles": n_particles, "n_steps": n_steps}, len(particle_history), {"final_estimate": final_estimate, "final_variance": final_variance})
            sequential_results_csv("Nonlinear Tracking Filter", {"n_particles": n_particles, "n_steps": n_steps}, len(particle_history), {"final_estimate": final_estimate, "final_variance": final_variance})
    
    elif smc_choice == 2:
        print("------------------------------------------------------------------------\nYou have selected Nonlinear Tracking Filter.")
        n_particles = safe_optional_int("Enter the number of particles [1000]: ", default=1000)
        while n_particles <= 0:
            print("Number of particles must be positive.")
            n_particles = safe_int("Enter the number of particles: ", min_val=1)
        n_steps = safe_optional_int("Enter the number of time steps [50]: ", default=50)
        while n_steps <= 0:
            print("Number of steps must be positive.")
            n_steps = safe_int("Enter the number of time steps: ", min_val=1)
        seed = safe_seed_input("Enter random seed or leave blank for random: ")
        
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
        
        vis_choice = safe_choice("------------------------------------------------------------------------\nWould you like to visualize the filter results? (trajectories/weights/ess/subplot/no): ", ['trajectories', 'weights', 'ess', 'subplot', 'no', 'n'])
        if vis_choice == 'trajectories':
            visualize_particle_trajectories(particle_history, weight_history, observations)
        elif vis_choice == 'weights':
            visualize_particle_weights(weight_history)
        elif vis_choice == 'ess':
            visualize_effective_sample_size(weight_history)
        elif vis_choice == 'subplot':
            visualize_sequential_subplot(particle_history, weight_history, observations)
        export_option = safe_choice("------------------------------------------------------------------------\nWould you like to export the filter results? (yes/no): ", ['yes', 'y', 'no', 'n'])
        if export_option in ['yes', 'y']:
            sequential_results_json("Nonlinear Tracking Filter", {"n_particles": n_particles, "n_steps": n_steps}, len(particle_history), {"final_estimate": final_estimate, "final_variance": final_variance})
            sequential_results_csv("Nonlinear Tracking Filter", {"n_particles": n_particles, "n_steps": n_steps}, len(particle_history), {"final_estimate": final_estimate, "final_variance": final_variance})
    else:
        print("Invalid selection. Please try again.")


def bootstrap_particle_filter(observations, n_particles, transition_fn, likelihood_fn, resampling='multinomial', seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    n_steps = len(observations)
    particles = np.random.randn(n_particles)
    weights = np.ones(n_particles) / n_particles
    
    particle_history = [particles.copy()]
    weight_history = [weights.copy()]
    
    for t in range(n_steps):
        particles = transition_fn(particles, t)
        obs = observations[t]
        likelihood = likelihood_fn(obs, particles)
        weights = weights * likelihood
        weights = weights / np.sum(weights)
        
        particle_history.append(particles.copy())
        weight_history.append(weights.copy())
        
        n_eff = 1.0 / np.sum(weights ** 2)
        if n_eff < n_particles / 2:
            particles, weights = resample_particles(particles, weights, resampling)
    
    return np.array(particle_history), np.array(weight_history)


def resample_particles(particles, weights, method='multinomial'):
    n_particles = len(particles)
    
    if method == 'multinomial':
        indices = np.random.choice(n_particles, size=n_particles, p=weights)
    elif method == 'systematic':
        indices = systematic_resample(weights)
    else:
        indices = np.arange(n_particles)
    
    return particles[indices], np.ones(n_particles) / n_particles


def systematic_resample(weights):
    n_particles = len(weights)
    cumsum = np.cumsum(weights)
    u = (np.arange(n_particles) + np.random.rand()) / n_particles
    indices = np.searchsorted(cumsum, u)
    return np.clip(indices, 0, n_particles - 1)


def state_estimate(particles, weights):
    return np.average(particles, weights=weights, axis=0)


def state_variance(particles, weights, estimate):
    return np.average((particles - estimate) ** 2, weights=weights, axis=0)


def linear_gaussian_filter(observations, n_particles, F=1.0, Q=1.0, H=1.0, R=1.0, seed=None):
    def transition(x, t):
        return F * x + np.sqrt(Q) * np.random.randn(len(x))
    
    def likelihood(obs, x):
        return np.exp(-0.5 * ((obs - H * x) ** 2) / R)
    
    return bootstrap_particle_filter(observations, n_particles, transition, likelihood, resampling='systematic', seed=seed)


def nonlinear_tracking_filter(observations, n_particles, seed=None):
    def transition(x, t):
        return 0.5 * x + 25.0 * x / (1.0 + x ** 2) + 8.0 * np.cos(1.2 * (t + 1)) + np.sqrt(10) * np.random.randn(len(x))
    
    def likelihood(obs, x):
        return np.exp(-0.5 * ((obs - x ** 2 / 20.0) ** 2))
    
    return bootstrap_particle_filter(observations, n_particles, transition, likelihood, resampling='systematic', seed=seed)
