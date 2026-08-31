"""Membuat seluruh aset pixel art undangan dari kode.

Semua gambar digambar pada resolusi kecil lalu diperbesar dengan metode
nearest-neighbour supaya pikselnya tetap tajam. Jalankan ulang kapan saja:

    python tools/buat_aset.py

Keluaran di static/game/:
  tileset.png   deretan tile lantai (urutannya harus sama dengan INDEKS_TILE
                di static/js/game.js)
  tepi.png      lapisan tepi rumput supaya batas lantai tidak berupa kotak kaku
  karakter_*.png  lembar sprite 4 arah x 4 frame
  <properti>.png  masing-masing satu berkas
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game"
SKALA = 2
UKURAN_TILE = 16

GARIS = (54, 42, 52, 255)

RUMPUT_DASAR = (110, 164, 97, 255)
RUMPUT_GELAP = (97, 149, 86, 255)
RUMPUT_TERANG = (126, 179, 112, 255)


# --------------------------------------------------------------------------
# Peralatan dasar
# --------------------------------------------------------------------------
def kanvas(lebar, tinggi, latar=(0, 0, 0, 0)):
    img = Image.new("RGBA", (lebar, tinggi), latar)
    return img, ImageDraw.Draw(img)


def perbesar(img, skala=SKALA):
    return img.resize((img.width * skala, img.height * skala), Image.NEAREST)


def garis_luar(img, warna=GARIS):
    """Menambahkan outline 1 piksel di sekeliling siluet."""
    lebar, tinggi = img.size
    sumber = img.load()
    hasil = img.copy()
    tujuan = hasil.load()
    for y in range(tinggi):
        for x in range(lebar):
            if sumber[x, y][3] != 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < lebar and 0 <= ny < tinggi and sumber[nx, ny][3] > 128:
                    tujuan[x, y] = warna
                    break
    return hasil


def bintik(d, acak, jumlah, warna, lebar=UKURAN_TILE, tinggi=UKURAN_TILE):
    for _ in range(jumlah):
        d.point((acak.randrange(lebar), acak.randrange(tinggi)), fill=warna)


# --------------------------------------------------------------------------
# Tile lantai
# --------------------------------------------------------------------------
def tile_rumput(seed=1, berbunga=False):
    img, d = kanvas(16, 16, RUMPUT_DASAR)
    r = random.Random(seed)
    bintik(d, r, 26, RUMPUT_GELAP)
    bintik(d, r, 16, RUMPUT_TERANG)
    for _ in range(7):
        x, y = r.randrange(1, 15), r.randrange(3, 15)
        d.line([(x, y), (x, y - 2)], fill=(91, 141, 81, 255))
    if berbunga:
        for warna, inti in (
            ((248, 242, 178, 255), (250, 206, 110, 255)),
            ((243, 176, 196, 255), (232, 128, 158, 255)),
            ((252, 250, 246, 255), (250, 214, 128, 255)),
        ):
            x, y = r.randrange(2, 12), r.randrange(2, 12)
            d.rectangle([x, y, x + 1, y + 1], fill=warna)
            d.point((x, y + 1), fill=inti)
    return img


def tile_jalan(seed=2):
    img, d = kanvas(16, 16, (219, 207, 185, 255))
    r = random.Random(seed)
    nat = (189, 174, 149, 255)
    d.line([(0, 7), (15, 7)], fill=nat)
    d.line([(7, 0), (7, 6)], fill=nat)
    d.line([(3, 8), (3, 15)], fill=nat)
    d.line([(11, 8), (11, 15)], fill=nat)
    bintik(d, r, 18, (231, 222, 204, 255))
    bintik(d, r, 12, (204, 191, 168, 255))
    return img


def tile_karpet(seed=3, tepi=None):
    img, d = kanvas(16, 16, (168, 62, 74, 255))
    r = random.Random(seed)
    bintik(d, r, 20, (156, 54, 66, 255))
    bintik(d, r, 12, (186, 78, 90, 255))
    if tepi == "kiri":
        d.rectangle([0, 0, 1, 15], fill=(216, 176, 104, 255))
        d.line([(2, 0), (2, 15)], fill=(190, 148, 84, 255))
    if tepi == "kanan":
        d.rectangle([14, 0, 15, 15], fill=(216, 176, 104, 255))
        d.line([(13, 0), (13, 15)], fill=(190, 148, 84, 255))
    return img


def tile_kayu(seed=4):
    img, d = kanvas(16, 16, (172, 130, 88, 255))
    r = random.Random(seed)
    for y in (0, 5, 10, 15):
        d.line([(0, y), (15, y)], fill=(140, 102, 66, 255))
    d.line([(6, 1), (6, 4)], fill=(140, 102, 66, 255))
    d.line([(11, 6), (11, 9)], fill=(140, 102, 66, 255))
    d.line([(3, 11), (3, 14)], fill=(140, 102, 66, 255))
    bintik(d, r, 10, (186, 146, 104, 255))
    return img


def tile_marmer(seed=5):
    """Marmer krem dengan nat halus; urat sengaja samar agar tidak berpola."""
    img, d = kanvas(16, 16, (243, 239, 232, 255))
    r = random.Random(seed)
    nat = (226, 220, 210, 255)
    d.line([(0, 0), (15, 0)], fill=nat)
    d.line([(0, 0), (0, 15)], fill=nat)
    for _ in range(3):
        x, y = r.randrange(3, 12), r.randrange(3, 12)
        d.point((x, y), fill=(234, 229, 220, 255))
        d.point((x + 1, y + 1), fill=(234, 229, 220, 255))
    return img


def tile_air(seed=6, fase=0):
    """Air dengan tiga fase riak untuk animasi."""
    img, d = kanvas(16, 16, (104, 162, 196, 255))
    r = random.Random(seed)
    bintik(d, r, 16, (92, 148, 184, 255))
    geser = fase * 5
    for i, y in enumerate((3, 8, 12)):
        x = (r.randrange(0, 10) + geser + i * 3) % 16
        d.line([(x, y), (min(15, x + 4), y)], fill=(150, 198, 222, 255))
        if x + 4 > 15:
            d.line([(0, y), (x + 4 - 16, y)], fill=(150, 198, 222, 255))
    kilau = (186, 220, 236, 255)
    d.point(((2 + geser) % 16, 5), fill=kilau)
    d.point(((9 + geser) % 16, 10), fill=kilau)
    return img


def tile_pagar_tanaman(seed=7):
    img, d = kanvas(16, 16, (58, 106, 66, 255))
    r = random.Random(seed)
    for _ in range(9):
        x, y = r.randrange(0, 14), r.randrange(0, 14)
        d.ellipse([x, y, x + 3, y + 2], fill=(76, 130, 80, 255))
    bintik(d, r, 20, (46, 88, 56, 255))
    bintik(d, r, 10, (92, 150, 94, 255))
    return img


def tile_tanah(seed=8):
    img, d = kanvas(16, 16, (190, 160, 124, 255))
    r = random.Random(seed)
    bintik(d, r, 24, (172, 142, 108, 255))
    bintik(d, r, 14, (206, 178, 142, 255))
    return img


def tile_taman_bunga(seed=9):
    """Bedeng bunga: tanah gelap penuh kuntum. Tidak bisa dilewati."""
    img, d = kanvas(16, 16, (122, 92, 70, 255))
    r = random.Random(seed)
    bintik(d, r, 22, (104, 78, 58, 255))
    warna = [
        (243, 176, 196, 255),
        (252, 250, 246, 255),
        (248, 226, 170, 255),
        (226, 158, 182, 255),
        (198, 154, 214, 255),
    ]
    for _ in range(9):
        x, y = r.randrange(1, 14), r.randrange(1, 14)
        d.line([(x, y + 2), (x, y + 3)], fill=(84, 128, 78, 255))
        w = r.choice(warna)
        d.rectangle([x - 1, y, x + 1, y + 1], fill=w)
        d.point((x, y), fill=(250, 214, 128, 255))
    return img


# Urutan ini WAJIB sama dengan INDEKS_TILE di static/js/game.js
URUTAN_TILE = [
    ("rumput", lambda: tile_rumput(11)),
    ("rumput2", lambda: tile_rumput(23)),
    ("rumput3", lambda: tile_rumput(37)),
    ("rumput_bunga", lambda: tile_rumput(12, berbunga=True)),
    ("jalan", tile_jalan),
    ("karpet", lambda: tile_karpet(31)),
    ("karpet_kiri", lambda: tile_karpet(32, tepi="kiri")),
    ("karpet_kanan", lambda: tile_karpet(33, tepi="kanan")),
    ("kayu", tile_kayu),
    ("marmer", tile_marmer),
    ("air1", lambda: tile_air(61, 0)),
    ("air2", lambda: tile_air(61, 1)),
    ("air3", lambda: tile_air(61, 2)),
    ("pagar_tanaman", tile_pagar_tanaman),
    ("tanah", tile_tanah),
    ("taman_bunga", tile_taman_bunga),
]


def buat_tileset():
    tiles = [fungsi() for _, fungsi in URUTAN_TILE]
    lembar, _ = kanvas(16 * len(tiles), 16)
    for i, t in enumerate(tiles):
        lembar.paste(t, (i * 16, 0))
    perbesar(lembar).save(KELUARAN / "tileset.png")
    return [nama for nama, _ in URUTAN_TILE]


# --------------------------------------------------------------------------
# Tepi rumput
#
# Digambar DI ATAS tile lantai pada sisi yang bersebelahan dengan rumput,
# sehingga rumput terlihat menjorok ke lantai dan batasnya tidak lurus kaku.
# --------------------------------------------------------------------------
def tepi_sisi(sisi, seed):
    rumput = tile_rumput(seed)
    masker = Image.new("L", (16, 16), 0)
    dm = ImageDraw.Draw(masker)
    r = random.Random(seed + 900)
    for i in range(16):
        tebal = 3 + r.choice([0, 0, 1, 1, 2])
        if sisi == "atas":
            dm.line([(i, 0), (i, tebal)], fill=255)
        elif sisi == "bawah":
            dm.line([(i, 15 - tebal), (i, 15)], fill=255)
        elif sisi == "kiri":
            dm.line([(0, i), (tebal, i)], fill=255)
        else:
            dm.line([(15 - tebal, i), (15, i)], fill=255)
    hasil = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    hasil.paste(rumput, (0, 0), masker)
    return hasil


def tepi_sudut(sudut, seed):
    """Gundukan kecil untuk pojok dalam (hanya diagonalnya yang rumput)."""
    rumput = tile_rumput(seed)
    masker = Image.new("L", (16, 16), 0)
    dm = ImageDraw.Draw(masker)
    jari = 5
    pusat = {
        "kiri_atas": (0, 0),
        "kanan_atas": (15, 0),
        "kiri_bawah": (0, 15),
        "kanan_bawah": (15, 15),
    }[sudut]
    dm.ellipse(
        [pusat[0] - jari, pusat[1] - jari, pusat[0] + jari, pusat[1] + jari], fill=255
    )
    hasil = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    hasil.paste(rumput, (0, 0), masker)
    return hasil


# Urutan WAJIB sama dengan TEPI di static/js/game.js
URUTAN_TEPI = [
    ("atas", lambda: tepi_sisi("atas", 101)),
    ("bawah", lambda: tepi_sisi("bawah", 102)),
    ("kiri", lambda: tepi_sisi("kiri", 103)),
    ("kanan", lambda: tepi_sisi("kanan", 104)),
    ("kiri_atas", lambda: tepi_sudut("kiri_atas", 105)),
    ("kanan_atas", lambda: tepi_sudut("kanan_atas", 106)),
    ("kiri_bawah", lambda: tepi_sudut("kiri_bawah", 107)),
    ("kanan_bawah", lambda: tepi_sudut("kanan_bawah", 108)),
]


def buat_tepi():
    potongan = [fungsi() for _, fungsi in URUTAN_TEPI]
    lembar, _ = kanvas(16 * len(potongan), 16)
    for i, t in enumerate(potongan):
        lembar.paste(t, (i * 16, 0))
    perbesar(lembar).save(KELUARAN / "tepi.png")
    return [nama for nama, _ in URUTAN_TEPI]


# --------------------------------------------------------------------------
# Karakter
# --------------------------------------------------------------------------
# Tamu pun berbusana Indonesia: pria berkemeja batik, wanita berkebaya
# dengan kain batik.
PALET_PRIA = {
    "kulit": (240, 200, 164, 255),
    "kulit_gelap": (212, 168, 132, 255),
    "rambut": (58, 44, 44, 255),
    "rambut_terang": (86, 66, 62, 255),
    "baju": (122, 82, 56, 255),
    "baju_gelap": (98, 64, 44, 255),
    "motif": (204, 174, 132, 255),
    "bawahan": (52, 48, 56, 255),
    "sepatu": (40, 36, 40, 255),
    "aksen": (206, 168, 96, 255),
}

PALET_WANITA = {
    "kulit": (246, 210, 176, 255),
    "kulit_gelap": (218, 178, 144, 255),
    "rambut": (58, 40, 36, 255),
    "rambut_terang": (92, 66, 54, 255),
    "baju": (250, 244, 234, 255),
    "baju_gelap": (228, 220, 208, 255),
    "motif": (212, 172, 98, 255),
    "bawahan": (152, 106, 66, 255),
    "sepatu": (110, 76, 52, 255),
    "aksen": (206, 168, 96, 255),
}

ARAH = ["bawah", "kiri", "kanan", "atas"]


def karakter_frame(arah, frame, p, rok=False):
    img, d = kanvas(18, 28)
    ayun = [0, 1, 0, -1][frame]

    # --- kaki ---
    y_kaki = 21 if rok else 19
    for x0, sisi in ((5, ayun), (10, -ayun)):
        atas = y_kaki + (1 if sisi > 0 else 0)
        bawah = 24 - (1 if sisi > 0 else 0)
        d.rectangle([x0, atas, x0 + 2, bawah], fill=p["kulit"] if rok else p["bawahan"])
        d.rectangle([x0, bawah - 1, x0 + 2, bawah], fill=p["sepatu"])

    # --- badan ---
    if rok:
        # kain batik melebar, lalu kebaya menutupi bagian atas
        d.polygon([(5, 14), (12, 14), (14, 21), (3, 21)], fill=p["bawahan"])
        for y in (16, 18, 20):
            for x in range(4, 13, 3):
                d.point((x, y), fill=p["motif"])
        d.rectangle([5, 12, 12, 17], fill=p["baju"])
        d.line([(5, 17), (12, 17)], fill=p["baju_gelap"])
    else:
        # kemeja batik
        d.rectangle([5, 12, 12, 18], fill=p["baju"])
        d.line([(5, 18), (12, 18)], fill=p["baju_gelap"])
        for y in (14, 17):
            for x in range(6, 12, 2):
                d.point((x, y), fill=p["motif"])

    if arah != "atas":
        if rok:
            d.rectangle([7, 12, 10, 13], fill=p["baju_gelap"])
            d.point((8, 14), fill=p["aksen"])
            d.point((9, 14), fill=p["aksen"])
        else:
            d.rectangle([8, 12, 9, 13], fill=p["baju_gelap"])

    # --- lengan ---
    for x0, sisi in ((3, -ayun), (13, ayun)):
        atas = 13 + (1 if sisi > 0 else 0)
        d.rectangle([x0, atas, x0 + 1, atas + 4], fill=p["baju"])
        d.rectangle([x0, atas + 5, x0 + 1, atas + 5], fill=p["kulit"])

    # --- kepala ---
    d.rectangle([5, 4, 12, 11], fill=p["kulit"])
    d.line([(5, 11), (12, 11)], fill=p["kulit_gelap"])

    # --- rambut ---
    rambut, kilau = p["rambut"], p["rambut_terang"]
    if arah == "atas":
        d.rectangle([5, 3, 12, 10], fill=rambut)
        d.line([(6, 3), (11, 3)], fill=kilau)
    else:
        d.rectangle([5, 3, 12, 6], fill=rambut)
        d.line([(6, 3), (10, 3)], fill=kilau)
        if arah == "bawah":
            d.rectangle([5, 7, 5, 9], fill=rambut)
            d.rectangle([12, 7, 12, 9], fill=rambut)
            d.line([(7, 7), (9, 7)], fill=rambut)
        elif arah == "kiri":
            d.rectangle([11, 7, 12, 10], fill=rambut)
        else:
            d.rectangle([5, 7, 6, 10], fill=rambut)

    if rok:  # rambut disanggul + hiasan melati
        d.ellipse([7, 1, 11, 5], fill=rambut)
        d.point((8, 2), fill=kilau)
        d.rectangle([4, 6, 4, 11], fill=rambut)
        d.rectangle([13, 6, 13, 11], fill=rambut)
        d.point((6, 2), fill=(250, 248, 242, 255))
        d.point((12, 3), fill=(250, 248, 242, 255))

    # --- wajah ---
    mata = (52, 40, 46, 255)
    if arah == "bawah":
        d.point((7, 8), fill=mata)
        d.point((10, 8), fill=mata)
        d.line([(8, 10), (9, 10)], fill=(198, 138, 126, 255))
    elif arah == "kiri":
        d.point((6, 8), fill=mata)
        d.point((8, 8), fill=mata)
    elif arah == "kanan":
        d.point((9, 8), fill=mata)
        d.point((11, 8), fill=mata)

    return garis_luar(img)


def buat_karakter(nama, palet, rok):
    lembar, _ = kanvas(18 * 4, 28 * 4)
    for baris, arah in enumerate(ARAH):
        for kolom in range(4):
            lembar.paste(karakter_frame(arah, kolom, palet, rok), (kolom * 18, baris * 28))
    perbesar(lembar).save(KELUARAN / f"{nama}.png")


# --------------------------------------------------------------------------
# Properti / dekorasi — bernuansa pernikahan adat Indonesia
# --------------------------------------------------------------------------
JATI_TUA = (88, 56, 38, 255)
JATI = (122, 82, 54, 255)
JATI_TERANG = (150, 108, 74, 255)
UKIR = (206, 166, 92, 255)          # emas ukiran
UKIR_TERANG = (238, 206, 138, 255)
KAIN_GADING = (246, 238, 220, 255)
KAIN_BAYANG = (226, 214, 190, 255)
MERAH = (154, 48, 60, 255)
MERAH_TUA = (122, 36, 48, 255)
DAUN = (68, 122, 74, 255)
DAUN_TERANG = (88, 148, 88, 255)
JANUR = (214, 210, 104, 255)        # janur kuning
JANUR_TERANG = (240, 238, 156, 255)
JANUR_GELAP = (172, 172, 74, 255)
BAMBU = (176, 156, 96, 255)
BAMBU_GELAP = (142, 124, 74, 255)
MELATI = (250, 250, 244, 255)
BUNGA = [
    (250, 246, 240, 255),
    (243, 176, 196, 255),
    (248, 226, 170, 255),
    (226, 158, 182, 255),
]


def _ukiran_sulur(d, x0, y0, x1, y1, warna=UKIR):
    """Motif ukiran sulur sederhana di dalam sebuah panel."""
    for y in range(y0, y1 - 2, 7):
        d.rectangle([x0, y, x1, y + 1], fill=warna)
        tengah = (x0 + x1) // 2
        d.rectangle([tengah - 1, y + 2, tengah + 1, y + 4], fill=warna)
        d.point((x0 + 1, y + 3), fill=warna)
        d.point((x1 - 1, y + 3), fill=warna)


def prop_pelaminan():
    """Gebyok Jawa berukir dengan ceruk melengkung dan hiasan janur."""
    img, d = kanvas(72, 54)

    # panggung
    d.rectangle([0, 46, 71, 53], fill=MERAH)
    d.rectangle([0, 46, 71, 47], fill=UKIR)
    d.rectangle([0, 52, 71, 53], fill=MERAH_TUA)

    # badan gebyok
    d.rectangle([2, 9, 69, 47], fill=JATI_TUA)

    # panel samping berukir
    for x0 in (4, 53):
        d.rectangle([x0, 12, x0 + 14, 45], fill=JATI)
        d.rectangle([x0 + 1, 13, x0 + 13, 44], fill=JATI_TERANG)
        _ukiran_sulur(d, x0 + 2, 15, x0 + 12, 44)

    # ceruk tengah: persegi + lengkung di atas
    d.rectangle([21, 26, 50, 47], fill=KAIN_GADING)
    d.ellipse([21, 12, 50, 40], fill=KAIN_GADING)
    for y in range(18, 46, 6):
        for x in range(24, 49, 6):
            if (x - 35.5) ** 2 / 210 + (y - 27) ** 2 / 290 > 1.05:
                continue
            d.point((x, y), fill=KAIN_BAYANG)
            d.point((x + 1, y + 1), fill=KAIN_BAYANG)

    # bingkai emas ceruk
    d.arc([20, 11, 51, 41], 180, 360, fill=UKIR, width=2)
    d.rectangle([19, 26, 20, 47], fill=UKIR)
    d.rectangle([51, 26, 52, 47], fill=UKIR)

    # mahkota gunungan di puncak, bertingkat supaya siluetnya jelas
    d.rectangle([24, 5, 47, 11], fill=JATI_TUA)
    d.rectangle([25, 6, 46, 10], fill=UKIR)
    for x in range(27, 46, 4):
        d.rectangle([x, 7, x + 1, 9], fill=JATI_TUA)
    d.polygon([(35, 0), (28, 6), (43, 6)], fill=JATI_TUA)
    d.polygon([(35, 1), (30, 6), (41, 6)], fill=UKIR)
    d.polygon([(35, 3), (33, 6), (38, 6)], fill=UKIR_TERANG)
    # sulur ukiran di kiri-kanan mahkota
    d.polygon([(24, 11), (16, 6), (19, 11)], fill=UKIR)
    d.polygon([(47, 11), (55, 6), (52, 11)], fill=UKIR)

    # janur kuning terurai di dua sudut atas
    for x0, arah in ((8, -1), (63, 1)):
        for i in range(7):
            warna = JANUR if i % 2 else JANUR_TERANG
            d.line([(x0, 14), (x0 + arah * (2 + i), 4 + i)], fill=warna)
        d.rectangle([x0 - 1, 13, x0 + 1, 17], fill=JANUR_GELAP)

    # roncean melati mengikuti lengkung ceruk
    for derajat in range(182, 359, 9):
        t = math.radians(derajat)
        x = round(35.5 + 16.5 * math.cos(t))
        y = round(26.5 + 15.5 * math.sin(t))
        d.rectangle([x, y, x + 1, y + 1], fill=MELATI)
        d.point((x, y + 2), fill=(228, 228, 218, 255))

    return garis_luar(img)


def prop_pengantin_pria():
    """Mempelai pria: beskap gading, blangkon bermondolan, kain jarik batik."""
    img, d = kanvas(20, 36)
    kulit = (240, 202, 166, 255)
    kulit_gelap = (212, 170, 134, 255)
    beskap = (248, 242, 228, 255)
    beskap_bayang = (222, 212, 194, 255)
    jarik = (118, 80, 50, 255)
    jarik_motif = (162, 122, 84, 255)
    gelap = (56, 42, 38, 255)
    blangkon = (96, 66, 46, 255)
    blangkon_terang = (132, 96, 68, 255)

    # kain jarik menutup kaki, lalu selop
    d.rectangle([5, 26, 14, 33], fill=jarik)
    for y in range(27, 33, 2):
        for x in range(6, 14, 3):
            d.rectangle([x, y, x + 1, y], fill=jarik_motif)
    d.rectangle([5, 33, 14, 34], fill=gelap)

    # beskap
    d.rectangle([5, 17, 14, 27], fill=beskap)
    d.line([(5, 26), (14, 26)], fill=beskap_bayang)
    d.rectangle([9, 17, 10, 26], fill=beskap_bayang)
    for y in (19, 21, 23):
        d.point((9, y), fill=UKIR)
    d.rectangle([7, 17, 12, 18], fill=beskap_bayang)

    # lengan
    for x0 in (3, 15):
        d.rectangle([x0, 18, x0 + 1, 25], fill=beskap)
        d.rectangle([x0, 25, x0 + 1, 26], fill=kulit)

    # keris terselip di pinggang belakang
    d.line([(15, 24), (17, 19)], fill=UKIR)
    d.point((17, 18), fill=UKIR_TERANG)

    # kepala
    d.rectangle([6, 9, 13, 16], fill=kulit)
    d.line([(6, 16), (13, 16)], fill=kulit_gelap)

    # blangkon: kain batik melilit + mondolan di belakang
    d.ellipse([12, 3, 16, 8], fill=blangkon)
    d.point((14, 4), fill=blangkon_terang)
    d.rectangle([5, 5, 14, 10], fill=blangkon)
    d.rectangle([5, 5, 14, 6], fill=blangkon_terang)
    d.rectangle([5, 9, 14, 10], fill=(72, 50, 36, 255))
    for x in range(6, 14, 2):
        d.point((x, 7), fill=(208, 186, 152, 255))

    # wajah
    d.point((8, 12), fill=gelap)
    d.point((11, 12), fill=gelap)
    d.line([(9, 14), (10, 14)], fill=(198, 138, 126, 255))

    return garis_luar(img)


def prop_pengantin_wanita():
    """Mempelai wanita: kebaya, sanggul + cunduk mentul, paes, roncean melati."""
    img, d = kanvas(20, 36)
    kulit = (246, 212, 178, 255)
    kulit_gelap = (218, 180, 146, 255)
    kebaya = (250, 246, 238, 255)
    kebaya_bayang = (230, 224, 212, 255)
    songket = (174, 130, 68, 255)
    songket_motif = (214, 174, 98, 255)
    rambut = (46, 36, 34, 255)
    rambut_kilau = (78, 62, 58, 255)
    gelap = (52, 40, 44, 255)

    # kain songket yang melebar ke bawah
    d.polygon([(6, 24), (13, 24), (15, 33), (4, 33)], fill=songket)
    for y in range(26, 33, 2):
        for x in range(5, 15, 3):
            d.point((x, y), fill=songket_motif)
    d.rectangle([4, 33, 15, 34], fill=(112, 82, 48, 255))

    # kebaya berenda emas
    d.rectangle([5, 17, 14, 25], fill=kebaya)
    d.line([(5, 24), (14, 24)], fill=kebaya_bayang)
    d.rectangle([9, 17, 10, 24], fill=kebaya_bayang)
    for y in (19, 21):
        d.point((7, y), fill=UKIR)
        d.point((12, y), fill=UKIR)
    d.rectangle([7, 17, 12, 18], fill=kebaya_bayang)

    # lengan
    for x0 in (3, 15):
        d.rectangle([x0, 18, x0 + 1, 24], fill=kebaya)
        d.rectangle([x0, 24, x0 + 1, 25], fill=kulit)

    # kepala
    d.rectangle([6, 9, 13, 16], fill=kulit)
    d.line([(6, 16), (13, 16)], fill=kulit_gelap)

    # rambut disanggul: siluet simetris dengan gundukan di atas belakang
    d.rectangle([5, 6, 14, 10], fill=rambut)
    d.rectangle([5, 10, 5, 13], fill=rambut)
    d.rectangle([14, 10, 14, 13], fill=rambut)
    d.ellipse([7, 2, 12, 7], fill=rambut)
    d.point((9, 3), fill=rambut_kilau)

    # cunduk mentul
    for x, puncak in ((7, 0), (9, 0), (12, 1)):
        d.line([(x, 4), (x, puncak)], fill=UKIR)
        d.rectangle([x - 1, puncak, x, puncak + 1], fill=UKIR_TERANG)

    # paes di dahi
    d.line([(6, 10), (7, 9)], fill=rambut)
    d.line([(13, 10), (12, 9)], fill=rambut)
    d.rectangle([9, 9, 10, 9], fill=rambut)

    # roncean melati menjuntai di kedua sisi sanggul
    for y in range(10, 17, 2):
        d.point((4, y), fill=MELATI)
        d.point((4, y + 1), fill=(232, 232, 222, 255))
        d.point((15, y), fill=MELATI)
        d.point((15, y + 1), fill=(232, 232, 222, 255))

    # wajah & anting
    d.point((8, 12), fill=gelap)
    d.point((11, 12), fill=gelap)
    d.line([(9, 14), (10, 14)], fill=(206, 132, 128, 255))
    d.point((6, 12), fill=UKIR)
    d.point((13, 12), fill=UKIR)

    return garis_luar(img)


def prop_gerbang():
    """Gapura janur kuning: tiang bambu dengan lengkung anyaman janur."""
    img, d = kanvas(54, 48)

    for x in (4, 44):
        d.rectangle([x, 15, x + 5, 46], fill=BAMBU)
        d.rectangle([x, 15, x + 1, 46], fill=BAMBU_GELAP)
        for y in range(19, 46, 7):
            d.line([(x, y), (x + 5, y)], fill=BAMBU_GELAP)

    cx, cy, rx, ry = 26.5, 20.0, 22.5, 15.0
    d.arc([4, 5, 49, 35], 180, 360, fill=JANUR, width=5)
    for derajat in range(180, 361, 4):
        t = math.radians(derajat)
        x = round(cx + rx * math.cos(t))
        y = round(cy + ry * math.sin(t))
        warna = JANUR_TERANG if (derajat // 4) % 2 else JANUR_GELAP
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=warna)

    # janur menjuntai dari lengkung
    for x in range(9, 46, 4):
        u = (x - cx) / rx
        if abs(u) > 0.96:
            continue
        y = round(cy - ry * math.sqrt(1 - u * u)) + 4
        panjang = 5 + (x % 3) * 3
        d.line([(x, y), (x, y + panjang)], fill=JANUR)
        d.point((x, y + panjang), fill=JANUR_TERANG)

    # roncean melati
    for derajat in range(186, 355, 10):
        t = math.radians(derajat)
        x = round(cx + (rx - 5) * math.cos(t))
        y = round(cy + (ry - 4) * math.sin(t))
        d.rectangle([x, y, x + 1, y + 1], fill=MELATI)

    return garis_luar(img)


def prop_kembar_mayang():
    """Kembar mayang: rangkaian janur kuning di atas dudukan kayu."""
    img, d = kanvas(24, 42)

    d.polygon([(8, 32), (15, 32), (14, 40), (9, 40)], fill=JATI)
    d.rectangle([7, 30, 16, 33], fill=JATI_TERANG)
    d.line([(9, 31), (14, 31)], fill=JATI_TUA)
    d.rectangle([11, 14, 12, 32], fill=JANUR_GELAP)

    for i, lebar in enumerate((3, 5, 7, 8, 8, 7, 5)):
        y = 13 + i * 3
        d.line([(11 - lebar, y + 2), (11, y - 1)], fill=JANUR)
        d.line([(12 + lebar, y + 2), (12, y - 1)], fill=JANUR)
        d.point((11 - lebar, y + 2), fill=JANUR_TERANG)
        d.point((12 + lebar, y + 2), fill=JANUR_TERANG)

    # burung janur di puncak
    d.polygon([(11, 9), (8, 4), (14, 7)], fill=JANUR_TERANG)
    d.line([(8, 4), (10, 6)], fill=JANUR_GELAP)
    d.point((12, 6), fill=(56, 44, 38, 255))

    for x, y in ((6, 19), (17, 23), (8, 27), (16, 16)):
        d.rectangle([x, y, x + 1, y + 1], fill=MELATI)

    return garis_luar(img)


def prop_umbul_umbul():
    """Umbul-umbul: tiang bambu dengan kain panji menjuntai."""
    img, d = kanvas(17, 46)

    d.ellipse([3, 41, 12, 45], fill=(96, 82, 66, 255))
    d.rectangle([7, 3, 8, 43], fill=BAMBU)
    d.rectangle([7, 3, 7, 43], fill=BAMBU_GELAP)
    d.rectangle([6, 0, 9, 3], fill=UKIR)
    d.point((7, 0), fill=UKIR_TERANG)

    d.polygon([(9, 5), (15, 5), (15, 27), (12, 32), (9, 27)], fill=MERAH)
    d.rectangle([9, 5, 15, 7], fill=UKIR)
    for y in range(10, 27, 5):
        d.line([(9, y), (15, y)], fill=(198, 78, 88, 255))
        d.point((12, y + 2), fill=UKIR)
    d.point((12, 31), fill=UKIR_TERANG)

    return garis_luar(img)


def prop_pohon_palem():
    img, d = kanvas(32, 46)
    batang = (154, 124, 86, 255)
    batang_gelap = (122, 96, 64, 255)

    for i, y in enumerate(range(19, 44)):
        x = 15 + round(math.sin(i * 0.11) * 1.6)
        d.rectangle([x, y, x + 3, y], fill=batang)
        d.point((x, y), fill=batang_gelap)
        if i % 3 == 0:
            d.point((x + 3, y), fill=batang_gelap)

    for sudut in (198, 224, 250, 290, 316, 342):
        t = math.radians(sudut)
        ux, uy = math.cos(t), math.sin(t)
        for j in range(3, 15):
            x = round(16 + ux * j)
            y = round(19 + uy * j + j * j * 0.035)
            warna = DAUN if j > 8 else DAUN_TERANG
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=warna)

    d.ellipse([12, 17, 15, 20], fill=(126, 96, 62, 255))
    d.ellipse([17, 18, 20, 21], fill=(126, 96, 62, 255))
    return garis_luar(img)


def prop_pohon_kamboja():
    img, d = kanvas(32, 46)
    batang = (178, 160, 140, 255)
    batang_gelap = (146, 128, 110, 255)

    d.rectangle([14, 28, 18, 44], fill=batang)
    d.rectangle([14, 28, 15, 44], fill=batang_gelap)
    d.line([(16, 30), (10, 23)], fill=batang, width=2)
    d.line([(16, 30), (23, 22)], fill=batang, width=2)
    d.line([(16, 28), (16, 19)], fill=batang, width=2)

    d.ellipse([3, 9, 29, 30], fill=DAUN)
    d.ellipse([6, 6, 26, 24], fill=DAUN_TERANG)
    r = random.Random(77)
    for _ in range(30):
        x, y = r.randrange(5, 28), r.randrange(7, 28)
        if (x - 16) ** 2 / 165 + (y - 16) ** 2 / 120 > 1:
            continue
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(252, 250, 238, 255))
        d.point((x, y), fill=(250, 214, 128, 255))
    return garis_luar(img)


def prop_meja_tumpeng():
    """Meja tumpeng: nasi kuning di atas daun pisang dan taplak merah."""
    img, d = kanvas(32, 34)
    nasi = (246, 214, 96, 255)
    nasi_terang = (252, 234, 146, 255)

    d.polygon([(3, 17), (28, 17), (26, 32), (5, 32)], fill=MERAH)
    d.polygon([(3, 27), (28, 27), (26, 32), (5, 32)], fill=MERAH_TUA)
    d.rectangle([2, 15, 29, 18], fill=(196, 74, 84, 255))
    d.line([(2, 18), (29, 18)], fill=UKIR)
    for x in range(5, 27, 5):
        d.line([(x, 19), (x - 1, 31)], fill=(178, 60, 70, 255))

    d.ellipse([7, 11, 24, 17], fill=DAUN)
    d.ellipse([9, 12, 22, 16], fill=DAUN_TERANG)

    d.polygon([(15, 0), (8, 14), (23, 14)], fill=nasi)
    d.polygon([(15, 0), (11, 14), (15, 14)], fill=nasi_terang)
    d.point((15, 1), fill=(198, 70, 60, 255))
    d.point((15, 2), fill=(198, 70, 60, 255))
    for x in (10, 13, 18, 21):
        d.rectangle([x, 12, x + 1, 13], fill=(250, 244, 226, 255))

    d.ellipse([4, 12, 8, 16], fill=(198, 130, 70, 255))
    d.ellipse([23, 12, 27, 16], fill=(150, 172, 88, 255))
    return garis_luar(img)


def prop_galeri():
    img, d = kanvas(30, 34)
    d.line([(7, 33), (14, 13)], fill=JATI, width=2)
    d.line([(23, 33), (16, 13)], fill=JATI, width=2)
    d.line([(15, 20), (15, 33)], fill=JATI_TUA, width=2)
    d.line([(9, 27), (21, 27)], fill=JATI, width=1)
    d.rectangle([4, 3, 25, 24], fill=UKIR)
    d.rectangle([5, 4, 24, 23], fill=(184, 146, 80, 255))
    d.rectangle([6, 5, 23, 22], fill=(250, 247, 240, 255))
    d.rectangle([6, 5, 23, 7], fill=(214, 228, 240, 255))
    # siluet sepasang pengantin adat di dalam foto
    d.rectangle([9, 12, 13, 21], fill=(238, 232, 218, 255))
    d.ellipse([9, 8, 13, 12], fill=(226, 190, 158, 255))
    d.rectangle([9, 7, 13, 9], fill=(98, 68, 46, 255))
    d.polygon([(16, 21), (20, 21), (21, 13), (15, 13)], fill=(244, 240, 232, 255))
    d.ellipse([16, 8, 20, 12], fill=(238, 202, 170, 255))
    d.ellipse([16, 6, 21, 11], fill=(46, 36, 34, 255))
    return garis_luar(img)


def prop_buku_tamu():
    img, d = kanvas(24, 30)
    d.ellipse([5, 25, 18, 29], fill=JATI_TUA)
    d.rectangle([10, 13, 13, 27], fill=JATI)
    d.polygon([(3, 10), (20, 10), (22, 15), (1, 15)], fill=JATI)
    d.polygon([(3, 10), (20, 10), (21, 12), (2, 12)], fill=JATI_TUA)
    d.line([(2, 13), (21, 13)], fill=UKIR)
    d.polygon([(4, 6), (19, 6), (20, 11), (3, 11)], fill=(250, 248, 242, 255))
    d.line([(11, 6), (11, 11)], fill=(216, 208, 192, 255))
    for y in (8, 9):
        d.line([(5, y), (10, y)], fill=(198, 190, 176, 255))
        d.line([(13, y), (18, y)], fill=(198, 190, 176, 255))
    d.line([(17, 2), (20, 7)], fill=(198, 88, 96, 255), width=1)
    d.point((17, 2), fill=(248, 240, 226, 255))
    return garis_luar(img)


def prop_papan():
    img, d = kanvas(28, 32)
    d.rectangle([12, 17, 15, 30], fill=JATI)
    d.rectangle([12, 17, 12, 30], fill=JATI_TUA)
    d.rectangle([2, 3, 25, 19], fill=JATI_TUA)
    d.rectangle([3, 4, 24, 18], fill=JATI)
    d.rectangle([4, 5, 23, 17], fill=(246, 238, 224, 255))
    d.rectangle([5, 6, 22, 8], fill=MERAH)
    for y in (11, 13, 15):
        d.line([(6, y), (21, y)], fill=(176, 164, 146, 255))
    # ukiran kecil di sudut papan
    for x, y in ((3, 4), (24, 4), (3, 18), (24, 18)):
        d.point((x, y), fill=UKIR)
    d.rectangle([9, 29, 18, 31], fill=(110, 152, 96, 255))
    return garis_luar(img)


def prop_hadiah():
    """Kotak angpao kayu bermotif batik kawung."""
    img, d = kanvas(28, 30)
    d.rectangle([3, 11, 24, 26], fill=JATI_TERANG)
    d.rectangle([3, 22, 24, 26], fill=JATI)
    d.rectangle([2, 7, 25, 12], fill=JATI)
    d.rectangle([3, 8, 24, 10], fill=JATI_TERANG)
    for y in range(14, 22, 4):
        for x in range(5, 24, 4):
            d.point((x, y), fill=JATI_TUA)
            d.point((x + 1, y + 1), fill=JATI_TUA)
            d.point((x + 1, y), fill=UKIR)
            d.point((x, y + 1), fill=UKIR)
    d.rectangle([2, 7, 25, 8], fill=UKIR)
    d.rectangle([3, 25, 24, 26], fill=UKIR)
    d.rectangle([8, 9, 19, 10], fill=(48, 36, 32, 255))
    d.polygon([(13, 2), (10, 7), (17, 7)], fill=UKIR)
    d.polygon([(13, 4), (12, 7), (15, 7)], fill=UKIR_TERANG)
    return garis_luar(img)


def prop_bangku():
    img, d = kanvas(30, 20)
    d.rectangle([3, 2, 26, 4], fill=JATI)
    d.rectangle([3, 5, 26, 6], fill=JATI_TUA)
    d.line([(4, 3), (25, 3)], fill=UKIR)
    d.rectangle([2, 9, 27, 12], fill=JATI)
    d.line([(2, 12), (27, 12)], fill=JATI_TUA)
    for x in (4, 24):
        d.rectangle([x, 2, x + 1, 17], fill=JATI_TUA)
    d.rectangle([6, 13, 7, 18], fill=JATI_TUA)
    d.rectangle([22, 13, 23, 18], fill=JATI_TUA)
    return garis_luar(img)


def prop_semak():
    img, d = kanvas(22, 18)
    d.ellipse([1, 5, 20, 16], fill=DAUN)
    d.ellipse([4, 2, 17, 13], fill=DAUN_TERANG)
    r = random.Random(51)
    for _ in range(6):
        x, y = r.randrange(4, 17), r.randrange(4, 13)
        d.rectangle([x, y, x + 1, y + 1], fill=(226, 96, 152, 255))
    return garis_luar(img)


def prop_pot():
    """Pot tanah dengan bunga bugenvil."""
    img, d = kanvas(18, 22)
    d.polygon([(5, 13), (12, 13), (11, 21), (6, 21)], fill=(180, 112, 86, 255))
    d.rectangle([4, 11, 13, 13], fill=(202, 130, 100, 255))
    d.line([(6, 12), (11, 12)], fill=(164, 100, 76, 255))
    for x, tinggi in ((6, 5), (9, 3), (12, 6)):
        d.line([(x, 11), (x, tinggi)], fill=DAUN)
    d.rectangle([5, 3, 7, 5], fill=(226, 96, 152, 255))
    d.rectangle([8, 1, 10, 3], fill=(244, 138, 178, 255))
    d.rectangle([11, 4, 13, 6], fill=(226, 96, 152, 255))
    d.point((9, 2), fill=(250, 214, 128, 255))
    return garis_luar(img)


def prop_lampu():
    img, d = kanvas(14, 34)
    d.ellipse([2, 29, 11, 33], fill=(72, 68, 76, 255))
    d.rectangle([6, 11, 8, 31], fill=(88, 84, 92, 255))
    d.rectangle([6, 11, 6, 31], fill=(66, 62, 70, 255))
    d.polygon([(3, 10), (11, 10), (10, 4), (4, 4)], fill=(252, 238, 186, 255))
    d.polygon([(4, 5), (10, 5), (9, 7), (5, 7)], fill=(254, 250, 226, 255))
    d.polygon([(2, 4), (12, 4), (10, 1), (4, 1)], fill=(72, 68, 76, 255))
    return garis_luar(img)


def prop_air_mancur():
    img, d = kanvas(34, 32)
    d.ellipse([1, 14, 32, 30], fill=(206, 198, 186, 255))
    d.ellipse([3, 16, 30, 28], fill=(110, 168, 200, 255))
    d.ellipse([5, 17, 28, 26], fill=(132, 186, 214, 255))
    d.ellipse([12, 12, 21, 18], fill=(206, 198, 186, 255))
    d.rectangle([15, 6, 18, 15], fill=(220, 213, 200, 255))
    d.ellipse([11, 3, 22, 9], fill=(232, 226, 214, 255))
    for dx in (-6, -3, 3, 6):
        d.line([(16 + dx, 6), (round(16 + dx * 1.6), 15)], fill=(176, 214, 234, 255))
    d.rectangle([15, 0, 18, 5], fill=(186, 220, 238, 255))
    r = random.Random(81)
    for _ in range(8):
        d.point((r.randrange(6, 28), r.randrange(18, 26)), fill=(196, 226, 240, 255))
    return garis_luar(img)


def prop_teratai():
    img, d = kanvas(16, 11)
    d.ellipse([0, 2, 11, 10], fill=(72, 132, 82, 255))
    d.ellipse([1, 3, 9, 9], fill=(92, 154, 96, 255))
    d.polygon([(5, 6), (5, 3), (7, 6)], fill=(60, 112, 70, 255))
    d.ellipse([9, 0, 15, 6], fill=(246, 206, 218, 255))
    d.ellipse([11, 2, 14, 5], fill=(252, 240, 244, 255))
    d.point((12, 3), fill=(250, 214, 128, 255))
    return garis_luar(img)


PROPERTI = {
    "pelaminan": prop_pelaminan,
    "pengantin_pria": prop_pengantin_pria,
    "pengantin_wanita": prop_pengantin_wanita,
    "galeri": prop_galeri,
    "buku_tamu": prop_buku_tamu,
    "papan": prop_papan,
    "hadiah": prop_hadiah,
    "gerbang": prop_gerbang,
    "kembar_mayang": prop_kembar_mayang,
    "umbul_umbul": prop_umbul_umbul,
    "meja_tumpeng": prop_meja_tumpeng,
    "pohon_palem": prop_pohon_palem,
    "pohon_kamboja": prop_pohon_kamboja,
    "semak": prop_semak,
    "pot": prop_pot,
    "bangku": prop_bangku,
    "lampu": prop_lampu,
    "air_mancur": prop_air_mancur,
    "teratai": prop_teratai,
}


def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    nama_tile = buat_tileset()
    nama_tepi = buat_tepi()
    buat_karakter("karakter_pria", PALET_PRIA, rok=False)
    buat_karakter("karakter_wanita", PALET_WANITA, rok=True)
    for nama, fungsi in PROPERTI.items():
        perbesar(fungsi()).save(KELUARAN / f"{nama}.png")

    print("Tileset  :", ", ".join(f"{i}={n}" for i, n in enumerate(nama_tile)))
    print("Tepi     :", ", ".join(f"{i}={n}" for i, n in enumerate(nama_tepi)))
    print("Karakter : karakter_pria.png, karakter_wanita.png")
    print("Properti :", ", ".join(PROPERTI))
    print("Tersimpan di", KELUARAN)


if __name__ == "__main__":
    main()
