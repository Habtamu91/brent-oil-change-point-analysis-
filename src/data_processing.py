import pandas as pd
import numpy as np
from pathlib import Path
from src.config import *
from src.utils import validate_date_range, log_execution
import warnings
from typing import Tuple
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self._ensure_directories_exist()

    def _ensure_directories_exist(self):
        """Create required directories if they don't exist"""
        try:
            PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directories: {str(e)}")
            raise

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
    def load_raw_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load and validate raw data files"""
        try:
            logger.info("Loading Brent data...")
            brent = pd.read_csv(
                BRENT_RAW_PATH,
                parse_dates=['Date'],
                dayfirst=True
            )
            self._validate_brent_data(brent)

            logger.info("Loading Events data...")
            events = pd.read_csv(
                EVENTS_RAW_PATH,
                parse_dates=['Event_date'],
                infer_datetime_format=True
            )
            self._validate_events_data(events)

            return brent, events

        except Exception as e:
            logger.error(f"Data loading failed: {str(e)}")
            raise

    @log_execution
    def process_brent_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process Brent oil price data"""
        try:
            df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
            
            if len(df) == 0:
                raise ValueError("Empty DataFrame after date conversion")
                
            df = (
                df
                .sort_values('Date')
                .drop_duplicates('Date')
                .set_index('Date')
                .asfreq('D')
                .interpolate(method='time')
                .reset_index()
            )
            
            df['log_return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))
            df['pct_change'] = df['Price'].pct_change() * 100

            df = validate_date_range(df, 'Date', DEFAULT_START_DATE, DEFAULT_END_DATE)
            return df.dropna()

        except Exception as e:
            logger.error(f"Brent data processing failed: {str(e)}")
            raise

    @log_execution
    def process_events_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process events data"""
        try:
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
            logger.error(f"Events data processing failed: {str(e)}")
            raise

    @log_execution
    def save_processed_data(self, brent_df: pd.DataFrame, events_df: pd.DataFrame):
        """Save processed data to CSV"""
        try:
            logger.info(f"Saving Brent data to: {BRENT_PROCESSED_PATH}")
            logger.info(f"Saving Events data to: {EVENTS_PROCESSED_PATH}")

            brent_df.to_csv(BRENT_PROCESSED_PATH, index=False)
            events_df.to_csv(EVENTS_PROCESSED_PATH, index=False)

            logger.info("Data saved successfully")

        except Exception as e:
            logger.error(f"Failed to save processed data: {str(e)}")
            raise

    def run_pipeline(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Run the full processing pipeline"""
        try:
            logger.info("Starting data processing pipeline...")
            brent_raw, events_raw = self.load_raw_data()
            brent_processed = self.process_brent_data(brent_raw)
            events_processed = self.process_events_data(events_raw)
            self.save_processed_data(brent_processed, events_processed)
            logger.info("Pipeline completed successfully")
            return brent_processed, events_processed
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        processor = DataProcessor()
        brent_df, events_df = processor.run_pipeline()
        logger.info("🎉 Pipeline completed. Check the data/processed folder for CSV files.")
    except Exception as e:
        logger.error(f"❌ Pipeline execution failed: {str(e)}")