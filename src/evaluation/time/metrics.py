"""
Time evaluation metrics implementation
"""

import statistics
from typing import List, Dict, Any
import numpy as np


def filter_outliers(times: List[float], iqr_factor: float = 1.5) -> List[float]:
    """
    Filter outliers from timing data using IQR method
    
    Args:
        times: List of timing values
        iqr_factor: IQR factor for outlier detection (default 1.5)
        
    Returns:
        Filtered list of timing values
    """
    if len(times) < 4:
        # Not enough data for outlier filtering
        return times
    
    q1 = np.percentile(times, 25)
    q3 = np.percentile(times, 75)
    iqr = q3 - q1
    lower_bound = q1 - iqr_factor * iqr
    upper_bound = q3 + iqr_factor * iqr
    
    filtered_times = [t for t in times if lower_bound <= t <= upper_bound]
    
    # If filtering removes too many values, return original
    if len(filtered_times) < len(times) * 0.5:
        return times
    
    return filtered_times


def calculate_time_statistics(times: List[float], filter_outliers_flag: bool = True) -> Dict[str, Any]:
    """
    Calculate comprehensive timing statistics
    
    Args:
        times: List of timing values in seconds
        filter_outliers_flag: Whether to filter outliers
        
    Returns:
        Dictionary with timing statistics
    """
    if not times:
        return {
            'mean': 0.0,
            'median': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std': 0.0,
            'count': 0,
            'filtered_count': 0
        }
    
    # Filter outliers if requested and enough data
    filtered_times = times
    if filter_outliers_flag and len(times) >= 4:
        filtered_times = filter_outliers(times)
    
    if not filtered_times:
        return {
            'mean': 0.0,
            'median': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std': 0.0,
            'count': len(times),
            'filtered_count': 0
        }
    
    return {
        'mean': round(statistics.mean(filtered_times), 4),
        'median': round(statistics.median(filtered_times), 4),
        'min': round(min(filtered_times), 4),
        'max': round(max(filtered_times), 4),
        'std': round(statistics.stdev(filtered_times) if len(filtered_times) > 1 else 0.0, 4),
        'count': len(times),
        'filtered_count': len(filtered_times)
    }


