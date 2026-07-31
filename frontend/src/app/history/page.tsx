"use client";

import { useEffect, useState } from "react";
import { History, Search, Filter, Eye, Trash2, ShieldAlert, CheckCircle2, ChevronLeft, ChevronRight } from "lucide-react";
import { getScanHistory, getScanDetail, deleteScanRecord } from "@/lib/api";
import { ScanListItem, ScanResult } from "@/types";
import ThreatDrawer from "@/components/ThreatDrawer";

export default function HistoryPage() {
  const [items, setItems] = useState<ScanListItem[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [limit] = useState(15);
  const [scanType, setScanType] = useState<string>("");
  const [search, setSearch] = useState<string>("");
  const [onlyPhishing, setOnlyPhishing] = useState<boolean | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  
  const [selectedScan, setSelectedScan] = useState<ScanResult | null>(null);

  const fetchHistory = () => {
    setLoading(true);
    getScanHistory(page, limit, scanType || undefined, search || undefined, onlyPhishing)
      .then((res) => {
        setItems(res.items);
        setTotal(res.total);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, [page, scanType, onlyPhishing]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchHistory();
  };

  const handleViewDetail = async (id: number) => {
    try {
      const detail = await getScanDetail(id);
      setSelectedScan(detail);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Are you sure you want to delete this scan record?")) {
      try {
        await deleteScanRecord(id);
        fetchHistory();
      } catch (err) {
        console.error(err);
      }
    }
  };

  const totalPages = Math.ceil(total / limit) || 1;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400">
            <History className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-white">Phishing Audit History Log</h1>
            <p className="text-xs text-slate-400 mt-0.5">
              Historical intelligence database of URL, Email, and Web Content scans ({total} Total Records).
            </p>
          </div>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-card p-4 rounded-2xl border border-slate-800 flex flex-col md:flex-row gap-3 justify-between items-center">
        <form onSubmit={handleSearchSubmit} className="relative flex-1 w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by target input or domain..."
            className="w-full bg-slate-950/80 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/60 font-mono transition"
          />
        </form>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="flex items-center gap-2 bg-slate-950/80 border border-slate-800 px-3 py-1.5 rounded-xl text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={scanType}
              onChange={(e) => { setScanType(e.target.value); setPage(1); }}
              className="bg-transparent text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="" className="bg-slate-900">All Vectors</option>
              <option value="url" className="bg-slate-900">URL Scans</option>
              <option value="email" className="bg-slate-900">Email Scans</option>
              <option value="website" className="bg-slate-900">Website Audits</option>
            </select>
          </div>

          <button
            type="button"
            onClick={() => {
              setOnlyPhishing(onlyPhishing === undefined ? true : undefined);
              setPage(1);
            }}
            className={`px-3 py-2 rounded-xl text-xs font-semibold border transition ${
              onlyPhishing === true
                ? "bg-red-500/20 text-red-400 border-red-500/30"
                : "bg-slate-900 text-slate-400 border-slate-800 hover:text-white"
            }`}
          >
            Threats Only
          </button>
        </div>
      </div>

      {/* History Data Table */}
      <div className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
        {loading ? (
          <div className="py-16 text-center text-xs text-slate-400 animate-pulse">
            Loading History Records...
          </div>
        ) : items.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/90 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
                <tr>
                  <th className="p-4">ID</th>
                  <th className="p-4">Vector</th>
                  <th className="p-4">Target Input</th>
                  <th className="p-4">Verdict</th>
                  <th className="p-4">Risk Score</th>
                  <th className="p-4">Confidence</th>
                  <th className="p-4">Date / Time</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30 transition">
                    <td className="p-4 font-mono text-slate-500">#{item.id}</td>
                    <td className="p-4 uppercase font-mono text-[11px] text-slate-400">
                      {item.scan_type}
                    </td>
                    <td className="p-4 max-w-sm truncate font-mono text-slate-200">
                      {item.target_input}
                    </td>
                    <td className="p-4">
                      <span className={`px-2.5 py-1 rounded-full font-bold text-[10px] uppercase flex items-center gap-1 w-fit ${
                        item.is_phishing
                          ? "bg-red-500/20 text-red-400 border border-red-500/30"
                          : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                      }`}>
                        {item.is_phishing ? <ShieldAlert className="w-3 h-3" /> : <CheckCircle2 className="w-3 h-3" />}
                        {item.risk_level}
                      </span>
                    </td>
                    <td className="p-4 font-mono font-bold">
                      <span className={item.is_phishing ? "text-red-400" : "text-emerald-400"}>
                        {item.risk_score}/100
                      </span>
                    </td>
                    <td className="p-4 font-mono text-slate-400">
                      {item.confidence_score}%
                    </td>
                    <td className="p-4 text-slate-400 text-[11px]">
                      {new Date(item.created_at).toLocaleString()}
                    </td>
                    <td className="p-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => handleViewDetail(item.id)}
                          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-blue-400 transition"
                          title="View Full Diagnosis"
                        >
                          <Eye className="w-4 h-4" />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-red-400 transition"
                          title="Delete Record"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="py-16 text-center text-slate-400 text-xs">
            No history records match the current filters.
          </div>
        )}

        {/* Pagination Footer */}
        {totalPages > 1 && (
          <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <span>Showing Page {page} of {totalPages} ({total} Items)</span>
            <div className="flex items-center gap-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                className="p-1.5 rounded-lg bg-slate-800 disabled:opacity-40 hover:bg-slate-700 transition"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(page + 1)}
                className="p-1.5 rounded-lg bg-slate-800 disabled:opacity-40 hover:bg-slate-700 transition"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      <ThreatDrawer scan={selectedScan} onClose={() => setSelectedScan(null)} />
    </div>
  );
}
