export const callClaudeAI = async (data) => {
  const household = data.household || {};
  const prompt = `Analyze this energy data and return ONLY valid JSON (no markdown, no explanation).

Household Profile:
- Home: ${household.location || 'Unknown location'}
- Size: ${household.size_sqft || 1500} sq ft
- Occupants: ${household.occupants || 4}
- Electricity Rate: $${household.tariff_rate || 0.12}/kWh

Device: ${data.device_name || 'Home Energy'}
Readings count: ${data.readings_count}

Return this exact JSON structure:
{"summary":{"average_power_watts":0,"peak_power_watts":0,"daily_kwh":0,"monthly_cost_estimate":0,"description":"text"},"forecast":{"projected_monthly_kwh":0,"projected_monthly_cost":0,"trend":"stable","confidence":"medium","explanation":"text"},"anomalies":[],"recommendations":[{"type":"behavioral","title":"text","description":"text","estimated_savings_kwh":0,"estimated_savings_currency":0,"actions":["text"],"priority":"medium"}],"score":{"value":0,"grade":"B","breakdown":"text"}}`;

  try {
    const response = await puter.ai.chat(prompt, { model: 'claude-sonnet-4-6' });
    let text = response.message.content[0].text;
    
    // Remove markdown code blocks if present
    text = text.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
    
    return JSON.parse(text);
  } catch (error) {
    console.error('Claude AI error:', error);
    return getDefaultAnalysis();
  }
};

export const getDefaultAnalysis = () => ({
  summary: {
    average_power_watts: 0,
    peak_power_watts: 0,
    daily_kwh: 0,
    monthly_cost_estimate: 0,
    description: 'No data available yet.'
  },
  forecast: {
    projected_monthly_kwh: 0,
    projected_monthly_cost: 0,
    trend: 'stable',
    confidence: 'low',
    explanation: 'Generate readings to see forecasts.'
  },
  anomalies: [],
  recommendations: [
    {
      type: 'behavioral',
      title: 'Add a device to get started',
      description: 'Create a simulated device and generate readings to get personalized recommendations.',
      estimated_savings_kwh: 0,
      estimated_savings_currency: 0,
      actions: ['Go to Devices tab', 'Add a device', 'Generate readings'],
      priority: 'high'
    }
  ],
  score: { value: 0, grade: 'N/A', breakdown: 'No data yet' }
});
