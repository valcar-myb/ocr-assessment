"""
Script to generate text files from raw OCR outputs
"""

import json
import argparse
import yaml
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from parsing.parsers import OCRParser

def main():
    parser = argparse.ArgumentParser(description='Generate text files from raw OCR outputs')
    parser.add_argument('--config', default='config/experiments.yaml')
    parser.add_argument('--raw-dir', default='results/raw_outputs')
    parser.add_argument('--output-dir', default='results/text_outputs')
    
    args = parser.parse_args()
    
    # Load config
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    
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
                
                # Parse and save
                text = parse_func(data['raw_output'])
                image_name = data['image_filename']
                txt_file = output_dir / f"{Path(image_name).stem}.txt"
                
                with open(txt_file, 'w') as f:
                    f.write(text)
                
                print(f"  Generated: {txt_file}")

if __name__ == "__main__":
    main()
