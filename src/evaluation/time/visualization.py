"""
Time evaluation visualization module
Creates plots and tables for timing analysis
"""

import json
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from matplotlib.colors import to_rgb, to_hex
from matplotlib.patches import Patch
import glob
import numpy as np
from typing import Dict, List, Any, Optional

# === FONT SIZE CONFIG ===
plt.rcParams.update({
    "font.size": 16,
    "axes.titlesize": 20,
    "axes.labelsize": 28,
    "xtick.labelsize": 28,
    "ytick.labelsize": 28,
    "legend.fontsize": 14,
    "legend.title_fontsize": 16
})

# Colori per tipi di sistema OCR
SYSTEM_TYPE_COLORS = {
    "opensource_ocr": "#38b6ff",      # Blu - Open source
    "commercial_ocr": "#ffd700",      # Oro - Commercial OCR
    "commercial_llm": "#ff6b35",      # Arancione - Commercial LLM
    "opensource_llm": "#4ecdc4",      # Turchese - Open source LLM
    "default": "#666666"              # Grigio - Default
}

def load_system_types(config_path: str = "config/experiments.yaml") -> Dict[str, str]:
    """
    Load system types from configuration file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary mapping system names to their types
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        system_types = {}
        if 'ocr_systems' in config:
            for system in config['ocr_systems']:
                if 'name' in system and 'type' in system:
                    system_types[system['name']] = system['type']
        
        return system_types
    except Exception as e:
        print(f"[!] Error loading system types: {e}")
        return {}

def get_system_color(system_name: str, system_types: Dict[str, str] = None) -> str:
    """
    Get color for a system based on its type
    
    Args:
        system_name: Name of the system
        system_types: Dictionary mapping system names to types
        
    Returns:
        Color code for the system
    """
    if system_types is None:
        system_types = load_system_types()
    
    system_type = system_types.get(system_name, "default")
    return SYSTEM_TYPE_COLORS.get(system_type, SYSTEM_TYPE_COLORS["default"])

def wrap_label(text: str) -> str:
    """Replace underscores or spaces with line breaks"""
    return text.replace("_", "\n").replace(" ", "\n")

def load_timing_data_from_results(timing_results_file: Path) -> List[Dict[str, Any]]:
    """
    Load timing data from evaluation results JSON file
    
    Args:
        timing_results_file: Path to timing results JSON file
        
    Returns:
        List of timing data records
    """
    data = []
    
    if not timing_results_file.exists():
        print(f"[!] Timing results file not found: {timing_results_file}")
        return data
    
    # Load system types for color assignment
    system_types = load_system_types()
    
    try:
        with open(timing_results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        for system_name, system_data in results.items():
            if 'error' in system_data:
                print(f"[!] Error in {system_name}: {system_data['error']}")
                continue
            
            timing_stats = system_data.get('timing_stats', {})
            n_samples = system_data.get('n_samples', 0)
            
            data.append({
                "System": system_name,
                "Label": wrap_label(system_name),
                "Mean": timing_stats.get('mean_seconds', 0.0),
                "Median": timing_stats.get('median_seconds', 0.0),
                "Min": timing_stats.get('min_seconds', 0.0),
                "Max": timing_stats.get('max_seconds', 0.0),
                "Std": timing_stats.get('std_seconds', 0.0),
                "Count": n_samples,
                "Color": get_system_color(system_name, system_types),
                "Dataset": system_data.get('dataset', 'unknown')
            })
    
    except Exception as e:
        print(f"[!] Error loading timing results: {e}")
    
    return data

def load_timing_data_from_raw_outputs(raw_outputs_dir: Path, dataset_name: str, 
                                     systems: List[str]) -> List[Dict[str, Any]]:
    """
    Load timing data directly from raw outputs
    
    Args:
        raw_outputs_dir: Base directory containing raw outputs
        dataset_name: Name of the dataset
        systems: List of systems to process
        
    Returns:
        List of timing data records
    """
    data = []
    
    # Load system types for color assignment
    system_types = load_system_types()
    
    for system_name in systems:
        system_dir = raw_outputs_dir / dataset_name / system_name
        
        if not system_dir.exists():
            print(f"[!] System directory not found: {system_dir}")
            continue
        
        # Load individual JSON files (not summary.json)
        json_files = [f for f in system_dir.glob("*.json") if f.name != "summary.json"]
        times = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                
                if isinstance(file_data, dict) and 'processing_time_seconds' in file_data:
                    time_val = file_data['processing_time_seconds']
                    if isinstance(time_val, (int, float)) and time_val > 0:
                        times.append(float(time_val))
            
            except Exception as e:
                print(f"[!] Error reading {json_file}: {e}")
                continue
        
        if not times:
            print(f"[!] No timing data found for {system_name}")
            continue
        
        # Calculate statistics
        times_array = np.array(times)
        
        data.append({
            "System": system_name,
            "Label": wrap_label(system_name),
            "Mean": times_array.mean(),
            "Median": np.median(times_array),
            "Min": times_array.min(),
            "Max": times_array.max(),
            "Std": times_array.std(),
            "Count": len(times),
            "Color": get_system_color(system_name, system_types),
            "Dataset": dataset_name
        })
    
    return data

def create_timing_comparison_plot(data: List[Dict[str, Any]], dataset_name: str, 
                                 output_dir: Path) -> Path:
    """
    Create timing comparison bar plot
    
    Args:
        data: List of timing data records
        dataset_name: Name of the dataset
        output_dir: Output directory for plots
        
    Returns:
        Path to saved plot
    """
    if not data:
        print("[!] No data to plot")
        return None
    
    df = pd.DataFrame(data)
    
    # Sort by mean time
    df_sorted = df.sort_values("Mean")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create bar plot
    bars = ax.bar(df_sorted["Label"], df_sorted["Mean"], 
                  color=df_sorted["Color"], alpha=0.8)
    
    # Add error bars (min/max)
    ax.errorbar(df_sorted["Label"], df_sorted["Mean"],
                yerr=[df_sorted["Mean"] - df_sorted["Min"], 
                      df_sorted["Max"] - df_sorted["Mean"]],
                fmt='o', color='black', capsize=5, label="Min/Max")
    
    ax.set_title(f"Processing Time Comparison - {dataset_name.upper()}", fontweight='bold')
    ax.set_ylabel("Time (seconds)")
    ax.set_xlabel("OCR System")
    
    # Add values on bars
    for i, (bar, mean_val) in enumerate(zip(bars, df_sorted["Mean"])):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{mean_val:.2f}s', ha='center', va='bottom', fontweight='bold')
    
    # Create legend with system types
    system_types = load_system_types()
    type_legend_patches = []
    used_types = set()
    
    for _, row in df_sorted.iterrows():
        system_type = system_types.get(row["System"], "default")
        if system_type not in used_types:
            type_legend_patches.append(Patch(
                color=SYSTEM_TYPE_COLORS.get(system_type, SYSTEM_TYPE_COLORS["default"]), 
                label=system_type.replace("_", " ").title()
            ))
            used_types.add(system_type)
    
    # Add min/max patch
    type_legend_patches.append(Patch(color='black', label='Min/Max'))
    
    ax.legend(handles=type_legend_patches, title="System Types", loc="upper right")
    
    plt.tight_layout()
    
    # Save plot
    output_dir.mkdir(parents=True, exist_ok=True)
    plot_path = output_dir / f"{dataset_name}_timing_comparison.png"
    plt.savefig(plot_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    return plot_path

def create_timing_boxplot(data: List[Dict[str, Any]], dataset_name: str, 
                         output_dir: Path) -> Path:
    """
    Create timing box plot
    
    Args:
        data: List of timing data records
        dataset_name: Name of the dataset
        output_dir: Output directory for plots
        
    Returns:
        Path to saved plot
    """
    if not data:
        print("[!] No data to plot")
        return None
    
    # For box plot, we need the raw timing data
    # This would require loading from raw outputs
    print("[!] Box plot requires raw timing data - not implemented yet")
    return None

def save_timing_statistics_table(data: List[Dict[str, Any]], dataset_name: str, 
                                output_dir: Path) -> Path:
    """
    Save timing statistics to CSV and Markdown tables
    
    Args:
        data: List of timing data records
        dataset_name: Name of the dataset
        output_dir: Output directory for tables
        
    Returns:
        Path to saved CSV file
    """
    if not data:
        print("[!] No data to save")
        return None
    
    df = pd.DataFrame(data)
    
    # Select columns for table
    table_columns = ["System", "Label", "Mean", "Median", "Min", "Max", "Std", "Count"]
    table_df = df[table_columns].copy()
    
    # Round numeric columns
    numeric_columns = ["Mean", "Median", "Min", "Max", "Std"]
    for col in numeric_columns:
        table_df[col] = table_df[col].round(3)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    csv_path = output_dir / f"{dataset_name}_timing_statistics.csv"
    table_df.to_csv(csv_path, index=False)
    
    # Save Markdown
    md_path = output_dir / f"{dataset_name}_timing_statistics.md"
    table_df.to_markdown(md_path, index=False)
    
    return csv_path

def generate_timing_visualizations(dataset_name: str, timing_results_file: Optional[Path] = None,
                                 raw_outputs_dir: Optional[Path] = None, 
                                 systems: Optional[List[str]] = None,
                                 output_base_dir: str = "results/visualizations") -> Dict[str, Path]:
    """
    Generate all timing visualizations for a dataset
    
    Args:
        dataset_name: Name of the dataset
        timing_results_file: Path to timing results JSON (optional)
        raw_outputs_dir: Path to raw outputs directory (optional)
        systems: List of systems to process (optional)
        output_base_dir: Base output directory
        
    Returns:
        Dictionary with paths to generated files
    """
    output_dir = Path(output_base_dir)
    plots_dir = output_dir / "time" / "plots"
    tables_dir = output_dir / "time" / "tables"
    
    print(f"\n{'='*60}")
    print(f"Generating timing visualizations for: {dataset_name.upper()}")
    print(f"{'='*60}")
    
    # Load data
    if timing_results_file and timing_results_file.exists():
        print("Loading data from timing results...")
        data = load_timing_data_from_results(timing_results_file)
        
        # Filter systems if specified
        if systems:
            data = [d for d in data if d["System"] in systems]
            print(f"Filtered to {len(data)} systems: {[d['System'] for d in data]}")
            
    elif raw_outputs_dir and systems:
        print("Loading data from raw outputs...")
        data = load_timing_data_from_raw_outputs(raw_outputs_dir, dataset_name, systems)
    else:
        print("[!] No valid data source provided")
        return {}
    
    if not data:
        print(f"[!] No timing data found for {dataset_name}")
        return {}
    
    print(f"Loaded {len(data)} systems")
    
    # Generate visualizations
    results = {}
    
    # Create comparison plot
    plot_path = create_timing_comparison_plot(data, dataset_name, plots_dir)
    if plot_path:
        results['comparison_plot'] = plot_path
        print(f"[✓] Comparison plot saved: {plot_path}")
    
    # Save statistics table
    table_path = save_timing_statistics_table(data, dataset_name, tables_dir)
    if table_path:
        results['statistics_table'] = table_path
        print(f"[✓] Statistics table saved: {table_path}")
    
    # Print summary
    print(f"\n=== TIMING STATISTICS SUMMARY - {dataset_name.upper()} ===")
    for record in data:
        print(f"{record['Label']}:")
        print(f"  Mean: {record['Mean']:.3f}s")
        print(f"  Median: {record['Median']:.3f}s")
        print(f"  Min: {record['Min']:.3f}s")
        print(f"  Max: {record['Max']:.3f}s")
        print(f"  Std: {record['Std']:.3f}s")
        print(f"  Samples: {record['Count']}")
        print()
    
    return results
