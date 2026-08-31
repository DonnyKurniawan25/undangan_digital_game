"""Generator Karakter Pixel Art Stardew Valley Edition untuk Undangan Digital Game.

Menghasilkan sprite sheet berkualitas tinggi dengan proporsi dan detail ala Stardew Valley:
- 4 Arah (Bawah, Kiri, Kanan, Atas)
- 4 Frame Walk Cycle (Idle, Langkah Kiri, Passing, Langkah Kanan) dengan bobbing & arm swing
- Detail realistis: mata ekspresif berglint, pipi blush, sanggul & cunduk mentul, ronce melati,
  blangkon mondholan, sapuk sasak, mahkota lambung emas, beskap/kebaya/songket, sabuk pending, dan keris.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
LEBAR_FRAME = 24
TINGGI_FRAME = 40
SKALA = 2  # Menghasilkan sprite 48x80 pixel per frame

# Outline & Shadow
GARIS = (40, 30, 34, 255)
GARIS_TERANG = (65, 48, 52, 255)

def kanvas(w=LEBAR_FRAME, h=TINGGI_FRAME, latar=(0, 0, 0, 0)):
    img = Image.new("RGBA", (w, h), latar)
    return img, ImageDraw.Draw(img)

def garis_luar(img, warna=GARIS):
    w, h = img.size
    sumber = img.load()
    hasil = img.copy()
    tujuan = hasil.load()
    for y in range(h):
        for x in range(w):
            if sumber[x, y][3] != 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and sumber[nx, ny][3] > 64:
                    tujuan[x, y] = warna
                    break
    return hasil

# ==============================================================================
# PALET WARNA DETAIL (Multi-tone shading)
# ==============================================================================
KULIT = {
    "sorot": (255, 238, 224, 255),
    "dasar": (246, 212, 186, 255),
    "bayang": (222, 174, 142, 255),
    "gelap": (192, 140, 110, 255),
    "blush": (248, 154, 150, 255),
    "bibir": (216, 112, 110, 255),
}

MATA = {
    "putih": (250, 250, 252, 255),
    "pupil": (36, 28, 32, 255),
    "iris_cokelat": (94, 60, 48, 255),
    "kilau": (255, 255, 255, 255),
    "alis": (48, 36, 38, 255),
}

EMAS = {
    "sorot": (255, 244, 180, 255),
    "terang": (244, 214, 104, 255),
    "dasar": (218, 172, 54, 255),
    "gelap": (168, 122, 32, 255),
}

PERAK_PUTIH = {
    "sorot": (255, 255, 255, 255),
    "terang": (244, 244, 248, 255),
    "dasar": (220, 222, 230, 255),
    "gelap": (178, 182, 194, 255),
}

MELATI = {
    "putih": (255, 255, 250, 255),
    "kuning": (255, 230, 110, 255),
    "daun": (78, 142, 70, 255),
}

# ---------------- Tema Jawa ----------------
PALET_PRIA_JAWA = {
    "tipe": "jawa_pria",
    "rambut": (42, 34, 36, 255),
    "blangkon_dasar": (120, 78, 52, 255),
    "blangkon_motif": (64, 40, 28, 255),
    "blangkon_lis": EMAS["terang"],
    "beskap_sorot": (68, 58, 66, 255),
    "beskap_dasar": (38, 32, 38, 255),
    "beskap_gelap": (24, 20, 24, 255),
    "kancing": EMAS["terang"],
    "kancing_rantai": EMAS["dasar"],
    "kerah_putih": (246, 246, 250, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "pending": EMAS["terang"],
    "jarik_dasar": (158, 110, 72, 255),
    "jarik_motif": (88, 54, 34, 255),
    "jarik_sorot": (210, 172, 126, 255),
    "keris_gagang": EMAS["terang"],
    "keris_sarung": (148, 102, 60, 255),
    "selop": (28, 24, 28, 255),
    "selop_emas": EMAS["dasar"],
}

PALET_WANITA_JAWA = {
    "tipe": "jawa_wanita",
    "rambut": (38, 30, 32, 255),
    "rambut_sorot": (68, 54, 56, 255),
    "paes": (32, 26, 28, 255),
    "paes_emas": EMAS["terang"],
    "kebaya_sorot": (252, 250, 252, 255),
    "kebaya_dasar": (232, 232, 240, 255),
    "kebaya_gelap": (176, 176, 196, 255),
    "kebaya_renda": (255, 255, 255, 255),
    "kemben": (180, 54, 72, 255),
    "bros": EMAS["terang"],
    "bros_permata": (216, 40, 60, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "jarik_dasar": (152, 104, 68, 255),
    "jarik_motif": (78, 48, 30, 255),
    "jarik_sorot": (206, 168, 122, 255),
    "cunduk_mentul": EMAS["sorot"],
    "cunduk_batang": EMAS["terang"],
    "selop": (168, 52, 68, 255),
    "selop_emas": EMAS["terang"],
}

# ---------------- Tema Sasak Lombok ----------------
PALET_PRIA_SASAK = {
    "tipe": "sasak_pria",
    "rambut": (40, 32, 34, 255),
    "sapuk_dasar": (34, 30, 36, 255),
    "sapuk_songket": (178, 44, 60, 255),
    "sapuk_emas": EMAS["terang"],
    "baju_sorot": (58, 50, 58, 255),
    "baju_dasar": (32, 28, 34, 255),
    "baju_gelap": (20, 18, 22, 255),
    "rompi_bordir": EMAS["terang"],
    "kerah_putih": (246, 246, 250, 255),
    "dodot_dasar": (168, 38, 54, 255),
    "dodot_motif": EMAS["terang"],
    "dodot_sorot": (210, 70, 86, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "celana_dasar": (36, 32, 38, 255),
    "selop": (28, 24, 28, 255),
    "selop_emas": EMAS["dasar"],
}

PALET_WANITA_SASAK = {
    "tipe": "sasak_wanita",
    "rambut": (38, 30, 32, 255),
    "rambut_sorot": (66, 52, 54, 255),
    "mahkota_sorot": EMAS["sorot"],
    "mahkota_dasar": EMAS["terang"],
    "mahkota_gelap": EMAS["gelap"],
    "mahkota_permata": (224, 40, 58, 255),
    "lambung_sorot": (214, 64, 82, 255),
    "lambung_dasar": (178, 38, 54, 255),
    "lambung_gelap": (132, 24, 38, 255),
    "lambung_bordir": EMAS["terang"],
    "kalung": EMAS["sorot"],
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "songket_dasar": (158, 34, 52, 255),
    "songket_motif": EMAS["terang"],
    "songket_sorot": (208, 68, 88, 255),
    "anting": EMAS["sorot"],
    "selop": (158, 34, 52, 255),
    "selop_emas": EMAS["terang"],
}


# ==============================================================================
# DETAIL PENGGAMBARAN SPRITE (Stardew Valley Quality)
# ==============================================================================

# ==============================================================================
# PENGGAMBARAN SPRITE — proporsi asli Stardew Valley
#
# Stardew menggambar karakter pada kanvas kecil lalu memperbesarnya dengan
# NEAREST. Perbandingan yang membuatnya khas: kepala kira-kira 43% dari tinggi
# badan, mata besar tiga piksel, garis luar tegas, dan bayangan cuma dua
# tingkat. Menggambar halus di resolusi besar tidak akan pernah terlihat sama,
# jadi seluruh karakter di sini digambar pada 24x40 lalu diperbesar 2x.
#
#   y 2..17  kepala (rambut + wajah)
#   y 18..29 badan dan lengan
#   y 30..38 tungkai dan alas kaki
# ==============================================================================
KEPALA_ATAS = 2
WAJAH_ATAS, WAJAH_BAWAH = 5, 17
BADAN_ATAS, BADAN_BAWAH = 18, 29
KAKI_ATAS, KAKI_BAWAH = 30, 38


def gambar_mata_stardew(d, x, y, arah="bawah", alis_tinggi=0):
    """Sepasang piksel mata bergaya sama dengan karakter utama. Dipakai oleh
    properti penari dan pemusik yang digambar terpisah."""
    d.rectangle([x, y, x + 2, y + 2], fill=MATA["putih"])
    d.rectangle([x + 1, y, x + 2, y + 2], fill=MATA["iris_cokelat"])
    d.rectangle([x + 1, y + 1, x + 1, y + 2], fill=MATA["pupil"])
    d.point((x, y), fill=MATA["kilau"])


# ==============================================================================
# PENGGAMBARAN SPRITE — proporsi asli Stardew Valley
#
# Stardew menggambar karakter pada kanvas kecil lalu memperbesarnya dengan
# NEAREST; itu sumber siluet chunky dan garis tegasnya. Yang membuat proporsinya
# khas: kepala kira-kira 44% dari tinggi badan, badan hanya sekitar 55% lebar
# bingkai (bukan selebar bingkai), mata tiga piksel, dan bayangan cuma dua
# tingkat.
#
# Semua digambar pada 24x40 lalu diperbesar 2x menjadi 48x80.
#
#   x 5..18  batas terluar siluet (termasuk lengan)
#   y 2..17  kepala (rambut + wajah)
#   y 18..27 badan dan lengan
#   y 28..37 tungkai dan alas kaki
# ==============================================================================
KEPALA_ATAS = 2
WAJAH_ATAS, WAJAH_BAWAH = 6, 17
BADAN_ATAS, BADAN_BAWAH = 18, 27
KAKI_ATAS, KAKI_BAWAH = 28, 37


def _kosongkan(d, titik):
    for t in titik:
        d.point(t, fill=(0, 0, 0, 0))


def _batas(arah, bagian):
    """Batas kiri-kanan tiap bagian. Dari samping badan sedikit lebih ramping."""
    samping = arah in ("kiri", "kanan")
    if bagian == "kepala":
        return (7, 16) if samping else (6, 17)
    return (8, 15) if samping else (7, 16)


def _warna_atasan(p):
    """Tiga tingkat warna atasan, apa pun jenis busananya."""
    for kunci in ("beskap", "kebaya", "baju", "lambung"):
        if f"{kunci}_dasar" in p:
            return (p.get(f"{kunci}_sorot", p[f"{kunci}_dasar"]),
                    p[f"{kunci}_dasar"],
                    p.get(f"{kunci}_gelap", p[f"{kunci}_dasar"]))
    return ((90, 80, 90, 255), (60, 52, 60, 255), (40, 34, 40, 255))


def _warna_bawahan(p):
    """Warna kain bawah: jarik, dodot, songket, atau celana polos."""
    for kunci in ("jarik", "dodot", "songket"):
        if f"{kunci}_dasar" in p:
            return (p.get(f"{kunci}_sorot", p[f"{kunci}_dasar"]),
                    p[f"{kunci}_dasar"], p.get(f"{kunci}_motif"))
    dasar = p.get("celana_dasar", (48, 42, 48, 255))
    return (dasar, dasar, None)


# ------------------------------------------------------------------ kepala
def _kepala(d, p, arah, is_wanita):
    """Wajah lalu rambut, supaya poni menutup dahi dan bukan sebaliknya."""
    rambut = p["rambut"]
    sorot_rambut = p.get(
        "rambut_sorot", tuple(min(255, c + 30) for c in rambut[:3]) + (255,))
    kiri, kanan = _batas(arah, "kepala")

    # ---- wajah ----
    if arah != "atas":
        d.rectangle([kiri, WAJAH_ATAS, kanan, WAJAH_BAWAH], fill=KULIT["dasar"])
        d.rectangle([kanan, WAJAH_ATAS, kanan, WAJAH_BAWAH], fill=KULIT["bayang"])
        d.rectangle([kiri, WAJAH_BAWAH, kanan, WAJAH_BAWAH], fill=KULIT["bayang"])
        # dagu meruncing
        _kosongkan(d, [(kiri, WAJAH_BAWAH), (kanan, WAJAH_BAWAH)])
        if arah == "kiri":
            d.point((kiri - 1, 12), fill=KULIT["dasar"])          # hidung

    # ---- rambut: kubah bertingkat supaya ubun-ubun membulat ----
    dasar_rambut = 16 if arah == "atas" else 10
    d.rectangle([kiri, 4, kanan, dasar_rambut], fill=rambut)
    d.rectangle([kiri + 1, KEPALA_ATAS, kanan - 1, 4], fill=rambut)
    d.rectangle([kiri + 1, 4, kanan - 3, 6], fill=sorot_rambut)
    d.rectangle([kiri + 2, KEPALA_ATAS, kanan - 3, 4], fill=sorot_rambut)
    _kosongkan(d, [(kiri + 1, KEPALA_ATAS), (kanan - 1, KEPALA_ATAS)])

    if arah == "bawah":
        d.rectangle([kiri, 10, kiri, 14], fill=rambut)            # cambang
        d.rectangle([kanan, 10, kanan, 14], fill=rambut)
        if is_wanita:
            d.rectangle([kiri - 1, 11, kiri, BADAN_ATAS], fill=rambut)
            d.rectangle([kanan, 11, kanan + 1, BADAN_ATAS], fill=rambut)
    elif arah == "kiri":
        d.rectangle([kanan - 2, 4, kanan, 14], fill=rambut)       # belakang kepala
        if is_wanita:
            d.rectangle([kanan, 11, kanan + 1, BADAN_ATAS], fill=rambut)
    else:                                                          # tampak belakang
        d.rectangle([kiri, 4, kanan, 16], fill=sorot_rambut)
        d.rectangle([kiri + 1, KEPALA_ATAS, kanan - 1, 4], fill=sorot_rambut)
        d.line([(kiri, 15), (kanan, 15)], fill=rambut)   # tengkuk
        d.line([(kiri, 16), (kanan, 16)], fill=rambut)
        _kosongkan(d, [(kiri, 16), (kanan, 16),
                       (kiri + 1, KEPALA_ATAS), (kanan - 1, KEPALA_ATAS)])
        if is_wanita:
            d.rectangle([kiri - 1, 11, kanan + 1, BADAN_ATAS], fill=rambut)
        # garis bahu supaya kepala gelap tidak menyatu dengan baju gelap
        d.line([(kiri, BADAN_ATAS - 1), (kanan, BADAN_ATAS - 1)], fill=GARIS)
        return

    # ---- mata: tiga piksel, kilau putih di sudut luar ----
    mata = [(8, 10)] if arah == "kiri" else [(8, 10), (13, 15)]
    for mx0, mx1 in mata:
        d.rectangle([mx0, 11, mx1, 13], fill=MATA["putih"])
        d.rectangle([mx0 + 1, 11, mx1, 13], fill=MATA["iris_cokelat"])
        d.rectangle([mx0 + 1, 12, mx1 - 1, 13], fill=MATA["pupil"])
        d.point((mx0, 11), fill=MATA["kilau"])

    # ---- mulut dan rona pipi ----
    if arah == "kiri":
        d.point((9, 15), fill=KULIT["gelap"])
    else:
        d.rectangle([11, 15, 12, 15], fill=KULIT["gelap"])
        if is_wanita:
            d.point((kiri + 1, 14), fill=KULIT["blush"])
            d.point((kanan - 1, 14), fill=KULIT["blush"])


# --------------------------------------------------------- hiasan kepala
def _hiasan_kepala(d, p, arah):
    """Penutup kepala dibuat rendah dan menempel batok, bukan kotak besar,
    supaya kepala tetap terbaca sebagai kepala."""
    jenis = p["tipe"]
    kiri, kanan = _batas(arah, "kepala")

    if jenis == "jawa_pria":                       # blangkon
        d.rectangle([kiri, 3, kanan, 7], fill=p["blangkon_dasar"])
        d.rectangle([kiri + 1, KEPALA_ATAS, kanan - 1, 3], fill=p["blangkon_dasar"])
        d.rectangle([kiri, 3, kanan - 3, 5], fill=p["blangkon_motif"])
        d.line([(kiri, 7), (kanan, 7)], fill=p["blangkon_lis"])
        _kosongkan(d, [(kiri + 1, KEPALA_ATAS), (kanan - 1, KEPALA_ATAS)])
        if arah != "bawah":                        # mondholan di belakang
            d.rectangle([kanan, 5, kanan + 1, 8], fill=p["blangkon_dasar"])

    elif jenis == "sasak_pria":                    # sapuk
        d.rectangle([kiri, 3, kanan, 7], fill=p["sapuk_dasar"])
        d.rectangle([kiri + 1, KEPALA_ATAS, kanan - 1, 3], fill=p["sapuk_dasar"])
        d.rectangle([kiri, 4, kanan, 5], fill=p["sapuk_songket"])
        d.polygon([(kiri, 4), (kiri, 0), (kiri + 4, 3)], fill=p["sapuk_dasar"])
        d.line([(kiri + 1, 1), (kiri + 1, 3)], fill=p["sapuk_emas"])
        d.line([(kiri, 6), (kanan, 6)], fill=p["sapuk_emas"])
        _kosongkan(d, [(kiri + 1, KEPALA_ATAS), (kanan - 1, KEPALA_ATAS)])

    elif jenis == "jawa_wanita":                   # sanggul + cunduk mentul
        d.rectangle([kiri + 2, 2, kanan - 2, 5], fill=p["rambut"])
        d.rectangle([kiri + 3, 3, kanan - 4, 4], fill=p["rambut_sorot"])
        _kosongkan(d, [(kiri + 2, 2), (kanan - 2, 2)])
        for x in (kiri + 3, kanan - 3):            # cunduk mentul
            d.line([(x, 2), (x, 1)], fill=p["cunduk_batang"])
            d.point((x, 1), fill=p["cunduk_mentul"])
        d.point((11, 9), fill=p["paes_emas"])      # jamang tipis di dahi
        for y in (12, 15):                          # ronce melati di telinga
            d.point((kiri - 1, y), fill=MELATI["putih"])
            d.point((kiri - 1, y + 1), fill=MELATI["kuning"])

    elif jenis == "sasak_wanita":                  # mahkota lambung emas
        d.rectangle([kiri, 4, kanan, 7], fill=p["mahkota_dasar"])
        d.line([(kiri, 7), (kanan, 7)], fill=p["mahkota_gelap"])
        d.polygon([(kiri, 4), (kiri + 2, 1), (kiri + 4, 4)], fill=p["mahkota_sorot"])
        d.polygon([(9, 4), (11, 0), (13, 4)], fill=p["mahkota_sorot"])
        d.polygon([(kanan - 4, 4), (kanan - 2, 1), (kanan, 4)], fill=p["mahkota_sorot"])
        d.point((11, 2), fill=p["mahkota_permata"])
        d.point((kiri + 2, 5), fill=p["mahkota_permata"])
        d.point((kanan - 2, 5), fill=p["mahkota_permata"])
        d.point((kiri - 1, 13), fill=p["anting"])
        d.point((kanan + 1, 13), fill=p["anting"])


# ------------------------------------------------------------------ badan
def _badan(d, p, arah, ayun, is_wanita):
    sorot, dasar, gelap = _warna_atasan(p)
    kiri, kanan = _batas(arah, "badan")
    bawah_atasan = BADAN_BAWAH - (2 if is_wanita else 0)

    d.rectangle([kiri, BADAN_ATAS, kanan, bawah_atasan], fill=dasar)
    d.rectangle([kiri, BADAN_ATAS, kiri, bawah_atasan], fill=sorot)
    d.rectangle([kanan - 1, BADAN_ATAS, kanan, bawah_atasan], fill=gelap)
    d.line([(kiri, BADAN_ATAS), (kanan, BADAN_ATAS)], fill=GARIS)

    if arah == "bawah":
        if is_wanita:
            d.line([(10, BADAN_ATAS), (11, BADAN_ATAS + 3)], fill=gelap)
            d.line([(13, BADAN_ATAS), (12, BADAN_ATAS + 3)], fill=gelap)
            d.point((11, BADAN_ATAS + 4), fill=p.get("bros", EMAS["terang"]))
        else:
            if "kerah_putih" in p:
                d.polygon([(9, BADAN_ATAS), (11, BADAN_ATAS + 3), (14, BADAN_ATAS)],
                          fill=p["kerah_putih"])
            for y in range(BADAN_ATAS + 4, bawah_atasan - 1, 3):
                d.point((11, y), fill=p.get("kancing", EMAS["terang"]))
            if "rompi_bordir" in p:
                d.line([(kiri + 1, BADAN_ATAS + 1), (kiri + 1, bawah_atasan - 1)],
                       fill=p["rompi_bordir"])
                d.line([(kanan - 1, BADAN_ATAS + 1), (kanan - 1, bawah_atasan - 1)],
                       fill=p["rompi_bordir"])

    # sabuk tipis di pinggang, sekadar aksen
    if "sabuk_dasar" in p:
        d.line([(kiri, bawah_atasan), (kanan, bawah_atasan)], fill=p["sabuk_dasar"])
        if arah == "bawah":
            d.point((11, bawah_atasan), fill=p.get("pending", EMAS["sorot"]))

    # ---- lengan ----
    # Dari samping hanya lengan terdekat yang tampak, dan diletakkan di TEPI
    # depan badan; kalau di tengah, telapaknya terbaca sebagai noda di dada.
    if arah == "kiri":
        pasangan = [(kiri - 2, -1)]
    else:
        pasangan = [(kiri - 2, -1), (kanan + 1, 1)]
    for x0, sisi in pasangan:
        dorong = -ayun * sisi
        geser = 1 if dorong > 0 else (-1 if dorong < 0 else 0)
        atas = BADAN_ATAS + 1 + geser
        ujung = BADAN_ATAS + 6 + geser
        d.rectangle([x0, atas, x0 + 1, ujung], fill=dasar)
        d.rectangle([x0 + (1 if sisi > 0 else 0), atas,
                     x0 + (1 if sisi > 0 else 0), ujung], fill=gelap)
        # telapak menumpuk ujung lengan, bukan bola terpisah
        d.rectangle([x0, ujung, x0 + 1, ujung + 2], fill=KULIT["dasar"])
        d.point((x0 + 1, ujung + 2), fill=KULIT["bayang"])
        # garis pemisah supaya lengan gelap tidak melebur ke badan gelap
        batas_x = x0 + 2 if sisi < 0 else x0 - 1
        d.line([(batas_x, atas), (batas_x, ujung + 1)], fill=GARIS)

    # keris terselip di pinggang mempelai pria Jawa
    if p["tipe"] == "jawa_pria" and arah != "atas":
        d.line([(kanan, bawah_atasan - 1), (kanan + 2, bawah_atasan - 5)],
               fill=p["keris_sarung"])
        d.point((kanan + 2, bawah_atasan - 6), fill=p["keris_gagang"])


# ---------------------------------------------------------------- bawahan
def _bawahan(d, p, arah, ayun, is_wanita):
    """Tungkai. Kedua telapak selalu menapak garis tanah; yang berubah hanya
    renggang langkah dan panjang alas kaki, supaya tidak terlihat melayang."""
    sorot_kain, dasar_kain, motif = _warna_bawahan(p)
    kiri, kanan = _batas(arah, "badan")

    if is_wanita:
        # kain panjang sedikit melebar ke bawah
        d.polygon([(kiri, KAKI_ATAS - 3), (kanan, KAKI_ATAS - 3),
                   (kanan + 1, KAKI_BAWAH - 1), (kiri - 1, KAKI_BAWAH - 1)],
                  fill=dasar_kain)
        d.polygon([(12, KAKI_ATAS - 3), (kanan, KAKI_ATAS - 3),
                   (kanan + 1, KAKI_BAWAH - 1), (13, KAKI_BAWAH - 1)],
                  fill=sorot_kain)
        if motif:
            for y in (KAKI_ATAS + 2, KAKI_BAWAH - 4):
                d.line([(kiri, y), (kanan, y)], fill=motif)
                for x in range(kiri + 1, kanan, 3):
                    d.point((x, y + 1), fill=motif)
        # ujung selop mengintip di bawah kain
        for x0, maju in ((8, ayun > 0), (13, ayun < 0)):
            x = x0 + (-1 if (maju and x0 == 8) else (1 if maju else 0))
            d.rectangle([x, KAKI_BAWAH - 1, x + 2, KAKI_BAWAH], fill=p["selop"])
            d.point((x + 1, KAKI_BAWAH - 1), fill=p["selop_emas"])
        return

    # ---- tungkai pria ----
    celana = p.get("celana_dasar", (42, 36, 42, 255))
    for x0, maju in ((8, ayun > 0), (13, ayun < 0)):
        x = x0 + (-1 if (maju and x0 == 8) else (1 if maju else 0))
        d.rectangle([x, KAKI_ATAS, x + 2, KAKI_BAWAH - 2], fill=celana)
        d.rectangle([x + 2, KAKI_ATAS, x + 2, KAKI_BAWAH - 2],
                    fill=p.get("beskap_gelap", (24, 20, 24, 255)))
        # alas kaki: telapak depan sedikit lebih panjang, keduanya tetap menapak
        panjang = 1 if maju else 0
        d.rectangle([x - panjang, KAKI_BAWAH - 2, x + 2, KAKI_BAWAH], fill=p["selop"])
        d.point((x + 1, KAKI_BAWAH - 2), fill=p["selop_emas"])

    # lilitan jarik tipis di pinggul, sekadar penanda busana adat
    if motif and arah != "atas":
        d.rectangle([kiri, KAKI_ATAS, kanan, KAKI_ATAS + 1], fill=dasar_kain)
        d.line([(kiri, KAKI_ATAS + 1), (kanan, KAKI_ATAS + 1)], fill=motif)
        for x in range(kiri, kanan + 1, 2):
            d.point((x, KAKI_ATAS), fill=sorot_kain)


def render_karakter_frame(tipe_palet, arah, frame_idx):
    """Satu bingkai. Badan sengaja tidak ikut naik-turun tiap frame; hanya
    tungkai dan lengan yang bergerak, supaya siluetnya tidak terlihat
    berbayang saat berjalan."""
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    p = tipe_palet
    is_wanita = "wanita" in p["tipe"]
    ayun = [0, 1, 0, -1][frame_idx]

    _bawahan(d, p, arah, ayun, is_wanita)
    _badan(d, p, arah, ayun, is_wanita)
    _kepala(d, p, arah, is_wanita)
    _hiasan_kepala(d, p, arah)
    return garis_luar(img, GARIS)


def buat_sprite_sheet(palet, nama_file, direktori_tujuan):
    """Membuat sprite sheet 4 arah x 4 frame (192 x 320 px jika skala=2)."""
    ARAH = ["bawah", "kiri", "kanan", "atas"]
    lembar = Image.new("RGBA", (LEBAR_FRAME * 4, TINGGI_FRAME * 4), (0, 0, 0, 0))

    for baris, arah in enumerate(ARAH):
        for kolom in range(4):
            if arah == "kanan":
                frame_img = render_karakter_frame(palet, "kiri", kolom)
                frame_img = frame_img.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                frame_img = render_karakter_frame(palet, arah, kolom)

            lembar.paste(frame_img, (kolom * LEBAR_FRAME, baris * TINGGI_FRAME))

    hasil = lembar.resize((lembar.width * SKALA, lembar.height * SKALA), Image.NEAREST)
    direktori_tujuan.mkdir(parents=True, exist_ok=True)
    hasil.save(direktori_tujuan / nama_file)
    print(f"  -> Tersimpan {direktori_tujuan / nama_file} ({hasil.size[0]}x{hasil.size[1]} px)")


def prop_pengantin_duduk(palet):
    """Mempelai duduk megah di kursi pelaminan dengan pose anggun."""
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    # Render frame bawah (idle duduk)
    frame_duduk = render_karakter_frame(palet, "bawah", 0)
    img.paste(frame_duduk, (0, 0))
    hasil = img.resize((img.width * SKALA, img.height * SKALA), Image.NEAREST)
    return hasil


def prop_penari_sasak():
    """Penari Gandrung Sasak dinamis dengan selendang emas."""
    img, d = kanvas(LEBAR_FRAME + 4, TINGGI_FRAME)
    p = PALET_WANITA_SASAK
    cx = 14
    # Badan meliuk menari
    d.rectangle([cx - 4, 18, cx + 4, 25], fill=p["lambung_dasar"])
    d.line([(cx - 4, 18), (cx - 4, 25)], fill=p["lambung_sorot"])
    # Selendang emas melingkar di bahu dan melambai ke samping
    d.polygon([(cx - 10, 16), (cx - 4, 20), (cx - 8, 28), (cx - 12, 22)], fill=EMAS["terang"])
    d.polygon([(cx + 4, 20), (cx + 11, 16), (cx + 13, 22), (cx + 8, 28)], fill=EMAS["terang"])
    # Kain songket melingkar
    d.polygon([(cx - 5, 25), (cx + 5, 25), (cx + 6, 36), (cx - 6, 36)], fill=p["songket_dasar"])
    for y in (27, 30, 33):
        d.line([(cx - 5, y), (cx + 5, y)], fill=p["songket_motif"])
    # Lengan menari lentik
    d.line([(cx - 4, 20), (cx - 11, 15)], fill=KULIT["dasar"], width=2)
    d.line([(cx + 4, 20), (cx + 11, 15)], fill=KULIT["dasar"], width=2)
    d.point((cx - 12, 14), fill=KULIT["sorot"])
    d.point((cx + 12, 14), fill=KULIT["sorot"])
    # Kepala & Mahkota Emas
    d.rectangle([cx - 4, 7, cx + 4, 16], fill=KULIT["dasar"])
    gambar_mata_stardew(d, cx - 3, 11, arah="bawah")
    gambar_mata_stardew(d, cx + 1, 11, arah="bawah")
    d.point((cx, 13), fill=KULIT["bayang"])
    d.line([(cx - 1, 15), (cx + 1, 15)], fill=KULIT["bibir"])
    # Mahkota Tajuk Emas Gandrung
    d.polygon([(cx - 5, 7), (cx, 1), (cx + 5, 7)], fill=EMAS["sorot"])
    d.rectangle([cx - 5, 7, cx + 5, 9], fill=EMAS["terang"])
    d.point((cx, 4), fill=p["mahkota_permata"])
    # Kamboja putih di samping
    d.point((cx - 5, 9), fill=(255, 255, 240, 255))
    d.point((cx + 5, 9), fill=(255, 255, 240, 255))
    hasil = garis_luar(img, GARIS)
    return hasil.resize((hasil.width * SKALA, hasil.height * SKALA), Image.NEAREST)


def prop_pemusik_gendang():
    """Penabuh Gendang Beleq Sasak berdiri dengan instrumen drum megah."""
    img, d = kanvas(32, TINGGI_FRAME)
    p = PALET_PRIA_SASAK
    cx = 10
    # Gendang Beleq besar di samping kanan
    d.ellipse([14, 14, 30, 36], fill=(154, 84, 46, 255))
    d.ellipse([26, 15, 30, 35], fill=(244, 226, 192, 255))  # Kulit drum
    d.line([(14, 25), (26, 25)], fill=EMAS["terang"], width=2)
    d.line([(16, 18), (28, 18)], fill=p["dodot_dasar"], width=2)
    d.line([(16, 32), (28, 32)], fill=p["dodot_dasar"], width=2)
    # Tubuh Pemusik
    d.rectangle([cx - 5, 18, cx + 4, 27], fill=p["baju_dasar"])
    d.rectangle([cx - 4, 27, cx + 3, 36], fill=p["celana_dasar"])
    d.rectangle([cx - 4, 36, cx - 1, 38], fill=p["selop"])
    d.rectangle([cx + 1, 36, cx + 4, 38], fill=p["selop"])
    # Lengan memukul gendang
    d.line([(cx + 3, 20), (18, 23)], fill=KULIT["dasar"], width=2)
    d.point((19, 23), fill=EMAS["terang"])  # Stik pemukul
    # Kepala & Sapuk
    d.rectangle([cx - 4, 7, cx + 4, 16], fill=KULIT["dasar"])
    gambar_mata_stardew(d, cx - 3, 11, arah="bawah")
    gambar_mata_stardew(d, cx + 1, 11, arah="bawah")
    d.point((cx, 13), fill=KULIT["bayang"])
    d.line([(cx - 1, 15), (cx + 1, 15)], fill=KULIT["bibir"])
    # Sapuk ikat kepala
    d.rectangle([cx - 5, 6, cx + 5, 9], fill=p["sapuk_dasar"])
    d.line([(cx - 4, 8), (cx + 4, 8)], fill=p["sapuk_emas"])
    d.polygon([(cx + 2, 6), (cx + 6, 2), (cx + 4, 7)], fill=p["sapuk_dasar"])
    hasil = garis_luar(img, GARIS)
    return hasil.resize((hasil.width * SKALA, hasil.height * SKALA), Image.NEAREST)


def main():
    print("=== Membuat Sprite Karakter Stardew Valley Edition ===")
    
    # 1. Tema Jawa
    dir_jawa = AKAR / "static" / "game"
    print("\n[1] Tema Jawa (Taman Keraton):")
    buat_sprite_sheet(PALET_PRIA_JAWA, "karakter_pria.png", dir_jawa)
    buat_sprite_sheet(PALET_WANITA_JAWA, "karakter_wanita.png", dir_jawa)
    prop_pengantin_duduk(PALET_PRIA_JAWA).save(dir_jawa / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_WANITA_JAWA).save(dir_jawa / "pengantin_wanita.png")
    print("  -> Tersimpan pengantin_pria.png & pengantin_wanita.png (Jawa)")

    # 2. Tema Lombok
    dir_lombok = AKAR / "static" / "game_lombok"
    print("\n[2] Tema Lombok (Pantai Sasak):")
    buat_sprite_sheet(PALET_PRIA_SASAK, "karakter_pria.png", dir_lombok)
    buat_sprite_sheet(PALET_WANITA_SASAK, "karakter_wanita.png", dir_lombok)
    prop_pengantin_duduk(PALET_PRIA_SASAK).save(dir_lombok / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_WANITA_SASAK).save(dir_lombok / "pengantin_wanita.png")
    prop_penari_sasak().save(dir_lombok / "penari_sasak.png")
    prop_pemusik_gendang().save(dir_lombok / "pemusik_gendang.png")
    print("  -> Tersimpan pengantin duduk, penari_sasak.png & pemusik_gendang.png (Lombok)")

    # 3. Tema Tropis
    dir_tropis = AKAR / "static" / "game_tropis"
    print("\n[3] Tema Tropis:")
    buat_sprite_sheet(PALET_PRIA_JAWA, "karakter_pria.png", dir_tropis)
    buat_sprite_sheet(PALET_WANITA_JAWA, "karakter_wanita.png", dir_tropis)
    prop_pengantin_duduk(PALET_PRIA_JAWA).save(dir_tropis / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_WANITA_JAWA).save(dir_tropis / "pengantin_wanita.png")
    print("  -> Tersimpan pengantin_pria.png & pengantin_wanita.png (Tropis)")

    print("\n=== Selesai Membuat Seluruh Karakter Stardew Valley! ===")


if __name__ == "__main__":
    main()

