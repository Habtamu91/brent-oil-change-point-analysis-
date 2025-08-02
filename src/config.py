from pathlib import Path
from datetime import datetime
import pytz

# Project paths
PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Data files
BRENT_RAW_PATH = RAW_DATA_DIR / "BrentOilPrices.csv"
EVENTS_RAW_PATH = RAW_DATA_DIR / "events.csv"
BRENT_PROCESSED_PATH = PROCESSED_DATA_DIR / "brent_processed.parquet"
EVENTS_PROCESSED_PATH = PROCESSED_DATA_DIR / "events_processed.parquet"

# Date ranges (all timezone-naive)
DEFAULT_START_DATE = datetime(1987, 5, 20)  # No timezone
DEFAULT_END_DATE = datetime(2022, 9, 30)    # No timezone

# Model configuration
MODEL_CONFIG = {
    "n_changepoints": 5,
    "n_samples": 2000,
    "tune": 1000,
    "target_accept": 0.95,
    "random_seed": 42
}

# Event matching
EVENT_MATCH_WINDOW_DAYS = 30
MIN_EVENT_IMPACT = "Medium"  # Only match events with this impact level or higher