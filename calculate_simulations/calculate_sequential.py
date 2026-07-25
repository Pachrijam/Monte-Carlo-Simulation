import numpy as np


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
