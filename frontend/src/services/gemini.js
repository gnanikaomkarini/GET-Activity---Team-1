const API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

const promptTemplate = (data) => {
  const appliancesList = data.appliances
    .filter(a => a.count > 0)
    .map(a => {
      const dailyWh = a.count * a.wattage * a.hours;
      const monthlyKwh = dailyWh * 30 / 1000;
      return `- ${a.name}: ${a.count} ${a.unit}(s), ${a.hours}h/day usage = ${monthlyKwh.toFixed(1)} kWh/month`;
    })
    .join('\n');

  const totalMonthlyKwh = data.appliances
    .filter(a => a.count > 0)
    .reduce((sum, a) => sum + (a.count * a.wattage * a.hours * 30 / 1000), 0);

  return `You are an energy efficiency advisor. Analyze this household's energy consumption and provide detailed recommendations.

HOUSEHOLD INFO:
- Location: ${data.location || 'Not specified'}
- Occupants: ${data.occupants} people

APPLIANCES:
${appliancesList}

CURRENT ESTIMATED USAGE: ${totalMonthlyKwh.toFixed(1)} kWh/month

ADDITIONAL CONTEXT:
${data.context || 'None provided'}

Please provide your response in this exact JSON format:
{
  "summary": {
    "totalMonthlyKwh": number,
    "largestConsumer": "appliance name",
    "comparisonToAverage": "description"
  },
  "wasteAnalysis": [
    {
      "appliance": "name",
      "issue": "description of the problem",
      "monthlyWasteKwh": number
    }
  ],
  "savingTips": [
    {
      "appliance": "name",
      "tip": "specific actionable advice",
      "potentialMonthlyKwh": number,
      "difficulty": "easy|medium|hard"
    }
  ],
  "recommendations": [
    {
      "title": "recommendation title",
      "description": "detailed explanation",
      "impact": "high|medium|low",
      "actionSteps": ["step 1", "step 2"]
    }
  ],
  "estimatedAfterSavings": {
    "monthlyKwh": number,
    "percentReduction": number
  }
}

Respond ONLY with valid JSON, no markdown or extra text.`;
};

export async function getEnergyAdvice(data) {
  const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
  
  if (!apiKey || apiKey === 'your_api_key_here') {
    throw new Error('API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
  }

  const prompt = promptTemplate(data);
  
  const response = await fetch(`${API_URL}?key=${apiKey}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      contents: [{
        parts: [{ text: prompt }]
      }],
      generationConfig: {
        responseMimeType: 'application/json',
      }
    })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API Error: ${response.status} - ${error}`);
  }

  const result = await response.json();
  const text = result.candidates?.[0]?.content?.parts?.[0]?.text;
  
  if (!text) {
    throw new Error('No response from AI');
  }
  
  return JSON.parse(text);
}
