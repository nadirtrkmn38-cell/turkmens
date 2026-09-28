# Görselleri "temiz arka plan" + "yazı katmanı" olarak ikiye ayırır.
#
#   orijinal = clean + D
#
# clean : yazıların silinip arka planın tamamlandığı görsel
# D     : sadece yazıların farkı (koyu çizgiler); blok blok ayrılmış halde
# Yazılar koyu, arka plan açık olduğu için morfolojik kapama (closing) ile
# arka plan tahmin edilir ve yazı pikselleri bu tahminle doldurulur.
import os
import cv2
import numpy as np

from blocks import BLOCKS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, 'kaynak')
GROW = 3   # yazı maskesinin kenar yumuşatma/JPEG hâlesi için genişletme (px)


def load_rgb(n):
    im = cv2.imread(os.path.join(SRC_DIR, f'{n}.jpg'), cv2.IMREAD_COLOR)
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32)


def luma(img):
    return img[..., 0] * 0.299 + img[..., 1] * 0.587 + img[..., 2] * 0.114


def ellipse(d):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d))


class Block:
    """Tek bir yazı bloğunun katmanı (kaynak görsel koordinatlarında)."""

    def __init__(self, bid, x0, y0, d, core, glyph_boxes):
        self.id = bid
        self.x0, self.y0 = x0, y0          # kırpmanın sol üst köşesi
        self.d = d                         # h x w x 3 fark katmanı
        self.core = core                   # h x w yazı çekirdeği maskesi
        self.h, self.w = d.shape[:2]
        self.cx = x0 + self.w / 2.0
        self.cy = y0 + self.h / 2.0
        self.strips = self._strips(glyph_boxes)
        self.bands = self._bands()

    def _strips(self, boxes):
        # Harfleri x ekseninde birleştirip dikey şeritlere böl (harf aralığı animasyonu için)
        iv = sorted((int(bx0) - self.x0, int(bx1) - self.x0) for bx0, bx1 in boxes)
        merged = []
        for a, b in iv:
            if merged and a <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        cuts = [0] + [(merged[i][1] + merged[i + 1][0]) // 2 for i in range(len(merged) - 1)] + [self.w]
        return [(cuts[i], cuts[i + 1], (merged[i][0] + merged[i][1]) / 2.0) for i in range(len(merged))]

    def _bands(self):
        # Satırları y eksenindeki boşluklardan ayır (satır satır animasyon için)
        rows = np.nonzero(self.core.any(axis=1))[0]
        if len(rows) == 0:
            return [(0, self.h)]
        runs = []
        start = prev = rows[0]
        for r in rows[1:]:
            if r > prev + 2:
                runs.append((start, prev + 1))
                start = r
            prev = r
        runs.append((start, prev + 1))
        # Nokta/çengel gibi küçük parçaları (ö, ü, ş) en yakın satıra kat
        while len(runs) > 1:
            hs = [b - a for a, b in runs]
            small = [i for i, v in enumerate(hs) if v < 0.5 * max(hs)]
            if not small:
                break
            i = small[0]
            gap_up = runs[i][0] - runs[i - 1][1] if i > 0 else 1 << 30
            gap_dn = runs[i + 1][0] - runs[i][1] if i + 1 < len(runs) else 1 << 30
            j = i - 1 if gap_up <= gap_dn else i + 1
            a, b = min(i, j), max(i, j)
            runs[a:b + 1] = [(runs[a][0], runs[b][1])]
        cuts = [0] + [(runs[i][1] + runs[i + 1][0]) // 2 for i in range(len(runs) - 1)] + [self.h]
        return [(cuts[i], cuts[i + 1]) for i in range(len(runs))]


class Plate:
    def __init__(self, n, orig, clean, blocks):
        self.n = n
        self.orig = orig
        self.clean = clean
        self.blocks = blocks
        self.h, self.w = orig.shape[:2]


def normalized_fill(img, valid):
    """Sadece geçerli (yazı olmayan) pikselleri kullanarak yerel ortalama arka plan."""
    out = None
    acc_w = None
    for sigma, need in ((4.0, 0.35), (10.0, 0.2), (28.0, 0.0)):
        num = cv2.GaussianBlur(img * valid[..., None], (0, 0), sigma)
        den = cv2.GaussianBlur(valid, (0, 0), sigma)
        est = num / np.maximum(den, 1e-6)[..., None]
        w = np.clip(den / need, 0.0, 1.0) if need > 0 else np.ones_like(den)
        if out is None:
            out, acc_w = est * w[..., None], w
        else:
            rest = (1.0 - acc_w)
            out = out + est * (rest * w)[..., None]
            acc_w = acc_w + rest * w
    return out


def prep(n):
    orig = load_rgb(n)
    H, W = orig.shape[:2]
    L = luma(orig)
    specs = BLOCKS[n]

    # Yazı çekirdeği: yerel arka plandan belirgin koyu VE mutlak olarak yeterince koyu
    stroke = np.zeros((H, W), np.uint8)
    for b in specs:
        x0, y0, x1, y1 = b['box']
        k = b.get('k', 25)
        thr = b.get('thr', 28)
        lmax = b.get('lmax', 235)
        X0, Y0, X1, Y1 = max(0, x0 - k), max(0, y0 - k), min(W, x1 + k), min(H, y1 + k)
        Lc = L[Y0:Y1, X0:X1]
        ref = cv2.GaussianBlur(cv2.morphologyEx(Lc, cv2.MORPH_CLOSE, ellipse(k)), (0, 0), 2.0)
        s = (((ref - Lc) > thr) & (Lc < lmax)).astype(np.uint8)
        stroke[y0:y1, x0:x1] |= s[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]

    # Bağlı bileşenleri (harfleri) ağırlık merkezine göre bloklara dağıt
    num, lab, stats, cents = cv2.connectedComponentsWithStats(stroke, connectivity=8)
    owner = np.full(num, -1, np.int32)
    for i in range(1, num):
        cx, cy = cents[i]
        for bi, b in enumerate(specs):
            x0, y0, x1, y1 = b['box']
            if x0 <= cx < x1 and y0 <= cy < y1:
                owner[i] = bi
                break
        else:
            sx, sy, sw, sh = stats[i][:4]
            ys, xs = np.nonzero(lab[sy:sy + sh, sx:sx + sw] == i)
            ys, xs = ys + sy, xs + sx
            best, bi_best = 0, -1
            for bi, b in enumerate(specs):
                x0, y0, x1, y1 = b['box']
                c = int(((xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1)).sum())
                if c > best:
                    best, bi_best = c, bi
            owner[i] = bi_best
    bmap = np.where(lab > 0, owner[lab], -1)

    grow = 2 * GROW + 1
    masks = []
    for bi in range(len(specs)):
        m = cv2.dilate((bmap == bi).astype(np.uint8), ellipse(grow))
        masks.append(np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.0) * 1.25, 0.0, 1.0))
    total = np.sum(masks, axis=0)
    fill = np.clip(total, 0.0, 1.0)

    # Arka planı yazı olmayan komşu piksellerden tamamla
    valid = (cv2.dilate((bmap >= 0).astype(np.uint8), ellipse(grow + 2)) == 0).astype(np.float32)
    bg = normalized_fill(orig, valid)
    # Dokulu yüzeydeki (cilt) ince çizgiler: dokuyu birkaç satır yukarıdan taşı
    for bi, b in enumerate(specs):
        if 'shift' in b:
            sh = np.roll(orig, b['shift'], axis=0)
            m = masks[bi] > 0
            bg[m] = sh[m]
    diff = orig - bg
    clean = orig - diff * fill[..., None]

    blocks = {}
    norm = fill / np.maximum(total, 1e-6)
    for bi, b in enumerate(specs):
        w = masks[bi] * norm
        ys, xs = np.nonzero(w > 1e-3)
        if len(ys) == 0:
            continue
        x0, y0 = max(0, int(xs.min()) - 2), max(0, int(ys.min()) - 2)
        x1, y1 = min(W, int(xs.max()) + 3), min(H, int(ys.max()) + 3)
        d = (diff[y0:y1, x0:x1] * w[y0:y1, x0:x1, None]).astype(np.float32)
        core = bmap[y0:y1, x0:x1] == bi
        glyphs = []
        for i in np.nonzero(owner == bi)[0]:
            sx, sy, sw, sh, area = stats[i]
            if area >= 3:
                glyphs.append((sx, sx + sw))
        blocks[b['id']] = Block(b['id'], x0, y0, d, core, glyphs)
    return Plate(n, orig, clean.astype(np.float32), blocks)


def debug(n, out_dir):
    p = prep(n)
    os.makedirs(out_dir, exist_ok=True)
    save = lambda name, img: cv2.imwrite(os.path.join(out_dir, name),
                                         cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_RGB2BGR))
    save(f'{n}_clean.png', p.clean)
    txt = np.full_like(p.orig, 255.0)
    rng = np.random.default_rng(n)
    col = np.zeros_like(p.orig)
    for b in p.blocks.values():
        txt[b.y0:b.y0 + b.h, b.x0:b.x0 + b.w] += b.d
        c = rng.uniform(40, 220, 3)
        a = np.clip(-b.d.mean(axis=2, keepdims=True) / 120.0, 0, 1)
        col[b.y0:b.y0 + b.h, b.x0:b.x0 + b.w] = col[b.y0:b.y0 + b.h, b.x0:b.x0 + b.w] * (1 - a) + c * a
        for (a0, a1) in b.bands:
            cv2.rectangle(col, (b.x0, b.y0 + a0), (b.x0 + b.w - 1, b.y0 + a1 - 1), (255, 0, 0), 1)
    save(f'{n}_text.png', txt)
    save(f'{n}_blocks.png', col + (255 - col.max(axis=2, keepdims=True)) * 0)
    recon = p.clean.copy()
    for b in p.blocks.values():
        recon[b.y0:b.y0 + b.h, b.x0:b.x0 + b.w] += b.d
    err = np.abs(recon - p.orig).max()
    print(n, 'blocks:', {k: (len(v.bands), len(v.strips)) for k, v in p.blocks.items()}, 'recon err', round(float(err), 3))


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'debug'
    for n in (3, 7, 1, 2, 6, 5, 4):
        debug(n, out)
