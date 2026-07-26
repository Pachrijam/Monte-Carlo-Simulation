from utils.exceptions import safe_int

def get_menu_choice() -> int:
    print("--------------------------------<<MENU>>--------------------------------\nSELECT AN OPTION FROM BELOW:\n------------------------------------------------------------------------")
    print("""1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of pi using the Monte Carlo method
3. Variance Reduction Techniques
4. Markov Chain Monte Carlo (MCMC) Methods
5. PDE and SDE Solvers
6. Sequential Monte Carlo Analysis (particle filters)
7. Rare event and Tail Risk Simulation
8. European Option Pricing (Black-Scholes Monte Carlo)
9. Exit
------------------------------------------------------------------------""")
    
    sim_choice = safe_int("Enter the number of the simulation you would like to run (1-9): ", min_val=1, max_val=9)
    return sim_choice