"use client";

import { useState } from "react";
import { Globe, ShieldAlert, Sparkles, AlertCircle, CheckCircle2, ArrowRight } from "lucide-react";
import { scanWebsite } from "@/lib/api";
import { ScanResult } from "@/types";
import RiskGauge from "@/components/RiskGauge";
import ThreatDrawer from "@/components/ThreatDrawer";

export default function WebsiteAuditorPage() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState("");
  const [showDrawer, setShowDrawer] = useState(false);

  const sampleTargets = [
    "http://192.168.1.1/paypal-security-update-verify-account.login.php",
    "https://www.google.com"
  ];

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await scanWebsite(url.trim());
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to audit website content");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-purple-500/20 bg-gradient-to-r from-purple-950/20 via-slate-900 to-indigo-950/20">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-purple-600/20 border border-purple-500/30 text-purple-400">
            <Globe className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white">Live Website DOM & SSL Auditor</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Performs live HTML fetching to inspect form actions, password fields over HTTP, iframe overlays, and brand clone spoofing.
            </p>
          </div>
        </div>
      </div>

      {/* Input Form */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <form onSubmit={handleScan} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Globe className="w-5 h-5 text-slate-500 absolute left-4 top-3.5" />
            <input
              type="text"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Enter live website URL (e.g. https://example.com)..."
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-12 pr-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/60 font-mono transition"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !url.trim()}
            className="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-purple-500/25 flex items-center justify-center gap-2 transition flex-shrink-0"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Auditing Live Web Page DOM...</span>
              </>
            ) : (
              <>
                <Globe className="w-4 h-4" />
                <span>Audit Web Content</span>
              </>
            )}
          </button>
        </form>

        <div className="flex items-center gap-2 pt-2 border-t border-slate-800/60 text-xs">
          <span className="text-slate-400 font-semibold">Test Targets:</span>
          {sampleTargets.map((sample, i) => (
            <button
              key={i}
              onClick={() => setUrl(sample)}
              className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 font-mono text-[11px] truncate max-w-xs transition"
            >
              {sample}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-semibold flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6 animate-fade-in">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              <RiskGauge
                score={result.risk_score}
                level={result.risk_level}
                confidence={result.confidence_score}
              />
            </div>

            <div className="md:col-span-2 glass-card p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className={`px-3 py-1 rounded-full text-xs font-extrabold uppercase tracking-wider flex items-center gap-1.5 ${
                    result.is_phishing
                      ? "bg-red-500/20 text-red-400 border border-red-500/30"
                      : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                  }`}>
                    {result.is_phishing ? <ShieldAlert className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
                    <span>{result.is_phishing ? "Web Page Flagged Malicious" : "Clean Web Page Structure"}</span>
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    Confidence: {result.confidence_score}%
                  </span>
                </div>

                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2 mb-2">
                  <Sparkles className="w-4 h-4" />
                  <span>Gemini AI Web Audit Summary</span>
                </h3>
                <p className="text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                  {result.ai_explanation.summary}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-800 mt-4 flex justify-end">
                <button
                  onClick={() => setShowDrawer(true)}
                  className="px-4 py-2 text-xs font-bold rounded-xl bg-purple-600/20 hover:bg-purple-600/30 text-purple-400 border border-purple-500/30 flex items-center gap-2 transition"
                >
                  <span>View DOM & SSL Report</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <ThreatDrawer
        scan={showDrawer ? result : null}
        onClose={() => setShowDrawer(false)}
      />
    </div>
  );
}
