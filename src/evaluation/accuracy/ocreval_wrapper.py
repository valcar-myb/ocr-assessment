"""
Wrapper for ocreval command-line tools
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, Optional


class OCREvalWrapper:
    """
    Wrapper for ocreval accuracy and accsum commands
    """
    
    def __init__(self, accuracy_cmd: str = "accuracy",
                 wordacc_cmd: str = "wordacc",
                 accsum_cmd: str = "accsum",
                 wordaccsum_cmd: str = "wordaccsum"):
        """
        Initialize the wrapper
        
        Args:
            accuracy_cmd: Path to accuracy command (default: "accuracy")
            wordacc_cmd: Path to wordacc command (default: "wordacc")
            accsum_cmd: Path to accsum command (default: "accsum")
            wordaccsum_cmd: Path to wordaccsum command (default: "wordaccsum")
        """
        self.accuracy_cmd = accuracy_cmd
        self.wordacc_cmd = wordacc_cmd
        self.accsum_cmd = accsum_cmd
        self.wordaccsum_cmd = wordaccsum_cmd
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """
        Check if ocreval commands are installed and available
        
        Returns:
            True if available, raises RuntimeError otherwise
        """
        # Check accuracy command
        try:
            subprocess.run(
                [self.accuracy_cmd, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                f"ocreval '{self.accuracy_cmd}' command not found. "
                f"Please install ocreval. See setup/ocreval/README.md for instructions."
            ) from e
        
        # Check wordacc command
        try:
            subprocess.run(
                [self.wordacc_cmd, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                f"ocreval '{self.wordacc_cmd}' command not found. "
                f"Please install ocreval. See setup/ocreval/README.md for instructions."
            ) from e
        
        # Check accsum command
        try:
            subprocess.run(
                [self.accsum_cmd, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                f"ocreval '{self.accsum_cmd}' command not found. "
                f"Please install ocreval. See setup/ocreval/README.md for instructions."
            ) from e
        
        # Check wordaccsum command
        try:
            subprocess.run(
                [self.wordaccsum_cmd, "-h"],
                capture_output=True,
                text=True,
                timeout=5
            )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
            raise RuntimeError(
                f"ocreval '{self.wordaccsum_cmd}' command not found. "
                f"Please install ocreval. See setup/ocreval/README.md for instructions."
            ) from e
        
        return True
    
    def run_accuracy(self, gt_path: Path, pred_path: Path, 
                    output_path: Path) -> bool:
        """
        Run accuracy command and save report to file (character accuracy)
        
        Args:
            gt_path: Path to ground truth file
            pred_path: Path to prediction file
            output_path: Path to save partial report (required)
            
        Returns:
            True if successful, False otherwise
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Run accuracy command
            command = [self.accuracy_cmd, str(gt_path), str(pred_path), str(output_path)]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"[✗] accuracy failed: {result.stderr}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            print(f"[✗] accuracy command timed out for {output_path}")
            return False
        except Exception as e:
            print(f"[✗] Error running accuracy: {e}")
            return False
    
    def run_wordacc(self, gt_path: Path, pred_path: Path, 
                    output_path: Path) -> bool:
        """
        Run wordacc command and save report to file (word accuracy)
        
        Args:
            gt_path: Path to ground truth file
            pred_path: Path to prediction file
            output_path: Path to save partial word accuracy report (required)
            
        Returns:
            True if successful, False otherwise
        """
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Run wordacc command
            command = [self.wordacc_cmd, str(gt_path), str(pred_path), str(output_path)]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"[✗] wordacc failed: {result.stderr}")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            print(f"[✗] wordacc command timed out for {output_path}")
            return False
        except Exception as e:
            print(f"[✗] Error running wordacc: {e}")
            return False
    
    def _parse_accuracy_output(self, output_path: Path) -> Dict[str, float]:
        """
        Parse accuracy command output file
        
        Args:
            output_path: Path to accuracy output file
            
        Returns:
            Dictionary with parsed metrics
        """
        if not output_path.exists():
            return {}
        
        metrics = {}
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse ocreval character accuracy format
        # Format: "  228159   Characters\n   12365   Errors\n   94.58%  Accuracy"
        char_match = re.search(r'(\d+)\s+Characters\s+(\d+)\s+Errors\s+([\d.]+)%\s+Accuracy', content, re.MULTILINE)
        if char_match:
            total_chars = int(char_match.group(1))
            char_errors = int(char_match.group(2))
            char_accuracy = float(char_match.group(3))
            metrics['char_accuracy'] = char_accuracy / 100.0  # Convert to 0-1 range
            metrics['char_errors'] = char_errors
            metrics['total_chars'] = total_chars
            metrics['cer'] = char_errors / total_chars if total_chars > 0 else 0.0
        
        # Parse ocreval word accuracy format (from wordaccsum)
        # Format: "   41370   Words\n    1552   Misrecognized\n   96.25%  Accuracy"
        word_match = re.search(r'(\d+)\s+Words\s+(\d+)\s+Misrecognized\s+([\d.]+)%\s+Accuracy', content, re.MULTILINE)
        if word_match:
            total_words = int(word_match.group(1))
            word_errors = int(word_match.group(2))
            word_accuracy = float(word_match.group(3))
            metrics['word_accuracy'] = word_accuracy / 100.0  # Convert to 0-1 range
            metrics['word_errors'] = word_errors
            metrics['total_words'] = total_words
            metrics['wer'] = word_errors / total_words if total_words > 0 else 0.0
        
        return metrics
    
    def generate_partial_reports(self, gt_files: Dict[str, Path], pred_files: Dict[str, Path],
                                output_dir: Path) -> list:
        """
        Generate partial character accuracy reports for each file pair
        
        Args:
            gt_files: Dictionary mapping file IDs to ground truth paths
            pred_files: Dictionary mapping file IDs to prediction paths
            output_dir: Directory to save partial reports
            
        Returns:
            List of generated report file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_reports = []
        
        # Find matching files
        matched_keys = set(gt_files.keys()) & set(pred_files.keys())
        missing_gt = set(pred_files.keys()) - matched_keys
        missing_pred = set(gt_files.keys()) - matched_keys
        
        # Report missing files
        for key in missing_gt:
            print(f"[!] Ground truth missing for: {key}")
        for key in missing_pred:
            print(f"[!] Prediction missing for: {key}")
        
        # Generate reports for matched files
        for key in matched_keys:
            gt_path = gt_files[key]
            pred_path = pred_files[key]
            output_path = output_dir / f"{key}.txt"
            
            if self.run_accuracy(gt_path, pred_path, output_path):
                generated_reports.append(output_path)
                print(f"[✓] Report generated: {output_path.name}")
            else:
                print(f"[✗] Failed: {key}")
        
        return generated_reports
    
    def generate_word_partial_reports(self, gt_files: Dict[str, Path], pred_files: Dict[str, Path],
                                      output_dir: Path) -> list:
        """
        Generate partial word accuracy reports for each file pair using wordacc
        
        Args:
            gt_files: Dictionary mapping file IDs to ground truth paths
            pred_files: Dictionary mapping file IDs to prediction paths
            output_dir: Directory to save partial word accuracy reports
            
        Returns:
            List of generated report file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_reports = []
        
        # Find matching files
        matched_keys = set(gt_files.keys()) & set(pred_files.keys())
        missing_gt = set(pred_files.keys()) - matched_keys
        missing_pred = set(gt_files.keys()) - matched_keys
        
        # Report missing files
        for key in missing_gt:
            print(f"[!] Ground truth missing for: {key}")
        for key in missing_pred:
            print(f"[!] Prediction missing for: {key}")
        
        # Generate word accuracy reports for matched files
        for key in matched_keys:
            gt_path = gt_files[key]
            pred_path = pred_files[key]
            output_path = output_dir / f"{key}.txt"
            
            if self.run_wordacc(gt_path, pred_path, output_path):
                generated_reports.append(output_path)
                print(f"[✓] Word report generated: {output_path.name}")
            else:
                print(f"[✗] Failed: {key}")
        
        return generated_reports
    
    def run_accsum(self, partial_reports: list, output_path: Path) -> bool:
        """
        Run accsum to aggregate partial reports
        
        Args:
            partial_reports: List of paths to partial report files
            output_path: Path to save aggregated report
            
        Returns:
            True if successful, False otherwise
        """
        if not partial_reports:
            print("[!] No partial reports to aggregate")
            return False
        
        # accsum requires at least 2 files
        if len(partial_reports) < 2:
            print(f"[!] accsum requires at least 2 files, got {len(partial_reports)}. Copying single file.")
            # Copy the single file as the aggregate
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(partial_reports[0], 'r', encoding='utf-8') as src:
                    content = src.read()
                with open(output_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                print(f"[✓] Single file copied as aggregate: {output_path}")
                return True
            except Exception as e:
                print(f"[✗] Error copying single file: {e}")
                return False
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Run accsum command
            command = [self.accsum_cmd] + [str(p) for p in partial_reports]
            
            with open(output_path, 'w', encoding='utf-8') as out_file:
                result = subprocess.run(
                    command,
                    stdout=out_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30
                )
            
            if result.returncode != 0:
                print(f"[✗] accsum failed: {result.stderr}")
                return False
            
            print(f"[✓] Aggregated report created: {output_path}")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"[✗] accsum command timed out")
            return False
        except Exception as e:
            print(f"[✗] Error running accsum: {e}")
            return False
    
    def run_wordaccsum(self, partial_reports: list, output_path: Path) -> bool:
        """
        Run wordaccsum to aggregate partial reports for word accuracy
        
        Args:
            partial_reports: List of paths to partial report files
            output_path: Path to save aggregated word accuracy report
            
        Returns:
            True if successful, False otherwise
        """
        if not partial_reports:
            print("[!] No partial reports to aggregate")
            return False
        
        # wordaccsum requires at least 2 files
        if len(partial_reports) < 2:
            print(f"[!] wordaccsum requires at least 2 files, got {len(partial_reports)}. Copying single file.")
            # Copy the single file as the aggregate
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(partial_reports[0], 'r', encoding='utf-8') as src:
                    content = src.read()
                with open(output_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                print(f"[✓] Single file copied as word aggregate: {output_path}")
                return True
            except Exception as e:
                print(f"[✗] Error copying single file: {e}")
                return False
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            # Run wordaccsum command
            command = [self.wordaccsum_cmd] + [str(p) for p in partial_reports]
            
            with open(output_path, 'w', encoding='utf-8') as out_file:
                result = subprocess.run(
                    command,
                    stdout=out_file,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=30
                )
            
            if result.returncode != 0:
                print(f"[✗] wordaccsum failed: {result.stderr}")
                return False
            
            print(f"[✓] Word accuracy aggregated report created: {output_path}")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"[✗] wordaccsum command timed out")
            return False
        except Exception as e:
            print(f"[✗] Error running wordaccsum: {e}")
            return False
    
    def parse_aggregate_report(self, report_path: Path) -> Dict[str, float]:
        """
        Parse aggregated report from accsum
        
        Args:
            report_path: Path to aggregate report file
            
        Returns:
            Dictionary with parsed metrics
        """
        return self._parse_accuracy_output(report_path)

