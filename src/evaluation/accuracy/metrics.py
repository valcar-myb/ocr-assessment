"""
OCR accuracy metrics implementation
"""

import re
from typing import List, Tuple


def normalize_text(text: str, remove_punctuation: bool = True) -> str:
    """
    Normalize text for comparison
    
    Args:
        text: Input text to normalize
        remove_punctuation: Whether to remove punctuation
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Convert to lowercase and remove extra whitespace
    text = re.sub(r'\s+', ' ', text.lower().strip())
    
    # Remove punctuation if specified
    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)
    
    return text


def calculate_cer(prediction: str, ground_truth: str, normalize: bool = True) -> float:
    """
    Calculate Character Error Rate (CER) - simplified version
    Note: This is a basic implementation. For accurate CER, use ocreval.
    
    Args:
        prediction: Predicted text
        ground_truth: Ground truth text
        normalize: Whether to normalize texts before comparison
        
    Returns:
        CER value (0.0 = perfect, higher = worse)
    """
    if normalize:
        prediction = normalize_text(prediction, remove_punctuation=False)
        ground_truth = normalize_text(ground_truth, remove_punctuation=False)
    
    if len(ground_truth) == 0:
        return 0.0 if len(prediction) == 0 else 1.0
    
    # Simple character-level comparison
    correct_chars = sum(1 for p, g in zip(prediction, ground_truth) if p == g)
    total_chars = len(ground_truth)
    
    return 1.0 - (correct_chars / total_chars) if total_chars > 0 else 0.0


def calculate_wer(prediction: str, ground_truth: str, normalize: bool = True) -> float:
    """
    Calculate Word Error Rate (WER) - simplified version
    Note: This is a basic implementation. For accurate WER, use ocreval.
    
    Args:
        prediction: Predicted text
        ground_truth: Ground truth text
        normalize: Whether to normalize texts before comparison
        
    Returns:
        WER value (0.0 = perfect, higher = worse)
    """
    if normalize:
        prediction = normalize_text(prediction, remove_punctuation=False)
        ground_truth = normalize_text(ground_truth, remove_punctuation=False)
    
    # Split into words
    pred_words = prediction.split()
    gt_words = ground_truth.split()
    
    if len(gt_words) == 0:
        return 0.0 if len(pred_words) == 0 else 1.0
    
    # Simple word-level comparison
    correct_words = sum(1 for p, g in zip(pred_words, gt_words) if p == g)
    total_words = len(gt_words)
    
    return 1.0 - (correct_words / total_words) if total_words > 0 else 0.0


def calculate_character_accuracy(prediction: str, ground_truth: str, normalize: bool = True) -> float:
    """
    Calculate character-level accuracy
    
    Args:
        prediction: Predicted text
        ground_truth: Ground truth text
        normalize: Whether to normalize texts before comparison
        
    Returns:
        Character accuracy (0.0 to 1.0, 1.0 = perfect)
    """
    if normalize:
        prediction = normalize_text(prediction, remove_punctuation=False)
        ground_truth = normalize_text(ground_truth, remove_punctuation=False)
    
    if len(ground_truth) == 0:
        return 1.0 if len(prediction) == 0 else 0.0
    
    # Calculate matching characters
    correct_chars = sum(1 for p, g in zip(prediction, ground_truth) if p == g)
    
    # Account for length differences
    max_len = max(len(prediction), len(ground_truth))
    
    return correct_chars / max_len if max_len > 0 else 1.0


def calculate_word_accuracy(prediction: str, ground_truth: str, normalize: bool = True) -> float:
    """
    Calculate word-level accuracy
    
    Args:
        prediction: Predicted text
        ground_truth: Ground truth text
        normalize: Whether to normalize texts before comparison
        
    Returns:
        Word accuracy (0.0 to 1.0, 1.0 = perfect)
    """
    if normalize:
        prediction = normalize_text(prediction, remove_punctuation=False)
        ground_truth = normalize_text(ground_truth, remove_punctuation=False)
    
    # Split into words
    pred_words = prediction.split()
    gt_words = ground_truth.split()
    
    if len(gt_words) == 0:
        return 1.0 if len(pred_words) == 0 else 0.0
    
    # Calculate matching words
    correct_words = sum(1 for p, g in zip(pred_words, gt_words) if p == g)
    
    # Account for length differences
    max_len = max(len(pred_words), len(gt_words))
    
    return correct_words / max_len if max_len > 0 else 1.0


# NED and batch metrics removed - using only ocreval

