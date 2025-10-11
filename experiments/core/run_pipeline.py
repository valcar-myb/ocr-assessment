"""
Modular OCR evaluation pipeline
"""

import yaml
import json
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import sys
from tqdm import tqdm

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from evaluation.accuracy import AccuracyEvaluator
from ocr_systems import get_ocr_system

class OCRPipeline:
    """Modular OCR evaluation pipeline"""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.datasets = self.config['datasets']
        self.ocr_systems = self.config['ocr_systems']
        self.evaluate_systems = self.config.get('evaluate_systems', [])
        self.output_config = self.config['output']
        
        # Create output directories
        self.raw_output_dir = Path("results/raw_outputs")
        self.eval_output_dir = Path(self.output_config['path'])
        self.raw_output_dir.mkdir(parents=True, exist_ok=True)
        self.eval_output_dir.mkdir(parents=True, exist_ok=True)
    
    def step_extract_ocr(self):
        """Step 1: Extract text from images using OCR systems"""
        print("=== Step 1: OCR Text Extraction ===")
        
        # Calculate total number of operations for progress tracking
        total_operations = 0
        for dataset in self.datasets:
            dataset_path = Path(dataset['path'])
            metadata_file = dataset_path / 'dataset.json'
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    dataset_metadata = json.load(f)
                total_operations += len(self.ocr_systems) * len(dataset_metadata)
        
        # Single progress bar for overall extraction
        with tqdm(total=total_operations, desc="OCR Extraction", unit="images", 
                 bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}") as pbar:
            
            for dataset in self.datasets:
                dataset_name = dataset['name']
                dataset_path = Path(dataset['path'])
                
                # Load dataset metadata
                metadata_file = dataset_path / 'dataset.json'
                if not metadata_file.exists():
                    print(f"Warning: dataset.json not found in {dataset_path}")
                    continue
                
                with open(metadata_file, 'r') as f:
                    dataset_metadata = json.load(f)
                
                # Process each OCR system
                for ocr_system_config in self.ocr_systems:
                    system_name = ocr_system_config['name']
                    
                    # Update progress bar description
                    pbar.set_postfix_str(f"{dataset_name} - {system_name}")
                    
                    # Initialize OCR system
                    ocr_system = get_ocr_system(system_name, ocr_system_config['config'])
                    
                    # Process all images and save raw outputs
                    image_paths = []
                    for item in dataset_metadata:
                        image_path = dataset_path / item['img']
                        if image_path.exists():
                            image_paths.append(str(image_path))
                    
                    # Process images individually for better progress tracking
                    for img_path in image_paths:
                        try:
                            # Measure processing time if enabled in config
                            measure_time = ocr_system.config.get('measure_time', False)
                            
                            start_time = time.time()
                            # Extract raw output from single image
                            raw_output = ocr_system.extract_raw_output(img_path)
                            end_time = time.time()
                            
                            processing_time = end_time - start_time if measure_time else None
                            timestamp = datetime.now().isoformat()
                            
                            # Save individual result (replicate the logic from batch_extract_and_save)
                            dataset_system_dir = ocr_system.output_dir / dataset_name / system_name
                            dataset_system_dir.mkdir(parents=True, exist_ok=True)
                            
                            # Create filename from image path
                            image_file = Path(img_path)
                            output_filename = image_file.stem + "_raw.json"
                            output_file = dataset_system_dir / output_filename
                            
                            # Prepare output data
                            output_data = {
                                'image_path': str(image_path),
                                'system': system_name,
                                'dataset': dataset_name,
                                'timestamp': timestamp,
                                'raw_output': raw_output
                            }
                            
                            if processing_time is not None:
                                output_data['processing_time_seconds'] = processing_time
                            
                            # Save to file
                            with open(output_file, 'w') as f:
                                json.dump(output_data, f, indent=2)
                            
                            # Update progress
                            pbar.update(1)
                            
                        except Exception as e:
                            print(f"⚠️  Error processing {img_path}: {e}")
                            # Still update progress even on error
                            pbar.update(1)
                    
                    print(f"✓ {system_name}: {len(image_paths)} images processed")
        
        print("\n=== OCR Extraction Complete ===")
    
    def step_clean_ground_truth(self):
        """Step 2: Clean ground truth files using character whitelist"""
        print("=== Step 2: Clean Ground Truth Files ===")
        
        # Import and run ground truth cleaning script
        import subprocess
        import sys
        
        clean_gt_script = Path(__file__).parent.parent / "utilities" / "clean_ground_truth.py"
        
        if clean_gt_script.exists():
            # Process each dataset
            for dataset in self.datasets:
                dataset_name = dataset['name']
                print(f"\nCleaning ground truth for dataset: {dataset_name}")
                
                result = subprocess.run(
                    [sys.executable, str(clean_gt_script), 
                     "--config", str(self.config_path),
                     "--dataset", dataset_name],
                    capture_output=False,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✓ Ground truth cleaned for {dataset_name}")
                else:
                    print(f"✗ Error cleaning ground truth for {dataset_name}")
            
            print("\n=== Ground Truth Cleaning Complete ===")
        else:
            print(f"Error: {clean_gt_script} not found")
            print("Please run: python experiments/utilities/clean_ground_truth.py")
    
    def step_generate_text(self):
        """Step 3: Generate cleaned text files from raw OCR outputs"""
        print("=== Step 3: Generate Text Files ===")
        
        # Import and run text generation script
        import subprocess
        import sys
        
        text_script = Path(__file__).parent.parent / "utilities" / "generate_text.py"
        
        if text_script.exists():
            result = subprocess.run(
                [sys.executable, str(text_script), "--config", str(self.config_path)],
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print("\n=== Text Generation Complete ===")
            else:
                print("\n=== Error generating text files ===")
        else:
            print(f"Error: {text_script} not found")
            print("Please run: python experiments/utilities/generate_text.py")
    
    def step_evaluate_results(self):
        """Step 4: Evaluate OCR results using ocreval workflow"""
        print("=== Step 4: OCR Evaluation with ocreval ===")
        
        # Check if evaluate_systems is configured
        if not self.evaluate_systems:
            print("Warning: No systems configured for evaluation in 'evaluate_systems'")
            print("Please add system names to the 'evaluate_systems' list in your config file")
            return
        
        print(f"Evaluating {len(self.evaluate_systems)} systems: {', '.join(self.evaluate_systems)}")
        
        # Initialize accuracy evaluator
        evaluator = AccuracyEvaluator()
        
        # Phase 1: Generate partial reports (character and word)
        print("\n--- Phase 1: Generating Partial Reports ---")
        for dataset in self.datasets:
            dataset_name = dataset['name']
            dataset_path = Path(dataset['path'])
            dataset_json = dataset_path / 'dataset.json'
            ground_truth_dir = dataset_path / 'gt'
            text_outputs_base_dir = Path('results/text_outputs') / dataset_name
            
            if not dataset_json.exists():
                print(f"Warning: dataset.json not found for {dataset_name}")
                continue
            
            print(f"\nDataset: {dataset_name}")
            
            for system_name in self.evaluate_systems:
                text_outputs_dir = text_outputs_base_dir / system_name
                
                if not text_outputs_dir.exists():
                    print(f"  Warning: Text outputs not found for {system_name}")
                    continue
                
                print(f"  {system_name}:")
                
                # Generate character accuracy partial reports
                try:
                    char_reports = evaluator.generate_partial_reports(
                        dataset_name, system_name, text_outputs_dir,
                        ground_truth_dir, dataset_json
                    )
                    print(f"    ✓ Generated {len(char_reports)} character partial reports")
                except Exception as e:
                    print(f"    ✗ Error generating character reports: {e}")
                
                # Generate word accuracy partial reports
                try:
                    word_reports = evaluator.generate_word_partial_reports(
                        dataset_name, system_name, text_outputs_dir,
                        ground_truth_dir, dataset_json
                    )
                    print(f"    ✓ Generated {len(word_reports)} word partial reports")
                except Exception as e:
                    print(f"    ✗ Error generating word reports: {e}")
        
        # Phase 2: Aggregate reports
        print("\n--- Phase 2: Aggregating Reports ---")
        for dataset in self.datasets:
            dataset_name = dataset['name']
            print(f"\nDataset: {dataset_name}")
            
            for system_name in self.evaluate_systems:
                print(f"  {system_name}:")
                
                # Aggregate character accuracy
                try:
                    char_agg = evaluator.aggregate_reports(dataset_name, system_name)
                    if char_agg:
                        print(f"    ✓ Character aggregate: {char_agg.name}")
                except Exception as e:
                    print(f"    ✗ Error aggregating character reports: {e}")
                
                # Aggregate word accuracy
                try:
                    word_agg = evaluator.aggregate_word_reports(dataset_name, system_name)
                    if word_agg:
                        print(f"    ✓ Word aggregate: {word_agg.name}")
                except Exception as e:
                    print(f"    ✗ Error aggregating word reports: {e}")
        
        print("\n=== Evaluation Complete ===")
        print(f"\nPartial reports saved to:")
        print(f"  Character: {evaluator.partials_base_dir}")
        print(f"  Word:      {evaluator.partials_word_base_dir}")
        print(f"Aggregated reports saved to:")
        print(f"  {evaluator.aggregates_base_dir}")
        print(f"\nNext step: Run 'python experiments/aggregation/build_benchmark.py' to generate final metrics")
    
    def step_generate_summary(self):
        """Step 5: Generate benchmark summary from aggregated reports"""
        print("=== Step 5: Generating Benchmark Summary ===")
        
        # Import and run benchmark builder
        import subprocess
        import sys
        
        build_script = Path(__file__).parent.parent / "aggregation" / "build_benchmark.py"
        
        if build_script.exists():
            result = subprocess.run(
                [sys.executable, str(build_script)],
                capture_output=False,
                text=True
            )
            
            if result.returncode == 0:
                print("\n=== Summary Complete ===")
            else:
                print("\n=== Error generating summary ===")
        else:
            print(f"Error: {build_script} not found")
            print("Please run: python experiments/aggregation/build_benchmark.py")

def main():
    parser = argparse.ArgumentParser(description='OCR Evaluation Pipeline')
    parser.add_argument('--config', default='config/experiments.yaml', 
                       help='Path to configuration file')
    parser.add_argument('--step', choices=['extract', 'clean_gt', 'generate_text', 'evaluate', 'summary', 'all'], 
                       default='all', help='Which step to run')
    
    args = parser.parse_args()
    
    pipeline = OCRPipeline(args.config)
    
    if args.step == 'extract' or args.step == 'all':
        pipeline.step_extract_ocr()
    
    if args.step == 'clean_gt' or args.step == 'all':
        pipeline.step_clean_ground_truth()
    
    if args.step == 'generate_text' or args.step == 'all':
        pipeline.step_generate_text()
    
    if args.step == 'evaluate' or args.step == 'all':
        pipeline.step_evaluate_results()
    
    if args.step == 'summary' or args.step == 'all':
        pipeline.step_generate_summary()

if __name__ == "__main__":
    main()
