import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './components/Dashboard';
import StatusPanel from './components/StatusPanel';
import './App.css';

function App() {
  const [dataLoaded, setDataLoaded] = useState(false);
  
  // Simulate data loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setDataLoaded(true);
    }, 1500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="app-container">
      <Header />
      <div className="main-content">
        {dataLoaded ? (
          <Dashboard />
        ) : (
          <div className="loading-screen">Loading Dashboard...</div>
        )}
        <StatusPanel />
      </div>
    </div>
  );
}

export default App;