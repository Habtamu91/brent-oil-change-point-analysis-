import React from 'react';
import './StatusPanel.css';

const StatusPanel = () => {
  const statusItems = [
    { name: "Data Connection", status: "active", lastChecked: "2 min ago" },
    { name: "Analysis Model", status: "active", lastChecked: "Just now" },
    { name: "Visualization", status: "active", lastChecked: "1 min ago" },
    { name: "API Service", status: "active", lastChecked: "5 min ago" }
  ];

  return (
    <div className="status-panel">
      <h2>System Status</h2>
      <div className="status-items">
        {statusItems.map((item, index) => (
          <div key={index} className={`status-item ${item.status}`}>
            <div className="status-indicator"></div>
            <div className="status-info">
              <div className="status-name">{item.name}</div>
              <div className="status-meta">{item.lastChecked}</div>
            </div>
          </div>
        ))}
      </div>
      <div className="last-updated">
        Last updated: {new Date().toLocaleString()}
      </div>
    </div>
  );
};

export default StatusPanel;