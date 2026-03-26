import { useState, useEffect } from 'react';
import { api } from '../api';

export default function Settings({ onMessage }) {
  const [household, setHousehold] = useState({
    name: 'My Home',
    size_sqft: 1500,
    occupants: 4,
    location: 'Unknown',
    tariff_rate: 0.12,
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadHousehold();
  }, []);

  const loadHousehold = async () => {
    const data = await api.getHousehold();
    setHousehold(data);
  };

  const handleSave = async () => {
    setSaving(true);
    await api.saveHousehold(household);
    setSaving(false);
    onMessage('Settings saved!');
  };

  const handleChange = (field, value) => {
    setHousehold({ ...household, [field]: value });
  };

  return (
    <div className="card">
      <h2>Household Settings</h2>
      <p style={{ color: '#666', marginBottom: 20 }}>
        Configure your household details for more accurate energy analysis.
      </p>

      <div style={{ display: 'grid', gap: 16 }}>
        <div>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 500 }}>
            Home Name
          </label>
          <input
            type="text"
            value={household.name}
            onChange={e => handleChange('name', e.target.value)}
            style={{ width: '100%', padding: 10, border: '1px solid #ddd', borderRadius: 8 }}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div>
            <label style={{ display: 'block', marginBottom: 6, fontWeight: 500 }}>
              Home Size (sq ft)
            </label>
            <input
              type="number"
              value={household.size_sqft}
              onChange={e => handleChange('size_sqft', parseInt(e.target.value))}
              style={{ width: '100%', padding: 10, border: '1px solid #ddd', borderRadius: 8 }}
            />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: 6, fontWeight: 500 }}>
              Number of Occupants
            </label>
            <input
              type="number"
              value={household.occupants}
              onChange={e => handleChange('occupants', parseInt(e.target.value))}
              style={{ width: '100%', padding: 10, border: '1px solid #ddd', borderRadius: 8 }}
            />
          </div>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 500 }}>
            Location
          </label>
          <input
            type="text"
            value={household.location}
            onChange={e => handleChange('location', e.target.value)}
            placeholder="e.g., California, USA"
            style={{ width: '100%', padding: 10, border: '1px solid #ddd', borderRadius: 8 }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: 6, fontWeight: 500 }}>
            Electricity Rate ($/kWh)
          </label>
          <input
            type="number"
            step="0.01"
            value={household.tariff_rate}
            onChange={e => handleChange('tariff_rate', parseFloat(e.target.value))}
            style={{ width: '100%', padding: 10, border: '1px solid #ddd', borderRadius: 8 }}
          />
        </div>

        <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
      </div>
    </div>
  );
}
