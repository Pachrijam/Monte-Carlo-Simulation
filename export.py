import json
import csv
from datetime import datetime
from pathlib import Path

def export_pi_results(num_samples, pi_estimate, error_percentage, confidence_data, filename=None):
    """
    Export Pi estimation results to CSV and JSON files.
    
    Args:
        num_samples: Number of samples used
        pi_estimate: Estimated value of pi
        error_percentage: Percent error
        confidence_data: List of dicts with confidence interval info
        filename: Base name for output files (without extension)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pi_results_{timestamp}"
    
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Export to JSON
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
    
    # Export to CSV
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


def export_integration_results(function_name, lower_bound, upper_bound, num_samples, integral_estimate, filename=None):
    """
    Export integration results to CSV and JSON files.
    
    Args:
        function_name: Name/description of the function integrated
        lower_bound: Lower bound of integration
        upper_bound: Upper bound of integration
        num_samples: Number of samples used
        integral_estimate: Estimated integral value
        filename: Base name for output files (without extension)
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"integration_results_{timestamp}"
    
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Export to JSON
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
    
    # Export to CSV
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
