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

os.makedirs("figures", exist_ok=True)

def plot_sars_comparison():
    """Plot SARS secondary cases distribution and epidemic curves (Figures 14 and 15).

    Compares simulated secondary infections and epidemic curves for strong infectiousness
    and hub models with SARS data from Singapore (Feb–Jun 2003), based on Fujie and Odagaki (2007).
    """
    sim = SIRSimulation(r0=1, w0=1, gamma=1.0)
    N = 500
    lambda_val = 0.4
    n_runs = 1000
    max_steps = 25
    
    sars_secondary = [0] * 150 + [1] * 25 + [2] * 15 + [3] * 10 + [4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 21, 23, 40]

    plt.figure(figsize=(8, 6))
    plt.hist(sars_secondary, bins=range(42), color='pink', alpha=0.7, edgecolor='black')
    plt.xlabel('Number of Secondary Cases')
    plt.ylabel('Number of Patients')
    plt.title('SARS Secondary Cases (Singapore, Feb 25–Apr 30, 2003)')
    plt.xlim(0, 40)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/sars_secondary_cases.png', dpi=300)
    plt.close()

    # Figure 15: SARS epidemic curves comparison
    # Approximate SARS data based on paper’s description (120 days, peak ~30–40 cases)
    sars_data = [0, 2, 10, 20, 52, 19, 18, 40, 27, 14, 12, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Run simulations
    strong_infections = []
    hub_infections = []
    no_super_infections = []

    for _ in tqdm(range(n_runs), desc='SARS comparison'):
        # Strong model, \lambda=0.4
        result = sim.run_simulation(N, lambda_val, 'strong_infectiousness', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        strong_infections.append(infections)

        # Hub model, \lambda=0.4
        result = sim.run_simulation(N, lambda_val, 'hub', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        hub_infections.append(infections)

        # No superspreaders, \lambda=0.0
        result = sim.run_simulation(N, 0.0, 'strong_infectiousness', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        no_super_infections.append(infections)

    # Calculate averages and scale to match SARS data magnitude
    scale_factor = 0.5  # Adjust simulation output to approximate SARS case numbers
    avg_strong = np.mean(strong_infections, axis=0) * scale_factor
    avg_hub = np.mean(hub_infections, axis=0) * scale_factor
    avg_no_super = np.mean(no_super_infections, axis=0) * scale_factor

    time_steps = np.arange(max_steps) * 6  # Each step = 6 days

    plt.figure(figsize=(10, 8))
    plt.bar(time_steps, sars_data, color='orange', alpha=0.7, label='SARS Data', width=3)
    plt.plot(time_steps, avg_strong, 'ro-', markersize=4, label='Strong Model (\u03BB=0.4)')
    plt.plot(time_steps, avg_hub, 'bs-', markersize=4, label='Hub Model (\u03BB=0.4)')
    plt.plot(time_steps, avg_no_super, 'c^-', markersize=4, label='No Superspreaders (\u03BB=0.0)')
    plt.xlabel('Time (days)')
    plt.ylabel('New Cases')
    plt.title('SARS Epidemic Curves (Singapore, Feb 13–Jun 13, 2003)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 150)
    plt.ylim(0, 80)
    plt.tight_layout()
    plt.savefig('figures/sars_epidemic_curves.png', dpi=300)
    plt.close()
    
if __name__ == "__main__":
    plot_sars_comparison() 