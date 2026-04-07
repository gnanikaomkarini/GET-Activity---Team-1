export default function Results({ data, onReset }) {
  if (!data) return null;

  const { summary, wasteAnalysis, savingTips, recommendations, estimatedAfterSavings } = data;

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '#10b981';
      case 'medium': return '#f59e0b';
      case 'hard': return '#ef4444';
      default: return '#6b7280';
    }
  };

  return (
    <div className="results">
      <div className="results-header">
        <h2>Your Energy Analysis</h2>
        <button onClick={onReset} className="reset-btn">Analyze Another Home</button>
      </div>

      <div className="summary-cards">
        <div className="summary-card">
          <div className="summary-value">{summary.totalMonthlyKwh.toFixed(0)}</div>
          <div className="summary-label">kWh Used/Month</div>
        </div>
        <div className="summary-card highlight">
          <div className="summary-value">{summary.largestConsumer}</div>
          <div className="summary-label">Biggest Energy User</div>
        </div>
      </div>

      <p className="comparison-text">{summary.comparisonToAverage}</p>

      {wasteAnalysis && wasteAnalysis.length > 0 && (
        <div className="section">
          <h3>Energy Waste Found</h3>
          <div className="waste-list">
            {wasteAnalysis.map((item, idx) => (
              <div key={idx} className="waste-item">
                <div className="waste-header">
                  <span className="waste-icon">⚠️</span>
                  <span className="waste-appliance">{item.appliance}</span>
                </div>
                <p className="waste-issue">{item.issue}</p>
                <div className="waste-costs">
                  <span>Wasting {item.monthlyWasteKwh.toFixed(1)} kWh/month</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {savingTips && savingTips.length > 0 && (
        <div className="section">
          <h3>Top Saving Tips</h3>
          <div className="tips-list">
            {savingTips.map((tip, idx) => (
              <div key={idx} className="tip-item">
                <div className="tip-header">
                  <span className="tip-appliance">{tip.appliance}</span>
                  <span 
                    className="tip-difficulty" 
                    style={{ backgroundColor: getDifficultyColor(tip.difficulty) }}
                  >
                    {tip.difficulty}
                  </span>
                </div>
                <p className="tip-text">{tip.tip}</p>
                <div className="tip-savings">
                  <span>Save {tip.potentialMonthlyKwh.toFixed(1)} kWh/month</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {recommendations && recommendations.length > 0 && (
        <div className="section">
          <h3>Recommendations</h3>
          <div className="recommendations-list">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="recommendation-item">
                <div className="rec-header">
                  <h4>{rec.title}</h4>
                  <span 
                    className="rec-impact"
                    style={{ backgroundColor: getImpactColor(rec.impact) }}
                  >
                    {rec.impact} impact
                  </span>
                </div>
                <p className="rec-description">{rec.description}</p>
                <div className="rec-steps">
                  <strong>Action Steps:</strong>
                  <ol>
                    {rec.actionSteps.map((step, sIdx) => (
                      <li key={sIdx}>{step}</li>
                    ))}
                  </ol>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {estimatedAfterSavings && (
        <div className="savings-summary">
          <h3>After Following Recommendations</h3>
          <div className="savings-numbers">
            <div className="savings-stat">
              <span className="savings-value">{estimatedAfterSavings.monthlyKwh.toFixed(0)}</span>
              <span className="savings-label">kWh/month</span>
            </div>
            <div className="savings-stat highlight">
              <span className="savings-value">{estimatedAfterSavings.percentReduction.toFixed(0)}%</span>
              <span className="savings-label">reduction</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
