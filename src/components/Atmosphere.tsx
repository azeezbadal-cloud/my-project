import React, {useEffect, useRef} from 'react';
import {colors} from '../theme';
import {rand} from '../lib/anim';

/**
 * Cinematic atmosphere drawn on a canvas (half resolution, scaled up – the glows are soft anyway):
 * drifting colour blooms, long light streaks, twinkling particles and bokeh discs.
 * Fully deterministic: the same frame always paints the same pixels.
 */
const CW = 540;
const CH = 960;

const PALETTE = [colors.brightBlue, colors.sky, colors.mint, colors.emerald, '#FFFFFF', colors.goldSoft];

const rgba = (hex: string, a: number) => {
  const n = parseInt(hex.replace('#', ''), 16);
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
};

type Props = {t: number; intensity?: number; style?: React.CSSProperties};

export const Atmosphere: React.FC<Props> = ({t, intensity = 1, style}) => {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const cv = ref.current;
    if (!cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, CW, CH);
    ctx.globalCompositeOperation = 'lighter';

    // 1 ─ colour blooms
    const blooms = [
      {x: 0.16, y: 0.2, r: 330, c: colors.brightBlue, a: 0.2, sp: 0.07},
      {x: 0.86, y: 0.34, r: 300, c: colors.emerald, a: 0.15, sp: 0.09},
      {x: 0.5, y: 0.7, r: 380, c: colors.navyMid, a: 0.28, sp: 0.05},
    ];
    blooms.forEach((b, i) => {
      const cx = (b.x + Math.sin(t * b.sp * 6.28 + i * 2) * 0.08) * CW;
      const cy = (b.y + Math.cos(t * b.sp * 6.28 + i) * 0.06) * CH;
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, b.r);
      g.addColorStop(0, rgba(b.c, b.a * intensity));
      g.addColorStop(1, rgba(b.c, 0));
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, CW, CH);
    });

    // 2 ─ light streaks (diagonal, drifting up-right)
    const ang = (-62 * Math.PI) / 180;
    const dx = Math.cos(ang);
    const dy = Math.sin(ang);
    for (let i = 0; i < 11; i++) {
      const speed = 0.05 + rand(i + 1) * 0.07;
      const phase = rand(i + 40);
      const p = (t * speed + phase) % 1;
      const len = 260 + rand(i + 9) * 520;
      const px = -0.3 * CW + rand(i + 20) * 1.6 * CW;
      const py = CH * (1.15 - p * 1.5);
      const cx = px + (p - 0.5) * 160;
      const col = PALETTE[Math.floor(rand(i + 60) * 4)];
      const a = Math.pow(Math.sin(Math.PI * p), 2) * (0.5 + rand(i + 3) * 0.45) * intensity;
      const x0 = cx - (dx * len) / 2;
      const y0 = py - (dy * len) / 2;
      const x1 = cx + (dx * len) / 2;
      const y1 = py + (dy * len) / 2;
      const g = ctx.createLinearGradient(x0, y0, x1, y1);
      g.addColorStop(0, rgba(col, 0));
      g.addColorStop(0.5, rgba(col, a));
      g.addColorStop(1, rgba(col, 0));
      ctx.strokeStyle = g;
      ctx.lineCap = 'round';
      ctx.lineWidth = 1.2 + rand(i + 77) * 3.2;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
      // soft wide halo of the same streak
      ctx.lineWidth = 8 + rand(i + 5) * 8;
      const g2 = ctx.createLinearGradient(x0, y0, x1, y1);
      g2.addColorStop(0, rgba(col, 0));
      g2.addColorStop(0.5, rgba(col, a * 0.22));
      g2.addColorStop(1, rgba(col, 0));
      ctx.strokeStyle = g2;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
    }

    // 3 ─ particles
    for (let i = 0; i < 130; i++) {
      const depth = 0.35 + rand(i + 100) * 0.65;
      const x0 = rand(i + 200) * CW;
      const y0 = rand(i + 300) * CH;
      const vy = (6 + rand(i + 400) * 16) * depth;
      const y = (((y0 - t * vy) % CH) + CH) % CH;
      const x = x0 + Math.sin(t * (0.4 + rand(i + 500)) + i) * 9 * depth;
      const tw = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * (1.2 + rand(i + 600) * 2.4) + i * 3.1));
      const r = (0.9 + rand(i + 700) * 2.4) * depth;
      const col = PALETTE[Math.floor(rand(i + 800) * PALETTE.length)];
      const g = ctx.createRadialGradient(x, y, 0, x, y, r * 3.2);
      g.addColorStop(0, rgba(col, 0.95 * tw * intensity));
      g.addColorStop(0.35, rgba(col, 0.35 * tw * intensity));
      g.addColorStop(1, rgba(col, 0));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, r * 3.2, 0, Math.PI * 2);
      ctx.fill();
    }

    // 4 ─ bokeh discs
    for (let i = 0; i < 9; i++) {
      const r = 14 + rand(i + 900) * 30;
      const x = (rand(i + 910) + Math.sin(t * 0.12 + i) * 0.03) * CW;
      const y = (((rand(i + 920) * CH - t * (4 + rand(i + 930) * 6)) % CH) + CH) % CH;
      const col = PALETTE[Math.floor(rand(i + 940) * 5)];
      const g = ctx.createRadialGradient(x, y, r * 0.55, x, y, r);
      g.addColorStop(0, rgba(col, 0.04 * intensity));
      g.addColorStop(0.85, rgba(col, 0.12 * intensity));
      g.addColorStop(1, rgba(col, 0));
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
    }
  }, [t, intensity]);

  return (
    <canvas
      ref={ref}
      width={CW}
      height={CH}
      style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 1920, mixBlendMode: 'screen', ...style}}
    />
  );
};
