import { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Devices from './components/Devices';
import Analysis from './components/Analysis';
import Scenarios from './components/Scenarios';
import Settings from './components/Settings';
import SimulationHistory from './components/SimulationHistory';
import { api } from './api';
import './App.css';

const views = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'devices', label: 'Devices' },
  { id: 'analysis', label: 'AI Analysis' },
  { id: 'scenarios', label: 'Scenarios' },
  { id: 'history', label: 'History' },
  { id: 'settings', label: 'Settings' },
];

export default function App() {
  const [view, setView] = useState('dashboard');
  const [devices, setDevices] = useState([]);
  const [household, setHousehold] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const [devicesData, householdData] = await Promise.all([
      api.getDevices(),
      api.getHousehold(),
    ]);
    setDevices(devicesData);
    setHousehold(householdData);
  };

  const handleMessage = (msg) => {
    setMessage(msg);
    setTimeout(() => setMessage(''), 4000);
    loadData();
  };

  const renderView = () => {
    switch (view) {
      case 'dashboard':
        return <Dashboard devices={devices} household={household} />;
      case 'devices':
        return <Devices onMessage={handleMessage} />;
      case 'analysis':
        return <Analysis devices={devices} household={household} onMessage={handleMessage} />;
      case 'scenarios':
        return <Scenarios onRun={handleMessage} />;
      case 'history':
        return <SimulationHistory />;
      case 'settings':
        return <Settings onMessage={handleMessage} />;
      default:
        return <Dashboard devices={devices} household={household} />;
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>
          Energy Efficiency Advisor 
          <span className="ai-badge">Powered by Claude AI</span>
        </h1>
        <p>AI-powered energy simulation and personalized recommendations</p>
      </header>

      {message && <div className="toast">{message}</div>}

      <nav className="nav">
        {views.map(v => (
          <button
            key={v.id}
            className={view === v.id ? 'active' : ''}
            onClick={() => setView(v.id)}
          >
            {v.label}
          </button>
        ))}
      </nav>

      <main>{renderView()}</main>
    </div>
  );
}
