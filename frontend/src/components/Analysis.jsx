import { useState } from 'react';
import { api } from '../api';
import { callClaudeAI } from '../ai';

export default function Analysis({ devices, onMessage }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const loadAnalysis = async () => {
    setLoading(true);
    const data = await api.getAnalysis();
    if (data.analysis) {
      setAnalysis(data.analysis);
    }
    setLoading(false);
  };

  const runAIAnalysis = async () => {
    if (devices.length === 0) {
      onMessage('Add a device first!');
      return;
    }

    setAnalyzing(true);
    try {
      const readingsData = await api.getDeviceReadings(devices[0].id);
      
      if (readingsData.readings_count < 5) {
        onMessage('Generate readings first!');
        setAnalyzing(false);
        return;
      }

      if (readingsData.cached_analysis) {
        setAnalysis(readingsData.cached_analysis);
        await api.saveAnalysis({
          device_id: devices[0].id,
          readings_hash: readingsData.readings_hash,
          analysis_data: readingsData.cached_analysis,
          readings_count: readingsData.readings_count,
        });
        onMessage('Loaded cached analysis!');
      } else {
        const newAnalysis = await callClaudeAI(readingsData);
        setAnalysis(newAnalysis);
        await api.saveAnalysis({
          device_id: devices[0].id,
          readings_hash: readingsData.readings_hash,
          analysis_data: newAnalysis,
          readings_count: readingsData.readings_count,
        });
        onMessage('AI analysis complete!');
      }
    } catch (error) {
      console.error('Analysis error:', error);
      onMessage('Analysis failed');
    }
    setAnalyzing(false);
  };

  if (loading) {
    return <div className="card"><p>Loading...</p></div>;
  }

  return (
    <div className="analysis">
      <div className="card">
        <div className="card-header">
          <h2>AI Energy Analysis</h2>
          <button 
            className="btn btn-primary" 
            onClick={devices.length > 0 ? runAIAnalysis : loadAnalysis}
            disabled={analyzing}
          >
            {analyzing ? 'Analyzing with AI...' : analysis ? 'Refresh' : 'Get AI Analysis'}
          </button>
        </div>

        {!analysis ? (
          <p className="empty-text">Click "Get AI Analysis" to analyze your energy data.</p>
        ) : (
          <>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">{Math.round(analysis.summary?.average_power_watts || 0)}</div>
                <div className="stat-label">Avg Power (W)</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{Math.round(analysis.summary?.peak_power_watts || 0)}</div>
                <div className="stat-label">Peak Power (W)</div>
              </div>
              <div className="stat-card">
                <div className="stat-value">{(analysis.summary?.daily_kwh || 0).toFixed(1)}</div>
                <div className="stat-label">Daily kWh</div>
              </div>
              <div className="stat-card grade">
                <div className="stat-value">{analysis.score?.grade || '--'}</div>
                <div className="stat-label">Score</div>
              </div>
            </div>

            <h3 style={{ margin: '20px 0 12px' }}>📈 Forecast</h3>
            <div className="forecast-grid">
              <div className="forecast-item">
                <div className="forecast-label">Projected Monthly</div>
                <div className="forecast-value">{analysis.forecast?.projected_monthly_kwh?.toFixed(0)} kWh</div>
                <span className={`trend ${analysis.forecast?.trend}`}>{analysis.forecast?.trend}</span>
              </div>
              <div className="forecast-item">
                <div className="forecast-label">Est. Monthly Cost</div>
                <div className="forecast-value">${analysis.forecast?.projected_monthly_cost?.toFixed(0)}</div>
              </div>
              <div className="forecast-item">
                <div className="forecast-label">Confidence</div>
                <div className="forecast-value">{analysis.forecast?.confidence}</div>
              </div>
            </div>
            <p style={{ marginTop: 12, color: '#666', fontSize: 14 }}>{analysis.forecast?.explanation}</p>

            {analysis.anomalies?.length > 0 && (
              <>
                <h3 style={{ margin: '24px 0 12px' }}>⚠️ Anomalies</h3>
                {analysis.anomalies.map((an, i) => (
                  <div key={i} className="anomaly">
                    <h3>{an.type?.toUpperCase()}: {an.description}</h3>
                    <p>{an.recommendation}</p>
                    <p className="cause">Possible cause: {an.possible_cause}</p>
                  </div>
                ))}
              </>
            )}

            <h3 style={{ margin: '24px 0 12px' }}>💡 Recommendations</h3>
            {analysis.recommendations?.map((rec, i) => (
              <div key={i} className={`recommendation ${rec.priority}`}>
                <h3>[{rec.priority?.toUpperCase()}] {rec.title}</h3>
                <p>{rec.description}</p>
                <div className="rec-meta">
                  <span>💡 Save {rec.estimated_savings_kwh} kWh/mo</span>
                  <span>💰 ${rec.estimated_savings_currency}/mo</span>
                </div>
                <div className="rec-actions">
                  {rec.actions?.map((action, j) => (
                    <span key={j} className="action-tag">{action}</span>
                  ))}
                </div>
              </div>
            ))}

            <h3 style={{ margin: '24px 0 12px' }}>📊 Score Breakdown</h3>
            <div className="card-inner">
              <p>{analysis.score?.breakdown}</p>
              <p style={{ fontSize: 48, fontWeight: 'bold', color: '#10b981', margin: '16px 0' }}>
                {analysis.score?.value || 0}/100
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
