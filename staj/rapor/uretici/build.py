# -*- coding: utf-8 -*-
"""İME ön raporu üretici: şablon XML'ini doldurur, iki geçişte sayfa numaralarını yerleştirir."""
import copy, json, os, re, shutil, subprocess, sys
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

AC_H = 12200            # Açıklama satırının asgari yüksekliği (twip)
TEXT_W_FRONT = 11906 - 2 * 1843   # ön sayfalarda metin genişliği

def frag(xml):
    return list(etree.fromstring('<w:body %s>%s</w:body>' % (NSDECL, xml)))

TNR = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
def rpr(sz=24, b=False):
    return '<w:rPr>%s%s<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (TNR, '<w:b/><w:bCs/>' if b else '', sz, sz)
def run(t, sz=24, b=False):
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr(sz, b), escape(t))
def tab_run(sz=24, b=False):
    return '<w:r>%s<w:tab/></w:r>' % rpr(sz, b)
def para(runs, jc='both', before=0, after=120, line=276, keep=False, ind='', pbb=False, sz=24,
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

def sectpr(hdr=(), ftr=(), title_pg=False, fmt=None, start=None, mar=(1417, 1417, 1417, 1417)):
    x = '<w:sectPr>'
    for t, rid in hdr: x += '<w:headerReference w:type="%s" r:id="%s"/>' % (t, rid)
    for t, rid in ftr: x += '<w:footerReference w:type="%s" r:id="%s"/>' % (t, rid)
    x += '<w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
    top, right, bottom, left = mar
    x += ('<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="708" w:footer="708" '
          'w:gutter="0"/>') % (top, right, bottom, left)
    if fmt or start is not None:
        x += '<w:pgNumType%s%s/>' % (' w:fmt="%s"' % fmt if fmt else '', ' w:start="%d"' % start if start is not None else '')
    x += '<w:cols w:space="708"/>' + ('<w:titlePg/>' if title_pg else '') + '<w:docGrid w:linePitch="360"/></w:sectPr>'
    return x

# ---------------------------------------------------------------- görseller
IMAGES = {}   # dosya -> (rid, px_w, px_h)
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
    return (para(drw, jc='center', before=120, after=0, line=240, keep=True) +
            para(run(caption, 20), jc='center', before=170, after=160, line=240, sz=20))

def table(cols_cm, rows, sz=20):
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

def blocks_xml(blocks):
    out = []
    for b in blocks:
        k = b[0]
        if k == 'h1':
            out.append(para(run(b[1], 28, True), jc='left', before=60, after=240, keep=True, outline=0))
        elif k == 'h2':
            out.append(para(run(b[1], 24, True), jc='left', before=160, after=120, keep=True, outline=1))
        elif k == 'h3':
            out.append(para(run(b[1], 24, True), jc='left', before=120, after=100, keep=True, outline=2))
        elif k == 'p':
            out.append(para(run(b[1]), jc='both', after=120))
        elif k == 'li':
            out.append(para(run(b[1]), jc='both', after=80, ind='<w:ind w:left="397" w:hanging="397"/>'))
        elif k == 'fig':
            out.append(figure(b[1], b[2], b[3]))
        elif k == 'tbl':
            if b[1]:
                out.append(para(run(b[1], 20), jc='left', before=120, after=170, line=240, keep=True, sz=20))
            out.append(table(b[2], b[3]))
            out.append(para('', jc='left', before=0, after=60, line=240, sz=12))
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

def append_after(root, label, value, sz=20, nth=0, b=False):
    """label ile başlayan nth paragrafın sonuna değer ekler."""
    hits = [p for p in root.iter(W + 'p') if ptext(p).replace('\xa0', ' ').strip().startswith(label)]
    p = hits[nth]
    for e in frag(run(value, sz, b)):
        p.append(e)

# ---------------------------------------------------------------- belge kurulumu
def build(pages):
    """pages: {'front': {anahtar: roma}, 'frames': {id: sayfa}} ya da None (1. geçiş)."""
    IMAGES.clear(); DOCPR[0] = 200
    src = etree.parse(os.path.join(TPL, 'word', 'document.xml'))
    root = src.getroot(); body = root.find(W + 'body')
    T = list(body)
    cover, ickapak, week_t, frame_t = T[0], T[1:21], T[22], T[25]
    for ch in list(body):
        body.remove(ch)

    def fp(key):   # ön sayfa numarası
        return pages['front'].get(key, '') if pages else '00'
    def bp(fid):   # gövde sayfa numarası
        return str(pages['frames'][fid]) if pages else '00'

    # 1) dış kapak
    cv = strip_ids(copy.deepcopy(cover))
    sc = cv.find(W + 'sdtContent')
    last = sc.findall(W + 'p')[-1]
    if last.find('.//' + W + 'br') is not None:
        sc.remove(last)
    append_after(cv, 'DÖNEM', ' ' + C.DONEM, 36, b=True)
    append_after(cv, 'YIL', ' ' + C.YIL, 36, b=True)
    body.append(cv)
    for e in frag(tiny(sect=sectpr(ftr=[('default', 'rIdFB'), ('first', 'rIdFB')]))):
        body.append(e)

    # 2) iç kapak
    ik = [strip_ids(copy.deepcopy(e)) for e in ickapak]
    for e in ik:
        for t in e.iter(W + 't'):
            if 'MÜHENDİSLİĞİ BÖLÜMÜ' in (t.text or ''):
                t.text = 'ENERJİ SİSTEMLERİ MÜHENDİSLİĞİ BÖLÜMÜ'
    kimlik, ikamet, kurum = ik[12], ik[15], ik[18]
    append_after(kimlik, 'Adı- Soyadı:', ' ' + C.AD)
    append_after(kimlik, 'Bölümü:', ' Enerji Sistemleri Mühendisliği')
    append_after(kimlik, 'Öğrenci No:', ' [Öğrenci No]')
    append_after(kimlik, 'Sınıfı:', ' 4')
    append_after(ikamet, 'Ülke:', ' Türkiye')
    append_after(kurum, 'Kurumun Adı:', ' Enerjisa Enerji A.Ş. (Müşteri Çözümleri – Enerji Verimliliği)', 18)
    append_after(kurum, 'Telefon No:', ' 0216 579 05 79', 18)
    append_after(kurum, 'Çalışma Alanı:', ' Elektrik dağıtımı, perakende satışı ve müşteri enerji çözümleri', 18)
    append_after(kurum, 'Faks No:', ' 0216 579 05 30', 18)
    append_after(kurum, 'Adresi:', ' Barbaros Mah. Begonya Sok. Nida Kule Ataşehir Batı Sitesi No: 1/1, 34746 Ataşehir/İstanbul', 18)
    append_after(kurum, 'E-posta Adresi:', ' enerjisa-info@enerjisa.com', 18)
    append_after(kurum, 'Web Adresi:', ' www.enerjisa.com.tr', 18)
    for t in kurum.iter(W + 't'):
        if t.text and '…' in t.text and 'Gün' not in t.text:
            t.text = t.text.replace('…', '5')
    for p in kurum.iter(W + 'p'):
        if 'Haftalık Çalışma Gün Sayısı' in ptext(p):
            for t in p.iter(W + 't'):
                if '…' in (t.text or ''):
                    t.text = t.text.replace('…', '5')
    append_after(kurum, 'Adı SOYADI:', ' [Yetkili Ad SOYAD]', 18)
    append_after(kurum, 'Unvanı:', ' [Unvan]', 18)
    for e in ik:
        body.append(e)
    for e in frag(tiny(sect=sectpr(ftr=[('default', 'rIdFB'), ('first', 'rIdFB')]))):
        body.append(e)

    # 3) ön sayfalar
    H = lambda t, first=False: para(run(t, 28, True), jc='left', before=1134, after=720, keep=True,
                                    pbb=not first, outline=0)
    P = lambda t: para(run(t), jc='both', after=120)
    fx = H('ÖNSÖZ', True) + ''.join(P(t) for t in C.ONSOZ)
    fx += para(run('Kasım 2026'), jc='right', before=480, after=0) + para(run(C.AD), jc='right', after=0)

    # içindekiler
    tabR = '<w:tab w:val="right" w:leader="dot" w:pos="%d"/>' % TEXT_W_FRONT
    def toc_line(level, text, num):
        ind = {1: 0, 2: 397, 3: 794}[level]
        return para(run(text, 24, level == 1) + tab_run() + run(num, 24, level == 1), jc='left',
                    before=60 if level == 1 else 0, after=40, line=240, tabs=tabR,
                    ind='<w:ind w:left="%d" w:right="567" w:hanging="0"/>' % ind if ind else '<w:ind w:right="0"/>')
    fx += H('İÇİNDEKİLER')
    for key, label in [('onsoz', 'ÖNSÖZ'), ('simge', 'SİMGELER VE KISALTMALAR'), ('sekil', 'ŞEKİLLER LİSTESİ'),
                       ('tablo', 'TABLOLAR LİSTESİ'), ('ozet', 'ÖZET'), ('hafta', 'HAFTALIK ÇALIŞMA TABLOLARI')]:
        fx += toc_line(1, label, fp(key))
    for fr in C.FRAMES:
        for lvl, txt in fr['toc']:
            fx += toc_line(lvl, txt, bp(fr['id']))

    # simgeler ve kısaltmalar
    tabS = '<w:tab w:val="left" w:pos="2268"/>'
    def sym(a, b_):
        return para(run(a) + tab_run() + run(b_), jc='left', after=40, line=240, tabs=tabS,
                    ind='<w:ind w:left="2268" w:hanging="2268"/>')
    fx += H('SİMGELER VE KISALTMALAR')
    fx += para(run('Simgeler', 24, True), jc='left', after=120, keep=True)
    fx += ''.join(sym(a, b_) for a, b_ in C.SIMGELER)
    fx += para(run('Kısaltmalar', 24, True), jc='left', before=240, after=120, keep=True)
    fx += ''.join(sym(a, b_) for a, b_ in C.KISALTMALAR)

    # şekil ve tablo listeleri
    def cap_list(prefix):
        items = []
        for fr in C.FRAMES:
            for b in fr['blocks']:
                if b[0] == 'fig' and prefix == 'Şekil':
                    items.append((b[3], fr['id']))
                if b[0] == 'tbl' and prefix == 'Tablo' and b[1].startswith('Tablo'):
                    items.append((b[1], fr['id']))
        out = ''
        for cap, fid in items:
            m = re.match(r'((?:Şekil|Tablo) \d+\.\d+) (.*)', cap)
            out += para(run(m.group(1)) + tab_run() + run(m.group(2)) + tab_run() + run(bp(fid)), jc='left',
                        after=80, line=240, tabs='<w:tab w:val="left" w:pos="1134"/>' + tabR,
                        ind='<w:ind w:left="1134" w:right="567" w:hanging="1134"/>')
        return out
    fx += H('ŞEKİLLER LİSTESİ') + cap_list('Şekil')
    fx += H('TABLOLAR LİSTESİ') + cap_list('Tablo')
    fx += H('ÖZET') + ''.join(P(t) for t in C.OZET)
    fx += tiny(sect=sectpr(ftr=[('default', 'rIdFR'), ('first', 'rIdFR')], fmt='lowerRoman', start=2,
                           mar=(1701, 1843, 1417, 1843)))
    for e in frag(fx):
        body.append(e)

    # 4) haftalık çalışma tabloları
    from datetime import datetime, timedelta
    for wi, (start, end, days) in enumerate(C.HAFTALAR):
        t = strip_ids(copy.deepcopy(week_t))
        rows = t.findall(W + 'tr')
        set_cell(rows[0].find(W + 'tc'), para(run('%s Tarihinden %s Tarihine Kadar Bir Haftalık Çalışma Tablosu'
                                                  % (start, end), 22, True), jc='center', after=0, line=240, sz=22), 'center')
        total = 0; complete = True
        for i, (d, text, refs, hrs) in enumerate(days):
            tr = rows[2 + i]; tcs = tr.findall(W + 'tc')
            tr.find('.//' + W + 'trHeight').set(W + 'val', '1250')
            dayname = ptext(tcs[1]).strip()
            set_cell(tcs[0], para(run(d, 20), jc='center', after=0, line=240, sz=20), 'center')
            set_cell(tcs[1], para(run(dayname, 20), jc='center', after=0, line=240, sz=20), 'center')
            set_cell(tcs[2], para(run(text, 20), jc='left', after=0, line=240, sz=20), 'center')
            nums = sorted({int(bp(r)) for r in refs}) if (refs and pages) else []
            ref = ('%d' % nums[0] if len(nums) == 1 else '%d-%d' % (nums[0], nums[-1])) if nums else ('00' if refs else '')
            set_cell(tcs[3], para(run(ref, 20), jc='center', after=0, line=240, sz=20), 'center')
            set_cell(tcs[4], para(run('' if hrs is None else str(hrs), 20), jc='center', after=0, line=240, sz=20), 'center')
            if hrs is None: complete = False
            else: total += hrs
        sat = (datetime.strptime(start, '%d.%m.%Y') + timedelta(days=5)).strftime('%d.%m.%Y')
        tcs = rows[7].findall(W + 'tc')
        set_cell(tcs[0], para(run(sat, 20), jc='center', after=0, line=240, sz=20), 'center')
        set_cell(tcs[1], para(run('Cumartesi', 20), jc='center', after=0, line=240, sz=20), 'center')
        set_cell(tcs[2], para(run('–', 20), jc='left', after=0, line=240, sz=20), 'center')
        set_cell(tcs[3], para(run('', 20), jc='center', after=0, line=240, sz=20), 'center')
        set_cell(tcs[4], para(run('', 20), jc='center', after=0, line=240, sz=20), 'center')
        tcs = rows[8].findall(W + 'tc')
        set_cell(tcs[-1], para(run(str(total) if complete else '', 20, True), jc='center', after=0, line=240, sz=20), 'center')
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

    # 5) gövde: çerçeveli sayfalar, her bölüm ayrı kesit
    groups = []
    for fr in C.FRAMES:
        if not groups or groups[-1][0] != fr['bolum']:
            groups.append((fr['bolum'], []))
        groups[-1][1].append(fr)
    for gi, (bolum, frs) in enumerate(groups):
        for fi, fr in enumerate(frs):
            t = strip_ids(copy.deepcopy(frame_t))
            rows = t.findall(W + 'tr')
            c0, c1 = rows[0].findall(W + 'tc')
            set_cell(c0, para(run('Yapılan İş: ', 22) + run(fr['title'], 22, True), jc='left', after=0, line=240, sz=22))
            set_cell(c1, para(run('Tarih: ', 22) + run(fr['date'], 22, True), jc='left', after=0, line=240, sz=22))
            rows[1].find('.//' + W + 'trHeight').set(W + 'val', str(AC_H))
            set_cell(rows[1].find(W + 'tc'),
                     para(run('Açıklama:', 20, True), jc='left', after=60, line=240, sz=20) + blocks_xml(fr['blocks']))
            append_after(rows[2], 'ADI VE SOYADI:', ' [Sorumlu Ad SOYAD]', 20)
            body.append(t)
            if fi < len(frs) - 1:
                for e in frag(tiny(br=True)):
                    body.append(e)
        sp = sectpr(hdr=[('default', 'rIdHN'), ('first', 'rIdHB')], ftr=[('default', 'rIdFB'), ('first', 'rIdFB')],
                    title_pg=True, fmt='decimal', start=1 if gi == 0 else None)
        if gi < len(groups) - 1:
            for e in frag(tiny(sect=sp)):
                body.append(e)
        else:
            body.append(frag(sp)[0])
    return src

HDR_FTR = {
    'header_num.xml': ('hdr', '<w:p><w:pPr><w:jc w:val="right"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr></w:pPr>'
                       '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                       '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
                       '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                       '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr><w:t>1</w:t></w:r>'
                       '<w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:b/><w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p>'),
    'header_blank.xml': ('hdr', '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'),
    'footer_roman.xml': ('ftr', '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
                         '<w:r><w:rPr>' + TNR + '<w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>'
                         '<w:r><w:rPr>' + TNR + '<w:sz w:val="24"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
                         '<w:r><w:rPr>' + TNR + '<w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="separate"/></w:r>'
                         '<w:r><w:rPr>' + TNR + '<w:sz w:val="24"/></w:rPr><w:t>ii</w:t></w:r>'
                         '<w:r><w:rPr>' + TNR + '<w:sz w:val="24"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r></w:p>'),
    'footer_blank.xml': ('ftr', '<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>'),
}
RIDS = {'header_num.xml': 'rIdHN', 'header_blank.xml': 'rIdHB', 'footer_roman.xml': 'rIdFR', 'footer_blank.xml': 'rIdFB'}

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
    rels = rels.replace('</Relationships>', add + '</Relationships>')
    open(rels_p, 'w', encoding='utf-8').write(rels)
    ct_p = os.path.join(work, '[Content_Types].xml')
    ct = open(ct_p, encoding='utf-8').read()
    add = ''
    if 'Extension="png"' not in ct:
        add += '<Default Extension="png" ContentType="image/png"/>'
    for fn in RIDS:
        kind = 'header' if fn.startswith('header') else 'footer'
        add += '<Override PartName="/word/%s" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/>' % (fn, kind)
    ct = ct.replace('</Types>', add + '</Types>')
    open(ct_p, 'w', encoding='utf-8').write(ct)
    if os.path.exists(path):
        os.remove(path)
    subprocess.run(['zip', '-q', '-X', '-r', path, '.'], cwd=work, check=True)

def to_pdf(docx):
    cmd = (['/usr/bin/python3', SOFFICE] if os.path.exists(SOFFICE) else ['soffice'])
    subprocess.run(cmd + ['--headless', '--convert-to', 'pdf', '--outdir', OUT, docx], check=True, capture_output=True)
    return docx[:-5] + '.pdf'

def page_texts(pdf):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    out = []
    for i in range(1, n + 1):
        out.append(subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), pdf, '-'],
                                  capture_output=True, text=True).stdout)
    return out

ROMAN = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi',
         'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv']

def analyse(pdf):
    pt = page_texts(pdf)
    def first_line(t):
        for ln in t.splitlines():
            if ln.strip():
                return ln.strip()
        return ''
    front = {}
    heads = {'onsoz': 'ÖNSÖZ', 'icindekiler': 'İÇİNDEKİLER', 'simge': 'SİMGELER VE KISALTMALAR',
             'sekil': 'ŞEKİLLER LİSTESİ', 'tablo': 'TABLOLAR LİSTESİ', 'ozet': 'ÖZET'}
    for k, h in heads.items():
        for i, t in enumerate(pt):
            if first_line(t) == h:
                front[k] = ROMAN[i + 1 - 1]   # fiziksel sayfa p → roma (p-1)
                break
    for i, t in enumerate(pt):
        if 'Tarihinden' in t and 'Haftalık' in t:
            front['hafta'] = ROMAN[i]
            break
    frames = {}; phys = {}
    for fr in C.FRAMES:
        pat = re.compile(r'Yapılan İş:\s*' + re.escape(fr['title']) + r'(?!\s*\(devam\))')
        hits = [i for i, t in enumerate(pt) if pat.search(t)]
        phys[fr['id']] = hits
    first = phys[C.FRAMES[0]['id']][0]
    problems = []
    for k, fr in enumerate(C.FRAMES):
        h = phys[fr['id']]
        if len(h) != 1:
            problems.append('%s başlığı %d sayfada bulundu' % (fr['id'], len(h)))
            continue
        frames[fr['id']] = h[0] - first + 1
        if h[0] != first + k:
            problems.append('%s beklenen sayfada değil (taşma?)' % fr['id'])
    if len(pt) != first + len(C.FRAMES):
        problems.append('toplam sayfa %d, beklenen %d' % (len(pt), first + len(C.FRAMES)))
    return dict(front=front, frames=frames, problems=problems, npages=len(pt), first=first + 1)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    d1 = os.path.join(OUT, 'gecis1.docx')
    write_docx(build(None), d1)
    a1 = analyse(to_pdf(d1))
    print('1. geçiş:', json.dumps(a1, ensure_ascii=False))
    final = os.path.join(OUT, 'IME-On-Rapor.docx')
    write_docx(build(a1), final)
    a2 = analyse(to_pdf(final))
    print('2. geçiş:', json.dumps(a2, ensure_ascii=False))
    if a2['front'] != a1['front'] or a2['frames'] != a1['frames']:
        print('UYARI: sayfa numaraları ikinci geçişte değişti')
