import {
  AdditiveBlending,
  BufferAttribute,
  BufferGeometry,
  Color,
  MathUtils,
  PerspectiveCamera,
  Points,
  Scene,
  ShaderMaterial,
  Vector2,
  Vector4,
  WebGLRenderer,
} from 'three';
import { buildShapes, mulberry32, randoms, sampleWord, scatter, SHAPE_BOUNDS } from './shapes.js';
import { particleFragment, particleVertex, starFragment, starVertex } from './shaders.js';

const FOV = 35;
const CAM_Z = 10;
const TAN = Math.tan(MathUtils.degToRad(FOV / 2));
const WORD_INDEX = 5;

const damp = (a, b, lambda, dt) => MathUtils.lerp(a, b, 1 - Math.exp(-lambda * dt));
const smooth = (x) => x * x * (3 - 2 * x);
const clamp = MathUtils.clamp;

/**
 * Sitenin arkasındaki 3D sahne.
 * Her bölümün içinde görünmez bir "sahne kutusu" ([data-stage]) vardır;
 * parçacıklar o kutunun ekrandaki yerine ve boyutuna yerleşir.
 * Kutunun CSS değişkenleri (--c1, --c2, --stage-opacity) renk ve parlaklığı belirler.
 */
export class World {
  constructor(canvas, { count = 30000, reducedMotion = false, maxPixelRatio = 2 } = {}) {
    this.canvas = canvas;
    this.count = count;
    this.reduced = reducedMotion;

    this.renderer = new WebGLRenderer({
      canvas,
      antialias: false,
      alpha: false,
      depth: false,
      stencil: false,
      powerPreference: 'high-performance',
    });
    this.renderer.setClearColor('#07070a', 1);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, maxPixelRatio));

    this.scene = new Scene();
    this.camera = new PerspectiveCamera(FOV, 1, 0.1, 120);
    this.camera.position.set(0, 0, CAM_Z);

    this.time = 0;
    this.last = performance.now();
    this.running = false;
    this.sections = [];
    this.stages = [];
    this.styles = [];
    this.tops = [];
    this.wordBounds = [7.6, 2.0];
    this.wordBoundsPrev = [7.6, 2.0];
    this.frameTimes = [];
    this.adapted = false;

    this.state = {
      progress: 0,
      pointer: new Vector2(0, 0),
      pointerPrev: new Vector2(0, 0),
      pointerSmooth: new Vector2(0, 0),
      pointerActive: false,
      force: 0,
      hold: 0,
      holdVel: 0,
      holdTarget: 0,
      pressTime: 0,
      shock: new Vector2(0, 0),
      shockAge: 99,
      shockStrength: 0,
      intro: 0,
      introStarted: false,
      wordBlend: 1,
      parallax: new Vector2(0, 0),
    };

    this.buildParticles();
    this.buildStars();
    this.resize();

    this.loop = this.loop.bind(this);
    this.onResize = () => {
      clearTimeout(this.resizeTimer);
      this.resizeTimer = setTimeout(() => this.resize(), 80);
    };
    window.addEventListener('resize', this.onResize);
    if ('ResizeObserver' in window) {
      this.ro = new ResizeObserver(() => this.measure());
      this.ro.observe(document.body);
    }
  }

  /* ───────────── kurulum ───────────── */

  buildParticles() {
    const n = this.count;
    const rand = mulberry32(20261109);
    const shapes = buildShapes(n, rand);
    const geometry = new BufferGeometry();

    const position = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      position[i * 3] = shapes[0][i * 4];
      position[i * 3 + 1] = shapes[0][i * 4 + 1];
      position[i * 3 + 2] = shapes[0][i * 4 + 2];
    }
    geometry.setAttribute('position', new BufferAttribute(position, 3));
    shapes.forEach((arr, i) => geometry.setAttribute(`aShape${i}`, new BufferAttribute(arr, 4)));
    // kelime, yazı tipi yüklenene kadar kürenin kopyası olarak başlar
    geometry.setAttribute('aWord', new BufferAttribute(shapes[0].slice(), 4));
    geometry.setAttribute('aWordPrev', new BufferAttribute(shapes[0].slice(), 4));
    geometry.setAttribute('aScatter', new BufferAttribute(scatter(n, rand), 3));
    geometry.setAttribute('aRandom', new BufferAttribute(randoms(n, rand), 4));

    this.uniforms = {
      uTime: { value: 0 },
      uFrom: { value: 0 },
      uTo: { value: 0 },
      uT: { value: 0 },
      uStagger: { value: 0.32 },
      uIntro: { value: 0 },
      uSize: { value: 2.5 },
      uSizeScale: { value: 1 },
      uPixelRatio: { value: this.renderer.getPixelRatio() },
      uOpacity: { value: 0 },
      uAspect: { value: 1 },
      uTanHalfFov: { value: TAN },
      uMouse: { value: new Vector2(0, 0) },
      uMouseForce: { value: 0 },
      uHold: { value: 0 },
      uShock: { value: new Vector4(0, 0, 99, 0) },
      uTurbulence: { value: this.reduced ? 0 : 0.85 },
      uWordBlend: { value: 1 },
      uColorA: { value: new Color('#ff7a45') },
      uColorB: { value: new Color('#8f7bff') },
      uColorC: { value: new Color('#ffffff') },
    };
    this.material = new ShaderMaterial({
      vertexShader: particleVertex,
      fragmentShader: particleFragment,
      uniforms: this.uniforms,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      blending: AdditiveBlending,
    });

    this.geometry = geometry;
    this.points = new Points(geometry, this.material);
    this.points.frustumCulled = false;
    this.scene.add(this.points);
  }

  buildStars() {
    const n = 1400;
    const rand = mulberry32(38);
    const pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const u = rand() * 2 - 1;
      const th = rand() * Math.PI * 2;
      const s = Math.sqrt(1 - u * u);
      const r = 22 + rand() * 30;
      pos[i * 3] = s * Math.cos(th) * r;
      pos[i * 3 + 1] = u * r;
      pos[i * 3 + 2] = s * Math.sin(th) * r - 10;
    }
    const geometry = new BufferGeometry();
    geometry.setAttribute('position', new BufferAttribute(pos, 3));
    geometry.setAttribute('aRandom', new BufferAttribute(randoms(n, rand), 4));
    this.starUniforms = {
      uTime: { value: 0 },
      uPixelRatio: { value: this.renderer.getPixelRatio() },
      uOpacity: { value: 0 },
    };
    const material = new ShaderMaterial({
      vertexShader: starVertex,
      fragmentShader: starFragment,
      uniforms: this.starUniforms,
      transparent: true,
      depthWrite: false,
      depthTest: false,
      blending: AdditiveBlending,
    });
    this.stars = new Points(geometry, material);
    this.stars.frustumCulled = false;
    this.scene.add(this.stars);
  }

  /* ───────────── dış dünya ile bağlantı ───────────── */

  setSections(sectionEls) {
    this.sections = sectionEls;
    this.stages = sectionEls.map((s) => s.querySelector('[data-stage]') || s);
    this.readStyles();
    this.measure();
  }

  readStyles() {
    const fallback = this.styles[0];
    this.styles = this.stages.map((stage) => {
      const cs = getComputedStyle(stage);
      const read = (name, def) => (cs.getPropertyValue(name) || '').trim() || def;
      return {
        c1: new Color(read('--c1', '#ff7a45')),
        c2: new Color(read('--c2', '#8f7bff')),
        opacity: parseFloat(read('--stage-opacity', '1')),
        size: parseFloat(read('--stage-size', '1')),
      };
    });
    if (!this.styles.length && fallback) this.styles = [fallback];
  }

  measure() {
    const sy = window.scrollY;
    this.tops = this.sections.map((s) => s.getBoundingClientRect().top + sy);
  }

  /** Kaydırma konumundan "hangi şekil" ilerlemesini hesaplar (0 … bölüm sayısı-1) */
  progressFromScroll() {
    const vh = this.height;
    const c = window.scrollY + vh * 0.5;
    const w = vh * 0.36;
    const b = this.tops;
    for (let k = 1; k < b.length; k++) {
      if (c < b[k] - w) return k - 1;
      if (c <= b[k] + w) return k - 1 + (c - (b[k] - w)) / (2 * w);
    }
    return Math.max(0, b.length - 1);
  }

  layoutFor(k) {
    const stage = this.stages[k];
    const style = this.styles[k] || this.styles[0];
    if (!stage) return { x: 0, y: 0, s: 1, ...style };
    const r = stage.getBoundingClientRect();
    const halfH = TAN * CAM_Z;
    const halfW = halfH * this.aspect;
    const x = ((r.left + r.width / 2) / this.width) * 2 - 1;
    const y = -(((r.top + r.height / 2) / this.height) * 2 - 1);
    const wU = (r.width / this.width) * 2 * halfW;
    const hU = (r.height / this.height) * 2 * halfH;
    let b = SHAPE_BOUNDS[k] || SHAPE_BOUNDS[0];
    if (k === WORD_INDEX) {
      const wb = smooth(this.state.wordBlend);
      b = [
        MathUtils.lerp(this.wordBoundsPrev[0], this.wordBounds[0], wb),
        MathUtils.lerp(this.wordBoundsPrev[1], this.wordBounds[1], wb),
      ];
    }
    const s = Math.max(0.05, Math.min(wU / b[0], hU / b[1]) * (style.size || 1));
    return { x: x * halfW, y: y * halfH, s, c1: style.c1, c2: style.c2, opacity: style.opacity };
  }

  /** İletişim bölümündeki dev kelimeyi ayarlar (dil değişince akarak dönüşür) */
  setWord(text, animate = false) {
    const { positions, bounds } = sampleWord(text, this.count, mulberry32(7));
    const word = this.geometry.attributes.aWord;
    const prev = this.geometry.attributes.aWordPrev;
    if (animate && this.wordReady) {
      prev.array.set(word.array);
      this.wordBoundsPrev = this.wordBounds;
      this.state.wordBlend = 0;
    } else {
      prev.array.set(positions);
      this.wordBoundsPrev = bounds;
      this.state.wordBlend = 1;
    }
    word.array.set(positions);
    word.needsUpdate = true;
    prev.needsUpdate = true;
    this.wordBounds = bounds;
    this.wordReady = true;
  }

  pointerMove(clientX, clientY) {
    this.state.pointer.set((clientX / this.width) * 2 - 1, -(clientY / this.height) * 2 + 1);
    if (!this.state.pointerActive) this.state.pointerSmooth.copy(this.state.pointer);
    this.state.pointerActive = true;
  }

  pointerLeave() {
    this.state.pointerActive = false;
  }

  press() {
    if (this.reduced) return;
    this.state.holdTarget = 1;
    this.state.pressTime = this.time;
  }

  release() {
    const st = this.state;
    if (st.holdTarget === 0) return;
    st.holdTarget = 0;
    const held = this.time - st.pressTime;
    st.shock.copy(st.pointer);
    st.shockAge = 0;
    st.shockStrength = clamp(0.55 + held * 0.9, 0.55, 1.6);
  }

  startIntro() {
    this.state.introStarted = true;
    if (this.reduced) this.state.intro = 1;
  }

  start() {
    if (this.running) return;
    this.running = true;
    this.last = performance.now();
    this.raf = requestAnimationFrame(this.loop);
  }

  stop() {
    this.running = false;
    cancelAnimationFrame(this.raf);
  }

  /** Düşük performansta parçacık sayısını ve çözünürlüğü azaltır */
  degrade() {
    this.renderer.setPixelRatio(1);
    this.geometry.setDrawRange(0, Math.floor(this.count * 0.6));
    this.uniforms.uSize.value *= 1.12;
    this.resize();
  }

  resize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    this.width = w;
    this.height = h;
    this.aspect = w / h;
    this.renderer.setSize(w, h, false);
    this.camera.aspect = this.aspect;
    this.camera.updateProjectionMatrix();
    this.uniforms.uAspect.value = this.aspect;
    this.uniforms.uPixelRatio.value = this.renderer.getPixelRatio();
    this.starUniforms.uPixelRatio.value = this.renderer.getPixelRatio();
    // küçük ekranlarda parçacıklar biraz daha küçük
    this.uniforms.uSize.value = w < 700 ? 2.25 : 2.5;
    if (this.sections.length) {
      this.readStyles();
      this.measure();
    }
  }

  /* ───────────── döngü ───────────── */

  loop(now) {
    if (!this.running) return;
    const dt = Math.min((now - this.last) / 1000, 1 / 20);
    this.last = now;
    this.time += dt;
    this.update(dt);
    this.renderer.render(this.scene, this.camera);
    this.raf = requestAnimationFrame(this.loop);
  }

  update(dt) {
    const st = this.state;
    const u = this.uniforms;
    u.uTime.value = this.time;
    this.starUniforms.uTime.value = this.time;

    // açılış
    if (st.introStarted && st.intro < 1) st.intro = Math.min(1, st.intro + dt / 2.6);
    u.uIntro.value = st.intro;

    // kaydırma → şekil ilerlemesi
    const n = Math.max(1, this.sections.length);
    const target = this.sections.length ? this.progressFromScroll() : 0;
    st.progress = this.reduced ? target : damp(st.progress, target, 4.5, dt);
    if (Math.abs(st.progress - target) < 0.0004) st.progress = target;
    const from = Math.min(Math.floor(st.progress), n - 1);
    const to = Math.min(from + 1, n - 1);
    const t = from === to ? 0 : st.progress - from;
    u.uFrom.value = from;
    u.uTo.value = to;
    u.uT.value = t;

    // yerleşim: iki bölümün sahne kutusu arasında yumuşak geçiş
    const A = this.layoutFor(from);
    const B = t > 0 ? this.layoutFor(to) : A;
    const E = smooth(t);
    this.points.position.set(MathUtils.lerp(A.x, B.x, E), MathUtils.lerp(A.y, B.y, E), 0);
    const s = MathUtils.lerp(A.s, B.s, E);
    this.points.scale.setScalar(s);
    u.uSizeScale.value = clamp(Math.sqrt(s), 0.55, 1.15);
    u.uColorA.value.copy(A.c1).lerp(B.c1, E);
    u.uColorB.value.copy(A.c2).lerp(B.c2, E);

    // kelime dönüşümü
    if (st.wordBlend < 1) st.wordBlend = Math.min(1, st.wordBlend + dt / 1.5);
    u.uWordBlend.value = smooth(st.wordBlend);

    // imleç
    const speed = st.pointer.distanceTo(st.pointerPrev) / Math.max(dt, 1e-3);
    st.pointerPrev.copy(st.pointer);
    const targetForce = st.pointerActive && !this.reduced ? Math.min(0.32 + speed * 0.32, 1.35) : 0;
    st.force = damp(st.force, targetForce, targetForce > st.force ? 9 : 2.2, dt);
    st.pointerSmooth.x = damp(st.pointerSmooth.x, st.pointer.x, 14, dt);
    st.pointerSmooth.y = damp(st.pointerSmooth.y, st.pointer.y, 14, dt);
    u.uMouse.value.copy(st.pointerSmooth);
    u.uMouseForce.value = st.force;

    // basılı tutma (yay fiziği → bırakınca hafif patlama)
    const acc = (st.holdTarget - st.hold) * 42 - st.holdVel * 6.2;
    st.holdVel += acc * dt;
    st.hold += st.holdVel * dt;
    if (st.holdTarget === 0 && Math.abs(st.hold) < 0.0005 && Math.abs(st.holdVel) < 0.001) st.hold = 0;
    u.uHold.value = st.hold;

    // şok dalgası
    st.shockAge += dt;
    const sh = u.uShock.value;
    sh.x = st.shock.x;
    sh.y = st.shock.y;
    sh.z = st.shockAge;
    sh.w = st.shockStrength;

    // genel parlaklık
    const fadeIn = smooth(clamp(st.intro * 2.2, 0, 1));
    u.uOpacity.value = MathUtils.lerp(A.opacity, B.opacity, E) * fadeIn;
    this.starUniforms.uOpacity.value = fadeIn;

    // imlece göre hafif paralaks + şeklin eğilmesi
    if (!this.reduced) {
      st.parallax.x = damp(st.parallax.x, st.pointerSmooth.x, 2.2, dt);
      st.parallax.y = damp(st.parallax.y, st.pointerSmooth.y, 2.2, dt);
    }
    this.camera.position.x = st.parallax.x * 0.22;
    this.camera.position.y = st.parallax.y * 0.14;
    this.camera.lookAt(0, 0, 0);
    this.points.rotation.x = -st.parallax.y * 0.16;
    this.points.rotation.y = st.parallax.x * 0.22;
    this.stars.rotation.y = this.time * 0.006 + st.progress * 0.05;
    this.stars.rotation.x = st.progress * 0.06;

    // ilk saniyelerde performansı ölç, gerekirse kaliteyi düşür
    if (!this.adapted && st.intro >= 1) {
      this.frameTimes.push(dt);
      if (this.frameTimes.length >= 100) {
        const avg = this.frameTimes.reduce((a, b) => a + b, 0) / this.frameTimes.length;
        this.adapted = true;
        if (avg > 1 / 40 && !navigator.webdriver) this.degrade();
      }
    }
  }
}
