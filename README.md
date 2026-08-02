# Monte Carlo Simulation

A Python practice project exploring Monte Carlo simulation techniques and their applications.

## Overview

This repository contains implementations of various Monte Carlo simulations—a statistical method for modeling and analyzing systems with random variables. The project demonstrates the power of using random sampling to solve complex problems and make predictions about real-world systems.

## Project Structure
```
Monte-Carlo-Simulation/
│
├── main.py
│
├── menu.py
│
├── calculate_simulations/                     # all simulation logic
│   ├── calculate_european_options.py
│   ├── calculate_int.py
│   ├── calculate_mcmc_bayes.py
│   ├── calculate_pde_sde.py
│   ├── calculate_pi.py
│   ├── calculate_rare_event.py
│   ├── calculate_confidence.py
│   ├── calculate_sequential.py
│   └── calculate_variance.py
│
├── visualizations/                   # all plotting / matplotlib logic
│   ├── visualizationInt.py
│   ├── visualizationMCMC.py
│   ├── visualizationPDE_SDE.py
│   ├── visualizationPi.py
│   ├── visualizationRareEvent.py
│   ├── visualizationSequential.py
│   └── visualizationVariance.py
│
├── animations/                       # cli animations
│   ├── progressbar.py
│   └── spinner.py
│
├── utils/
│   ├── exceptions.py                # handles invalid user input and export results
│   ├── export_csv.py
│   └── export_json.py 
│
├── README.md
└── LICENSE.md
```

## Features

This project includes implementations of the following Monte Carlo simulations:

- **Monte Carlo Integration** - Estimate the integral of a function using Monte Carlo integration
- **Pi Estimation** - Estimate the value of pi using the Monte Carlo method
- **Variance Reduction Techniques** - Advanced variance reduction techniques for improved simulation efficiency
- **Markov Chain Monte Carlo (MCMC) Methods** - Bayesian inference using MCMC methods for probabilistic modeling
- **PDE and SDE Solvers** - Solve partial differential equations and stochastic differential equations
- **Sequential Monte Carlo Analysis** - Sequential Monte Carlo analysis using particle filters
- **Rare Event and Tail Risk Simulation** - Estimate the probability of rare events in complex systems
- **European Option Pricing** - Evaluate financial derivatives using Black-Scholes Monte Carlo simulation

Each simulation includes interactive visualizations to help understand the concepts and results.

## Usage Examples

Run the main application:
```bash
python main.py
```

The program provides an interactive menu where you can select which simulation to run:

```
--------------------------------<<MENU>>--------------------------------
SELECT AN OPTION FROM BELOW:
------------------------------------------------------------------------
1. Estimate the integral of a function using Monte Carlo integration
2. Estimate the value of pi using the Monte Carlo method
3. Variance Reduction Techniques
4. Markov Chain Monte Carlo (MCMC) Methods
5. PDE and SDE Solvers
6. Sequential Monte Carlo Analysis (particle filters)
7. Rare event and Tail Risk Simulation
8. European Option Pricing (Black-Scholes Monte Carlo)
9. Exit
------------------------------------------------------------------------
```

Simply enter the number corresponding to the simulation you'd like to run (1-8), configure the simulation parameters when prompted, view the results and visualizations, and optionally export your results to CSV or JSON format. Select option 9 to exit the program.

## Video Resources
  ### Monte Carlo Pi Estimation
  - "DataMListic": https://youtu.be/lY4rSeX8IL4?si=5dUTObqbJ73dSNQc4
  ### Monte Carlo Integration
  - "lj37": https://youtu.be/0zbLv2k17vU?si=bVJ2NB_j9vA4dzgR
  ### Markov Chains
  - "Veritasium": https://youtu.be/KZeIEiBrT_w?si=WUUBXs1a3AdS_zEl
  - "SISL": https://youtu.be/3qodjHRUxAo?si=AwqZTTr_warI1HFc
  - "DataMListic": https://youtu.be/nndtTssgtZE?si=BSZdz250n0NFnsnx
  - "ritvikMath": https://youtu.be/yApmR-c_hKU?si=AhyUATM4EMC-zjJ8
  ### PDE & SDE
  - "Jafar Ghazanfarian": https://youtu.be/8w7v_pM6GWM?si=lYTgmc0Xu5afSyeg
  ### European Options
  - "QuantPy": https://youtu.be/fk38oX9GsxE?si=6T5Jlrj-Xe1kpNF5
  ### CSV & json
  - "Tech with Tim": https://youtu.be/-51jxlQaxyA?si=PPVqpGcIc1I4L6eR
  - "Corey Schafer": https://youtu.be/q5uM4VKywbA?si=Gr5vnjPuDrPmBJNm
  ### Miscellaneous
  - "The Synthetic Mind": https://youtu.be/WjmNedsX1T0?si=uSVoNJQRyHhcCifr
  - "Decision Lab": https://youtu.be/psOYFdx838E?si=dRDkmuvgSk-EPnJg
  - "MIT OpenCourseWare": https://youtu.be/OgO1gpXSUzU?si=iEBuJNuf8liokxNn

## License

This project is licensed under the terms specified in [LICENSE.md](LICENSE.md). See the LICENSE file for more details.
