import { useState } from 'react';
import HomeForm from './components/HomeForm';
import Results from './components/Results';
import Loading from './components/Loading';
import { getEnergyAdvice } from './services/gemini';
import './App.css';

export default function App() {
  const [view, setView] = useState('form');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const advice = await getEnergyAdvice(data);
      setResults(advice);
      setView('results');
    } catch (err) {
      setError(err.message);
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setView('form');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Energy Efficiency Advisor</h1>
        <p>Get AI-powered recommendations to reduce your energy bills</p>
      </header>

      <main className="main">
        {view === 'form' && (
          <>
            {error && <div className="error-banner">{error}</div>}
            <HomeForm onSubmit={handleSubmit} loading={loading} />
            {loading && <Loading />}
          </>
        )}
        
        {view === 'results' && results && (
          <Results data={results} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>Powered by Google Gemini AI</p>
      </footer>
    </div>
  );
}
