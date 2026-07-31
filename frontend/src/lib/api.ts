import { getAuthToken } from "./auth";
import {
  ScanResult, ScanHistoryResponse, DashboardStats, ModelStatus, AuthToken, User
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Network request failed" }));
    throw new Error(errorData.detail || `Error ${res.status}: ${res.statusText}`);
  }

  return res.json();
}

// Authentication APIs
export async function registerUser(fullName: string, email: string, password: str): Promise<AuthToken> {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ full_name: fullName, email, password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Registration failed" }));
    throw new Error(err.detail || "Registration failed");
  }
  return res.json();
}

export async function loginUser(email: string, password: str): Promise<AuthToken> {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail || "Invalid email or password");
  }
  return res.json();
}

export async function getCurrentUserProfile(): Promise<User> {
  return fetchWithAuth("/auth/me");
}

// Scanning APIs
export async function scanUrl(url: string): Promise<ScanResult> {
  return fetchWithAuth("/scan/url", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
}

export async function scanEmail(body: string, subject?: string, headers?: string): Promise<ScanResult> {
  return fetchWithAuth("/scan/email", {
    method: "POST",
    body: JSON.stringify({ body, subject, headers }),
  });
}

export async function scanWebsite(url: string): Promise<ScanResult> {
  return fetchWithAuth("/scan/website", {
    method: "POST",
    body: JSON.stringify({ url }),
  });
}

// History & Detail APIs
export async function getScanHistory(
  page = 1,
  limit = 20,
  scanType?: string,
  search?: string,
  onlyPhishing?: boolean
): Promise<ScanHistoryResponse> {
  const params = new URLSearchParams();
  params.append("page", page.toString());
  params.append("limit", limit.toString());
  if (scanType) params.append("scan_type", scanType);
  if (search) params.append("search", search);
  if (onlyPhishing !== undefined) params.append("only_phishing", onlyPhishing.toString());

  return fetchWithAuth(`/history?${params.toString()}`);
}

export async function getScanDetail(id: number): Promise<ScanResult> {
  return fetchWithAuth(`/history/${id}`);
}

export async function deleteScanRecord(id: number): Promise<void> {
  return fetchWithAuth(`/history/${id}`, { method: "DELETE" });
}

// Analytics APIs
export async function getDashboardStats(): Promise<DashboardStats> {
  return fetchWithAuth("/stats/dashboard");
}

// ML Model Management APIs
export async function getModelStatus(): Promise<ModelStatus> {
  return fetchWithAuth("/model/status");
}

export async function retrainModel(): Promise<{ message: string; details: any }> {
  return fetchWithAuth("/model/retrain", { method: "POST" });
}
