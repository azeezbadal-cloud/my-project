import React from 'react';
import {OffthreadVideo, staticFile} from 'remotion';
import {config} from '../config';
import {colors, H, W, windowGeom} from '../theme';
import {easeInOutCubic, lerp, prog} from '../lib/anim';
import {Atmosphere} from './Atmosphere';

/** 0 → 1 : how far the footage has shrunk into its floating window (stays 1 after the map starts). */
export const windowProgress = (t: number) =>
  easeInOutCubic(prog(t, config.expansion.start, config.window.seconds));

/** Slow cinematic push-in on the footage + a tiny punch at each scene change. */
const zoomAt = (t: number) => {
  const base = 0.032 * prog(t, 0, config.expansion.start);
  const punch = (at: number) => {
    const d = t - at;
    if (d < 0 || d > 1.1) return 0;
    return 0.02 * (d < 0.22 ? d / 0.22 : Math.pow(1 - (d - 0.22) / 0.88, 2));
  };
  return base + punch(config.open.start) + punch(config.services.start);
};

const FOOTAGE = staticFile(config.files.footage);
const SPEAKER = staticFile(config.files.speaker);
const FACE_ORIGIN = '540px 760px';

type Props = {
  t: number;
  /** Elements that sit BEHIND the speaker (glass banners etc.) – they are clipped/scaled with the window. */
  behind?: React.ReactNode;
};

export const VideoStage: React.FC<Props> = ({t, behind}) => {
  const p = windowProgress(t);
  const g = windowGeom(p);
  const z = zoomAt(t) * (1 - p);
  const cut = config.useSpeakerCutout;

  // Only the BACKGROUND fades into the surrounding fill at the top of the window – the speaker stays solid.
  const fadeLen = 340 * p;
  const mask = p > 0.001 ? `linear-gradient(to bottom, transparent 0px, rgba(0,0,0,0.08) ${fadeLen * 0.2}px, #000 ${fadeLen}px)` : undefined;
  const bgBrightness = lerp(0.66, 0.52, p);

  const windowRect: React.CSSProperties = {
    position: 'absolute',
    left: g.left,
    top: g.top,
    width: g.w,
    height: g.h,
    borderRadius: g.radius,
    overflow: 'hidden',
  };
  const scaled: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: W, height: H, transform: `scale(${g.s})`, transformOrigin: '0 0'};

  return (
    <>
      {/* ── fill that appears around the shrunken window ─────────────────────── */}
      {p > 0.001 && (
        <div style={{position: 'absolute', inset: 0, overflow: 'hidden', background: colors.navyDeep, opacity: Math.min(1, p * 2.2)}}>
          <div style={{width: 270, height: 480, transform: 'scale(4)', transformOrigin: '0 0', filter: 'blur(7px) brightness(0.45) saturate(1.3)'}}>
            <OffthreadVideo src={FOOTAGE} style={{width: 270, height: 480}} />
          </div>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background:
                'radial-gradient(120% 60% at 50% 18%, rgba(24,92,255,0.30) 0%, rgba(0,32,120,0.20) 45%, rgba(2,8,34,0.78) 100%)',
            }}
          />
          <Atmosphere t={t + 3.1} intensity={1.15} />
        </div>
      )}

      {/* ── background layer of the window (graded + softly blurred footage, atmosphere, glass banners) ── */}
      <div style={{...windowRect, background: p > 0.001 ? undefined : colors.navyDeep, WebkitMaskImage: mask, maskImage: mask}}>
        <div style={scaled}>
          {cut ? (
            <>
              <div style={{position: 'absolute', inset: 0, transform: `scale(${1 + z})`, transformOrigin: FACE_ORIGIN}}>
                <OffthreadVideo
                  src={FOOTAGE}
                  style={{width: W, height: H, filter: `brightness(${bgBrightness}) saturate(0.82) contrast(1.08) blur(5px)`}}
                />
              </div>
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'linear-gradient(180deg, rgba(0,26,110,0.62) 0%, rgba(0,32,120,0.28) 40%, rgba(2,10,44,0.50) 100%)',
                }}
              />
              <Atmosphere t={t} intensity={1} />
              {behind}
            </>
          ) : (
            <>
              <div style={{position: 'absolute', inset: 0, transform: `scale(${1 + z})`, transformOrigin: FACE_ORIGIN}}>
                <OffthreadVideo src={FOOTAGE} style={{width: W, height: H}} />
              </div>
              <Atmosphere t={t} intensity={0.55} />
              {behind}
            </>
          )}
        </div>
      </div>

      {/* ── the speaker, sharp, with a faint brand-blue rim light (kept outside the fading mask) ── */}
      {cut && (
        <div style={{...windowRect, boxShadow: p > 0.001 ? '0 40px 120px rgba(0,8,40,0.55)' : undefined}}>
          <div style={scaled}>
            <div style={{position: 'absolute', inset: 0, transform: `scale(${1 + z})`, transformOrigin: FACE_ORIGIN}}>
              <OffthreadVideo
                src={SPEAKER}
                transparent
                style={{width: W, height: H, filter: 'drop-shadow(0 0 22px rgba(70,165,255,0.38))'}}
              />
            </div>
          </div>
        </div>
      )}

      {/* ── glass frame around the window ────────────────────────────────────── */}
      {p > 0.02 && (
        <div
          style={{
            position: 'absolute',
            left: g.left - 3,
            top: g.top - 3,
            width: g.w + 6,
            height: g.h + 6,
            opacity: Math.min(1, p * 1.6),
            WebkitMaskImage: 'linear-gradient(to bottom, transparent 0%, transparent 22%, #000 52%)',
            maskImage: 'linear-gradient(to bottom, transparent 0%, transparent 22%, #000 52%)',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              position: 'absolute',
              inset: 0,
              borderRadius: g.radius + 3,
              padding: 3,
              background:
                'linear-gradient(160deg, rgba(255,255,255,0.95), rgba(138,212,255,0.35) 22%, rgba(255,255,255,0.05) 55%, rgba(92,240,176,0.7))',
              WebkitMask: 'linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)',
              WebkitMaskComposite: 'xor',
              maskComposite: 'exclude',
            }}
          />
        </div>
      )}
    </>
  );
};
