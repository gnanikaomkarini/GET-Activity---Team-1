# Energy Efficiency Advisor

AI-powered energy efficiency advisor that analyzes your household appliances and provides personalized recommendations to reduce energy consumption.

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### Setup API Key

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a `.env` file in the `frontend` folder:
   ```
   VITE_GEMINI_API_KEY=your_api_key_here
   ```
3. Restart the dev server

## Features

- **Appliance Analysis** - Input your household appliances and usage patterns
- **AI Recommendations** - Personalized tips powered by Gemini AI
- **Energy Waste Detection** - Identify where you're using too much energy
- **Savings Calculator** - See how much you can reduce your usage
- **India-Focused** - Designed for Indian households with common appliances

## How It Works

1. Enter your household info (occupants, location)
2. Select your appliances and daily usage
3. Add any additional context
4. Get AI-powered recommendations

## Tech Stack

- **Frontend**: React + Vite
- **AI**: Google Gemini 2.5 Flash

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main app
│   ├── App.css              # Styles
│   ├── components/
│   │   ├── HomeForm.jsx    # Appliance input form
│   │   ├── Results.jsx     # AI recommendations
│   │   └── Loading.jsx     # Loading spinner
│   ├── services/
│   │   └── gemini.js       # Gemini API integration
│   └── data/
│       └── appliances.js    # Appliance database
├── .env.example             # API key template
└── package.json
```
