import numpy as np

z_Scores = {
    0.90: 1.645,
    0.95: 1.96,
    0.99: 2.576
}

def confidence_interval(estimates, confidence=0.95):
    if confidence not in z_Scores:
        raise ValueError("Unsupported confidence level. Supported levels are: 0.90, 0.95, 0.99.")
    
    z = z_Scores[confidence]

    mean = np.mean(estimates)
    std_dev = np.std(estimates, ddof=1)
    n = len(estimates)
    margin_of_error = z * (std_dev / np.sqrt(n))

    lower = mean - margin_of_error
    upper = mean + margin_of_error

    return {
        "confidence_level": confidence,
        "mean": mean,
        "lower": lower,
        "upper": upper,
        "margin_of_error": margin_of_error
    }