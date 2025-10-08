"""
OCR evaluation metrics implementation
"""

import re
from difflib import SequenceMatcher

def calculate_character_accuracy(predictions, ground_truth):
    """Calculate character-level accuracy"""
    total_chars = 0
    correct_chars = 0
    
    for pred, gt in zip(predictions, ground_truth):
        # Normalize text
        pred_norm = normalize_text(pred)
        gt_norm = normalize_text(gt)
        
        total_chars += len(gt_norm)
        correct_chars += sum(1 for p, g in zip(pred_norm, gt_norm) if p == g)
    
    return correct_chars / total_chars if total_chars > 0 else 0.0

def calculate_word_accuracy(predictions, ground_truth):
    """Calculate word-level accuracy"""
    total_words = 0
    correct_words = 0
    
    for pred, gt in zip(predictions, ground_truth):
        # Split into words
        pred_words = normalize_text(pred).split()
        gt_words = normalize_text(gt).split()
        
        total_words += len(gt_words)
        correct_words += sum(1 for p, g in zip(pred_words, gt_words) if p == g)
    
    return correct_words / total_words if total_words > 0 else 0.0

def calculate_cer(predictions, ground_truth):
    """Calculate Character Error Rate"""
    total_chars = 0
    total_errors = 0
    
    for pred, gt in zip(predictions, ground_truth):
        pred_norm = normalize_text(pred)
        gt_norm = normalize_text(gt)
        
        total_chars += len(gt_norm)
        
        # Calculate edit distance
        matcher = SequenceMatcher(None, gt_norm, pred_norm)
        total_errors += len(gt_norm) - matcher.matching_blocks[0].size if matcher.matching_blocks else len(gt_norm)
    
    return total_errors / total_chars if total_chars > 0 else 0.0

def calculate_wer(predictions, ground_truth):
    """Calculate Word Error Rate"""
    total_words = 0
    total_errors = 0
    
    for pred, gt in zip(predictions, ground_truth):
        pred_words = normalize_text(pred).split()
        gt_words = normalize_text(gt).split()
        
        total_words += len(gt_words)
        
        # Calculate edit distance for words
        matcher = SequenceMatcher(None, gt_words, pred_words)
        total_errors += len(gt_words) - matcher.matching_blocks[0].size if matcher.matching_blocks else len(gt_words)
    
    return total_errors / total_words if total_words > 0 else 0.0

def normalize_text(text):
    """Normalize text for comparison"""
    if not text:
        return ""
    
    # Convert to lowercase and remove extra whitespace
    text = re.sub(r'\s+', ' ', text.lower().strip())
    
    # Remove punctuation for some metrics
    text = re.sub(r'[^\w\s]', '', text)
    
    return text
