from app.utils.data_loader import load_event_data
from datetime import timedelta
import pandas as pd

def match_change_to_event(change_date_str, window=10):
    events_df = load_event_data()
    change_date = pd.to_datetime(change_date_str)

    for _, row in events_df.iterrows():
        event_date = row['Date']
        if abs((event_date - change_date).days) <= window:
            return {
                "matched_event": row['Event'],
                "event_date": str(row['Date'].date()),
                "description": row['Description']
            }
    
    return {
        "matched_event": None,
        "event_date": None,
        "description": "No event found within window"
    }
