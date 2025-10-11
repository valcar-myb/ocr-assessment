"""
Script to clean ground truth files using the same character whitelist as OCR outputs
This ensures fair comparison during evaluation by applying the same text cleaning to both
ground truth and OCR outputs.
"""

import json
import argparse
import yaml
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from parsing.parsers import OCRParser


def clean_text(text: str, char_whitelist: dict) -> str:
    """
    Clean text by keeping only allowed characters
    
    Args:
        text: Input text to clean
        char_whitelist: Dictionary with allowed character sets
        
    Returns:
        Cleaned text with only allowed characters
    """
    # Build allowed characters set
    allowed_chars = set()
    
    # Add letters (handle both string and list formats)
    uppercase = char_whitelist["letters"]["uppercase"]
    lowercase = char_whitelist["letters"]["lowercase"]
    
    if isinstance(uppercase, str):
        allowed_chars.update(uppercase)
    else:
        allowed_chars.update(uppercase)
        
    if isinstance(lowercase, str):
        allowed_chars.update(lowercase)
    else:
        allowed_chars.update(lowercase)
    
    # Add digits
    digits = char_whitelist["digits"]
    if isinstance(digits, str):
        allowed_chars.update(digits)
    else:
        allowed_chars.update(digits)
    
    # Add whitespace
    whitespace = char_whitelist["whitespace"]
    if isinstance(whitespace, str):
        allowed_chars.update(whitespace)
    else:
        allowed_chars.update(whitespace)
    
    # Add punctuation
    punctuation = char_whitelist["punctuation"]
    if isinstance(punctuation, str):
        allowed_chars.update(punctuation)
    else:
        allowed_chars.update(punctuation)
    
    # Filter text to keep only allowed characters
    cleaned_text = ''.join(char for char in text if char in allowed_chars)
    
    return cleaned_text


def clean_ground_truth_files(dataset_path: Path, char_whitelist: dict, backup: bool = True):
    """
    Clean all ground truth files in a dataset directory
    
    Args:
        dataset_path: Path to dataset directory (e.g., data/raw/sroie)
        char_whitelist: Character whitelist configuration
        backup: Whether to create backup of original files
    """
    gt_dir = dataset_path / 'gt'
    if not gt_dir.exists():
        print(f"Warning: Ground truth directory not found: {gt_dir}")
        return
    
    # Create backup directory if requested
    if backup:
        backup_dir = dataset_path / 'gt_backup'
        backup_dir.mkdir(exist_ok=True)
        print(f"Backup directory: {backup_dir}")
    
    # Process all .txt files in gt directory
    gt_files = list(gt_dir.glob("*.txt"))
    
    if not gt_files:
        print(f"No ground truth files found in {gt_dir}")
        return
    
    print(f"Processing {len(gt_files)} ground truth files...")
    
    total_original_chars = 0
    total_cleaned_chars = 0
    files_modified = 0
    
    for gt_file in gt_files:
        try:
            # Read original file
            with open(gt_file, 'r', encoding='utf-8') as f:
                original_text = f.read()
            
            original_length = len(original_text)
            total_original_chars += original_length
            
            # Clean the text
            cleaned_text = clean_text(original_text, char_whitelist)
            cleaned_length = len(cleaned_text)
            total_cleaned_chars += cleaned_length
            
            # Create backup if requested
            if backup and original_length != cleaned_length:
                backup_file = backup_dir / gt_file.name
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_text)
            
            # Write cleaned text back to original file
            with open(gt_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            if original_length != cleaned_length:
                files_modified += 1
                
        except Exception as e:
            print(f"  ✗ Error processing {gt_file.name}: {e}")
    
    # Summary
    print(f"Cleaned: {files_modified}/{len(gt_files)} files, {total_original_chars - total_cleaned_chars} chars removed")


def main():
    parser = argparse.ArgumentParser(description='Clean ground truth files using character whitelist')
    parser.add_argument('--config', default='config/experiments_active.yaml',
                       help='Path to configuration file')
    parser.add_argument('--dataset', default='sroie',
                       help='Dataset name to clean (e.g., sroie, iam)')
    parser.add_argument('--data-dir', default='data/raw',
                       help='Base directory containing datasets')
    parser.add_argument('--no-backup', action='store_true',
                       help='Do not create backup of original files')
    
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Get text cleaning configuration
    text_cleaning_config = config.get('text_cleaning', {})
    cleaning_enabled = text_cleaning_config.get('enabled', False)
    char_whitelist = text_cleaning_config.get('char_whitelist', {})
    
    if not cleaning_enabled:
        print("Text cleaning is disabled in configuration. Exiting.")
        sys.exit(1)
    
    if not char_whitelist:
        print("No character whitelist found in configuration. Exiting.")
        sys.exit(1)
    
    # Process dataset
    dataset_path = Path(args.data_dir) / args.dataset
    
    if not dataset_path.exists():
        print(f"Error: Dataset directory not found: {dataset_path}")
        sys.exit(1)
    
    print(f"Cleaning ground truth for dataset: {args.dataset}")
    
    # Clean ground truth files
    clean_ground_truth_files(dataset_path, char_whitelist, backup=not args.no_backup)


if __name__ == "__main__":
    main()
