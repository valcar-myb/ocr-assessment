"""
Modular OCR evaluation pipeline
"""

import yaml
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from evaluation.evaluator import OCREvaluator
from ocr_systems import get_ocr_system

class OCRPipeline:
    """Modular OCR evaluation pipeline"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.datasets = self.config['datasets']
        self.ocr_systems = self.config['ocr_systems']
        self.output_config = self.config['output']
        
        # Create output directories
        self.raw_output_dir = Path("results/raw_outputs")
        self.eval_output_dir = Path(self.output_config['path'])
        self.raw_output_dir.mkdir(parents=True, exist_ok=True)
        self.eval_output_dir.mkdir(parents=True, exist_ok=True)
    
    def step_extract_ocr(self):
        """Step 1: Extract text from images using OCR systems"""
        print("=== Step 1: OCR Text Extraction ===")
        
        for dataset in self.datasets:
            dataset_name = dataset['name']
            dataset_path = Path(dataset['path'])
            
            print(f"\nProcessing dataset: {dataset_name}")
            
            # Load dataset metadata
            metadata_file = dataset_path / 'dataset.json'
            if not metadata_file.exists():
                print(f"Warning: dataset.json not found in {dataset_path}")
                continue
            
            with open(metadata_file, 'r') as f:
                dataset_metadata = json.load(f)
            
            for ocr_system_config in self.ocr_systems:
                system_name = ocr_system_config['name']
                print(f"  Processing with {system_name}...")
                
                # Initialize OCR system
                ocr_system = get_ocr_system(system_name, ocr_system_config['config'])
                
                # Process all images and save raw outputs
                image_paths = []
                for item in dataset_metadata:
                    image_path = dataset_path / item['img']
                    if image_path.exists():
                        image_paths.append(str(image_path))
                
                # Use the new batch method that saves raw outputs individually
                output_dir = ocr_system.batch_extract_and_save(image_paths, dataset_name)
                print(f"    Saved {len(image_paths)} individual files to {output_dir}")
        
        print("\n=== OCR Extraction Complete ===")
    
    def step_evaluate_results(self):
        """Step 2: Evaluate OCR results and calculate metrics"""
        print("=== Step 2: OCR Evaluation ===")
        
        evaluator = OCREvaluator(self.config)
        
        for dataset in self.datasets:
            dataset_name = dataset['name']
            print(f"\nEvaluating dataset: {dataset_name}")
            
            for ocr_system_config in self.ocr_systems:
                system_name = ocr_system_config['name']
                print(f"  Evaluating {system_name}...")
                
                # Load raw results from new directory structure
                raw_dir = self.raw_output_dir / dataset_name / system_name
                if not raw_dir.exists():
                    print(f"    Warning: Raw results directory not found: {raw_dir}")
                    continue
                
                # Find all raw files
                raw_files = list(raw_dir.glob("*_raw.json"))
                if not raw_files:
                    print(f"    Warning: No raw files found in {raw_dir}")
                    continue
                
                # Extract predictions and ground truth
                predictions = []
                ground_truth = []
                
                for raw_file in raw_files:
                    with open(raw_file, 'r') as f:
                        raw_data = json.load(f)
                    
                    predictions.append(raw_data.get('extracted_text', ''))
                    
                    # Load ground truth
                    image_filename = raw_data.get('image_filename', '')
                    if image_filename:
                        # Find corresponding ground truth file
                        gt_filename = Path(image_filename).stem + '.txt'
                        gt_path = Path(dataset['path']) / 'gt' / gt_filename
                        if gt_path.exists():
                            with open(gt_path, 'r', encoding='utf-8') as f:
                                gt_text = f.read().strip()
                                ground_truth.append(gt_text)
                        else:
                            ground_truth.append("")
                    else:
                        ground_truth.append("")
                
                # Calculate metrics
                from evaluation.metrics import (
                    calculate_character_accuracy, 
                    calculate_word_accuracy, 
                    calculate_cer, 
                    calculate_wer
                )
                
                metrics_results = {}
                for metric in self.config['metrics']:
                    if metric == 'character_accuracy':
                        metrics_results[metric] = calculate_character_accuracy(predictions, ground_truth)
                    elif metric == 'word_accuracy':
                        metrics_results[metric] = calculate_word_accuracy(predictions, ground_truth)
                    elif metric == 'cer':
                        metrics_results[metric] = calculate_cer(predictions, ground_truth)
                    elif metric == 'wer':
                        metrics_results[metric] = calculate_wer(predictions, ground_truth)
                
                # Save evaluation results
                eval_file = self.eval_output_dir / f"{dataset_name}_{system_name}_eval.json"
                eval_data = {
                    'dataset': dataset_name,
                    'system': system_name,
                    'metrics': metrics_results,
                    'sample_count': len(predictions),
                    'raw_results_directory': str(raw_dir),
                    'raw_files_count': len(raw_files)
                }
                
                with open(eval_file, 'w') as f:
                    json.dump(eval_data, f, indent=2)
                
                print(f"    Saved evaluation to {eval_file}")
                print(f"    Metrics: {metrics_results}")
        
        print("\n=== Evaluation Complete ===")
    
    def step_generate_summary(self):
        """Step 3: Generate summary report"""
        print("=== Step 3: Generating Summary Report ===")
        
        summary_data = {}
        
        for dataset in self.datasets:
            dataset_name = dataset['name']
            summary_data[dataset_name] = {}
            
            for ocr_system_config in self.ocr_systems:
                system_name = ocr_system_config['name']
                
                eval_file = self.eval_output_dir / f"{dataset_name}_{system_name}_eval.json"
                if eval_file.exists():
                    with open(eval_file, 'r') as f:
                        eval_data = json.load(f)
                    summary_data[dataset_name][system_name] = eval_data['metrics']
        
        # Save summary
        summary_file = self.eval_output_dir / "summary_report.json"
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        print(f"Summary report saved to {summary_file}")
        print("\n=== Summary Complete ===")

def main():
    parser = argparse.ArgumentParser(description='OCR Evaluation Pipeline')
    parser.add_argument('--config', default='config/experiments.yaml', 
                       help='Path to configuration file')
    parser.add_argument('--step', choices=['extract', 'evaluate', 'summary', 'all'], 
                       default='all', help='Which step to run')
    
    args = parser.parse_args()
    
    pipeline = OCRPipeline(args.config)
    
    if args.step == 'extract' or args.step == 'all':
        pipeline.step_extract_ocr()
    
    if args.step == 'evaluate' or args.step == 'all':
        pipeline.step_evaluate_results()
    
    if args.step == 'summary' or args.step == 'all':
        pipeline.step_generate_summary()

if __name__ == "__main__":
    main()
