import React, { useState } from 'react';
import './DataUploadPanel.css';

const DataUploadPanel = () => {
  const [file, setFile] = useState(null);

  const sampleDatasets = [
    { name: "Brent Daily Prices (1987-2022)", type: "time-series" },
    { name: "Geopolitical Events", type: "events" },
    { name: "OPEC Decisions", type: "events" },
    { name: "Economic Indicators", type: "time-series" }
  ];

  return (
    <div className="data-upload-panel">
      <h2>Data Sources</h2>
      <div className="upload-area">
        <label className="file-upload">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          {file ? file.name : "Choose CSV file"}
        </label>
        <button 
          className="upload-button" 
          disabled={!file}
          onClick={() => alert(`Would upload ${file.name}`)}
        >
          Upload
        </button>
      </div>
      <div className="sample-datasets">
        <h3>Available Datasets</h3>
        <ul>
          {sampleDatasets.map((dataset, index) => (
            <li key={index}>
              <span className="dataset-name">{dataset.name}</span>
              <span className="dataset-type">{dataset.type}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DataUploadPanel;