import React from 'react';

export type GlassTint = 'blue' | 'green' | 'duo' | 'navy' | 'white';

export const TINTS: Record<GlassTint, {a: string; b: string; glow: string; edge: string}> = {
  blue: {a: 'rgba(40,125,255,0.30)', b: 'rgba(6,28,112,0.55)', glow: 'rgba(45,156,255,0.50)', edge: 'rgba(150,215,255,0.9)'},
  green: {a: 'rgba(16,185,129,0.34)', b: 'rgba(4,68,72,0.55)', glow: 'rgba(16,185,129,0.50)', edge: 'rgba(130,255,205,0.9)'},
  duo: {a: 'rgba(12,160,115,0.46)', b: 'rgba(10,72,200,0.60)', glow: 'rgba(40,205,205,0.60)', edge: 'rgba(170,255,235,0.95)'},
  navy: {a: 'rgba(22,56,160,0.30)', b: 'rgba(3,12,52,0.66)', glow: 'rgba(45,120,255,0.38)', edge: 'rgba(165,205,255,0.75)'},
  white: {a: 'rgba(255,255,255,0.34)', b: 'rgba(255,255,255,0.12)', glow: 'rgba(255,255,255,0.35)', edge: 'rgba(255,255,255,0.95)'},
};

export type GlassProps = {
  x: number;
  y: number;
  w: number;
  h: number;
  radius?: number;
  tint?: GlassTint;
  /** override glow colour */
  glow?: string;
  /** 0..1.5 – strength of the coloured outer glow */
  glowStrength?: number;
  blur?: number;
  /** 0..1 position of a light sheen travelling across the glass (null = none) */
  sheen?: number | null;
  rotateX?: number;
  rotateY?: number;
  rotateZ?: number;
  scale?: number;
  tx?: number;
  ty?: number;
  opacity?: number;
  /** stretch along x to fake motion smear on fast slides (1 = none) */
  smear?: number;
  children?: React.ReactNode;
  style?: React.CSSProperties;
};

/**
 * Frosted-glass panel: real backdrop blur of whatever is behind it, tinted body, specular band,
 * bright gradient hairline edge, inner highlight, coloured outer glow and a travelling light sheen.
 */
export const Glass: React.FC<GlassProps> = ({
  x,
  y,
  w,
  h,
  radius = 44,
  tint = 'blue',
  glow,
  glowStrength = 1,
  blur = 26,
  sheen = null,
  rotateX = 0,
  rotateY = 0,
  rotateZ = 0,
  scale = 1,
  tx = 0,
  ty = 0,
  opacity = 1,
  smear = 1,
  children,
  style,
}) => {
  const c = TINTS[tint];
  const glowColor = glow ?? c.glow;
  if (opacity <= 0.001) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: w,
        height: h,
        opacity,
        transform: `translate3d(${tx}px, ${ty}px, 0) perspective(1800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) rotateZ(${rotateZ}deg) scale(${scale * smear}, ${scale})`,
        ...style,
      }}
    >
      {/* coloured glow + ground shadow */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: radius,
          boxShadow: `0 0 ${90 * glowStrength}px ${4 * glowStrength}px ${glowColor}, 0 46px 90px -24px rgba(0,6,32,0.65)`,
        }}
      />
      {/* glass body */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: radius,
          overflow: 'hidden',
          background: `linear-gradient(135deg, ${c.a} 0%, ${c.b} 100%)`,
          backdropFilter: `blur(${blur}px) saturate(1.7) brightness(1.04)`,
          WebkitBackdropFilter: `blur(${blur}px) saturate(1.7) brightness(1.04)`,
          boxShadow:
            'inset 0 2px 0 rgba(255,255,255,0.62), inset 0 -2px 0 rgba(255,255,255,0.10), inset 0 0 70px rgba(150,215,255,0.13), inset 2px 0 0 rgba(0,235,255,0.16), inset -2px 0 0 rgba(255,70,150,0.12)',
        }}
      >
        {/* specular band */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'linear-gradient(118deg, rgba(255,255,255,0.26) 0%, rgba(255,255,255,0.05) 28%, rgba(255,255,255,0) 52%, rgba(255,255,255,0.10) 100%)',
          }}
        />
        {/* top rim light */}
        <div
          style={{
            position: 'absolute',
            left: radius * 0.6,
            right: radius * 0.6,
            top: 0,
            height: 3,
            background: 'linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.85), rgba(255,255,255,0))',
            filter: 'blur(1px)',
          }}
        />
        {sheen !== null && sheen > 0 && sheen < 1 && (
          <div
            style={{
              position: 'absolute',
              top: -30,
              bottom: -30,
              width: '34%',
              left: `${-45 + sheen * 190}%`,
              transform: 'skewX(-20deg)',
              background: 'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.62) 50%, rgba(255,255,255,0) 100%)',
              mixBlendMode: 'screen',
              filter: 'blur(7px)',
            }}
          />
        )}
      </div>
      {/* gradient hairline edge */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          borderRadius: radius,
          padding: 2,
          background: `linear-gradient(135deg, rgba(255,255,255,0.98), rgba(255,255,255,0.18) 26%, rgba(255,255,255,0.05) 58%, ${c.edge})`,
          WebkitMask: 'linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)',
          WebkitMaskComposite: 'xor',
          maskComposite: 'exclude',
          pointerEvents: 'none',
        }}
      />
      <div style={{position: 'absolute', inset: 0}}>{children}</div>
    </div>
  );
};
