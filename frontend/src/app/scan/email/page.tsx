"use client";

import { useState } from "react";
import { Mail, ShieldAlert, Sparkles, AlertCircle, CheckCircle2, ArrowRight } from "lucide-react";
import { scanEmail } from "@/lib/api";
import { ScanResult } from "@/types";
import RiskGauge from "@/components/RiskGauge";
import ThreatDrawer from "@/components/ThreatDrawer";

export default function EmailInspectorPage() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [headers, setHeaders] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState("");
  const [showDrawer, setShowDrawer] = useState(false);

  const fillPhishingSample = () => {
    setSubject("URGENT: Your Account Has Been Temporarily Suspended!");
    setBody("Dear Customer,\n\nWe detected unusual login activity on your online banking account. To prevent unauthorized access, your account has been locked.\n\nPlease verify your password immediately by clicking the link below:\nhttp://192.168.1.105/bank-security-verify/login.php\n\nIf you do not complete verification within 24 hours, your account will be permanently closed.\n\nThank you,\nSecurity Operations Team");
    setHeaders("From: support@official-bank-update.com\nReply-To: hacker@phishdomain.ru\nReturn-Path: spoofed@phishdomain.ru");
  };

  const handleScan = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!body.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await scanEmail(body.trim(), subject.trim(), headers.trim());
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to inspect email payload");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-indigo-500/20 bg-gradient-to-r from-indigo-950/20 via-slate-900 to-purple-950/20">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <Mail className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white">Email Phishing & NLP Inspector</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Analyzes social engineering triggers, urgent tone, suspicious IP links, and header domain spoofing.
            </p>
          </div>
        </div>
      </div>

      {/* Input Form */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">Email Content Payload</h2>
          <button
            type="button"
            onClick={fillPhishingSample}
            className="text-xs font-semibold text-indigo-400 hover:underline"
          >
            Load Sample Phishing Email
          </button>
        </div>

        <form onSubmit={handleScan} className="space-y-4">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Subject Line (Optional)
            </label>
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="e.g. URGENT: Action Required on Your Account"
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/60 transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Email Body Content (Required)
            </label>
            <textarea
              rows={6}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              placeholder="Paste full email body text or HTML payload here..."
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/60 font-mono transition"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-1.5">
              Raw Headers (Optional - For Sender Spoofing Audit)
            </label>
            <textarea
              rows={3}
              value={headers}
              onChange={(e) => setHeaders(e.target.value)}
              placeholder="Paste From:, Reply-To:, Return-Path: headers..."
              className="w-full bg-slate-950/80 border border-slate-800 rounded-xl p-3 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/60 font-mono transition"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !body.trim()}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 transition"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Running Email NLP Model...</span>
              </>
            ) : (
              <>
                <Mail className="w-4 h-4" />
                <span>Audit Email Safety</span>
              </>
            )}
          </button>
        </form>
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
                    <span>{result.is_phishing ? "Email Phishing Threat Flagged" : "Safe Email Payload"}</span>
                  </span>
                  <span className="text-xs font-mono text-slate-400">
                    Confidence: {result.confidence_score}%
                  </span>
                </div>

                <h3 className="text-sm font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2 mb-2">
                  <Sparkles className="w-4 h-4" />
                  <span>Gemini AI NLP Verdict</span>
                </h3>
                <p className="text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                  {result.ai_explanation.summary}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-800 mt-4 flex justify-end">
                <button
                  onClick={() => setShowDrawer(true)}
                  className="px-4 py-2 text-xs font-bold rounded-xl bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 flex items-center gap-2 transition"
                >
                  <span>View Full Threat Breakdown</span>
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
