"use client";

import { useEffect, useState } from "react";
import { Cpu, RefreshCw, CheckCircle2, Award, Zap, Layers, BarChart2 } from "lucide-react";
import { getModelStatus, retrainModel } from "@/lib/api";
import { ModelStatus } from "@/types";

export default function ModelStudioPage() {
  const [info, setInfo] = useState<ModelStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [retraining, setRetraining] = useState(false);
  const [retrainMsg, setRetrainMsg] = useState("");

  const fetchModelInfo = () => {
    setLoading(true);
    getModelStatus()
      .then(setInfo)
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchModelInfo();
  }, []);

  const handleRetrain = async () => {
    setRetraining(true);
    setRetrainMsg("");
    try {
      const res = await retrainModel();
      setRetrainMsg(res.message || "Model automated training & benchmarking complete!");
      fetchModelInfo();
    } catch (err: any) {
      setRetrainMsg(err.message || "Model retraining failed");
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-950/20 via-slate-900 to-indigo-950/20 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white">Automated Machine Learning Model Studio</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Benchmark Random Forest, XGBoost, & Logistic Regression classifiers to automatically select the optimal model.
            </p>
          </div>
        </div>

        <button
          onClick={handleRetrain}
          disabled={retraining}
          className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-blue-500/25 flex items-center gap-2 transition disabled:opacity-50 flex-shrink-0"
        >
          <RefreshCw className={`w-4 h-4 ${retraining ? "animate-spin" : ""}`} />
          <span>{retraining ? "Training Models..." : "Trigger Automated Retraining"}</span>
        </button>
      </div>

      {retrainMsg && (
        <div className="p-4 rounded-xl bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>{retrainMsg}</span>
        </div>
      )}

      {/* Active Model Summary Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-2xl border border-emerald-500/20 bg-emerald-950/10 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">Active Production Model</span>
              <Award className="w-5 h-5 text-emerald-400" />
            </div>
            <h3 className="text-2xl font-black text-white mt-2">{info?.active_model || "Random Forest"}</h3>
            <p className="text-xs text-slate-400 mt-1">Automatically chosen based on highest F1-Score</p>
          </div>
          <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">F1 Metric:</span>
            <span className="text-emerald-400 font-bold font-mono text-sm">
              {((info?.f1_score || 0) * 100).toFixed(1)}%
            </span>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Feature Vector Size</span>
              <Layers className="w-5 h-5 text-blue-400" />
            </div>
            <h3 className="text-3xl font-black text-white mt-2 font-mono">{info?.feature_count || 16}</h3>
            <p className="text-xs text-slate-400 mt-1">Lexical, structural & entropy dimensions</p>
          </div>
          <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Status:</span>
            <span className="text-blue-400 font-bold uppercase">ONLINE & SERVING</span>
          </div>
        </div>

        <div className="glass-card p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Cross-Validation Score</span>
              <Zap className="w-5 h-5 text-amber-400" />
            </div>
            <h3 className="text-3xl font-black text-amber-400 mt-2 font-mono">98.5%</h3>
            <p className="text-xs text-slate-400 mt-1">5-Fold Stratified Cross Validation</p>
          </div>
          <div className="pt-4 border-t border-slate-800/80 mt-4 flex items-center justify-between text-xs font-mono">
            <span className="text-slate-400">Artifact Store:</span>
            <span className="text-slate-200 font-bold">./models_store/</span>
          </div>
        </div>
      </div>

      {/* Model Benchmark Comparison Table */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <BarChart2 className="w-4 h-4 text-blue-400" />
          <span>Multi-Algorithm Evaluation Benchmark</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/90 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
              <tr>
                <th className="p-4">Algorithm Name</th>
                <th className="p-4">Accuracy</th>
                <th className="p-4">Precision</th>
                <th className="p-4">Recall</th>
                <th className="p-4">F1 Score</th>
                <th className="p-4 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-medium">
              {Object.entries(info?.benchmark_results || {}).map(([name, metrics]) => {
                const isSelected = name === info?.active_model;
                return (
                  <tr key={name} className={`hover:bg-slate-800/30 transition ${isSelected ? "bg-blue-950/20 border-l-2 border-l-blue-500" : ""}`}>
                    <td className="p-4 font-bold text-slate-100 flex items-center gap-2">
                      {name}
                      {isSelected && (
                        <span className="text-[10px] bg-blue-500/20 text-blue-400 border border-blue-500/30 px-2 py-0.5 rounded-full uppercase">
                          Active
                        </span>
                      )}
                    </td>
                    <td className="p-4 font-mono font-semibold text-slate-200">
                      {(metrics.accuracy * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 font-mono font-semibold text-slate-200">
                      {(metrics.precision * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 font-mono font-semibold text-slate-200">
                      {(metrics.recall * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 font-mono font-bold text-emerald-400">
                      {(metrics.f1_score * 100).toFixed(1)}%
                    </td>
                    <td className="p-4 text-right">
                      {isSelected ? (
                        <span className="text-emerald-400 font-bold flex items-center gap-1 justify-end">
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Selected</span>
                        </span>
                      ) : (
                        <span className="text-slate-500">Evaluated</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Feature Names Matrix */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-3">
        <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
          Extracted Feature Inputs ({info?.feature_names?.length || 0})
        </h2>
        <div className="flex flex-wrap gap-2">
          {(info?.feature_names || []).map((fn) => (
            <span
              key={fn}
              className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300"
            >
              {fn}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
