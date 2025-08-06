import React from 'react';
import AnalysisPanel from './AnalysisPanel';
import DataUploadPanel from './DataUploadPanel';
import ResultsPanel from './ResultsPanel';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-grid">
      <DataUploadPanel />
      <AnalysisPanel />
      <ResultsPanel />
    </div>
  );
};

export default Dashboard;