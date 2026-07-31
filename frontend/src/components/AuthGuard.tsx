"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { getAuthToken } from "@/lib/auth";
import { ShieldAlert, RefreshCw } from "lucide-react";

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    const publicPaths = ["/login", "/register"];
    const isPublic = publicPaths.includes(pathname);
    const token = getAuthToken();

    if (!token && !isPublic) {
      setAuthorized(false);
      router.push("/login");
    } else {
      setAuthorized(true);
    }
  }, [pathname, router]);

  const isPublicPath = ["/login", "/register"].includes(pathname);

  if (authorized === null && !isPublicPath) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center gap-4">
        <div className="p-3 rounded-2xl bg-blue-600/20 text-blue-400 border border-blue-500/30 animate-pulse">
          <ShieldAlert className="w-8 h-8" />
        </div>
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-400">
          <RefreshCw className="w-4 h-4 animate-spin text-blue-400" />
          <span>Verifying Security Credentials...</span>
        </div>
      </div>
    );
  }

  if (!authorized && !isPublicPath) {
    return null;
  }

  return <>{children}</>;
}
