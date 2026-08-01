from menu import get_menu_choice
from calculators.calculate_int import run_int
from calculators.calculate_pi import run_pi
from calculators.calculuate_variance import run_variance
from calculators.calculate_mcmc_bayes import run_mcmc
from calculators.calculate_pde_sde import run_pde_sde
from calculators.calculate_sequential import run_sequential
from calculators.calculate_rare_events import run_rare
from calculators.calculate_european_options import run_european


def main() -> None:
    while True:
        sim_choice: int = get_menu_choice()
        if sim_choice == 9:
            print("------------------------------------------------------------------------\nExiting the program. Thank you!")
            break
        elif sim_choice == 1:
            run_int()
        elif sim_choice == 2:
            run_pi()
        elif sim_choice == 3:
            run_variance()
        elif sim_choice == 4:
            run_mcmc()
        elif sim_choice == 5:
            run_pde_sde()
        elif sim_choice == 6:
            run_sequential()
        elif sim_choice == 7:
            run_rare()
        elif sim_choice == 8:
            run_european()
        else:
            print("Invalid choice. Please select a number between 1 and 9.")


if __name__ == "__main__":
    main()
