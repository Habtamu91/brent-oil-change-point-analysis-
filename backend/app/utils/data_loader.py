import pandas as pd
import numpy as np

def load_data():
    # Load and preprocess data
    prices = pd.read_csv('data/BrentOilPrices.csv', parse_dates=['Date'])
    prices = prices.sort_values('Date')
    
    # Calculate log returns
    prices['log_return'] = np.log(prices['Price']) - np.log(prices['Price'].shift(1))
    prices = prices.dropna()
    
    return prices