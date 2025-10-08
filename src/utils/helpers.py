"""
Utility functions
"""

import os
from pathlib import Path

def ensure_dir(path):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

def get_file_list(directory, extensions=None):
    """Get list of files from directory"""
    if extensions is None:
        extensions = ['.jpg', '.png', '.tiff']
    
    files = []
    for ext in extensions:
        files.extend(Path(directory).glob(f'*{ext}'))
    
    return files
