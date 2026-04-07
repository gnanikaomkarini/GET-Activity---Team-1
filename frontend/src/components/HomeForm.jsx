import { useState } from 'react';
import { appliances } from '../data/appliances';

export default function HomeForm({ onSubmit, loading }) {
  const [household, setHousehold] = useState({
    occupants: 4,
    location: '',
    tariffRate: 0.12,
  });
  const [applianceData, setApplianceData] = useState(() => {
    const initial = {};
    appliances.forEach(a => {
      initial[a.id] = { count: 0, usageIndex: 1 };
    });
    return initial;
  });
  const [context, setContext] = useState('');

  const handleApplianceChange = (id, field, value) => {
    setApplianceData(prev => ({
      ...prev,
      [id]: { ...prev[id], [field]: value },
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const formattedAppliances = appliances
      .filter(a => applianceData[a.id].count > 0)
      .map(a => ({
        name: a.name,
        wattage: a.wattage,
        count: applianceData[a.id].count,
        unit: a.unit,
        hours: a.usageOptions[applianceData[a.id].usageIndex]?.hours || 0,
      }));

    onSubmit({
      ...household,
      appliances: formattedAppliances,
      context,
    });
  };

  const hasAppliances = Object.values(applianceData).some(a => a.count > 0);

  return (
    <form onSubmit={handleSubmit}>
      <div className="section">
        <h2>Household Info</h2>
        <div className="form-grid">
          <div className="form-group">
            <label>Number of Occupants</label>
            <input
              type="number"
              min="1"
              max="20"
              value={household.occupants}
              onChange={e => setHousehold({ ...household, occupants: parseInt(e.target.value) || 1 })}
              required
            />
          </div>
          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              placeholder="e.g., California, USA"
              value={household.location}
              onChange={e => setHousehold({ ...household, location: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Electricity Rate ($/kWh)</label>
            <input
              type="number"
              step="0.01"
              min="0.01"
              value={household.tariffRate}
              onChange={e => setHousehold({ ...household, tariffRate: parseFloat(e.target.value) || 0.12 })}
              required
            />
          </div>
        </div>
      </div>

      <div className="section">
        <h2>Your Appliances</h2>
        <p className="subtitle">Select how many of each appliance you have and your daily usage.</p>
        
        <div className="appliance-grid">
          {appliances.map(appliance => (
            <div key={appliance.id} className="appliance-card">
              <div className="appliance-header">
                <span className="appliance-icon">{appliance.icon}</span>
                <div>
                  <div className="appliance-name">{appliance.name}</div>
                  <div className="appliance-desc">{appliance.description}</div>
                </div>
              </div>
              <div className="appliance-controls">
                <div className="form-group">
                  <label>Count</label>
                  <input
                    type="number"
                    min="0"
                    max="20"
                    value={applianceData[appliance.id].count}
                    onChange={e => handleApplianceChange(appliance.id, 'count', parseInt(e.target.value) || 0)}
                  />
                </div>
                <div className="form-group">
                  <label>Usage</label>
                  <select
                    value={applianceData[appliance.id].usageIndex}
                    onChange={e => handleApplianceChange(appliance.id, 'usageIndex', parseInt(e.target.value))}
                    disabled={applianceData[appliance.id].count === 0}
                  >
                    {appliance.usageOptions.map((opt, idx) => (
                      <option key={idx} value={idx}>{opt.label}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h2>Additional Context</h2>
        <p className="subtitle">Anything else we should know? (e.g., work from home, elderly family members, pool pump)</p>
        <textarea
          className="context-input"
          placeholder="I work from home 3 days a week. We have a pool that runs 6 hours daily..."
          value={context}
          onChange={e => setContext(e.target.value)}
          rows={4}
        />
      </div>

      <button 
        type="submit" 
        className="submit-btn" 
        disabled={loading || !hasAppliances}
      >
        {loading ? 'Analyzing...' : 'Get Energy Advice'}
      </button>
      
      {!hasAppliances && (
        <p className="hint">Add at least one appliance to get recommendations.</p>
      )}
    </form>
  );
}
