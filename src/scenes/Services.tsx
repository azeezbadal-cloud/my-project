import React from 'react';
import {config, ServiceItem} from '../config';
import {TL, serviceTimes} from '../timeline';
import {accent, band, fonts} from '../theme';
import {clamp01, easeInCubic, easeInOutCubic, easeOutCubic, prog, sp} from '../lib/anim';
import {slideState} from '../lib/slide';
import {useT} from '../lib/useT';
import {Glass, GlassTint} from '../components/Glass';
import {SplitText} from '../components/SplitText';
import {Icon} from '../components/Icon';

const TINT_FOR: Record<ServiceItem['accent'], GlassTint> = {blue: 'blue', green: 'green', aqua: 'blue', gold: 'navy'};

const fill = {position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'} as const;

const Heading: React.FC = () => {
  const {frame, fps, t} = useT();
  const T = TL.services;
  const c = config.services;
  const s = slideState(frame, fps, T.headingIn, T.headingOut, 1250, -1300, {damping: 18, stiffness: 100, mass: 0.95});
  if (s.done || !s.started) return null;
  const sheen = prog(t, T.headingIn + 0.55, 0.7);
  return (
    <Glass x={band.x} y={band.y} w={band.w} h={band.h} tint="blue" tx={s.tx} smear={s.smear} rotateY={s.lean * -16} sheen={sheen} glowStrength={1.1}>
      <div style={fill}>
        <SplitText
          text={c.heading[0]}
          t={t}
          start={T.headingIn + 0.15}
          stagger={0.028}
          dur={0.5}
          sweep={sheen}
          colorFrom="#FFFFFF"
          colorTo="#CBE8FF"
          style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 58, lineHeight: 1.05, letterSpacing: '0.02em'}}
        />
        <SplitText
          text={c.heading[1]}
          t={t}
          start={T.headingIn + 0.3}
          stagger={0.03}
          dur={0.5}
          sweep={sheen}
          colorFrom={colors_mint}
          colorTo={colors_sky}
          glow="rgba(60,230,170,0.45)"
          style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 58, lineHeight: 1.05, letterSpacing: '0.1em'}}
        />
      </div>
    </Glass>
  );
};

const colors_mint = '#5CF0B0';
const colors_sky = '#8AD4FF';

const Card: React.FC<{k: number; item: ServiceItem}> = ({k, item}) => {
  const {frame, fps, t} = useT();
  const sv = serviceTimes();
  const e = sv.enter(k);
  if (t < e - 0.02) return null;

  // how many newer cards sit in front of this one (smoothly animated)
  let level = 0;
  for (let j = k + 1; j < sv.n; j++) level += easeInOutCubic(prog(t, sv.enter(j), 0.42));

  // everything swipes away together at the end of the section
  const exitAt = config.services.end - 0.2 + level * 0.035;
  const exitX = -easeInCubic(prog(t, exitAt, 0.3)) * 1350;
  if (exitX <= -1349) return null;

  const pin = sp(frame, fps, e, {damping: 17, stiffness: 115, mass: 0.9});
  const prevPin = sp(frame - 1, fps, e, {damping: 17, stiffness: 115, mass: 0.9});
  const tx = (1 - pin) * 1150 + exitX;
  const dx = (1 - pin) * 1150 - (1 - prevPin) * 1150;
  const smear = 1 + Math.min(0.28, Math.abs(dx) / 1000);
  const opacity = clamp01(1 - level * 0.36);
  if (opacity <= 0) return null;

  const ac = accent(item.accent);
  const tileScale = 0.55 + 0.45 * sp(frame, fps, e + 0.1, {damping: 11, stiffness: 170, mass: 0.8});
  const draw = prog(t, e + 0.12, 0.55);
  const fillGlow = easeOutCubic(prog(t, e + 0.55, 0.3));
  const sheen = prog(t, e + 0.28, 0.7);
  const bar = prog(t, e + 0.2, sv.d - 0.1);
  const ring = prog(t, e + 0.34, 0.6);
  const showContent = level < 0.9;

  return (
    <Glass
      x={band.x}
      y={band.y + 4}
      w={band.w}
      h={198}
      radius={42}
      tint={TINT_FOR[item.accent]}
      glow={ac.glow}
      glowStrength={0.75}
      tx={tx}
      ty={-level * 28}
      scale={Math.pow(0.945, level)}
      opacity={opacity}
      smear={smear}
      rotateY={Math.max(-1, Math.min(1, (1 - pin) * 1.2)) * -18}
      sheen={sheen}
    >
      {showContent && (
        <>
          {/* icon tile */}
          <div
            style={{
              position: 'absolute',
              left: 34,
              top: 37,
              width: 124,
              height: 124,
              borderRadius: 34,
              transform: `scale(${tileScale})`,
              background: `linear-gradient(145deg, ${ac.soft} -25%, ${ac.main} 42%, color-mix(in srgb, ${ac.main} 45%, #001030) 125%)`,
              boxShadow: `0 0 44px ${ac.glow}, inset 0 2px 0 rgba(255,255,255,0.6), inset 0 -12px 26px rgba(0,10,50,0.22)`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Icon name={item.icon} size={78} draw={draw} fill={fillGlow} color="#FFFFFF" glow="rgba(255,255,255,0.75)" strokeWidth={1.8} />
          </div>
          {/* digital pulse ring */}
          {ring > 0 && ring < 1 && (
            <div
              style={{
                position: 'absolute',
                left: 34 + 62 - 62,
                top: 37,
                width: 124,
                height: 124,
                borderRadius: 34,
                border: `3px solid ${ac.soft}`,
                opacity: (1 - ring) * 0.5,
                transform: `scale(${1 + easeOutCubic(ring) * 0.55})`,
              }}
            />
          )}
          {/* text */}
          <div style={{position: 'absolute', left: 184, right: 60, top: 0, bottom: 12, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
            <SplitText
              text={item.lines[0]}
              t={t}
              start={e + 0.16}
              stagger={0.016}
              dur={0.4}
              rise={30}
              blur={8}
              rotate={-35}
              popScale={0.1}
              glow={ac.glow}
              style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 54, lineHeight: 1.12, color: '#fff'}}
            />
            <SplitText
              text={item.lines[1]}
              t={t}
              start={e + 0.24}
              stagger={0.016}
              dur={0.4}
              rise={30}
              blur={8}
              rotate={-35}
              popScale={0.1}
              glow={ac.glow}
              colorFrom="#FFFFFF"
              colorTo={ac.soft}
              style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 58, lineHeight: 1.12}}
            />
          </div>
          {/* counter */}
          <div
            style={{
              position: 'absolute',
              right: 34,
              top: 26,
              fontFamily: fonts.body,
              fontWeight: 700,
              fontSize: 23,
              letterSpacing: '0.12em',
              color: ac.soft,
              opacity: 0.85,
            }}
          >
            {String(k + 1).padStart(2, '0')} / {String(sv.n).padStart(2, '0')}
          </div>
          {/* time bar */}
          <div style={{position: 'absolute', left: 184, right: 60, bottom: 20, height: 4, borderRadius: 4, background: 'rgba(255,255,255,0.14)'}}>
            <div style={{width: `${bar * 100}%`, height: '100%', borderRadius: 4, background: ac.soft, boxShadow: `0 0 12px ${ac.main}`}} />
          </div>
        </>
      )}
    </Glass>
  );
};

/** 00:06 – 00:14  Heading, then seven service cards swiping in one after another with animated icons. */
export const Services: React.FC = () => {
  const {t} = useT();
  if (t < config.services.start - 0.1 || t > config.services.end + 0.1) return null;
  return (
    <>
      <Heading />
      {config.services.items.map((item, k) => (
        <Card key={k} k={k} item={item} />
      ))}
    </>
  );
};
