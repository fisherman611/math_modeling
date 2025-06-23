import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from models.SIR import SIRSimulation

def plot_infection_probabilities():
    """
    Plot the infection probabilities for Strong Infectiousness and Hub models.
    
    This function generates two plots showing how infection probability varies with distance
    for both normal individuals and superspreaders in each model.
    """
    sim = SIRSimulation()
    os.makedirs("figures", exist_ok=True)

    # Figure 1: Strong Infectiousness Model
    r_values = np.linspace(0, 1, 100)
    prob_normal = [sim.infection_probability(r, False, model_type="strong_infectiousness") for r in r_values]
    prob_super = [sim.infection_probability(r, True, model_type="strong_infectiousness") for r in r_values]
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_values, prob_super, 'orange', linewidth=3, label='Superspreader')
    plt.plot(r_values, prob_normal, 'blue', linestyle='--', linewidth=3, label='Normal')
    plt.xlabel(r'$r/r_0$', fontsize=14)
    plt.ylabel(r'$w(r)/w_0$', fontsize=14)
    plt.title('Strong Infectiousness Model - Infection Probability vs Distance', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1)
    plt.ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig('figures/strong_infection_prob.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 2: Hub Model
    r_values_hub = np.linspace(0, 2.5, 250)
    prob_normal_hub = [sim.infection_probability(r, False, model_type="hub") for r in r_values_hub]
    prob_super_hub = [sim.infection_probability(r, True, model_type="hub") for r in r_values_hub]
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_values_hub, prob_super_hub, 'orange', linewidth=3, label='Superspreader')
    plt.plot(r_values_hub, prob_normal_hub, 'blue', linestyle='--', linewidth=3, label='Normal')
    plt.xlabel(r'$r/r_0$', fontsize=14)
    plt.ylabel(r'$w(r)/w_0$', fontsize=14)
    plt.title('Hub Model - Infection Probability vs Distance', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 2.5)
    plt.ylim(0, 1.1)
    plt.tight_layout()
    plt.savefig('figures/hub_infection_prob.png', dpi=300, bbox_inches='tight')
    plt.close()
if __name__ == "__main__":
    plot_infection_probabilities() 