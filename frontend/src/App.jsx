import { useState, useEffect } from 'react';
import { getDashboardMetrics, getWorkers, getWorkstations, seedData } from './api';
import './App.css';

function App() {
  const [dashboardData, setDashboardData] = useState(null);
  const [workers, setWorkers] = useState([]);
  const [workstations, setWorkstations] = useState([]);
  const [selectedWorker, setSelectedWorker] = useState('all');
  const [selectedWorkstation, setSelectedWorkstation] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [metricsData, workersData, workstationsData] = await Promise.all([
        getDashboardMetrics(),
        getWorkers(),
        getWorkstations(),
      ]);
      
      setDashboardData(metricsData);
      setWorkers(workersData);
      setWorkstations(workstationsData);
    } catch (err) {
      setError('Failed to load dashboard data. Please make sure the backend is running.');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await seedData(7);
      await loadData();
    } catch (err) {
      setError('Failed to refresh data');
      console.error('Error refreshing data:', err);
    } finally {
      setRefreshing(false);
    }
  };

  const getUtilizationClass = (utilization) => {
    if (utilization >= 70) return 'utilization-high';
    if (utilization >= 50) return 'utilization-medium';
    return 'utilization-low';
  };

  const filteredWorkerMetrics = dashboardData?.worker_metrics.filter(
    worker => selectedWorker === 'all' || worker.worker_id === selectedWorker
  ) || [];

  const filteredWorkstationMetrics = dashboardData?.workstation_metrics.filter(
    station => selectedWorkstation === 'all' || station.station_id === selectedWorkstation
  ) || [];

  if (loading) {
    return (
      <div className="loading">
        <h2>Loading dashboard...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={loadData} style={{ marginTop: '20px', padding: '10px 20px' }}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>🏭 Worker Productivity Dashboard</h1>
          <p>AI-Powered Real-Time Monitoring System</p>
          <button 
            className="refresh-button" 
            onClick={handleRefresh} 
            disabled={refreshing}
          >
            {refreshing ? 'Refreshing...' : '🔄 Refresh Data'}
          </button>
        </div>
      </header>

      <div className="container">
        {/* Factory-Level Metrics */}
        <section className="factory-metrics">
          <h2>📊 Factory-Wide Performance</h2>
          <div className="factory-stats">
            <div className="factory-stat">
              <div className="factory-stat-label">Total Productive Time</div>
              <div className="factory-stat-value">
                {dashboardData?.factory_metrics.total_productive_time}
                <span className="factory-stat-unit">hrs</span>
              </div>
            </div>
            <div className="factory-stat">
              <div className="factory-stat-label">Total Production</div>
              <div className="factory-stat-value">
                {dashboardData?.factory_metrics.total_production_count}
                <span className="factory-stat-unit">units</span>
              </div>
            </div>
            <div className="factory-stat">
              <div className="factory-stat-label">Avg Production Rate</div>
              <div className="factory-stat-value">
                {dashboardData?.factory_metrics.average_production_rate}
                <span className="factory-stat-unit">units/hr</span>
              </div>
            </div>
            <div className="factory-stat">
              <div className="factory-stat-label">Avg Utilization</div>
              <div className="factory-stat-value">
                {dashboardData?.factory_metrics.average_utilization}
                <span className="factory-stat-unit">%</span>
              </div>
            </div>
          </div>
        </section>

        {/* Worker Metrics */}
        <section>
          <div className="section-header">
            <h2>👷 Worker Metrics</h2>
            <select
              className="filter-select"
              value={selectedWorker}
              onChange={(e) => setSelectedWorker(e.target.value)}
            >
              <option value="all">All Workers</option>
              {workers.map(worker => (
                <option key={worker.worker_id} value={worker.worker_id}>
                  {worker.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="metrics-grid">
            {filteredWorkerMetrics.map(worker => (
              <div key={worker.worker_id} className="metric-card">
                <div className="metric-card-header">
                  <div className="metric-card-title">{worker.name}</div>
                  <div className="metric-card-id">{worker.worker_id}</div>
                </div>
                <div className="metric-card-body">
                  <div className="metric-item">
                    <div className="metric-item-label">Active Time</div>
                    <div className="metric-item-value">
                      {worker.total_active_time}
                      <span className="metric-item-unit">hrs</span>
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Idle Time</div>
                    <div className="metric-item-value">
                      {worker.total_idle_time}
                      <span className="metric-item-unit">hrs</span>
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Utilization</div>
                    <div className={`utilization-badge ${getUtilizationClass(worker.utilization_percentage)}`}>
                      {worker.utilization_percentage}%
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Units Produced</div>
                    <div className="metric-item-value">
                      {worker.total_units_produced}
                      <span className="metric-item-unit">units</span>
                    </div>
                  </div>
                  <div className="metric-item" style={{ gridColumn: 'span 2' }}>
                    <div className="metric-item-label">Production Rate</div>
                    <div className="metric-item-value">
                      {worker.units_per_hour}
                      <span className="metric-item-unit">units/hr</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Workstation Metrics */}
        <section>
          <div className="section-header">
            <h2>🏗️ Workstation Metrics</h2>
            <select
              className="filter-select"
              value={selectedWorkstation}
              onChange={(e) => setSelectedWorkstation(e.target.value)}
            >
              <option value="all">All Workstations</option>
              {workstations.map(station => (
                <option key={station.station_id} value={station.station_id}>
                  {station.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="metrics-grid">
            {filteredWorkstationMetrics.map(station => (
              <div key={station.station_id} className="metric-card">
                <div className="metric-card-header">
                  <div className="metric-card-title">{station.name}</div>
                  <div className="metric-card-id">{station.station_id}</div>
                </div>
                <div className="metric-card-body">
                  <div className="metric-item">
                    <div className="metric-item-label">Occupancy Time</div>
                    <div className="metric-item-value">
                      {station.occupancy_time}
                      <span className="metric-item-unit">hrs</span>
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Utilization</div>
                    <div className={`utilization-badge ${getUtilizationClass(station.utilization_percentage)}`}>
                      {station.utilization_percentage}%
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Units Produced</div>
                    <div className="metric-item-value">
                      {station.total_units_produced}
                      <span className="metric-item-unit">units</span>
                    </div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-item-label">Throughput Rate</div>
                    <div className="metric-item-value">
                      {station.throughput_rate}
                      <span className="metric-item-unit">units/hr</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
