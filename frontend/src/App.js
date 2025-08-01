import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ReferenceLine } from 'recharts';
import { Select, DatePicker, Card, Statistic, Row, Col, Table } from 'antd';
import './App.css';

const { Option } = Select;
const { RangePicker } = DatePicker;

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [stats, setStats] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [dateRange, setDateRange] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch all data when component mounts
    Promise.all([
      fetch('http://localhost:5000/api/prices').then(res => res.json()),
      fetch('http://localhost:5000/api/events').then(res => res.json()),
      fetch('http://localhost:5000/api/change_points').then(res => res.json())
    ]).then(([pricesData, eventsData, changePointsData]) => {
      setPrices(pricesData);
      setEvents(eventsData);
      setChangePoints(changePointsData);
      setLoading(false);
    });
  }, []);

  const handleEventSelect = (value) => {
    const event = events.find(e => e.Event === value);
    setSelectedEvent(event);
    
    // Set date range to 3 months before and after event
    if (event) {
      const eventDate = new Date(event.Date);
      const startDate = new Date(eventDate);
      startDate.setMonth(startDate.getMonth() - 3);
      const endDate = new Date(eventDate);
      endDate.setMonth(endDate.getMonth() + 3);
      
      setDateRange([startDate, endDate]);
      fetchPeriodStats(startDate.toISOString().split('T')[0], endDate.toISOString().split('T')[0]);
    }
  };

  const handleDateRangeChange = (dates) => {
    setDateRange(dates);
    if (dates && dates.length === 2) {
      fetchPeriodStats(dates[0].format('YYYY-MM-DD'), dates[1].format('YYYY-MM-DD'));
    }
  };

  const fetchPeriodStats = (startDate, endDate) => {
    fetch('http://localhost:5000/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ start_date: startDate, end_date: endDate }),
    })
      .then(res => res.json())
      .then(data => {
        if (!data.error) {
          setStats(data);
        }
      });
  };

  const eventColumns = [
    {
      title: 'Date',
      dataIndex: 'Date',
      key: 'Date',
      sorter: (a, b) => new Date(a.Date) - new Date(b.Date),
    },
    {
      title: 'Event',
      dataIndex: 'Event',
      key: 'Event',
    },
    {
      title: 'Description',
      dataIndex: 'Description',
      key: 'Description',
    },
    {
      title: 'Category',
      dataIndex: 'Category',
      key: 'Category',
      filters: [
        { text: 'Geopolitical', value: 'Geopolitical' },
        { text: 'Economic', value: 'Economic' },
        { text: 'Policy', value: 'Policy' },
        { text: 'Natural Disaster', value: 'Natural Disaster' },
      ],
      onFilter: (value, record) => record.Category === value,
    },
  ];

  return (
    <div className="App">
      <h1>Brent Oil Price Change Point Analysis</h1>
      
      <div className="controls">
        <Select
          showSearch
          style={{ width: 300 }}
          placeholder="Select an event"
          optionFilterProp="children"
          onChange={handleEventSelect}
          filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
          }
        >
          {events.map(event => (
            <Option key={event.Event} value={event.Event}>{event.Event}</Option>
          ))}
        </Select>
        
        <RangePicker
          style={{ marginLeft: 20 }}
          onChange={handleDateRangeChange}
          value={dateRange}
        />
      </div>
      
      {stats && (
        <Row gutter={16} style={{ margin: '20px 0' }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="Price Change"
                value={stats.price_change.toFixed(2)}
                precision={2}
                valueStyle={{ color: stats.price_change >= 0 ? '#3f8600' : '#cf1322' }}
                prefix={stats.price_change >= 0 ? '+' : ''}
                suffix="USD"
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Percentage Change"
                value={stats.pct_change.toFixed(2)}
                precision={2}
                valueStyle={{ color: stats.pct_change >= 0 ? '#3f8600' : '#cf1322' }}
                prefix={stats.pct_change >= 0 ? '+' : ''}
                suffix="%"
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="Annualized Volatility"
                value={(stats.volatility * 100).toFixed(2)}
                precision={2}
                suffix="%"
              />
            </Card>
          </Col>
        </Row>
      )}
      
      <div className="chart-container">
        <LineChart
          width={1200}
          height={500}
          data={prices}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="Date" 
            tickFormatter={(date) => new Date(date).toLocaleDateString()}
          />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip 
            labelFormatter={(date) => new Date(date).toLocaleDateString()}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="Price" 
            stroke="#8884d8" 
            dot={false}
            name="Brent Oil Price (USD)" 
          />
          
          {/* Add reference lines for events */}
          {selectedEvent && (
            <ReferenceLine 
              x={selectedEvent.Date}
              stroke="red"
              label={selectedEvent.Event}
            />
          )}
          
          {/* Add reference lines for change points */}
          {changePoints.map((cp, index) => (
            <ReferenceLine
              key={index}
              x={cp.date}
              stroke="#ff7300"
              label={`Change ${index+1}`}
            />
          ))}
        </LineChart>
      </div>
      
      <div className="tables-container">
        <div className="events-table">
          <h2>Key Events</h2>
          <Table 
            dataSource={events} 
            columns={eventColumns} 
            rowKey="Event"
            pagination={{ pageSize: 5 }}
          />
        </div>
        
        <div className="change-points-table">
          <h2>Detected Change Points</h2>
          <Table 
            dataSource={changePoints.map((cp, i) => ({ ...cp, key: i }))} 
            columns={[
              { title: 'Date', dataIndex: 'date', key: 'date' },
              { title: 'Mean Before', dataIndex: 'mean_before', key: 'mean_before', render: val => val.toFixed(2) },
              { title: 'Mean After', dataIndex: 'mean_after', key: 'mean_after', render: val => val.toFixed(2) },
              { 
                title: 'Change (%)', 
                dataIndex: 'pct_change', 
                key: 'pct_change',
                render: val => (
                  <span style={{ color: val >= 0 ? '#3f8600' : '#cf1322' }}>
                    {val.toFixed(2)}%
                  </span>
                )
              },
            ]} 
            pagination={{ pageSize: 5 }}
          />
        </div>
      </div>
    </div>
  );
}

export default App;