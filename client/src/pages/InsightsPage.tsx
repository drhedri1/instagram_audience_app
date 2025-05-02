import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface InsightsResponse {
  insights: string[];
}

const InsightsPage: React.FC = () => {
  const [insights, setInsights] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchInsights = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get<InsightsResponse>('/api/insights/');
        setInsights(response.data.insights);
      } catch (err: any) {
        console.error("Error fetching insights:", err);
        setError(err.response?.data?.error || err.message || "Failed to fetch insights");
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, []);

  return (
    <div>
      <h2>Actionable Insights</h2>
      <p>Here are some insights based on your audience data to help guide your content strategy:</p>
      {loading && <p>Loading insights...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {insights.length > 0 ? (
        <ul style={{ listStyleType: 'disc', marginLeft: '2rem' }}>
          {insights.map((insight, index) => (
            <li key={index} style={{ marginBottom: '0.5rem' }}>{insight}</li>
          ))}
        </ul>
      ) : (
        !loading && !error && <p>No insights available.</p>
      )}
    </div>
  );
};

export default InsightsPage;

