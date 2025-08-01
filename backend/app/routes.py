from flask import jsonify, request
from app import app
import pandas as pd
import numpy as np
import pymc3 as pm
import json
from datetime import datetime
from .utils.data_loader import load_data
from .models.change_point import detect_change_points

@app.route('/api/prices', methods=['GET'])
def get_prices():
    prices = load_data()
    return jsonify(prices.to_dict(orient='records'))

@app.route('/api/events', methods=['GET'])
def get_events():
    events = pd.read_csv('data/events.csv', parse_dates=['Date'])
    return jsonify(events.to_dict(orient='records'))

@app.route('/api/change_points', methods=['GET'])
def get_change_points():
    prices = load_data()
    results = detect_change_points(prices)
    return jsonify(results)

@app.route('/api/analyze', methods=['POST'])
def analyze_period():
    data = request.json
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    
    prices = load_data()
    period_data = prices[(prices['Date'] >= start_date) & (prices['Date'] <= end_date)]
    
    if len(period_data) == 0:
        return jsonify({"error": "No data for selected period"}), 400
    
    # Basic statistics
    stats = {
        'start_price': float(period_data['Price'].iloc[0]),
        'end_price': float(period_data['Price'].iloc[-1]),
        'price_change': float(period_data['Price'].iloc[-1] - period_data['Price'].iloc[0]),
        'pct_change': float((period_data['Price'].iloc[-1] - period_data['Price'].iloc[0]) / period_data['Price'].iloc[0] * 100),
        'volatility': float(period_data['log_return'].std() * np.sqrt(252))  # Annualized
    }
    
    return jsonify(stats)