/**
 * Parçacıkların dönüştüğü enerji temalı şekiller.
 * Her şekil parçacık başına 4 değer tutar: x, y, z ve w.
 *   w ≤ 1  → parçacığın görünürlüğü (0–1)
 *   w > 1  → shader'da özel davranış (dönen kanat, akan enerji, elektron…)
 *
 * Bölüm sırası (shader'daki indeksler ile aynı):
 *   0 güneş (giriş) · 1 rüzgar türbinleri (hakkımda) · 2 enerji nakil hattı (deneyim)
 *   3 atom (yetkinlikler) · 4 güneş paneli tarlası (projeler) · 5 kelime (iletişim)
 */

const TAU = Math.PI * 2;

/** Tekrarlanabilir rastgele sayı üreteci */
export function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gauss(rand) {
  let u = 0;
  while (u === 0) u = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(TAU * rand());
}

function randomDir(rand) {
  const u = rand() * 2 - 1;
  const th = rand() * TAU;
  const s = Math.sqrt(1 - u * u);
  return [s * Math.cos(th), u, s * Math.sin(th)];
}

const normalize = ([x, y, z]) => {
  const l = Math.hypot(x, y, z) || 1;
  return [x / l, y / l, z / l];
};

function put(out, i, x, y, z, w = 1) {
  const j = i * 4;
  out[j] = x;
  out[j + 1] = y;
  out[j + 2] = z;
  out[j + 3] = w;
}

/** Çizgi parçalarından uzunluklarıyla orantılı nokta seçer */
function segmentSampler(segments) {
  const cum = [];
  let total = 0;
  for (const s of segments) {
    total += Math.hypot(s[3] - s[0], s[4] - s[1], s[5] - s[2]) * (s[6] ?? 1);
    cum.push(total);
  }
  return (rand) => {
    const r = rand() * total;
    let lo = 0;
    let hi = cum.length - 1;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (cum[mid] < r) lo = mid + 1;
      else hi = mid;
    }
    const s = segments[lo];
    const t = rand();
    return [s[0] + (s[3] - s[0]) * t, s[1] + (s[4] - s[1]) * t, s[2] + (s[5] - s[2]) * t, s[7] ?? 1];
  };
}

/** Şekillerin yaklaşık ekran kaplama alanı [genişlik, yükseklik] (sahne birimi) */
export const SHAPE_BOUNDS = [
  [4.3, 4.3], // güneş
  [4.4, 5.3], // rüzgar türbinleri
  [7.2, 3.1], // enerji nakil hattı
  [4.1, 4.1], // atom
  [6.6, 2.9], // güneş paneli tarlası
];

/* Rüzgar türbinleri: göbek konumu, ölçek ve dönüş hızı (shader ile ortak) */
export const TURBINES = [
  { hub: [0.62, 0.95, 0.4], scale: 1.0, speed: 0.85 },
  { hub: [-1.5, 0.08, -1.3], scale: 0.74, speed: 1.08 },
  { hub: [-0.3, -0.5, -2.9], scale: 0.56, speed: 1.3 },
];
const GROUND_Y = -2.5;

/* 0 — Güneş: kaynayan yüzey + iç parıltı + titreşen korona ışınları + püskürmeler */
function sun(n, rand) {
  const out = new Float32Array(n * 4);
  const R = 1.55;
  const rays = Array.from({ length: 110 }, () => randomDir(rand));
  const loops = Array.from({ length: 4 }, () => {
    const a = randomDir(rand);
    const b = normalize([a[0] + gauss(rand) * 0.28, a[1] + gauss(rand) * 0.28, a[2] + gauss(rand) * 0.28]);
    return { a, b, h: 0.25 + rand() * 0.3 };
  });
  for (let i = 0; i < n; i++) {
    const k = rand();
    if (k < 0.64) {
      const [x, y, z] = randomDir(rand);
      const r = R + gauss(rand) * 0.015;
      put(out, i, x * r, y * r, z * r, 1);
    } else if (k < 0.76) {
      const [x, y, z] = randomDir(rand);
      const r = R * Math.cbrt(rand()) * 0.96;
      put(out, i, x * r, y * r, z * r, 0.5);
    } else if (k < 0.96) {
      const ray = rays[Math.floor(rand() * rays.length)];
      const [x, y, z] = normalize([ray[0] + gauss(rand) * 0.035, ray[1] + gauss(rand) * 0.035, ray[2] + gauss(rand) * 0.035]);
      const r = R * (1.02 + Math.pow(rand(), 1.9) * 0.72);
      put(out, i, x * r, y * r, z * r, 2 + rand() * 0.98); // korona
    } else {
      const l = loops[Math.floor(rand() * loops.length)];
      const t = rand();
      const d = normalize([l.a[0] * (1 - t) + l.b[0] * t, l.a[1] * (1 - t) + l.b[1] * t, l.a[2] * (1 - t) + l.b[2] * t]);
      const r = R + Math.sin(Math.PI * t) * l.h + gauss(rand) * 0.015;
      put(out, i, d[0] * r, d[1] * r, d[2] * r, 0.85);
    }
  }
  return out;
}

/* 1 — Rüzgar türbinleri: kule + nasel + göbek + dönen kanatlar + zemin + rüzgar çizgileri */
function windFarm(n, rand) {
  const out = new Float32Array(n * 4);
  const share = [0.56, 0.2, 0.12];
  const streaks = Array.from({ length: 16 }, () => ({
    x: (rand() - 0.5) * 6.4,
    y: -1.9 + rand() * 4.2,
    z: -2.5 + rand() * 3,
    len: 0.35 + rand() * 0.7,
    speed: rand() * 0.98,
  }));
  for (let i = 0; i < n; i++) {
    const k = rand();
    if (k >= 0.88) {
      if (k < 0.955) {
        // zemin: hafif dalgalı noktalı tepe
        const x = (rand() - 0.5) * 5.4;
        const z = -3.4 + rand() * 4.4;
        const y = GROUND_Y + Math.sin(x * 1.1 + z * 0.6) * 0.08 + gauss(rand) * 0.012;
        put(out, i, x, y, z, 0.26);
      } else {
        // rüzgar çizgileri (shader'da soldan sağa akar)
        const s = streaks[Math.floor(rand() * streaks.length)];
        const u = rand();
        put(out, i, s.x + u * s.len, s.y + gauss(rand) * 0.004, s.z, 5 + s.speed);
      }
      continue;
    }
    const ti = k < share[0] ? 0 : k < share[0] + share[1] ? 1 : 2;
    const { hub, scale: s } = TURBINES[ti];
    const [hx, hy, hz] = hub;
    const part = rand();
    if (part < 0.28) {
      // kule (aşağıdan yukarı incelen boru)
      const t = rand();
      const y = GROUND_Y + (hy - GROUND_Y) * t;
      const r = (0.085 - 0.04 * t) * s;
      const a = rand() * TAU;
      put(out, i, hx + Math.cos(a) * r, y, hz - 0.06 * s + Math.sin(a) * r, 0.75);
    } else if (part < 0.36) {
      // nasel (göbeğin arkasındaki gövde)
      let x = (rand() - 0.5) * 0.19;
      let y = (rand() - 0.5) * 0.17;
      let z = -rand() * 0.5;
      const f = rand();
      if (f < 0.33) x = Math.sign(x || 1) * 0.095;
      else if (f < 0.66) y = Math.sign(y || 1) * 0.085;
      else if (f < 0.8) z = -0.5;
      put(out, i, hx + x * s, hy + y * s, hz + z * s, 0.9);
    } else if (part < 0.4) {
      // göbek burnu
      const t = rand();
      const a = rand() * TAU;
      const r = 0.095 * s * Math.sqrt(1 - t);
      put(out, i, hx + Math.cos(a) * r, hy + Math.sin(a) * r, hz + 0.02 * s + t * 0.15 * s, 1);
    } else {
      // kanatlar: kök dar, %15'te en geniş, uca doğru incelir
      const b = Math.floor(rand() * 3);
      const f = Math.pow(rand(), 0.9);
      const L = 1.55 * s;
      const width = s * (0.03 + 0.13 * Math.pow(1 - f, 1.25) * Math.min(1, f * 6.5));
      const across = (rand() * 1.1 - 0.35) * width;
      const ang = (b * TAU) / 3 + Math.PI / 2;
      const along = 0.08 * s + f * L;
      const x = hx + Math.cos(ang) * along - Math.sin(ang) * across;
      const y = hy + Math.sin(ang) * along + Math.cos(ang) * across;
      put(out, i, x, y, hz + 0.06 * s + gauss(rand) * 0.008, 2 + ti);
    }
  }
  return out;
}

/* 2 — Enerji nakil hattı: kafes direkler + sarkan iletkenler (shader'da üzerlerinden enerji akar) */
function powerLine(n, rand) {
  const out = new Float32Array(n * 4);
  const pylonX = [-3, -1, 1, 3];
  const H = 2.45;
  const lift = -1.2;
  const hw = (y) => (y <= 1.5 ? 0.34 + (0.085 - 0.34) * (y / 1.5) : 0.085);
  const segs = [];
  const seg = (a, b, w = 1, v = 1) => segs.push([a[0], a[1] + lift, a[2], b[0], b[1] + lift, b[2], w, v]);
  const corners = [
    [-1, -1],
    [1, -1],
    [1, 1],
    [-1, 1],
  ];
  const levels = [0, 0.5, 0.95, 1.35, 1.75, 2.1];
  const attach = [];
  for (const cx of pylonX) {
    const c = (sx, sz, y) => [cx + sx * hw(y), y, sz * hw(y)];
    // ana ayaklar
    for (const [sx, sz] of corners) {
      for (let j = 0; j < levels.length - 1; j++) seg(c(sx, sz, levels[j]), c(sx, sz, levels[j + 1]), 1.6, 0.95);
      seg(c(sx, sz, 2.1), [cx, H, 0], 1.6, 0.95);
    }
    // çapraz örgüler (her yüzde X)
    for (let f = 0; f < 4; f++) {
      const [ax, az] = corners[f];
      const [bx, bz] = corners[(f + 1) % 4];
      for (let j = 0; j < levels.length - 1; j++) {
        const y0 = levels[j];
        const y1 = levels[j + 1];
        seg(c(ax, az, y0), c(bx, bz, y1), 0.7, 0.6);
        seg(c(bx, bz, y0), c(ax, az, y1), 0.7, 0.6);
        seg(c(ax, az, y1), c(bx, bz, y1), 0.7, 0.6);
      }
    }
    // konsollar (hatta dik) + izolatörler
    for (const [y, L] of [
      [1.75, 0.8],
      [2.1, 0.6],
    ]) {
      for (const side of [-1, 1]) {
        const tip = [cx, y, side * L];
        seg([cx - 0.085, y, side * 0.085], tip, 1.2, 0.9);
        seg([cx + 0.085, y, side * 0.085], tip, 1.2, 0.9);
        seg([cx, y + 0.17, side * 0.085], tip, 1, 0.75);
        seg(tip, [cx, y - 0.17, side * L], 1.4, 1);
        attach.push({ x: cx, y: y - 0.17, z: side * L });
      }
    }
    attach.push({ x: cx, y: H, z: 0, earth: true });
  }
  const pylonSample = segmentSampler(segs);

  // iletkenler: aynı hizadaki bağlantı noktalarını birleştir
  const keyOf = (a) => `${a.y.toFixed(2)}|${a.z.toFixed(2)}`;
  const lines = new Map();
  for (const a of attach) {
    if (!lines.has(keyOf(a))) lines.set(keyOf(a), []);
    lines.get(keyOf(a)).push(a);
  }
  const spans = [];
  const X0 = -4.6;
  const X1 = 4.6;
  for (const pts of lines.values()) {
    pts.sort((p, q) => p.x - q.x);
    const sag = pts[0].earth ? 0.16 : 0.24;
    const first = pts[0];
    const last = pts[pts.length - 1];
    spans.push({ a: { x: X0, y: first.y + 0.05, z: first.z }, b: first, sag, fadeA: true });
    for (let j = 0; j < pts.length - 1; j++) spans.push({ a: pts[j], b: pts[j + 1], sag });
    spans.push({ a: last, b: { x: X1, y: last.y + 0.05, z: last.z }, sag, fadeB: true });
  }

  for (let i = 0; i < n; i++) {
    if (rand() < 0.5) {
      const [x, y, z, v] = pylonSample(rand);
      put(out, i, x + gauss(rand) * 0.006, y + gauss(rand) * 0.006, z + gauss(rand) * 0.006, v);
    } else {
      const s = spans[Math.floor(rand() * spans.length)];
      const t = rand();
      const x = s.a.x + (s.b.x - s.a.x) * t;
      const y = s.a.y + (s.b.y - s.a.y) * t - s.sag * 4 * t * (1 - t) + lift;
      const tg = (x - X0) / (X1 - X0);
      // uçlarda solan iletkenler
      const fade = s.fadeA ? Math.min(1, t * 1.6) : s.fadeB ? Math.min(1, (1 - t) * 1.6) : 1;
      if (fade < rand()) {
        put(out, i, x, y, s.a.z, 0);
      } else {
        put(out, i, x, y + gauss(rand) * 0.004, s.a.z + gauss(rand) * 0.004, 2 + Math.min(0.999, Math.max(0, tg)));
      }
    }
  }
  return out;
}

/* 3 — Atom: çekirdek + üç yörünge (⚛) + yörüngede dönen elektronlar */
function atom(n, rand) {
  const out = new Float32Array(n * 4);
  const R = 1.78;
  const nucleons = [];
  while (nucleons.length < 18) {
    const [x, y, z] = randomDir(rand);
    const r = Math.cbrt(rand()) * 0.34;
    const p = [x * r, y * r, z * r];
    if (nucleons.every((q) => Math.hypot(p[0] - q[0], p[1] - q[1], p[2] - q[2]) > 0.16)) nucleons.push(p);
  }
  for (let i = 0; i < n; i++) {
    const k = rand();
    if (k < 0.28) {
      const c = nucleons[Math.floor(rand() * nucleons.length)];
      const [x, y, z] = randomDir(rand);
      const r = 0.14 * (0.8 + 0.2 * rand());
      put(out, i, c[0] + x * r, c[1] + y * r, c[2] + z * r, 1);
    } else if (k < 0.8) {
      const o = Math.floor(rand() * 3);
      const a = rand() * TAU;
      const r = R + gauss(rand) * 0.013;
      put(out, i, Math.cos(a) * r, gauss(rand) * 0.013, Math.sin(a) * r, 2 + o);
    } else if (k < 0.94) {
      const o = Math.floor(rand() * 3);
      const e = Math.floor(rand() * 2);
      const a = o * 1.9 + e * Math.PI;
      put(
        out,
        i,
        Math.cos(a) * R + gauss(rand) * 0.05,
        gauss(rand) * 0.05,
        Math.sin(a) * R + gauss(rand) * 0.05,
        5 + o,
      );
    } else {
      const [x, y, z] = randomDir(rand);
      const r = 0.5 + rand() * 1.9;
      put(out, i, x * r, y * r, z * r, 0.2);
    }
  }
  return out;
}

/* 4 — Güneş paneli tarlası: hücre çizgili, eğimli panel sıraları + ayaklar */
function solarFarm(n, rand) {
  const out = new Float32Array(n * 4);
  const rows = 4;
  const cols = 4;
  const PW = 1.32;
  const PH = 0.8;
  const tilt = 0.5;
  const gap = 0.16;
  const rowGap = 1.08;
  const cellsX = 6;
  const cellsY = 3;
  const V = [0, Math.sin(tilt), -Math.cos(tilt)];
  const panels = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const cx = (c - (cols - 1) / 2) * (PW + gap);
      const cz = 1.55 - r * rowGap;
      const cy = -0.55 + 0.32 + (PH / 2) * Math.sin(tilt);
      panels.push([cx, cy, cz]);
    }
  }
  const at = (p, u, v) => [p[0] + u, p[1] + V[1] * v, p[2] + V[2] * v];
  for (let i = 0; i < n; i++) {
    const p = panels[Math.floor(rand() * panels.length)];
    const k = rand();
    let u;
    let v;
    let w;
    if (k < 0.17) {
      const e = rand();
      const s = rand() - 0.5;
      if (e < 0.5) [u, v] = [s * PW, (e < 0.25 ? -0.5 : 0.5) * PH];
      else [u, v] = [(e < 0.75 ? -0.5 : 0.5) * PW, s * PH];
      w = 1;
    } else if (k < 0.55) {
      if (rand() < 0.62) {
        u = (-0.5 + Math.ceil(rand() * (cellsX - 1)) / cellsX) * PW;
        v = (rand() - 0.5) * PH;
      } else {
        u = (rand() - 0.5) * PW;
        v = (-0.5 + Math.ceil(rand() * (cellsY - 1)) / cellsY) * PH;
      }
      w = 0.62;
    } else if (k < 0.9) {
      u = (rand() - 0.5) * PW;
      v = (rand() - 0.5) * PH;
      w = 0.26;
    } else {
      // ayaklar: zeminden panelin altına
      const side = rand() < 0.5 ? -1 : 1;
      const top = at(p, side * PW * 0.32, -PH * 0.15);
      const t = rand();
      put(out, i, top[0], -0.55 + (top[1] + 0.55) * t, top[2], 0.45);
      continue;
    }
    const q = at(p, u, v);
    put(out, i, q[0], q[1], q[2], w);
  }
  return out;
}

export function buildShapes(n, rand) {
  return [sun(n, rand), windFarm(n, rand), powerLine(n, rand), atom(n, rand), solarFarm(n, rand)];
}

/** Açılış animasyonu için: parçacıklar etrafa saçılmış hâlde başlar */
export function scatter(n, rand) {
  const out = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const [x, y, z] = randomDir(rand);
    const r = 5 + rand() * 7;
    out[i * 3] = x * r;
    out[i * 3 + 1] = y * r * 0.7;
    out[i * 3 + 2] = Math.min(z * r, 5.5 - rand() * 2);
  }
  return out;
}

/** Parçacık başına rastgele değerler: gecikme, boyut, renk, faz */
export function randoms(n, rand) {
  const out = new Float32Array(n * 4);
  for (let i = 0; i < n * 4; i++) out[i] = rand();
  return out;
}

/**
 * Bir kelimeyi tuvale yazıp piksellerinden parçacık noktaları örnekler.
 * Dönüş: { positions: Float32Array(n*4), bounds: [genişlik, yükseklik] }
 */
export function sampleWord(text, n, rand, fontFamily = '"Space Grotesk Variable", "Space Grotesk", system-ui, sans-serif') {
  const fontSize = 200;
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const font = `700 ${fontSize}px ${fontFamily}`;
  ctx.font = font;
  const chars = [...text];
  const spacing = fontSize * 0.07;
  const widths = chars.map((ch) => ctx.measureText(ch).width);
  const total = widths.reduce((a, b) => a + b, 0) + spacing * Math.max(0, chars.length - 1);
  const pad = 24;
  canvas.width = Math.ceil(total + pad * 2);
  canvas.height = Math.ceil(fontSize * 1.3 + pad * 2);
  ctx.font = font;
  ctx.fillStyle = '#fff';
  ctx.textBaseline = 'middle';
  let cursor = pad;
  chars.forEach((ch, i) => {
    ctx.fillText(ch, cursor, canvas.height / 2);
    cursor += widths[i] + spacing;
  });

  const { data, width, height } = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const pts = [];
  let minX = Infinity;
  let maxX = -Infinity;
  let minY = Infinity;
  let maxY = -Infinity;
  for (let y = 0; y < height; y += 2) {
    for (let x = 0; x < width; x += 2) {
      if (data[(y * width + x) * 4 + 3] > 140) {
        pts.push(x, y);
        if (x < minX) minX = x;
        if (x > maxX) maxX = x;
        if (y < minY) minY = y;
        if (y > maxY) maxY = y;
      }
    }
  }

  const out = new Float32Array(n * 4);
  if (!pts.length) return { positions: out, bounds: [1, 1] };
  const targetW = 7.2;
  const k = targetW / Math.max(1, maxX - minX);
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;
  const count = pts.length / 2;
  for (let i = 0; i < n; i++) {
    const j = Math.floor(rand() * count) * 2;
    const px = pts[j] + rand() * 2;
    const py = pts[j + 1] + rand() * 2;
    put(out, i, (px - cx) * k, -(py - cy) * k, gauss(rand) * 0.09, 1);
  }
  return { positions: out, bounds: [targetW * 1.06, (maxY - minY) * k * 1.25] };
}
