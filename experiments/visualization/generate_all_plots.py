#!/usr/bin/env python3
"""
Generate all visualizations (accuracy and timing) for OCR systems
"""

import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from evaluation.time import generate_timing_visualizations
from evaluation.accuracy import generate_accuracy_visualizations

def load_config(config_path="config/experiments.yaml"):
    """Load configuration from experiments.yaml"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        return {}

def main():
    print("="*80)
    print("GENERATING ALL VISUALIZATIONS")
    print("="*80)
    
    # Load configuration
    config = load_config()
    
    # Get datasets and systems from config
    datasets = []
    if 'datasets' in config:
        datasets = [d['name'] for d in config['datasets'] if d.get('name')]
    
    evaluate_systems = []
    if 'evaluate_systems' in config:
        evaluate_systems = config['evaluate_systems']
    
    print(f"Datasets: {datasets}")
    print(f"Systems to evaluate: {evaluate_systems}")
    
    if not datasets or not evaluate_systems:
        print("[!] No datasets or systems configured")
        return
    
    # Generate timing visualizations for each dataset
    print("\n" + "="*60)
    print("GENERATING TIMING VISUALIZATIONS")
    print("="*60)
    
    for dataset_name in datasets:
        print(f"\nProcessing dataset: {dataset_name}")
        
        # Paths
        timing_results_file = Path(f"results/metrics/time_reports/{dataset_name}_timing_results.json")
        raw_outputs_dir = Path("results/raw_outputs")
        
        # Generate timing visualizations
        timing_results = generate_timing_visualizations(
            dataset_name=dataset_name,
            timing_results_file=timing_results_file,
            raw_outputs_dir=raw_outputs_dir,
            systems=evaluate_systems,
            output_base_dir="results/visualizations"
        )
        
        if timing_results:
            print(f"[✓] Generated {len(timing_results)} timing visualization files for {dataset_name}")
        else:
            print(f"[!] No timing visualizations generated for {dataset_name}")
    
    # Generate accuracy visualizations for each dataset
    print("\n" + "="*60)
    print("GENERATING ACCURACY VISUALIZATIONS")
    print("="*60)
    
    for dataset_name in datasets:
        print(f"\nProcessing dataset: {dataset_name}")
        
        # Paths
        accuracy_results_file = Path(f"results/metrics/accuracy_reports/{dataset_name}_accuracy_results.json")
        legacy_results_dir = Path("results")
        
        # Generate accuracy visualizations
        accuracy_results = generate_accuracy_visualizations(
            dataset_name=dataset_name,
            accuracy_results_file=accuracy_results_file,
            legacy_results_dir=legacy_results_dir,
            systems=evaluate_systems,
            output_base_dir="results/visualizations"
        )
        
        if accuracy_results:
            print(f"[✓] Generated {len(accuracy_results)} accuracy visualization files for {dataset_name}")
        else:
            print(f"[!] No accuracy visualizations generated for {dataset_name}")
    
    print("\n" + "="*80)
    print("ALL VISUALIZATION GENERATION COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("- Timing comparison plots: results/visualizations/time/plots/")
    print("- Timing statistics tables: results/visualizations/time/tables/")
    print("- Accuracy comparison plots: results/visualizations/accuracy/plots/")
    print("- Accuracy statistics tables: results/visualizations/accuracy/tables/")

if __name__ == "__main__":
    main()
