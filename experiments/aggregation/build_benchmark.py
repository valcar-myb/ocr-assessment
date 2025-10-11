"""
Build benchmark metrics from aggregated ocreval reports
Reads character and word accuracy from aggregate reports and creates final benchmark
"""

import os
import json
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

CHAR_AGGREGATED_REPORT_BASE_PATH = Path("results/metrics/accuracy_reports/aggregates")
WORD_AGGREGATED_REPORT_BASE_PATH = Path("results/metrics/accuracy_reports/aggregates")
OUTPUT_PATH = Path("results/benchmark")


def read_accuracy_from_file(file_path):
    """
    Read accuracy percentage from ocreval aggregate report
    Looks for 'Accuracy' line with '%' symbol
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "Accuracy" in line and "%" in line:
                    for part in line.split():
                        if "%" in part:
                            return float(part.strip('%'))
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")
    return None


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


def build_benchmark_metrics(datasets=None, ocr_systems=None):
    """
    Build benchmark metrics from aggregated reports
    
    Args:
        datasets: List of dataset names (auto-detected if None)
        ocr_systems: List of OCR system names (auto-detected if None)
        
    Returns:
        Dictionary with structure: {dataset: {ocr: {char_accuracy, word_accuracy}}}
    """
    # Auto-detect if not provided
    if datasets is None or ocr_systems is None:
        detected_datasets, detected_systems = get_datasets_and_systems()
        datasets = datasets or detected_datasets
        ocr_systems = ocr_systems or detected_systems
    
    print(f"Building benchmark for {len(datasets)} datasets and {len(ocr_systems)} OCR systems")
    print(f"Datasets: {datasets}")
    print(f"OCR Systems: {ocr_systems}")
    print()
    
    # Initialize benchmark structure
    benchmark = {
        dataset: {
            ocr: {"char_accuracy": 0.0, "word_accuracy": 0.0} 
            for ocr in ocr_systems
        } 
        for dataset in datasets
    }
    
    # Read accuracies from files
    for dataset in datasets:
        for ocr in ocr_systems:
            # Character accuracy file
            char_path = CHAR_AGGREGATED_REPORT_BASE_PATH / dataset / f"{dataset}_{ocr}.txt"
            # Word accuracy file
            word_path = WORD_AGGREGATED_REPORT_BASE_PATH / dataset / f"{dataset}_{ocr}_word.txt"
            
            # Read character accuracy
            char_acc = read_accuracy_from_file(char_path)
            if char_acc is not None:
                benchmark[dataset][ocr]["char_accuracy"] = char_acc
            else:
                print(f"[!] Character accuracy not found for {dataset} / {ocr}")
            
            # Read word accuracy
            word_acc = read_accuracy_from_file(word_path)
            if word_acc is not None:
                benchmark[dataset][ocr]["word_accuracy"] = word_acc
            else:
                print(f"[!] Word accuracy not found for {dataset} / {ocr}")
    
    return benchmark


def print_metrics_table(benchmark_metrics):
    """
    Print benchmark metrics as formatted tables
    """
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    
    rows = []
    for dataset, systems in benchmark_metrics.items():
        for ocr_system, metrics in systems.items():
            rows.append({
                "dataset": dataset,
                "ocr_system": ocr_system,
                "char_accuracy": round(metrics["char_accuracy"], 2),
                "word_accuracy": round(metrics["word_accuracy"], 2)
            })
    
    df = pd.DataFrame(rows)
    
    # Pivot tables: rows = dataset, columns = OCR system
    char_df = df.pivot(index="dataset", columns="ocr_system", values="char_accuracy")
    word_df = df.pivot(index="dataset", columns="ocr_system", values="word_accuracy")
    
    print("\n" + "="*80)
    print("CHARACTER ACCURACY TABLE (%)")
    print("="*80)
    print(char_df.round(2).to_string())
    
    print("\n" + "="*80)
    print("WORD ACCURACY TABLE (%)")
    print("="*80)
    print(word_df.round(2).to_string())
    print()


def save_benchmark(benchmark_metrics, output_dir=OUTPUT_PATH):
    """
    Save benchmark metrics to JSON and CSV files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_file = output_dir / f"benchmark_data_{timestamp}.json"
    with open(json_file, "w", encoding='utf-8') as f:
        json.dump(benchmark_metrics, f, indent=2, ensure_ascii=False)
    print(f"[✓] Benchmark JSON saved to: {json_file}")
    
    # Also save as latest
    json_file_latest = output_dir / "benchmark_data_latest.json"
    with open(json_file_latest, "w", encoding='utf-8') as f:
        json.dump(benchmark_metrics, f, indent=2, ensure_ascii=False)
    print(f"[✓] Benchmark JSON saved to: {json_file_latest}")
    
    # Save as CSV
    rows = []
    for dataset, systems in benchmark_metrics.items():
        for ocr_system, metrics in systems.items():
            rows.append({
                "dataset": dataset,
                "ocr_system": ocr_system,
                "char_accuracy": metrics["char_accuracy"],
                "word_accuracy": metrics["word_accuracy"]
            })
    
    df = pd.DataFrame(rows)
    csv_file = output_dir / f"benchmark_data_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    print(f"[✓] Benchmark CSV saved to: {csv_file}")
    
    csv_file_latest = output_dir / "benchmark_data_latest.csv"
    df.to_csv(csv_file_latest, index=False)
    print(f"[✓] Benchmark CSV saved to: {csv_file_latest}")


def main():
    print("="*80)
    print("BUILDING BENCHMARK METRICS FROM AGGREGATED REPORTS")
    print("="*80)
    print()
    
    # Build benchmark metrics
    benchmark_metrics = build_benchmark_metrics()
    
    # Save to files
    save_benchmark(benchmark_metrics)
    
    # Print tables
    print_metrics_table(benchmark_metrics)
    
    print("="*80)
    print("BENCHMARK BUILD COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()

