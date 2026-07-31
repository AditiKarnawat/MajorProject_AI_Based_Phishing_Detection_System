import { AuthToken } from "@/types";

const TOKEN_KEY = "phishguard_auth_token";
const USER_KEY = "phishguard_user_data";

export function saveAuthSession(data: AuthToken) {
  if (typeof window !== "undefined") {
    localStorage.setItem(TOKEN_KEY, data.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(data));
  }
}

export function getAuthToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

export function getAuthUser(): AuthToken | null {
  if (typeof window !== "undefined") {
    const raw = localStorage.getItem(USER_KEY);
    if (raw) {
      try {
        return JSON.parse(raw);
      } catch {
        return null;
      }
    }
  }
  return null;
}

export function clearAuthSession() {
  if (typeof window !== "undefined") {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }
}
