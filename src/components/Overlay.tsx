import React from 'react';
import {config} from '../config';
import {TL} from '../timeline';
import {easeInCubic, easeInOutCubic, lerp, prog} from '../lib/anim';

/** A diagonal bar of light that sweeps across the whole frame (used on scene changes). */
const Sweep: React.FC<{t: number; at: number; dur?: number; strength?: number}> = ({t, at, dur = 0.85, strength = 1}) => {
  const p = prog(t, at, dur);
  if (p <= 0 || p >= 1) return null;
  const e = easeInOutCubic(p);
  const x = lerp(-700, 1700, e);
  const a = Math.sin(Math.PI * p) * strength;
  return (
    <div
      style={{
        position: 'absolute',
        left: x - 210,
        top: -300,
        width: 420,
        height: 2500,
        transform: 'rotate(18deg)',
        background:
          'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(140,215,255,0.20) 30%, rgba(255,255,255,0.62) 50%, rgba(120,255,210,0.20) 70%, rgba(255,255,255,0) 100%)',
        opacity: a,
        mixBlendMode: 'screen',
        filter: 'blur(10px)',
        pointerEvents: 'none',
      }}
    />
  );
};

type Props = {t: number};

/** Global finishing layer: legibility gradients, scene-change light sweeps, final fade to black. */
export const Overlay: React.FC<Props> = ({t}) => {
  // the fade reaches pure black exactly on the last frame
  const lastT = (config.durationInFrames - 1) / config.fps;
  const fade = easeInCubic(prog(t, TL.outro.fade, lastT - TL.outro.fade));
  return (
    <>
      {/* soft top/bottom darkening keeps headlines legible and gives the frame a cinematic vignette */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background:
            'linear-gradient(180deg, rgba(2,10,44,0.50) 0%, rgba(2,10,44,0) 24%, rgba(2,10,44,0) 70%, rgba(2,10,44,0.42) 100%)',
          pointerEvents: 'none',
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(130% 90% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,6,30,0.38) 100%)',
          pointerEvents: 'none',
        }}
      />
      <Sweep t={t} at={config.open.start - 0.05} strength={0.85} />
      <Sweep t={t} at={config.services.start - 0.05} strength={0.85} />
      <Sweep t={t} at={config.expansion.start - 0.05} dur={1.0} strength={1} />
      <Sweep t={t} at={config.outro.start - 0.1} dur={1.0} strength={1} />
      {fade > 0 && <div style={{position: 'absolute', inset: 0, background: '#000', opacity: Math.min(1, fade)}} />}
    </>
  );
};
