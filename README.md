# Effects of Superspreaders in Spread of Epidemic

This repository contains simulation code and analysis scripts for studying the effects of superspreaders in epidemic transmission. The work replicates and extends the spatially-structured SIR model findings, demonstrating how different superspreader mechanisms influence epidemic dynamics, percolation thresholds, and propagation patterns.

## Overview

The project investigates a spatially-structured epidemic model where individuals are distributed in a 2D space with periodic boundary conditions. It explores two distinct superspreader models: the Strong Infectiousness model, where superspreaders have enhanced transmission probability, and the Hub model, where superspreaders have extended transmission range. The simulation reveals how superspreader fraction and model type affect epidemic curves, critical densities, propagation velocities, and secondary infection distributions, with validation against real SARS outbreak data from Singapore.

## Simulation

The `src/` directory contains the Python implementation of the epidemic simulation and visualization scripts. It includes:

- A `SIRSimulation` class in `models/SIR.py` that models spatial epidemic dynamics, calculates distance-dependent infection probabilities, and incorporates the two superspreader mechanisms.
- Visualization scripts in `visualization/` that generate various plots illustrating:
  - Epidemic curves comparing Strong, Hub, and no-superspreader models across different superspreader fractions.
  - Percolation probability diagrams showing the transition from contained to widespread epidemics as population density increases.
  - Propagation velocity analysis demonstrating how superspreaders accelerate spatial spread.
  - Secondary infection distributions revealing the heterogeneous nature of transmission.
  - Critical density plots mapping epidemic thresholds in parameter space.
  - Validation against SARS outbreak data showing model accuracy for real-world scenarios.

## How to Run the Simulation

To run the simulation and reproduce the figures:

1. Ensure you have Python 3.11 installed.
2. Install the necessary libraries from the requirements file:

   ```bash
   pip install -r requirements.txt
   ```

3. Run script to generate all plots:

   ```bash
   python src/visualization/run.py
   ```

4. Generated figures will be saved in the `figures/` directory.

## References

[1]  R. Fujie and T. Odagaki. Effects of superspreaders in spread of epidemic. Physica A: Statistical Mechanics and its Applications, 374(2):843–852, 2007. ISSN 0378-4371. doi: https://doi.org/10.1016/j.physa.2006.08.050. URL https://www.sciencedirect.com/science/article/pii/S0378437106008703.

[2] M. Lipsitch, T. Cohen, B. Cooper, J. M. Robins, S. Ma, L. James, G. Gopalakrishna, S. K. Chew, C. C. Tan, M. H. Samore, D. Fisman, and M. Murray. Transmission dynamics and
control of severe acute respiratory syndrome. Science, 300(5627):1966–1970, 2003. doi: 10.1126/science.1086616. URL https://www.science.org/doi/abs/10.1126/science.
1086616