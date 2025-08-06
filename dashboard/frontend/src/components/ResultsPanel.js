import React from 'react';
import './ResultsPanel.css';

const ResultsPanel = () => {
  const impactAnalysis = [
    {
      event: "Russia-Ukraine Conflict",
      date: "2022-03-01",
      impact: "+12%",
      duration: "1 month",
      confidence: "High"
    },
    {
      event: "OPEC Production Increase",
      date: "2022-07-01",
      impact: "-5%",
      duration: "1 month",
      confidence: "Medium"
    },
    {
      event: "Global Recession Concerns",
      date: "2022-10-01",
      impact: "+40% volatility",
      duration: "Ongoing",
      confidence: "High"
    }
  ];

  const stats = {
    totalChangePoints: 3,
    strongestImpact: "+12%",
    mostVolatilePeriod: "March 2022",
    correlationStrength: "0.82"
  };

  return (
    <div className="results-panel">
      <h2>Key Findings</h2>
      
      <div className="impact-analysis">
        <h3>Event Impact Analysis</h3>
        <div className="impact-list">
          {impactAnalysis.map((item, index) => (
            <div key={index} className="impact-item">
              <div className="impact-event">
                <strong>{item.event}</strong>
                <span className="impact-date">{item.date}</span>
              </div>
              <div className="impact-details">
                <div className="impact-value">{item.impact}</div>
                <div className="impact-meta">
                  <span>{item.duration}</span>
                  <span className={`confidence-${item.confidence.toLowerCase()}`}>
                    {item.confidence}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="summary-stats">
        <h3>Summary Statistics</h3>
        <div className="stats-grid">
          <div className="stat-item">
            <div className="stat-value">{stats.totalChangePoints}</div>
            <div className="stat-label">Change Points</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{stats.strongestImpact}</div>
            <div className="stat-label">Strongest Impact</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{stats.mostVolatilePeriod}</div>
            <div className="stat-label">Most Volatile</div>
          </div>
          <div className="stat-item">
            <div className="stat-value">{stats.correlationStrength}</div>
            <div className="stat-label">Correlation</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsPanel;