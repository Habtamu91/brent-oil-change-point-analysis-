import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './AnalysisPanel.css';

const AnalysisPanel = () => {
  const [activeTab, setActiveTab] = useState('changePoints');

  // Sample price data
  const priceData = [
    { date: '2022-01-01', price: 78.50 },
    { date: '2022-02-01', price: 82.30 },
    { date: '2022-03-01', price: 85.10 },
    { date: '2022-04-01', price: 83.75 },
    { date: '2022-05-01', price: 87.20 },
    { date: '2022-06-01', price: 89.50 },
    { date: '2022-07-01', price: 86.30 },
    { date: '2022-08-01', price: 84.90 },
    { date: '2022-09-01', price: 82.10 },
    { date: '2022-10-01', price: 85.40 },
    { date: '2022-11-01', price: 88.20 },
    { date: '2022-12-01', price: 86.75 }
  ];

  // Sample change points
  const changePoints = [
    { date: '2022-03-01', confidence: 0.95, description: 'Russia-Ukraine conflict impact' },
    { date: '2022-07-01', confidence: 0.88, description: 'OPEC production decision' },
    { date: '2022-10-01', confidence: 0.91, description: 'Global recession concerns' }
  ];

  return (
    <div className="analysis-panel">
      <div className="tabs">
        <button 
          className={activeTab === 'changePoints' ? 'active' : ''}
          onClick={() => setActiveTab('changePoints')}
        >
          Change Points
        </button>
        <button 
          className={activeTab === 'events' ? 'active' : ''}
          onClick={() => setActiveTab('events')}
        >
          Events Correlation
        </button>
      </div>
      
      <div className="tab-content">
        {activeTab === 'changePoints' && (
          <div className="change-points-analysis">
            <h3>Price Trend with Change Points</h3>
            <div className="chart-container">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={priceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    name="Brent Oil Price" 
                    stroke="#3498db" 
                    strokeWidth={2}
                    dot={false}
                  />
                  {changePoints.map((cp, index) => (
                    <line
                      key={index}
                      x1={cp.date}
                      x2={cp.date}
                      y1={0}
                      y2={100}
                      stroke="#e74c3c"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                    />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div className="change-points-list">
              <h4>Detected Change Points</h4>
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Confidence</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {changePoints.map((cp, index) => (
                    <tr key={index}>
                      <td>{cp.date}</td>
                      <td>{(cp.confidence * 100).toFixed(0)}%</td>
                      <td>{cp.description}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
        
        {activeTab === 'events' && (
          <div className="events-analysis">
            <h3>Events Correlation Analysis</h3>
            <div className="events-list">
              <div className="event-item">
                <div className="event-date">2022-03-01</div>
                <div className="event-content">
                  <strong>Russia-Ukraine Conflict</strong>
                  <p>Price increased by 12% in following month</p>
                </div>
              </div>
              <div className="event-item">
                <div className="event-date">2022-07-01</div>
                <div className="event-content">
                  <strong>OPEC Production Increase</strong>
                  <p>Price decreased by 5% in following month</p>
                </div>
              </div>
              <div className="event-item">
                <div className="event-date">2022-10-01</div>
                <div className="event-content">
                  <strong>Global Recession Concerns</strong>
                  <p>Price volatility increased by 40%</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisPanel;