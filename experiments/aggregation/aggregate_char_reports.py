"""
Script to aggregate partial accuracy reports using ocreval 'accsum' command
Phase 2: Aggregate individual reports into dataset/system summaries
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evaluation.accuracy import AccuracyEvaluator


def main():
    # Configuration
    datasets = ['sroie']  # Add more datasets as needed: ['iam', 'sroie', 'funsd']
    
    # OCR systems to aggregate (optional - if empty, aggregates all found systems)
    ocr_systems = []  # e.g., ['tesseract', 'doctr', 'paddleocr', 'gpt4o', ...]
    
    # Initialize evaluator
    print("Initializing accuracy evaluator...")
    evaluator = AccuracyEvaluator()
    
    # Aggregate reports for each dataset and system
    for dataset_name in datasets:
        print(f"\n{'='*80}")
        print(f"Aggregating reports for dataset: {dataset_name}")
        print(f"{'='*80}")
        
        # Find all OCR systems with partial reports
        dataset_partial_dir = evaluator.partials_base_dir / dataset_name
        
        if not dataset_partial_dir.exists():
            print(f"[!] No partial reports found for dataset {dataset_name}")
            continue
        
        # Get list of OCR systems
        if ocr_systems:
            systems_to_process = ocr_systems
        else:
            # Auto-detect from directory structure
            systems_to_process = [d.name for d in dataset_partial_dir.iterdir() if d.is_dir()]
        
        # Aggregate each system
        for ocr_system in systems_to_process:
            print(f"\n{'-'*80}")
            print(f"OCR System: {ocr_system}")
            print(f"{'-'*80}")
            
            try:
                aggregate_report = evaluator.aggregate_reports(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_system
                )
                
                if aggregate_report:
                    print(f"[✓] Success: {aggregate_report}")
                else:
                    print(f"[✗] Failed to aggregate reports for {ocr_system}")
                    
            except Exception as e:
                print(f"[✗] Error aggregating {ocr_system}: {e}")
    
    print(f"\n{'='*80}")
    print("Aggregation complete!")
    print(f"{'='*80}")
    print(f"\nAggregated reports saved to: {evaluator.aggregates_base_dir}")


if __name__ == '__main__':
    main()

