"""
Time evaluation for OCR systems
Analyzes processing time from raw JSON outputs
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from .metrics import calculate_time_statistics


class TimeEvaluator:
    """
    Evaluator for processing time analysis of OCR systems
    """
    
    def __init__(self, config_path: str = "config/experiments.yaml",
                 results_base_dir: str = "results/metrics/time_reports"):
        self.config_path = Path(config_path)
        self.results_base_dir = Path(results_base_dir)
        self.evaluate_systems = self._load_evaluate_systems()
        
        # Create results directory
        self.results_base_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    def extract_processing_times(self, raw_outputs_dir: Path, 
                                dataset_name: str, ocr_tool_name: str) -> List[float]:
        """
        Extract processing times from raw JSON outputs
        
        Args:
            raw_outputs_dir: Base directory containing raw outputs
            dataset_name: Name of the dataset
            ocr_tool_name: Name of the OCR tool
            
        Returns:
            List of processing times in seconds
        """
        tool_dir = raw_outputs_dir / dataset_name / ocr_tool_name
        
        if not tool_dir.exists():
            print(f"[!] Tool directory not found: {tool_dir}")
            return []
        
        processing_times = []
        
        # Look for individual JSON files (not summary.json)
        json_files = [f for f in tool_dir.glob("*.json") if f.name != "summary.json"]
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract processing time
                if isinstance(data, dict) and 'processing_time_seconds' in data:
                    time_val = data['processing_time_seconds']
                    if isinstance(time_val, (int, float)) and time_val > 0:
                        processing_times.append(float(time_val))
                
            except Exception as e:
                print(f"[!] Error reading {json_file}: {e}")
                continue
        
        print(f"[✓] Extracted {len(processing_times)} processing times for {ocr_tool_name}")
        return processing_times
    
    def evaluate_dataset(self, dataset_name: str, ocr_tool_name: str,
                        raw_outputs_dir: Path) -> Dict[str, Any]:
        """
        Evaluate processing time for a specific dataset and OCR tool
        
        Args:
            dataset_name: Name of the dataset
            ocr_tool_name: Name of the OCR tool
            raw_outputs_dir: Base directory containing raw outputs
            
        Returns:
            Dictionary with timing evaluation results
        """
        print(f"\n--- Evaluating time for {ocr_tool_name} on {dataset_name} ---")
        
        # Extract processing times
        processing_times = self.extract_processing_times(
            raw_outputs_dir, dataset_name, ocr_tool_name
        )
        
        if not processing_times:
            return {
                'dataset': dataset_name,
                'ocr_tool': ocr_tool_name,
                'error': 'No processing times found'
            }
        
        # Calculate statistics
        stats = calculate_time_statistics(processing_times, filter_outliers_flag=True)
        
        # Prepare results
        results = {
            'dataset': dataset_name,
            'ocr_tool': ocr_tool_name,
            'n_samples': stats['count'],
            'n_filtered_samples': stats['filtered_count'],
            'timing_stats': {
                'mean_seconds': stats['mean'],
                'median_seconds': stats['median'],
                'min_seconds': stats['min'],
                'max_seconds': stats['max'],
                'std_seconds': stats['std']
            }
        }
        
        print(f"[✓] {ocr_tool_name}: {stats['count']} samples, "
              f"mean={stats['mean']:.3f}s, median={stats['median']:.3f}s")
        
        return results
    
    def evaluate_all_tools(self, dataset_name: str, raw_outputs_base_dir: Path) -> Dict[str, Any]:
        """
        Evaluate processing time for all configured OCR tools
        
        Args:
            dataset_name: Name of the dataset
            raw_outputs_base_dir: Base directory containing raw outputs
            
        Returns:
            Dictionary with timing evaluation results for all tools
        """
        print(f"\nEvaluating processing time for configured OCR tools on {dataset_name} dataset...")
        
        if not self.evaluate_systems:
            print("[!] No systems configured for evaluation in config file")
            return {}
        
        print(f"Configured systems to evaluate: {self.evaluate_systems}")
        
        raw_outputs_dir = Path(raw_outputs_base_dir)
        if not raw_outputs_dir.exists():
            print(f"[!] Raw outputs directory not found: {raw_outputs_dir}")
            return {}
        
        # Check if dataset directory exists
        dataset_dir = raw_outputs_dir / dataset_name
        if not dataset_dir.exists():
            print(f"[!] Dataset directory not found: {dataset_dir}")
            return {}
        
        available_tools = [d.name for d in dataset_dir.iterdir() if d.is_dir()]
        
        if not available_tools:
            print(f"[!] No OCR tool directories found in {dataset_dir}")
            return {}
        
        print(f"Available OCR tools: {available_tools}")
        
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
            try:
                tool_results = self.evaluate_dataset(
                    dataset_name=dataset_name,
                    ocr_tool_name=ocr_tool_name,
                    raw_outputs_dir=raw_outputs_dir
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
    
    def save_results(self, results: Dict[str, Any], dataset_name: str) -> Path:
        """
        Save timing evaluation results to JSON file
        
        Args:
            results: Results dictionary
            dataset_name: Name of the dataset
            
        Returns:
            Path to saved results file
        """
        output_file = self.results_base_dir / f"{dataset_name}_timing_results.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"[✓] Timing results saved to: {output_file}")
        return output_file
