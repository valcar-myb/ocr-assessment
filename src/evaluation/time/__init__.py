"""
Time evaluation module for OCR systems
Analyzes processing time from raw outputs
"""

from .metrics import (
    calculate_time_statistics,
    filter_outliers
)
from .evaluator import TimeEvaluator
from .visualization import generate_timing_visualizations

__all__ = [
    'calculate_time_statistics',
    'filter_outliers',
    'TimeEvaluator',
    'generate_timing_visualizations'
]