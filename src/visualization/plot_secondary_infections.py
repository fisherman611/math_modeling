import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy import stats
from models.SIR import SIRSimulation

def plot_secondary_infections():
    """
    Plot secondary infection distributions for different superspreader scenarios.
    
    This function generates histograms showing the distribution of secondary infections
    for scenarios with and without superspreaders.
    """
    sim = SIRSimulation()
    N = 500
    n_runs = 1000
    max_steps = 100
    
    os.makedirs("figures", exist_ok=True)
    
    # Collect data
    print("Collecting secondary infection data...")
    
    # Figure 12: λ=0.0 (No superspreaders)
    all_secondary_no_super = []
    for _ in tqdm(range(n_runs), desc='Secondary infections λ=0.0'):
        result = sim.run_simulation(N, 0.0, 'strong_infectiousness', max_steps)
        secondary = list(result['secondary_infections'].values())
        all_secondary_no_super.extend(secondary)
    
    # Figure 13: λ=0.2 (With superspreaders)
    all_secondary_strong = []
    all_secondary_hub = []
    
    for _ in tqdm(range(n_runs), desc='Secondary infections λ=0.2'):
        # Strong model
        result = sim.run_simulation(N, 0.2, 'strong_infectiousness', max_steps)
        secondary = list(result['secondary_infections'].values())
        all_secondary_strong.extend(secondary)
        
        # Hub model
        result = sim.run_simulation(N, 0.2, 'hub', max_steps)
        secondary = list(result['secondary_infections'].values())
        all_secondary_hub.extend(secondary)
    
    # Set up matplotlib for better plots
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.linewidth'] = 1.2
    
    # Plot Figure 12: No superspreaders (λ=0.0)
    plt.figure(figsize=(8, 6))
    
    # Calculate histogram data
    max_val = min(20, max(all_secondary_no_super)) if all_secondary_no_super else 20
    bins = np.arange(0, max_val + 2) - 0.5  # Center bins on integers
    hist_data, bin_edges = np.histogram(all_secondary_no_super, bins=bins, density=True)
    
    # Create bar plot to match the reference style
    bin_centers = np.arange(0, max_val + 1)
    plt.bar(bin_centers, hist_data, width=0.8, color='cyan', alpha=0.8, 
            edgecolor='black', linewidth=1.0)

    
    plt.xlabel('the number of links', fontsize=12)
    plt.ylabel('', fontsize=12)  # Empty y-label to match reference
    plt.xlim(-0.5, max_val + 0.5)
    plt.ylim(0, 0.8)  # Match the reference y-axis range    
    # Clean up the plot appearance
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().set_axisbelow(True)
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('figures/no_superspreaders_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot Figure 13: With superspreaders (λ=0.2)
    plt.figure(figsize=(8, 6))
    
    # Calculate histogram data for both models
    max_val = min(20, max(max(all_secondary_strong) if all_secondary_strong else [0], 
                         max(all_secondary_hub) if all_secondary_hub else [0]))
    bins = np.arange(0, max_val + 2) - 0.5
    
    hist_strong, _ = np.histogram(all_secondary_strong, bins=bins, density=True)
    hist_hub, _ = np.histogram(all_secondary_hub, bins=bins, density=True)
    
    bin_centers = np.arange(0, max_val + 1)
    width = 0.35  # Width of bars for side-by-side plotting
    
    # Create side-by-side bars
    plt.bar(bin_centers - width/2, hist_strong, width, 
            color='red', alpha=0.8, label='Strong infectiousness model', 
            edgecolor='black', linewidth=0.8)
    plt.bar(bin_centers + width/2, hist_hub, width, 
            color='blue', alpha=0.8, label='Hub model', 
            edgecolor='black', linewidth=0.8)
    
    plt.xlabel('the number of links', fontsize=12)
    plt.ylabel('', fontsize=12)  # Empty y-label to match reference
    plt.xlim(-0.5, max_val + 0.5)
    plt.ylim(0, 0.8)  # Match the reference y-axis range
    
    # Add legend in top right corner
    plt.legend(loc='upper right', frameon=True, fancybox=False, shadow=False)
    
    # Clean up the plot appearance
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().set_axisbelow(True)
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig('figures/superspreaders_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    plot_secondary_infections()