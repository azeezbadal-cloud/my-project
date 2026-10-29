import React from 'react';
import {config} from '../config';
import {TL} from '../timeline';
import {band, colors, fonts} from '../theme';
import {easeOutCubic, prog, pulse} from '../lib/anim';
import {slideState} from '../lib/slide';
import {useT} from '../lib/useT';
import {Glass} from '../components/Glass';
import {SplitText} from '../components/SplitText';

const fill = {position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'} as const;

/** 00:00 – 00:03  A glass banner sweeps in: "WELCOME TO OUR COMMUNITY" → "WAGGA WAGGA COMMUNITY CARE" */
export const Welcome: React.FC = () => {
  const {frame, fps, t} = useT();
  const T = TL.welcome;
  const c = config.welcome;
  const s = slideState(frame, fps, T.panelIn, T.panelOut, -1250, -1300, {damping: 22, stiffness: 80, mass: 1.05});
  if (s.done || !s.started) return null;

  const sheen = prog(t, T.sweep, 0.85);
  const glow = 0.85 + 0.7 * pulse(t, T.panelIn + 0.55, 0.6) + 0.5 * pulse(t, T.sweep + 0.4, 0.5);
  const accentW = 330 * easeOutCubic(prog(t, T.title + 0.55, 0.6));

  return (
    <Glass
      x={band.x}
      y={band.y}
      w={band.w}
      h={band.h}
      tint="blue"
      tx={s.tx}
      smear={s.smear}
      rotateY={s.lean * -16}
      glowStrength={glow}
      sheen={sheen}
    >
      <div style={fill}>
        <SplitText
          text={c.eyebrow}
          t={t}
          start={T.eyebrow}
          stagger={0.026}
          dur={0.5}
          outStart={T.eyebrowOut}
          style={{fontFamily: fonts.display, fontWeight: 700, fontSize: 39, letterSpacing: '0.16em', position: 'absolute'}}
        />
      </div>
      <div style={{...fill, paddingBottom: 10}}>
        <SplitText
          text={c.title[0]}
          t={t}
          start={T.title}
          stagger={0.034}
          dur={0.55}
          sweep={sheen}
          colorFrom="#FFFFFF"
          colorTo="#CBE8FF"
          style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 90, lineHeight: 1, letterSpacing: '0.02em'}}
        />
        <SplitText
          text={c.title[1]}
          t={t}
          start={T.title + 0.28}
          stagger={0.03}
          dur={0.55}
          sweep={sheen}
          colorFrom={colors.mint}
          colorTo={colors.sky}
          glow="rgba(60,230,170,0.45)"
          style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 53, lineHeight: 1.05, letterSpacing: '0.12em', marginTop: 6}}
        />
        <div
          style={{
            marginTop: 12,
            height: 3,
            width: accentW,
            borderRadius: 3,
            background: `linear-gradient(90deg, rgba(255,226,160,0), ${colors.goldSoft}, rgba(255,226,160,0))`,
            boxShadow: `0 0 14px ${colors.gold}`,
          }}
        />
      </div>
    </Glass>
  );
};
