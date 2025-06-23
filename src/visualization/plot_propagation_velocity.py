import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from models.SIR import SIRSimulation

def plot_propagation_velocity():
    """
    Plot propagation velocity as a function of superspreader fraction.
    
    This function compares how epidemic propagation velocity varies with superspreader
    fraction for both Strong Infectiousness and Hub models.
    """
    sim = SIRSimulation()
    lambda_values = np.linspace(0, 1, 20)
    N = 500
    n_runs = 1000
    max_steps = 100 
    
    os.makedirs("figures", exist_ok=True)
    
    strong_velocities = []
    hub_velocities = []
    
    for lambda_val in tqdm(lambda_values, desc='Computing velocities'):
        # Strong model
        strong_vels = []
        for _ in tqdm(range(n_runs)):
            result = sim.run_simulation(N, lambda_val, 'strong_infectiousness', max_steps)
            distances = result['max_distances']
            if len(distances) > 5:
                # Calculate velocity as slope of first 5 steps to avoid noise
                velocity = np.polyfit(range(min(5, len(distances))), 
                                    distances[:min(5, len(distances))], 1)[0]
                strong_vels.append(max(0, velocity))
        strong_velocities.append(np.mean(strong_vels) if strong_vels else 0)
        
        # Hub model
        hub_vels = []
        for _ in range(n_runs):
            result = sim.run_simulation(N, lambda_val, 'hub', max_steps)
            distances = result['max_distances']
            if len(distances) > 5:
                velocity = np.polyfit(range(min(5, len(distances))), 
                                    distances[:min(5, len(distances))], 1)[0]
                hub_vels.append(max(0, velocity))
        hub_velocities.append(np.mean(hub_vels) if hub_vels else 0)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    plt.plot(lambda_values, strong_velocities, 'ro-', markersize=8, linewidth=3, 
             label='Strong Infectiousness Model', markeredgewidth=2, markeredgecolor='darkred')
    plt.plot(lambda_values, hub_velocities, 'bs-', markersize=8, linewidth=3, 
             label='Hub Model', markeredgewidth=2, markeredgecolor='darkblue')
    
    
    plt.xlabel(r'Superspreader Fraction ($\lambda$)', fontsize=14)
    plt.ylabel(r'Propagation Velocity ($v/v_0$)', fontsize=14)
    plt.title('Epidemic Propagation Velocity vs Superspreader Fraction', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1)
    plt.ylim(0, max(max(strong_velocities), max(hub_velocities)) * 1.1)
    plt.tight_layout()
    plt.savefig('figures/propagation_velocity.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_propagation_velocity() 