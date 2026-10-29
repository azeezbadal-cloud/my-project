import {SpringCfg, easeInCubic, prog, sp} from './anim';

/**
 * Horizontal "glass slide": springs in from `fromX`, later accelerates out to `toX`.
 * Also returns a small horizontal smear factor that grows with speed (cheap motion-blur look).
 */
export const slideState = (
  frame: number,
  fps: number,
  inAt: number,
  outAt: number | null,
  fromX: number,
  toX: number,
  cfg: SpringCfg = {damping: 20, stiffness: 95, mass: 1},
  outDur = 0.42,
) => {
  const at = (f: number) => {
    const t = f / fps;
    const pin = sp(f, fps, inAt, cfg);
    const out = outAt === null ? 0 : easeInCubic(prog(t, outAt, outDur));
    return (1 - pin) * fromX + out * toX;
  };
  const tx = at(frame);
  const dx = tx - at(frame - 1);
  const t = frame / fps;
  const out = outAt === null ? 0 : prog(t, outAt, outDur);
  return {
    tx,
    smear: 1 + Math.min(0.3, Math.abs(dx) / 1050),
    done: out >= 1,
    started: t >= inAt - 1 / fps,
    /** −1…1 : normalised distance from the resting position (for 3D yaw) */
    lean: Math.max(-1, Math.min(1, tx / 1100)),
  };
};

/** Mix two rgba()/hex-free colour strings of the form rgba(r,g,b,a) */
export const mixRgba = (a: [number, number, number, number], b: [number, number, number, number], t: number) => {
  const m = a.map((v, i) => v + (b[i] - v) * t);
  return `rgba(${Math.round(m[0])},${Math.round(m[1])},${Math.round(m[2])},${m[3].toFixed(3)})`;
};
