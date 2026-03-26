const API_URL = 'http://localhost:8000/api';

export const api = {
  async getDevices() {
    const res = await fetch(`${API_URL}/devices`);
    return res.json();
  },

  async createDevice(device) {
    const res = await fetch(`${API_URL}/devices`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(device),
    });
    return res.json();
  },

  async deleteDevice(id) {
    await fetch(`${API_URL}/devices/${id}`, { method: 'DELETE' });
  },

  async getReadings(deviceId, limit = 100) {
    const url = deviceId 
      ? `${API_URL}/readings?device_id=${deviceId}&limit=${limit}`
      : `${API_URL}/readings?limit=${limit}`;
    const res = await fetch(url);
    return res.json();
  },

  async generateReadings(deviceId, count = 96, householdId = 1) {
    const res = await fetch(`${API_URL}/simulate/generate?device_id=${deviceId}&count=${count}&household_id=${householdId}`, {
      method: 'POST',
    });
    return res.json();
  },

  async runScenario(deviceId, scenario, hours = 48, householdId = 1) {
    const res = await fetch(`${API_URL}/simulate/scenario?device_id=${deviceId}&scenario=${scenario}&duration_hours=${hours}&household_id=${householdId}`, {
      method: 'POST',
    });
    return res.json();
  },

  async getDeviceReadings(deviceId) {
    const res = await fetch(`${API_URL}/devices/${deviceId}/readings`);
    return res.json();
  },

  async saveAnalysis(data) {
    const res = await fetch(`${API_URL}/analysis`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  async getAnalysis() {
    const res = await fetch(`${API_URL}/analysis`);
    return res.json();
  },

  async deleteReadings(deviceId) {
    await fetch(`${API_URL}/readings/${deviceId}`, { method: 'DELETE' });
  },

  // Household profile
  async getHousehold() {
    const res = await fetch(`${API_URL}/household`);
    return res.json();
  },

  async saveHousehold(data) {
    const res = await fetch(`${API_URL}/household`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },

  // Simulation runs history
  async getSimulationRuns(deviceId = null) {
    const url = deviceId 
      ? `${API_URL}/simulation-runs?device_id=${deviceId}`
      : `${API_URL}/simulation-runs`;
    const res = await fetch(url);
    return res.json();
  },
};
