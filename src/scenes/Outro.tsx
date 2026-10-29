import React from 'react';
import {Img, staticFile} from 'remotion';
import {config} from '../config';
import {TL} from '../timeline';
import {colors, fonts} from '../theme';
import {clamp01, easeInOutCubic, easeOutCubic, easeOutQuart, prog, pulse, sp} from '../lib/anim';
import {useT} from '../lib/useT';
import {Glass} from '../components/Glass';
import {GlassChip} from '../components/GlassChip';
import {SplitText} from '../components/SplitText';
import {Sparkles} from '../components/Sparkles';

const LOGO = staticFile(config.files.logo);

/** Vertical slices of the supplied logo artwork (fractions of its height) – emblem / wordmark / tagline. */
const EMBLEM_BOTTOM = 0.618;
const WORD_BOTTOM = 0.822;

const LogoSlice: React.FC<{size: number; clip: string; style?: React.CSSProperties}> = ({size, clip, style}) => (
  <Img src={LOGO} style={{position: 'absolute', left: 0, top: 0, width: size, height: size, clipPath: clip, ...style}} />
);

/** 00:19 – end  Light bloom → emblem → wordmark → tagline wipe, then promise line and call-to-action. */
export const Outro: React.FC = () => {
  const {frame, fps, t} = useT();
  const T = TL.outro;
  const o = config.outro;
  if (t < T.bloom - 0.7) return null;

  const contact = o.contact;
  const hasContact = Boolean(contact.website || contact.phone || contact.email);
  const L = hasContact ? 510 : 590;
  const lx = (1080 - L) / 2;
  const ly = hasContact ? 226 : 214;
  const cy = ly + L * 0.5;

  // ── light bloom ──────────────────────────────────────────────────────────────────────────
  const bp = prog(t, T.bloom - 0.15, 1.3);
  const bloomA = Math.sin(Math.PI * Math.min(1, bp)) * 0.95;
  const halo = easeOutCubic(prog(t, T.emblem, 1.0)) * (0.7 + 0.12 * Math.sin(t * 2));

  // ── logo slices ──────────────────────────────────────────────────────────────────────────
  const ep = sp(frame, fps, T.emblem, {damping: 15, stiffness: 90, mass: 1});
  const emblemA = clamp01(ep * 1.6);
  const wp = easeInOutCubic(prog(t, T.wordmark, 0.62));
  const tp = easeInOutCubic(prog(t, T.tagline, 0.5));
  const allIn = tp >= 1 && wp >= 1 && ep > 0.98;
  const sweep = prog(t, T.tagline + 0.45, 0.95);

  // ── promise line + CTA ───────────────────────────────────────────────────────────────────
  const goalsY = ly + L * 0.907 + 24;
  const ctaY = hasContact ? 868 : goalsY + 78;
  const cp = sp(frame, fps, T.cta, {damping: 15, stiffness: 100, mass: 0.95});
  const ctaSheen = prog(t, T.cta + 0.4, 0.9);
  const arrowDraw = prog(t, T.cta + 0.3, 0.5);

  return (
    <div style={{position: 'absolute', inset: 0}}>
      {/* bloom + halo */}
      <div
        style={{
          position: 'absolute',
          left: 540 - 560,
          top: cy - 560,
          width: 1120,
          height: 1120,
          opacity: bloomA,
          transform: `scale(${0.35 + 1.15 * easeOutCubic(bp)})`,
          background: 'radial-gradient(closest-side, rgba(220,240,255,0.95), rgba(70,165,255,0.45) 38%, rgba(20,80,255,0) 100%)',
          mixBlendMode: 'screen',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 540 - 420,
          top: cy - 420,
          width: 840,
          height: 840,
          opacity: halo,
          background: 'radial-gradient(closest-side, rgba(60,150,255,0.40), rgba(30,100,255,0.16) 55%, rgba(0,0,0,0) 100%)',
          mixBlendMode: 'screen',
        }}
      />

      {/* the supplied logo */}
      <div style={{position: 'absolute', left: lx, top: ly, width: L, height: L}}>
        {allIn ? (
          <Img src={LOGO} style={{position: 'absolute', inset: 0, width: L, height: L, filter: 'drop-shadow(0 12px 40px rgba(0,10,60,0.55))'}} />
        ) : (
          <>
            <LogoSlice
              size={L}
              clip={`inset(0 0 ${(1 - EMBLEM_BOTTOM) * 100}% 0)`}
              style={{
                opacity: emblemA,
                transform: `scale(${0.8 + 0.2 * ep})`,
                transformOrigin: '50% 32%',
                filter: `blur(${(1 - clamp01(ep)) * 22}px) drop-shadow(0 12px 40px rgba(0,10,60,0.55))`,
              }}
            />
            <LogoSlice
              size={L}
              clip={`inset(${EMBLEM_BOTTOM * 100}% ${(1 - wp) * 100}% ${(1 - WORD_BOTTOM) * 100}% 0)`}
              style={{filter: 'drop-shadow(0 12px 40px rgba(0,10,60,0.55))'}}
            />
            <LogoSlice
              size={L}
              clip={`inset(${WORD_BOTTOM * 100}% ${(1 - tp) * 100}% 0 0)`}
              style={{filter: 'drop-shadow(0 12px 40px rgba(0,10,60,0.55))'}}
            />
          </>
        )}
        {/* bright wipe edges */}
        {wp > 0 && wp < 1 && (
          <div
            style={{
              position: 'absolute',
              left: wp * L - 6,
              top: L * EMBLEM_BOTTOM,
              width: 12,
              height: L * (WORD_BOTTOM - EMBLEM_BOTTOM),
              background: 'linear-gradient(180deg, rgba(255,255,255,0), #fff, rgba(255,255,255,0))',
              boxShadow: '0 0 34px 10px rgba(130,210,255,0.9)',
              borderRadius: 8,
            }}
          />
        )}
        {tp > 0 && tp < 1 && (
          <div
            style={{
              position: 'absolute',
              left: tp * L - 5,
              top: L * WORD_BOTTOM,
              width: 10,
              height: L * (1 - WORD_BOTTOM) * 0.9,
              background: 'linear-gradient(180deg, rgba(255,255,255,0), #fff, rgba(255,255,255,0))',
              boxShadow: '0 0 28px 8px rgba(130,210,255,0.9)',
              borderRadius: 8,
            }}
          />
        )}
        {/* light sweep clipped to the logo's own shape */}
        {sweep > 0 && sweep < 1 && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              WebkitMaskImage: `url(${LOGO})`,
              maskImage: `url(${LOGO})`,
              WebkitMaskSize: '100% 100%',
              maskSize: '100% 100%',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                position: 'absolute',
                top: -40,
                bottom: -40,
                width: '30%',
                left: `${-40 + easeInOutCubic(sweep) * 160}%`,
                transform: 'skewX(-20deg)',
                background: 'linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.95), rgba(255,255,255,0))',
                mixBlendMode: 'overlay',
              }}
            />
          </div>
        )}
      </div>

      <Sparkles t={t} start={T.emblem + 0.35} cx={540} cy={cy - 40} radius={330} count={22} seed={5} dur={1.4} />

      {/* promise line */}
      <div style={{position: 'absolute', left: 0, right: 0, top: goalsY, display: 'flex', justifyContent: 'center'}}>
        <SplitText
          text={o.tagline}
          t={t}
          start={T.goals}
          stagger={0.028}
          dur={0.5}
          sweep={prog(t, T.goals + 0.55, 0.7)}
          colorFrom="#FFFFFF"
          colorTo={colors.goldSoft}
          glow="rgba(248,176,0,0.45)"
          style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 46, letterSpacing: '0.13em'}}
        />
      </div>

      {/* optional contact details – only rendered when you provide them in config.ts */}
      {hasContact && (
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: goalsY + 74,
            display: 'flex',
            justifyContent: 'center',
            gap: 14,
            opacity: easeOutCubic(prog(t, T.goals + 0.3, 0.5)),
          }}
        >
          {[contact.website, contact.phone, contact.email].filter(Boolean).map((v, i) => (
            <GlassChip key={i} tint="navy" height={56}>
              <span style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 27, color: '#fff', letterSpacing: '0.02em'}}>{v}</span>
            </GlassChip>
          ))}
        </div>
      )}
      {contact.qrImage && (
        <div
          style={{
            position: 'absolute',
            left: 64,
            top: ctaY - 20,
            width: 132,
            height: 132,
            padding: 10,
            borderRadius: 24,
            background: '#fff',
            opacity: easeOutCubic(prog(t, T.cta + 0.2, 0.5)),
          }}
        >
          <Img src={staticFile(contact.qrImage)} style={{width: 112, height: 112}} />
        </div>
      )}

      {/* call to action */}
      {cp > 0.001 && (
        <Glass
          x={240}
          y={ctaY}
          w={600}
          h={104}
          radius={52}
          tint="duo"
          glowStrength={1.2 + 0.5 * pulse(t, T.cta + 0.5, 0.5)}
          ty={(1 - Math.min(1.2, cp)) * 120}
          opacity={clamp01(cp * 3)}
          sheen={ctaSheen}
        >
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 20}}>
            <span
              style={{
                fontFamily: fonts.display,
                fontWeight: 800,
                fontSize: 42,
                letterSpacing: '0.12em',
                color: '#fff',
                textShadow: '0 2px 8px rgba(0,16,64,0.55), 0 0 22px rgba(80,255,190,0.5)',
              }}
            >
              {o.cta}
            </span>
            <svg width={44} height={44} viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth={2.2} strokeLinecap="round" strokeLinejoin="round" style={{filter: 'drop-shadow(0 0 8px rgba(255,255,255,0.8))'}}>
              <path d="M5 12h14" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - easeOutQuart(arrowDraw)} />
              <path d="m12 5 7 7-7 7" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - easeOutQuart(clamp01(arrowDraw * 1.3 - 0.3))} />
            </svg>
          </div>
        </Glass>
      )}

    </div>
  );
};
