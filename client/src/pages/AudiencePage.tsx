import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AudiencePage: React.FC = () => {
  const [audienceData, setAudienceData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAudienceData = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get('/api/audience/');
        setAudienceData(response.data);
      } catch (err: any) {
        console.error("Error fetching audience data:", err);
        setError(err.response?.data?.error || err.message || "Failed to fetch audience data");
      } finally {
        setLoading(false);
      }
    };

    fetchAudienceData();
  }, []);

  return (
    <div>
      <h2>Audience Analysis</h2>
      {loading && <p>Loading audience data...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {audienceData && (
        <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '5px', whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
          {JSON.stringify(audienceData, null, 2)}
        </pre>
      )}
      {/* More detailed visualization components will go here */}
    </div>
  );
};

export default AudiencePage;

