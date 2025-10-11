"""
Script to aggregate both character and word accuracy reports
Runs both 'accsum' and 'wordaccsum' commands
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
    
    # Aggregate reports for each dataset and system
    for dataset_name in datasets:
        print(f"\n{'='*80}")
        print(f"Aggregating all reports for dataset: {dataset_name}")
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
                # Aggregate character accuracy
                char_report = evaluator.aggregate_reports(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_system
                )
                
                if not char_report:
                    print(f"[✗] Failed to aggregate character reports for {ocr_system}")
                
                # Aggregate word accuracy
                word_report = evaluator.aggregate_word_reports(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_system
                )
                
                if not word_report:
                    print(f"[✗] Failed to aggregate word reports for {ocr_system}")
                
                if char_report and word_report:
                    print(f"[✓] Both reports generated successfully")
                    
            except Exception as e:
                print(f"[✗] Error aggregating {ocr_system}: {e}")
    
    print(f"\n{'='*80}")
    print("Aggregation complete!")
    print(f"{'='*80}")
    print(f"\nReports saved to: {evaluator.aggregates_base_dir}")
    print(f"  Character accuracy: {{dataset}}_{{tool}}.txt")
    print(f"  Word accuracy:      {{dataset}}_{{tool}}_word.txt")


if __name__ == '__main__':
    main()

