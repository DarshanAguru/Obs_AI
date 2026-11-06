import React from 'react';

interface ObsAiIconProps {
  size?: number;
  className?: string;
}

export const ObsAiIcon: React.FC<ObsAiIconProps> = ({ size = 28, className = '' }) => {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`shrink-0 ${className}`}
    >
      <defs>
        <linearGradient id="obs-ai-comp-grad" x1="4" y1="4" x2="28" y2="28" gradientUnits="userSpaceOnUse">
          <stop stopColor="#38BDF8" />
          <stop offset="0.5" stopColor="#6366F1" />
          <stop offset="1" stopColor="#8B5CF6" />
        </linearGradient>
      </defs>
      <rect width="32" height="32" rx="7" fill="#090D16" />
      <rect x="0.5" y="0.5" width="31" height="31" rx="6.5" stroke="#1E2330" />
      
      {/* Observability Lens Contour */}
      <path
        d="M 5 16 C 9 9, 23 9, 27 16 C 23 23, 9 23, 5 16 Z"
        stroke="url(#obs-ai-comp-grad)"
        strokeWidth="1.8"
        strokeLinejoin="round"
      />
      
      {/* Concentric Telemetry Ring */}
      <circle cx="16" cy="16" r="5" stroke="#818CF8" strokeWidth="1" strokeDasharray="2 1.5" />
      
      {/* Central Core & AI Telemetry Nodes */}
      <circle cx="16" cy="16" r="2.5" fill="url(#obs-ai-comp-grad)" />
      <circle cx="16" cy="16" r="1" fill="#FFFFFF" />
      <circle cx="5" cy="16" r="1.5" fill="#6366F1" />
      <circle cx="27" cy="16" r="1.5" fill="#38BDF8" />
      <circle cx="16" cy="7" r="1.4" fill="#38BDF8" />
      <circle cx="16" cy="25" r="1.4" fill="#8B5CF6" />
    </svg>
  );
};

export const ObsAiLogo: React.FC<{ iconSize?: number; className?: string }> = ({
  iconSize = 28,
  className = '',
}) => {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <ObsAiIcon size={iconSize} />
      <div className="flex flex-col">
        <span className="font-bold text-sm tracking-tight text-white font-mono leading-none">
          Obs_<span className="text-sky-400">AI</span>
        </span>
        <span className="text-[10px] text-slate-400 font-mono leading-none mt-1">AI Observability</span>
      </div>
    </div>
  );
};

// Backward-compatibility export
export const AiObsIcon = ObsAiIcon;
export const AiObsLogo = ObsAiLogo;
