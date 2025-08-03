'use client';

import { useState } from 'react';
import axios from 'axios';
import { Search, Car, Loader2, AlertCircle } from 'lucide-react';

export default function Home() {
  const [vehicle1, setVehicle1] = useState('');
  const [vehicle2, setVehicle2] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!vehicle1.trim() || !vehicle2.trim()) {
      setError('Please enter both vehicle models');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/analyze-vehicles', {
        vehicle1: vehicle1.trim(),
        vehicle2: vehicle2.trim()
      }, {
        timeout: 300000 // 5 minutes timeout for AI processing
      });

      setResults(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to analyze vehicles. Please try again.';
      setError(errorMessage);
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Car className="text-indigo-600 mr-2" size={48} />
            <h1 className="text-4xl font-bold text-gray-900">Vehicle Analyst</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Compare vehicles and find current listings in Sri Lanka
          </p>
        </div>

        {/* Input Form */}
        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                First Vehicle Model
              </label>
              <input
                type="text"
                value={vehicle1}
                onChange={(e) => setVehicle1(e.target.value)}
                placeholder="e.g., Toyota Vitz"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                disabled={loading}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Second Vehicle Model
              </label>
              <input
                type="text"
                value={vehicle2}
                onChange={(e) => setVehicle2(e.target.value)}
                placeholder="e.g., Suzuki Swift"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                disabled={loading}
              />
            </div>

            {error && (
              <div className="flex items-center text-red-600 text-sm bg-red-50 p-3 rounded-md">
                <AlertCircle className="mr-2" size={16} />
                {error}
              </div>
            )}

            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin mr-2" size={20} />
                  Analyzing... (This may take a few minutes)
                </>
              ) : (
                <>
                  <Search className="mr-2" size={20} />
                  Analyze Vehicles
                </>
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        {results && (
          <div className="max-w-6xl mx-auto space-y-6">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
                <Car className="mr-2 text-indigo-600" size={24} />
                Comparison: {results.vehicle1} vs {results.vehicle2}
              </h2>
              <div className="prose max-w-none">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                    {results.comparison_report}
                  </pre>
                </div>
              </div>
              
              {results.message && (
                <div className="mt-4 text-sm text-green-600 bg-green-50 p-3 rounded-md">
                  ✓ {results.message}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}