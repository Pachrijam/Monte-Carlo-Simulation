# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this Monte Carlo Simulation repository.

## Project Overview

This is a Python practice project exploring Monte Carlo simulation techniques and their applications. It implements various Monte Carlo methods for:
- Estimating integrals
- Estimating π
- Markov Chain Monte Carlo (MCMC) methods
- PDE and SDE solvers
- Sequential Monte Carlo (particle filters)
- Rare event and tail risk simulation
- European option pricing

## Project Structure

```
MonteCarlo/
├── main.py                    # Main menu-driven interface
├── calculate_simulations/     # All simulation logic
│   ├── calculate_pi.py        # Pi estimation methods
│   ├── calculate_int.py       # Monte Carlo integration
│   ├── calculate_european_options.py  # Option pricing
│   ├── calculate_mcmc_bayes.py      # MCMC methods
│   ├── calculate_pde_sde.py         # PDE/SDE solvers
│   ├── calculate_rare_events.py     # Rare event simulation
│   ├── calculate_sequential.py      # Sequential Monte Carlo
│   └── calculate_variance.py        # Variance reduction (placeholder)
├── visualizations/            # All plotting / matplotlib logic
│   ├── visualizationPi.py         # Pi estimation plots
│   ├── visualizationInt.py        # Integration plots
│   ├── visualizationMCMC.py       # MCMC plots
│   ├── visualizationPDE_SDE.py    # PDE/SDE plots
│   ├── visualizationRareEvents.py # Rare event plots
│   ├── visualizationSequential.py # Sequential MC plots
│   └── visualizationVariance.py   # Variance reduction plots
├── utils/                     # Utility functions
│   ├── exceptions.py          # Safe input handling functions
│   ├── export_csv.py          # CSV export functions
│   └── export_json.py         # JSON export functions
├── results/                   # Auto-generated directory for results (JSON/CSV)
├── README.md                  # Project overview and video resources
└── LICENSE.md                 # MIT license
```

## Setup and Dependencies

This project requires:
- Python 3.x
- numpy
- matplotlib

To install dependencies:
```bash
pip install numpy matplotlib
```

## Running the Application

To start the interactive menu:
```bash
python main.py
```

The program presents a menu of nine simulation options:
1. Estimate integrals using Monte Carlo integration
2. Estimate π using Monte Carlo method
3. Variance Reduction Techniques (currently under development)
4. Markov Chain Monte Carlo (MCMC) Methods
5. PDE and SDE Solvers
6. Sequential Monte Carlo Analysis (particle filters)
7. Rare event and Tail Risk Simulation
8. European Option Pricing (Black-Scholes Monte Carlo)
9. Exit

## Running Specific Simulations

Each simulation module can be imported and used directly. For example, to use the pi estimation:
```python
from calculate_simulations.calculate_pi import monte_carlo_pi, percent_error
pi_estimate = monte_carlo_pi(1000000)
error = percent_error(1000000)
```

## Exporting Results

All simulations can export results to JSON and CSV formats in the `results/` directory. Export functions are named consistently:
- `{simulation_type}_results_json(...)`
- `{simulation_type}_results_csv(...)`

Common parameters include:
- Simulation-specific parameters (e.g., `num_samples`, `lower_bound`, `upper_bound`)
- Results data (estimates, errors, confidence intervals, etc.)
- Optional filename parameter

## Visualization

Each simulation module has corresponding visualization functions in the `visualizations/` directory:
- `visualize{Name}Estimates(samples)` - Shows estimates over sample count
- `visualize{Name}PercentError(samples)` - Shows percent error over sample count
- `visualize{Name}Subplot(samples)` - Shows both estimates and error in subplot

All visualizations use matplotlib with a dark background theme.

## Code Conventions

### Input Handling
All user input uses safe validation functions from `utils.exceptions.py`:
- `safe_int(prompt, min_val=None, max_val=None)`
- `safe_float(prompt, min_val=None, max_val=None)`
- `safe_choice(prompt, valid_options)`
- `safe_optional_int(prompt, default=None)`
- `safe_optional_float(prompt, default=None)`
- `safe_seed_input(prompt)`

### Export Functions
Export functions follow a consistent pattern:
1. Create results directory if it doesn't exist
2. Generate timestamp-based filename if none provided
3. Create dictionary with metadata and results
4. Write JSON/CSV with proper formatting
5. Print confirmation message

### Visualization Functions
Visualization functions:
- Use matplotlib with `dark_background` style
- Create appropriately sized figures (typically 10x6 inches)
- Include grids, labels, titles, and legends
- Set appropriate axis limits with margins
- Display plots using `plt.show()`

## Extending the Project

To add a new simulation:
1. Create a new file in `calculate_simulations/` (e.g., `calculate_newsim.py`)
2. Implement the core simulation logic as a function
3. Create corresponding visualization functions in `visualizations/`
4. Add export functions to both `export_json.py` and `export_csv.py`
5. Import and integrate the new simulation in `main.py`:
   - Add import statement at top
   - Add menu option in `get_menu_choice()`
   - Add handler function similar to existing ones
   - Add case in `main()` function

## Testing

Currently, there are no automated tests in this project. To improve maintainability, consider adding:
- Unit tests for simulation functions using pytest
- Tests for utility functions
- Tests for export functions
- Integration tests for the main menu

Example test structure:
```
tests/
├── test_calculate_pi.py
├── test_calculate_int.py
├── test_export_json.py
└── test_utils.py
```

## Common Development Tasks

### Running a Specific Simulation Directly
Instead of using the menu, you can import and run simulations directly:
```python
# For pi estimation
from calculate_simulations.calculate_pi import monte_carlo_pi
result = monte_carlo_pi(1000000)

# For integration
from calculate_simulations.calculate_int import calculate_monte_carlo_integration
import math
result = calculate_monte_carlo_integration(math.sin, 0, math.pi, 100000)
```

### Adding Visualization to Existing Simulation
1. Create/update visualization function in `visualizations/visualization{Name}.py`
2. Import the visualization function in main.py or simulation handler
3. Call it after computation when user requests visualization

### Improving Performance
Consider:
- Using numpy vectorization (already implemented in many functions)
- Adding multiprocessing options (already in pi estimation)
- Implementing variance reduction techniques
- Using quasi-random sequences (e.g., Sobol, Halton) instead of pseudorandom

## Troubleshooting

### Common Issues
1. **Missing dependencies**: Install numpy and matplotlib with pip
2. **Plots not displaying**: Ensure you're running in an environment that supports GUI displays
3. **Input errors**: The safe input functions handle most validation issues
4. **Directory permissions**: Ensure you have write access to create the results directory

### Debugging Tips
- All simulation functions return values that can be inspected
- Visualization functions can be called independently to debug output
- Export functions create human-readable JSON/CSV files for inspection
- Input validation functions provide clear error messages for invalid input

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.