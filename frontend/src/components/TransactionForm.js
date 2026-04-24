import React, { useState } from 'react';

const TransactionForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    scaled_amount: 100,
    scaled_time: 0,
    V1: 0,
    V2: 0,
    V3: 0,
    V4: 0,
    V5: 0,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: parseFloat(value) });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const Slider = ({ name, label, min = -5, max = 5, step = 0.1 }) => (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <label className="text-sm font-medium text-slate-400">{label}</label>
        <span className="text-xs font-mono text-emerald-400">{formData[name].toFixed(2)}</span>
      </div>
      <input
        type="range"
        name={name}
        min={min}
        max={max}
        step={step}
        value={formData[name]}
        onChange={handleChange}
        className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
      />
    </div>
  );

  return (
    <div className="glass-card p-6 rounded-2xl animate-in">
      <h2 className="text-xl font-semibold mb-6 text-white flex items-center gap-2">
        <span className="p-2 bg-emerald-500/10 rounded-lg">
          <svg className="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </span>
        New Transaction
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-xs font-medium text-slate-500 uppercase mb-2">Amount ($)</label>
            <input
              type="number"
              name="scaled_amount"
              value={formData.scaled_amount}
              onChange={handleChange}
              className="w-full bg-slate-900/50 border border-white/5 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 text-slate-100 transition-all"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-slate-500 uppercase mb-2">Time (Sec)</label>
            <input
              type="number"
              name="scaled_time"
              value={formData.scaled_time}
              onChange={handleChange}
              className="w-full bg-slate-900/50 border border-white/5 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 text-slate-100 transition-all"
            />
          </div>
        </div>

        <div className="space-y-2">
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4">PCA Features (V1-V5)</h3>
          <Slider name="V1" label="V1 (Principal Component 1)" />
          <Slider name="V2" label="V2 (Principal Component 2)" />
          <Slider name="V3" label="V3 (Principal Component 3)" />
          <Slider name="V4" label="V4 (Principal Component 4)" />
          <Slider name="V5" label="V5 (Principal Component 5)" />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full mt-8 py-4 rounded-xl font-bold uppercase tracking-widest text-sm transition-all flex items-center justify-center gap-2 ${
            loading 
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed' 
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/20 active:scale-[0.98]'
          }`}
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-slate-400 border-t-transparent rounded-full animate-spin"></div>
              Analyzing...
            </>
          ) : (
            'Validate Transaction'
          )}
        </button>
      </form>
    </div>
  );
};

export default TransactionForm;
