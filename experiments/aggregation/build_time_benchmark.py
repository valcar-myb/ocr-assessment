"""
Build time benchmark metrics from timing evaluation results
Reads timing statistics and creates final benchmark
"""

import json
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

TIMING_RESULTS_BASE_PATH = Path("results/metrics/time_reports")
OUTPUT_PATH = Path("results/benchmark")


def load_config(config_path="config/experiments.yaml"):
    """
    Load configuration from experiments.yaml
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        return {}


def get_datasets_and_systems():
    """
    Get datasets and OCR systems from config file
    """
    config = load_config()
    
    # Get datasets from config
    datasets = []
    if 'datasets' in config:
        datasets = [d['name'] for d in config['datasets'] if d.get('name')]
    
    # Get systems to evaluate from config
    ocr_systems = []
    if 'evaluate_systems' in config:
        ocr_systems = config['evaluate_systems']
    
    print(f"[✓] Loaded from config - Datasets: {datasets}, Systems: {ocr_systems}")
    
    return datasets, ocr_systems


def build_time_benchmark_metrics(datasets=None, ocr_systems=None):
    """
    Build time benchmark metrics from timing results
    
    Args:
        datasets: List of dataset names (auto-detected if None)
        ocr_systems: List of OCR system names (auto-detected if None)
        
    Returns:
        Dictionary with structure: {dataset: {ocr: {timing_metrics}}}
    """
    # Auto-detect if not provided
    if datasets is None or ocr_systems is None:
        detected_datasets, detected_systems = get_datasets_and_systems()
        datasets = datasets or detected_datasets
        ocr_systems = ocr_systems or detected_systems
    
    print(f"Building time benchmark for {len(datasets)} datasets and {len(ocr_systems)} OCR systems")
    print(f"Datasets: {datasets}")
    print(f"OCR Systems: {ocr_systems}")
    print()
    
    # Initialize benchmark structure
    benchmark = {
        dataset: {
            ocr: {
                "mean_seconds": 0.0,
                "median_seconds": 0.0,
                "min_seconds": 0.0,
                "max_seconds": 0.0,
                "std_seconds": 0.0,
                "n_samples": 0
            } 
            for ocr in ocr_systems
        } 
        for dataset in datasets
    }
    
    # Read timing results from files
    for dataset in datasets:
        timing_file = TIMING_RESULTS_BASE_PATH / f"{dataset}_timing_results.json"
        
        if not timing_file.exists():
            print(f"[!] Timing results file not found: {timing_file}")
            continue
        
        try:
            with open(timing_file, 'r', encoding='utf-8') as f:
                timing_data = json.load(f)
            
            for ocr in ocr_systems:
                if ocr in timing_data:
                    tool_data = timing_data[ocr]
                    
                    if 'error' not in tool_data:
                        timing_stats = tool_data.get('timing_stats', {})
                        
                        benchmark[dataset][ocr] = {
                            "mean_seconds": timing_stats.get('mean_seconds', 0.0),
                            "median_seconds": timing_stats.get('median_seconds', 0.0),
                            "min_seconds": timing_stats.get('min_seconds', 0.0),
                            "max_seconds": timing_stats.get('max_seconds', 0.0),
                            "std_seconds": timing_stats.get('std_seconds', 0.0),
                            "n_samples": tool_data.get('n_samples', 0)
                        }
                    else:
                        print(f"[!] Error in {ocr} data: {tool_data['error']}")
                else:
                    print(f"[!] No data found for {ocr} in {timing_file}")
        
        except Exception as e:
            print(f"[!] Error reading {timing_file}: {e}")
    
    return benchmark


def print_time_metrics_table(benchmark_metrics):
    """
    Print time benchmark metrics as formatted tables
    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    
    # Processing time tables
    rows = []
    for dataset, systems in benchmark_metrics.items():
        for ocr_system, metrics in systems.items():
            rows.append({
                "dataset": dataset,
                "ocr_system": ocr_system,
                "mean_seconds": round(metrics["mean_seconds"], 3),
                "median_seconds": round(metrics["median_seconds"], 3),
                "min_seconds": round(metrics["min_seconds"], 3),
                "max_seconds": round(metrics["max_seconds"], 3),
                "std_seconds": round(metrics["std_seconds"], 3),
                "n_samples": metrics["n_samples"]
            })
    
    df = pd.DataFrame(rows)
    
    # Pivot tables: rows = dataset, columns = OCR system
    mean_df = df.pivot(index="dataset", columns="ocr_system", values="mean_seconds")
    median_df = df.pivot(index="dataset", columns="ocr_system", values="median_seconds")
    
    print("\n" + "="*80)
    print("MEAN PROCESSING TIME TABLE (seconds)")
    print("="*80)
    print(mean_df.round(3).to_string())
    
    print("\n" + "="*80)
    print("MEDIAN PROCESSING TIME TABLE (seconds)")
    print("="*80)
    print(median_df.round(3).to_string())
    print()


def save_time_benchmark(benchmark_metrics, output_dir=OUTPUT_PATH):
    """
    Save time benchmark metrics to JSON and CSV files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_file = output_dir / f"time_benchmark_{timestamp}.json"
    with open(json_file, "w", encoding='utf-8') as f:
        json.dump(benchmark_metrics, f, indent=2, ensure_ascii=False)
    print(f"[✓] Time benchmark JSON saved to: {json_file}")
    
    # Also save as latest
    json_file_latest = output_dir / "time_benchmark_latest.json"
    with open(json_file_latest, "w", encoding='utf-8') as f:
        json.dump(benchmark_metrics, f, indent=2, ensure_ascii=False)
    print(f"[✓] Time benchmark JSON saved to: {json_file_latest}")
    
    # Save as CSV
    rows = []
    for dataset, systems in benchmark_metrics.items():
        for ocr_system, metrics in systems.items():
            rows.append({
                "dataset": dataset,
                "ocr_system": ocr_system,
                "mean_seconds": metrics["mean_seconds"],
                "median_seconds": metrics["median_seconds"],
                "min_seconds": metrics["min_seconds"],
                "max_seconds": metrics["max_seconds"],
                "std_seconds": metrics["std_seconds"],
                "n_samples": metrics["n_samples"]
            })
    
    df = pd.DataFrame(rows)
    csv_file = output_dir / f"time_benchmark_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    print(f"[✓] Time benchmark CSV saved to: {csv_file}")
    
    csv_file_latest = output_dir / "time_benchmark_latest.csv"
    df.to_csv(csv_file_latest, index=False)
    print(f"[✓] Time benchmark CSV saved to: {csv_file_latest}")


def main():
    print("="*80)
    print("BUILDING TIME BENCHMARK METRICS FROM TIMING RESULTS")
    print("="*80)
    print()
    
    # Build benchmark metrics
    benchmark_metrics = build_time_benchmark_metrics()
    
    # Save to files
    save_time_benchmark(benchmark_metrics)
    
    # Print tables
    print_time_metrics_table(benchmark_metrics)
    
    print("="*80)
    print("TIME BENCHMARK BUILD COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
