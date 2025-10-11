"""
Script to aggregate word accuracy reports using ocreval 'wordaccsum' command
Aggregates partial reports into word accuracy summaries
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evaluation.accuracy import AccuracyEvaluator


def main():
    # Configuration
    datasets = ['sroie']  # Add more datasets: ['iam', 'sroie', 'funsd']
    
    # OCR systems to aggregate (optional - if empty, aggregates all found systems)
    ocr_systems = []  # e.g., ['tesseract', 'doctr', 'paddleocr', 'gpt4o', ...]
    
    # Initialize evaluator
    print("Initializing accuracy evaluator...")
    evaluator = AccuracyEvaluator()
    
    # Aggregate word accuracy reports for each dataset and system
    for dataset_name in datasets:
        print(f"\n{'='*80}")
        print(f"Aggregating word accuracy reports for dataset: {dataset_name}")
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
                # Aggregate word accuracy reports
                word_report = evaluator.aggregate_word_reports(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_system
                )
                
                if word_report:
                    print(f"[✓] Success: {word_report}")
                else:
                    print(f"[✗] Failed to aggregate word reports for {ocr_system}")
                    
            except Exception as e:
                print(f"[✗] Error aggregating {ocr_system}: {e}")
    
    print(f"\n{'='*80}")
    print("Word accuracy aggregation complete!")
    print(f"{'='*80}")
    print(f"\nWord accuracy aggregated reports saved to: {evaluator.aggregates_base_dir}")
    print(f"Filenames: {{dataset}}_{{tool}}_word.txt")


if __name__ == '__main__':
    main()

