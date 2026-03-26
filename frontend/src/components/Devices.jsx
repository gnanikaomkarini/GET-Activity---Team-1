import { useState, useEffect } from 'react';
import { api } from '../api';

const icons = {
  smart_meter: '⚡',
  thermostat: '🌡️',
  plug: '🔌',
  energy_monitor: '📊',
};

export default function Devices({ onMessage }) {
  const [devices, setDevices] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newDevice, setNewDevice] = useState({ name: '', type: 'smart_meter' });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    const data = await api.getDevices();
    setDevices(data);
  };

  const handleAdd = async () => {
    if (!newDevice.name.trim()) return;
    await api.createDevice({ ...newDevice, location: 'Home', params: {} });
    setNewDevice({ name: '', type: 'smart_meter' });
    setShowModal(false);
    loadDevices();
    onMessage('Device added!');
  };

  const handleGenerate = async (id) => {
    setLoading(true);
    await api.generateReadings(id, 96);
    await api.deleteReadings(id);
    await api.getReadings(id, 200).then(r => r);
    setLoading(false);
    onMessage('Data generated!');
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this device?')) return;
    await api.deleteDevice(id);
    loadDevices();
    onMessage('Device deleted');
  };

  return (
    <div className="devices">
      <div className="card">
        <div className="card-header">
          <h2>Your Devices</h2>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            + Add Device
          </button>
        </div>

        {devices.length === 0 ? (
          <p className="empty-text">No devices yet. Add one to get started!</p>
        ) : (
          <div className="device-list">
            {devices.map(device => (
              <div key={device.id} className="device-item">
                <div className="device-info">
                  <div className="device-icon">{icons[device.type] || '⚡'}</div>
                  <div>
                    <div className="device-name">{device.name}</div>
                    <div className="device-type">{device.type}</div>
                  </div>
                </div>
                <div className="device-actions">
                  <button 
                    className="btn btn-primary btn-sm" 
                    onClick={() => handleGenerate(device.id)}
                    disabled={loading}
                  >
                    {loading ? 'Generating...' : 'Generate Data'}
                  </button>
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(device.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h3>Add New Device</h3>
            <input
              type="text"
              placeholder="Device name"
              value={newDevice.name}
              onChange={e => setNewDevice({ ...newDevice, name: e.target.value })}
              autoFocus
            />
            <select value={newDevice.type} onChange={e => setNewDevice({ ...newDevice, type: e.target.value })}>
              <option value="smart_meter">Smart Meter</option>
              <option value="thermostat">Thermostat</option>
              <option value="plug">Smart Plug</option>
              <option value="energy_monitor">Energy Monitor</option>
            </select>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={() => setShowModal(false)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleAdd}>Add Device</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
