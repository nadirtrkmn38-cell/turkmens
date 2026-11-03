# -*- coding: utf-8 -*-
"""İME ön raporu üretici.

KOÜ Teknoloji Fakültesi İME şablonunu (tpl/) doldurur; içerik icerik.py'dedir.
Uygulanan kurallar (Yönerge m. 10, Rapor Yazım Kuralları 2.x):
  - kenar boşlukları sol/sağ 3,25 cm, üst 3 cm, alt 2,5 cm (kapaklar şablondaki gibi)
  - Times New Roman 12 pt, başlıklar 14/12 pt koyu, şekil-tablo açıklamaları 10 pt tek aralık
  - ana metin 1,15 satır aralığı; paragraflar ve alt başlıklar arasında 3 aralık (18 nk)
  - ilk sayfalarda başlık üstten 5 cm, başlıktan sonra 4,5 aralık (27 nk)
  - ön sayfalar i, ii… alt orta; metin 1, 2… üst sağ Arial Bold 12; bölüm ilk sayfalarında numara yok
  - her sayfanın altında sorumlu imza/kaşe alanı; bölüm ilk sayfasında işletme yöneticisi imza/kaşe
Çalıştırma: python3 build.py   (taşan "Yapılan İş" sayfaları otomatik olarak "(devam)" sayfasına bölünür)
"""
import copy, json, os, re, shutil, subprocess, sys
from datetime import datetime, timedelta
from xml.sax.saxutils import escape
from lxml import etree
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import icerik as C

TPL = os.path.join(HERE, 'tpl')   # şablonun açılmış ve run'ları birleştirilmiş hâli
FIG = os.path.join(HERE, 'fig')
OUT = os.path.join(HERE, 'out')
SOFFICE = '/root/.claude/skills/synced/6751a5cd-4f7f-407f-9ff4-5fd3a8be5315_e5b01c29-0de8-4179-8b57-4c2efe80941b/docx/scripts/office/soffice.py'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NSDECL = ('xmlns:w="%s" xmlns:r="%s" '
          'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
          'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
          'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"') % (W_NS, R_NS)
W = '{%s}' % W_NS
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'

MAR = (1701, 1843, 1417, 1843)          # üst, sağ, alt, sol (twip): 3 / 3,25 / 2,5 / 3,25 cm
TEXT_W = 11906 - 2 * 1843               # 8220 twip = 14,5 cm
FRAME_GRID = [3860, 2064, 2296]
WEEK_GRID = [1300, 1250, 1650, 1650, 870, 1500]
AC_H, AC_H_FIRST = 11650, 10900         # Açıklama satırının asgari yüksekliği (normal / bölüm ilk sayfası)
SP_PARA = 360                           # 3 aralık = 18 nk
SP_HEAD_AFTER = 540                     # 4,5 aralık = 27 nk

def frag(xml):
    return list(etree.fromstring('<w:body %s>%s</w:body>' % (NSDECL, xml)))

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
def rpr(sz=24, b=False):
    return '<w:rPr>%s%s<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (TNR, '<w:b/><w:bCs/>' if b else '', sz, sz)
def run(t, sz=24, b=False):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr(sz, b), escape(t))
def tab_run(sz=24, b=False):
    return '<w:r>%s<w:tab/></w:r>' % rpr(sz, b)
def para(runs, jc='both', before=0, after=SP_PARA, line=276, keep=False, ind='', pbb=False, sz=24,
         tabs='', outline=None):
    p = '<w:pPr>'
    if keep: p += '<w:keepNext/>'
    if pbb: p += '<w:pageBreakBefore/>'
    if tabs: p += '<w:tabs>%s</w:tabs>' % tabs
    p += '<w:spacing w:before="%d" w:after="%d" w:line="%d" w:lineRule="auto"/>' % (before, after, line)
    p += ind
    p += '<w:jc w:val="%s"/>' % jc
    if outline is not None: p += '<w:outlineLvl w:val="%d"/>' % outline
    p += rpr(sz) + '</w:pPr>'
    return '<w:p>%s%s</w:p>' % (p, runs)

def tiny(br=False, sect=''):
    r = '<w:r><w:rPr><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr><w:br w:type="page"/></w:r>' if br else ''
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:rPr><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr>%s</w:pPr>%s</w:p>') % (sect, r)

def sectpr(hdr=(), ftr=(), title_pg=False, fmt=None, start=None, mar=MAR):
    x = '<w:sectPr>'
    for t, rid in hdr: x += '<w:headerReference w:type="%s" r:id="%s"/>' % (t, rid)
    for t, rid in ftr: x += '<w:footerReference w:type="%s" r:id="%s"/>' % (t, rid)
    x += '<w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
    top, right, bottom, left = mar
    x += ('<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="737" w:footer="567" '
          'w:gutter="0"/>') % (top, right, bottom, left)
    if fmt or start is not None:
        x += '<w:pgNumType%s%s/>' % (' w:fmt="%s"' % fmt if fmt else '', ' w:start="%d"' % start if start is not None else '')
    x += '<w:cols w:space="708"/>' + ('<w:titlePg/>' if title_pg else '') + '<w:docGrid w:linePitch="360"/></w:sectPr>'
    return x

# ---------------------------------------------------------------- görseller, tablolar, bloklar
IMAGES = {}
def img_rid(fn):
    if fn not in IMAGES:
        w, h = Image.open(os.path.join(FIG, fn)).size
        IMAGES[fn] = ('rIdImg%d' % (len(IMAGES) + 1), w, h)
    return IMAGES[fn]

DOCPR = [200]
def figure(fn, width_cm, caption):
    rid, w, h = img_rid(fn)
    cx = int(width_cm * 360000); cy = int(cx * h / w)
    DOCPR[0] += 1; did = DOCPR[0]
    drw = ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="%d" cy="%d"/>'
           '<wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="%d" name="Resim %d"/>'
           '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
           '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:pic>'
           '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
           '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
           '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
           '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
           '</wp:inline></w:drawing></w:r>') % (cx, cy, did, did, did, fn, rid, cx, cy)
    # şekil açıklaması şeklin altında, 10 pt, tek aralık, şekille arasında 1,5 aralık (9 nk); sonda nokta yok
    return (para(drw, jc='center', before=0, after=0, line=240, keep=True) +
            para(run(caption, 20), jc='center' if len(caption) < 88 else 'both', before=180, after=SP_PARA,
                 line=240, sz=20))

def table(cols_cm, rows, sz=24):
    tw = [int(round(c * 567)) for c in cols_cm]
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in tw)
    bd = ''.join('<w:%s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % s
                 for s in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'))
    x = ('<w:tbl><w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders>%s</w:tblBorders>'
         '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="28" w:type="dxa"/><w:left w:w="85" w:type="dxa"/>'
         '<w:bottom w:w="28" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar>'
         '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
         '</w:tblPr><w:tblGrid>%s</w:tblGrid>') % (sum(tw), bd, grid)
    for i, row in enumerate(rows):
        x += '<w:tr><w:trPr><w:cantSplit/>%s</w:trPr>' % ('<w:tblHeader/>' if i == 0 else '')
        for j, cell in enumerate(row):
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="E7E6E6"/>' if i == 0 else ''
            x += '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s<w:vAlign w:val="center"/></w:tcPr>%s</w:tc>' % (
                tw[j], shd, para(run(cell, sz, b=(i == 0)), jc='left', after=0, line=240, sz=sz))
        x += '</w:tr>'
    return x + '</w:tbl>'

def blocks_xml(blocks, first_page):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'h1':   # bölüm başlığı: sayfanın üst kenarından ≈ 5 cm aşağıda, sonrasında 4,5 aralık
            out.append(para(run(b[1], 28, True), jc='left', before=454 if first_page else 0, after=SP_HEAD_AFTER,
                            keep=True, outline=0))
        elif k in ('h2', 'h3'):
            out.append(para(run(b[1], 24, True), jc='left', before=0, after=SP_PARA, keep=True,
                            outline=1 if k == 'h2' else 2))
        elif k == 'p':
            out.append(para(run(b[1]), jc='both', after=SP_PARA))
        elif k == 'fig':
            out.append(figure(b[1], b[2], b[3]))
        elif k == 'tbl':
            if b[1]:   # tablo açıklaması tablonun üstünde, tabloyla arasında 1,5 aralık
                out.append(para(run(b[1], 20), jc='left', before=0, after=180, line=240, keep=True, sz=20))
            out.append(table(b[2], b[3]))
            out.append(para('', jc='left', before=0, after=SP_PARA - 60, line=240, sz=4))
    return ''.join(out)

# ---------------------------------------------------------------- şablon yardımcıları
def strip_ids(el):
    for e in el.iter():
        for a in list(e.attrib):
            if a.startswith(W14):
                del e.attrib[a]
    return el

def ptext(p):
    return ''.join(p.itertext())

def set_cell(tc, xml, valign=None):
    for ch in list(tc):
        if ch.tag != W + 'tcPr':
            tc.remove(ch)
    for e in frag(xml):
        tc.append(e)
    if valign:
        tcpr = tc.find(W + 'tcPr')
        for v in tcpr.findall(W + 'vAlign'):
            tcpr.remove(v)
        v = etree.SubElement(tcpr, W + 'vAlign'); v.set(W + 'val', valign)

def append_after(root, label, value, sz=24, nth=0, b=False):
    hits = [p for p in root.iter(W + 'p') if ptext(p).replace('\xa0', ' ').strip().startswith(label)]
    for e in frag(run(value, sz, b)):
        hits[nth].append(e)

def regrid(tbl, grid):
    """Tablo genişliğini metin alanına (14,5 cm) uydurur; hücre genişliklerini sütun birleşimlerine göre yeniden yazar."""
    tp = tbl.find(W + 'tblPr')
    for e in tp.findall(W + 'tblpPr'):
        tp.remove(e)
    tw = tp.find(W + 'tblW')
    tw.set(W + 'w', str(sum(grid))); tw.set(W + 'type', 'dxa')
    if tp.find(W + 'tblLayout') is None:
        lay = etree.Element(W + 'tblLayout'); lay.set(W + 'type', 'fixed')
        anchor = tp.find(W + 'tblCellMar')
        if anchor is None: anchor = tp.find(W + 'tblLook')
        if anchor is not None: anchor.addprevious(lay)
        else: tp.append(lay)
    tg = tbl.find(W + 'tblGrid')
    for g in list(tg): tg.remove(g)
    for w in grid:
        g = etree.SubElement(tg, W + 'gridCol'); g.set(W + 'w', str(w))
    for tr in tbl.findall(W + 'tr'):
        col = 0
        for tc in tr.findall(W + 'tc'):
            gs = tc.find(W + 'tcPr/' + W + 'gridSpan')
            span = int(gs.get(W + 'val')) if gs is not None else 1
            tcw = tc.find(W + 'tcPr/' + W + 'tcW')
            tcw.set(W + 'w', str(sum(grid[col:col + span]))); tcw.set(W + 'type', 'dxa')
            col += span

def yonetici_row():
    lab = lambda t: run(t, 20, True)
    return ('<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="700"/></w:trPr><w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>'
            '<w:gridSpan w:val="3"/></w:tcPr>%s%s</w:tc></w:tr>') % (
        TEXT_W,
        para(lab('İŞLETME YÖNETİCİSİNİN (bölümün ilk sayfası);'), jc='left', before=40, after=0, line=240, sz=20),
        para(lab('ADI VE SOYADI: ') + run('[Yönetici Ad SOYAD]', 20) + lab('          İMZASI / KAŞE VEYA MÜHÜR:'),
             jc='left', before=60, after=60, line=240, sz=20))

# ---------------------------------------------------------------- çerçeve örnekleri ("(devam)" bölmesi)
def instances(breaks):
    out = []
    for fr in C.FRAMES:
        bl = fr['blocks']
        bounds = [0] + sorted(breaks.get(fr['id'], [])) + [len(bl)]
        for k in range(len(bounds) - 1):
            out.append(dict(fid=fr['id'], k=k, bolum=fr['bolum'], date=fr['date'], start=bounds[k],
                            end=bounds[k + 1], blocks=bl[bounds[k]:bounds[k + 1]],
                            title=fr['title'] if k == 0 else fr['title'] + ' (devam)'))
    seen = set()
    for ins in out:
        ins['first'] = ins['bolum'] not in seen
        seen.add(ins['bolum'])
    return out

def split(breaks, ins):
    """Taşan örneğin son bloğunu bir sonraki sayfaya taşır (başlık sayfa sonunda kalmaz)."""
    fid, s, e = ins['fid'], ins['start'], ins['end']
    blocks = [fr for fr in C.FRAMES if fr['id'] == fid][0]['blocks']
    nb = e - 1
    while nb > s and blocks[nb - 1][0] in ('h1', 'h2', 'h3'):
        nb -= 1
    if nb <= s:
        raise SystemExit('Bölünemiyor: %s (%d–%d) tek blok sayfaya sığmıyor' % (fid, s, e))
    br = set(breaks.get(fid, []))
    br.discard(e)
    br.add(nb)
    breaks[fid] = sorted(br)

# ---------------------------------------------------------------- belge
def build(insts, pages):
    IMAGES.clear(); DOCPR[0] = 200
    src = etree.parse(os.path.join(TPL, 'word', 'document.xml'))
    root = src.getroot(); body = root.find(W + 'body')
    T = list(body)
    cover, ickapak, week_t, frame_t = T[0], T[1:20], T[22], T[25]
    for ch in list(body):
        body.remove(ch)

    def fp(key):
        return pages['front'].get(key, '') if pages else '00'
    def ip(i):
        return str(pages['inst'][i]) if pages else '00'

    blank = [('default', 'rIdFB'), ('first', 'rIdFB')]
    # 1) dış kapak
    cv = strip_ids(copy.deepcopy(cover))
    sc = cv.find(W + 'sdtContent')
    last = sc.findall(W + 'p')[-1]
    if last.find('.//' + W + 'br') is not None:
        sc.remove(last)
    append_after(cv, 'DÖNEM', ' ' + C.DONEM, 36, b=True)
    append_after(cv, 'YIL', ' ' + C.YIL, 36, b=True)
    body.append(cv)
    for e in frag(tiny(sect=sectpr(ftr=blank, mar=(1417, 1417, 1417, 1417)))):
        body.append(e)

    # 2) iç kapak (şablondaki düzen korunur; yazılan değerler 12 pt)
    ik = [strip_ids(copy.deepcopy(e)) for e in ickapak]
    for e in ik:
        for t in e.iter(W + 't'):
            if 'MÜHENDİSLİĞİ BÖLÜMÜ' in (t.text or ''):
                t.text = 'ENERJİ SİSTEMLERİ MÜHENDİSLİĞİ BÖLÜMÜ'
    kimlik, ikamet, kurum = ik[12], ik[15], ik[18]
    for sp_p in (ik[13], ik[16]):   # tablolar arasındaki boş paragraflar küçültülür; iç kapak tek sayfada kalır
        for ch in list(sp_p):
            sp_p.remove(ch)
        for e in frag(para('', jc='left', before=0, after=0, line=240, sz=12))[0]:
            sp_p.append(e)
    for tb in (kimlik, ikamet, kurum):   # tam yükseklikli satırlar, değer sığsın diye "en az" yapılır
        for h in tb.iter(W + 'trHeight'):
            if h.get(W + 'hRule') == 'exact':
                del h.attrib[W + 'hRule']
    append_after(kimlik, 'Adı- Soyadı:', ' ' + C.AD)
    append_after(kimlik, 'Bölümü:', ' Enerji Sistemleri Mühendisliği')
    append_after(kimlik, 'Öğrenci No:', ' [Öğrenci No]')
    append_after(kimlik, 'Sınıfı:', ' 4')
    append_after(ikamet, 'Ülke:', ' Türkiye')
    append_after(kurum, 'Kurumun Adı:', ' Enerjisa Enerji A.Ş. (Müşteri Çözümleri – Enerji Verimliliği)')
    append_after(kurum, 'Telefon No:', ' 0216 579 05 79')
    append_after(kurum, 'Çalışma Alanı:', ' Elektrik ve enerji hizmetleri')
    append_after(kurum, 'Faks No:', ' 0216 579 05 30')
    append_after(kurum, 'Adresi:', ' Barbaros Mah. Begonya Sok. Nida Kule Ataşehir Batı Sitesi No: 1/1, Ataşehir/İstanbul')
    append_after(kurum, 'E-posta Adresi:', ' enerjisa-info@enerjisa.com')
    append_after(kurum, 'Web Adresi:', ' www.enerjisa.com.tr')
    for p in kurum.iter(W + 'p'):
        if 'Haftalık Çalışma Gün Sayısı' in ptext(p):
            for t in p.iter(W + 't'):
                if '…' in (t.text or ''):
                    t.text = t.text.replace('…', '5')
    append_after(kurum, 'Adı SOYADI:', ' [Yetkili Ad SOYAD]')
    append_after(kurum, 'Unvanı:', ' [Unvan]')
    for e in ik:
        body.append(e)
    for e in frag(tiny(sect=sectpr(ftr=blank, mar=(1417, 1417, 1417, 1417)))):
        body.append(e)

    # 3) ön sayfalar
    H = lambda t, first=False: para(run(t, 28, True), jc='left', before=1134, after=SP_HEAD_AFTER, keep=True,
                                    pbb=not first, outline=0)
    P = lambda t: para(run(t), jc='both', after=SP_PARA)
    fx = H('ÖNSÖZ', True) + ''.join(P(t) for t in C.ONSOZ)
    fx += para(run('Kasım 2026'), jc='right', before=240, after=0) + para(run(C.AD), jc='right', after=0)

    tabR = '<w:tab w:val="right" w:leader="dot" w:pos="%d"/>' % TEXT_W
    def toc_line(level, text, num):
        ind = {1: 0, 2: 397, 3: 794}[level]
        return para(run(text, 24, level == 1) + tab_run() + run(num, 24, level == 1), jc='left',
                    before=120 if level == 1 else 0, after=60, line=240, tabs=tabR,
                    ind='<w:ind w:left="%d" w:right="567" w:hanging="0"/>' % ind)
    fx += H('İÇİNDEKİLER')
    for key, label in [('onsoz', 'ÖNSÖZ'), ('simge', 'SİMGELER LİSTESİ'), ('sekil', 'ŞEKİLLER LİSTESİ'),
                       ('tablo', 'TABLOLAR LİSTESİ'), ('ozet', 'ÖZET'), ('hafta', 'HAFTALIK ÇALIŞMA TABLOLARI')]:
        fx += toc_line(1, label, fp(key))
    for i, ins in enumerate(insts):
        for b in ins['blocks']:
            if b[0] in ('h1', 'h2', 'h3'):
                fx += toc_line({'h1': 1, 'h2': 2, 'h3': 3}[b[0]], b[1], ip(i))

    tabS = '<w:tab w:val="left" w:pos="2041"/>'
    def sym(a, b_):
        return para(run(a) + tab_run() + run(b_), jc='left', after=20, line=240, tabs=tabS,
                    ind='<w:ind w:left="2041" w:hanging="2041"/>')
    fx += H('SİMGELER LİSTESİ') + ''.join(sym(a, b_) for a, b_ in C.SIMGELER)
    fx += para(run('Kısaltmalar', 24, True), jc='left', before=300, after=SP_PARA, keep=True, outline=1)
    fx += ''.join(sym(a, b_) for a, b_ in C.KISALTMALAR)

    def cap_list(prefix):
        out = ''
        for i, ins in enumerate(insts):
            for b in ins['blocks']:
                cap = b[3] if b[0] == 'fig' else (b[1] if b[0] == 'tbl' else '')
                if cap.startswith(prefix):
                    m = re.match(r'((?:Şekil|Tablo) \d+\.\d+) (.*)', cap)
                    out += para(run(m.group(1)) + tab_run() + run(m.group(2)) + tab_run() + run(ip(i)), jc='left',
                                after=120, line=240, tabs='<w:tab w:val="left" w:pos="1134"/>' + tabR,
                                ind='<w:ind w:left="1134" w:right="567" w:hanging="1134"/>')
        return out
    fx += H('ŞEKİLLER LİSTESİ') + cap_list('Şekil')
    fx += H('TABLOLAR LİSTESİ') + cap_list('Tablo')
    fx += H('ÖZET') + ''.join(P(t) for t in C.OZET)
    fx += tiny(sect=sectpr(ftr=[('default', 'rIdFS'), ('first', 'rIdFS')], fmt='lowerRoman', start=2))
    for e in frag(fx):
        body.append(e)

    # 4) haftalık çalışma tabloları (şablon tablosu, 14,5 cm genişliğe uydurulmuş)
    def refs_txt(refs):
        if not refs: return ''
        if not pages: return '00'
        nums = sorted({pages['inst'][i] for i, ins in enumerate(insts) if ins['fid'] in refs})
        return str(nums[0]) if len(nums) == 1 else '%d-%d' % (nums[0], nums[-1])
    c = lambda t, jc='center', b=False: para(run(t, 24, b), jc=jc, after=0, line=240)
    for wi, (start, end, days) in enumerate(C.HAFTALAR):
        t = strip_ids(copy.deepcopy(week_t))
        regrid(t, WEEK_GRID)
        rows = t.findall(W + 'tr')
        h0 = rows[0].find('.//' + W + 'trHeight'); h0.set(W + 'val', '640'); h0.attrib.pop(W + 'hRule', None)
        set_cell(rows[0].find(W + 'tc'), c('%s Tarihinden %s Tarihine Kadar Bir Haftalık Çalışma Tablosu'
                                           % (start, end), b=True), 'center')
        total, complete = 0, True
        for i, (d, text, refs, hrs) in enumerate(days):
            tr = rows[2 + i]; tcs = tr.findall(W + 'tc')
            tr.find('.//' + W + 'trHeight').set(W + 'val', '1400')
            dayname = ptext(tcs[1]).strip()
            set_cell(tcs[0], c(d), 'center')
            set_cell(tcs[1], c(dayname), 'center')
            set_cell(tcs[2], c(text, 'left'), 'center')
            set_cell(tcs[3], c(refs_txt(refs)), 'center')
            set_cell(tcs[4], c('' if hrs is None else str(hrs)), 'center')
            if hrs is None: complete = False
            else: total += hrs
        sat = (datetime.strptime(start, '%d.%m.%Y') + timedelta(days=5)).strftime('%d.%m.%Y')
        tcs = rows[7].findall(W + 'tc')
        for tc, v, jc in zip(tcs, [sat, 'Cumartesi', '–', '', ''], ['center', 'center', 'left', 'center', 'center']):
            set_cell(tc, c(v, jc), 'center')
        set_cell(rows[8].findall(W + 'tc')[-1], c(str(total) if complete else '', b=True), 'center')
        sig_l, sig_r = rows[10].findall(W + 'tc')
        append_after(sig_l, 'Adı SOYADI:', ' ' + C.AD)
        append_after(sig_l, 'Çalıştığı Bölüm:', ' Enerji Verimliliği')
        append_after(sig_r, 'Adı SOYADI:', ' [Yetkili Ad SOYAD]')
        append_after(sig_r, 'Unvanı:', ' [Unvan]')
        body.append(t)
        if wi < len(C.HAFTALAR) - 1:
            for e in frag(tiny(br=True)):
                body.append(e)
    for e in frag(tiny(sect=sectpr(ftr=[('default', 'rIdFR'), ('first', 'rIdFR')], fmt='lowerRoman'))):
        body.append(e)

    # 5) gövde: her bölüm ayrı kesit, her "Yapılan İş" çerçevesi bir sayfa
    groups = []
    for i, ins in enumerate(insts):
        if not groups or groups[-1][0] != ins['bolum']:
            groups.append((ins['bolum'], []))
        groups[-1][1].append(ins)
    for gi, (bolum, grp) in enumerate(groups):
        for fi, ins in enumerate(grp):
            t = strip_ids(copy.deepcopy(frame_t))
            regrid(t, FRAME_GRID)
            rows = t.findall(W + 'tr')
            c0, c1 = rows[0].findall(W + 'tc')
            set_cell(c0, para(run('Yapılan İş: ') + run(ins['title'], 24, True), jc='left', after=0, line=240))
            set_cell(c1, para(run('Tarih: ') + run(ins['date'], 24, True), jc='left', after=0, line=240))
            rows[1].find('.//' + W + 'trHeight').set(W + 'val', str(AC_H_FIRST if ins['first'] else AC_H))
            set_cell(rows[1].find(W + 'tc'),
                     para(run('Açıklama:', 24, True), jc='left', after=60, line=240) +
                     blocks_xml(ins['blocks'], ins['first']))
            append_after(rows[2], 'ADI VE SOYADI:', ' [Sorumlu Ad SOYAD]', 20)
            for tt in rows[2].findall(W + 'tc')[1].iter(W + 't'):
                if (tt.text or '').replace('\xa0', ' ').strip().startswith('İMZASI'):
                    tt.text = 'İMZASI / KAŞESİ: '
                    tt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            if ins['first']:
                for e in frag('<w:tbl>' + yonetici_row() + '</w:tbl>')[0].findall(W + 'tr'):
                    t.append(e)
            body.append(t)
            if fi < len(grp) - 1:
                for e in frag(tiny(br=True)):
                    body.append(e)
        sp = sectpr(hdr=[('default', 'rIdHN'), ('first', 'rIdHB')], ftr=blank, title_pg=True, fmt='decimal',
                    start=1 if gi == 0 else None)
        if gi < len(groups) - 1:
            for e in frag(tiny(sect=sp)):
                body.append(e)
        else:
            body.append(frag(sp)[0])
    return src

def _field(fmt_rpr, sample):
    return ('<w:r>%s<w:fldChar w:fldCharType="begin"/></w:r><w:r>%s<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            '<w:r>%s<w:fldChar w:fldCharType="separate"/></w:r><w:r>%s<w:t>%s</w:t></w:r>'
            '<w:r>%s<w:fldChar w:fldCharType="end"/></w:r>') % (fmt_rpr, fmt_rpr, fmt_rpr, fmt_rpr, sample, fmt_rpr)
ARIAL_B = '<w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:bCs/><w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
TNR12 = '<w:rPr>' + TNR + '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr>'
HDR_FTR = {
    'header_num.xml': ('hdr', '<w:p><w:pPr><w:jc w:val="right"/></w:pPr>%s</w:p>' % _field(ARIAL_B, '2')),
    'header_blank.xml': ('hdr', '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'),
    'footer_roman.xml': ('ftr', '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>%s</w:p>' % _field(TNR12, 'ii')),
    # ön sayfalar: her sayfanın altında İME sorumlusunun imza ve kaşesi (Yönerge m. 10/4)
    'footer_roman_imza.xml': ('ftr', '<w:p><w:pPr><w:spacing w:after="60"/><w:jc w:val="right"/></w:pPr>%s</w:p>'
                              '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>%s</w:p>'
                              % (run('İME sorumlusu (ad soyad, imza, kaşe): ……………………………………', 20), _field(TNR12, 'ii'))),
    'footer_blank.xml': ('ftr', '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'),
}
RIDS = {'header_num.xml': 'rIdHN', 'header_blank.xml': 'rIdHB', 'footer_roman.xml': 'rIdFR',
        'footer_roman_imza.xml': 'rIdFS', 'footer_blank.xml': 'rIdFB'}

def write_docx(doc, path):
    work = os.path.join(OUT, 'pkg')
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(TPL, work)
    doc.write(os.path.join(work, 'word', 'document.xml'), xml_declaration=True, encoding='UTF-8', standalone=True)
    for fn, (kind, inner) in HDR_FTR.items():
        with open(os.path.join(work, 'word', fn), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:%s %s>%s</w:%s>' % (kind, NSDECL, inner, kind))
    os.makedirs(os.path.join(work, 'word', 'media'), exist_ok=True)
    rels_p = os.path.join(work, 'word', '_rels', 'document.xml.rels')
    rels = open(rels_p, encoding='utf-8').read()
    add = ''
    for fn, rid in RIDS.items():
        kind = 'header' if fn.startswith('header') else 'footer'
        add += '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/%s" Target="%s"/>' % (rid, kind, fn)
    for fn, (rid, w, h) in IMAGES.items():
        shutil.copy(os.path.join(FIG, fn), os.path.join(work, 'word', 'media', fn))
        add += '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/%s"/>' % (rid, fn)
    open(rels_p, 'w', encoding='utf-8').write(rels.replace('</Relationships>', add + '</Relationships>'))
    ct_p = os.path.join(work, '[Content_Types].xml')
    ct = open(ct_p, encoding='utf-8').read()
    add = '' if 'Extension="png"' in ct else '<Default Extension="png" ContentType="image/png"/>'
    for fn in RIDS:
        kind = 'header' if fn.startswith('header') else 'footer'
        add += '<Override PartName="/word/%s" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>' % (fn, kind)
    open(ct_p, 'w', encoding='utf-8').write(ct.replace('</Types>', add + '</Types>'))
    if os.path.exists(path):
        os.remove(path)
    subprocess.run(['zip', '-q', '-X', '-r', path, '.'], cwd=work, check=True)

def to_pdf(docx):
    cmd = (['/usr/bin/python3', SOFFICE] if os.path.exists(SOFFICE) else ['soffice'])
    subprocess.run(cmd + ['--headless', '--convert-to', 'pdf', '--outdir', OUT, docx], check=True, capture_output=True)
    return docx[:-5] + '.pdf'

def page_texts(pdf):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    return [subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), pdf, '-'],
                           capture_output=True, text=True).stdout for i in range(1, n + 1)]

ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi',
         'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx']

def analyse(pdf, insts):
    pt = page_texts(pdf)
    first_line = lambda t: next((ln.strip() for ln in t.splitlines() if ln.strip()), '')
    front = {}
    for k, h in {'onsoz': 'ÖNSÖZ', 'icindekiler': 'İÇİNDEKİLER', 'simge': 'SİMGELER LİSTESİ',
                 'sekil': 'ŞEKİLLER LİSTESİ', 'tablo': 'TABLOLAR LİSTESİ', 'ozet': 'ÖZET'}.items():
        for i, t in enumerate(pt):
            if first_line(t) == h:
                front[k] = ROMAN[i]   # fiziksel sayfa i+1 → roma (i+1)−1
                break
    for i, t in enumerate(pt):
        if 'Tarihinden' in t and 'Tarihine Kadar' in t:
            front['hafta'] = ROMAN[i]
            break
    body0 = next(i for i, t in enumerate(pt) if 'Yapılan İş:' in t)
    groups = []
    for i in range(body0, len(pt)):
        if 'Yapılan İş:' in pt[i]:
            groups.append([i])
        elif groups:
            groups[-1].append(i)
    res = dict(front=front, npages=len(pt), body0=body0 + 1, problems=[])
    if len(groups) != len(insts):
        res['problems'].append('çerçeve sayısı %d, beklenen %d' % (len(groups), len(insts)))
    res['overflow'] = [k for k, g in enumerate(groups) if len(g) > 1]
    res['inst'] = [g[0] - body0 + 1 for g in groups]
    return res

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    bfile = os.path.join(OUT, 'breaks.json')
    breaks = json.load(open(bfile)) if os.path.exists(bfile) else {}
    final = os.path.join(OUT, 'IME-On-Rapor.docx')
    pages = None
    for it in range(1, 16):
        insts = instances(breaks)
        write_docx(build(insts, pages), final)
        res = analyse(to_pdf(final), insts)
        print('geçiş %d: %d sayfa, %d çerçeve, taşan: %s %s' % (
            it, res['npages'], len(insts), [insts[k]['fid'] for k in res['overflow']], res['problems']), flush=True)
        if res['overflow']:
            for k in res['overflow']:
                split(breaks, insts[k])
            json.dump(breaks, open(bfile, 'w'))
            pages = None
            continue
        if res['problems']:
            raise SystemExit('Sorun: %s' % res['problems'])
        if pages and pages['front'] == res['front'] and pages['inst'] == res['inst']:
            print('tamam:', json.dumps({'front': res['front'], 'npages': res['npages']}, ensure_ascii=False))
            break
        pages = res
