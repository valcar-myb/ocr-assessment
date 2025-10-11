"""
Script to generate partial accuracy reports using ocreval 'accuracy' command
Phase 1: Generate individual reports for each file
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evaluation.accuracy import AccuracyEvaluator


def main():
    # Configuration
    datasets = ['sroie']  # Add more datasets as needed: ['iam', 'sroie', 'funsd']
    
    # Paths
    project_root = Path(__file__).parent.parent
    
    # Initialize evaluator
    print("Initializing accuracy evaluator...")
    evaluator = AccuracyEvaluator()
    
    # Generate partial reports for each dataset
    for dataset_name in datasets:
        print(f"\n{'='*80}")
        print(f"Processing dataset: {dataset_name}")
        print(f"{'='*80}")
        
        dataset_json = project_root / 'data' / 'raw' / dataset_name / 'dataset.json'
        ground_truth_dir = project_root / 'data' / 'raw' / dataset_name / 'gt'
        text_outputs_base_dir = project_root / 'results' / 'text_outputs' / dataset_name
        
        if not dataset_json.exists():
            print(f"[!] Dataset metadata not found: {dataset_json}")
            continue
        
        # Iterate through all OCR tool directories
        for tool_dir in text_outputs_base_dir.iterdir():
            if tool_dir.is_dir():
                ocr_tool_name = tool_dir.name
                
                print(f"\n{'-'*80}")
                print(f"OCR Tool: {ocr_tool_name}")
                print(f"{'-'*80}")
                
                try:
                    # Generate partial reports
                    partial_reports = evaluator.generate_partial_reports(
                        dataset_name=dataset_name,
                        ocr_tool_name=ocr_tool_name,
                        text_outputs_dir=tool_dir,
                        ground_truth_dir=ground_truth_dir,
                        dataset_json=dataset_json
                    )
                    
                    print(f"[✓] Generated {len(partial_reports)} partial reports")
                    
                except Exception as e:
                    print(f"[✗] Error processing {ocr_tool_name}: {e}")
    
    print(f"\n{'='*80}")
    print("Partial reports generation complete!")
    print(f"{'='*80}")
    print(f"\nPartial reports saved to: {evaluator.partials_base_dir}")
    print(f"\nNext step: Run 'python aggregate_reports.py' to create aggregated reports")


if __name__ == '__main__':
    main()

