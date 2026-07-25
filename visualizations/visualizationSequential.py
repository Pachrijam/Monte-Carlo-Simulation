import numpy as np
import matplotlib.pyplot as plt


def visualize_particle_trajectories(particle_history, weight_history, observations=None, show=True):
    plt.style.use('dark_background')
    n_steps = len(particle_history)
    n_particles = len(particle_history[0])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i in range(n_particles):
        trajectory = [particle_history[t][i] for t in range(n_steps)]
        alpha = np.mean(weight_history[-1]) if i == 0 else 0.1
        ax.plot(range(n_steps), trajectory, alpha=0.3, linewidth=0.5, color='blue')
    
    estimates = [np.average(particle_history[t], weights=weight_history[t]) for t in range(n_steps)]
    ax.plot(range(n_steps), estimates, 'r-', linewidth=2, label='Particle Filter Estimate')
    
    if observations is not None:
        ax.plot(range(len(observations)), observations, 'g*', markersize=8, label='Observations')
    
    ax.set_xlabel('Time', fontsize=14)
    ax.set_ylabel('State Value', fontsize=14)
    ax.set_title('Particle Filter: State Trajectories', fontsize=16, fontweight='bold')
    ax.legend()
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    if show:
        plt.tight_layout()
        plt.show()
    else:
        return fig


def visualize_particle_weights(weight_history, show=True):
    plt.style.use('dark_background')
    n_steps = len(weight_history)
    weight_means = [np.mean(weight_history[t]) for t in range(n_steps)]
    weight_stds = [np.std(weight_history[t]) for t in range(n_steps)]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.fill_between(range(n_steps), 
                     np.array(weight_means) - np.array(weight_stds),
                     np.array(weight_means) + np.array(weight_stds),
                     alpha=0.3, label='±1 Std Dev')
    ax.plot(range(n_steps), weight_means, 'b-', linewidth=2, label='Mean Weight')
    ax.plot(range(n_steps), np.max(weight_history, axis=1), 'r--', linewidth=1, label='Max Weight')
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Particle Weight')
    ax.set_title('Particle Weights Over Time')
    ax.legend()
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    if show:
        plt.tight_layout()
        plt.show()
    else:
        return fig


def visualize_effective_sample_size(weight_history, show=True):
    plt.style.use('dark_background')
    n_steps = len(weight_history)
    n_particles = len(weight_history[0])
    ess = [1.0 / np.sum(weight_history[t] ** 2) for t in range(n_steps)]
    ess_ratio = [e / n_particles for e in ess]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(range(n_steps), ess_ratio, 'b-', linewidth=2)
    ax.axhline(y=0.5, color='r', linestyle='--', linewidth=1, label='Resample Threshold')
    ax.fill_between(range(n_steps), 0, ess_ratio, alpha=0.3)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('ESS / N')
    ax.set_title('Effective Sample Size Ratio')
    ax.set_ylim([0, 1.1])
    ax.legend()
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    if show:
        plt.tight_layout()
        plt.show()
    else:
        return fig


def visualize_sequential_subplot(particle_history, weight_history, observations=None, show=True):
    plt.style.use('dark_background')
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    n_steps = len(particle_history)
    n_particles = len(particle_history[0])
    
    for i in range(n_particles):
        trajectory = [particle_history[t][i] for t in range(n_steps)]
        axes[0].plot(range(n_steps), trajectory, alpha=0.3, linewidth=0.5, color='blue')
    
    estimates = [np.average(particle_history[t], weights=weight_history[t]) for t in range(n_steps)]
    axes[0].plot(range(n_steps), estimates, 'r-', linewidth=2, label='Estimate')
    
    if observations is not None:
        axes[0].plot(range(len(observations)), observations, 'g*', markersize=8, label='Observations')
    
    axes[0].set_ylabel('State')
    axes[0].set_title('Particle Trajectories & Estimates')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    weight_means = [np.mean(weight_history[t]) for t in range(n_steps)]
    weight_stds = [np.std(weight_history[t]) for t in range(n_steps)]
    axes[1].fill_between(range(n_steps),
                         np.array(weight_means) - np.array(weight_stds),
                         np.array(weight_means) + np.array(weight_stds),
                         alpha=0.3)
    axes[1].plot(range(n_steps), weight_means, 'b-', linewidth=2)
    axes[1].set_ylabel('Weight')
    axes[1].set_title('Particle Weights')
    axes[1].grid(True, alpha=0.3)
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    ess = [1.0 / np.sum(weight_history[t] ** 2) for t in range(n_steps)]
    ess_ratio = [e / n_particles for e in ess]
    axes[2].plot(range(n_steps), ess_ratio, 'b-', linewidth=2)
    axes[2].axhline(y=0.5, color='r', linestyle='--', linewidth=1)
    axes[2].fill_between(range(n_steps), 0, ess_ratio, alpha=0.3)
    axes[2].set_xlabel('Time')
    axes[2].set_ylabel('ESS / N')
    axes[2].set_title('Effective Sample Size Ratio')
    axes[2].set_ylim([0, 1.1])
    axes[2].grid(True, alpha=0.3)
    plt.grid(color='gray', linestyle='-', linewidth=0.5, alpha=0.2)
    
    if show:
        plt.tight_layout()
        plt.show()
    else:
        return fig
