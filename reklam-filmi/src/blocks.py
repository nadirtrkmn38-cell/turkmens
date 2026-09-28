# Bright Correct reklam filmi - görsellerdeki yazı bloklarının konumları
#
# Her kutu (x0, y0, x1, y1) kaynak görselin piksel koordinatındadır.
# Bu kutulardaki koyu yazılar arka plandan ayrılıp ayrı katman olarak canlandırılır.
#   k   : arka plan tahmini için morfolojik kapama çekirdeği (kalın yazıda büyük)
#   thr : yazı sayılması için arka plana göre minimum koyuluk farkı

BLOCKS = {
    # Damlalık - "Bilimin gücü leke karşıtı bakımda."
    3: [
        dict(id='hdr_l', box=(44, 124, 134, 137)),
        dict(id='hdr_t', box=(138, 106, 400, 139)),
        dict(id='hdr_r', box=(400, 124, 494, 137)),
        dict(id='hdr_s', box=(138, 139, 400, 164)),
        dict(id='l1', box=(94, 430, 422, 508), k=35),
        dict(id='l2', box=(94, 504, 376, 575), k=35),
        dict(id='l3', box=(94, 575, 338, 636), k=35),
        dict(id='dash', box=(96, 662, 164, 682)),
        dict(id='bc', box=(96, 944, 458, 983)),
        dict(id='s1', box=(96, 994, 310, 1028)),
        dict(id='s2', box=(96, 1027, 408, 1056)),
    ],
    # Damlalık + şişe ağzı - "Bright Correct"
    7: [
        dict(id='hdr_l', box=(82, 93, 162, 109)),
        dict(id='hdr_t', box=(166, 74, 426, 104)),
        dict(id='hdr_r', box=(426, 93, 506, 109)),
        dict(id='hdr_s', box=(166, 105, 430, 129)),
        dict(id='bright', box=(68, 212, 454, 368), k=45),
        dict(id='correct', box=(42, 338, 484, 462), k=45),
        dict(id='s1', box=(70, 478, 342, 521)),
        dict(id='s2', box=(68, 521, 446, 560)),
        dict(id='dash', box=(70, 608, 136, 628)),
        dict(id='t1', box=(72, 650, 332, 712), k=31),
        dict(id='t2', box=(72, 708, 284, 765), k=31),
        dict(id='t3', box=(72, 764, 258, 814), k=31),
    ],
    # Cilt üzerinde serum - üç fayda
    1: [
        dict(id='bc', box=(74, 58, 502, 101)),
        dict(id='rule', box=(74, 120, 154, 136)),
        dict(id='h1', box=(72, 158, 306, 262), k=41),
        dict(id='h2', box=(72, 266, 642, 364), k=41),
        dict(id='h3', box=(72, 364, 708, 464), k=41),
        dict(id='h4', box=(72, 464, 602, 566), k=41),
        dict(id='c1t', box=(268, 638, 464, 702), lmax=170),
        dict(id='c1l', shift=26, box=(466, 668, 802, 700), lmax=128),
        dict(id='c1b', box=(268, 706, 572, 830), lmax=170),
        dict(id='c2t', box=(226, 870, 452, 936), lmax=170),
        dict(id='c2l', shift=26, box=(458, 900, 802, 932), lmax=128),
        dict(id='c2b', box=(226, 940, 464, 1036), lmax=170),
        dict(id='c3t', box=(228, 1078, 486, 1142), lmax=170),
        dict(id='c3l', shift=26, box=(490, 1066, 760, 1134), lmax=128),
        dict(id='c3b', box=(230, 1146, 486, 1274), lmax=170),
    ],
    # Molekül baloncukları - üç aktif içerik
    2: [
        dict(id='n_t', box=(78, 80, 392, 140), k=31),
        dict(id='n_r', box=(80, 148, 146, 168)),
        dict(id='n_b', box=(78, 170, 462, 334)),
        dict(id='a_t', box=(66, 594, 462, 646), k=31),
        dict(id='a_r', box=(72, 654, 140, 676)),
        dict(id='a_b', box=(72, 678, 396, 876)),
        dict(id='t_t', box=(76, 1132, 472, 1182), k=31),
        dict(id='t_r', box=(78, 1186, 146, 1208)),
        dict(id='t_b', box=(76, 1208, 426, 1402)),
    ],
    # Şişe + "içermez" listesi
    6: [
        dict(id='i1', box=(546, 206, 688, 350)),
        dict(id='l1', box=(704, 242, 852, 318)),
        dict(id='i2', box=(546, 372, 688, 517)),
        dict(id='l2', box=(704, 392, 844, 500)),
        dict(id='i3', box=(546, 540, 688, 684)),
        dict(id='l3', box=(704, 574, 928, 654)),
        dict(id='i4', box=(546, 710, 688, 852)),
        dict(id='l4', box=(704, 742, 928, 822)),
        dict(id='i5', box=(546, 882, 688, 1024)),
        dict(id='l5', box=(704, 920, 846, 1000)),
        dict(id='i6', box=(546, 1046, 688, 1188)),
        dict(id='l6', box=(704, 1080, 888, 1156)),
    ],
    # Kişiselleştirme - analiz / denge / tolerans
    5: [
        dict(id='h1', box=(86, 154, 632, 246), k=41),
        dict(id='h2', box=(86, 248, 896, 354), k=41),
        dict(id='h3', box=(86, 338, 628, 446), k=41),
        dict(id='i1', box=(88, 498, 246, 658)),
        dict(id='b1', box=(258, 538, 274, 620)),
        dict(id='l1', box=(294, 546, 554, 598)),
        dict(id='i2', box=(86, 680, 248, 842)),
        dict(id='b2', box=(258, 718, 274, 808)),
        dict(id='l2', box=(296, 712, 606, 810)),
        dict(id='i3', box=(86, 862, 248, 1028)),
        dict(id='b3', box=(258, 902, 274, 990)),
        dict(id='l3', box=(296, 894, 668, 994)),
    ],
    # Ürün şişesi - kapanış
    4: [
        dict(id='hdr_l', box=(202, 99, 306, 117)),
        dict(id='hdr_t', box=(310, 70, 636, 107)),
        dict(id='hdr_r', box=(636, 91, 744, 117)),
        dict(id='hdr_s', box=(310, 110, 636, 140)),
        dict(id='bright', box=(238, 186, 700, 372), k=45),
        dict(id='correct', box=(208, 328, 736, 466), k=45),
        dict(id='s1', box=(300, 480, 640, 529)),
        dict(id='s2', box=(228, 526, 708, 566)),
        dict(id='p_r', box=(64, 686, 128, 706)),
        dict(id='para', box=(62, 710, 318, 912), k=31),
    ],
}
