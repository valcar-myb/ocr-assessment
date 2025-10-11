"""
Accuracy evaluation module for OCR systems
Integrates ocreval for industry-standard metrics
"""

from .metrics import (
    calculate_cer,
    calculate_wer,
    calculate_character_accuracy,
    calculate_word_accuracy
)
from .evaluator import AccuracyEvaluator
from .ocreval_wrapper import OCREvalWrapper
from .visualization import generate_accuracy_visualizations

__all__ = [
    'calculate_cer',
    'calculate_wer',
    'calculate_character_accuracy',
    'calculate_word_accuracy',
    'AccuracyEvaluator',
    'OCREvalWrapper',
    'generate_accuracy_visualizations'
]

