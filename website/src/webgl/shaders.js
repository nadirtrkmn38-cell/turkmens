/* GLSL shader'ları — parçacıklar ve arka plan yıldızları */
import { TURBINES } from './shapes.js';

// Simplex 3D gürültü — Ian McEwan, Stefan Gustavson (github.com/stegu/webgl-noise) · MIT Lisansı
const noise = /* glsl */ `
vec4 permute(vec4 x) { return mod(((x * 34.0) + 1.0) * x, 289.0); }
vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }
float snoise(vec3 v) {
  const vec2 C = vec2(1.0 / 6.0, 1.0 / 3.0);
  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
  vec3 i = floor(v + dot(v, C.yyy));
  vec3 x0 = v - i + dot(i, C.xxx);
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min(g.xyz, l.zxy);
  vec3 i2 = max(g.xyz, l.zxy);
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + 2.0 * C.xxx;
  vec3 x3 = x0 - 1.0 + 3.0 * C.xxx;
  i = mod(i, 289.0);
  vec4 p = permute(permute(permute(
            i.z + vec4(0.0, i1.z, i2.z, 1.0))
          + i.y + vec4(0.0, i1.y, i2.y, 1.0))
          + i.x + vec4(0.0, i1.x, i2.x, 1.0));
  float n_ = 1.0 / 7.0;
  vec3 ns = n_ * D.wyz - D.xzx;
  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_);
  vec4 x = x_ * ns.x + ns.yyyy;
  vec4 y = y_ * ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);
  vec4 b0 = vec4(x.xy, y.xy);
  vec4 b1 = vec4(x.zw, y.zw);
  vec4 s0 = floor(b0) * 2.0 + 1.0;
  vec4 s1 = floor(b1) * 2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));
  vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
  vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
  vec3 p0 = vec3(a0.xy, h.x);
  vec3 p1 = vec3(a0.zw, h.y);
  vec3 p2 = vec3(a1.xy, h.z);
  vec3 p3 = vec3(a1.zw, h.w);
  vec4 norm = taylorInvSqrt(vec4(dot(p0, p0), dot(p1, p1), dot(p2, p2), dot(p3, p3)));
  p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
  vec4 m = max(0.6 - vec4(dot(x0, x0), dot(x1, x1), dot(x2, x2), dot(x3, x3)), 0.0);
  m = m * m;
  return 42.0 * dot(m * m, vec4(dot(p0, x0), dot(p1, x1), dot(p2, x2), dot(p3, x3)));
}
`;

const f = (x) => (Number.isInteger(x) ? x.toFixed(1) : String(x));
const turbineConsts = TURBINES.map(
  (t, i) => `const vec3 HUB${i} = vec3(${t.hub.map(f).join(', ')});\nconst float SPIN${i} = ${f(t.speed)};`,
).join('\n');

export const particleVertex = /* glsl */ `
#define PI 3.141592653589793
#define TAU 6.283185307179586

uniform float uTime;
uniform float uFrom;
uniform float uTo;
uniform float uT;
uniform float uStagger;
uniform float uIntro;
uniform float uSize;
uniform float uSizeScale;
uniform float uPixelRatio;
uniform float uOpacity;
uniform float uAspect;
uniform float uTanHalfFov;
uniform vec2 uMouse;
uniform float uMouseForce;
uniform float uHold;
uniform vec4 uShock;
uniform float uTurbulence;
uniform float uWordBlend;
uniform vec3 uColorA;
uniform vec3 uColorB;
uniform vec3 uColorC;

attribute vec4 aShape0;
attribute vec4 aShape1;
attribute vec4 aShape2;
attribute vec4 aShape3;
attribute vec4 aShape4;
attribute vec4 aWord;
attribute vec4 aWordPrev;
attribute vec3 aScatter;
attribute vec4 aRandom;

varying vec3 vColor;
varying float vAlpha;

${turbineConsts}

${noise}

vec2 rot2(vec2 v, float a) {
  float c = cos(a);
  float s = sin(a);
  return vec2(c * v.x - s * v.y, s * v.x + c * v.y);
}

// Bölüm indeksine göre şeklin canlandırılmış hâli.
// Dönüş: xyz konum, w görünürlük (1'in üzeri = ekstra parlama)
vec4 shapeAt(float idx) {
  vec4 s;
  vec3 p;
  if (idx < 0.5) {
    // ── güneş: kaynayan yüzey, titreşen korona
    s = aShape0;
    p = s.xyz;
    p.xz = rot2(p.xz, uTime * 0.05);
    float r0 = length(p);
    vec3 nrm = p / max(r0, 0.0001);
    if (s.w > 1.5) {
      float fl = snoise(nrm * 2.3 + vec3(0.0, uTime * 0.32, fract(s.w) * 4.0));
      p = nrm * (r0 + (r0 - 1.5) * 0.45 * fl);
      s.w = 0.5 * (1.0 - smoothstep(1.7, 2.75, r0));
    } else {
      float n1 = snoise(p * 1.35 + vec3(0.0, uTime * 0.28, 0.0));
      float n2 = snoise(p * 3.2 - vec3(uTime * 0.22));
      p *= 1.0 + 0.065 * n1 + 0.028 * n2;
    }
  } else if (idx < 1.5) {
    // ── rüzgar türbinleri: kanatlar göbek etrafında döner, rüzgar çizgileri akar
    s = aShape1;
    p = s.xyz;
    if (s.w > 4.5) {
      float sp = 0.45 + fract(s.w) * 0.7;
      p.x = mod(p.x + uTime * sp + 3.3, 6.6) - 3.3;
      s.w = (1.0 - smoothstep(2.0, 3.2, abs(p.x))) * 0.6;
    } else if (s.w > 1.5) {
      float ti = floor(s.w - 1.5);
      vec3 hub = ti < 0.5 ? HUB0 : (ti < 1.5 ? HUB1 : HUB2);
      float spin = ti < 0.5 ? SPIN0 : (ti < 1.5 ? SPIN1 : SPIN2);
      p.xy = hub.xy + rot2(p.xy - hub.xy, -uTime * spin - ti * 1.3);
      s.w = 1.0;
    }
    p.xz = rot2(p.xz, 0.32);
    p.yz = rot2(p.yz, 0.06);
  } else if (idx < 2.5) {
    // ── enerji nakil hattı: iletkenlerde ilerleyen enerji darbeleri
    s = aShape2;
    p = s.xyz;
    if (s.w > 1.5) {
      float tg = s.w - 2.0;
      float pulse = pow(fract(tg * 2.6 - uTime * 0.2), 16.0);
      p.y += sin(tg * 30.0 + uTime * 1.1) * 0.01;
      s.w = 0.42 + pulse * 2.4;
    }
    p.xz = rot2(p.xz, -0.5);
    p.yz = rot2(p.yz, 0.1);
  } else if (idx < 3.5) {
    // ── atom: yörüngeler ⚛ biçiminde, elektronlar üzerinde döner
    s = aShape3;
    p = s.xyz;
    if (s.w > 1.5) {
      float isE = step(4.5, s.w);
      float o = floor(s.w - 2.0 - 3.0 * isE + 0.5);
      p.xz = rot2(p.xz, uTime * (0.75 + o * 0.24));
      p.yz = rot2(p.yz, 0.3);
      p.xy = rot2(p.xy, o * 1.0472 + 0.35);
      s.w = isE > 0.5 ? 1.8 : 0.5;
    }
    p.xz = rot2(p.xz, sin(uTime * 0.23) * 0.42);
    p.yz = rot2(p.yz, cos(uTime * 0.19) * 0.14);
  } else if (idx < 4.5) {
    // ── güneş paneli tarlası: paneller üzerinde gezinen ışık yansıması
    s = aShape4;
    p = s.xyz;
    float glint = pow(max(0.0, sin(p.x * 0.8 - p.z * 0.95 - uTime * 0.85)), 24.0);
    s.w += glint * 1.5 * step(0.2, s.w);
    p.yz = rot2(p.yz, 0.36);
    p.xz = rot2(p.xz, -0.16);
  } else {
    // ── kelime: dil değişince bir kelimeden diğerine akar
    s = mix(aWordPrev, aWord, uWordBlend);
    p = s.xyz;
    float wm = sin(uWordBlend * PI);
    if (wm > 0.001) {
      vec3 q = p * 0.8 + aRandom.w * 3.0;
      p += vec3(snoise(q), snoise(q + 7.1), snoise(q + 13.7)) * wm * 0.8;
    }
    p.z += sin(p.x * 0.8 + uTime * 1.3) * 0.08;
    p.y += sin(p.x * 0.55 + uTime * 0.9) * 0.035;
  }
  return vec4(p, s.w);
}

void main() {
  // geçiş: her parçacık biraz farklı zamanda yola çıkar
  float tp = clamp((uT - aRandom.x * uStagger) / (1.0 - uStagger), 0.0, 1.0);
  float e = tp * tp * (3.0 - 2.0 * tp);
  vec4 S = shapeAt(uFrom);
  if (uT > 0.0001) {
    S = mix(S, shapeAt(uTo), e);
  }
  vec3 pos = S.xyz;
  float glow = max(S.w - 1.0, 0.0);
  float vis = min(S.w, 1.0);

  // geçişin ortasında girdap gibi türbülans
  float mid = sin(e * PI);
  if (mid > 0.001) {
    vec3 q = pos * 0.55 + aRandom.w * 4.0 + uTime * 0.2;
    vec3 turb = vec3(snoise(q), snoise(q + vec3(9.2, 0.0, 0.0)), snoise(q + vec3(0.0, 17.7, 0.0)));
    pos += turb * mid * uTurbulence;
    vis = max(vis, mid * 0.35);
  }

  // dinlenirken hafif salınım
  pos += vec3(
    sin(uTime * 0.9 + aRandom.w * 40.0),
    cos(uTime * 0.7 + aRandom.y * 40.0),
    sin(uTime * 0.8 + aRandom.z * 40.0)) * 0.012;

  // açılış: dağınık hâlden şekle toplanma
  float it = clamp((uIntro - aRandom.x * 0.4) / 0.6, 0.0, 1.0);
  it = 1.0 - pow(1.0 - it, 3.0);
  pos = mix(aScatter, pos, it);

  vec4 mv = modelViewMatrix * vec4(pos, 1.0);
  float depth = max(-mv.z, 0.2);
  vec4 clip = projectionMatrix * mv;
  vec2 ndc = clip.xy / clip.w;
  float unit = depth * uTanHalfFov; // ekran birimini sahne birimine çevirir

  // imleç: parçacıkları nazikçe iter
  vec2 diff = (ndc - uMouse) * vec2(uAspect, 1.0);
  float d = length(diff);
  float push = 1.0 - smoothstep(0.0, 0.3, d);
  push = push * push * uMouseForce;
  mv.xy += (diff / max(d, 0.0001)) * push * 0.12 * unit;

  // tıklama: şok dalgası
  vec2 sd2 = (ndc - uShock.xy) * vec2(uAspect, 1.0);
  float sd = length(sd2);
  float ring = exp(-pow((sd - uShock.z * 1.3) * 6.0, 2.0)) * exp(-uShock.z * 1.7) * uShock.w;
  mv.xy += (sd2 / max(sd, 0.0001)) * ring * 0.2 * unit;

  // basılı tutma: imlecin etrafında dönen bir girdap
  if (abs(uHold) > 0.001) {
    vec2 target = vec2(uMouse.x * uAspect, uMouse.y) * unit;
    float rn = 0.012 + pow(aRandom.y, 1.7) * 0.22;
    float ang = aRandom.w * TAU + uTime * (0.7 + 0.11 / (rn + 0.025));
    vec2 orbit = vec2(cos(ang), sin(ang) * 0.82) * rn * unit;
    mv.xy = mix(mv.xy, target + orbit, uHold * (0.78 + 0.22 * aRandom.z));
  }

  gl_Position = projectionMatrix * mv;

  float tw = 0.72 + 0.28 * sin(uTime * (1.1 + aRandom.z * 2.4) + aRandom.w * 50.0);
  float size = uSize * (0.42 + pow(aRandom.y, 2.0) * 1.4) * (1.0 + mid * 0.45 + glow * 0.35);
  gl_PointSize = clamp(size * uSizeScale * uPixelRatio * (10.0 / depth), 0.0, 36.0 * uPixelRatio);

  // renk: merkezden dışa doğru iki renk arası geçiş + nadir beyaz pırıltılar
  float g = clamp(length(pos) / 3.2, 0.0, 1.0);
  float m = clamp(g * 0.9 + (aRandom.z - 0.5) * 0.55, 0.0, 1.0);
  vec3 col = mix(uColorA, uColorB, m);
  col = mix(col, uColorC, clamp(step(0.968, aRandom.z) * 0.85 + glow * 0.45, 0.0, 1.0));
  col *= 1.0 + mid * 0.55 + push * 0.9 + ring * 1.6 + abs(uHold) * 0.35 + glow * 0.9;
  vColor = col;

  float fade = smoothstep(32.0, 7.0, depth);
  vAlpha = vis * fade * uOpacity * tw * (0.2 + 0.8 * it);
}
`;

export const particleFragment = /* glsl */ `
varying vec3 vColor;
varying float vAlpha;

void main() {
  float d = length(gl_PointCoord - 0.5);
  float a = smoothstep(0.5, 0.04, d);
  a *= a;
  if (a * vAlpha < 0.002) discard;
  gl_FragColor = vec4(vColor, a * vAlpha);
  #include <colorspace_fragment>
}
`;

export const starVertex = /* glsl */ `
uniform float uTime;
uniform float uPixelRatio;
uniform float uOpacity;
attribute vec4 aRandom;
varying float vAlpha;

void main() {
  vec4 mv = modelViewMatrix * vec4(position, 1.0);
  gl_Position = projectionMatrix * mv;
  float tw = 0.5 + 0.5 * sin(uTime * (0.4 + aRandom.x * 1.8) + aRandom.y * 40.0);
  gl_PointSize = (0.8 + aRandom.z * 1.8) * uPixelRatio;
  vAlpha = (0.12 + 0.5 * tw) * (0.35 + aRandom.w * 0.65) * uOpacity;
}
`;

export const starFragment = /* glsl */ `
varying float vAlpha;

void main() {
  float d = length(gl_PointCoord - 0.5);
  float a = smoothstep(0.5, 0.0, d);
  gl_FragColor = vec4(vec3(0.82, 0.86, 1.0), a * vAlpha);
  #include <colorspace_fragment>
}
`;
