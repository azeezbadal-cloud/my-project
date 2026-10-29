import React from 'react';
import {colors} from '../theme';
import {easeOutCubic, prog, rand} from '../lib/anim';

const STAR = 'M0,-1 Q0.10,-0.10 1,0 Q0.10,0.10 0,1 Q-0.10,0.10 -1,0 Q-0.10,-0.10 0,-1Z';
const COLS = ['#FFFFFF', colors.goldSoft, colors.mint, colors.sky, '#FFFFFF'];

type Props = {
  t: number;
  /** burst start (s) */
  start: number;
  cx: number;
  cy: number;
  count?: number;
  /** burst radius (px) */
  radius?: number;
  /** burst duration (s) */
  dur?: number;
  seed?: number;
};

/** Celebratory sparkle burst: four-point glints that fly out, twinkle and fade, plus small glitter dots. */
export const Sparkles: React.FC<Props> = ({t, start, cx, cy, count = 22, radius = 360, dur = 1.25, seed = 1}) => {
  const p = prog(t, start, dur);
  if (p <= 0 || p >= 1) return null;
  const items = Array.from({length: count}, (_, i) => {
    const a = rand(seed * 100 + i) * Math.PI * 2;
    const d = (0.35 + rand(seed * 100 + i + 30) * 0.65) * radius;
    const delay = rand(seed * 100 + i + 60) * 0.28;
    const lp = prog(p, delay, 1 - delay);
    const e = easeOutCubic(lp);
    const size = (16 + rand(seed * 100 + i + 90) * 40) * Math.sin(Math.PI * Math.min(1, lp * 1.05));
    return {
      x: cx + Math.cos(a) * d * e,
      y: cy + Math.sin(a) * d * e * 0.7,
      size,
      rot: rand(seed * 100 + i + 120) * 90 + lp * 90,
      col: COLS[Math.floor(rand(seed * 100 + i + 150) * COLS.length)],
      star: i % 3 !== 0,
    };
  });
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
      <defs>
        <filter id="spk-glow" x="-100%" y="-100%" width="300%" height="300%">
          <feGaussianBlur stdDeviation="2.4" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g filter="url(#spk-glow)">
        {items.map((s, i) =>
          s.star ? (
            <path key={i} d={STAR} fill={s.col} transform={`translate(${s.x} ${s.y}) rotate(${s.rot}) scale(${s.size})`} />
          ) : (
            <circle key={i} cx={s.x} cy={s.y} r={Math.max(0, s.size * 0.16)} fill={s.col} />
          ),
        )}
      </g>
    </svg>
  );
};
