"""
Script to generate text files from raw OCR outputs
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

def main():
    parser = argparse.ArgumentParser(description='Generate text files from raw OCR outputs')
    parser.add_argument('--config', default='config/experiments.yaml')
    parser.add_argument('--raw-dir', default='results/raw_outputs')
    parser.add_argument('--output-dir', default='results/text_outputs')
    
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
    # Get text cleaning configuration
    text_cleaning_config = config.get('text_cleaning', {})
    cleaning_enabled = text_cleaning_config.get('enabled', False)
    char_whitelist = text_cleaning_config.get('char_whitelist', {})
    
    if cleaning_enabled:
        uppercase = char_whitelist.get('letters', {}).get('uppercase', '')
        lowercase = char_whitelist.get('letters', {}).get('lowercase', '')
        digits = char_whitelist.get('digits', '')
        punctuation = char_whitelist.get('punctuation', '')
        
        print(f"Text cleaning enabled with whitelist: {len(uppercase)} uppercase + {len(lowercase)} lowercase + {len(digits)} digits + {len(punctuation)} punctuation")
    else:
        print("Text cleaning disabled")
    
    # Process each dataset/system
    for dataset in config['datasets']:
        for ocr_config in config['ocr_systems']:
            dataset_name = dataset['name']
            system_name = ocr_config['name']
            
            print(f"Processing {dataset_name}/{system_name}")
            
            # Get parser for this system
            parse_func = OCRParser.get_parser(system_name)
            
            # Find raw files
            raw_dir = Path(args.raw_dir) / dataset_name / system_name
            if not raw_dir.exists():
                continue
                
            raw_files = list(raw_dir.glob("*_raw.json"))
            
            # Create output directory
            output_dir = Path(args.output_dir) / dataset_name / system_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each file
            for raw_file in raw_files:
                with open(raw_file, 'r') as f:
                    data = json.load(f)
                
                # Parse text from raw output
                text = parse_func(data['raw_output'])
                
                # Apply text cleaning if enabled
                if cleaning_enabled and char_whitelist:
                    original_length = len(text)
                    text = clean_text(text, char_whitelist)
                    cleaned_length = len(text)
                    if original_length != cleaned_length:
                        print(f"    Cleaned text: {original_length} -> {cleaned_length} characters")
                
                # Save with UTF-8 encoding (required by ocreval)
                image_path = data['image_path']
                image_name = Path(image_path).name
                txt_file = output_dir / f"{Path(image_name).stem}.txt"
                
                with open(txt_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                print(f"  Generated: {txt_file}")

if __name__ == "__main__":
    main()
