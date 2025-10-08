"""
Main OCR evaluator class
"""

import yaml
import json
from pathlib import Path
from .metrics import calculate_character_accuracy, calculate_word_accuracy, calculate_cer, calculate_wer
from ocr_systems import get_ocr_system

class OCREvaluator:
    def __init__(self, config):
        self.config = config
        self.datasets = config['datasets']
        self.ocr_systems = config['ocr_systems']
        self.metrics = config['metrics']
        self.output_config = config['output']
    
    def run_evaluation(self):
        """Run complete OCR evaluation"""
        results = {}
        
        for dataset in self.datasets:
            results[dataset['name']] = {}
            
            # Load dataset metadata
            dataset_path = Path(dataset['path'])
            metadata_file = dataset_path / 'dataset.json'
            
            if not metadata_file.exists():
                print(f"Warning: dataset.json not found in {dataset_path}")
                continue
                
            with open(metadata_file, 'r') as f:
                dataset_metadata = json.load(f)
            
            for ocr_system_config in self.ocr_systems:
                system_name = ocr_system_config['name']
                print(f"Evaluating {system_name} on {dataset['name']}...")
                
                # Initialize OCR system
                ocr_system = get_ocr_system(system_name, ocr_system_config['config'])
                
                # Run OCR system on dataset
                predictions = self._run_ocr_system(ocr_system, dataset_metadata, dataset_path)
                ground_truth = self._load_ground_truth(dataset_metadata, dataset_path)
                
                # Calculate metrics
                system_results = {}
                for metric in self.metrics:
                    if metric == 'character_accuracy':
                        system_results[metric] = calculate_character_accuracy(predictions, ground_truth)
                    elif metric == 'word_accuracy':
                        system_results[metric] = calculate_word_accuracy(predictions, ground_truth)
                    elif metric == 'cer':
                        system_results[metric] = calculate_cer(predictions, ground_truth)
                    elif metric == 'wer':
                        system_results[metric] = calculate_wer(predictions, ground_truth)
                
                results[dataset['name']][system_name] = system_results
        
        return results
    
    def _run_ocr_system(self, ocr_system, dataset_metadata, dataset_path):
        """Run specific OCR system on dataset"""
        predictions = []
        
        for item in dataset_metadata:
            image_path = dataset_path / item['img']
            if image_path.exists():
                text = ocr_system.extract_text(str(image_path))
                predictions.append(text)
            else:
                print(f"Warning: Image not found: {image_path}")
                predictions.append("")
        
        return predictions
    
    def _load_ground_truth(self, dataset_metadata, dataset_path):
        """Load ground truth for dataset"""
        ground_truth = []
        
        for item in dataset_metadata:
            gt_path = dataset_path / item['gt']
            if gt_path.exists():
                with open(gt_path, 'r', encoding='utf-8') as f:
                    text = f.read().strip()
                    ground_truth.append(text)
            else:
                print(f"Warning: Ground truth not found: {gt_path}")
                ground_truth.append("")
        
        return ground_truth
    
    def save_results(self, results):
        """Save evaluation results"""
        output_path = Path(self.output_config['path'])
        output_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.output_config['filename']}.{self.output_config['format']}"
        filepath = output_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
