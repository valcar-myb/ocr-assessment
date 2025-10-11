"""
Accuracy evaluation visualization module
Creates plots and tables for accuracy analysis
"""

import json
import yaml
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from matplotlib.patches import Patch
from matplotlib.colors import to_rgb, to_hex
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

# Mappa delle categorie dei sistemi
SOLUTIONS_CATEGORY_MAP = {
    "tesseract": "OPEN_OCR",
    "doctr": "OPEN_OCR",
    "paddleocr": "OPEN_OCR",
    "paddleocr-ft": "OPEN_OCR",
    "google_vision": "COMMERCIAL_OCR",
    "google_document": "COMMERCIAL_OCR",
    "azure_document": "COMMERCIAL_OCR",
    "azure_vision": "COMMERCIAL_OCR",
    "aws_textract": "COMMERCIAL_OCR",
    "gpt4o": "COMMERCIAL_VLM",
    "gemini_flash": "COMMERCIAL_VLM",
    "mistral_ocr": "COMMERCIAL_VLM",
    "claude_haiku": "COMMERCIAL_VLM",
    "qwen25vl_3b": "OPEN_VLM",
    "gemma3_4b": "OPEN_VLM"
}

# Colori per categorie
CATEGORY_COLORS = {
    "OPEN_OCR": "#3de7f9",  # blu medio
    "COMMERCIAL_OCR": "#38b6ff",  # blu
    "COMMERCIAL_VLM": "#ffde59",  # giallo
    "OPEN_VLM": "#ffbd59"  # arancione
}

def darken_color(hex_color, factor=0.8):
    """Scurisce un colore hex"""
    rgb = to_rgb(hex_color)
    dark_rgb = tuple(c * factor for c in rgb)
    return to_hex(dark_rgb)

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

def get_system_category(system_name: str, system_types: Dict[str, str] = None) -> str:
    """
    Get system category for color assignment
    
    Args:
        system_name: Name of the system
        system_types: Dictionary mapping system names to types
        
    Returns:
        Category string
    """
    if system_types and system_name in system_types:
        system_type = system_types[system_name]
        if system_type == "opensource_ocr":
            return "OPEN_OCR"
        elif system_type == "commercial_ocr":
            return "COMMERCIAL_OCR"
        elif system_type == "commercial_llm":
            return "COMMERCIAL_VLM"
        elif system_type == "opensource_llm":
            return "OPEN_VLM"
    
    # Fallback to direct mapping
    return SOLUTIONS_CATEGORY_MAP.get(system_name, "OPEN_OCR")

def load_accuracy_data_from_results(accuracy_results_file: Path) -> List[Dict[str, Any]]:
    """
    Load accuracy data from evaluation results JSON file
    
    Args:
        accuracy_results_file: Path to accuracy results JSON file
        
    Returns:
        List of accuracy data records
    """
    data = []
    
    if not accuracy_results_file.exists():
        print(f"[!] Accuracy results file not found: {accuracy_results_file}")
        return data
    
    # Load system types for category assignment
    system_types = load_system_types()
    
    try:
        with open(accuracy_results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        for system_name, system_data in results.items():
            if 'error' in system_data:
                print(f"[!] Error in {system_name}: {system_data['error']}")
                continue
            
            accuracy_stats = system_data.get('accuracy_stats', {})
            n_samples = system_data.get('n_samples', 0)
            
            # Extract accuracy metrics
            char_accuracy = accuracy_stats.get('character_accuracy', 0.0) * 100  # Convert to percentage
            word_accuracy = accuracy_stats.get('word_accuracy', 0.0) * 100  # Convert to percentage
            
            category = get_system_category(system_name, system_types)
            color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["OPEN_OCR"])
            
            data.append({
                "Provider": system_name,
                "Category": category,
                "character_accuracy": char_accuracy,
                "word_accuracy": word_accuracy,
                "Color": color,
                "word_accuracy_Color": darken_color(color),
                "Label": system_name.replace("_", "\n").title(),
                "Count": n_samples,
                "Dataset": system_data.get('dataset', 'unknown')
            })
    
    except Exception as e:
        print(f"[!] Error loading accuracy results: {e}")
    
    return data

def load_accuracy_data_from_legacy(legacy_results_dir: Path, dataset_name: str, 
                                 systems: List[str]) -> List[Dict[str, Any]]:
    """
    Load accuracy data from legacy results directory
    
    Args:
        legacy_results_dir: Path to legacy results directory
        dataset_name: Name of the dataset
        systems: List of system names to process
        
    Returns:
        List of accuracy data records
    """
    data = []
    
    # Load system types for category assignment
    system_types = load_system_types()
    
    for system_name in systems:
        try:
            # Look for accuracy results in legacy format
            accuracy_file = legacy_results_dir / "benchmark" / "benchmark_data_latest.json"
            
            if accuracy_file.exists():
                with open(accuracy_file, 'r', encoding='utf-8') as f:
                    benchmark_data = json.load(f)
                
                if dataset_name in benchmark_data and system_name in benchmark_data[dataset_name]:
                    system_data = benchmark_data[dataset_name][system_name]
                    
                    char_accuracy = system_data.get("char_accuracy", 0.0)  # Already in percentage
                    word_accuracy = system_data.get("word_accuracy", 0.0)  # Already in percentage
                    
                    category = get_system_category(system_name, system_types)
                    color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["OPEN_OCR"])
                    
                    data.append({
                        "Provider": system_name,
                        "Category": category,
                        "character_accuracy": char_accuracy,
                        "word_accuracy": word_accuracy,
                        "Color": color,
                        "word_accuracy_Color": darken_color(color),
                        "Label": system_name.replace("_", "\n").title(),
                        "Count": 0,  # Not available in legacy format
                        "Dataset": dataset_name
                    })
        
        except Exception as e:
            print(f"[!] Error loading legacy data for {system_name}: {e}")
    
    return data

def generate_accuracy_visualizations(dataset_name: str, 
                                   accuracy_results_file: Path = None,
                                   legacy_results_dir: Path = None,
                                   systems: List[str] = None,
                                   output_base_dir: str = "results/visualizations") -> List[str]:
    """
    Generate accuracy visualizations for a dataset
    
    Args:
        dataset_name: Name of the dataset
        accuracy_results_file: Path to accuracy results JSON file
        legacy_results_dir: Path to legacy results directory
        systems: List of system names to process
        output_base_dir: Base directory for output files
        
    Returns:
        List of generated file paths
    """
    generated_files = []
    
    # Create output directories
    plot_output_dir = Path(output_base_dir) / "accuracy" / "plots"
    table_output_dir = Path(output_base_dir) / "accuracy" / "tables"
    plot_output_dir.mkdir(parents=True, exist_ok=True)
    table_output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    data = []
    
    # Try to load from accuracy results file first
    if accuracy_results_file and accuracy_results_file.exists():
        data = load_accuracy_data_from_results(accuracy_results_file)
    
    # If no data from results file, try legacy format
    if not data and legacy_results_dir:
        data = load_accuracy_data_from_legacy(legacy_results_dir, dataset_name, systems or [])
    
    if not data:
        print(f"[!] No accuracy data found for {dataset_name}")
        return generated_files
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    if df.empty:
        print(f"[!] No accuracy data to visualize for {dataset_name}")
        return generated_files
    
    # Sort by provider name for consistent ordering
    df = df.sort_values("Provider")
    
    # Generate plots
    try:
        # Create accuracy comparison plot
        x = range(len(df))
        width = 0.35
        
        # Adjust figure size based on number of systems
        fig_width = min(12, max(8, len(df) * 1.2))
        fig_height = 6
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Character accuracy bars
        char_bars = ax.bar([p - width/2 for p in x], df["character_accuracy"], 
                          width=width, label="Character Accuracy", 
                          align="center", color=df["Color"])
        
        # Word accuracy bars
        word_bars = ax.bar([p + width/2 for p in x], df["word_accuracy"], 
                          width=width, label="Word Accuracy", 
                          align="center", color=df["word_accuracy_Color"])
        
        # Add value labels on bars (only if there's space)
        if len(df) <= 10:  # Only add labels if not too many systems
            for i, (char_acc, word_acc) in enumerate(zip(df["character_accuracy"], df["word_accuracy"])):
                ax.text(i - width/2, char_acc + 0.5, f"{char_acc:.1f}%", 
                       ha='center', va='bottom', fontsize=8, fontweight='bold')
                ax.text(i + width/2, word_acc + 0.5, f"{word_acc:.1f}%", 
                       ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # Customize plot
        ax.set_xticks(x)
        ax.set_xticklabels(df["Label"], rotation=45, ha="right")
        ax.set_ylabel("Accuracy (%)")
        ax.set_title(f"Character and Word Accuracy Comparison - {dataset_name.upper()}")
        ax.set_ylim(0, 105)
        
        # Add grid
        ax.grid(True, alpha=0.3, axis='y')
        
        # Create legend (simplified for better layout)
        category_patches = []
        for category in df["Category"].unique():
            color = CATEGORY_COLORS.get(category, CATEGORY_COLORS["OPEN_OCR"])
            category_patches.append(Patch(color=color, label=f"{category}"))
        
        ax.legend(
            handles=category_patches,
            title="System Categories",
            loc="upper right",
            bbox_to_anchor=(1.0, 1.0)
        )
        
        # Use subplots_adjust instead of tight_layout for better control
        plt.subplots_adjust(bottom=0.15, left=0.1, right=0.9, top=0.9)
        
        # Save plot
        plot_path = plot_output_dir / f"{dataset_name}_accuracy_comparison.png"
        plt.savefig(plot_path, bbox_inches='tight', dpi=100)
        plt.close()
        generated_files.append(str(plot_path))
        
        # Generate summary table
        table_data = df[["Provider", "Category", "character_accuracy", "word_accuracy"]].copy()
        table_data = table_data.round(2)
        
        # Save CSV
        csv_path = table_output_dir / f"{dataset_name}_accuracy.csv"
        table_data.to_csv(csv_path, index=False)
        generated_files.append(str(csv_path))
        
        # Save Markdown
        md_path = table_output_dir / f"{dataset_name}_accuracy.md"
        table_data.to_markdown(md_path, index=False)
        generated_files.append(str(md_path))
        
        print(f"[✓] Generated accuracy visualizations for {dataset_name}")
        print(f"    - Plot: {plot_path}")
        print(f"    - Table: {csv_path}")
        
    except Exception as e:
        print(f"[!] Error generating accuracy visualizations: {e}")
    
    return generated_files
