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

def plot_distance_evolution():
    """Plot the distance evolution"""
    sim = SIRSimulation()
    lambda_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    N = 500
    n_runs = 1000
    max_steps = 100
    
    colors = ['red', 'green', 'purple', 'blue', 'yellow', 'pink']
    markers = ['o', 's', 's', 's', '^', '^']
    
    plt.figure(figsize=(10, 8))
    
    for lambda_idx, lambda_val in enumerate(lambda_values):
        all_distances = []
        
        for _ in tqdm(range(n_runs), desc=f'λ={lambda_val}'):
            result = sim.run_simulation(N, lambda_val, 'strong_infectiousness', max_steps)
            distances = result['max_distances']
            # Pad with last value if simulation ended early
            while len(distances) < max_steps:
                distances.append(distances[-1] if distances else 0)
            all_distances.append(distances)
        
        # Calculate average
        avg_distances = np.mean(all_distances, axis=0)
        time_steps = range(max_steps)
        
        plt.plot(time_steps, avg_distances, 
                color=colors[lambda_idx], marker=markers[lambda_idx], 
                markersize=4, label=f'λ = {lambda_val}')
    
    plt.xlabel('Time')
    plt.ylabel(r'$r_{t}/r_{0}$')
    plt.title('Time Evolution of Distance (Strong Model)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 40)
    plt.ylim(0, 7)
    plt.tight_layout()
    plt.savefig('figures/strong_distance_evolution.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    plot_distance_evolution()