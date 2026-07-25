import json
from datetime import datetime
from pathlib import Path

def pi_results_json(num_samples, pi_estimate, error_percentage, confidence_data, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pi_results_{timestamp}"
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": "Monte Carlo Pi Estimation",
        "num_samples": num_samples,
        "pi_estimate": float(pi_estimate),
        "error_percentage": float(error_percentage),
        "confidence_intervals": confidence_data
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")

def mcmc_results_json(method_name, parameters, num_samples, posterior_summary_data, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mcmc_results_{timestamp}"
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": method_name,
        "parameters": parameters,
        "num_samples": num_samples,
        "posterior_summary": posterior_summary_data
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")

def integration_results_json(function_name, lower_bound, upper_bound, num_samples, integral_estimate, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"integration_results_{timestamp}"

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
        
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": "Monte Carlo Integration",
        "function": function_name,
        "lower_bound": lower_bound,
        "upper_bound": upper_bound,
        "num_samples": num_samples,
        "integral_estimate": float(integral_estimate)
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")

def european_option_results_json(S, K, T, r, sigma, num_simulations, option_price_estimate, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"european_option_results_{timestamp}"
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": "Monte Carlo European Option Pricing",
        "parameters": {
            "S": S,
            "K": K,
            "T": T,
            "r": r,
            "sigma": sigma,
            "num_simulations": num_simulations
        },
        "option_price_estimate": float(option_price_estimate)
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")
    
def pde_sde_results_json(solver_type, parameters, num_samples, results_summary, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{solver_type}_results_{timestamp}"
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "solver_type": solver_type,
        "parameters": parameters,
        "num_samples": num_samples,
        "results_summary": results_summary
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")
    
def rare_event_results_json(initial_condition, x0, time_horizon, n_paths, threshold, rare_event_probability_estimate, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rare_event_results_{timestamp}"
    
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": "Monte Carlo Rare Event Probability Estimation",
        "initial_condition": initial_condition,
        "x0": x0,
        "time_horizon": time_horizon,
        "n_paths": n_paths,
        "threshold": threshold,
        "rare_event_probability_estimate": float(rare_event_probability_estimate)
    }
    
    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")
    
def sequential_results_json(method_name, parameters, num_samples, results_summary, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sequential_results_{timestamp}"

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": method_name,
        "parameters": parameters,
        "num_samples": num_samples,
        "results_summary": results_summary
    }

    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")

def variance_results_json(method_name, parameters, num_samples, variance_estimate, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"variance_results_{timestamp}"

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    json_data = {
        "timestamp": datetime.now().isoformat(),
        "method": method_name,
        "parameters": parameters,
        "num_samples": num_samples,
        "variance_estimate": float(variance_estimate)
    }

    json_file = results_dir / f"{filename}.json"
    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Results exported to {json_file}")