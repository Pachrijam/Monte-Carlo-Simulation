import json
import csv
from datetime import datetime
from pathlib import Path

def _get_summary_value(summary, *keys, default=""):
    for key in keys:
        if key in summary:
            return summary[key]
    return default

def export_pi_results(num_samples, pi_estimate, error_percentage, confidence_data, filename=None):
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
    
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Method", "Monte Carlo Pi Estimation"])
        writer.writerow(["Number of Samples", num_samples])
        writer.writerow(["Pi Estimate", pi_estimate])
        writer.writerow(["Error Percentage", f"{error_percentage}%"])
        writer.writerow([])
        writer.writerow(["Confidence Level", "Mean", "Lower Bound", "Upper Bound", "Margin of Error"])
        for conf in confidence_data:
            writer.writerow([
                f"{int(conf['confidence_level']*100)}%",
                conf['mean'],
                conf['lower'],
                conf['upper'],
                conf['margin_of_error']
            ])
    print(f"Results exported to {csv_file}")

def export_mcmc_results(method_name, parameters, num_samples, posterior_summary_data, filename=None):
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
    
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Method", method_name])
        for param, value in parameters.items():
            writer.writerow([f"Parameter: {param}", value])
        writer.writerow(["Number of Samples", num_samples])
        writer.writerow([])
        writer.writerow(["Parameter", "Mean", "Median", "Standard Deviation", "95% CI Lower", "95% CI Upper"])
        for summary in posterior_summary_data:
            writer.writerow([
                _get_summary_value(summary, 'parameter', default=''),
                _get_summary_value(summary, 'mean', default=''),
                _get_summary_value(summary, 'median', default=''),
                _get_summary_value(summary, 'std_dev', default=''),
                _get_summary_value(summary, 'ci_lower', 'lower', '95% CI Lower', default=''),
                _get_summary_value(summary, 'ci_upper', 'upper', '95% CI Upper', default='')
            ])
    print(f"Results exported to {csv_file}")

def export_integration_results(function_name, lower_bound, upper_bound, num_samples, integral_estimate, filename=None):
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
    
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Method", "Monte Carlo Integration"])
        writer.writerow(["Function", function_name])
        writer.writerow(["Lower Bound", lower_bound])
        writer.writerow(["Upper Bound", upper_bound])
        writer.writerow(["Number of Samples", num_samples])
        writer.writerow(["Integral Estimate", integral_estimate])
    print(f"Results exported to {csv_file}")

def export_european_option_results(S, K, T, r, sigma, num_simulations, option_price_estimate, filename=None):
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
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Method", "Monte Carlo European Option Pricing"])
        writer.writerow(["Current Stock Price (S)", S])
        writer.writerow(["Strike Price (K)", K])
        writer.writerow(["Time to Maturity (T)", T])
        writer.writerow(["Risk-Free Rate (r)", r])
        writer.writerow(["Volatility (sigma)", sigma])
        writer.writerow(["Number of Simulations", num_simulations])
        writer.writerow(["Option Price Estimate", option_price_estimate])
    print(f"Results exported to {csv_file}")
    
def export_pde_sde_results(solver_type, parameters, num_samples, results_summary, filename=None):
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
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Solver Type", solver_type])
        for param, value in parameters.items():
            writer.writerow([f"Parameter: {param}", value])
        writer.writerow(["Number of Samples", num_samples])
        writer.writerow([])
        writer.writerow(["Result Metric", "Value"])
        for metric, value in results_summary.items():
            writer.writerow([metric, value])
    print(f"Results exported to {csv_file}")    
    
def export_rare_event_results(initial_condition, x0, time_horizon, n_paths, threshold, rare_event_probability_estimate, filename=None):
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
    
    csv_file = results_dir / f"{filename}.csv"
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Timestamp", datetime.now().isoformat()])
        writer.writerow(["Method", "Monte Carlo Rare Event Probability Estimation"])
        writer.writerow(["Initial Condition", initial_condition])
        writer.writerow(["x0", x0])
        writer.writerow(["Time Horizon", time_horizon])
        writer.writerow(["Number of Paths", n_paths])
        writer.writerow(["Threshold", threshold])
        writer.writerow(["Rare Event Probability Estimate", rare_event_probability_estimate])
    print(f"Results exported to {csv_file}")