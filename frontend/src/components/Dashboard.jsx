import { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export default function Dashboard({ analysis, readings }) {
  const analysisData = analysis?.analysis;

  const chartData = {
    labels: readings.slice(-48).reverse().map(r => 
      new Date(r.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    ),
    datasets: [
      {
        label: 'Power (W)',
        data: readings.slice(-48).reverse().map(r => r.power_watts),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } },
  };

  return (
    <div className="dashboard">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{Math.round(analysisData?.summary?.average_power_watts || 0)}</div>
          <div className="stat-label">Avg Power (W)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{(analysisData?.summary?.daily_kwh || 0).toFixed(1)}</div>
          <div className="stat-label">Daily (kWh)</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${Math.round(analysisData?.summary?.monthly_cost_estimate || 0)}</div>
          <div className="stat-label">Est. Monthly</div>
        </div>
        <div className="stat-card grade">
          <div className="stat-value">{analysisData?.score?.grade || '--'}</div>
          <div className="stat-label">Energy Score</div>
        </div>
      </div>

      <div className="card">
        <h2>Energy Usage</h2>
        {readings.length > 0 ? (
          <Line data={chartData} options={chartOptions} />
        ) : (
          <p className="empty-text">No readings yet. Generate data from a device.</p>
        )}
      </div>

      <div className="card">
        <h2>Quick Recommendations</h2>
        {analysisData?.recommendations?.slice(0, 3).map((rec, i) => (
          <div key={i} className={`recommendation ${rec.priority || 'medium'}`}>
            <h3>{rec.title}</h3>
            <p>{rec.description}</p>
            <div className="rec-meta">
              <span>💡 {rec.estimated_savings_kwh} kWh</span>
              <span>💰 ${rec.estimated_savings_currency}/mo</span>
            </div>
            <div className="rec-actions">
              {rec.actions?.map((action, j) => (
                <span key={j} className="action-tag">{action}</span>
              ))}
            </div>
          </div>
        )) || <p className="empty-text">No recommendations yet.</p>}
      </div>
    </div>
  );
}
