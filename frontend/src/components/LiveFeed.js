import React from 'react';

const LiveFeed = ({ transactions }) => {
  return (
    <div className="glass-card p-6 rounded-2xl animate-in mt-6 overflow-hidden flex flex-col h-full">
      <h3 className="text-sm font-semibold text-slate-400 uppercase mb-4 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        Live Feed (Last 10)
      </h3>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-white/5 text-slate-500">
              <th className="pb-3 font-medium">Time</th>
              <th className="pb-3 font-medium">Amount</th>
              <th className="pb-3 font-medium">Score</th>
              <th className="pb-3 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {transactions.length === 0 ? (
              <tr>
                <td colSpan="4" className="py-8 text-center text-slate-500">
                  No transactions yet.
                </td>
              </tr>
            ) : (
              transactions.map((tx, index) => {
                const isFraud = tx.prediction === 1 || tx.prediction === 'Fraud' || tx.prediction === true;
                const score = tx.anomaly_score || tx.probability || 0;
                
                return (
                  <tr key={index} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                    <td className="py-3 font-mono text-slate-400">{tx.scaled_time}s</td>
                    <td className="py-3 font-mono text-slate-200">${tx.scaled_amount.toFixed(2)}</td>
                    <td className="py-3 font-mono">
                      <span className={score > 0.5 ? 'text-red-400' : 'text-emerald-400'}>
                        {(score * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="py-3">
                      <span className={`px-2 py-1 text-xs rounded-md font-medium ${
                        isFraud ? 'bg-red-500/20 text-red-400 border border-red-500/20' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
                      }`}>
                        {isFraud ? 'Fraud' : 'Legit'}
                      </span>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LiveFeed;
