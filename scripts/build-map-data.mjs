// Builds the data for the animated Australia map (dot-matrix land + coastline) from Natural Earth
// (public domain, via the `world-atlas` npm package).   Run:  npm run build:map
// Output (committed – you rarely need to re-run this):
//   src/data/au-dots.json       coarse dots, whole continent (wide shot)
//   src/data/au-dots-east.json  fine dots, eastern + southern Australia (zoomed shot)
//   src/data/au-coast.json      simplified coastline
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {feature} from 'topojson-client';
import {geoContains, geoMercator, geoArea} from 'd3-geo';

const require = createRequire(import.meta.url);
const topo = JSON.parse(fs.readFileSync(require.resolve('world-atlas/countries-50m.json'), 'utf8'));
const countries = feature(topo, topo.objects.countries);
const aus = countries.features.find((f) => String(f.id) === '036' || f.properties?.name === 'Australia');
if (!aus) throw new Error('Australia not found in dataset');

const round = (n, d = 2) => Math.round(n * 10 ** d) / 10 ** d;
const polys = aus.geometry.type === 'MultiPolygon' ? aus.geometry.coordinates : [aus.geometry.coordinates];

// ── coastline: drop tiny islands, thin the rings, round the coordinates ─────────────────────────
const keep = [];
for (const poly of polys) {
  const deg2 = geoArea({type: 'Feature', geometry: {type: 'Polygon', coordinates: poly}}) * (180 / Math.PI) ** 2;
  if (deg2 < 0.6) continue; // keep mainland + Tasmania
  const ring = poly[0];
  const step = ring.length > 1500 ? 2 : 1;
  keep.push([ring.filter((_, i) => i % step === 0 || i === ring.length - 1).map(([x, y]) => [round(x), round(y)])]);
}
const coast = {type: 'Feature', properties: {name: 'Australia'}, geometry: {type: 'MultiPolygon', coordinates: keep}};

// ── dot matrix: hexagonal grid in Mercator space, kept where it falls on land ───────────────────
const proj = geoMercator().scale(1).translate([0, 0]);
const land = {type: 'Feature', geometry: {type: 'MultiPolygon', coordinates: polys}};

const grid = (S, [lonMin, latMax], [lonMax, latMin]) => {
  const [x0, y0] = proj([lonMin, latMax]);
  const [x1, y1] = proj([lonMax, latMin]);
  const dots = [];
  let row = 0;
  for (let y = y0; y <= y1; y += S * 0.866, row++) {
    for (let x = x0 + (row % 2 ? S / 2 : 0); x <= x1; x += S) {
      const ll = proj.invert([x, y]);
      if (geoContains(land, ll)) dots.push([round(ll[0], 3), round(ll[1], 3)]);
    }
  }
  return dots;
};

const coarse = grid(0.0072, [112, -9], [154.5, -44]);
const fine = grid(0.0031, [127, -21], [156, -44.5]);

const outDir = path.resolve('src/data');
fs.mkdirSync(outDir, {recursive: true});
fs.writeFileSync(path.join(outDir, 'au-dots.json'), JSON.stringify(coarse));
fs.writeFileSync(path.join(outDir, 'au-dots-east.json'), JSON.stringify(fine));
fs.writeFileSync(path.join(outDir, 'au-coast.json'), JSON.stringify(coast));
console.log(`coarse dots: ${coarse.length}  fine dots: ${fine.length}  coast polygons: ${keep.length}`);
