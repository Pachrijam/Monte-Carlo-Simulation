import random
import time
import multiprocessing

def monte_carlo_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate

def simulateChunk(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x**2 + y**2 <= 1:
            inside_circle += 1

    return inside_circle

def parallel_monte_carlo_pi(num_samples, num_processes):
    pool = multiprocessing.Pool(processes=num_processes)
    samples_per_process = num_samples // num_processes
    results = pool.map(simulateChunk, [samples_per_process] * num_processes)
    pool.close()
    pool.join()

    total_inside_circle = sum(results)
    pi_estimate = (total_inside_circle / num_samples) * 4
    return pi_estimate

def percent_error(num_samples, parallel=False, processes=None):
    if parallel:
        pi_estimate = parallel_monte_carlo_pi(num_samples, processes)
    else:
        pi_estimate = monte_carlo_pi(num_samples)

    error = abs(pi_estimate - 3.141592653589793)
    return round(error / 3.141592653589793 * 100, 4)

def benchmark(num_samples, parallel=False, processes=None):
    start_time = time.time()
    if parallel:
        pi_estimate = parallel_monte_carlo_pi(num_samples, processes)
    else:
        pi_estimate = monte_carlo_pi(num_samples)
    end_time = time.time()

    execution_time = end_time - start_time
    error_percentage = percent_error(num_samples, parallel, processes)

    return pi_estimate, execution_time, error_percentage

if __name__ == "__main__":
    samples = 1_000_000

    # Run benchmark
    benchmark(samples)

    # Example percent error
    err = percent_error(samples, parallel=True)
    print(f"\nPercent Error: {err}%")