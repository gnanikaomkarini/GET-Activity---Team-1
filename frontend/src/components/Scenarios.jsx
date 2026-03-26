import { useState, useEffect } from 'react';
import { api } from '../api';

const scenarios = [
  { id: 'normal', name: 'Normal Usage', desc: 'Typical daily energy usage' },
  { id: 'heating', name: 'Winter Heating', desc: 'Higher consumption due to heating' },
  { id: 'cooling', name: 'Summer Cooling', desc: 'Peak AC usage during hot days' },
  { id: 'vacation', name: 'Vacation Mode', desc: 'Minimal usage while away' },
  { id: 'high_consumption', name: 'High Usage', desc: 'Elevated baseline consumption' },
  { id: 'anomaly_spike', name: 'Anomaly Spike', desc: 'Sudden spike in usage' },
  { id: 'anomaly_drop', name: 'Anomaly Drop', desc: 'Unexpected drop in usage' },
];

export default function Scenarios({ onRun }) {
  const [devices, setDevices] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState('normal');
  const [selectedDevice, setSelectedDevice] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    const data = await api.getDevices();
    setDevices(data);
    if (data.length > 0) setSelectedDevice(data[0].id);
  };

  const handleRun = async () => {
    if (!selectedDevice) return;
    
    setLoading(true);
    setResult(null);
    
    try {
      const res = await api.runScenario(selectedDevice, selectedScenario, 48);
      setResult(res);
      onRun(`Simulation complete! ${res.count} readings generated. Avg: ${Math.round(res.avg_power)}W`);
    } catch (error) {
      onRun('Simulation failed');
    }
    
    setLoading(false);
  };

  const scenarioInfo = scenarios.find(s => s.id === selectedScenario);

  return (
    <div className="scenarios">
      <div className="card">
        <h2>Run Simulation Scenarios</h2>
        <p style={{ color: '#666', marginBottom: 20 }}>
          Test different energy scenarios to see how they affect your consumption.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 12, marginBottom: 20 }}>
          {scenarios.map(s => (
            <button
              key={s.id}
              className={`scenario-btn ${selectedScenario === s.id ? 'active' : ''}`}
              onClick={() => setSelectedScenario(s.id)}
              style={{ padding: 16, textAlign: 'left' }}
            >
              <div style={{ fontWeight: 600, marginBottom: 4 }}>{s.name}</div>
              <div style={{ fontSize: 12, opacity: 0.8 }}>{s.desc}</div>
            </button>
          ))}
        </div>

        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 8, fontWeight: 500 }}>
            Select Device:
          </label>
          <select
            value={selectedDevice}
            onChange={e => setSelectedDevice(Number(e.target.value))}
            style={{ width: '100%', padding: 12, border: '1px solid #ddd', borderRadius: 8, fontSize: 14 }}
          >
            {devices.length === 0 ? (
              <option value="">No devices - add one first</option>
            ) : (
              devices.map(d => (
                <option key={d.id} value={d.id}>{d.name} ({d.type})</option>
              ))
            )}
          </select>
        </div>

        <button
          className="btn btn-primary"
          onClick={handleRun}
          disabled={!selectedDevice || loading}
          style={{ marginBottom: 20 }}
        >
          {loading ? 'Running Simulation...' : `Run ${scenarioInfo?.name || 'Scenario'}`}
        </button>

        {result && (
          <div style={{ background: '#f0fdf4', border: '1px solid #10b981', borderRadius: 12, padding: 20 }}>
            <h3 style={{ color: '#10b981', marginBottom: 16 }}>✓ Simulation Complete</h3>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, marginBottom: 16 }}>
              <div style={{ background: 'white', padding: 16, borderRadius: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 12, color: '#666' }}>Readings Generated</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#10b981' }}>{result.count}</div>
              </div>
              <div style={{ background: 'white', padding: 16, borderRadius: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 12, color: '#666' }}>Avg Power</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#10b981' }}>{Math.round(result.avg_power)}W</div>
              </div>
              <div style={{ background: 'white', padding: 16, borderRadius: 8, textAlign: 'center' }}>
                <div style={{ fontSize: 12, color: '#666' }}>Est. Cost</div>
                <div style={{ fontSize: 24, fontWeight: 700, color: '#10b981' }}>${result.estimated_cost?.toFixed(2)}</div>
              </div>
            </div>
            
            <p style={{ fontSize: 14, color: '#666' }}>
              {scenarioInfo?.desc} - Generated {result.count} readings over 48 hours.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
