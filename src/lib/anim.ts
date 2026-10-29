import {spring} from 'remotion';

export const clamp01 = (v: number) => Math.min(1, Math.max(0, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
/** 0 → 1 progress of `t` through [start, start + dur]. */
export const prog = (t: number, start: number, dur: number) => clamp01((t - start) / dur);
/** map v from [a,b] to [c,d] (clamped) */
export const remap = (v: number, a: number, b: number, c: number, d: number) => lerp(c, d, clamp01((v - a) / (b - a)));

export const easeOutCubic = (x: number) => 1 - Math.pow(1 - x, 3);
export const easeInCubic = (x: number) => x * x * x;
export const easeOutQuart = (x: number) => 1 - Math.pow(1 - x, 4);
export const easeOutQuint = (x: number) => 1 - Math.pow(1 - x, 5);
export const easeOutExpo = (x: number) => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x));
export const easeInOutCubic = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
export const easeInOutQuart = (x: number) => (x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2);
export const easeInOutSine = (x: number) => -(Math.cos(Math.PI * x) - 1) / 2;
export const easeOutBack = (x: number, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);

export type SpringCfg = {damping?: number; stiffness?: number; mass?: number};

/** Remotion spring that starts at `startSec`. 0 before it begins, settles to 1. */
export const sp = (frame: number, fps: number, startSec: number, cfg: SpringCfg = {}) =>
  spring({
    frame: frame - Math.round(startSec * fps),
    fps,
    config: {damping: 16, stiffness: 120, mass: 0.9, ...cfg},
  });

/** Soft 0→1→0 pulse centred on `centre` seconds. */
export const pulse = (t: number, centre: number, halfWidth: number) => {
  const x = Math.abs(t - centre) / halfWidth;
  return x >= 1 ? 0 : 0.5 * (1 + Math.cos(Math.PI * x));
};

/** Deterministic hash → [0,1) (so particle layouts are identical on every render). */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453123;
  return x - Math.floor(x);
};
