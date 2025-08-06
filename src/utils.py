# src/utils.py
from datetime import datetime
from functools import wraps
import time
import logging
import pandas as pd
from typing import Callable, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_execution(func: Callable) -> Callable:
    """Decorator to log function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        logger.info(f"Executing {func.__name__}...")
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"Completed {func.__name__} in {elapsed:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def validate_date_range(df: pd.DataFrame, date_col: str, 
                       start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Ensure DataFrame dates are within expected range
    and convert to timezone-naive if needed
    """
    try:
        # Ensure datetime and remove timezone if present
        if pd.api.types.is_datetime64tz_dtype(df[date_col]):
            df[date_col] = df[date_col].dt.tz_localize(None)
        elif not pd.api.types.is_datetime64_dtype(df[date_col]):
            df[date_col] = pd.to_datetime(df[date_col])
        
        # Validate range
        mask = (df[date_col] >= start_date) & (df[date_col] <= end_date)
        if not mask.all():
            filtered_count = len(df) - mask.sum()
            logger.warning(f"Filtering {filtered_count} rows outside date range {start_date} to {end_date}")
        
        return df[mask].copy()
        
    except Exception as e:
        raise ValueError(f"Date validation failed: {str(e)}")