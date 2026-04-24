import React from 'react';

const ResultCard = ({ result }) => {
  if (!result) return null;

  const isFraud = result.prediction === 1 || result.prediction === 'Fraud' || result.prediction === true;
  const score = result.anomaly_score || result.probability || 0;
  
  return (
    <div className={`glass-card p-6 rounded-2xl animate-in mt-6 border-l-4 ${isFraud ? 'border-l-red-500' : 'border-l-emerald-500'}`}>
      <h3 className="text-sm font-semibold text-slate-400 uppercase mb-4">Analysis Result</h3>
      
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${isFraud ? 'bg-red-500 animate-pulse' : 'bg-emerald-500'}`}></div>
          <span className={`text-2xl font-bold tracking-wide ${isFraud ? 'text-red-500' : 'text-emerald-500'}`}>
            {isFraud ? 'FRAUDULENT' : 'LEGITIMATE'}
          </span>
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Anomaly Score</span>
          <span className="font-mono text-white">{(score * 100).toFixed(2)}%</span>
        </div>
        <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden">
          <div 
            className={`h-2.5 rounded-full transition-all duration-1000 ${isFraud ? 'bg-red-500' : 'bg-emerald-500'}`}
            style={{ width: `${Math.min(100, Math.max(0, score * 100))}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
