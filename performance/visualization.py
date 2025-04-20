# performance/simple_visualization.py
import os
import json
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def visualize_policy_comparison(results_file=None):
    """
    Visualize policy comparison results
    
    Args:
        results_file: Path to the results JSON file
    """
    # If no results file is specified, find the most recent one
    if not results_file:
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        if os.path.exists(results_dir):
            result_files = [f for f in os.listdir(results_dir) if f.startswith('performance_results_') and f.endswith('.json')]
            if result_files:
                result_files.sort(reverse=True)  # Most recent first
                results_file = os.path.join(results_dir, result_files[0])
                print(f"Using most recent results file: {results_file}")
    
    if not results_file or not os.path.exists(results_file):
        print("No results file specified or file not found")
        return
    
    # Load results
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    print(f"Loaded results from {results_file}")
    
    # Check if we have policy comparison results
    if "policy_comparison" not in results or not results["policy_comparison"]:
        print("No policy comparison results available")
        return
    
    policy_results = {}
    for result in results["policy_comparison"]:
        policy = result["policy"]
        policy_results[policy] = result
    
    policies = list(policy_results.keys())
    
    # Create directory for saving visualizations
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = os.path.join(os.path.dirname(__file__), "..", "results", f"policy_viz_{timestamp}")
    os.makedirs(save_dir, exist_ok=True)
    
    # Create figure with two subplots
    plt.figure(figsize=(14, 10))
    
    # Response Time plot
    plt.subplot(2, 1, 1)
    response_times = [policy_results[policy]['avg_response_time'] for policy in policies]
    
    bars = plt.bar(policies, response_times, color=['#3498db', '#2ecc71', '#e74c3c'])
    plt.title('Average Response Time by Scheduling Policy (lower is better)', fontsize=16)
    plt.ylabel('Average Response Time (seconds)', fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f}s', ha='center', va='bottom', fontsize=12)
    
    # Throughput plot
    plt.subplot(2, 1, 2)
    throughputs = [policy_results[policy]['throughput'] for policy in policies]
    
    bars = plt.bar(policies, throughputs, color=['#3498db', '#2ecc71', '#e74c3c'])
    plt.title('Throughput by Scheduling Policy (higher is better)', fontsize=16)
    plt.ylabel('Throughput (jobs/second)', fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height:.2f} jobs/s', ha='center', va='bottom', fontsize=12)
    
    # Add execution order information
    plt.figtext(0.1, 0.02, "Job Execution Order:", fontsize=12, weight='bold')
    
    y_pos = 0.0
    for policy in policies:
        if 'execution_order' in policy_results[policy]:
            order_text = f"{policy}: {' → '.join(policy_results[policy]['execution_order'])}"
            plt.figtext(0.1, y_pos - 0.03, order_text, fontsize=10)
            y_pos -= 0.03
    
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])
    
    # Save and display the visualization
    save_path = os.path.join(save_dir, "policy_comparison.png")
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Policy comparison visualization saved to {save_path}")
    
    # Also create a summary table
    create_summary_table(policy_results, save_dir)
    
    # Return path for display in notebook environments
    return save_path

def create_summary_table(policy_results, save_dir):
    """
    Create a summary table of policy comparison results
    
    Args:
        policy_results: Dictionary of policy results
        save_dir: Directory to save the table
    """
    # Create a new figure for the table
    plt.figure(figsize=(10, 6))
    plt.axis('off')
    plt.title('Policy Comparison Summary', fontsize=16)
    
    policies = list(policy_results.keys())
    
    # Create table data
    cell_text = []
    for policy in policies:
        result = policy_results[policy]
        cell_text.append([
            policy,
            f"{result['avg_response_time']:.2f}s",
            f"{result['throughput']:.2f} jobs/s",
            f"{result['test_duration']:.2f}s"
        ])
    
    # Create the table
    table = plt.table(
        cellText=cell_text,
        colLabels=['Policy', 'Avg Response Time', 'Throughput', 'Test Duration'],
        cellLoc='center',
        loc='center'
    )
    
    # Adjust table appearance
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    # Save the table
    save_path = os.path.join(save_dir, "policy_summary_table.png")
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Policy summary table saved to {save_path}")

def main():
    parser = argparse.ArgumentParser(description='Visualize CSUbatch policy comparison results')
    parser.add_argument('--results', type=str, help='Path to results JSON file')
    
    args = parser.parse_args()
    
    visualize_policy_comparison(args.results)

if __name__ == '__main__':
    main()