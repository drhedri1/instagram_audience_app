import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ReportSummary {
  id: number;
  report_name: string;
  generation_date: string;
}

interface ReportDetails extends ReportSummary {
  report_data: any; // Adjust type based on actual report structure
}

const ReportsPage: React.FC = () => {
  const [reports, setReports] = useState<ReportSummary[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportDetails | null>(null);
  const [loadingList, setLoadingList] = useState<boolean>(true);
  const [loadingDetails, setLoadingDetails] = useState<boolean>(false);
  const [generating, setGenerating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async () => {
    setLoadingList(true);
    setError(null);
    try {
      const response = await axios.get<ReportSummary[]>('/api/reports/');
      setReports(response.data);
    } catch (err: any) {
      console.error("Error fetching reports:", err);
      setError(err.response?.data?.error || err.message || "Failed to fetch reports list");
    } finally {
      setLoadingList(false);
    }
  };

  const fetchReportDetails = async (reportId: number) => {
    setLoadingDetails(true);
    setSelectedReport(null); // Clear previous selection
    setError(null);
    try {
      const response = await axios.get<ReportDetails>(`/api/reports/${reportId}`);
      setSelectedReport(response.data);
    } catch (err: any) {
      console.error("Error fetching report details:", err);
      setError(err.response?.data?.error || err.message || "Failed to fetch report details");
    } finally {
      setLoadingDetails(false);
    }
  };

  const handleGenerateReport = async () => {
    setGenerating(true);
    setError(null);
    try {
      const response = await axios.post('/api/reports/');
      alert(`Report '${response.data.report_name}' generated successfully!`);
      // Refresh the list of reports
      fetchReports();
    } catch (err: any) {
      console.error("Error generating report:", err);
      setError(err.response?.data?.error || err.message || "Failed to generate report");
      alert(`Error generating report: ${err.response?.data?.error || err.message}`);
    } finally {
      setGenerating(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  return (
    <div>
      <h2>Reports</h2>
      <button onClick={handleGenerateReport} disabled={generating}>
        {generating ? 'Generating...' : 'Generate New Audience Report'}
      </button>
      {error && <p style={{ color: 'red', marginTop: '1rem' }}>Error: {error}</p>}

      <h3 style={{ marginTop: '2rem' }}>Generated Reports</h3>
      {loadingList ? (
        <p>Loading reports list...</p>
      ) : reports.length > 0 ? (
        <ul>
          {reports.map((report) => (
            <li key={report.id} style={{ marginBottom: '0.5rem' }}>
              {report.report_name} ({new Date(report.generation_date).toLocaleString()}){' '}
              <button onClick={() => fetchReportDetails(report.id)} disabled={loadingDetails}>
                {loadingDetails && selectedReport?.id !== report.id ? 'Loading...' : 'View Details'}
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No reports generated yet.</p>
      )}

      {loadingDetails && <p>Loading report details...</p>}
      {selectedReport && (
        <div style={{ marginTop: '2rem', border: '1px solid #eee', padding: '1rem' }}>
          <h4>Report Details: {selectedReport.report_name}</h4>
          <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: '5px', whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
            {JSON.stringify(selectedReport.report_data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ReportsPage;

