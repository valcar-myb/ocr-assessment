#!/usr/bin/env python3
"""
Convenience script for running common OCR evaluation experiments.
This script provides easy access to the most commonly used commands.
"""

import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"COMMAND: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n{description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{description} failed with exit code {e.returncode}")
        return False
    except KeyboardInterrupt:
        print(f"\n{description} interrupted by user")
        return False

def main():
    """Main function with available commands"""
    if len(sys.argv) < 2:
        print("OCR Evaluation Experiments - Convenience Script")
        print("\nUsage: python run_experiments.py <command> [options]")
        print("\nAvailable commands:")
        print("  extract     - Run OCR text extraction")
        print("  clean_gt    - Clean ground truth files with character whitelist")
        print("  generate_text - Generate cleaned text files from raw outputs")
        print("  evaluate    - Run accuracy evaluation")
        print("  summary     - Generate benchmark summary")
        print("  all         - Run complete pipeline (extract + clean_gt + generate_text + evaluate + summary)")
        print("  benchmark   - Generate benchmark from existing results")
        print("  help        - Show this help message")
        print("\nExamples:")
        print("  python run_experiments.py all")
        print("  python run_experiments.py evaluate")
        print("  python run_experiments.py benchmark")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    config_file = "config/experiments_active.yaml"
    
    # Override config if specified
    if "--config" in sys.argv:
        config_idx = sys.argv.index("--config")
        if config_idx + 1 < len(sys.argv):
            config_file = sys.argv[config_idx + 1]
    
    pipeline_script = Path(__file__).parent / "experiments" / "core" / "run_pipeline.py"
    benchmark_script = Path(__file__).parent / "experiments" / "aggregation" / "build_benchmark.py"
    
    if not pipeline_script.exists():
        print(f"Error: Pipeline script not found at {pipeline_script}")
        sys.exit(1)
    
    success = True
    
    if command == "extract":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "extract"]
        success = run_command(cmd, "OCR Text Extraction")
        
    elif command == "clean_gt":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "clean_gt"]
        success = run_command(cmd, "Ground Truth Cleaning")
        
    elif command == "generate_text":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "generate_text"]
        success = run_command(cmd, "Text File Generation")
        
    elif command == "evaluate":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "evaluate"]
        success = run_command(cmd, "Accuracy Evaluation")
        
    elif command == "summary":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "summary"]
        success = run_command(cmd, "Benchmark Summary Generation")
        
    elif command == "all":
        cmd = [sys.executable, str(pipeline_script), "--config", config_file, "--step", "all"]
        success = run_command(cmd, "Complete OCR Evaluation Pipeline")
        
    elif command == "benchmark":
        if not benchmark_script.exists():
            print(f"Error: Benchmark script not found at {benchmark_script}")
            sys.exit(1)
        cmd = [sys.executable, str(benchmark_script)]
        success = run_command(cmd, "Benchmark Generation")
        
    elif command == "help":
        print("OCR Evaluation Experiments - Convenience Script")
        print("\nThis script provides easy access to common OCR evaluation tasks.")
        print("All commands use the active configuration by default.")
        print("\nFor more advanced usage, use the individual scripts directly:")
        print("  python experiments/core/run_pipeline.py --help")
        print("  python experiments/aggregation/build_benchmark.py --help")
        sys.exit(0)
        
    else:
        print(f"Error: Unknown command '{command}'")
        print("Use 'python run_experiments.py help' for available commands")
        sys.exit(1)
    
    if success:
        print(f"\n🎉 All operations completed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 Some operations failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
