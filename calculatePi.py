import random
import time
import multiprocessing
import numpy as np

def monte_carlo_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate

def monte_carlo_pi_numpy(num_samples):
    x = np.random.uniform(0, 1, num_samples)
    y = np.random.uniform(0, 1, num_samples)

    inside_circle = np.sum(x**2 + y**2 <= 1)
    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate

def simulateChunk_numpy(num_samples):
    x = np.random.rand(num_samples)
    y = np.random.rand(num_samples)

    inside_circle = np.sum(x**2 + y**2 <= 1)
    return inside_circle

def parallel_monte_carlo_pi(num_samples, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    samples_per_process = num_samples // num_processes
    results = pool.map(simulateChunk_numpy, [samples_per_process] * num_processes)
    pool.close()
    pool.join()

    total_inside_circle = sum(results)
    return (total_inside_circle / num_samples) * 4

def percent_error(num_samples, mode = "normal", processes=None):
    if mode == "normal":
        pi_estimate = monte_carlo_pi(num_samples)
    elif mode == "parallel":
        pi_estimate = parallel_monte_carlo_pi(num_samples, processes)
    elif mode == "numpy":
        pi_estimate = monte_carlo_pi_numpy(num_samples)
    else:
        raise ValueError("Invalid mode. Choose 'normal', 'parallel', or 'numpy'.")
    
    error = abs(pi_estimate - np.pi) / np.pi * 100
    return error

def benchmark(num_samples, processes=None):
    print(f"\nRunning benchmark with {num_samples:,} samples...\n")

    start = time.time()
    pi_normal = monte_carlo_pi(num_samples)
    t1 = time.time() - start
    print(f"Normal π ≈ {pi_normal}")
    print(f"Time: {t1:.4f} sec\n")

    start = time.time()
    pi_numpy = monte_carlo_pi_numpy(num_samples)
    t2 = time.time() - start
    print(f"NumPy π ≈ {pi_numpy}")
    print(f"Time: {t2:.4f} sec\n")

    start = time.time()
    pi_parallel = parallel_monte_carlo_pi(num_samples, processes)
    t3 = time.time() - start
    print(f"Parallel NumPy π ≈ {pi_parallel}")
    print(f"Time: {t3:.4f} sec\n")

    print("Speedups:")
    print(f"NumPy vs Normal: {t1/t2:.2f}x")
    print(f"Parallel vs Normal: {t1/t3:.2f}x")
    print(f"Parallel vs NumPy: {t2/t3:.2f}x")


if __name__ == "__main__":
    samples = 1_000_000

    benchmark(samples)

    err = percent_error(samples, mode="parallel", processes=4)
    print(f"\nPercent Error: {err}%")