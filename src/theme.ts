import {AccentName, config} from './config';

export const colors = config.colors;
export const fonts = {
  display: `'${config.fonts.display}', 'Inter', system-ui, sans-serif`,
  body: `'${config.fonts.body}', 'Inter', system-ui, sans-serif`,
};

export const W = config.width;
export const H = config.height;
export const FPS = config.fps;

export const safe = config.safe;
export const contentW = W - safe.left - safe.right;

/** Top band used by the first three scenes (sits above the speaker's head). */
export const band = {x: safe.left, y: safe.top - 14, w: contentW, h: 214};

export const accent = (name: AccentName) => {
  switch (name) {
    case 'green':
      return {main: colors.emerald, soft: colors.mint, glow: 'rgba(16,185,129,0.55)'};
    case 'aqua':
      return {main: '#22D3EE', soft: '#A5F3FC', glow: 'rgba(34,211,238,0.5)'};
    case 'gold':
      return {main: colors.gold, soft: colors.goldSoft, glow: 'rgba(248,176,0,0.5)'};
    default:
      return {main: colors.brightBlue, soft: colors.sky, glow: 'rgba(45,156,255,0.55)'};
  }
};

/** Geometry of the floating video window used from the map onwards. */
export const windowGeom = (progress: number) => {
  const target = config.window.scale;
  const s = 1 + (target - 1) * progress;
  const bottom = config.window.bottom * progress;
  const w = W * s;
  const h = H * s;
  return {s, w, h, left: (W - w) / 2, top: H - bottom - h, radius: config.window.radius * progress};
};
