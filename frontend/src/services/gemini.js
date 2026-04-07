import { GoogleGenerativeAI } from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY);

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
- Electricity Rate: $${data.tariffRate}/kWh

APPLIANCES:
${appliancesList}

CURRENT ESTIMATED USAGE: ${totalMonthlyKwh.toFixed(1)} kWh/month ($${(totalMonthlyKwh * data.tariffRate).toFixed(2)}/month)

ADDITIONAL CONTEXT:
${data.context || 'None provided'}

Please provide your response in this exact JSON format:
{
  "summary": {
    "totalMonthlyKwh": number,
    "totalMonthlyCost": number,
    "largestConsumer": "appliance name",
    "comparisonToAverage": "description"
  },
  "wasteAnalysis": [
    {
      "appliance": "name",
      "issue": "description of the problem",
      "monthlyWasteKwh": number,
      "monthlyWasteCost": number
    }
  ],
  "savingTips": [
    {
      "appliance": "name",
      "tip": "specific actionable advice",
      "potentialMonthlyKwh": number,
      "potentialMonthlySavings": number,
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
    "monthlyCost": number,
    "percentReduction": number
  }
}

Respond ONLY with valid JSON, no markdown or extra text.`;
};

export async function getEnergyAdvice(data) {
  if (!import.meta.env.VITE_GEMINI_API_KEY || import.meta.env.VITE_GEMINI_API_KEY === 'your_api_key_here') {
    throw new Error('API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
  }

  const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });
  const prompt = promptTemplate(data);
  
  const result = await model.generateContent(prompt);
  const response = await result.response;
  const text = response.text();
  
  const cleanedText = text.replace(/```json\n?/g, '').replace(/```\n?$/g, '').trim();
  
  return JSON.parse(cleanedText);
}
