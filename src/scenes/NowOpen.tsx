import React from 'react';
import {config} from '../config';
import {TL} from '../timeline';
import {band, fonts} from '../theme';
import {prog, pulse} from '../lib/anim';
import {mixRgba, slideState} from '../lib/slide';
import {useT} from '../lib/useT';
import {Glass} from '../components/Glass';
import {SplitText} from '../components/SplitText';
import {Sparkles} from '../components/Sparkles';

const fill = {position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'} as const;

/** 00:03 – 00:06  "WE'RE NOW OPEN!" on glowing green-and-blue glass, with a celebratory sparkle. */
export const NowOpen: React.FC = () => {
  const {frame, fps, t} = useT();
  const T = TL.open;
  const c = config.open;
  const s = slideState(frame, fps, T.panelIn, T.panelOut, 1250, -1300, {damping: 15, stiffness: 105, mass: 0.95});
  if (s.done || !s.started) return null;

  // glow slowly breathes between emerald and bright blue
  const mixT = 0.5 + 0.5 * Math.sin((t - T.panelIn) * 2.6);
  const glow = mixRgba([16, 200, 140, 0.62], [40, 130, 255, 0.62], mixT);
  const strength = 1.1 + 0.9 * pulse(t, T.sparkle, 0.55);
  const sheen = prog(t, T.headline + 0.5, 0.9);

  return (
    <>
      <Glass
        x={band.x}
        y={band.y - 6}
        w={band.w}
        h={band.h + 12}
        tint="duo"
        glow={glow}
        glowStrength={strength}
        tx={s.tx}
        smear={s.smear}
        rotateY={s.lean * -18}
        sheen={sheen}
      >
        <div style={{...fill, paddingBottom: 6}}>
          <SplitText
            text={c.headline}
            t={t}
            start={T.headline}
            stagger={0.036}
            dur={0.55}
            popScale={0.45}
            rise={70}
            sweep={sheen}
            colorFrom="#FFFFFF"
            colorTo="#D9FFF0"
            glow="rgba(80,255,190,0.55)"
            style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 84, lineHeight: 1, letterSpacing: '0.015em'}}
          />
          <SplitText
            text={c.subline}
            t={t}
            start={T.subline}
            stagger={0.012}
            dur={0.45}
            rise={22}
            blur={6}
            rotate={0}
            popScale={0}
            glow="rgba(0,40,120,0.5)"
            style={{fontFamily: fonts.body, fontWeight: 600, fontSize: 34, marginTop: 16, letterSpacing: '0.015em', color: '#fff'}}
          />
        </div>
      </Glass>
      <Sparkles t={t} start={T.sparkle} cx={540} cy={band.y + 105} radius={440} count={26} seed={3} />
      <Sparkles t={t} start={T.sparkle + 0.18} cx={300} cy={band.y + 60} radius={220} count={10} seed={7} dur={1.0} />
      <Sparkles t={t} start={T.sparkle + 0.1} cx={790} cy={band.y + 60} radius={220} count={10} seed={11} dur={1.0} />
      {/* light ring that blooms behind the headline on the sparkle */}
      <div
        style={{
          position: 'absolute',
          left: 540 - 520,
          top: band.y + 105 - 130,
          width: 1040,
          height: 260,
          borderRadius: '50%',
          background: `radial-gradient(closest-side, rgba(120,255,210,${0.38 * pulse(t, T.sparkle + 0.1, 0.5)}), rgba(40,140,255,0))`,
          mixBlendMode: 'screen',
          pointerEvents: 'none',
        }}
      />
    </>
  );
};

