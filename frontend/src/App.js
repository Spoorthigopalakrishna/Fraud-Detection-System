import React, { useState } from 'react';
import { predictTransaction } from './services/api';
import TransactionForm from './components/TransactionForm';
import ResultCard from './components/ResultCard';
import LiveFeed from './components/LiveFeed';
import Dashboard from './components/Dashboard';

function App() {
  const [stats, setStats] = useState({ legit: 0, fraud: 0 });
  const [history, setHistory] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [currentResult, setCurrentResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTransactionSubmit = async (formData) => {
    setLoading(true);
    try {
      const result = await predictTransaction(formData); 

      // Support various backend formats natively (e.g. { prediction: 1, anomaly_score: 0.99 } or { prediction: "Fraud", probability: 0.99 })
      const isFraud = result.prediction === 1 || result.prediction === 'Fraud' || result.prediction === true;
      const score = result.anomaly_score !== undefined ? result.anomaly_score : (result.probability !== undefined ? result.probability : (isFraud ? 1 : 0));

      const standardResult = { ...result, prediction: isFraud ? 1 : 0, anomaly_score: score };

      setCurrentResult(standardResult);

      setStats(prev => ({
        legit: prev.legit + (isFraud ? 0 : 1),
        fraud: prev.fraud + (isFraud ? 1 : 0),
      }));

      const now = new Date();
      const timeString = now.toLocaleTimeString([], { hour12: false });
      
      setHistory(prev => {
        const newHistory = [...prev, { time: timeString, score: score }];
        if (newHistory.length > 20) newHistory.shift(); // keep last 20 points for chart
        return newHistory;
      });

      setTransactions(prev => {
        const newTx = [{ ...formData, ...standardResult, timestamp: timeString }, ...prev];
        if (newTx.length > 10) newTx.pop(); // limit to 10 rows
        return newTx;
      });
      
    } catch (error) {
      console.error('Error fetching prediction:', error);
      alert('Error connecting to backend: ' + error.message + '. Make sure the Flask API is running on http://localhost:5000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      <header className="mb-8 animate-in text-center md:text-left">
        <h1 className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-400">
          NexusGuard Fraud Detection
        </h1>
        <p className="text-slate-400 mt-2">Real-time transaction analysis powered by AI</p>
      </header>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-6">
        {/* Left Column: Form & Result */}
        <div className="xl:col-span-4 flex flex-col h-full">
          <TransactionForm onSubmit={handleTransactionSubmit} loading={loading} />
          <ResultCard result={currentResult} />
        </div>

        {/* Right Column: Dashboard & Feed */}
        <div className="xl:col-span-8 flex flex-col gap-6">
          <Dashboard stats={stats} history={history} />
          <div className="flex-1">
            <LiveFeed transactions={transactions} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
