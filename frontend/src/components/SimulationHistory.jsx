import { useState, useEffect } from 'react';
import { api } from '../api';

export default function SimulationHistory() {
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRuns();
  }, []);

  const loadRuns = async () => {
    setLoading(true);
    const data = await api.getSimulationRuns();
    setRuns(data);
    setLoading(false);
  };

  if (loading) {
    return <div className="card"><p>Loading...</p></div>;
  }

  return (
    <div className="card">
      <h2>Simulation History</h2>
      <p style={{ color: '#666', marginBottom: 20 }}>
        View your past simulation runs and their results.
      </p>

      {runs.length === 0 ? (
        <p className="empty-text">
          No simulations run yet. Go to Scenarios to run your first simulation.
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {runs.map(run => (
            <div key={run.id} className="device-item" style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                <div>
                  <div className="device-name" style={{ textTransform: 'capitalize' }}>
                    {run.scenario.replace('_', ' ')}
                  </div>
                  <div className="device-type">
                    {new Date(run.created_at).toLocaleString()}
                  </div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontWeight: 600, color: '#10b981' }}>
                    {run.readings_count} readings
                  </div>
                </div>
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16, width: '100%' }}>
                <div style={{ background: '#f9fafb', padding: 12, borderRadius: 8, textAlign: 'center' }}>
                  <div style={{ fontSize: 12, color: '#666' }}>Avg Power</div>
                  <div style={{ fontSize: 18, fontWeight: 600 }}>{Math.round(run.avg_power)}W</div>
                </div>
                <div style={{ background: '#f9fafb', padding: 12, borderRadius: 8, textAlign: 'center' }}>
                  <div style={{ fontSize: 12, color: '#666' }}>Total Energy</div>
                  <div style={{ fontSize: 18, fontWeight: 600 }}>{run.total_energy.toFixed(1)}kWh</div>
                </div>
                <div style={{ background: '#f9fafb', padding: 12, borderRadius: 8, textAlign: 'center' }}>
                  <div style={{ fontSize: 12, color: '#666' }}>Duration</div>
                  <div style={{ fontSize: 18, fontWeight: 600 }}>{run.duration_hours}h</div>
                </div>
              </div>
              
              {run.summary && (
                <div style={{ fontSize: 13, color: '#666', fontStyle: 'italic' }}>
                  {run.summary}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
