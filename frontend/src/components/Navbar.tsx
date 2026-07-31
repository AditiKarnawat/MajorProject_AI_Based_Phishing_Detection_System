"use client";

import { useEffect, useState } from "react";
import { ShieldCheck, Cpu, RefreshCw } from "lucide-react";
import { getModelStatus } from "@/lib/api";
import { ModelStatus } from "@/types";

export default function Navbar() {
  const [modelInfo, setModelInfo] = useState<ModelStatus | null>(null);

  useEffect(() => {
    getModelStatus()
      .then(setModelInfo)
      .catch(() => setModelInfo(null));
  }, []);

  return (
    <header className="h-16 glass-panel border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <span className="flex h-2.5 w-2.5 relative">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
        </span>
        <span className="text-xs font-semibold text-slate-300 tracking-wide uppercase">
          AI Protection Engine Active
        </span>
      </div>

      <div className="flex items-center gap-4">
        {modelInfo ? (
          <div className="flex items-center gap-2 bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-lg text-xs">
            <Cpu className="w-3.5 h-3.5 text-blue-400" />
            <span className="text-slate-400">Model:</span>
            <span className="font-semibold text-slate-200">{modelInfo.active_model}</span>
            <span className="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono font-medium">
              F1: {(modelInfo.f1_score * 100).toFixed(1)}%
            </span>
          </div>
        ) : (
          <div className="flex items-center gap-1.5 text-xs text-slate-400 animate-pulse">
            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
            <span>Connecting ML Engine...</span>
          </div>
        )}

        <div className="flex items-center gap-1.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1.5 rounded-lg text-xs font-semibold">
          <ShieldCheck className="w-4 h-4" />
          <span>Gemini AI Connected</span>
        </div>
      </div>
    </header>
  );
}
