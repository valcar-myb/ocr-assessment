"""
Accuracy evaluator for OCR systems
"""

import json
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
# Removed NED calculation - using only ocreval
from .ocreval_wrapper import OCREvalWrapper


def clean_ground_truth_text(text: str) -> str:
    """
    Clean ground truth text by normalizing whitespace
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text with normalized whitespace
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text


class AccuracyEvaluator:
    """
    Evaluator for OCR accuracy metrics using ocreval
    Two-phase approach:
    1. Generate partial reports with 'accuracy' command
    2. Aggregate with 'accsum' command
    """
    
    def __init__(self, config_path: str = "config/experiments.yaml",
                 partials_base_dir: str = "results/metrics/accuracy_reports/partials",
                 partials_word_base_dir: str = "results/metrics/accuracy_reports/partials_word",
                 aggregates_base_dir: str = "results/metrics/accuracy_reports/aggregates"):
        """
        Initialize the accuracy evaluator
        
        Args:
            config_path: Path to experiments configuration file
            partials_base_dir: Base directory for character accuracy partial reports
            partials_word_base_dir: Base directory for word accuracy partial reports
            aggregates_base_dir: Base directory for aggregated reports
        """
        self.config_path = Path(config_path)
        self.partials_base_dir = Path(partials_base_dir)
        self.partials_word_base_dir = Path(partials_word_base_dir)
        self.aggregates_base_dir = Path(aggregates_base_dir)
        self.ocreval = OCREvalWrapper()
        self.evaluate_systems = self._load_evaluate_systems()
    
    def _load_evaluate_systems(self) -> List[str]:
        """
        Load the list of systems to evaluate from config file
        
        Returns:
            List of system names to evaluate
        """
        if not self.config_path.exists():
            print(f"[!] Config file not found: {self.config_path}")
            return []
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            evaluate_systems = config.get('evaluate_systems', [])
            print(f"[✓] Loaded evaluate_systems: {evaluate_systems}")
            return evaluate_systems
            
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            return []
    
    def generate_partial_reports(self, dataset_name: str, ocr_tool_name: str,
                                text_outputs_dir: Path, ground_truth_dir: Path,
                                dataset_json: Path) -> list:
        """
        Generate partial accuracy reports for a specific OCR tool on a dataset
        Phase 1: Run 'accuracy' command for each file
        
        Args:
            dataset_name: Name of the dataset (e.g., 'sroie', 'iam')
            ocr_tool_name: Name of the OCR tool (e.g., 'tesseract', 'gpt4o')
            text_outputs_dir: Directory containing OCR text outputs
            ground_truth_dir: Directory containing ground truth files
            dataset_json: Path to dataset.json file
            
        Returns:
            List of generated partial report paths
        """
        print(f"\nGenerating partial reports for {dataset_name}/{ocr_tool_name}...")
        
        # Load dataset metadata
        with open(dataset_json, 'r', encoding='utf-8') as f:
            dataset_metadata = json.load(f)
        
        # Build file dictionaries
        gt_files = {}
        pred_files = {}
        
        for item in dataset_metadata:
            # Get file ID (without extension)
            file_id = Path(item['img']).stem
            
            # Check prediction file
            pred_file = text_outputs_dir / f"{file_id}.txt"
            if pred_file.exists():
                pred_files[file_id] = pred_file
            
            # Check ground truth file
            gt_file = ground_truth_dir / f"{file_id}.txt"
            if gt_file.exists():
                gt_files[file_id] = gt_file
        
        # Determine output directory for partial reports
        partial_dir = self.partials_base_dir / dataset_name / ocr_tool_name
        
        # Clean ground truth files and create temporary cleaned versions
        # Only for files that have both ground truth and predictions
        cleaned_gt_files = {}
        matched_files = set(gt_files.keys()) & set(pred_files.keys())
        for file_id in matched_files:
            gt_file = gt_files[file_id]
            # Read and clean ground truth
            with open(gt_file, 'r', encoding='utf-8') as f:
                gt_text = clean_ground_truth_text(f.read())
            
            # Create temporary cleaned file
            cleaned_gt_file = partial_dir / f"cleaned_{file_id}.txt"
            with open(cleaned_gt_file, 'w', encoding='utf-8') as f:
                f.write(gt_text)
            
            cleaned_gt_files[file_id] = cleaned_gt_file
        
        # Generate partial reports with cleaned ground truth
        generated_reports = self.ocreval.generate_partial_reports(
            cleaned_gt_files, pred_files, partial_dir
        )
        
        return generated_reports
    
    def generate_word_partial_reports(self, dataset_name: str, ocr_tool_name: str,
                                      text_outputs_dir: Path, ground_truth_dir: Path,
                                      dataset_json: Path) -> list:
        """
        Generate partial word accuracy reports for a specific OCR tool on a dataset
        Phase 1 (Word): Run 'wordacc' command for each file
        
        Args:
            dataset_name: Name of the dataset (e.g., 'sroie', 'iam')
            ocr_tool_name: Name of the OCR tool (e.g., 'tesseract', 'gpt4o')
            text_outputs_dir: Directory containing OCR text outputs
            ground_truth_dir: Directory containing ground truth files
            dataset_json: Path to dataset.json file
            
        Returns:
            List of generated partial word accuracy report paths
        """
        print(f"\nGenerating word accuracy partial reports for {dataset_name}/{ocr_tool_name}...")
        
        # Load dataset metadata
        with open(dataset_json, 'r', encoding='utf-8') as f:
            dataset_metadata = json.load(f)
        
        # Build file dictionaries
        gt_files = {}
        pred_files = {}
        
        for item in dataset_metadata:
            # Get file ID (without extension)
            file_id = Path(item['img']).stem
            
            # Check prediction file
            pred_file = text_outputs_dir / f"{file_id}.txt"
            if pred_file.exists():
                pred_files[file_id] = pred_file
            
            # Check ground truth file
            gt_file = ground_truth_dir / f"{file_id}.txt"
            if gt_file.exists():
                gt_files[file_id] = gt_file
        
        # Determine output directory for word accuracy partial reports
        partial_word_dir = self.partials_word_base_dir / dataset_name / ocr_tool_name
        
        # Clean ground truth files and create temporary cleaned versions
        # Only for files that have both ground truth and predictions
        cleaned_gt_files = {}
        matched_files = set(gt_files.keys()) & set(pred_files.keys())
        for file_id in matched_files:
            gt_file = gt_files[file_id]
            # Read and clean ground truth
            with open(gt_file, 'r', encoding='utf-8') as f:
                gt_text = clean_ground_truth_text(f.read())
            
            # Create temporary cleaned file
            cleaned_gt_file = partial_word_dir / f"cleaned_{file_id}.txt"
            with open(cleaned_gt_file, 'w', encoding='utf-8') as f:
                f.write(gt_text)
            
            cleaned_gt_files[file_id] = cleaned_gt_file
        
        # Generate partial word accuracy reports with cleaned ground truth
        generated_reports = self.ocreval.generate_word_partial_reports(
            cleaned_gt_files, pred_files, partial_word_dir
        )
        
        return generated_reports
    
    def aggregate_reports(self, dataset_name: str, ocr_tool_name: str) -> Optional[Path]:
        """
        Aggregate partial reports into single report
        Phase 2: Run 'accsum' command on all partial reports
        
        Args:
            dataset_name: Name of the dataset
            ocr_tool_name: Name of the OCR tool
            
        Returns:
            Path to aggregated report if successful, None otherwise
        """
        print(f"\nAggregating character accuracy reports for {dataset_name}/{ocr_tool_name}...")
        
        # Find partial reports
        partial_dir = self.partials_base_dir / dataset_name / ocr_tool_name
        
        if not partial_dir.exists():
            print(f"[!] No partial reports found in {partial_dir}")
            return None
        
        # Get only ocreval report files, exclude cleaned ground truth files
        partial_reports = [f for f in partial_dir.glob("*.txt") if not f.name.startswith("cleaned_")]
        
        if not partial_reports:
            print(f"[!] No partial reports found for {dataset_name}/{ocr_tool_name}")
            return None
        
        # Output path for aggregated report
        aggregate_dir = self.aggregates_base_dir / dataset_name
        output_report = aggregate_dir / f"{dataset_name}_{ocr_tool_name}.txt"
        
        # Run accsum
        if self.ocreval.run_accsum(partial_reports, output_report):
            return output_report
        else:
            return None
    
    def aggregate_word_reports(self, dataset_name: str, ocr_tool_name: str) -> Optional[Path]:
        """
        Aggregate partial word accuracy reports into single word accuracy report
        Phase 2: Run 'wordaccsum' command on all partial word reports
        
        Args:
            dataset_name: Name of the dataset
            ocr_tool_name: Name of the OCR tool
            
        Returns:
            Path to aggregated word accuracy report if successful, None otherwise
        """
        print(f"\nAggregating word accuracy reports for {dataset_name}/{ocr_tool_name}...")
        
        # Find partial word accuracy reports
        partial_word_dir = self.partials_word_base_dir / dataset_name / ocr_tool_name
        
        if not partial_word_dir.exists():
            print(f"[!] No partial word reports found in {partial_word_dir}")
            return None
        
        # Get only ocreval report files, exclude cleaned ground truth files
        partial_reports = [f for f in partial_word_dir.glob("*.txt") if not f.name.startswith("cleaned_")]
        
        if not partial_reports:
            print(f"[!] No partial word reports found for {dataset_name}/{ocr_tool_name}")
            return None
        
        # Output path for aggregated word accuracy report
        aggregate_dir = self.aggregates_base_dir / dataset_name
        output_report = aggregate_dir / f"{dataset_name}_{ocr_tool_name}_word.txt"
        
        # Run wordaccsum
        if self.ocreval.run_wordaccsum(partial_reports, output_report):
            return output_report
        else:
            return None
    
    def evaluate_dataset(self, dataset_name: str, ocr_tool_name: str,
                        text_outputs_dir: Path, ground_truth_dir: Path,
                        dataset_json: Path) -> Dict:
        """
        Full evaluation: generate partial reports and aggregate
        
        Args:
            dataset_name: Name of the dataset
            ocr_tool_name: Name of the OCR tool
            text_outputs_dir: Directory containing OCR text outputs
            ground_truth_dir: Directory containing ground truth files
            dataset_json: Path to dataset.json file
            
        Returns:
            Dictionary containing evaluation results
        """
        # Phase 1: Generate partial reports
        partial_reports = self.generate_partial_reports(
            dataset_name, ocr_tool_name, text_outputs_dir,
            ground_truth_dir, dataset_json
        )
        
        if not partial_reports:
            print(f"[!] No partial reports generated for {ocr_tool_name}")
            return {
                'dataset': dataset_name,
                'ocr_tool': ocr_tool_name,
                'error': 'No partial reports generated'
            }
        
        # Phase 1: Generate word accuracy partial reports
        word_partial_reports = self.generate_word_partial_reports(
            dataset_name, ocr_tool_name, text_outputs_dir,
            ground_truth_dir, dataset_json
        )
        
        # Phase 2: Aggregate character accuracy reports
        aggregate_report = self.aggregate_reports(dataset_name, ocr_tool_name)
        
        if not aggregate_report:
            print(f"[!] Failed to aggregate character reports for {ocr_tool_name}")
            return {
                'dataset': dataset_name,
                'ocr_tool': ocr_tool_name,
                'error': 'Character aggregation failed'
            }
        
        # Phase 2: Aggregate word accuracy reports
        word_aggregate_report = self.aggregate_word_reports(dataset_name, ocr_tool_name)
        
        if not word_aggregate_report:
            print(f"[!] Failed to aggregate word reports for {ocr_tool_name}")
            return {
                'dataset': dataset_name,
                'ocr_tool': ocr_tool_name,
                'error': 'Word aggregation failed'
            }
        
        # Parse aggregated reports
        char_metrics = self.ocreval.parse_aggregate_report(aggregate_report)
        word_metrics = self.ocreval.parse_aggregate_report(word_aggregate_report)
        
        # Combine metrics
        metrics = {**char_metrics, **word_metrics}
        
        # Prepare results (only ocreval metrics)
        results = {
            'dataset': dataset_name,
            'ocr_tool': ocr_tool_name,
            'n_samples': len(partial_reports),
            'metrics': {
                'char_accuracy': metrics.get('char_accuracy', 0.0),
                'word_accuracy': metrics.get('word_accuracy', 0.0),
                'cer': metrics.get('cer', 0.0),
                'wer': metrics.get('wer', 0.0),
            },
            'totals': {
                'total_chars': metrics.get('total_chars', 0),
                'total_words': metrics.get('total_words', 0),
                'char_errors': metrics.get('char_errors', 0),
                'word_errors': metrics.get('word_errors', 0),
            },
            'partial_reports_dir': str(self.partials_base_dir / dataset_name / ocr_tool_name),
            'aggregate_report': str(aggregate_report)
        }
        
        return results
    
    def evaluate_all_tools(self, dataset_name: str, dataset_json: Path,
                          ground_truth_dir: Path, text_outputs_base_dir: Path) -> Dict:
        """
        Evaluate configured OCR tools for a dataset
        
        Args:
            dataset_name: Name of the dataset
            dataset_json: Path to dataset.json file
            ground_truth_dir: Directory containing ground truth files
            text_outputs_base_dir: Base directory containing all OCR tool outputs
            
        Returns:
            Dictionary with OCR tool names as keys and their evaluation results as values
        """
        print(f"\nEvaluating configured OCR tools on {dataset_name} dataset...")
        
        if not self.evaluate_systems:
            print("[!] No systems configured for evaluation in config file")
            return {}
        
        print(f"Configured systems to evaluate: {self.evaluate_systems}")
        
        # Find all OCR tool directories
        text_outputs_dir = Path(text_outputs_base_dir)
        if not text_outputs_dir.exists():
            print(f"[!] Text outputs directory not found: {text_outputs_dir}")
            return {}
        
        # Get all subdirectories (OCR tools)
        available_tools = [d.name for d in text_outputs_dir.iterdir() if d.is_dir()]
        
        if not available_tools:
            print(f"[!] No OCR tool directories found in {text_outputs_dir}")
            return {}
        
        print(f"Available OCR tools: {available_tools}")
        
        # Filter to only configured systems
        tools_to_evaluate = [tool for tool in self.evaluate_systems if tool in available_tools]
        missing_tools = [tool for tool in self.evaluate_systems if tool not in available_tools]
        
        if missing_tools:
            print(f"[!] Missing configured tools: {missing_tools}")
        
        if not tools_to_evaluate:
            print("[!] No configured tools found in available tools")
            return {}
        
        print(f"Tools to evaluate: {tools_to_evaluate}")
        
        results = {}
        
        for ocr_tool_name in tools_to_evaluate:
            print(f"\n--- Evaluating {ocr_tool_name} ---")
            
            tool_outputs_dir = text_outputs_dir / ocr_tool_name
            
            try:
                tool_results = self.evaluate_dataset(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_tool_name,
                    text_outputs_dir=tool_outputs_dir,
                    ground_truth_dir=ground_truth_dir,
                    dataset_json=dataset_json
                )
                results[ocr_tool_name] = tool_results
                
            except Exception as e:
                print(f"[!] Error evaluating {ocr_tool_name}: {e}")
                results[ocr_tool_name] = {
                    'dataset': dataset_name,
                    'ocr_tool': ocr_tool_name,
                    'error': str(e)
                }
        
        return results
    
    def save_results(self, results: Dict, output_file: Path):
        """
        Save evaluation results to JSON file
        
        Args:
            results: Evaluation results dictionary
            output_file: Path to output JSON file
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {output_file}")
    
    def print_summary(self, results: Dict):
        """
        Print a summary of evaluation results
        
        Args:
            results: Evaluation results dictionary
        """
        print("\n" + "="*80)
        print("ACCURACY EVALUATION SUMMARY")
        print("="*80)
        
        for tool_name, tool_results in results.items():
            if 'error' in tool_results:
                print(f"\n{tool_name}: ERROR - {tool_results['error']}")
                continue
            
            print(f"\n{tool_name}:")
            print(f"  Dataset: {tool_results['dataset']}")
            print(f"  Samples: {tool_results['n_samples']}")
            print(f"  Metrics:")
            
            for metric_name, metric_value in tool_results['metrics'].items():
                print(f"    {metric_name}: {metric_value:.4f}")
        
        print("\n" + "="*80)

