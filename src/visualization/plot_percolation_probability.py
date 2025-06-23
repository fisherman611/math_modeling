import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from models.SIR import SIRSimulation

def plot_percolation_probability():
    """
    Plot the percolation probabilities for Strong Infectiousness and Hub models.
    
    This function generates plots showing how percolation probability varies with density
    for different superspreader fractions in both models.
    """
    sim = SIRSimulation()
    L = sim.L
    lambda_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    N_values = range(150, 901, 10)
    n_runs = 1000
    
    os.makedirs("figures", exist_ok=True)
    
    colors = ['red', 'green', 'blue', 'magenta', 'cyan', 'orange']
    markers = ['o', 'o', 's', 's', '^', '^']
    
    # Store data for analysis
    percolation_data = {
        'strong_infectiousness': {'densities': [], 'probabilities': []},
        'hub': {'densities': [], 'probabilities': []}
    }
    
    for model_idx, model_type in enumerate(['strong_infectiousness', 'hub']):
        plt.figure(figsize=(10, 8))
        
        model_percolation_data = []
        
        for lambda_idx, lambda_val in enumerate(lambda_values):
            percolation_probs = []
            rho_pi_r0_squared = []
            
            for N in tqdm(N_values, desc=f'{model_type} model, λ={lambda_val}'):
                percolated_count = 0
                
                for _ in range(n_runs):
                    result = sim.run_simulation(N, lambda_val, model_type)
                    max_dist = max(result['max_distances']) if result['max_distances'] else 0
                    if max_dist >= 5:  # Percolation threshold
                        percolated_count += 1
                
                percolation_prob = percolated_count / n_runs
                percolation_probs.append(percolation_prob)
                rho_pi_r0_squared.append(N * np.pi / L ** 2)
            
            # Store data for analysis
            percolation_data[model_type]['densities'].append(rho_pi_r0_squared)
            percolation_data[model_type]['probabilities'].append(percolation_probs)
            
            plt.plot(rho_pi_r0_squared, percolation_probs, 
                    color=colors[lambda_idx], marker=markers[lambda_idx], 
                    markersize=6, label=f'λ = {lambda_val}')
        
        plt.xlabel(r'$\rho \pi r_0^2$', fontsize=14)
        plt.ylabel('Percolation Probability', fontsize=14)
        plt.title(f'{"Strong Infectiousness" if model_type == "strong_infectiousness" else "Hub"} Model - Percolation Analysis', fontsize=16)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 30)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(f'figures/{model_type}_percolation.png', dpi=300, bbox_inches='tight')
        plt.close()
        

if __name__ == "__main__":
    plot_percolation_probability() 