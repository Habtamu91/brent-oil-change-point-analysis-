# src/data_processing.py
import pandas as pd
import numpy as np
from pathlib import Path
from src.config import *
from src.utils import validate_date_range, log_execution
import warnings
from typing import Tuple

warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        self._ensure_directories_exist()
        
    def _ensure_directories_exist(self):
        """Create required directories if they don't exist"""
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    @log_execution
    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load and validate raw data files with US date format (MM/DD/YYYY)"""
        try:
            # Load Brent data (dayfirst=True for DD/MM/YYYY format)
            brent = pd.read_csv(
                BRENT_RAW_PATH,
                parse_dates=['Date'],
                dayfirst=True
            )
            self._validate_brent_data(brent)
            
            # Load Events data with explicit US date format (MM/DD/YYYY)
            events = pd.read_csv(
                EVENTS_RAW_PATH,
                parse_dates=['Event_date'],
                infer_datetime_format=True
            )
            self._validate_events_data(events)
            
            return brent, events
            
        except Exception as e:
            raise ValueError(f"Data loading failed: {str(e)}")
    
    def _validate_brent_data(self, df: pd.DataFrame):
        """Validate Brent oil price data"""
        required_cols = {'Date', 'Price'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Brent data must contain columns: {required_cols}")
        
        if df['Date'].isnull().any():
            raise ValueError("Brent data contains null dates")
            
        if df['Price'].isnull().any():
            raise ValueError("Brent data contains null prices")
            
        if (df['Price'] <= 0).any():
            raise ValueError("Brent data contains non-positive prices")
    
    def _validate_events_data(self, df: pd.DataFrame):
        """Validate events data"""
        required_cols = {'Event_name', 'Event_date', 'Description', 'Expected_Impact'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Events data must contain columns: {required_cols}")
        
        if df['Event_date'].isnull().any():
            invalid_dates = df[df['Event_date'].isnull()]['Event_date'].tolist()
            raise ValueError(f"Invalid date formats found: {invalid_dates[:3]}...")
            
        if df['Event_name'].isnull().any():
            raise ValueError("Events data contains null names")
    
    @log_execution
    def process_brent_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process Brent oil price data"""
        try:
            # Convert to datetime and ensure tz-naive
            df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
            
            # Clean and transform
            df = (
                df
                .sort_values('Date')
                .drop_duplicates('Date')
                .set_index('Date')
                .asfreq('D')
                .interpolate(method='time')
                .reset_index()
            )
            
            # Calculate returns
            df['log_return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
            df['pct_change'] = df['Price'].pct_change() * 100
            
            # Filter date range
            df = validate_date_range(df, 'Date', DEFAULT_START_DATE, DEFAULT_END_DATE)
            
            return df.dropna()
            
        except Exception as e:
            raise ValueError(f"Brent data processing failed: {str(e)}")
    
    @log_execution
    def process_events_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process events data with US date format (MM/DD/YYYY)"""
        try:
            # Ensure tz-naive and validate
            df['Event_date'] = pd.to_datetime(df['Event_date']).dt.tz_localize(None)
            df = (
                df
                .sort_values('Event_date')
                .drop_duplicates('Event_name')
                .pipe(validate_date_range, 'Event_date', DEFAULT_START_DATE, DEFAULT_END_DATE)
                .reset_index(drop=True)
            )
            
            return df
            
        except Exception as e:
            raise ValueError(f"Events data processing failed: {str(e)}")
    
    @log_execution
    def save_processed_data(self, brent_df: pd.DataFrame, events_df: pd.DataFrame):
        """Save processed data"""
        try:
            brent_df.to_parquet(BRENT_PROCESSED_PATH)
            events_df.to_parquet(EVENTS_PROCESSED_PATH)
        except Exception as e:
            raise ValueError(f"Failed to save processed data: {str(e)}")
        
    def run_pipeline(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Execute full data processing pipeline"""
        brent_raw, events_raw = self.load_raw_data()
        brent_processed = self.process_brent_data(brent_raw)
        events_processed = self.process_events_data(events_raw)
        self.save_processed_data(brent_processed, events_processed)
        
        return brent_processed, events_processed