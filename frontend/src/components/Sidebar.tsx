"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  ShieldAlert, LayoutDashboard, Link2, Mail, Globe, 
  History, Cpu, LogOut, User as UserIcon 
} from "lucide-react";
import { getAuthUser, clearAuthSession } from "@/lib/auth";
import { useEffect, useState } from "react";
import { AuthToken } from "@/types";

export default function Sidebar() {
  const pathname = usePathname();
  const [user, setUser] = useState<AuthToken | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setUser(getAuthUser());
  }, [pathname]);

  const navItems = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard },
    { name: "URL Scanner", href: "/scan/url", icon: Link2 },
    { name: "Email Inspector", href: "/scan/email", icon: Mail },
    { name: "Website Auditor", href: "/scan/website", icon: Globe },
    { name: "Scan History", href: "/history", icon: History },
    { name: "Model Studio", href: "/model", icon: Cpu },
  ];

  const handleLogout = () => {
    clearAuthSession();
    window.location.href = "/login";
  };

  return (
    <aside className="w-64 glass-panel border-r border-slate-800 flex flex-col justify-between hidden md:flex min-h-screen sticky top-0 z-40">
      <div>
        {/* Brand Header */}
        <div className="p-6 border-b border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 shadow-lg shadow-blue-500/20 text-white">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg text-white tracking-wide flex items-center gap-1.5">
              Phish<span className="text-blue-400">Guard</span> AI
            </h1>
            <p className="text-xs text-slate-400 font-medium">Enterprise Threat Intel</p>
          </div>
        </div>

        {/* Navigation List */}
        <nav className="p-4 space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 px-3.5 py-3 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? "bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? "text-blue-400" : "text-slate-400"}`} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* User Session Footer */}
      <div className="p-4 border-t border-slate-800/80">
        {!mounted ? (
          <div className="h-10 animate-pulse bg-slate-900/50 rounded-xl" />
        ) : user ? (
          <div className="bg-slate-900/70 rounded-xl p-3 border border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 font-semibold text-xs">
                {user.full_name ? user.full_name.charAt(0).toUpperCase() : "U"}
              </div>
              <div className="overflow-hidden">
                <p className="text-xs font-semibold text-slate-200 truncate">{user.full_name}</p>
                <p className="text-[10px] text-slate-400 truncate">{user.email}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              title="Logout"
              className="p-1.5 text-slate-400 hover:text-red-400 rounded-lg hover:bg-slate-800 transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="flex gap-2">
            <Link
              href="/login"
              className="flex-1 py-2 text-center text-xs font-semibold text-slate-300 bg-slate-800/60 hover:bg-slate-800 border border-slate-700 rounded-lg transition"
            >
              Sign In
            </Link>
            <Link
              href="/register"
              className="flex-1 py-2 text-center text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded-lg transition shadow-sm"
            >
              Register
            </Link>
          </div>
        )}
      </div>
    </aside>
  );
}
