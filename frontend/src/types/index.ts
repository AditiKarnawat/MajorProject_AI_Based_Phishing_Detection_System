export interface User {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user_id: number;
  full_name: string;
  email: string;
}

export interface IndicatorItem {
  title: string;
  severity: 'high' | 'medium' | 'low' | 'info';
  description: string;
}

export interface AIExplanation {
  summary: string;
  key_threats: string[];
  technical_analysis: string;
  recommendations: string[];
}

export interface ScanResult {
  id?: number;
  scan_type: 'url' | 'email' | 'website';
  target_input: string;
  is_phishing: boolean;
  risk_score: number;
  confidence_score: number;
  risk_level: 'Safe' | 'Low Risk' | 'Medium Risk' | 'High Risk' | 'Critical Threat';
  extracted_features: Record<string, any>;
  indicators: IndicatorItem[];
  ai_explanation: AIExplanation;
  created_at: string;
}

export interface ScanListItem {
  id: number;
  scan_type: 'url' | 'email' | 'website';
  target_input: string;
  is_phishing: boolean;
  risk_score: number;
  confidence_score: number;
  risk_level: string;
  created_at: string;
}

export interface ScanHistoryResponse {
  total: number;
  page: number;
  limit: number;
  items: ScanListItem[];
}

export interface RiskLevelCount {
  name: string;
  value: number;
}

export interface ScanTypeCount {
  name: string;
  value: number;
}

export interface TimelinePoint {
  date: string;
  total: number;
  phishing: number;
  safe: number;
}

export interface DashboardStats {
  total_scans: number;
  total_phishing_detected: number;
  total_safe_scans: number;
  phishing_ratio: number;
  average_risk_score: number;
  scans_by_type: ScanTypeCount[];
  scans_by_risk_level: RiskLevelCount[];
  timeline: TimelinePoint[];
  recent_threats: {
    id: number;
    scan_type: string;
    target_input: string;
    risk_score: number;
    risk_level: string;
    created_at: string;
  }[];
}

export interface ModelStatus {
  status: string;
  active_model: string;
  f1_score: number;
  feature_count: number;
  feature_names: string[];
  benchmark_results: Record<string, {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  }>;
}
