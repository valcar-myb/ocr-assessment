"""
Script to evaluate OCR accuracy for all tools on a dataset
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from evaluation.accuracy import AccuracyEvaluator


def main():
    # Configuration
    dataset_name = 'sroie'
    
    # Paths
    project_root = Path(__file__).parent.parent
    dataset_json = project_root / 'data' / 'raw' / dataset_name / 'dataset.json'
    ground_truth_dir = project_root / 'data' / 'raw' / dataset_name / 'gt'
    text_outputs_base_dir = project_root / 'results' / 'text_outputs' / dataset_name
    output_file = project_root / 'results' / 'metrics' / f'{dataset_name}_accuracy.json'
    
    # Initialize evaluator with ocreval
    # Partial reports: results/metrics/accuracy_reports/partials/{dataset}/{tool}/
    # Aggregate reports: results/metrics/accuracy_reports/aggregates/{dataset}/
    print("Initializing accuracy evaluator with ocreval...")
    evaluator = AccuracyEvaluator()
    
    # Evaluate all tools
    print(f"\nEvaluating all OCR tools on {dataset_name} dataset...")
    results = evaluator.evaluate_all_tools(
        dataset_name=dataset_name,
        dataset_json=dataset_json,
        ground_truth_dir=ground_truth_dir,
        text_outputs_base_dir=text_outputs_base_dir
    )
    
    # Save results
    evaluator.save_results(results, output_file)
    
    # Print summary
    evaluator.print_summary(results)


if __name__ == '__main__':
    main()

