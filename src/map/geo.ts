import {geoMercator} from 'd3-geo';
import {TL} from '../timeline';
import {easeInOutCubic, lerp, prog} from '../lib/anim';

/** Region of the 1080×1920 canvas occupied by the map canvas. */
export const MAP_RECT = {x: 0, y: 250, w: 1080, h: 770};

// Camera: starts on the whole continent, then pushes in on the east coast.
const WIDE = {lon: 133.4, lat: -27.0, scale: 800, cx: 540, cy: 662};
const EAST = {lon: 150.05, lat: -31.6, scale: 2350, cx: 500, cy: 706};

export const zoomE = (t: number) => easeInOutCubic(prog(t, TL.expansion.zoom, 0.9));

export const projectionAt = (t: number) => {
  const e = zoomE(t);
  const scale = Math.exp(lerp(Math.log(WIDE.scale), Math.log(EAST.scale), e));
  return geoMercator()
    .center([lerp(WIDE.lon, EAST.lon, e), lerp(WIDE.lat, EAST.lat, e)])
    .scale(scale)
    .translate([lerp(WIDE.cx, EAST.cx, e), lerp(WIDE.cy, EAST.cy, e)]);
};
