import React from 'react';
import {clamp01, easeInCubic, easeOutQuart, lerp, prog} from '../lib/anim';

type Props = {
  text: string;
  /** current time (s) */
  t: number;
  /** time (s) the first letter starts to appear */
  start: number;
  /** delay between letters (s) */
  stagger?: number;
  /** per-letter animation length (s) */
  dur?: number;
  rise?: number;
  blur?: number;
  rotate?: number;
  popScale?: number;
  /** exit animation start (s) – letters lift away and blur out */
  outStart?: number;
  outDur?: number;
  /** 0..1 progress of a bright light sweep across the text (null = none) */
  sweep?: number | null;
  colorFrom?: string;
  colorTo?: string;
  glow?: string;
  style?: React.CSSProperties;
};

const hex = (h: string) => {
  const n = parseInt(h.replace('#', ''), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
const mix = (a: string, b: string, t: number) => {
  const A = hex(a);
  const B = hex(b);
  return `rgb(${Math.round(lerp(A[0], B[0], t))},${Math.round(lerp(A[1], B[1], t))},${Math.round(lerp(A[2], B[2], t))})`;
};

/** Cinematic per-letter reveal: letters rise, un-blur, un-rotate and scale into place; optional light sweep + exit. */
export const SplitText: React.FC<Props> = ({
  text,
  t,
  start,
  stagger = 0.03,
  dur = 0.5,
  rise = 44,
  blur = 12,
  rotate = -55,
  popScale = 0.2,
  outStart,
  outDur = 0.35,
  sweep = null,
  colorFrom = '#FFFFFF',
  colorTo = '#FFFFFF',
  glow = 'rgba(80,170,255,0.55)',
  style,
}) => {
  const chars = Array.from(text);
  const n = chars.length;
  const letters = (withAnim: boolean) =>
    chars.map((ch, i) => {
      const p = withAnim ? easeOutQuart(prog(t, start + i * stagger, dur)) : 1;
      const o = withAnim && outStart !== undefined ? easeInCubic(prog(t, outStart + i * 0.012, outDur)) : 0;
      const vis = clamp01(p * (1 - o));
      return (
        <span
          key={i}
          style={{
            display: 'inline-block',
            opacity: withAnim ? vis : 1,
            color: mix(colorFrom, colorTo, n > 1 ? i / (n - 1) : 0),
            transform: withAnim
              ? `translateY(${(1 - p) * rise - o * 34}px) rotateX(${(1 - p) * rotate}deg) scale(${1 + (1 - p) * popScale})`
              : undefined,
            transformOrigin: '50% 100%',
            filter: withAnim && (p < 0.999 || o > 0) ? `blur(${(1 - p) * blur + o * 10}px)` : undefined,
          }}
        >
          {ch === ' ' ? ' ' : ch}
        </span>
      );
    });

  const x = sweep === null ? 0 : lerp(-30, 130, sweep);
  return (
    <div style={{position: 'relative', display: 'inline-block', whiteSpace: 'pre', perspective: 900, ...style}}>
      <div style={{textShadow: `0 2px 8px rgba(0,16,64,0.55), 0 0 26px ${glow}`}}>{letters(true)}</div>
      {sweep !== null && sweep > 0 && sweep < 1 && (
        <div
          aria-hidden
          style={{
            position: 'absolute',
            inset: 0,
            color: '#fff',
            WebkitMaskImage: `linear-gradient(105deg, transparent ${x - 16}%, #000 ${x}%, transparent ${x + 16}%)`,
            maskImage: `linear-gradient(105deg, transparent ${x - 16}%, #000 ${x}%, transparent ${x + 16}%)`,
            textShadow: '0 0 14px rgba(255,255,255,0.85)',
            mixBlendMode: 'screen',
          }}
        >
          {letters(false)}
        </div>
      )}
    </div>
  );
};
