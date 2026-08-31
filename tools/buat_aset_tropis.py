"""Aset pixel art untuk tema "Taman Tropis" (tampak atas).

Kamera lurus dari atas seperti Stardew Valley. Petak tanah persegi 48x48
digambar langsung pada resolusi akhir dan dijamin tileable; properti dan
karakter digambar sebagai gambar tegak yang berdiri di atas petak.

    python tools/buat_aset_tropis.py

Keluaran di static/game_tropis/.
"""

import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from buat_aset import garis_luar, kanvas, perbesar  # noqa: E402

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game_tropis"

LEBAR_PETAK = 32          # lebar belah ketupat sebelum diperbesar
TINGGI_PETAK = 16
GARIS_ISO = (38, 30, 26, 255)

# Palet yang mengikuti acuan: hijau tropis pekat, batu abu hangat, air cerah.
RUMPUT = (96, 170, 68, 255)
RUMPUT_GELAP = (74, 144, 52, 255)
RUMPUT_TERANG = (128, 196, 92, 255)
BATU = (152, 150, 140, 255)
BATU_TERANG = (176, 174, 162, 255)
BATU_GELAP = (118, 116, 108, 255)
AIR = (74, 170, 208, 255)
AIR_TERANG = (128, 212, 238, 255)
AIR_GELAP = (54, 142, 186, 255)
TANAH = (146, 108, 74, 255)
KAYU_TUA = (108, 66, 38, 255)
KAYU = (150, 98, 54, 255)
KAYU_TERANG = (188, 136, 80, 255)
EMAS = (220, 174, 88, 255)
EMAS_TERANG = (244, 212, 134, 255)
MERAH = (176, 52, 58, 255)
MERAH_TUA = (140, 38, 46, 255)
KREM = (240, 228, 202, 255)
DAUN_TUA = (38, 104, 52, 255)
DAUN = (54, 138, 62, 255)
DAUN_TERANG = (92, 178, 80, 255)
MELATI = (250, 250, 242, 255)

WARNA_BUNGA = [
    (232, 72, 76, 255),
    (248, 168, 60, 255),
    (250, 226, 96, 255),
    (238, 122, 176, 255),
    (168, 116, 216, 255),
    (252, 250, 244, 255),
]


# --------------------------------------------------------------------------
# Petak tanah persegi (tampak atas)
#
# Tiap petak digambar sembilan kali pada kanvas 144x144 lalu bagian tengahnya
# dipotong, sehingga bentuk yang melewati satu tepi muncul lagi di tepi
# seberang — petak dijamin bisa disusun tanpa sambungan terlihat.
# --------------------------------------------------------------------------
UKURAN_PETAK = 48

RUMPUT_KILAU = (156, 214, 110, 255)
RUMPUT_PEKAT = (54, 114, 42, 255)
BATU_PEKAT = (62, 58, 54, 255)
TANAH_PEKAT = (94, 68, 46, 255)


def _geser(xy, dx, dy):
    """Menggeser koordinat; menerima [x0,y0,x1,y1], [(x,y), ...], atau (x,y)."""
    if isinstance(xy, (list, tuple)) and xy and isinstance(xy[0], (list, tuple)):
        return [(x + dx, y + dy) for x, y in xy]
    nilai = list(xy)
    return [n + (dx if i % 2 == 0 else dy) for i, n in enumerate(nilai)]


class GambarBungkus:
    """Meneruskan tiap perintah gambar ke sembilan posisi petak."""

    def __init__(self, d, ukuran=UKURAN_PETAK, ulang=3):
        self._d = d
        self._u = ukuran
        self._n = ulang

    def __getattr__(self, nama):
        fungsi = getattr(self._d, nama)

        def bungkus(xy, *args, **kwargs):
            for baris in range(self._n):
                for kolom in range(self._n):
                    fungsi(_geser(xy, kolom * self._u, baris * self._u), *args, **kwargs)

        return bungkus


ULANG = 3
KANVAS_TERAKHIR = None


def petak(gambar_fn, latar):
    global KANVAS_TERAKHIR
    sisi = UKURAN_PETAK * ULANG
    besar = Image.new("RGBA", (sisi, sisi), latar)
    gambar_fn(GambarBungkus(ImageDraw.Draw(besar), UKURAN_PETAK, ULANG))
    KANVAS_TERAKHIR = besar
    return besar.crop((UKURAN_PETAK, UKURAN_PETAK, UKURAN_PETAK * 2, UKURAN_PETAK * 2))


def _bintik(d, r, jumlah, warna):
    for _ in range(jumlah):
        d.point((r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)), fill=warna)


def petak_rumput(seed=1, berbunga=False, gelap=False):
    dasar = (58, 122, 46, 255) if gelap else RUMPUT
    terang = (78, 148, 60, 255) if gelap else RUMPUT_TERANG
    kilau = (98, 172, 76, 255) if gelap else RUMPUT_KILAU
    bayang = (44, 96, 38, 255) if gelap else RUMPUT_GELAP
    pekat = (34, 76, 30, 255) if gelap else RUMPUT_PEKAT

    def gambar(d):
        r = random.Random(seed)
        for _ in range(7):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(16, 28), y + r.randint(6, 11)], fill=bayang)
        for _ in range(7):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(14, 24), y + r.randint(5, 9)], fill=terang)
        # rumpun helai
        for _ in range(60):
            px, py = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            condong = r.choice((-1, 0, 0, 1))
            for _ in range(r.randint(3, 5)):
                x = px + r.randint(-4, 4)
                y = py + r.randint(-3, 3)
                tinggi = r.randint(3, 5)
                d.line([(x, y), (x + condong, y - tinggi)], fill=pekat if r.random() < 0.35 else bayang)
                d.point((x + condong, y - tinggi), fill=kilau if r.random() < 0.5 else terang)
        _bintik(d, r, 70, kilau)
        _bintik(d, r, 60, pekat)
        if berbunga:
            for _ in range(7):
                x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
                w = r.choice(WARNA_BUNGA)
                d.rectangle([x, y, x + 1, y + 1], fill=w)
                d.point((x, y + 1), fill=(252, 236, 160, 255))

    return petak(gambar, dasar)


def petak_batu(seed=2):
    """Jalan setapak batu kali dengan nat tanah."""
    def gambar(d):
        r = random.Random(seed)
        for baris in range(0, UKURAN_PETAK, 12):
            for kolom in range(0, UKURAN_PETAK, 12):
                x = kolom + (6 if (baris // 12) % 2 else 0) + r.randint(0, 2)
                y = baris + r.randint(0, 2)
                lebar, tinggi = r.randint(9, 12), r.randint(8, 10)
                d.ellipse([x, y, x + lebar, y + tinggi], fill=BATU_PEKAT)
                d.ellipse([x, y, x + lebar - 1, y + tinggi - 1], fill=BATU)
                d.ellipse([x + 1, y + 1, x + lebar - 4, y + tinggi - 4], fill=BATU_TERANG)
                d.point((x + 3, y + 3), fill=(212, 208, 198, 255))
        _bintik(d, r, 40, BATU_GELAP)
        _bintik(d, r, 24, (206, 202, 192, 255))

    return petak(gambar, TANAH)


def petak_kayu(seed=3):
    """Lantai papan kayu."""
    def gambar(d):
        r = random.Random(seed)
        for baris in range(0, UKURAN_PETAK, 12):
            d.rectangle([0, baris, UKURAN_PETAK, baris + 10], fill=KAYU)
            d.line([(0, baris), (UKURAN_PETAK, baris)], fill=KAYU_TERANG)
            d.line([(0, baris + 11), (UKURAN_PETAK, baris + 11)], fill=KAYU_TUA)
            for _ in range(5):
                x = r.randrange(0, UKURAN_PETAK)
                d.line([(x, baris + 2), (x + r.randint(4, 10), baris + 2)], fill=KAYU_TUA)
            sambung = r.randrange(0, UKURAN_PETAK)
            d.line([(sambung, baris), (sambung, baris + 10)], fill=KAYU_TUA)
        _bintik(d, r, 30, KAYU_TERANG)

    return petak(gambar, KAYU)


def petak_tanah(seed=4, bedeng=False):
    dasar = (110, 78, 54, 255) if bedeng else TANAH

    def gambar(d):
        r = random.Random(seed)
        for _ in range(10):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(10, 20), y + r.randint(6, 12)], fill=TANAH_PEKAT)
        for _ in range(8):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(8, 16), y + r.randint(5, 9)], fill=(178, 136, 98, 255))
        for _ in range(22):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.point((x, y), fill=BATU_GELAP)
            d.point((x, y - 1), fill=BATU)
        _bintik(d, r, 50, TANAH_PEKAT)
        _bintik(d, r, 40, (196, 158, 118, 255))
        if bedeng:
            for _ in range(16):
                x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
                d.line([(x, y + 3), (x, y)], fill=DAUN_TUA)
                d.rectangle([x - 1, y - 2, x + 1, y], fill=r.choice(WARNA_BUNGA))
                d.point((x, y - 1), fill=(252, 240, 170, 255))

    return petak(gambar, dasar)


def petak_tepi_kolam(seed=9):
    """Tepian kolam: batu kali basah bercampur pasir. Bisa dipijak, dan
    sengaja TIDAK menyerupai air supaya pemain tidak terlihat berjalan di
    atas kolam."""
    def gambar(d):
        r = random.Random(seed)
        for _ in range(9):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(10, 18), y + r.randint(6, 11)], fill=(126, 118, 108, 255))
        for _ in range(7):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(8, 14), y + r.randint(5, 8)], fill=(176, 166, 150, 255))
        # batu kali
        for _ in range(16):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            lebar, tinggi = r.randint(5, 9), r.randint(4, 7)
            d.ellipse([x, y, x + lebar, y + tinggi], fill=BATU_PEKAT)
            d.ellipse([x, y, x + lebar - 1, y + tinggi - 1], fill=BATU)
            d.ellipse([x + 1, y + 1, x + lebar - 3, y + tinggi - 3], fill=BATU_TERANG)
        # lumut tipis di sela batu
        for _ in range(10):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.point((x, y), fill=(96, 132, 76, 255))
            d.point((x + 1, y), fill=(76, 110, 60, 255))
        _bintik(d, r, 30, (150, 142, 130, 255))

    return petak(gambar, (152, 144, 132, 255))


def petak_air(seed=5, fase=0, tepi=False):
    """Air kolam. Tiga fase riak dipakai bergantian untuk animasi."""
    def gambar(d):
        r = random.Random(seed)
        for _ in range(10):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(12, 22), y + r.randint(6, 11)], fill=AIR_GELAP)
        # riak: satu periode penuh melintasi petak agar menyambung
        for baris in range(0, UKURAN_PETAK, 12):
            for x in range(UKURAN_PETAK):
                y = baris + round(math.sin((x + fase * 8) / UKURAN_PETAK * math.pi * 2) * 3)
                d.point((x, y), fill=AIR_TERANG)
                if (x + fase * 6) % 16 < 4:
                    d.point((x, y - 1), fill=(196, 236, 248, 255))
        _bintik(d, r, 30, AIR_GELAP)
        if tepi:
            for _ in range(14):
                x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
                d.ellipse([x, y, x + r.randint(4, 7), y + r.randint(3, 5)], fill=BATU)
                d.point((x + 1, y + 1), fill=BATU_TERANG)

    return petak(gambar, AIR)


# Urutan WAJIB sama dengan INDEKS_PETAK di static/js/game_tropis.js
URUTAN_PETAK = [
    ("rumput", lambda: petak_rumput(11)),
    ("rumput2", lambda: petak_rumput(23)),
    ("rumput3", lambda: petak_rumput(37)),
    ("rumput_bunga", lambda: petak_rumput(12, berbunga=True)),
    ("batu", petak_batu),
    ("kayu", petak_kayu),
    ("tanah", petak_tanah),
    ("air1", lambda: petak_air(31, 0)),
    ("air2", lambda: petak_air(31, 1)),
    ("air3", lambda: petak_air(31, 2)),
    ("tepi_air", petak_tepi_kolam),
    ("bedeng", lambda: petak_tanah(41, bedeng=True)),
    ("rimba", lambda: petak_rumput(51, gelap=True)),
]


def buat_tileset():
    petakan = [fn() for _, fn in URUTAN_PETAK]
    lembar = Image.new("RGBA", (UKURAN_PETAK * len(petakan), UKURAN_PETAK), (0, 0, 0, 0))
    for i, t in enumerate(petakan):
        lembar.paste(t, (i * UKURAN_PETAK, 0))
    lembar.save(KELUARAN / "tileset.png")
    return [n for n, _ in URUTAN_PETAK]


# --------------------------------------------------------------------------
# Karakter — gaya Stardew Valley
#
# Kepala sengaja dibuat besar (kepala : tinggi total sekitar 1 : 2,6), mata
# lebar dengan kilau putih, dan bayangan hanya beberapa tingkat supaya
# terlihat rata. Lembar 4 kolom (frame jalan) x 4 baris (bawah, kiri, kanan,
# atas), tiap frame 44x76 dan digambar pada resolusi akhir.
# --------------------------------------------------------------------------
LEBAR_TAMU, TINGGI_TAMU = 44, 76
ARAH_TAMU = ["bawah", "kiri", "kanan", "atas"]
GARIS_TAMU = (44, 30, 26, 255)


def _w(r, g, b, a=255):
    return (r, g, b, a)


MATA_GELAP = _w(52, 36, 34)
MATA_PUTIH = _w(255, 253, 248)
PIPI = _w(244, 168, 156)

PALET_TAMU_PRIA = {
    "kulit": [_w(255, 226, 196), _w(246, 208, 172), _w(214, 168, 130)],
    "rambut": [_w(112, 80, 60), _w(74, 50, 38), _w(48, 32, 25)],
    "iris": _w(96, 66, 46),
    "baju": [_w(196, 148, 96), _w(162, 114, 68), _w(122, 82, 46)],
    "motif": _w(214, 180, 132),
    "sabuk": [_w(248, 216, 138), _w(206, 168, 84)],
    "bawahan": [_w(92, 82, 78), _w(66, 58, 56), _w(44, 38, 38)],
    "alas": [_w(96, 68, 48), _w(62, 42, 30)],
    "rok": False,
}

PALET_TAMU_WANITA = {
    "kulit": [_w(255, 232, 208), _w(250, 216, 186), _w(220, 178, 146)],
    "rambut": [_w(96, 66, 52), _w(62, 42, 34), _w(40, 26, 22)],
    "iris": _w(84, 56, 40),
    "baju": [_w(255, 252, 244), _w(242, 234, 218), _w(206, 194, 174)],
    "motif": _w(214, 174, 102),
    "sabuk": [_w(248, 216, 138), _w(206, 168, 84)],
    "bawahan": [_w(198, 152, 94), _w(166, 120, 70), _w(126, 86, 48)],
    "alas": [_w(140, 100, 66), _w(96, 64, 40)],
    "rok": True,
}


def _kapsul(d, x0, y0, x1, y1, warna):
    r = max(1, min((x1 - x0) // 2, (y1 - y0) // 2))
    d.rectangle([x0, y0 + r, x1, y1 - r], fill=warna)
    d.ellipse([x0, y0, x1, y0 + 2 * r], fill=warna)
    d.ellipse([x0, y1 - 2 * r, x1, y1], fill=warna)


def _mata(d, x, y, iris):
    """Mata kecil biasa: dua piksel gelap dengan satu titik kilau."""
    d.rectangle([x, y, x + 2, y + 2], fill=MATA_GELAP)
    d.point((x + 2, y + 2), fill=iris)
    d.point((x, y), fill=MATA_PUTIH)


def _kepala(d, arah, p, gy, hiasan=None):
    """Kepala berproporsi wajar (sekitar sepertiga tinggi badan).

    Rambut digambar penuh lebih dulu, lalu bidang wajah di atasnya, sehingga
    sisa rambut di atas dan samping otomatis menjadi poni.
    """
    kulit, rambut = p["kulit"], p["rambut"]
    hx0, hx1 = 14, 29
    hy0, hy1 = 5 + gy, 25 + gy

    # kubah kecil di atas supaya ubun-ubun membulat, tidak rata
    d.ellipse([hx0 + 2, hy0 - 4, hx1 - 2, hy0 + 6], fill=rambut[1])
    d.ellipse([hx0 - 1, hy0 - 1, hx1 + 1, hy1 - 2], fill=rambut[1])
    d.point((hx0 - 1, hy0 - 1), fill=(0, 0, 0, 0))
    d.point((hx1 + 1, hy0 - 1), fill=(0, 0, 0, 0))
    d.ellipse([hx0 + 1, hy0 - 2, hx1 - 4, hy0 + 8], fill=rambut[0])

    if arah == "atas":
        d.ellipse([hx0 + 2, hy0 - 4, hx1 - 2, hy0 + 6], fill=rambut[1])
        d.ellipse([hx0 - 1, hy0 - 1, hx1 + 1, hy1], fill=rambut[1])
        d.point((hx0 - 1, hy0 - 1), fill=(0, 0, 0, 0))
        d.point((hx1 + 1, hy0 - 1), fill=(0, 0, 0, 0))
        d.ellipse([hx0 + 1, hy0 - 2, hx1 - 4, hy0 + 9], fill=rambut[0])
        for x in range(hx0 + 2, hx1 - 1, 4):
            d.line([(x, hy0 + 2), (x, hy1 - 2)], fill=rambut[2])
        d.rectangle([hx0 + 5, hy1 - 1, hx1 - 5, hy1 + 2], fill=kulit[2])
        fx0 = fx1 = fy0 = None
    else:
        if arah == "kiri":
            fx0, fx1 = hx0, hx1 - 4
        elif arah == "kanan":
            fx0, fx1 = hx0 + 4, hx1
        else:
            fx0, fx1 = hx0 + 1, hx1 - 1
        fy0 = hy0 + 5
        d.ellipse([fx0, fy0, fx1, hy1], fill=kulit[2])
        d.ellipse([fx0, fy0, fx1 - 2, hy1 - 1], fill=kulit[1])
        d.ellipse([fx0 + 1, fy0 + 1, fx0 + 6, fy0 + 6], fill=kulit[0])
        if arah == "bawah":
            d.rectangle([fx0 - 2, fy0 + 5, fx0 - 1, fy0 + 8], fill=kulit[1])
            d.rectangle([fx1 + 1, fy0 + 5, fx1 + 2, fy0 + 8], fill=kulit[2])
        # helai poni jatuh sedikit ke dahi
        d.ellipse([fx0 + 1, fy0 - 3, fx0 + 6, fy0 + 1], fill=rambut[1])
        d.ellipse([fx1 - 5, fy0 - 3, fx1 - 1, fy0], fill=rambut[0])

    # ---- hiasan kepala ----
    if hiasan == "blangkon":
        coklat, terang = _w(104, 72, 48), _w(140, 102, 68)
        d.ellipse([hx0 - 2, hy0 - 5, hx1 + 2, hy0 + 8], fill=coklat)
        d.ellipse([hx0, hy0 - 4, hx1 - 5, hy0 + 3], fill=terang)
        for x in range(hx0 + 2, hx1 - 1, 4):
            d.point((x, hy0), fill=_w(214, 190, 154))
        d.ellipse([hx1 - 5, hy0 - 3, hx1 + 4, hy0 + 7], fill=coklat)
    elif hiasan == "sanggul":
        d.ellipse([hx0 + 3, hy0 - 10, hx1 - 3, hy0 + 2], fill=rambut[1])
        d.ellipse([hx0 + 5, hy0 - 9, hx1 - 7, hy0 - 2], fill=rambut[0])
        for x, puncak in ((hx0 + 4, hy0 - 15), (hx0 + 8, hy0 - 17), (hx1 - 6, hy0 - 15)):
            d.line([(x, hy0 - 7), (x, puncak + 2)], fill=_w(214, 174, 102))
            d.ellipse([x - 1, puncak, x + 1, puncak + 2], fill=_w(250, 216, 138))
        d.ellipse([hx0 + 4, hy0 - 8, hx0 + 7, hy0 - 5], fill=_w(252, 250, 244))
        d.ellipse([hx1 - 8, hy0 - 7, hx1 - 5, hy0 - 4], fill=_w(246, 176, 196))
        for y in range(hy0 + 8, hy0 + 19, 4):
            d.point((hx0 - 2, y), fill=_w(252, 250, 244))

    if arah == "atas":
        return

    # ---- wajah ----
    iris = p["iris"]
    ey = fy0 + 5
    tengah = (fx0 + fx1) // 2
    _mata(d, tengah - 4, ey, iris)
    _mata(d, tengah + 2, ey, iris)
    d.point((tengah, ey + 3), fill=kulit[2])
    d.line([(tengah - 1, ey + 6), (tengah + 1, ey + 6)], fill=_w(190, 128, 112))


def _badan(d, arah, p, gy, ayun, sabuk=True):
    """Badan, tungkai, dan lengan.

    Mengikuti siluet sprite RPG tampak atas: atasan panjang menutup pinggul,
    lengan lurus di sisi badan sewarna atasan, tungkai pendek dengan sepatu
    kecil. Badan sengaja tidak ikut naik-turun tiap frame supaya tidak
    terlihat berbayang; hanya kaki dan lengan yang bergerak.
    """
    kulit, baju, bawah, alas = p["kulit"], p["baju"], p["bawahan"], p["alas"]
    rok = p["rok"]
    ty0, ty1 = 26, 52

    # ---- tungkai ----
    if rok:
        for x0, maju in ((16, ayun > 0), (24, ayun < 0)):
            atas = 60
            bwh = 67 - (2 if maju else 0)
            _kapsul(d, x0, atas, x0 + 3, bwh, kulit[1])
            _kapsul(d, x0 - 1, bwh - 2, x0 + 4, bwh + 2, alas[0])
    else:
        # Kedua telapak selalu menyentuh tanah; yang berubah hanya renggang
        # tungkai dan beda tinggi 1 px, supaya tidak terlihat melayang.
        for x0, maju in ((15, ayun > 0), (24, ayun < 0)):
            x = x0 + (-1 if (maju and x0 == 15) else (1 if maju else 0))
            atas = ty1 - 4
            bwh = 66 - (1 if maju else 0)
            _kapsul(d, x, atas, x + 4, bwh, bawah[1])
            d.line([(x, atas + 2), (x, bwh - 2)], fill=bawah[0])
            d.line([(x + 4, atas + 2), (x + 4, bwh - 2)], fill=bawah[2])
            _kapsul(d, x - 1, bwh - 1, x + 5, bwh + 3, alas[0])
            d.line([(x, bwh + 2), (x + 4, bwh + 2)], fill=alas[1])
        d.line([(21, ty1 - 2), (21, 63)], fill=bawah[2])
        d.line([(22, ty1 - 2), (22, 63)], fill=bawah[2])

    # ---- kain panjang untuk yang berkebaya ----
    if rok:
        d.polygon([(14, 44), (30, 44), (34, 63), (10, 63)], fill=bawah[1])
        d.polygon([(23, 44), (30, 44), (34, 63), (25, 63)], fill=bawah[2])
        d.polygon([(14, 44), (17, 44), (14, 63), (10, 63)], fill=bawah[0])
        for yy in range(49, 62, 6):
            for xx in range(14, 31, 7):
                d.point((xx, yy), fill=p["motif"])
        ty1 = 46

    # ---- atasan panjang ----
    _kapsul(d, 13, ty0, 30, ty1, baju[1])
    d.rectangle([13, ty0 + 5, 15, ty1 - 3], fill=baju[0])
    d.rectangle([28, ty0 + 5, 30, ty1 - 3], fill=baju[2])
    d.line([(14, ty1 - 2), (29, ty1 - 2)], fill=baju[2])   # kelim bawah
    if not rok:
        for yy in range(ty0 + 6, ty1 - 5, 7):
            for xx in range(17, 28, 7):
                d.point((xx, yy), fill=p["motif"])

    # ---- kerah ----
    if arah != "atas":
        d.polygon([(18, ty0), (21, ty0 + 5), (25, ty0)], fill=baju[2])
        d.point((21, ty0 + 2), fill=baju[0])

    # ---- lengan lurus di sisi badan ----
    for x0, sisi in ((9, -1), (31, 1)):
        ayunL = -ayun * sisi
        atas = ty0 + 3 + (1 if ayunL > 0 else 0) - (1 if ayunL < 0 else 0)
        bawahL = ty1 - 4 + (1 if ayunL > 0 else 0) - (1 if ayunL < 0 else 0)
        _kapsul(d, x0, atas, x0 + 3, bawahL, baju[1])
        d.line([(x0, atas + 2), (x0, bawahL - 3)], fill=baju[0] if sisi < 0 else baju[2])
        pemisah = x0 + 4 if sisi < 0 else x0 - 1
        d.line([(pemisah, atas + 1), (pemisah, bawahL - 4)], fill=baju[2])
        # telapak kecil yang menumpuk ujung lengan, bukan bola terpisah
        d.rectangle([x0 + 1, bawahL - 2, x0 + 3, bawahL], fill=kulit[1])
        d.point((x0 + 3, bawahL), fill=kulit[2])
    return ty0


def karakter_frame(arah, frame, p):
    img, d = kanvas(LEBAR_TAMU, TINGGI_TAMU)
    ayun = [0, 1, 0, -1][frame]
    _badan(d, arah, p, 0, ayun)
    _kepala(d, arah, p, 0)
    return garis_luar(img, GARIS_TAMU)


def buat_karakter(nama, palet):
    lembar, _ = kanvas(LEBAR_TAMU * 4, TINGGI_TAMU * 4)
    for baris, arah in enumerate(ARAH_TAMU):
        for kolom in range(4):
            bingkai = karakter_frame("kiri" if arah == "kanan" else arah, kolom, palet)
            if arah == "kanan":
                bingkai = bingkai.transpose(Image.FLIP_LEFT_RIGHT)
            lembar.paste(bingkai, (kolom * LEBAR_TAMU, baris * TINGGI_TAMU))
    lembar.save(KELUARAN / f"{nama}.png")


# --------------------------------------------------------------------------
# Sepasang mempelai — sprite tersendiri, berdiri di depan pelaminan
# --------------------------------------------------------------------------
PALET_MEMPELAI_PRIA = {
    "kulit": PALET_TAMU_PRIA["kulit"],
    "rambut": PALET_TAMU_PRIA["rambut"],
    "iris": PALET_TAMU_PRIA["iris"],
    "baju": [_w(255, 252, 242), _w(244, 238, 222), _w(210, 202, 184)],
    "motif": _w(216, 178, 108),
    "sabuk": [_w(250, 220, 142), _w(208, 170, 86)],
    "bawahan": [_w(176, 132, 84), _w(142, 100, 58), _w(106, 72, 40)],
    "alas": [_w(88, 62, 44), _w(58, 40, 28)],
    "rok": False,
}

PALET_MEMPELAI_WANITA = {
    "kulit": PALET_TAMU_WANITA["kulit"],
    "rambut": PALET_TAMU_WANITA["rambut"],
    "iris": PALET_TAMU_WANITA["iris"],
    "baju": [_w(255, 254, 250), _w(250, 246, 238), _w(216, 208, 192)],
    "motif": _w(224, 186, 116),
    "sabuk": [_w(250, 220, 142), _w(208, 170, 86)],
    "bawahan": [_w(198, 156, 100), _w(166, 124, 74), _w(126, 90, 50)],
    "alas": [_w(128, 92, 60), _w(88, 60, 38)],
    "rok": True,
}


def prop_pengantin(pria):
    p = PALET_MEMPELAI_PRIA if pria else PALET_MEMPELAI_WANITA
    img, d = kanvas(LEBAR_TAMU, TINGGI_TAMU)
    ty0 = _badan(d, "bawah", p, 0, 0)
    if pria:
        # keris terselip di pinggang
        d.line([(29, ty0 + 22), (33, ty0 + 12)], fill=_w(208, 170, 86))
        d.ellipse([31, ty0 + 9, 35, ty0 + 14], fill=_w(248, 216, 138))
    else:
        # untaian melati di depan kebaya
        for y in range(ty0 + 7, ty0 + 19, 4):
            d.ellipse([20, y, 22, y + 2], fill=_w(252, 250, 244))
    _kepala(d, "bawah", p, 0, hiasan="blangkon" if pria else "sanggul")
    return garis_luar(img, GARIS_TAMU)


# --------------------------------------------------------------------------
# Tumbuhan
# --------------------------------------------------------------------------
def prop_palem():
    """Kelapa tinggi dengan pelepah panjang yang melengkung turun."""
    img, d = kanvas(54, 88)
    tinggi_batang = 62
    for i in range(tinggi_batang):
        y = 86 - i
        x = 25 + round(math.sin(i * 0.042) * 4)
        d.rectangle([x, y, x + 4, y], fill=(164, 124, 78, 255))
        d.point((x, y), fill=(124, 88, 54, 255))
        d.point((x + 4, y), fill=(124, 88, 54, 255))
        if i % 5 == 0:
            d.line([(x + 1, y), (x + 3, y)], fill=(136, 100, 62, 255))

    px = 25 + round(math.sin(tinggi_batang * 0.042) * 4) + 2
    py = 86 - tinggi_batang

    for sudut in (186, 208, 232, 256, 284, 308, 332, 354):
        t = math.radians(sudut)
        ux, uy = math.cos(t), math.sin(t)
        nx, ny = -uy, ux
        for j in range(3, 27):
            lengkung = (j / 26.0) ** 2 * 18
            x = px + ux * j
            y = py + uy * j + lengkung
            xi, yi = round(x), round(y)
            if 0 <= xi < 54 and 0 <= yi < 88:
                d.point((xi, yi), fill=DAUN_TUA)
            # anak daun tegak lurus tulang pelepah
            panjang = max(1, 5 - j // 7)
            for arah in (-1, 1):
                for k in range(1, panjang + 1):
                    ax = round(x + nx * k * arah)
                    ay = round(y + ny * k * arah + k * 0.5)
                    if 0 <= ax < 54 and 0 <= ay < 88:
                        d.point((ax, ay), fill=DAUN_TERANG if k == 1 else DAUN)

    for x, y in ((20, py + 1), (27, py + 2), (23, py + 4)):
        d.ellipse([x, y, x + 5, y + 5], fill=(154, 116, 68, 255))
        d.point((x + 1, y + 1), fill=(184, 146, 92, 255))
    return garis_luar(img, GARIS_ISO)


def prop_pisang():
    """Pohon pisang dengan daun lebar berbentuk dayung."""
    img, d = kanvas(48, 68)
    d.rectangle([19, 38, 27, 66], fill=(118, 158, 72, 255))
    d.rectangle([19, 38, 21, 66], fill=(88, 126, 54, 255))
    for y in range(42, 66, 7):
        d.line([(19, y), (27, y)], fill=(98, 136, 58, 255))

    pusat = (23, 38)
    for sudut, panjang, lebar in (
        (194, 23, 7), (220, 25, 8), (250, 22, 7),
        (290, 22, 7), (320, 25, 8), (346, 23, 7),
    ):
        t = math.radians(sudut)
        ux, uy = math.cos(t), math.sin(t)
        nx, ny = -uy, ux
        for j in range(2, panjang):
            lengkung = (j / panjang) ** 2 * 9
            x = pusat[0] + ux * j
            y = pusat[1] + uy * j + lengkung
            w = max(1, round(lebar * math.sin(j / panjang * math.pi) ** 0.55))
            for s in range(-w, w + 1):
                ax = round(x + nx * s)
                ay = round(y + ny * s)
                if 0 <= ax < 48 and 0 <= ay < 68:
                    d.point((ax, ay), fill=DAUN_TUA if abs(s) >= w - 1 else DAUN)
            xi, yi = round(x), round(y)
            if 0 <= xi < 48 and 0 <= yi < 68:
                d.point((xi, yi), fill=DAUN_TERANG)
    return garis_luar(img, GARIS_ISO)


def prop_pakis():
    """Rumpun pakis dengan pelepah melengkung."""
    img, d = kanvas(38, 32)
    for sudut, panjang in ((192, 16), (214, 18), (240, 17), (300, 17), (326, 18), (348, 16), (270, 15)):
        t = math.radians(sudut)
        ux, uy = math.cos(t), math.sin(t)
        nx, ny = -uy, ux
        for j in range(2, panjang):
            lengkung = (j / panjang) ** 2 * 9
            x = 19 + ux * j
            y = 27 + uy * j + lengkung
            xi, yi = round(x), round(y)
            if 0 <= xi < 38 and 0 <= yi < 32:
                d.point((xi, yi), fill=DAUN_TUA)
            for arah in (-1, 1):
                for k in (1, 2):
                    ax = round(x + nx * k * arah)
                    ay = round(y + ny * k * arah + k * 0.4)
                    if 0 <= ax < 38 and 0 <= ay < 32:
                        d.point((ax, ay), fill=DAUN_TERANG if k == 1 else DAUN)
    d.ellipse([15, 26, 23, 31], fill=(96, 70, 48, 255))
    return garis_luar(img, GARIS_ISO)


def prop_semak_bunga(seed=61):
    img, d = kanvas(34, 28)
    r = random.Random(seed)
    d.ellipse([1, 8, 32, 26], fill=DAUN_TUA)
    d.ellipse([4, 4, 28, 22], fill=DAUN)
    d.ellipse([8, 6, 22, 17], fill=DAUN_TERANG)
    for _ in range(14):
        x, y = r.randrange(4, 29), r.randrange(5, 23)
        if (x - 16) ** 2 / 160 + (y - 14) ** 2 / 90 > 1:
            continue
        w = r.choice(WARNA_BUNGA)
        d.rectangle([x, y, x + 1, y + 1], fill=w)
        d.point((x, y), fill=(252, 236, 160, 255))
    return garis_luar(img, GARIS_ISO)


def prop_rumpun_bunga(seed=62):
    img, d = kanvas(26, 20)
    r = random.Random(seed)
    for i in range(9):
        x = 3 + i * 2 + r.randrange(0, 2)
        tinggi = 6 + r.randrange(0, 6)
        d.line([(x, 18), (x, 18 - tinggi)], fill=DAUN)
        w = r.choice(WARNA_BUNGA)
        d.rectangle([x - 1, 17 - tinggi, x + 1, 18 - tinggi], fill=w)
        d.point((x, 18 - tinggi), fill=(252, 240, 170, 255))
    return garis_luar(img, GARIS_ISO)


# --------------------------------------------------------------------------
# Bangunan & perlengkapan
# --------------------------------------------------------------------------
def prop_pelaminan():
    """Pelaminan ukir dengan sepasang mempelai duduk di kursi singgasana."""
    img, d = kanvas(98, 86)

    # --- panggung kayu + karpet ---
    d.polygon([(6, 62), (91, 62), (83, 76), (14, 76)], fill=KAYU_TERANG)
    d.polygon([(6, 62), (91, 62), (91, 66), (6, 66)], fill=(206, 158, 100, 255))
    d.polygon([(14, 76), (83, 76), (83, 82), (14, 82)], fill=KAYU_TUA)
    d.polygon([(26, 62), (71, 62), (66, 76), (31, 76)], fill=MERAH)
    d.polygon([(26, 62), (71, 62), (70, 65), (27, 65)], fill=(206, 74, 80, 255))
    for x in range(30, 68, 6):
        d.point((x, 70), fill=EMAS)
    # anak tangga
    d.polygon([(34, 76), (63, 76), (60, 84), (37, 84)], fill=KAYU)
    d.line([(35, 80), (62, 80)], fill=KAYU_TUA)

    # --- latar ukir ---
    d.rectangle([14, 16, 83, 63], fill=KAYU_TUA)
    d.rectangle([17, 19, 80, 61], fill=KAYU)
    for x0 in (19, 62):
        d.rectangle([x0, 21, x0 + 16, 59], fill=KAYU_TERANG)
        for y in range(24, 57, 8):
            d.rectangle([x0 + 2, y, x0 + 14, y + 1], fill=EMAS)
            d.rectangle([x0 + 7, y + 2, x0 + 9, y + 4], fill=EMAS)
    d.rectangle([38, 21, 60, 59], fill=KREM)
    for y in range(25, 58, 7):
        for x in range(41, 59, 7):
            d.point((x, y), fill=(220, 206, 178, 255))
            d.point((x + 1, y + 1), fill=(220, 206, 178, 255))

    # --- mahkota gunungan ---
    d.rectangle([12, 10, 85, 18], fill=KAYU_TUA)
    d.rectangle([14, 12, 83, 16], fill=EMAS)
    for x in range(18, 82, 6):
        d.rectangle([x, 12, x + 1, 16], fill=KAYU_TUA)
    d.polygon([(49, 0), (38, 11), (60, 11)], fill=KAYU_TUA)
    d.polygon([(49, 2), (41, 11), (57, 11)], fill=EMAS)
    d.polygon([(49, 5), (45, 11), (53, 11)], fill=EMAS_TERANG)
    d.polygon([(12, 18), (2, 11), (6, 18)], fill=EMAS)
    d.polygon([(85, 18), (95, 11), (91, 18)], fill=EMAS)

    # --- untaian bunga di lengkung ---
    r = random.Random(21)
    for i in range(38, 61, 2):
        tinggi = 20 + int(math.sin((i - 38) / 22 * math.pi) * 8)
        d.line([(i, 19), (i, tinggi)], fill=DAUN)
        d.rectangle([i - 1, tinggi, i, tinggi + 1], fill=r.choice(
            [MELATI, (244, 154, 178, 255), (250, 214, 128, 255)]))
    for x0 in (30, 66):
        for y in range(22, 56, 4):
            d.rectangle([x0, y, x0 + 2, y + 2], fill=r.choice(
                [DAUN, MELATI, (244, 154, 178, 255)]))

    # --- dua kursi singgasana ---
    for cx in (40, 58):
        d.rectangle([cx - 7, 34, cx + 7, 58], fill=KAYU_TUA)
        d.rectangle([cx - 5, 36, cx + 5, 56], fill=EMAS)
        d.rectangle([cx - 4, 38, cx + 4, 46], fill=(198, 150, 74, 255))
        d.polygon([(cx - 7, 34), (cx, 28), (cx + 7, 34)], fill=EMAS)
        d.rectangle([cx - 8, 52, cx + 8, 56], fill=MERAH_TUA)

    return garis_luar(img, GARIS_ISO)


def prop_gapura():
    """Gapura bambu berhias janur kuning."""
    img, d = kanvas(84, 72)
    BAMBU = (198, 176, 96, 255)
    BAMBU_GELAP = (160, 140, 70, 255)
    JANUR = (232, 226, 108, 255)
    JANUR_TERANG = (250, 246, 160, 255)
    JANUR_GELAP = (188, 184, 74, 255)

    for x in (10, 66) :
        d.rectangle([x, 18, x + 8, 70], fill=BAMBU)
        d.rectangle([x, 18, x + 2, 70], fill=BAMBU_GELAP)
        for y in range(22, 70, 8):
            d.line([(x, y), (x + 8, y)], fill=BAMBU_GELAP)

    d.rectangle([6, 14, 78, 22], fill=BAMBU)
    d.rectangle([6, 20, 78, 22], fill=BAMBU_GELAP)

    # anyaman janur pada palang atas
    for x in range(8, 77, 3):
        d.line([(x, 12), (x, 22)], fill=JANUR if (x // 3) % 2 else JANUR_TERANG)
    # janur menjuntai
    for x in range(9, 76, 4):
        panjang = 8 + (x % 4) * 4
        d.line([(x, 22), (x, 22 + panjang)], fill=JANUR)
        d.point((x, 22 + panjang), fill=JANUR_TERANG)
        d.point((x + 1, 22 + panjang - 2), fill=JANUR_GELAP)
    # kipas janur di puncak tiang
    for x0, arah in ((14, -1), (74, 1)):
        for i in range(7):
            d.line([(x0, 16), (x0 + arah * (3 + i), 2 + i)],
                   fill=JANUR if i % 2 else JANUR_TERANG)
    # rangkaian bunga
    r = random.Random(44)
    for x in range(10, 76, 6):
        d.rectangle([x, 10, x + 2, 12], fill=r.choice(
            [(244, 154, 178, 255), MELATI, (250, 214, 128, 255)]))
    for x0 in (12, 68):
        for y in range(26, 62, 6):
            d.rectangle([x0, y, x0 + 3, y + 3], fill=r.choice([DAUN, MELATI, (244, 154, 178, 255)]))
    return garis_luar(img, GARIS_ISO)


def prop_umbul(warna, warna_gelap, seed=71):
    """Umbul-umbul: panji tinggi pada tiang bambu."""
    img, d = kanvas(18, 66)
    d.ellipse([4, 60, 14, 65], fill=(120, 96, 62, 255))
    d.rectangle([8, 4, 10, 63], fill=(198, 176, 96, 255))
    d.rectangle([8, 4, 8, 63], fill=(160, 140, 70, 255))
    d.rectangle([7, 0, 11, 5], fill=EMAS)
    d.polygon([(11, 6), (17, 6), (17, 40), (14, 47), (11, 40)], fill=warna)
    d.rectangle([11, 6, 17, 9], fill=EMAS)
    r = random.Random(seed)
    for y in range(12, 40, 6):
        d.line([(11, y), (17, y)], fill=warna_gelap)
        d.point((14, y + 2), fill=EMAS)
    d.point((14, 46), fill=EMAS_TERANG)
    return garis_luar(img, GARIS_ISO)


def prop_air_mancur():
    img, d = kanvas(44, 58)
    d.ellipse([2, 34, 42, 54], fill=BATU)
    d.ellipse([5, 36, 39, 52], fill=AIR)
    d.ellipse([8, 38, 36, 50], fill=AIR_TERANG)
    d.ellipse([15, 28, 29, 38], fill=BATU_TERANG)
    d.rectangle([20, 14, 24, 32], fill=BATU_TERANG)
    d.ellipse([14, 10, 30, 18], fill=BATU)
    for dx in (-9, -5, 5, 9):
        d.line([(22 + dx, 12), (round(22 + dx * 1.9), 34)], fill=AIR_TERANG)
        d.line([(22 + dx, 12), (round(22 + dx * 1.6), 26)], fill=(198, 236, 250, 255))
    d.rectangle([20, 0, 24, 12], fill=(198, 236, 250, 255))
    d.ellipse([18, 0, 26, 6], fill=(226, 246, 252, 255))
    r = random.Random(81)
    for _ in range(10):
        d.point((r.randrange(9, 36), r.randrange(39, 50)), fill=(206, 240, 252, 255))
    return garis_luar(img, GARIS_ISO)


def prop_jembatan():
    """Jembatan kayu melengkung menyeberangi kolam."""
    img, d = kanvas(76, 44)
    for i in range(70):
        x = 3 + i
        y = 26 - round(math.sin(i / 69 * math.pi) * 10)
        d.rectangle([x, y, x, y + 6], fill=KAYU_TERANG)
        if i % 5 == 0:
            d.rectangle([x, y, x, y + 6], fill=KAYU)
    for sisi in (0, 1):
        for i in range(70):
            x = 3 + i
            y = 26 - round(math.sin(i / 69 * math.pi) * 10) - (10 if sisi else 0)
            if sisi:
                d.point((x, y + 2), fill=KAYU)
        if sisi:
            for i in range(4, 70, 10):
                x = 3 + i
                y = 26 - round(math.sin(i / 69 * math.pi) * 10)
                d.rectangle([x, y - 10, x + 1, y], fill=KAYU)
    d.rectangle([1, 30, 6, 42], fill=KAYU_TUA)
    d.rectangle([70, 30, 75, 42], fill=KAYU_TUA)
    return garis_luar(img, GARIS_ISO)


def prop_batu_besar():
    img, d = kanvas(30, 22)
    d.ellipse([1, 6, 29, 21], fill=BATU_GELAP)
    d.ellipse([3, 4, 25, 18], fill=BATU)
    d.ellipse([7, 6, 18, 13], fill=BATU_TERANG)
    return garis_luar(img, GARIS_ISO)


def prop_teratai():
    img, d = kanvas(22, 14)
    d.ellipse([0, 3, 15, 13], fill=(46, 122, 64, 255))
    d.ellipse([2, 4, 13, 11], fill=(66, 152, 74, 255))
    d.polygon([(7, 8), (7, 4), (10, 8)], fill=(38, 102, 54, 255))
    d.ellipse([13, 0, 21, 8], fill=(246, 196, 214, 255))
    d.ellipse([15, 2, 19, 6], fill=(252, 238, 244, 255))
    d.point((17, 4), fill=(250, 214, 128, 255))
    return garis_luar(img, GARIS_ISO)


def prop_meja_tamu():
    """Meja buku tamu beratap kanopi kecil."""
    img, d = kanvas(52, 58)
    for x in (6, 44):
        d.rectangle([x, 18, x + 2, 52], fill=KAYU)
    d.polygon([(2, 18), (50, 18), (44, 6), (8, 6)], fill=MERAH)
    d.polygon([(2, 18), (50, 18), (50, 21), (2, 21)], fill=EMAS)
    for x in range(6, 47, 6):
        d.line([(x, 7), (x - 3, 18)], fill=MERAH_TUA)
    d.polygon([(8, 34), (44, 34), (48, 46), (4, 46)], fill=KREM)
    d.rectangle([4, 44, 48, 50], fill=(222, 208, 180, 255))
    for x in range(8, 45, 5):
        d.line([(x, 47), (x - 1, 50)], fill=(206, 192, 166, 255))
    d.polygon([(18, 30), (34, 30), (36, 35), (16, 35)], fill=(252, 250, 244, 255))
    d.line([(26, 30), (26, 35)], fill=(214, 206, 190, 255))
    d.line([(36, 24), (38, 30)], fill=MERAH)
    d.rectangle([10, 30, 14, 34], fill=(244, 154, 178, 255))
    d.rectangle([38, 31, 42, 35], fill=(250, 214, 128, 255))
    return garis_luar(img, GARIS_ISO)


def prop_kotak_angpao():
    img, d = kanvas(32, 34)
    d.polygon([(3, 12), (29, 12), (26, 30), (6, 30)], fill=KAYU_TERANG)
    d.polygon([(3, 12), (29, 12), (29, 16), (3, 16)], fill=KAYU)
    d.polygon([(6, 26), (26, 26), (26, 30), (6, 30)], fill=KAYU_TUA)
    for y in range(18, 27, 4):
        for x in range(7, 26, 4):
            d.point((x, y), fill=KAYU_TUA)
            d.point((x + 1, y + 1), fill=KAYU_TUA)
            d.point((x + 1, y), fill=EMAS)
    d.rectangle([3, 12, 29, 13], fill=EMAS)
    d.rectangle([10, 13, 22, 15], fill=(46, 36, 32, 255))
    d.polygon([(16, 4), (12, 11), (20, 11)], fill=EMAS)
    d.polygon([(16, 6), (14, 11), (18, 11)], fill=EMAS_TERANG)
    return garis_luar(img, GARIS_ISO)


def prop_papan_acara():
    img, d = kanvas(40, 48)
    d.rectangle([17, 26, 22, 46], fill=KAYU)
    d.rectangle([17, 26, 18, 46], fill=KAYU_TUA)
    d.rectangle([2, 2, 37, 28], fill=KAYU_TUA)
    d.rectangle([4, 4, 35, 26], fill=KAYU_TERANG)
    d.rectangle([6, 6, 33, 24], fill=KREM)
    d.rectangle([8, 8, 31, 11], fill=MERAH)
    for y in (14, 17, 20):
        d.line([(9, y), (30, y)], fill=(196, 182, 156, 255))
    for x, y in ((3, 3), (36, 3), (3, 27), (36, 27)):
        d.point((x, y), fill=EMAS)
    d.ellipse([12, 44, 27, 48], fill=DAUN_TUA)
    return garis_luar(img, GARIS_ISO)


def prop_galeri():
    img, d = kanvas(44, 52)
    d.line([(9, 50), (19, 20)], fill=KAYU, width=3)
    d.line([(35, 50), (25, 20)], fill=KAYU, width=3)
    d.line([(22, 30), (22, 50)], fill=KAYU_TUA, width=3)
    d.line([(12, 42), (32, 42)], fill=KAYU, width=2)
    d.rectangle([4, 2, 40, 34], fill=EMAS)
    d.rectangle([6, 4, 38, 32], fill=(190, 148, 74, 255))
    d.rectangle([8, 6, 36, 30], fill=(250, 246, 238, 255))
    d.rectangle([8, 6, 36, 12], fill=(198, 224, 240, 255))
    d.rectangle([13, 16, 20, 29], fill=(238, 230, 210, 255))
    d.ellipse([13, 11, 20, 18], fill=(238, 200, 166, 255))
    d.rectangle([13, 10, 20, 13], fill=(104, 72, 48, 255))
    d.polygon([(24, 29), (31, 29), (32, 17), (23, 17)], fill=(250, 246, 238, 255))
    d.ellipse([24, 11, 31, 18], fill=(244, 208, 176, 255))
    d.ellipse([24, 9, 32, 15], fill=(52, 40, 36, 255))
    return garis_luar(img, GARIS_ISO)


def prop_pagar_bambu():
    img, d = kanvas(46, 40)
    BAMBU = (198, 176, 96, 255)
    BAMBU_GELAP = (160, 140, 70, 255)
    for x in range(2, 45, 7):
        d.rectangle([x, 10, x + 3, 38], fill=BAMBU)
        d.rectangle([x, 10, x, 38], fill=BAMBU_GELAP)
        d.point((x + 1, 9), fill=BAMBU_GELAP)
    for y in (16, 28):
        d.rectangle([0, y, 45, y + 2], fill=BAMBU)
        d.line([(0, y + 2), (45, y + 2)], fill=BAMBU_GELAP)
    r = random.Random(91)
    for x in range(4, 44, 9):
        d.rectangle([x, 6, x + 3, 9], fill=r.choice([(244, 154, 178, 255), MELATI]))
        d.point((x + 1, 10), fill=DAUN)
    return garis_luar(img, GARIS_ISO)


def prop_ember():
    img, d = kanvas(18, 18)
    d.polygon([(3, 6), (15, 6), (13, 16), (5, 16)], fill=KAYU_TERANG)
    d.rectangle([2, 5, 16, 7], fill=KAYU)
    d.line([(4, 11), (14, 11)], fill=KAYU_TUA)
    d.arc([4, 0, 14, 8], 180, 360, fill=(120, 110, 100, 255), width=1)
    return garis_luar(img, GARIS_ISO)


PROPERTI = {
    "pelaminan": prop_pelaminan,
    "gapura": prop_gapura,
    "umbul_merah": lambda: prop_umbul((214, 56, 62, 255), (168, 40, 46, 255), 71),
    "umbul_kuning": lambda: prop_umbul((248, 200, 62, 255), (206, 160, 42, 255), 72),
    "umbul_biru": lambda: prop_umbul((62, 130, 210, 255), (44, 100, 172, 255), 73),
    "umbul_hijau": lambda: prop_umbul((80, 176, 96, 255), (56, 140, 74, 255), 74),
    "palem": prop_palem,
    "pisang": prop_pisang,
    "pakis": prop_pakis,
    "semak_bunga": prop_semak_bunga,
    "rumpun_bunga": prop_rumpun_bunga,
    "air_mancur": prop_air_mancur,
    "jembatan": prop_jembatan,
    "batu_besar": prop_batu_besar,
    "teratai": prop_teratai,
    "meja_tamu": prop_meja_tamu,
    "kotak_angpao": prop_kotak_angpao,
    "papan_acara": prop_papan_acara,
    "galeri": prop_galeri,
    "pagar_bambu": prop_pagar_bambu,
    "ember": prop_ember,
}


def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    nama_petak = buat_tileset()
    # Karakter dan mempelai TIDAK dibuat di sini. Berkas ini menggambar
    # bingkai 44x76, sedangkan ketiga mesin permainan memotong lembar sprite
    # per 48x80. Menjalankannya dulu membuat potongan bingkai meleset satu
    # sama lain sehingga karakter tampak cacat. Sumber tunggal karakter untuk
    # SEMUA tema sekarang tools/buat_karakter_stardew.py.
    for nama, fungsi in PROPERTI.items():
        perbesar(fungsi()).save(KELUARAN / f"{nama}.png")
    print("Petak    :", ", ".join(f"{i}={n}" for i, n in enumerate(nama_petak)))
    print("Karakter : dilewati - lihat tools/buat_karakter_stardew.py")
    print("Properti :", ", ".join(PROPERTI))
    print("Tersimpan di", KELUARAN)


if __name__ == "__main__":
    main()
