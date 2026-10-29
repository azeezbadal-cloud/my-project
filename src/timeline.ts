/**
 * Pure timing data (no React) – imported by the scenes AND by the audio generator so that
 * every sound effect lands on the same frame as the animation it belongs to.
 * All numbers are seconds. Scene start/end times come from src/config.ts.
 */
import {config} from './config';

const w0 = config.welcome.start;
const o0 = config.open.start;
const s0 = config.services.start;
const e0 = config.expansion.start;
const u0 = config.outro.start;

export const serviceTimes = () => {
  const n = config.services.items.length;
  const start = s0 + config.services.headingSeconds;
  const d = (config.services.end - start) / n;
  return {n, start, d, enter: (k: number) => start + k * d};
};

export const cityTimes = (k: number) => {
  const c = config.expansion.cityStart + k * config.expansion.cityStep;
  return {arc: c, land: c + 0.5, label: c + 0.42};
};

export const TL = {
  welcome: {
    panelIn: w0 + 0.0,
    eyebrow: w0 + 0.4,
    eyebrowOut: w0 + 1.55,
    title: w0 + 1.7,
    sweep: w0 + 2.25,
    panelOut: w0 + 2.82,
  },
  open: {
    panelIn: o0 + 0.05,
    headline: o0 + 0.28,
    sparkle: o0 + 0.95,
    subline: o0 + 1.15,
    panelOut: o0 + 2.68,
  },
  services: {
    headingIn: s0 + 0.05,
    headingOut: s0 + 1.22,
  },
  expansion: {
    shrink: e0,
    kicker: e0 + 0.35,
    kickerOut: e0 + 1.1,
    mapIn: e0 + 0.55,
    homePin: e0 + 0.85,
    /** the moment the Wagga Wagga pin touches the map */
    homeLand: e0 + 1.3,
    zoom: e0 + 1.3,
    next: e0 + 1.5,
    badge: e0 + 1.75,
    exit: config.expansion.end - 0.25,
  },
  outro: {
    bloom: u0,
    emblem: u0 + 0.15,
    wordmark: u0 + 0.7,
    tagline: u0 + 1.1,
    goals: u0 + 1.55,
    cta: u0 + 2.1,
    fade: config.outro.end - 0.5,
  },
};

export type CueKind = 'glass' | 'whoosh' | 'pulse' | 'impact' | 'sparkle' | 'riser' | 'logo' | 'shimmer' | 'ping';
export type Cue = {t: number; kind: CueKind; gain?: number; pan?: number; pitch?: number; dur?: number};

/** Sound-effect cue sheet – consumed by scripts/make-audio.ts */
export const buildCues = (): Cue[] => {
  const c: Cue[] = [];
  // Welcome
  c.push({t: TL.welcome.panelIn + 0.08, kind: 'glass', gain: 0.9, pan: -0.2});
  c.push({t: TL.welcome.panelIn + 0.05, kind: 'whoosh', gain: 0.8, pan: -0.3, dur: 0.7});
  c.push({t: TL.welcome.title, kind: 'whoosh', gain: 0.7, pan: 0.1, dur: 0.6});
  c.push({t: TL.welcome.sweep, kind: 'shimmer', gain: 0.8, dur: 0.9});
  // Now open
  c.push({t: TL.open.panelIn, kind: 'glass', gain: 1.0, pan: 0.2});
  c.push({t: TL.open.panelIn, kind: 'whoosh', gain: 0.9, pan: 0.3, dur: 0.6});
  c.push({t: TL.open.headline + 0.1, kind: 'impact', gain: 0.55, pitch: 0.8});
  c.push({t: TL.open.sparkle, kind: 'sparkle', gain: 1.0, dur: 1.2});
  c.push({t: TL.open.subline, kind: 'ping', gain: 0.55, pitch: 1.0});
  // Services
  c.push({t: TL.services.headingIn, kind: 'whoosh', gain: 0.8, pan: 0.1, dur: 0.6});
  c.push({t: TL.services.headingIn + 0.05, kind: 'glass', gain: 0.9});
  const sv = serviceTimes();
  const scale = [0, 2, 4, 7, 9, 11, 14]; // pentatonic-ish semitone steps
  for (let k = 0; k < sv.n; k++) {
    const t = sv.enter(k);
    c.push({t: t + 0.02, kind: 'glass', gain: 0.75, pan: k % 2 ? 0.25 : -0.25});
    c.push({t: t + 0.36, kind: 'pulse', gain: 0.8, pitch: Math.pow(2, scale[k % scale.length] / 12)});
  }
  // Expansion
  c.push({t: TL.expansion.shrink, kind: 'whoosh', gain: 1.0, pan: 0, dur: 0.9});
  c.push({t: TL.expansion.kicker - 0.05, kind: 'glass', gain: 0.8});
  c.push({t: TL.expansion.mapIn + 0.1, kind: 'shimmer', gain: 0.55, dur: 1.0});
  c.push({t: TL.expansion.homeLand, kind: 'impact', gain: 0.9, pitch: 0.9});
  c.push({t: TL.expansion.next, kind: 'whoosh', gain: 0.8, pan: -0.1, dur: 0.6});
  c.push({t: TL.expansion.badge, kind: 'ping', gain: 0.7, pitch: 1.5});
  config.expansion.cities.forEach((_, k) => {
    const ct = cityTimes(k);
    c.push({t: ct.arc, kind: 'whoosh', gain: 0.45, pan: k % 2 ? 0.3 : -0.3, dur: 0.5});
    c.push({t: ct.label, kind: 'glass', gain: 0.55, pan: k % 2 ? 0.3 : -0.3});
    c.push({t: ct.land, kind: 'impact', gain: 0.85, pitch: 1.0 + k * 0.06, pan: k % 2 ? 0.2 : -0.2});
  });
  // Outro
  c.push({t: TL.outro.bloom - 0.55, kind: 'riser', gain: 1.0, dur: 0.75});
  c.push({t: TL.outro.emblem + 0.05, kind: 'logo', gain: 1.0});
  c.push({t: TL.outro.wordmark, kind: 'shimmer', gain: 0.8, dur: 0.9});
  c.push({t: TL.outro.tagline, kind: 'ping', gain: 0.6, pitch: 1.25});
  c.push({t: TL.outro.goals, kind: 'glass', gain: 0.8});
  c.push({t: TL.outro.cta, kind: 'glass', gain: 1.0});
  c.push({t: TL.outro.cta + 0.15, kind: 'ping', gain: 0.8, pitch: 1.5});
  return c.sort((a, b) => a.t - b.t);
};
