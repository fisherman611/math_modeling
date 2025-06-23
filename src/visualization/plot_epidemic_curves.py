import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from models.SIR import SIRSimulation

def analyze_epidemic_curves(strong_data, hub_data, no_super_data):
    """
    Analyze epidemic curve characteristics.
    
    Args:
        strong_data: New infections per time step for strong model
        hub_data: New infections per time step for hub model  
        no_super_data: New infections per time step for no superspreaders
        
    Returns:
        dict: Analysis results including peak timing, magnitude, and curve shapes
    """
    analysis = {
        'peak_analysis': {},
        'total_infections': {},
        'curve_characteristics': {},
        'superspreader_impact': {}
    }
    
    curves = {
        'strong': strong_data,
        'hub': hub_data,
        'no_super': no_super_data
    }
    
    for model_name, curve in curves.items():
        # Find peak
        peak_day = np.argmax(curve)
        peak_magnitude = max(curve)
        
        # Total infections (area under curve)
        total_infections = np.sum(curve)
        
        # Curve width (days with >10% of peak)
        threshold = 0.1 * peak_magnitude
        above_threshold = np.where(curve > threshold)[0]
        curve_width = len(above_threshold) if len(above_threshold) > 0 else 0
        
        # Asymmetry (ratio of rise time to fall time)
        rise_time = peak_day
        fall_time = len(curve) - peak_day - 1
        asymmetry = fall_time / rise_time if rise_time > 0 else float('inf')
        
        analysis['peak_analysis'][model_name] = {
            'peak_day': peak_day,
            'peak_magnitude': peak_magnitude,
            'peak_ratio_vs_no_super': peak_magnitude / max(no_super_data) if max(no_super_data) > 0 else float('inf')
        }
        
        analysis['total_infections'][model_name] = total_infections
        
        analysis['curve_characteristics'][model_name] = {
            'curve_width': curve_width,
            'asymmetry': asymmetry,
            'rise_rate': peak_magnitude / peak_day if peak_day > 0 else float('inf'),
            'fall_rate': peak_magnitude / fall_time if fall_time > 0 else float('inf')
        }
    
    # Superspreader impact analysis
    analysis['superspreader_impact'] = {
        'peak_enhancement_strong': analysis['peak_analysis']['strong']['peak_ratio_vs_no_super'],
        'peak_enhancement_hub': analysis['peak_analysis']['hub']['peak_ratio_vs_no_super'],
        'total_enhancement_strong': analysis['total_infections']['strong'] / analysis['total_infections']['no_super'],
        'total_enhancement_hub': analysis['total_infections']['hub'] / analysis['total_infections']['no_super'],
        'model_comparison': analysis['peak_analysis']['hub']['peak_magnitude'] / analysis['peak_analysis']['strong']['peak_magnitude']
    }
    
    return analysis

def plot_epidemic_curves():
    """
    Plot epidemic curves comparing different superspreader models.
    
    This function generates epidemic curves showing new infections over time
    for Strong model, Hub model, and no superspreaders scenario.
    """
    sim = SIRSimulation()
    N = 500
    n_runs = 1000
    max_steps = 100
    
    os.makedirs("figures", exist_ok=True)
    
    # Run simulations
    strong_02_infections = []
    hub_02_infections = []
    no_super_infections = []
    
    for _ in tqdm(range(n_runs), desc='Generating epidemic curves'):
        # Strong model, λ=0.2
        result = sim.run_simulation(N, 0.2, 'strong_infectiousness', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        strong_02_infections.append(infections)
        
        # Hub model, λ=0.2
        result = sim.run_simulation(N, 0.2, 'hub', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        hub_02_infections.append(infections)
        
        # No superspreaders, λ=0.0
        result = sim.run_simulation(N, 0.0, 'strong_infectiousness', max_steps)
        infections = result['new_infections_per_step']
        while len(infections) < max_steps:
            infections.append(0)
        no_super_infections.append(infections)
    
    # Calculate averages and confidence intervals
    avg_strong_02 = np.mean(strong_02_infections, axis=0)
    std_strong_02 = np.std(strong_02_infections, axis=0)
    avg_hub_02 = np.mean(hub_02_infections, axis=0)
    std_hub_02 = np.std(hub_02_infections, axis=0)
    avg_no_super = np.mean(no_super_infections, axis=0)
    std_no_super = np.std(no_super_infections, axis=0)
    
    time_steps = range(max_steps)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot with confidence intervals
    plt.plot(time_steps, avg_strong_02, 'ro-', markersize=5, linewidth=2, 
             label='Strong Model (λ=0.2)')
    plt.plot(time_steps, avg_hub_02, 'bs-', markersize=5, linewidth=2, 
             label='Hub Model (λ=0.2)')
    plt.plot(time_steps, avg_no_super, '^-', color='cyan', markersize=5, linewidth=2, 
             label='No Superspreaders (λ=0.0)')
    plt.xlabel('Time Steps', fontsize=14)
    plt.ylabel('New Infections per Time Step', fontsize=14)
    plt.title('Epidemic Curves - Impact of Superspreaders', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 50)
    plt.ylim(0, max(max(avg_strong_02), max(avg_hub_02), max(avg_no_super)) * 1.2)
    
    # Perform analysis
    analysis = analyze_epidemic_curves(avg_strong_02, avg_hub_02, avg_no_super)
    
    # Add peak markers
    for model_name, color in [('strong', 'red'), ('hub', 'blue'), ('no_super', 'cyan')]:
        peak_day = analysis['peak_analysis'][model_name]['peak_day']
        peak_mag = analysis['peak_analysis'][model_name]['peak_magnitude']
        plt.annotate(f'Peak: {peak_mag:.1f}', 
                    xy=(peak_day, peak_mag), 
                    xytext=(peak_day + 5, peak_mag + 5),
                    arrowprops=dict(arrowstyle='->', color=color),
                    fontsize=10, color=color)
    
    plt.tight_layout()
    plt.savefig('figures/epidemic_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return analysis

if __name__ == "__main__":
    plot_epidemic_curves() 