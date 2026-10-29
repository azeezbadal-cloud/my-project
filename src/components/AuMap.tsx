import React, {useEffect, useRef} from 'react';
import {geoGraticule10, geoPath} from 'd3-geo';
import coastJson from '../data/au-coast.json';
import dotsCoarse from '../data/au-dots.json';
import dotsFine from '../data/au-dots-east.json';
import {config} from '../config';
import {TL, cityTimes} from '../timeline';
import {clamp01, easeOutCubic, prog} from '../lib/anim';
import {MAP_RECT, projectionAt, zoomE} from '../map/geo';

const BASE: [number, number, number] = [64, 132, 255];
const SKY: [number, number, number] = [190, 232, 255];
const MINT: [number, number, number] = [120, 250, 195];

const smooth = (a: number, b: number, x: number) => {
  const t = clamp01((x - a) / (b - a));
  return t * t * (3 - 2 * t);
};

type Pin = {x: number; y: number; land: number; home: boolean};

/** Dot-matrix Australia with a radial reveal from Wagga Wagga, glowing hotspots and a soft coastline. */
export const AuMap: React.FC<{t: number}> = ({t}) => {
  const ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const cv = ref.current;
    const ctx = cv?.getContext('2d');
    if (!cv || !ctx) return;
    ctx.clearRect(0, 0, cv.width, cv.height);
    ctx.save();
    ctx.translate(-MAP_RECT.x, -MAP_RECT.y);

    const proj = projectionAt(t);
    const scale = proj.scale();
    const ex = config.expansion;
    const home = proj([ex.home.lon, ex.home.lat]) as [number, number];
    const e = zoomE(t);

    const reveal = easeOutCubic(prog(t, TL.expansion.mapIn, 1.2));
    const R = reveal * 0.78 * scale; // px radius of the reveal wave
    const edge = 0.05 * scale;

    // hotspots (home + planned cities that have landed)
    const pins: Pin[] = [{x: home[0], y: home[1], land: TL.expansion.homeLand, home: true}];
    ex.cities.forEach((c, k) => {
      const p = proj([c.lon, c.lat]) as [number, number];
      pins.push({x: p[0], y: p[1], land: cityTimes(k).land, home: false});
    });
    const sigma = 0.03 * scale;

    // graticule (very faint)
    if (reveal > 0.05) {
      ctx.save();
      ctx.globalAlpha = 0.07 * reveal;
      ctx.strokeStyle = '#9fd0ff';
      ctx.lineWidth = 1;
      ctx.beginPath();
      geoPath(proj, ctx)(geoGraticule10());
      ctx.stroke();
      ctx.restore();
    }

    // dots
    const fineA = smooth(0.4, 0.9, e);
    const coarseA = 1 - smooth(0.3, 0.85, e);
    const drawSet = (dots: number[][], alpha: number, r: number) => {
      if (alpha <= 0.01) return;
      for (let i = 0; i < dots.length; i++) {
        const p = proj(dots[i] as [number, number]);
        if (!p) continue;
        const x = p[0];
        const y = p[1];
        if (x < -8 || x > 1088 || y < MAP_RECT.y - 8 || y > MAP_RECT.y + MAP_RECT.h + 8) continue;
        const d = Math.hypot(x - home[0], y - home[1]);
        const a0 = clamp01((R - d) / edge);
        if (a0 <= 0) continue;
        // heat from nearby hotspots
        let heat = 0;
        let hot = SKY;
        for (let k = 0; k < pins.length; k++) {
          const pn = pins[k];
          const age = t - pn.land;
          if (age < 0) continue;
          const dd = Math.hypot(x - pn.x, y - pn.y) / sigma;
          const h = Math.exp(-dd * dd) * (0.55 + 0.45 * Math.sin(age * 3 + k)) * easeOutCubic(clamp01(age / 0.5));
          if (h > heat) {
            heat = h;
            hot = pn.home ? MINT : SKY;
          }
        }
        // soft travelling shimmer across the land
        const wave = 0.5 + 0.5 * Math.sin(d / (0.05 * scale) - t * 2.2);
        const a = alpha * a0 * (0.5 + 0.22 * wave + heat * 0.6);
        const mixR = Math.round(BASE[0] + (hot[0] - BASE[0]) * heat);
        const mixG = Math.round(BASE[1] + (hot[1] - BASE[1]) * heat);
        const mixB = Math.round(BASE[2] + (hot[2] - BASE[2]) * heat);
        ctx.globalAlpha = Math.min(1, a);
        ctx.fillStyle = `rgb(${mixR},${mixG},${mixB})`;
        const rr = r * (1 + heat * 0.7);
        ctx.beginPath();
        ctx.arc(x, y, rr, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
    };
    drawSet(dotsCoarse as number[][], coarseA, 0.0004 * scale + 1.4);
    drawSet(dotsFine as number[][], fineA, 0.00112 * scale);

    // coastline, revealed by the same expanding circle
    if (reveal > 0.02) {
      ctx.save();
      ctx.beginPath();
      ctx.arc(home[0], home[1], R, 0, Math.PI * 2);
      ctx.clip();
      ctx.beginPath();
      geoPath(proj, ctx)(coastJson as never);
      ctx.fillStyle = 'rgba(40,110,255,0.10)';
      ctx.fill();
      ctx.strokeStyle = 'rgba(150,215,255,0.7)';
      ctx.lineWidth = 1.8;
      ctx.shadowColor = 'rgba(45,156,255,0.95)';
      ctx.shadowBlur = 16;
      ctx.stroke();
      ctx.restore();
    }
    ctx.restore();
  }, [t]);

  const fade = `linear-gradient(to bottom, transparent 0px, #000 130px, #000 ${MAP_RECT.h - 90}px, transparent ${MAP_RECT.h}px)`;
  return (
    <canvas
      ref={ref}
      width={MAP_RECT.w}
      height={MAP_RECT.h}
      style={{position: 'absolute', left: MAP_RECT.x, top: MAP_RECT.y, WebkitMaskImage: fade, maskImage: fade}}
    />
  );
};
