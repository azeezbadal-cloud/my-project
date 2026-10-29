import React from 'react';
import {GlassTint, TINTS} from './Glass';

type Props = {
  tint?: GlassTint;
  glow?: string;
  height?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
};

/** Auto-width frosted-glass pill (labels, badges). */
export const GlassChip: React.FC<Props> = ({tint = 'blue', glow, height = 62, children, style}) => {
  const c = TINTS[tint];
  return (
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 14,
        height,
        padding: `0 ${Math.round(height * 0.42)}px`,
        borderRadius: height / 2,
        background: `linear-gradient(135deg, ${c.a}, ${c.b})`,
        backdropFilter: 'blur(18px) saturate(1.7) brightness(1.05)',
        WebkitBackdropFilter: 'blur(18px) saturate(1.7) brightness(1.05)',
        border: '1.5px solid rgba(255,255,255,0.38)',
        boxShadow: `0 0 36px ${glow ?? c.glow}, 0 18px 40px -14px rgba(0,8,40,0.65), inset 0 1.5px 0 rgba(255,255,255,0.55), inset 0 0 24px rgba(150,215,255,0.12)`,
        whiteSpace: 'nowrap',
        ...style,
      }}
    >
      {children}
    </div>
  );
};
