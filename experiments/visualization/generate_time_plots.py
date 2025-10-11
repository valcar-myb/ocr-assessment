#!/usr/bin/env python3
"""
Generate timing visualizations for OCR systems
Simple script - just specify systems as arguments
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from evaluation.time import generate_timing_visualizations

def main():
    # Simple usage: python generate_time_plots.py [system1] [system2] ...
    systems = sys.argv[1:] if len(sys.argv) > 1 else []
    
    print("="*80)
    print("GENERATING TIMING VISUALIZATIONS")
    print("="*80)
    
    if not systems:
        print("Usage: python generate_time_plots.py [system1] [system2] ...")
        print("Example: python generate_time_plots.py tesseract mistral_ocr")
        print("Available systems: tesseract, mistral_ocr")
        return
    
    print(f"Systems to visualize: {systems}")
    
    # Generate visualizations for sroie dataset
    dataset_name = "sroie"
    timing_results_file = Path(f"results/metrics/time_reports/{dataset_name}_timing_results.json")
    raw_outputs_dir = Path("results/raw_outputs")
    
    print(f"\nProcessing dataset: {dataset_name}")
    
    # Generate visualizations
    results = generate_timing_visualizations(
        dataset_name=dataset_name,
        timing_results_file=timing_results_file,
        raw_outputs_dir=raw_outputs_dir,
        systems=systems,
        output_base_dir="results/visualizations"
    )
    
    if results:
        print(f"[✓] Generated {len(results)} visualization files for {dataset_name}")
    else:
        print(f"[!] No visualizations generated for {dataset_name}")
    
    print("\n" + "="*80)
    print("TIMING VISUALIZATION GENERATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
