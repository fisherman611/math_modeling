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

def plot_critical_density():
    """Plot the Critical density"""
    sim = SIRSimulation()
    lambda_values = np.linspace(0, 1, 10)
    N_values = np.arange(150, 901, 50)
    n_runs = 1000
    
    
    # Analytical curves
    r0 = sim.r0
    rs = sim.rs
    w0 = sim.w0
    
    # Strong model integrals
    I_n_strong = np.pi * w0 * (r0**2) / 6
    I_ss_strong = np.pi * w0 * (r0**2)
    R_c_strong = 4.5
    strong_critical = R_c_strong * w0 * np.pi * (r0**2) / (lambda_values * I_ss_strong + (1 - lambda_values) * I_n_strong)

    # Hub model integrals
    I_n_hub = I_n_strong
    I_ss_hub = np.pi * w0 * (rs**2) / 6
    R_c_hub = 3.2
    hub_critical = R_c_hub * w0 * np.pi * (r0**2) / (lambda_values * I_ss_hub + (1 - lambda_values) * I_n_hub)
    
    # Simulation points
    lambda_sim = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    strong_sim = []
    hub_sim = []

    for model_type, sim_points in [('strong_infectiousness', strong_sim), ('hub', hub_sim)]:
        for lambda_val in tqdm(lambda_sim, desc=f'Critical density {model_type}'):
            percolation_probs = []
            rho_values = []
            for N in tqdm(N_values):
                percolated_count = 0
                for _ in range(n_runs):
                    result = sim.run_simulation(N, lambda_val, model_type)
                    max_dist = max(result['max_distances']) if result['max_distances'] else 0
                    if max_dist >= 5:  # Percolation threshold as per paper
                        percolated_count += 1
                percolation_prob = percolated_count / n_runs
                percolation_probs.append(percolation_prob)
                rho_values.append(N / (10 * r0) ** 2)

            # Interpolate to find critical density where percolation_prob ~ 0.5
            interp = interp1d(rho_values, percolation_probs, bounds_error=False, fill_value=(0, 1))
            rho_range = np.linspace(min(rho_values), max(rho_values), 1000)
            probs = interp(rho_range)
            critical_rho = rho_range[np.argmin(np.abs(probs - 0.5))]
            sim_points.append(critical_rho * np.pi * r0 ** 2)

    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(lambda_values, strong_critical, 'g-', linewidth=2, label='Strong Model')
    plt.plot(lambda_values, hub_critical, 'm--', linewidth=2, label='Hub Model')
    plt.plot(lambda_sim, strong_sim, 'go', markersize=8, label='Strong Simulation')
    plt.plot(lambda_sim, hub_sim, 'ms', markersize=8, label='Hub Simulation')
    plt.xlabel(r'$\lambda$')
    plt.ylabel(r'$\rho_c \pi r_0^2$')
    plt.title('Dependence of Critical Density on Superspreader Fraction')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1)
    plt.ylim(0, 30)
    plt.tight_layout()
    plt.savefig('figures/critical_density.png', dpi=300)
    plt.close()
    
if __name__ == "__main__":
    plot_critical_density()