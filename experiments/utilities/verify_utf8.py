"""
Script to verify that all text files are UTF-8 encoded
"""

import sys
from pathlib import Path
import chardet


def check_file_encoding(file_path: Path) -> tuple:
    """
    Check encoding of a file
    
    Returns:
        tuple: (file_path, encoding, confidence, is_utf8)
    """
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        if not raw_data:
            return (file_path, 'empty', 1.0, True)
        
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']
        
        # Check if it's UTF-8 or ASCII (ASCII is subset of UTF-8)
        is_utf8 = encoding and (encoding.lower() in ['utf-8', 'ascii'])
        
        return (file_path, encoding, confidence, is_utf8)
    except Exception as e:
        return (file_path, f'ERROR: {e}', 0.0, False)


def convert_to_utf8(file_path: Path, original_encoding: str) -> bool:
    """
    Convert a file to UTF-8 encoding
    
    Returns:
        bool: True if conversion successful
    """
    try:
        # Read with original encoding
        with open(file_path, 'r', encoding=original_encoding) as f:
            content = f.read()
        
        # Write as UTF-8
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  Error converting {file_path}: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Verify and convert files to UTF-8')
    parser.add_argument('--directory', default='results/text_outputs',
                       help='Directory to check')
    parser.add_argument('--convert', action='store_true',
                       help='Convert non-UTF-8 files to UTF-8')
    parser.add_argument('--check-ground-truth', action='store_true',
                       help='Also check ground truth files in data/raw')
    
    args = parser.parse_args()
    
    # Collect directories to check
    dirs_to_check = []
    
    if Path(args.directory).exists():
        dirs_to_check.append(Path(args.directory))
    
    if args.check_ground_truth:
        gt_base = Path('data/raw')
        if gt_base.exists():
            for dataset_dir in gt_base.iterdir():
                if dataset_dir.is_dir():
                    gt_dir = dataset_dir / 'gt'
                    if gt_dir.exists():
                        dirs_to_check.append(gt_dir)
    
    # Check all .txt files
    non_utf8_files = []
    total_files = 0
    
    print("Checking file encodings...")
    print("=" * 80)
    
    for directory in dirs_to_check:
        print(f"\nChecking directory: {directory}")
        txt_files = list(directory.rglob("*.txt"))
        
        for file_path in txt_files:
            total_files += 1
            file_path, encoding, confidence, is_utf8 = check_file_encoding(file_path)
            
            if not is_utf8:
                non_utf8_files.append((file_path, encoding, confidence))
                print(f"  ❌ {file_path.relative_to('.')}")
                print(f"     Encoding: {encoding} (confidence: {confidence:.2f})")
            else:
                print(f"  ✓ {file_path.relative_to('.')}: {encoding}")
    
    print("\n" + "=" * 80)
    print(f"Summary: {total_files} files checked")
    print(f"  ✓ UTF-8 files: {total_files - len(non_utf8_files)}")
    print(f"  ❌ Non-UTF-8 files: {len(non_utf8_files)}")
    
    if non_utf8_files:
        print("\n" + "=" * 80)
        print("Non-UTF-8 files found:")
        for file_path, encoding, confidence in non_utf8_files:
            print(f"  - {file_path}: {encoding} (confidence: {confidence:.2f})")
        
        if args.convert:
            print("\n" + "=" * 80)
            print("Converting files to UTF-8...")
            converted = 0
            failed = 0
            
            for file_path, encoding, confidence in non_utf8_files:
                if encoding.startswith('ERROR'):
                    print(f"  ⊘ Skipping {file_path} (error during detection)")
                    failed += 1
                    continue
                
                print(f"  Converting {file_path} from {encoding}...")
                if convert_to_utf8(file_path, encoding):
                    converted += 1
                    print(f"    ✓ Converted successfully")
                else:
                    failed += 1
            
            print("\n" + "=" * 80)
            print(f"Conversion complete:")
            print(f"  ✓ Converted: {converted}")
            print(f"  ❌ Failed: {failed}")
        else:
            print("\nTo convert these files to UTF-8, run:")
            print(f"  python {Path(__file__).name} --directory {args.directory} --convert")
    else:
        print("\n✓ All files are UTF-8 encoded!")
    
    print("=" * 80)
    
    # Exit with error code if non-UTF-8 files found and not converted
    if non_utf8_files and not args.convert:
        sys.exit(1)


if __name__ == '__main__':
    main()

