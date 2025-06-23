import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict
from scipy.interpolate import interp1d
import random
from models.SIR import SIRSimulation
from visualization.plot_infection_probabilities import plot_infection_probabilities
from visualization.plot_percolation_probability import plot_percolation_probability
from visualization.plot_critical_density import plot_critical_density
from visualization.plot_distance_evolution import plot_distance_evolution
from visualization.plot_propagation_velocity import plot_propagation_velocity
from visualization.plot_epidemic_curves import plot_epidemic_curves
from visualization.plot_secondary_infections import plot_secondary_infections
from visualization.plot_sars_comparison import plot_sars_comparison


os.makedirs("figures", exist_ok=True)

def main():
    plot_infection_probabilities()
    plot_percolation_probability()
    plot_critical_density()
    plot_distance_evolution()
    plot_propagation_velocity()
    plot_epidemic_curves()
    plot_secondary_infections()
    plot_sars_comparison()
    
if __name__ == "__main__":
    main()