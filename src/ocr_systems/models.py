"""
Base OCR system interface and factory
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import time
from datetime import datetime
from pathlib import Path

class OCRSystem(ABC):
    """Base class for OCR systems"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.output_dir = Path("results/raw_outputs")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    @abstractmethod
    def extract_text(self, image_path: str) -> str:
        """Extract text from image"""
        pass
    
    @abstractmethod
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw OCR output from image"""
        pass
    
    @abstractmethod
    def parse_raw_output(self, raw_data: Dict[str, Any]) -> str:
        """Parse raw OCR output and return extracted text"""
        pass
    
    def batch_extract(self, image_paths: List[str]) -> List[str]:
        """Extract text from multiple images"""
        results = []
        for image_path in image_paths:
            text = self.extract_text(image_path)
            results.append(text)
        return results
    
    def batch_extract_and_save(self, image_paths: List[str], dataset_name: str) -> str:
        """Extract text from multiple images and save raw outputs individually"""
        # Create dataset/system directory structure
        dataset_system_dir = self.output_dir / dataset_name / self.name
        dataset_system_dir.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        
        for image_path in image_paths:
            try:
                # Measure processing time if enabled in config
                measure_time = self.config.get('measure_time', False)
                
                start_time = time.time()
                raw_output = self.extract_raw_output(image_path)
                end_time = time.time()
                
                processing_time = end_time - start_time if measure_time else None
                timestamp = datetime.now().isoformat()
                
                # Create filename from image path
                image_file = Path(image_path)
                output_filename = image_file.stem + "_raw.json"
                output_file = dataset_system_dir / output_filename
                
                # Save individual file with timing info
                file_data = {
                    'image_path': str(image_path),
                    'image_filename': image_file.name,
                    'raw_output': raw_output,
                    'timestamp': timestamp
                }
                
                if measure_time:
                    file_data['processing_time_seconds'] = processing_time
                
                with open(output_file, 'w') as f:
                    json.dump(file_data, f, indent=2)
                
                saved_files.append(str(output_file))
                
            except Exception as e:
                # Save error file
                image_file = Path(image_path)
                output_filename = image_file.stem + "_raw.json"
                output_file = dataset_system_dir / output_filename
                
                error_data = {
                    'image_path': str(image_path),
                    'image_filename': image_file.name,
                    'raw_output': None,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(output_file, 'w') as f:
                    json.dump(error_data, f, indent=2)
                
                saved_files.append(str(output_file))
        
        # Create summary file
        summary_file = dataset_system_dir / "summary.json"
        summary_data = {
            'dataset': dataset_name,
            'system': self.name,
            'total_images': len(image_paths),
            'processed_files': saved_files,
            'output_directory': str(dataset_system_dir)
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2)
        
        return str(dataset_system_dir)
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "name": self.name,
            "config": self.config
        }

class OCRSystemFactory:
    """Factory for creating OCR systems"""
    
    _systems = {}
    
    @classmethod
    def register_system(cls, name: str, system_class):
        """Register a new OCR system"""
        cls._systems[name] = system_class
    
    @classmethod
    def create_system(cls, name: str, config: Dict[str, Any]) -> OCRSystem:
        """Create OCR system instance"""
        if name not in cls._systems:
            raise ValueError(f"Unknown OCR system: {name}")
        
        return cls._systems[name](name, config)
    
    @classmethod
    def get_available_systems(cls) -> List[str]:
        """Get list of available systems"""
        return list(cls._systems.keys())
