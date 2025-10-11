"""
Evaluation module for OCR systems
Contains accuracy, time, and cost evaluation components
"""

from .accuracy import AccuracyEvaluator
from .time import TimeEvaluator

__all__ = ['AccuracyEvaluator', 'TimeEvaluator']
