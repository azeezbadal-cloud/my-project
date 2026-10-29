import React from 'react';
import {config} from '../config';
import {TL, cityTimes} from '../timeline';
import {band, colors, fonts} from '../theme';
import {clamp01, easeInCubic, easeInOutCubic, easeOutCubic, prog, pulse, sp} from '../lib/anim';
import {slideState} from '../lib/slide';
import {useT} from '../lib/useT';
import {Glass} from '../components/Glass';
import {GlassChip} from '../components/GlassChip';
import {SplitText} from '../components/SplitText';
import {AuMap} from '../components/AuMap';
import {windowProgress} from '../components/VideoStage';
import {projectionAt} from '../map/geo';

const PIN_PATH = 'M24 2C12.4 2 3 11.4 3 23c0 15.6 21 39 21 39s21-23.4 21-39C45 11.4 35.6 2 24 2z';

type XY = [number, number];

const arc = (p0: XY, p1: XY) => {
  const dx = p1[0] - p0[0];
  const dy = p1[1] - p0[1];
  const len = Math.hypot(dx, dy) || 1;
  let nx = dy / len;
  let ny = -dx / len;
  if (ny > 0) {
    nx = -nx;
    ny = -ny; // always bulge upwards
  }
  const c: XY = [(p0[0] + p1[0]) / 2 + nx * len * 0.24, (p0[1] + p1[1]) / 2 + ny * len * 0.24];
  const at = (u: number): XY => [
    (1 - u) * (1 - u) * p0[0] + 2 * (1 - u) * u * c[0] + u * u * p1[0],
    (1 - u) * (1 - u) * p0[1] + 2 * (1 - u) * u * c[1] + u * u * p1[1],
  ];
  return {d: `M${p0[0]} ${p0[1]} Q${c[0]} ${c[1]} ${p1[0]} ${p1[1]}`, at};
};

type PinProps = {x: number; y: number; t: number; frame: number; fps: number; land: number; home?: boolean; size: number};

const MapPin: React.FC<PinProps> = ({x, y, t, frame, fps, land, home, size}) => {
  const d = sp(frame, fps, land - 0.14, {damping: 9, stiffness: 170, mass: 0.7});
  if (t < land - 0.16) return null;
  const yOff = -Math.max(0, 1 - d) * 200;
  const squash = 0.14 * pulse(t, land + 0.03, 0.13);
  const s = size / 64;
  const age = t - land;
  const col = home ? colors.mint : colors.sky;
  // ripples on the ground
  const rings = [0, 0.38, 0.76].map((off, i) => {
    const cycle = home ? 1.9 : 2.3;
    const a = age - off;
    if (a < 0) return null;
    const p = (a % cycle) / cycle;
    const strength = a < cycle ? 1 : 0.45;
    const rx = 10 + 86 * easeOutCubic(p);
    return (
      <ellipse
        key={i}
        cx={x}
        cy={y}
        rx={rx}
        ry={rx * 0.4}
        fill="none"
        stroke={col}
        strokeWidth={2.4 * (1 - p) + 0.6}
        opacity={Math.pow(1 - p, 1.6) * 0.75 * strength}
      />
    );
  });
  return (
    <g>
      <ellipse cx={x} cy={y + 2} rx={22 * (1 - Math.max(0, 1 - d) * 0.6)} ry={7} fill="rgba(0,0,20,0.5)" opacity={clamp01(d * 2)} />
      {rings}
      <g
        transform={`translate(${x} ${y + yOff}) scale(${s * (1 + squash)} ${s * (1 - squash)}) translate(-24 -62)`}
        style={{filter: `drop-shadow(0 0 ${home ? 16 : 11}px ${home ? 'rgba(92,240,176,0.9)' : 'rgba(138,212,255,0.85)'})`}}
        opacity={clamp01(d * 5)}
      >
        {home ? (
          <>
            <path d={PIN_PATH} fill="url(#pinHome)" stroke="#fff" strokeWidth={2.5} />
            <circle cx={24} cy={23} r={9.5} fill="#fff" />
            <circle cx={24} cy={23} r={4.2} fill={colors.emerald} />
          </>
        ) : (
          <>
            <path d={PIN_PATH} fill="rgba(45,156,255,0.42)" stroke="#E6F6FF" strokeWidth={3.4} strokeDasharray="6 5" />
            <circle cx={24} cy={23} r={8.5} fill="#fff" opacity={0.65 + 0.35 * Math.sin(age * 5)} />
          </>
        )}
      </g>
    </g>
  );
};

/** 00:14 – 00:19  Floating map: Wagga Wagga first, then the planned expansion cities. */
export const Expansion: React.FC = () => {
  const {frame, fps, t} = useT();
  const T = TL.expansion;
  const ex = config.expansion;
  if (t < T.kicker - 0.3 || t > ex.end + 0.5) return null;

  const exitP = easeInCubic(prog(t, T.exit, 0.4));
  // keep the map clear of the presenter's head while the video window is still shrinking
  const wp = windowProgress(t);
  const mapGate = clamp01((wp - 0.7) / 0.25);
  const proj = projectionAt(t);
  const home = proj([ex.home.lon, ex.home.lat]) as XY;
  const homeLand = T.homeLand;

  // heading panel
  const head = slideState(frame, fps, T.kicker - 0.1, null, 1250, 0, {damping: 18, stiffness: 100, mass: 0.95});
  const headTx = head.tx - exitP * 1300;
  const tint = t < T.next ? 'green' : 'blue';
  const sheen = prog(t, T.next + 0.2, 0.8);

  // "Planned Expansion" badge
  const badgeP = easeOutCubic(prog(t, T.badge, 0.45));

  return (
    <>
      <div style={{position: 'absolute', inset: 0, opacity: (1 - exitP) * mapGate}}>
        <AuMap t={t} />
        <svg width={1080} height={1920} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          <defs>
            <linearGradient id="pinHome" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stopColor={colors.mint} />
              <stop offset="0.55" stopColor={colors.emerald} />
              <stop offset="1" stopColor="#0a7a55" />
            </linearGradient>
            <filter id="arcGlow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="5" />
            </filter>
          </defs>
          {/* arcs from Wagga Wagga to each planned city */}
          {ex.cities.map((c, k) => {
            const ct = cityTimes(k);
            const p1 = proj([c.lon, c.lat]) as XY;
            const a = arc(home, p1);
            const u = easeInOutCubic(prog(t, ct.arc, 0.55));
            if (u <= 0) return null;
            const head = a.at(u);
            const march = -(t - ct.arc) * 26;
            return (
              <g key={k}>
                <mask id={`arcMask${k}`}>
                  <path d={a.d} fill="none" stroke="#fff" strokeWidth={16} strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - u} />
                </mask>
                <g mask={`url(#arcMask${k})`}>
                  <path d={a.d} fill="none" stroke={colors.brightBlue} strokeWidth={9} opacity={0.5} filter="url(#arcGlow)" />
                  <path d={a.d} fill="none" stroke={colors.sky} strokeWidth={3.2} strokeLinecap="round" strokeDasharray="13 11" strokeDashoffset={march} />
                </g>
                {u < 1 && (
                  <>
                    <circle cx={head[0]} cy={head[1]} r={15} fill={colors.sky} opacity={0.35} filter="url(#arcGlow)" />
                    <circle cx={head[0]} cy={head[1]} r={6.5} fill="#fff" />
                  </>
                )}
              </g>
            );
          })}
          {/* pins */}
          <MapPin x={home[0]} y={home[1]} t={t} frame={frame} fps={fps} land={homeLand} home size={86} />
          {ex.cities.map((c, k) => {
            const p = proj([c.lon, c.lat]) as XY;
            return <MapPin key={k} x={p[0]} y={p[1]} t={t} frame={frame} fps={fps} land={cityTimes(k).land} size={78} />;
          })}
        </svg>

        {/* labels */}
        {ex.cities.map((c, k) => {
          const ct = cityTimes(k);
          const lp = easeOutCubic(prog(t, ct.label, 0.4));
          if (lp <= 0) return null;
          const p = proj([c.lon, c.lat]) as XY;
          const right = c.labelSide === 'right';
          const dx = (right ? -1 : 1) * (1 - lp) * 26;
          return (
            <div
              key={k}
              style={{
                position: 'absolute',
                left: right ? p[0] + 38 : undefined,
                right: right ? undefined : 1080 - (p[0] - 38),
                top: p[1] - 62 + (c.labelDy ?? 0),
                opacity: lp,
                transform: `translateX(${dx}px) scale(${0.94 + 0.06 * lp})`,
                transformOrigin: right ? '0 50%' : '100% 50%',
              }}
            >
              <GlassChip tint="blue" glow="rgba(45,156,255,0.45)" height={60}>
                <span style={{width: 12, height: 12, borderRadius: 12, background: colors.sky, boxShadow: `0 0 12px ${colors.sky}`}} />
                <span style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 33, letterSpacing: '0.07em', color: '#fff'}}>{c.name}</span>
              </GlassChip>
            </div>
          );
        })}
        {(() => {
          const lp = easeOutCubic(prog(t, homeLand + 0.1, 0.45));
          if (lp <= 0) return null;
          return (
            <div
              style={{
                position: 'absolute',
                left: home[0],
                top: home[1] + 22,
                opacity: lp,
                transform: `translate(-50%, ${(1 - lp) * 18}px)`,
              }}
            >
              <GlassChip tint="green" glow="rgba(16,185,129,0.55)" height={76} style={{flexDirection: 'column', gap: 0, justifyContent: 'center', padding: '0 34px'}}>
                <span style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 33, letterSpacing: '0.07em', color: '#fff', lineHeight: 1.1}}>{ex.home.name}</span>
                <span style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 21, letterSpacing: '0.22em', color: colors.mint, lineHeight: 1.3}}>NOW OPEN</span>
              </GlassChip>
            </div>
          );
        })()}
      </div>

      {/* heading banner */}
      {!head.done && head.started && (
        <Glass x={band.x} y={band.y} w={band.w} h={112} radius={40} tint={tint} tx={headTx} smear={head.smear} rotateY={head.lean * -16} sheen={sheen} glowStrength={1.0}>
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <SplitText
              text={ex.kicker}
              t={t}
              start={T.kicker}
              stagger={0.024}
              dur={0.5}
              outStart={T.kickerOut}
              style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 49, letterSpacing: '0.06em', position: 'absolute'}}
              colorFrom="#FFFFFF"
              colorTo={colors.mint}
              glow="rgba(60,230,170,0.45)"
            />
          </div>
          <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <SplitText
              text={ex.next}
              t={t}
              start={T.next}
              stagger={0.032}
              dur={0.5}
              sweep={sheen}
              style={{fontFamily: fonts.display, fontWeight: 800, fontSize: 58, letterSpacing: '0.1em'}}
              colorFrom="#FFFFFF"
              colorTo={colors.sky}
            />
          </div>
        </Glass>
      )}

      {/* planned-expansion badge */}
      {badgeP > 0 && (
        <div style={{position: 'absolute', right: band.x, top: band.y + 128, opacity: badgeP * (1 - exitP), transform: `translateX(${(1 - badgeP) * 60 + exitP * -900}px)`}}>
          <GlassChip tint="navy" glow="rgba(248,176,0,0.38)" height={58}>
            <svg width={26} height={26} viewBox="0 0 26 26">
              <circle cx={13} cy={13} r={10} fill="none" stroke={colors.gold} strokeWidth={2.6} strokeDasharray="4.2 3.6" />
              <circle cx={13} cy={13} r={3.6} fill={colors.goldSoft} />
            </svg>
            <span style={{fontFamily: fonts.body, fontWeight: 700, fontSize: 30, letterSpacing: '0.05em', color: colors.goldSoft}}>{ex.badge}</span>
          </GlassChip>
        </div>
      )}
    </>
  );
};
