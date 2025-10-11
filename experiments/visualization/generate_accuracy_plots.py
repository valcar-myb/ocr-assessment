#!/usr/bin/env python3
"""
Generate accuracy visualizations for OCR systems
Simple script - just specify systems as arguments
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / "src"))

from evaluation.accuracy import generate_accuracy_visualizations

def main():
    # Simple usage: python generate_accuracy_plots.py [system1] [system2] ...
    systems = sys.argv[1:] if len(sys.argv) > 1 else []
    
    print("="*80)
    print("GENERATING ACCURACY VISUALIZATIONS")
    print("="*80)
    
    if not systems:
        print("Usage: python generate_accuracy_plots.py [system1] [system2] ...")
        print("Example: python generate_accuracy_plots.py tesseract mistral_ocr")
        print("Available systems: tesseract, mistral_ocr")
        return
    
    print(f"Systems to visualize: {systems}")
    
    # Generate visualizations for sroie dataset
    dataset_name = "sroie"
    accuracy_results_file = Path(f"results/metrics/accuracy_reports/{dataset_name}_accuracy_results.json")
    legacy_results_dir = Path("results")
    
    print(f"\nProcessing dataset: {dataset_name}")
    
    # Generate visualizations
    results = generate_accuracy_visualizations(
        dataset_name=dataset_name,
        accuracy_results_file=accuracy_results_file,
        legacy_results_dir=legacy_results_dir,
        systems=systems,
        output_base_dir="results/visualizations"
    )
    
    if results:
        print(f"[✓] Generated {len(results)} visualization files for {dataset_name}")
        print("\nGenerated files:")
        for file_path in results:
            print(f"  - {file_path}")
    else:
        print(f"[!] No visualizations generated for {dataset_name}")
    
    print("\n" + "="*80)
    print("ACCURACY VISUALIZATION GENERATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
