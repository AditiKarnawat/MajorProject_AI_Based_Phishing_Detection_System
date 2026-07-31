"use client";

interface RiskGaugeProps {
  score: number;
  level: string;
  confidence: number;
}

export default function RiskGauge({ score, level, confidence }: RiskGaugeProps) {
  // Score range 0-100
  const normalizedScore = Math.min(100, Math.max(0, score));
  
  // Dynamic color palette
  let color = "#10b981"; // Emerald
  let bgGlow = "rgba(16, 185, 129, 0.25)";
  
  if (normalizedScore >= 88) {
    color = "#dc2626"; // Crimson
    bgGlow = "rgba(220, 38, 38, 0.4)";
  } else if (normalizedScore >= 70) {
    color = "#ef4444"; // Red
    bgGlow = "rgba(239, 68, 68, 0.35)";
  } else if (normalizedScore >= 45) {
    color = "#f59e0b"; // Amber
    bgGlow = "rgba(245, 158, 11, 0.3)";
  } else if (normalizedScore >= 20) {
    color = "#eab308"; // Yellow
    bgGlow = "rgba(234, 179, 8, 0.25)";
  }

  // SVG Gauge Calculations
  const radius = 70;
  const strokeWidth = 14;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 glass-panel rounded-2xl relative overflow-hidden">
      {/* Background radial glow */}
      <div 
        className="absolute inset-0 opacity-20 pointer-events-none transition-all duration-500 blur-2xl"
        style={{ background: bgGlow }}
      />

      <div className="relative w-44 h-44 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
          {/* Track Circle */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="#1e293b"
            strokeWidth={strokeWidth}
            fill="transparent"
          />
          {/* Dynamic Progress Circle */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke={color}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        {/* Center Score Readout */}
        <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
          <span className="text-4xl font-extrabold tracking-tight text-white font-mono">
            {normalizedScore}
          </span>
          <span className="text-[11px] font-bold tracking-widest uppercase text-slate-400 mt-0.5">
            Risk Score
          </span>
        </div>
      </div>

      {/* Threat Level Badge */}
      <div className="mt-4 flex flex-col items-center">
        <span 
          className="px-4 py-1.5 rounded-full text-xs font-extrabold uppercase tracking-wider shadow-lg transition-colors"
          style={{ 
            backgroundColor: `${color}20`,
            color: color,
            border: `1px solid ${color}40`
          }}
        >
          {level}
        </span>
        <p className="text-xs text-slate-400 font-medium mt-2">
          Model Confidence: <span className="text-slate-200 font-semibold">{confidence}%</span>
        </p>
      </div>
    </div>
  );
}
