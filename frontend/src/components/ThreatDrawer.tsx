"use client";

import { X, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, AlertOctagon, Terminal, Lightbulb } from "lucide-react";
import { ScanResult } from "@/types";
import RiskGauge from "./RiskGauge";

interface ThreatDrawerProps {
  scan: ScanResult | null;
  onClose: () => void;
}

export default function ThreatDrawer({ scan, onClose }: ThreatDrawerProps) {
  if (!scan) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/70 backdrop-blur-sm animate-fade-in">
      <div className="w-full max-w-2xl bg-slate-900 border-l border-slate-800 h-full overflow-y-auto flex flex-col shadow-2xl">
        
        {/* Modal Header */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between sticky top-0 bg-slate-900/95 backdrop-blur z-10">
          <div className="flex items-center gap-3">
            <div className={`p-2.5 rounded-xl ${
              scan.is_phishing 
                ? "bg-red-500/10 border border-red-500/30 text-red-400" 
                : "bg-emerald-500/10 border border-emerald-500/30 text-emerald-400"
            }`}>
              {scan.is_phishing ? <ShieldAlert className="w-6 h-6" /> : <CheckCircle2 className="w-6 h-6" />}
            </div>
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <span>Threat Diagnosis Report</span>
                <span className="text-xs px-2 py-0.5 rounded-full font-semibold uppercase bg-slate-800 text-slate-300 border border-slate-700">
                  {scan.scan_type}
                </span>
              </h2>
              <p className="text-xs text-slate-400 truncate max-w-md font-mono mt-0.5">
                Target: {scan.target_input}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-xl bg-slate-800/60 hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-6 flex-1">
          
          {/* Top Gauge & Quick Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
            <div className="md:col-span-1">
              <RiskGauge 
                score={scan.risk_score} 
                level={scan.risk_level} 
                confidence={scan.confidence_score} 
              />
            </div>

            <div className="md:col-span-2 glass-card p-5 rounded-2xl border border-slate-800">
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="w-4 h-4 text-amber-400" />
                <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400">
                  Gemini AI Verdict Summary
                </h3>
              </div>
              <p className="text-sm text-slate-200 leading-relaxed">
                {scan.ai_explanation?.summary || "Analysis completed without critical anomalies."}
              </p>
            </div>
          </div>

          {/* Key Threat Indicators List */}
          {scan.indicators && scan.indicators.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
                <AlertOctagon className="w-4 h-4 text-red-400" />
                <span>Detected Threat Flags ({scan.indicators.length})</span>
              </h3>

              <div className="space-y-2.5">
                {scan.indicators.map((ind, idx) => {
                  const isHigh = ind.severity === "high";
                  const isMed = ind.severity === "medium";
                  
                  return (
                    <div
                      key={idx}
                      className={`p-3.5 rounded-xl border transition-all ${
                        isHigh
                          ? "bg-red-950/20 border-red-800/40 text-red-200"
                          : isMed
                          ? "bg-amber-950/20 border-amber-800/40 text-amber-200"
                          : "bg-slate-800/40 border-slate-700/40 text-slate-300"
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-sm flex items-center gap-2">
                          <AlertTriangle className={`w-4 h-4 ${isHigh ? "text-red-400" : "text-amber-400"}`} />
                          {ind.title}
                        </span>
                        <span className={`text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-md ${
                          isHigh ? "bg-red-500/20 text-red-400 border border-red-500/30" : "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                        }`}>
                          {ind.severity}
                        </span>
                      </div>
                      <p className="text-xs text-slate-300/80 leading-normal pl-6">
                        {ind.description}
                      </p>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Technical Analysis Section */}
          {scan.ai_explanation?.technical_analysis && (
            <div className="glass-card p-5 rounded-2xl border border-slate-800 space-y-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-blue-400 flex items-center gap-2">
                <Terminal className="w-4 h-4" />
                <span>Deep Technical Inspection</span>
              </h3>
              <p className="text-xs text-slate-300 font-mono leading-relaxed bg-slate-950/80 p-3.5 rounded-xl border border-slate-800">
                {scan.ai_explanation.technical_analysis}
              </p>
            </div>
          )}

          {/* Recommendations Action Plan */}
          {scan.ai_explanation?.recommendations && scan.ai_explanation.recommendations.length > 0 && (
            <div className="glass-card p-5 rounded-2xl border border-blue-500/20 bg-blue-950/10 space-y-3">
              <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center gap-2">
                <Lightbulb className="w-4 h-4" />
                <span>Recommended Mitigation Steps</span>
              </h3>
              <ul className="space-y-2">
                {scan.ai_explanation.recommendations.map((rec, i) => (
                  <li key={i} className="flex items-start gap-2.5 text-xs text-slate-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Extracted Features Raw Grid */}
          <div className="space-y-2 pt-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Extracted Feature Matrix
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs font-mono">
              {Object.entries(scan.extracted_features || {}).map(([key, val]) => (
                <div key={key} className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-800/80">
                  <span className="text-slate-400 text-[10px] block truncate">{key}</span>
                  <span className="text-slate-200 font-semibold">{String(val)}</span>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
