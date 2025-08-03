# run_processing.py
from src.data_processing import DataProcessor

if __name__ == "__main__":
    processor = DataProcessor()
    brent, events = processor.run_pipeline()
    print(f"Processed {len(brent)} price records")
    print(f"Processed {len(events)} events")