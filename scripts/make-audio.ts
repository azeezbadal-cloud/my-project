/**
 * Sound design for the WWCC promo – everything is synthesised here (no samples, no licensing issues):
 *   • warm cinematic music bed (pad + soft plucks + bass + gentle percussion, 100 BPM, D major)
 *   • sound effects on the same cue sheet as the animations (src/timeline.ts):
 *       glass slides, light whooshes, icon pulses, location-marker impacts, sparkles, logo reveal
 *   • voice clean-up (high-pass, light denoise, presence EQ, gentle compression)
 *   • music ducks under the voice (side-chain), everything is loudness-normalised for social media
 *
 *   npm run audio        →  out/audio-mix.wav   (48 kHz stereo)
 *
 * Needs ffmpeg on the PATH and the untouched voice track at assets/work/voice_raw.wav (npm run prepare).
 */
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {config} from '../src/config';
import {buildCues, Cue} from '../src/timeline';

const SR = 48000;
const DUR = config.durationInFrames / config.fps; // picture length in seconds
const TAIL = 3;
const N = Math.ceil((DUR + TAIL) * SR);

// ── tiny DSP toolkit ──────────────────────────────────────────────────────────────────────────
const rng = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};
const hz = (note: number) => 440 * Math.pow(2, (note - 69) / 12); // midi → Hz
const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));
const smooth = (x: number) => {
  const t = clamp(x, 0, 1);
  return t * t * (3 - 2 * t);
};

type Stereo = {L: Float32Array; R: Float32Array};
const newStereo = (n = N): Stereo => ({L: new Float32Array(n), R: new Float32Array(n)});

/** mix a mono buffer into a stereo bus (equal-power pan −1…1) */
const addMono = (dst: Stereo, src: Float32Array, at: number, gain = 1, pan = 0) => {
  const a = ((clamp(pan, -1, 1) + 1) * Math.PI) / 4;
  const gl = Math.cos(a) * gain;
  const gr = Math.sin(a) * gain;
  const s0 = Math.round(at * SR);
  for (let i = 0; i < src.length; i++) {
    const j = s0 + i;
    if (j < 0 || j >= dst.L.length) continue;
    dst.L[j] += src[i] * gl;
    dst.R[j] += src[i] * gr;
  }
};
const addStereo = (dst: Stereo, src: Stereo, at = 0, gain = 1) => {
  const s0 = Math.round(at * SR);
  for (let i = 0; i < src.L.length; i++) {
    const j = s0 + i;
    if (j < 0 || j >= dst.L.length) continue;
    dst.L[j] += src.L[i] * gain;
    dst.R[j] += src.R[i] * gain;
  }
};

class TPT {
  s1 = 0;
  s2 = 0;
  process(x: number, fc: number, q: number) {
    const g = Math.tan((Math.PI * clamp(fc, 20, SR * 0.45)) / SR);
    const k = 1 / q;
    const a1 = 1 / (1 + g * (g + k));
    const a2 = g * a1;
    const a3 = g * a2;
    const v3 = x - this.s2;
    const v1 = a1 * this.s1 + a2 * v3;
    const v2 = this.s2 + a2 * this.s1 + a3 * v3;
    this.s1 = 2 * v1 - this.s1;
    this.s2 = 2 * v2 - this.s2;
    return {lp: v2, bp: v1, hp: x - k * v1 - v2};
  }
}

class Comb {
  buf: Float32Array;
  i = 0;
  store = 0;
  constructor(size: number) {
    this.buf = new Float32Array(size);
  }
  process(x: number, fb: number, damp: number) {
    const out = this.buf[this.i];
    this.store = out * (1 - damp) + this.store * damp;
    this.buf[this.i] = x + this.store * fb;
    if (++this.i >= this.buf.length) this.i = 0;
    return out;
  }
}
class Allpass {
  buf: Float32Array;
  i = 0;
  constructor(size: number) {
    this.buf = new Float32Array(size);
  }
  process(x: number) {
    const b = this.buf[this.i];
    const out = -x + b;
    this.buf[this.i] = x + b * 0.5;
    if (++this.i >= this.buf.length) this.i = 0;
    return out;
  }
}
/** Freeverb-style stereo reverb. Returns the wet signal only. */
const reverb = (inp: Stereo, room = 0.86, damp = 0.35): Stereo => {
  const sc = SR / 44100;
  const ct = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617].map((v) => Math.round(v * sc));
  const at = [556, 441, 341, 225].map((v) => Math.round(v * sc));
  const spread = Math.round(23 * sc);
  const cL = ct.map((s) => new Comb(s));
  const cR = ct.map((s) => new Comb(s + spread));
  const aL = at.map((s) => new Allpass(s));
  const aR = at.map((s) => new Allpass(s + spread));
  const out = newStereo(inp.L.length);
  const fb = 0.7 + room * 0.28;
  for (let n = 0; n < inp.L.length; n++) {
    const x = (inp.L[n] + inp.R[n]) * 0.015;
    let l = 0;
    let r = 0;
    for (let k = 0; k < 8; k++) {
      l += cL[k].process(x, fb, damp);
      r += cR[k].process(x, fb, damp);
    }
    for (let k = 0; k < 4; k++) {
      l = aL[k].process(l);
      r = aR[k].process(r);
    }
    out.L[n] = l;
    out.R[n] = r;
  }
  return out;
};

const rms = (s: Stereo, from = 0, to = N) => {
  let a = 0;
  for (let i = from; i < to; i++) a += s.L[i] * s.L[i] + s.R[i] * s.R[i];
  return Math.sqrt(a / (2 * (to - from)));
};
const peak = (s: Stereo) => {
  let p = 0;
  for (let i = 0; i < s.L.length; i++) p = Math.max(p, Math.abs(s.L[i]), Math.abs(s.R[i]));
  return p;
};
const scaleStereo = (s: Stereo, g: number) => {
  for (let i = 0; i < s.L.length; i++) {
    s.L[i] *= g;
    s.R[i] *= g;
  }
};

// ── instruments ───────────────────────────────────────────────────────────────────────────────
/** inharmonic-ish bell / glass tone */
const bell = (f: number, dur: number, decay = 0.6, partials = [1, 2.0, 3.01, 4.17], amps = [1, 0.36, 0.15, 0.06]) => {
  const n = Math.floor(dur * SR);
  const out = new Float32Array(n);
  partials.forEach((pr, p) => {
    const fp = f * pr;
    if (fp > 14000) return;
    const d = decay / (1 + p * 0.85);
    const w = (2 * Math.PI * fp) / SR;
    let ph = 0;
    for (let i = 0; i < n; i++) {
      const t = i / SR;
      out[i] += Math.sin(ph) * amps[p] * Math.exp(-t / d) * Math.min(1, t / 0.0025);
      ph += w;
    }
  });
  return out;
};

/** soft kalimba-like pluck */
const pluck = (f: number, dur = 0.7) => {
  const n = Math.floor(dur * SR);
  const out = new Float32Array(n);
  const w = (2 * Math.PI * f) / SR;
  let ph = 0;
  let ph2 = 0;
  let ph3 = 0;
  const lp = new TPT();
  for (let i = 0; i < n; i++) {
    const t = i / SR;
    const env = Math.exp(-t / 0.28) * Math.min(1, t / 0.003);
    const env2 = Math.exp(-t / 0.09);
    const x = Math.sin(ph) + 0.32 * Math.sin(ph2) * env2 + 0.1 * Math.sin(ph3) * env2;
    out[i] = lp.process(x * env, 4200, 0.7).lp;
    ph += w;
    ph2 += w * 2;
    ph3 += w * 3.01;
  }
  return out;
};

const noiseBuf = (dur: number, seed: number) => {
  const r = rng(seed);
  const n = Math.floor(dur * SR);
  const out = new Float32Array(n);
  for (let i = 0; i < n; i++) out[i] = r() * 2 - 1;
  return out;
};

// ── music ─────────────────────────────────────────────────────────────────────────────────────
const BPM = 100;
const BEAT = 60 / BPM; // 0.6 s
const BAR = BEAT * 4; // 2.4 s  (the logo hit at 19.2 s is bar 9, beat 1)
const BARS = Math.ceil((DUR + 0.5) / BAR);

// D major progression:  D  A  Bm  G  D  A  Bm  G | D(add9)  A→D
const CHORDS: {root: number; tones: number[]; bass: number}[] = [
  {root: 62, tones: [50, 57, 62, 66, 69], bass: 38}, // D
  {root: 57, tones: [45, 52, 57, 61, 64], bass: 45}, // A
  {root: 59, tones: [47, 54, 59, 62, 66], bass: 47}, // Bm
  {root: 55, tones: [43, 50, 55, 59, 62], bass: 43}, // G
  {root: 62, tones: [50, 57, 62, 66, 69], bass: 38},
  {root: 57, tones: [45, 52, 57, 61, 64], bass: 45},
  {root: 59, tones: [47, 54, 59, 62, 66], bass: 47},
  {root: 55, tones: [43, 50, 55, 59, 62], bass: 43},
  {root: 62, tones: [50, 57, 62, 64, 69], bass: 38}, // D add9  (logo reveal)
  {root: 57, tones: [45, 52, 57, 62, 64], bass: 45},
];
// intensity per bar – a slow build into the logo reveal
const INTENSITY = [1.0, 1.0, 1.0, 0.98, 1.0, 1.02, 1.05, 1.08, 1.12, 0.9, 0.8];
const ARP = [0, 2, 3, 2, 1, 3, 4, 3]; // indices into the chord's upper tones (8th-note pattern)

const makeMusic = (): Stereo => {
  const dry = newStereo();
  const send = newStereo(); // → reverb
  const echo = newStereo(); // → ping-pong delay
  const r = rng(11);

  // pad – detuned band-limited saws, slow attack, gently breathing low-pass
  const pad = newStereo();
  for (let b = 0; b < BARS; b++) {
    const ch = CHORDS[Math.min(b, CHORDS.length - 1)];
    const t0 = b * BAR - 0.25;
    const t1 = (b + 1) * BAR + 0.85;
    const g = 0.05 * INTENSITY[Math.min(b, INTENSITY.length - 1)];
    ch.tones.forEach((note, ni) => {
      const f0 = hz(note + (ni === 0 ? 0 : 0));
      [
        {side: 'L', cents: [-7, 3]},
        {side: 'R', cents: [7, -3]},
      ].forEach(({side, cents}) => {
        cents.forEach((c) => {
          const f = f0 * Math.pow(2, c / 1200);
          const s0 = Math.max(0, Math.floor(t0 * SR));
          const s1 = Math.min(N, Math.floor(t1 * SR));
          const buf = side === 'L' ? pad.L : pad.R;
          let ph = r() * 6.283;
          const w = (2 * Math.PI * f) / SR;
          for (let i = s0; i < s1; i++) {
            const t = i / SR;
            const env = smooth((t - t0) / 0.9) * smooth((t1 - t) / 0.9);
            let v = 0;
            for (let h = 1; h <= 5; h++) v += Math.sin(ph * h) / Math.pow(h, 1.15);
            buf[i] += v * env * g * (ni === 0 ? 1.25 : 1);
            ph += w;
          }
        });
      });
    });
  }
  const lpL = new TPT();
  const lpR = new TPT();
  for (let i = 0; i < N; i++) {
    const t = i / SR;
    const fc = 1150 + 520 * Math.sin((2 * Math.PI * t) / 9.6) + 380 * clamp((t - 14) / 6, 0, 1);
    pad.L[i] = lpL.process(pad.L[i], fc, 0.6).lp;
    pad.R[i] = lpR.process(pad.R[i], fc, 0.6).lp;
  }
  addStereo(dry, pad, 0, 1);
  addStereo(send, pad, 0, 0.35);

  // plucked arpeggio (8th notes) with a dotted-8th echo
  for (let b = 1; b < BARS; b++) {
    const ch = CHORDS[Math.min(b, CHORDS.length - 1)];
    const inten = INTENSITY[Math.min(b, INTENSITY.length - 1)];
    const up = ch.tones.map((n) => n + 12);
    for (let s = 0; s < 8; s++) {
      if (b < 2 && s % 2 === 1) continue; // sparse at first
      const t = b * BAR + s * (BEAT / 2) + (r() - 0.5) * 0.008;
      const note = up[ARP[s] % up.length];
      const accent = s % 4 === 0 ? 1 : s % 2 === 0 ? 0.78 : 0.62;
      const buf = pluck(hz(note), 0.9);
      const pan = ((s * 37) % 7) / 7 - 0.5;
      addMono(dry, buf, t, 0.085 * inten * accent, pan * 0.7);
      addMono(send, buf, t, 0.045 * inten * accent, pan * 0.7);
      addMono(echo, buf, t, 0.05 * inten * accent, pan * 0.5);
    }
  }
  // octave sparkle on the logo bar and the finale
  for (let b = 8; b < BARS; b++) {
    const ch = CHORDS[Math.min(b, CHORDS.length - 1)];
    for (let s = 0; s < 8; s += 1) {
      const t = b * BAR + s * (BEAT / 2) + 0.01;
      const note = ch.tones[(s * 2) % ch.tones.length] + 24;
      const buf = bell(hz(note), 1.6, 0.55);
      addMono(dry, buf, t, 0.022 * INTENSITY[b], ((s % 2) - 0.5) * 0.9);
      addMono(send, buf, t, 0.03 * INTENSITY[b], ((s % 2) - 0.5) * 0.9);
    }
  }
  // ping-pong echo (dotted 8th, low-passed feedback)
  {
    const d = Math.round(BEAT * 0.75 * SR);
    const fbk = 0.38;
    const lpa = new TPT();
    const lpb = new TPT();
    const bl = new Float32Array(N);
    const br = new Float32Array(N);
    for (let i = 0; i < N; i++) {
      const inL = echo.L[i] + (i >= d ? br[i - d] * fbk : 0);
      const inR = echo.R[i] + (i >= d ? bl[i - d] * fbk : 0);
      bl[i] = lpa.process(inL, 3200, 0.7).lp;
      br[i] = lpb.process(inR, 3200, 0.7).lp;
    }
    for (let i = 0; i < N; i++) {
      dry.L[i] += bl[i] * 0.8;
      dry.R[i] += br[i] * 0.8;
    }
    for (let i = 0; i < N; i++) {
      send.L[i] += bl[i] * 0.5;
      send.R[i] += br[i] * 0.5;
    }
  }

  // bass – soft, round (kept above ~70 Hz so phone speakers can still carry it with its harmonics)
  for (let b = 2; b < BARS; b++) {
    const ch = CHORDS[Math.min(b, CHORDS.length - 1)];
    const inten = INTENSITY[Math.min(b, INTENSITY.length - 1)];
    [0, 2.5].forEach((beat) => {
      const t0 = b * BAR + beat * BEAT;
      const len = beat === 0 ? 1.9 * BEAT : 1.4 * BEAT;
      const n = Math.floor(len * SR);
      const f = hz(ch.bass + 12);
      let ph = 0;
      const w = (2 * Math.PI * f) / SR;
      const buf = new Float32Array(n);
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const env = smooth(t / 0.02) * Math.exp(-t / (len * 0.55));
        buf[i] = (Math.sin(ph) + 0.28 * Math.sin(ph * 2) + 0.1 * Math.sin(ph * 3)) * env;
        ph += w;
      }
      addMono(dry, buf, t0, 0.15 * inten * (beat === 0 ? 1 : 0.7), 0);
    });
  }

  // percussion – soft kick on 1 & 3, whisper tick on 2 & 4, shaker 8ths (all very gentle)
  const tickNoise = noiseBuf(0.05, 99);
  for (let b = 2; b < BARS; b++) {
    const inten = INTENSITY[Math.min(b, INTENSITY.length - 1)];
    for (let beat = 0; beat < 4; beat++) {
      const t = b * BAR + beat * BEAT;
      if (b >= 4 && beat % 2 === 0) {
        const n = Math.floor(0.22 * SR);
        const buf = new Float32Array(n);
        let ph = 0;
        for (let i = 0; i < n; i++) {
          const tt = i / SR;
          const f = 52 + 70 * Math.exp(-tt / 0.03);
          ph += (2 * Math.PI * f) / SR;
          buf[i] = Math.sin(ph) * Math.exp(-tt / 0.07) * smooth(tt / 0.002);
        }
        addMono(dry, buf, t, 0.26 * inten, 0);
      }
      if (b >= 3 && beat % 2 === 1) {
        const hp = new TPT();
        const buf = new Float32Array(tickNoise.length);
        for (let i = 0; i < buf.length; i++) buf[i] = hp.process(tickNoise[i], 2600, 0.8).bp * Math.exp(-i / SR / 0.03);
        addMono(dry, buf, t, 0.1 * inten, 0.15);
        addMono(send, buf, t, 0.06 * inten, 0.15);
      }
    }
    for (let s = 0; s < 8; s++) {
      const t = b * BAR + s * (BEAT / 2) + BEAT / 4 * 0;
      const hp = new TPT();
      const nb = noiseBuf(0.04, 500 + b * 8 + s);
      const buf = new Float32Array(nb.length);
      for (let i = 0; i < buf.length; i++) buf[i] = hp.process(nb[i], 7000, 0.7).hp * Math.exp(-i / SR / 0.012);
      addMono(dry, buf, t + BEAT / 4, 0.03 * inten * (s % 2 ? 0.7 : 1), (s % 2 ? 0.3 : -0.3));
    }
  }

  const wet = reverb(send, 0.88, 0.4);
  addStereo(dry, wet, 0, 1.1);
  // normalise: music RMS ≈ −20 dBFS over the picture
  const target = 0.1;
  scaleStereo(dry, target / Math.max(1e-6, rms(dry, 0, Math.floor(DUR * SR))));
  return dry;
};

// ── sound effects ─────────────────────────────────────────────────────────────────────────────
const sfxMono = (cue: Cue, seed: number): {buf: Float32Array; send: number} => {
  const r = rng(seed);
  switch (cue.kind) {
    case 'glass': {
      // a short filtered-noise slide + two glassy partials
      const n = Math.floor(0.42 * SR);
      const out = new Float32Array(n);
      const f = new TPT();
      const nz = noiseBuf(0.42, seed);
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const fc = 2200 + 3800 * smooth(t / 0.18);
        const env = Math.sin(Math.PI * clamp(t / 0.22, 0, 1)) * Math.exp(-t / 0.12);
        out[i] += f.process(nz[i], fc, 2.2).bp * env * 0.9;
      }
      const base = 2637 * (0.97 + r() * 0.06);
      const pings = [bell(base, 0.5, 0.2, [1, 1.504, 2.31], [1, 0.5, 0.25]), bell(base * 1.498, 0.4, 0.14, [1, 2.0], [0.7, 0.3])];
      pings.forEach((p, k) => p.forEach((v, i) => (out[Math.floor(0.05 * SR * k) + i] += v * 0.35)));
      return {buf: out, send: 0.5};
    }
    case 'whoosh': {
      const dur = cue.dur ?? 0.7;
      const n = Math.floor(dur * SR);
      const out = new Float32Array(n);
      const nz = noiseBuf(dur, seed);
      const f = new TPT();
      const low = new TPT();
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const x = t / dur;
        const fc = 260 * Math.pow(14, smooth(x)); // 260 Hz → ~3.6 kHz
        const env = Math.pow(Math.sin(Math.PI * clamp(x, 0, 1)), 1.6);
        out[i] = (f.process(nz[i], fc, 1.4).bp * 1.0 + low.process(nz[i], 160, 0.7).lp * 0.5) * env;
      }
      return {buf: out, send: 0.3};
    }
    case 'pulse': {
      const f0 = 784 * (cue.pitch ?? 1);
      const n = Math.floor(0.5 * SR);
      const out = new Float32Array(n);
      let ph = 0;
      let ph2 = 0;
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const f = f0 * (1 + 0.025 * Math.exp(-t / 0.03));
        const env = Math.exp(-t / 0.11) * smooth(t / 0.002);
        out[i] = (Math.sin(ph) + 0.28 * Math.sin(ph2)) * env;
        ph += (2 * Math.PI * f) / SR;
        ph2 += (2 * Math.PI * f * 2.005) / SR;
      }
      // soft echo
      for (let i = Math.floor(0.12 * SR); i < n; i++) out[i] += out[i - Math.floor(0.12 * SR)] * 0.32;
      return {buf: out, send: 0.45};
    }
    case 'impact': {
      const n = Math.floor(0.9 * SR);
      const out = new Float32Array(n);
      let ph = 0;
      const p = cue.pitch ?? 1;
      const nz = noiseBuf(0.9, seed);
      const lp = new TPT();
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const f = (62 + 90 * Math.exp(-t / 0.045)) * p;
        ph += (2 * Math.PI * f) / SR;
        out[i] = Math.sin(ph) * Math.exp(-t / 0.16) * smooth(t / 0.002) * 0.9 + lp.process(nz[i], 900, 0.7).lp * Math.exp(-t / 0.03) * 0.5;
      }
      const ting = bell(1568 * p, 0.85, 0.32, [1, 1.5, 2.76], [1, 0.4, 0.2]);
      ting.forEach((v, i) => (out[i] += v * 0.3));
      return {buf: out, send: 0.55};
    }
    case 'sparkle': {
      const dur = cue.dur ?? 1.2;
      const n = Math.floor((dur + 0.8) * SR);
      const out = new Float32Array(n);
      const scale = [74, 76, 78, 81, 83, 86, 88, 90, 93]; // D major pentatonic, high
      const count = 12;
      for (let k = 0; k < count; k++) {
        const t = (k / count) * dur * (0.6 + 0.4 * r()) + r() * 0.05;
        const note = scale[Math.floor(r() * scale.length)];
        const b = bell(hz(note), 0.7, 0.16 + r() * 0.1, [1, 2.0, 3.0], [1, 0.3, 0.1]);
        const g = 0.5 * (1 - (k / count) * 0.6);
        b.forEach((v, i) => {
          const j = Math.floor(t * SR) + i;
          if (j < n) out[j] += v * g;
        });
      }
      return {buf: out, send: 0.6};
    }
    case 'riser': {
      const dur = cue.dur ?? 0.75;
      const n = Math.floor(dur * SR);
      const out = new Float32Array(n);
      const nz = noiseBuf(dur, seed);
      const f = new TPT();
      let ph = 0;
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const x = t / dur;
        const fc = 350 * Math.pow(26, x);
        const env = Math.pow(x, 2.2);
        ph += (2 * Math.PI * (180 * Math.pow(9, x))) / SR;
        out[i] = (f.process(nz[i], fc, 1.2).bp * 0.9 + Math.sin(ph) * 0.12) * env;
      }
      return {buf: out, send: 0.4};
    }
    case 'logo': {
      // soft boom + shimmering bell chord + airy swish
      const n = Math.floor(3.2 * SR);
      const out = new Float32Array(n);
      let ph = 0;
      const nz = noiseBuf(3.2, seed);
      const hpf = new TPT();
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const f = 44 + 70 * Math.exp(-t / 0.18);
        ph += (2 * Math.PI * f) / SR;
        const boom = Math.sin(ph) * Math.exp(-t / 0.55) * smooth(t / 0.006);
        const air = hpf.process(nz[i], 3000 + 5000 * smooth(t / 0.6), 0.8).hp * Math.sin(Math.PI * clamp(t / 0.9, 0, 1)) * 0.12;
        out[i] = boom * 0.85 + air;
      }
      [74, 78, 81, 86, 88].forEach((note, k) => {
        const b = bell(hz(note), 2.6, 1.15, [1, 2.0, 3.0, 4.2], [1, 0.4, 0.18, 0.08]);
        const off = Math.floor(k * 0.055 * SR);
        b.forEach((v, i) => {
          if (off + i < n) out[off + i] += v * 0.2;
        });
      });
      return {buf: out, send: 0.75};
    }
    case 'shimmer': {
      const dur = cue.dur ?? 0.9;
      const n = Math.floor((dur + 0.6) * SR);
      const out = new Float32Array(n);
      const phs = [0, 0, 0, 0];
      const nz = noiseBuf(dur + 0.6, seed);
      const hp = new TPT();
      for (let i = 0; i < n; i++) {
        const t = i / SR;
        const x = clamp(t / dur, 0, 1);
        const env = Math.sin(Math.PI * x) * Math.exp(-Math.max(0, t - dur) / 0.2);
        let v = 0;
        [1, 1.5, 2, 3].forEach((m, k) => {
          const f = 1500 * m * (1 + 0.5 * x);
          phs[k] += (2 * Math.PI * f) / SR;
          v += Math.sin(phs[k]) * (0.3 / (1 + k * 0.7)) * (0.7 + 0.3 * Math.sin(t * 22 + k));
        });
        v += hp.process(nz[i], 6500, 0.8).hp * 0.12;
        out[i] = v * env * 0.55;
      }
      return {buf: out, send: 0.6};
    }
    case 'ping': {
      const f = 1760 * (cue.pitch ?? 1);
      return {buf: bell(f, 0.9, 0.38, [1, 2.0, 3.01], [1, 0.32, 0.12]), send: 0.6};
    }
  }
};

const KIND_GAIN: Record<Cue['kind'], number> = {
  glass: 0.5,
  whoosh: 0.5,
  pulse: 0.36,
  impact: 0.55,
  sparkle: 0.34,
  riser: 0.5,
  logo: 0.95,
  shimmer: 0.42,
  ping: 0.3,
};

const makeSfx = (): Stereo => {
  const dry = newStereo();
  const send = newStereo();
  buildCues().forEach((cue, idx) => {
    const {buf, send: s} = sfxMono(cue, 1000 + idx * 17);
    const g = (cue.gain ?? 1) * KIND_GAIN[cue.kind];
    // riser lands exactly on its end time
    const start = cue.kind === 'riser' ? cue.t : cue.t;
    addMono(dry, buf, start, g, cue.pan ?? 0);
    addMono(send, buf, start, g * s, cue.pan ?? 0);
  });
  const wet = reverb(send, 0.8, 0.5);
  addStereo(dry, wet, 0, 1);
  // peak-normalise (the logo reveal is the loudest event)
  scaleStereo(dry, 0.5 / Math.max(1e-6, peak(dry)));
  return dry;
};

// ── WAV writer + ffmpeg mix ───────────────────────────────────────────────────────────────────
const writeWav = (file: string, s: Stereo) => {
  const n = s.L.length;
  const buf = Buffer.alloc(44 + n * 8);
  buf.write('RIFF', 0);
  buf.writeUInt32LE(36 + n * 8, 4);
  buf.write('WAVE', 8);
  buf.write('fmt ', 12);
  buf.writeUInt32LE(16, 16);
  buf.writeUInt16LE(3, 20); // float
  buf.writeUInt16LE(2, 22);
  buf.writeUInt32LE(SR, 24);
  buf.writeUInt32LE(SR * 8, 28);
  buf.writeUInt16LE(8, 32);
  buf.writeUInt16LE(32, 34);
  buf.write('data', 36);
  buf.writeUInt32LE(n * 8, 40);
  for (let i = 0; i < n; i++) {
    buf.writeFloatLE(s.L[i], 44 + i * 8);
    buf.writeFloatLE(s.R[i], 48 + i * 8);
  }
  fs.writeFileSync(file, buf);
};

const ff = (args: string[], quiet = true) => {
  const r = spawnSync('ffmpeg', ['-hide_banner', ...(quiet ? ['-nostats'] : []), '-y', ...args], {encoding: 'utf8', maxBuffer: 1 << 28});
  if (r.status !== 0) throw new Error(`ffmpeg failed:\n${r.stderr}`);
  return r.stderr;
};

const VOICE_CHAIN =
  'aresample=48000,aformat=channel_layouts=stereo,highpass=f=100,afftdn=nr=9:nf=-42,' +
  'equalizer=f=190:t=q:w=0.9:g=-2.5,equalizer=f=3200:t=q:w=1:g=2.5,equalizer=f=9500:t=h:w=0.7:g=1.8,' +
  'acompressor=threshold=0.06:ratio=2.8:attack=8:release=140:makeup=2.5';

const main = () => {
  const work = path.resolve('assets/work/audio');
  const out = path.resolve('out');
  fs.mkdirSync(work, {recursive: true});
  fs.mkdirSync(out, {recursive: true});
  const voice = path.resolve('assets/work/voice_raw.wav');
  if (!fs.existsSync(voice)) throw new Error('missing assets/work/voice_raw.wav – run: npm run prepare');

  console.log('synthesising music …');
  const music = makeMusic();
  writeWav(path.join(work, 'music.wav'), music);
  console.log('synthesising sound effects …');
  const sfx = makeSfx();
  writeWav(path.join(work, 'sfx.wav'), sfx);

  // voice level → −16.5 LUFS before it meets the music
  const raw = ff(['-i', voice, '-af', `${VOICE_CHAIN},ebur128=framelog=quiet`, '-f', 'null', '-']);
  const vm = [...raw.matchAll(/I:\s+(-?[\d.]+)\s+LUFS/g)].pop();
  const voiceI = vm ? parseFloat(vm[1]) : -24;
  const voiceGain = -16.5 - voiceI;
  console.log(`voice: ${voiceI.toFixed(1)} LUFS after clean-up → gain ${voiceGain.toFixed(1)} dB`);

  const MUSIC_DB = -1; // before ducking – the side-chain pulls it down a further ~8 dB while you speak
  const SFX_DB = -4;
  const common =
    `[0:a]${VOICE_CHAIN},volume=${voiceGain.toFixed(2)}dB,alimiter=limit=0.89:attack=3:release=60[v1];` +
    `[v1]asplit=2[vmix][vsc];` +
    `[1:a]volume=${MUSIC_DB}dB[m];` +
    `[m][vsc]sidechaincompress=threshold=0.03:ratio=2.6:attack=20:release=500:makeup=1[mduck];` +
    `[2:a]volume=${SFX_DB}dB[s]`;
  const graph =
    `${common};[vmix][mduck][s]amix=inputs=3:normalize=0:duration=longest[mix];` +
    `[mix]atrim=0:${DUR.toFixed(4)},afade=t=out:st=${(DUR - 0.5).toFixed(3)}:d=0.5[o]`;
  const inputs = ['-i', voice, '-i', path.join(work, 'music.wav'), '-i', path.join(work, 'sfx.wav')];

  const pre = path.join(work, 'mix_pre.wav');
  ff([...inputs, '-filter_complex', graph, '-map', '[o]', '-c:a', 'pcm_f32le', pre]);
  if (process.env.AUDIO_STEMS) {
    // diagnostic: the three stems exactly as they enter the final mix (voice / ducked music / effects)
    ff([...inputs, '-filter_complex', common, '-map', '[vmix]', path.join(work, 'stem_voice.wav'), '-map', '[mduck]', path.join(work, 'stem_music.wav'), '-map', '[s]', path.join(work, 'stem_sfx.wav')]);
  }

  // two-pass loudness normalisation to the social-media standard (−14 LUFS, −1 dBTP)
  const p1 = ff(['-i', pre, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=9:print_format=json', '-f', 'null', '-']);
  const j = JSON.parse(p1.slice(p1.lastIndexOf('{'), p1.lastIndexOf('}') + 1));
  const final = path.join(out, 'audio-mix.wav');
  ff([
    '-i',
    pre,
    '-af',
    `loudnorm=I=-14:TP=-1.0:LRA=9:measured_I=${j.input_i}:measured_TP=${j.input_tp}:measured_LRA=${j.input_lra}:measured_thresh=${j.input_thresh}:offset=${j.target_offset}:linear=true`,
    '-ar',
    '48000',
    '-c:a',
    'pcm_s24le',
    final,
  ]);
  console.log(`mix written: ${final}  (before normalisation: ${j.input_i} LUFS, true-peak ${j.input_tp} dBTP)`);
};

main();
