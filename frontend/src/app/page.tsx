"use client";

import { useEffect, useState } from "react";
import { 
  ShieldAlert, ShieldCheck, Activity, AlertTriangle, 
  Link2, Mail, Globe, ArrowRight, Eye, RefreshCcw 
} from "lucide-react";
import { getDashboardStats, getScanDetail } from "@/lib/api";
import { DashboardStats, ScanResult } from "@/types";
import ThreatDrawer from "@/components/ThreatDrawer";
import Link from "next/link";
import { 
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, BarChart, Bar 
} from "recharts";

const RISK_COLORS: Record<string, string> = {
  "Safe": "#10b981",
  "Low Risk": "#eab308",
  "Medium Risk": "#f59e0b",
  "High Risk": "#ef4444",
  "Critical Threat": "#dc2626"
};

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedScan, setSelectedScan] = useState<ScanResult | null>(null);

  const fetchStats = () => {
    setLoading(true);
    getDashboardStats()
      .then(setStats)
      .catch((err) => console.error("Error fetching stats:", err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const viewScanDetails = async (id: number) => {
    try {
      const detail = await getScanDetail(id);
      setSelectedScan(detail);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-950/30 via-slate-900 to-indigo-950/20">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">
            Threat Intelligence & Analytics Dashboard
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time AI monitoring for URL, Email, and Web Content phishing vectors.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchStats}
            className="px-3.5 py-2 text-xs font-semibold rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center gap-2 transition"
          >
            <RefreshCcw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>Refresh</span>
          </button>
          <Link
            href="/scan/url"
            className="px-4 py-2 text-xs font-bold rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-500/25 flex items-center gap-2 transition"
          >
            <ShieldAlert className="w-4 h-4" />
            <span>New Scan</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="glass-card p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Total Scans Audit</p>
            <h3 className="text-3xl font-extrabold text-white mt-1 font-mono">{stats?.total_scans || 0}</h3>
            <p className="text-[11px] text-blue-400 mt-1 font-medium">Multi-vector analysis</p>
          </div>
          <div className="p-3 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <Activity className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-red-500/20 bg-red-950/10 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-red-400">Phishing Detected</p>
            <h3 className="text-3xl font-extrabold text-red-400 mt-1 font-mono">{stats?.total_phishing_detected || 0}</h3>
            <p className="text-[11px] text-red-400/80 mt-1 font-medium">{stats?.phishing_ratio || 0}% Threat Ratio</p>
          </div>
          <div className="p-3 rounded-xl bg-red-500/10 text-red-400 border border-red-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-emerald-500/20 bg-emerald-950/10 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-emerald-400">Safe Scans</p>
            <h3 className="text-3xl font-extrabold text-emerald-400 mt-1 font-mono">{stats?.total_safe_scans || 0}</h3>
            <p className="text-[11px] text-emerald-400/80 mt-1 font-medium">Verified legitimate targets</p>
          </div>
          <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
        </div>

        <div className="glass-card p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Avg Risk Score</p>
            <h3 className="text-3xl font-extrabold text-amber-400 mt-1 font-mono">{stats?.average_risk_score || 0}<span className="text-xs text-slate-500">/100</span></h3>
            <p className="text-[11px] text-slate-400 mt-1 font-medium">Composite ML index</p>
          </div>
          <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Analytics Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline Area Chart */}
        <div className="lg:col-span-2 glass-card p-6 rounded-2xl border border-slate-800">
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400" />
            <span>Scan Activity & Threat Timeline (7 Days)</span>
          </h2>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.timeline || []}>
                <defs>
                  <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorPhish" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#64748b" fontSize={12} tickLine={false} />
                <YAxis stroke="#64748b" fontSize={12} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b", borderRadius: "12px", color: "#fff", fontSize: "12px" }} 
                />
                <Area type="monotone" dataKey="total" name="Total Scans" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorTotal)" />
                <Area type="monotone" dataKey="phishing" name="Phishing Detections" stroke="#ef4444" strokeWidth={2} fillOpacity={1} fill="url(#colorPhish)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Level Distribution Pie */}
        <div className="glass-card p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-2 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Risk Level Breakdown</span>
          </h2>
          <div className="h-52 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.scans_by_risk_level || []}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {(stats?.scans_by_risk_level || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={RISK_COLORS[entry.name] || "#3b82f6"} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b", borderRadius: "12px", color: "#fff", fontSize: "12px" }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-medium pt-2 border-t border-slate-800">
            {(stats?.scans_by_risk_level || []).map((r) => (
              <div key={r.name} className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: RISK_COLORS[r.name] || "#3b82f6" }} />
                <span className="text-slate-400">{r.name}:</span>
                <span className="text-slate-200 font-bold ml-auto">{r.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Launch Scanner Hub */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Link
          href="/scan/url"
          className="glass-card p-6 rounded-2xl border border-slate-800 hover:border-blue-500/40 group transition flex items-center justify-between"
        >
          <div className="flex items-center gap-4">
            <div className="p-3.5 rounded-xl bg-blue-500/10 text-blue-400 group-hover:bg-blue-600 group-hover:text-white transition">
              <Link2 className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base">URL Scanner</h3>
              <p className="text-xs text-slate-400">Lexical & domain entropy engine</p>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-500 group-hover:text-blue-400 group-hover:translate-x-1 transition" />
        </Link>

        <Link
          href="/scan/email"
          className="glass-card p-6 rounded-2xl border border-slate-800 hover:border-indigo-500/40 group transition flex items-center justify-between"
        >
          <div className="flex items-center gap-4">
            <div className="p-3.5 rounded-xl bg-indigo-500/10 text-indigo-400 group-hover:bg-indigo-600 group-hover:text-white transition">
              <Mail className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base">Email Inspector</h3>
              <p className="text-xs text-slate-400">NLP urgency & header analysis</p>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-1 transition" />
        </Link>

        <Link
          href="/scan/website"
          className="glass-card p-6 rounded-2xl border border-slate-800 hover:border-purple-500/40 group transition flex items-center justify-between"
        >
          <div className="flex items-center gap-4">
            <div className="p-3.5 rounded-xl bg-purple-500/10 text-purple-400 group-hover:bg-purple-600 group-hover:text-white transition">
              <Globe className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-bold text-white text-base">Website Auditor</h3>
              <p className="text-xs text-slate-400">Live DOM forms & SSL inspector</p>
            </div>
          </div>
          <ArrowRight className="w-5 h-5 text-slate-500 group-hover:text-purple-400 group-hover:translate-x-1 transition" />
        </Link>
      </div>

      {/* Recent Threats Table */}
      <div className="glass-card p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-red-400" />
            <span>Recent High Risk Threats Detected</span>
          </h2>
          <Link href="/history" className="text-xs font-semibold text-blue-400 hover:underline">
            View All History →
          </Link>
        </div>

        {stats?.recent_threats && stats.recent_threats.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-3">Type</th>
                  <th className="p-3">Target Input</th>
                  <th className="p-3">Risk Level</th>
                  <th className="p-3">Score</th>
                  <th className="p-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {stats.recent_threats.map((t) => (
                  <tr key={t.id} className="hover:bg-slate-800/30 transition">
                    <td className="p-3 uppercase font-mono text-[11px] text-slate-400">
                      {t.scan_type}
                    </td>
                    <td className="p-3 max-w-xs truncate font-mono text-slate-200">
                      {t.target_input}
                    </td>
                    <td className="p-3">
                      <span className="px-2.5 py-1 rounded-full font-bold text-[10px] uppercase bg-red-500/20 text-red-400 border border-red-500/30">
                        {t.risk_level}
                      </span>
                    </td>
                    <td className="p-3 font-mono font-bold text-red-400">
                      {t.risk_score}/100
                    </td>
                    <td className="p-3 text-right">
                      <button
                        onClick={() => viewScanDetails(t.id)}
                        className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-blue-400 transition"
                        title="View Report"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-8 text-slate-400 text-xs">
            No high-risk threats logged yet. Run a scan to populate intelligence records!
          </div>
        )}
      </div>

      {/* Threat Detail Drawer */}
      <ThreatDrawer scan={selectedScan} onClose={() => setSelectedScan(null)} />
    </div>
  );
}
