"""Generator Aset Pixel Art Lengkap untuk Tema "Desa Asri Parahyangan" (Gaya Stardew Valley).

Menghasilkan seluruh aset pixel art bertema pedesaan Indonesia berkualitas tinggi:
- tileset.png (48x48 tileable: rumput bunga liar, jalan tanah gembur, cobblestone, dek kayu, air sungai riak, sawah terasering, kebun sayur, pagar kayu, rimba)
- tepi.png (transisi rumput)
- pelaminan.png (Saung gazebo kayu rustic pesta kebun dengan ronce melati)
- papan.png (Notice board kayu ala Stardew Community Board)
- galeri.png (Jemuran foto tali rami di antara dua pohon buah)
- buku_tamu.png (Meja jamuan kebun panjang dengan tumpeng nasi kuning)
- hadiah.png (Peti kayu shipping box Stardew dengan ornamen kuningan)
- gerbang.png (Gapura kayu bambu rustic berhias bunga)
- pohon_buah.png (Pohon buah lebat pixel art khas Stardew)
- saung_lumbung.png (Lumbung padi kayu atap sirap pedesaan)
- ayam.png & kucing.png (Sprite hewan pedesaan yang hidup)
- karakter_pria.png & karakter_wanita.png (Sprite sheet 48x80 4 arah 4 frame gaya Stardew berbusana Sunda)
- pengantin_pria.png & pengantin_wanita.png (Pengantin duduk bersanding)
"""

import math
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game_desa"
UKURAN_PETAK = 48

# Helper warna RGBA
def _w(r, g, b, a=255):
    return (r, g, b, a)

# ==============================================================================
# PALET WARNA STARDEW VALLEY x NUSANTARA
# ==============================================================================
# Alam & Tanah
RUMPUT_KILAU = _w(176, 224, 98)
RUMPUT_TERANG = _w(134, 196, 72)
RUMPUT_DASAR = _w(102, 168, 54)
RUMPUT_BAYANG = _w(72, 134, 40)
RUMPUT_PEKAT = _w(48, 96, 30)

TANAH_TERANG = _w(194, 146, 96)
TANAH_DASAR = _w(156, 110, 68)
TANAH_BAYANG = _w(120, 80, 48)
TANAH_PEKAT = _w(86, 54, 32)
TANAH_GEMBUR = _w(108, 72, 44)

BATU_KILAU = _w(216, 214, 204)
BATU_TERANG = _w(182, 178, 168)
BATU_DASAR = _w(148, 144, 136)
BATU_BAYANG = _w(112, 108, 102)
BATU_PEKAT = _w(76, 72, 68)

KAYU_MADU_TERANG = _w(228, 172, 94)
KAYU_MADU = _w(188, 132, 64)
KAYU_MADU_BAYANG = _w(146, 96, 42)
KAYU_MADU_PEKAT = _w(98, 60, 26)

AIR_KILAU = _w(184, 238, 252)
AIR_TERANG = _w(118, 206, 238)
AIR_DASAR = _w(64, 168, 214)
AIR_BAYANG = _w(42, 130, 182)
AIR_PEKAT = _w(28, 92, 138)

EMAS_KILAU = _w(255, 248, 170)
EMAS_TERANG = _w(248, 214, 82)
EMAS_DASAR = _w(218, 168, 42)
EMAS_BAYANG = _w(164, 118, 26)

MELATI_PUTIH = _w(255, 255, 250)
MELATI_KUNING = _w(255, 228, 112)

BUNGA_WARNA = [
    _w(248, 104, 112), # Mawar merah
    _w(255, 178, 74),  # Marigold jingga
    _w(254, 226, 90),  # Krisan kuning
    _w(242, 136, 186), # Anggrek pink
    _w(176, 130, 230), # Lavender lembah
    _w(255, 255, 248), # Melati liar
]

GARIS_LUAR = _w(44, 32, 28)

def kanvas(w, h, latar=(0, 0, 0, 0)):
    img = Image.new("RGBA", (w, h), latar)
    return img, ImageDraw.Draw(img)

def garis_luar(img, warna=GARIS_LUAR):
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
                if 0 <= nx < w and 0 <= ny < h and sumber[nx, ny][3] > 40:
                    tujuan[x, y] = warna
                    break
    return hasil

def _geser(xy, dx, dy):
    if isinstance(xy, (list, tuple)) and xy and isinstance(xy[0], (list, tuple)):
        return [(x + dx, y + dy) for x, y in xy]
    nilai = list(xy)
    return [n + (dx if i % 2 == 0 else dy) for i, n in enumerate(nilai)]

class KanvasBungkus:
    """Menggambar 9x agar tile dijamin seamless / tileable."""
    def __init__(self, d, ukuran=UKURAN_PETAK):
        self._d = d
        self._u = ukuran
    def __getattr__(self, nama):
        f = getattr(self._d, nama)
        def bungkus(xy, *args, **kwargs):
            for by in range(3):
                for bx in range(3):
                    f(_geser(xy, bx * self._u, by * self._u), *args, **kwargs)
        return bungkus

def buat_petak_tileable(fungsi_gambar, warna_dasar):
    lebar_tiga = UKURAN_PETAK * 3
    img = Image.new("RGBA", (lebar_tiga, lebar_tiga), warna_dasar)
    d = ImageDraw.Draw(img)
    bungkus = KanvasBungkus(d, UKURAN_PETAK)
    fungsi_gambar(bungkus)
    return img.crop((UKURAN_PETAK, UKURAN_PETAK, UKURAN_PETAK * 2, UKURAN_PETAK * 2))

# ==============================================================================
# TILESET GENERATION (48x48)
# ==============================================================================
def tile_rumput(seed=12, bunga=True):
    def draw(d):
        r = random.Random(seed)
        for _ in range(25):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(6, 14), y + r.randint(4, 8)], fill=RUMPUT_BAYANG)
        for _ in range(20):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(5, 12), y + r.randint(3, 7)], fill=RUMPUT_TERANG)
        for _ in range(30):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.line([(x, y + 4), (x - 1, y)], fill=RUMPUT_TERANG)
            d.line([(x + 1, y + 4), (x + 2, y + 1)], fill=RUMPUT_KILAU)
        if bunga:
            for _ in range(8):
                x, y = r.randrange(4, UKURAN_PETAK - 4), r.randrange(4, UKURAN_PETAK - 4)
                warna_b = r.choice(BUNGA_WARNA)
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=warna_b)
                d.point((x, y), fill=EMAS_KILAU)
                d.point((x, y + 3), fill=RUMPUT_PEKAT)
    return buat_petak_tileable(draw, RUMPUT_DASAR)

def tile_tanah(seed=24):
    def draw(d):
        r = random.Random(seed)
        for _ in range(20):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(8, 16), y + r.randint(4, 9)], fill=TANAH_BAYANG)
        for _ in range(16):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(6, 12), y + r.randint(3, 7)], fill=TANAH_TERANG)
        # Butiran kerikil
        for _ in range(24):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.point((x, y), fill=BATU_DASAR)
            d.point((x, y + 1), fill=TANAH_PEKAT)
    return buat_petak_tileable(draw, TANAH_DASAR)

def tile_kebun_gembur(seed=35):
    """Petak tanah gembur bajakan sawah / bedeng sayur ala Stardew."""
    def draw(d):
        r = random.Random(seed)
        # Alur bajakan horisontal
        for y in range(0, UKURAN_PETAK, 12):
            d.rectangle([0, y, UKURAN_PETAK, y + 5], fill=TANAH_PEKAT)
            d.rectangle([0, y + 6, UKURAN_PETAK, y + 10], fill=TANAH_GEMBUR)
            d.line([(0, y + 6), (UKURAN_PETAK, y + 6)], fill=TANAH_TERANG)
        # Tanaman sayur / bibit cabe kecil
        for y in range(4, UKURAN_PETAK, 12):
            for x in range(6, UKURAN_PETAK, 16):
                d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=RUMPUT_TERANG)
                d.point((x, y - 1), fill=RUMPUT_KILAU)
                if (x + y) % 3 == 0:
                    d.point((x + 1, y), fill=_w(238, 48, 54))  # Cabai / tomat kecil
    return buat_petak_tileable(draw, TANAH_GEMBUR)

def tile_batu_kali(seed=46):
    """Jalan cobblestone batu kali pedesaan."""
    def draw(d):
        r = random.Random(seed)
        # Latar tanah di sela batu
        for by in range(0, UKURAN_PETAK, 12):
            for bx in range(0, UKURAN_PETAK, 12):
                x = bx + r.randint(-2, 2)
                y = by + r.randint(-2, 2)
                w = r.randint(9, 13)
                h = r.randint(8, 11)
                d.ellipse([x, y + 1, x + w, y + h + 1], fill=BATU_PEKAT)
                d.ellipse([x, y, x + w, y + h], fill=BATU_DASAR)
                d.ellipse([x + 2, y + 1, x + w - 2, y + h - 3], fill=BATU_TERANG)
                d.point((x + 3, y + 2), fill=BATU_KILAU)
        # Lumut tipis
        for _ in range(12):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.point((x, y), fill=RUMPUT_BAYANG)
    return buat_petak_tileable(draw, TANAH_DASAR)

def tile_kayu_papan(seed=58):
    """Panggung papan kayu jembatan rustic."""
    def draw(d):
        r = random.Random(seed)
        for y in range(0, UKURAN_PETAK, 12):
            d.rectangle([0, y, UKURAN_PETAK, y + 10], fill=KAYU_MADU)
            d.line([(0, y), (UKURAN_PETAK, y)], fill=KAYU_MADU_TERANG)
            d.line([(0, y + 11), (UKURAN_PETAK, y + 11)], fill=KAYU_MADU_PEKAT)
            # Paku kayu dan serat
            for x in (6, UKURAN_PETAK - 6):
                d.point((x, y + 3), fill=BATU_PEKAT)
                d.point((x, y + 4), fill=BATU_TERANG)
            d.line([(12, y + 5), (32, y + 5)], fill=KAYU_MADU_BAYANG)
    return buat_petak_tileable(draw, KAYU_MADU_BAYANG)

def tile_air_sungai(seed=61, fase=0):
    """Air sungai jernih beriak lembut khas lembah gunung."""
    def draw(d):
        r = random.Random(seed)
        for _ in range(15):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(12, 24), y + r.randint(5, 10)], fill=AIR_BAYANG)
        # Riak air animasi
        shift = (fase * 16) % UKURAN_PETAK
        for baris in range(6, UKURAN_PETAK, 16):
            y = baris
            d.arc([shift, y, shift + 20, y + 8], 0, 180, fill=AIR_KILAU, width=2)
            d.arc([shift + 22, y + 2, shift + 40, y + 9], 0, 180, fill=AIR_TERANG, width=1)
        # Batu bulat di dasar air
        for bx, by in ((10, 14), (32, 36)):
            d.ellipse([bx, by, bx + 8, by + 6], fill=_w(80, 130, 140))
    return buat_petak_tileable(draw, AIR_DASAR)

def tile_sawah(seed=72):
    """Petak sawah berundak dengan bibit padi muda."""
    def draw(d):
        r = random.Random(seed)
        # Air genangan sawah tenang
        d.rectangle([0, 0, UKURAN_PETAK, UKURAN_PETAK], fill=_w(94, 162, 134))
        # Rumpun bibit padi hijau
        for y in range(6, UKURAN_PETAK, 16):
            for x in range(8, UKURAN_PETAK, 16):
                # Rumpun 3 daun padi
                d.line([(x, y + 6), (x - 3, y - 2)], fill=RUMPUT_KILAU, width=2)
                d.line([(x, y + 6), (x, y - 4)], fill=RUMPUT_TERANG, width=2)
                d.line([(x, y + 6), (x + 3, y - 2)], fill=RUMPUT_KILAU, width=2)
                # Bayangan di air
                d.ellipse([x - 4, y + 5, x + 4, y + 8], fill=_w(62, 120, 98, 180))
    return buat_petak_tileable(draw, _w(94, 162, 134))

def tile_rimba(seed=83):
    """Petak semak hutan pembatas peta."""
    def draw(d):
        r = random.Random(seed)
        for _ in range(40):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(10, 22), y + r.randint(8, 18)], fill=RUMPUT_PEKAT)
        for _ in range(25):
            x, y = r.randrange(0, UKURAN_PETAK), r.randrange(0, UKURAN_PETAK)
            d.ellipse([x, y, x + r.randint(6, 14), y + r.randint(5, 11)], fill=RUMPUT_BAYANG)
    return buat_petak_tileable(draw, _w(32, 68, 22))

def tile_pagar():
    """Petak pagar kayu rustic peternakan."""
    img = tile_rumput(12, bunga=False)
    d = ImageDraw.Draw(img)
    # Tiang pagar kayu
    for x in (8, 28):
        d.rectangle([x, 10, x + 8, 44], fill=KAYU_MADU)
        d.line([(x, 10), (x, 44)], fill=KAYU_MADU_TERANG)
        d.line([(x + 8, 10), (x + 8, 44)], fill=KAYU_MADU_PEKAT)
        # Puncak runcing
        d.polygon([(x, 10), (x + 4, 4), (x + 8, 10)], fill=KAYU_MADU_TERANG)
    # Palang pagar horisontal
    for y in (16, 30):
        d.rectangle([0, y, UKURAN_PETAK, y + 6], fill=KAYU_MADU)
        d.line([(0, y), (UKURAN_PETAK, y)], fill=KAYU_MADU_TERANG)
        d.line([(0, y + 6), (UKURAN_PETAK, y + 6)], fill=KAYU_MADU_PEKAT)
    return img

URUTAN_TILES = [
    ("rumput", lambda: tile_rumput(11, bunga=True)),      # 0
    ("rumput_2", lambda: tile_rumput(22, bunga=False)),   # 1
    ("rumput_3", lambda: tile_rumput(33, bunga=True)),    # 2
    ("tanah", tile_tanah),                                # 3
    ("batu_kali", tile_batu_kali),                        # 4
    ("kayu_papan", tile_kayu_papan),                      # 5
    ("kebun_gembur", tile_kebun_gembur),                  # 6
    ("air_1", lambda: tile_air_sungai(61, 0)),            # 7
    ("air_2", lambda: tile_air_sungai(61, 1)),            # 8
    ("air_3", lambda: tile_air_sungai(61, 2)),            # 9
    ("sawah", tile_sawah),                                # 10
    ("rimba", tile_rimba),                                # 11
    ("pagar", tile_pagar),                                # 12
]

def buat_tileset():
    petakan = [fn() for _, fn in URUTAN_TILES]
    lembar = Image.new("RGBA", (UKURAN_PETAK * len(petakan), UKURAN_PETAK), (0, 0, 0, 0))
    for i, t in enumerate(petakan):
        lembar.paste(t, (i * UKURAN_PETAK, 0))
    lembar.save(KELUARAN / "tileset.png")
    return [n for n, _ in URUTAN_TILES]

# Tepi Rumput (Autotiles)
def buat_tepi():
    """Transisi tepi rumput ke tanah (8 sisi/sudut)."""
    rumput = tile_rumput(15, bunga=False)
    daftar = []
    # 4 Sisi: atas, bawah, kiri, kanan
    for arah in ("atas", "bawah", "kiri", "kanan"):
        m = Image.new("L", (UKURAN_PETAK, UKURAN_PETAK), 0)
        dm = ImageDraw.Draw(m)
        tebal = 14
        if arah == "atas": dm.rectangle([0, 0, UKURAN_PETAK, tebal], fill=255)
        elif arah == "bawah": dm.rectangle([0, UKURAN_PETAK - tebal, UKURAN_PETAK, UKURAN_PETAK], fill=255)
        elif arah == "kiri": dm.rectangle([0, 0, tebal, UKURAN_PETAK], fill=255)
        elif arah == "kanan": dm.rectangle([UKURAN_PETAK - tebal, 0, UKURAN_PETAK, UKURAN_PETAK], fill=255)
        hasil = Image.new("RGBA", (UKURAN_PETAK, UKURAN_PETAK), (0, 0, 0, 0))
        hasil.paste(rumput, (0, 0), m)
        daftar.append(hasil)
    # 4 Sudut: kiri_atas, kanan_atas, kiri_bawah, kanan_bawah
    for sudut in ("kiri_atas", "kanan_atas", "kiri_bawah", "kanan_bawah"):
        m = Image.new("L", (UKURAN_PETAK, UKURAN_PETAK), 0)
        dm = ImageDraw.Draw(m)
        r = 16
        if sudut == "kiri_atas": dm.ellipse([-r, -r, r, r], fill=255)
        elif sudut == "kanan_atas": dm.ellipse([UKURAN_PETAK - r, -r, UKURAN_PETAK + r, r], fill=255)
        elif sudut == "kiri_bawah": dm.ellipse([-r, UKURAN_PETAK - r, r, UKURAN_PETAK + r], fill=255)
        elif sudut == "kanan_bawah": dm.ellipse([UKURAN_PETAK - r, UKURAN_PETAK - r, UKURAN_PETAK + r, UKURAN_PETAK + r], fill=255)
        hasil = Image.new("RGBA", (UKURAN_PETAK, UKURAN_PETAK), (0, 0, 0, 0))
        hasil.paste(rumput, (0, 0), m)
        daftar.append(hasil)

    lembar = Image.new("RGBA", (UKURAN_PETAK * len(daftar), UKURAN_PETAK), (0, 0, 0, 0))
    for i, t in enumerate(daftar):
        lembar.paste(t, (i * UKURAN_PETAK, 0))
    lembar.save(KELUARAN / "tepi.png")

# ==============================================================================
# PROPERTI PERNIKAHAN & LINGKUNGAN DESA ASRI
# ==============================================================================
def prop_pelaminan():
    """Saung gazebo kayu rustic terbuka dengan ronce melati dan sulur bunga."""
    w, h = 136, 124
    img, d = kanvas(w, h)
    # Lantai panggung kayu
    d.polygon([(14, 88), (122, 88), (134, 116), (2, 116)], fill=KAYU_MADU)
    d.line([(2, 116), (134, 116)], fill=KAYU_MADU_PEKAT, width=2)
    # Karpet tenun merah marun di tengah
    d.polygon([(42, 90), (94, 90), (102, 116), (34, 116)], fill=_w(168, 48, 54))
    d.line([(42, 90), (94, 90)], fill=EMAS_TERANG, width=2)
    d.line([(34, 116), (102, 116)], fill=EMAS_TERANG, width=2)
    # Tiang gazebo kayu 4 pilar
    for x in (16, 44, 90, 118):
        d.rectangle([x, 26, x + 6, 94], fill=KAYU_MADU)
        d.line([(x, 26), (x, 94)], fill=KAYU_MADU_TERANG)
        d.line([(x + 6, 26), (x + 6, 94)], fill=KAYU_MADU_PEKAT)
        # Sulur tanaman merambat & melati di tiang
        for y in range(32, 90, 8):
            d.ellipse([x - 2, y, x + 3, y + 4], fill=RUMPUT_TERANG)
            d.point((x + 4, y + 2), fill=MELATI_PUTIH)
    # Atap sirap kayu julang ngapak khas Parahyangan
    d.polygon([(68, 4), (134, 34), (130, 42), (68, 16), (6, 42), (2, 34)], fill=KAYU_MADU_PEKAT)
    d.polygon([(68, 8), (128, 36), (8, 36)], fill=KAYU_MADU)
    d.line([(68, 4), (134, 34)], fill=KAYU_MADU_TERANG, width=2)
    d.line([(68, 4), (2, 34)], fill=KAYU_MADU_TERANG, width=2)
    # Tirai kain putih tipis melengkung
    for kx, arah in ((20, 1), (116, -1)):
        d.arc([kx - 8, 34, kx + 24, 76], 180, 360, fill=_w(250, 248, 240, 210), width=3)
    # Ronce melati menjuntai di bawah atap
    for x in range(24, 114, 6):
        panjang = 10 + int(math.sin(x * 0.1) * 6)
        for y in range(36, 36 + panjang, 3):
            d.point((x, y), fill=MELATI_PUTIH)
            d.point((x + 1, y), fill=MELATI_KUNING)
    # Kursi pelaminan kayu kembar dengan bantalan krem gading
    for cx in (46, 76):
        d.rectangle([cx, 74, cx + 14, 94], fill=KAYU_MADU_PEKAT)
        d.rectangle([cx + 2, 72, cx + 12, 86], fill=_w(248, 244, 230))
        d.rectangle([cx + 1, 84, cx + 13, 90], fill=EMAS_TERANG)
    # Bunga pot besar di sisi kanan dan kiri pelaminan
    for bx in (6, 122):
        d.ellipse([bx, 88, bx + 10, 102], fill=TANAH_PEKAT)
        for _ in range(6):
            d.ellipse([bx - 2, 80, bx + 12, 92], fill=RUMPUT_TERANG)
            d.point((bx + 4, 84), fill=_w(255, 120, 140))
            d.point((bx + 7, 86), fill=MELATI_PUTIH)
    return garis_luar(img)

def prop_papan():
    """Stardew Valley Community Bulletin Board bertema pengumuman desa."""
    w, h = 56, 68
    img, d = kanvas(w, h)
    # Dua kaki kayu tancap
    for x in (12, 40):
        d.rectangle([x, 34, x + 5, 64], fill=KAYU_MADU_PEKAT)
        d.line([(x, 34), (x, 64)], fill=KAYU_MADU)
    # Atap pelindung kayu miring
    d.polygon([(4, 12), (28, 4), (52, 12), (48, 16), (28, 8), (8, 16)], fill=KAYU_MADU_PEKAT)
    d.line([(4, 12), (28, 4), (52, 12)], fill=KAYU_MADU_TERANG, width=2)
    # Papan pengumuman kayu utama
    d.rectangle([6, 14, 50, 44], fill=KAYU_MADU_PEKAT)
    d.rectangle([8, 16, 48, 42], fill=KAYU_MADU)
    # Kertas-kertas pengumuman tertempel (Notes pinned)
    # Kertas 1: Jadwal Akad (Krem)
    d.rectangle([11, 19, 26, 32], fill=_w(252, 248, 232))
    d.point((18, 20), fill=_w(220, 60, 60)) # Pin merah
    for ly in (23, 26, 29):
        d.line([(13, ly), (24, ly)], fill=_w(160, 140, 120))
    # Kertas 2: Resepsi & Denah (Kuning pastel)
    d.rectangle([29, 21, 45, 36], fill=_w(254, 246, 186))
    d.point((37, 22), fill=_w(50, 140, 210)) # Pin biru
    for ly in (25, 28, 31, 34):
        d.line([(31, ly), (43, ly)], fill=_w(160, 140, 110))
    # Ornamen pita daun di sudut papan
    d.ellipse([5, 12, 11, 18], fill=RUMPUT_TERANG)
    d.point((8, 15), fill=MELATI_PUTIH)
    return garis_luar(img)

def prop_galeri():
    """Jemuran tali rami berpenjepit kayu memajang foto polaroid di antara dua pohon buah."""
    w, h = 96, 76
    img, d = kanvas(w, h)
    # Batang pohon rindang di kiri dan kanan
    for px in (6, 82):
        d.rectangle([px + 2, 26, px + 7, 72], fill=KAYU_MADU_PEKAT)
        d.ellipse([px - 8, 4, px + 18, 38], fill=RUMPUT_BAYANG)
        d.ellipse([px - 6, 2, px + 16, 34], fill=RUMPUT_TERANG)
        # Buah apel merah kecil di pohon
        d.point((px, 16), fill=_w(238, 50, 60))
        d.point((px + 6, 22), fill=_w(238, 50, 60))
    # Tali rami melengkung (clothesline)
    d.arc([12, 24, 84, 44], 0, 180, fill=TANAH_TERANG, width=2)
    # Tiga foto polaroid tergantung dengan penjepit kayu
    pos_foto = [(22, 34), (44, 37), (66, 34)]
    for fx, fy in pos_foto:
        # Penjepit kayu kecil
        d.line([(fx + 4, fy - 3), (fx + 4, fy)], fill=KAYU_MADU_PEKAT, width=2)
        # Bingkai foto polaroid
        d.rectangle([fx, fy, fx + 15, fy + 20], fill=_w(254, 252, 246))
        d.rectangle([fx + 2, fy + 2, fx + 13, fy + 14], fill=_w(176, 214, 238))
        # Siluet pasangan mempelai kecil di foto
        d.ellipse([fx + 4, fy + 4, fx + 7, fy + 8], fill=KAYU_MADU_PEKAT)
        d.ellipse([fx + 8, fy + 5, fx + 11, fy + 9], fill=_w(238, 120, 140))
        d.rectangle([fx + 3, fy + 9, fx + 12, fy + 13], fill=_w(248, 244, 230))
    return garis_luar(img)

def prop_buku_tamu():
    """Meja jamuan kebun panjang dengan tumpeng nasi kuning dan buku tamu."""
    w, h = 88, 64
    img, d = kanvas(w, h)
    # 4 Kaki meja kayu
    for kx in (10, 24, 62, 76):
        d.rectangle([kx, 34, kx + 4, 58], fill=KAYU_MADU_PEKAT)
    # Papan meja panjang kayu
    d.polygon([(6, 24), (82, 24), (86, 36), (2, 36)], fill=KAYU_MADU)
    d.line([(2, 36), (86, 36)], fill=KAYU_MADU_PEKAT, width=2)
    # Taplak meja motif kotak merah putih di tengah
    d.polygon([(26, 24), (62, 24), (64, 40), (24, 40)], fill=_w(246, 244, 240))
    for tx in range(26, 62, 6):
        d.line([(tx, 24), (tx, 40)], fill=_w(220, 64, 68))
    # Tumpeng Nasi Kuning di atas daun pisang
    d.ellipse([36, 24, 52, 32], fill=_w(78, 156, 64)) # Daun pisang alas
    d.polygon([(44, 10), (38, 26), (50, 26)], fill=EMAS_TERANG) # Kerucut nasi kuning
    d.point((44, 8), fill=_w(238, 48, 48)) # Cabe hias pucuk
    # Lauk pauk di keliling tumpeng (ayam goreng, telur dadar, mentimun)
    d.point((40, 24), fill=TANAH_PEKAT)
    d.point((48, 24), fill=_w(248, 214, 82))
    d.point((44, 25), fill=_w(120, 194, 96))
    # Buku Tamu terbuka di sisi kiri
    d.polygon([(10, 26), (22, 26), (23, 33), (9, 33)], fill=_w(252, 250, 242))
    d.line([(16, 26), (16, 33)], fill=TANAH_BAYANG) # Punggung buku
    d.point((24, 28), fill=EMAS_TERANG) # Pena bulu
    # Vas bunga liar kecil di sisi kanan
    d.rectangle([70, 22, 76, 28], fill=BATU_TERANG)
    d.ellipse([68, 14, 78, 22], fill=RUMPUT_TERANG)
    d.point((73, 16), fill=_w(254, 140, 180))
    d.point((71, 18), fill=MELATI_PUTIH)
    return garis_luar(img)

def prop_hadiah():
    """Peti kayu ukir kuningan ala Stardew Valley Shipping Box."""
    w, h = 48, 44
    img, d = kanvas(w, h)
    # Badan peti kayu kokoh
    d.rectangle([4, 14, 44, 40], fill=KAYU_MADU)
    d.rectangle([4, 14, 44, 18], fill=KAYU_MADU_TERANG)
    d.line([(4, 40), (44, 40)], fill=KAYU_MADU_PEKAT, width=2)
    # Behel bingkai besi kuningan / emas di sudut-sudut
    for bx in (4, 41):
        d.rectangle([bx, 14, bx + 3, 40], fill=EMAS_DASAR)
        d.line([(bx, 14), (bx, 40)], fill=EMAS_KILAU)
    for by in (14, 37):
        d.rectangle([4, by, 44, by + 3], fill=EMAS_DASAR)
    # Kunci gembok kuningan & lubang koin emas
    d.rectangle([21, 22, 27, 28], fill=EMAS_KILAU)
    d.point((24, 25), fill=BATU_PEKAT)
    # Celengan slot amplop di tutup peti
    d.rectangle([16, 15, 32, 17], fill=BATU_PEKAT)
    # Pita ornamen pernikahan di atas peti
    d.polygon([(24, 8), (18, 14), (30, 14)], fill=_w(228, 54, 64))
    d.point((24, 11), fill=EMAS_KILAU)
    return garis_luar(img)

def prop_gerbang():
    """Gapura kayu bambu rustic berhias bunga melati dan janur lengkung."""
    w, h = 96, 92
    img, d = kanvas(w, h)
    # Tiang bambu ganda kiri dan kanan
    for x in (12, 18, 72, 78):
        d.rectangle([x, 24, x + 4, 88], fill=KAYU_MADU)
        d.line([(x, 24), (x, 88)], fill=KAYU_MADU_TERANG)
    # Palang lengkung bambu atas
    d.arc([14, 8, 80, 48], 180, 360, fill=KAYU_MADU, width=5)
    d.arc([14, 8, 80, 48], 180, 360, fill=KAYU_MADU_TERANG, width=2)
    # Hiasan janur kuning & bunga matahari di lengkungan
    for x in range(22, 74, 8):
        y = 20 - int(math.sin((x - 22) / 52 * math.pi) * 12)
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=EMAS_TERANG)
        d.point((x, y), fill=TANAH_PEKAT)
    # Lentera gantung pedesaan di kanan kiri gapura
    for lx in (22, 70):
        d.line([(lx, 26), (lx, 36)], fill=BATU_PEKAT)
        d.rectangle([lx - 3, 36, lx + 3, 44], fill=EMAS_KILAU)
        d.point((lx, 40), fill=_w(255, 248, 180)) # Bohlam hangat
    return garis_luar(img)

def prop_pohon_buah():
    """Pohon buah apel/rambutan lebat bergaya pixel art Stardew Valley."""
    w, h = 76, 94
    img, d = kanvas(w, h)
    # Batang pohon bercabang
    d.rectangle([34, 46, 42, 90], fill=KAYU_MADU_PEKAT)
    d.line([(34, 46), (34, 90)], fill=KAYU_MADU)
    d.polygon([(34, 52), (24, 40), (28, 38), (36, 48)], fill=KAYU_MADU_PEKAT)
    d.polygon([(42, 54), (52, 42), (48, 39), (40, 50)], fill=KAYU_MADU_PEKAT)
    # Kanopi daun lebat bulat bertingkat khas Stardew
    gumpalan = [
        (38, 26, 32, 24, RUMPUT_BAYANG),
        (24, 34, 22, 18, RUMPUT_DASAR),
        (52, 34, 22, 18, RUMPUT_DASAR),
        (38, 20, 24, 18, RUMPUT_TERANG),
        (26, 26, 18, 14, RUMPUT_TERANG),
        (50, 26, 18, 14, RUMPUT_TERANG),
        (38, 14, 16, 12, RUMPUT_KILAU),
    ]
    for cx, cy, rx, ry, col in gumpalan:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=col)
    # Buah merah matang ranum tersebar
    buah_pos = [(26, 22), (44, 18), (34, 28), (52, 30), (22, 38), (42, 38), (56, 38)]
    for bx, by in buah_pos:
        d.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=_w(228, 42, 48))
        d.point((bx - 1, by - 1), fill=EMAS_KILAU) # Kilau buah
    return garis_luar(img)

def prop_saung_lumbung():
    """Lumbung padi / Saung panggung kayu khas pedesaan Jawa Barat."""
    w, h = 92, 98
    img, d = kanvas(w, h)
    # Tiang panggung kayu tinggi
    for x in (16, 38, 54, 76):
        d.rectangle([x, 56, x + 4, 94], fill=KAYU_MADU_PEKAT)
        d.line([(x, 56), (x, 94)], fill=KAYU_MADU)
    # Lantai panggung
    d.rectangle([10, 52, 82, 58], fill=KAYU_MADU)
    d.line([(10, 58), (82, 58)], fill=KAYU_MADU_PEKAT, width=2)
    # Dinding anyaman bambu (gedek)
    d.rectangle([16, 24, 76, 52], fill=_w(218, 182, 124))
    for y in range(26, 52, 5):
        d.line([(16, y), (76, y)], fill=_w(184, 146, 92))
    # Pintu kayu lumbung
    d.rectangle([40, 30, 52, 52], fill=KAYU_MADU_PEKAT)
    d.point((50, 42), fill=EMAS_TERANG) # Gagang pintu
    # Atap sirap ijuk melengkung tajam khas lumbung
    d.polygon([(46, 4), (88, 28), (84, 32), (46, 12), (8, 32), (4, 28)], fill=KAYU_MADU_PEKAT)
    d.polygon([(46, 8), (84, 28), (8, 28)], fill=_w(118, 76, 42))
    d.line([(46, 4), (88, 28)], fill=KAYU_MADU_TERANG, width=2)
    d.line([(46, 4), (4, 28)], fill=KAYU_MADU_TERANG, width=2)
    # Tangga kayu kecil
    d.line([(42, 54), (36, 94)], fill=KAYU_MADU_PEKAT, width=2)
    d.line([(48, 54), (42, 94)], fill=KAYU_MADU_PEKAT, width=2)
    for ty in range(60, 92, 8):
        d.line([(38, ty), (46, ty)], fill=KAYU_MADU)
    return garis_luar(img)

def buat_sprite_ayam():
    """Sprite sheet ayam kampung (4 frame jalan/patuk, ukuran 32x32 per frame)."""
    w, h = 32 * 4, 32
    img, d = kanvas(w, h)
    for f in range(4):
        ox = f * 32
        cx, cy = ox + 16, 16
        # Badan ayam oval putih/cokelat
        d.ellipse([cx - 7, cy - 4, cx + 5, cy + 6], fill=_w(248, 244, 236))
        # Sayap ayam
        d.ellipse([cx - 4, cy - 2, cx + 2, cy + 4], fill=_w(224, 186, 142))
        # Ekor ayam menjulang
        d.polygon([(cx - 7, cy - 1), (cx - 12, cy - 7), (cx - 4, cy - 1)], fill=_w(86, 64, 52))
        # Kepala & leher (mematuk di frame 1 dan 3)
        ky = cy - (6 if f in (0, 2) else 3)
        kx = cx + (4 if f in (0, 2) else 6)
        d.ellipse([kx - 3, ky - 4, kx + 3, ky + 2], fill=_w(248, 244, 236))
        d.point((kx + 1, ky - 2), fill=BATU_PEKAT) # Mata
        d.polygon([(kx + 2, ky - 1), (kx + 6, ky), (kx + 2, ky + 2)], fill=EMAS_TERANG) # Paruh kuning
        d.polygon([(kx - 1, ky - 5), (kx + 1, ky - 7), (kx + 2, ky - 4)], fill=_w(228, 48, 52)) # Jengger merah
        # Kaki ayam kuning kecil
        d.line([(cx - 2, cy + 6), (cx - 2, cy + 11)], fill=EMAS_TERANG)
        d.line([(cx + 2, cy + 6), (cx + 2, cy + 11)], fill=EMAS_TERANG)
    return garis_luar(img).save(KELUARAN / "ayam.png")

def buat_sprite_kucing():
    """Sprite kucing desa oren rebahan santai dengan ekor berkedut (4 frame)."""
    w, h = 32 * 4, 32
    img, d = kanvas(w, h)
    for f in range(4):
        ox = f * 32
        cx, cy = ox + 16, 18
        # Badan kucing oren tidur
        d.ellipse([cx - 8, cy - 4, cx + 8, cy + 6], fill=_w(238, 146, 68))
        d.ellipse([cx - 6, cy - 2, cx + 6, cy + 4], fill=_w(250, 182, 112))
        # Garis belang kucing
        for bx in (-3, 0, 3):
            d.line([(cx + bx, cy - 3), (cx + bx, cy + 2)], fill=_w(196, 108, 42))
        # Kepala kucing rebahan
        d.ellipse([cx + 5, cy - 3, cx + 13, cy + 5], fill=_w(238, 146, 68))
        # Telinga kucing runcing
        d.polygon([(cx + 8, cy - 5), (cx + 10, cy - 8), (cx + 12, cy - 3)], fill=_w(196, 108, 42))
        # Mata terpejam manis
        d.line([(cx + 8, cy), (cx + 11, cy)], fill=_w(92, 52, 24))
        # Ekor kucing berkedut pelan
        ey = cy - 2 + int(math.sin(f * math.pi / 2) * 3)
        d.arc([cx - 16, ey - 4, cx - 6, ey + 6], 90, 270, fill=_w(238, 146, 68), width=3)
    return garis_luar(img).save(KELUARAN / "kucing.png")

# ==============================================================================
# KARAKTER STARDEW VALLEY EDITION (BUSANA SUNDA PARAHYANGAN)
# ==============================================================================
# Resolusi frame: 48x80 (24x40 skala 2x)
LEBAR_FRAME = 24
TINGGI_FRAME = 40
SKALA = 2

PALET_SUNDA_PRIA = {
    "kulit_sorot": _w(255, 236, 218),
    "kulit_dasar": _w(244, 208, 182),
    "kulit_bayang": _w(218, 168, 138),
    "rambut": _w(44, 34, 32),
    # Bendo / Ikat Kepala Sunda
    "bendo_dasar": _w(132, 88, 56),
    "bendo_batik": _w(82, 50, 32),
    "bendo_emas": EMAS_TERANG,
    # Jas Tutup Krem Gading Elegan
    "jas_sorot": _w(255, 252, 244),
    "jas_dasar": _w(240, 234, 216),
    "jas_bayang": _w(198, 188, 168),
    "kancing": EMAS_TERANG,
    "ronce_melati": MELATI_PUTIH,
    # Kain Lereng Sunda
    "kain_dasar": _w(156, 106, 68),
    "kain_motif": _w(88, 54, 32),
    "celana": _w(44, 38, 42),
    "selop": _w(36, 28, 30),
}

PALET_SUNDA_WANITA = {
    "kulit_sorot": _w(255, 240, 226),
    "kulit_dasar": _w(248, 214, 190),
    "kulit_bayang": _w(220, 174, 146),
    "rambut": _w(40, 30, 32),
    # Siger Sunda Mahkota Emas & Kembang Goyang
    "siger_emas": EMAS_TERANG,
    "siger_kilau": EMAS_KILAU,
    "siger_bayang": EMAS_BAYANG,
    "ronce_melati": MELATI_PUTIH,
    # Kebaya Brokat Peach / Krem Anggun
    "kebaya_sorot": _w(255, 248, 242),
    "kebaya_dasar": _w(250, 226, 214), # Peach lembut
    "kebaya_bayang": _w(216, 182, 168),
    "kemben": _w(218, 88, 112),
    "bros_emas": EMAS_KILAU,
    # Kain Batik Lereng Eneng
    "kain_dasar": _w(168, 114, 76),
    "kain_motif": _w(94, 58, 36),
    "selop": _w(188, 64, 82),
}

def gambar_mata_stardew(d, x, y, arah="bawah"):
    if arah == "atas":
        return
    d.rectangle([x, y, x + 1, y + 2], fill=_w(36, 28, 30))
    d.point((x, y), fill=_w(255, 255, 255)) # Glint mata
    if arah == "bawah":
        d.point((x + 2, y + 2), fill=_w(246, 154, 148)) # Pipi blush

def frame_karakter_sunda(p, arah, frame_idx, wanita=False):
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    cx = LEBAR_FRAME // 2 # 12
    ayun = [0, 1, 0, -1][frame_idx]
    bob = 1 if frame_idx in (1, 3) else 0

    # 1. Kaki / Bawahan
    if wanita:
        # Kain panjang batik
        d.rectangle([cx - 4, 25 + bob, cx + 4, 36], fill=p["kain_dasar"])
        # Garis motif lereng
        for my in range(26 + bob, 36, 3):
            d.line([(cx - 3, my), (cx + 3, my - 1)], fill=p["kain_motif"])
        # Selop
        d.rectangle([cx - 3, 37, cx - 1, 38], fill=p["selop"])
        d.rectangle([cx + 1, 37, cx + 3, 38], fill=p["selop"])
    else:
        # Celana & Kain samping Sunda
        d.rectangle([cx - 4, 24 + bob, cx + 4, 29 + bob], fill=p["kain_dasar"])
        d.line([(cx - 3, 26 + bob), (cx + 3, 26 + bob)], fill=p["kain_motif"])
        # Kaki kiri dan kanan berayun
        dy_kiri = ayun if arah in ("kiri", "kanan") else (1 if frame_idx == 1 else 0)
        dy_kanan = -ayun if arah in ("kiri", "kanan") else (1 if frame_idx == 3 else 0)
        d.rectangle([cx - 4, 30 + bob, cx - 1, 36 - dy_kiri], fill=p["celana"])
        d.rectangle([cx + 1, 30 + bob, cx + 4, 36 - dy_kanan], fill=p["celana"])
        d.rectangle([cx - 4, 37 - dy_kiri, cx - 1, 38 - dy_kiri], fill=p["selop"])
        d.rectangle([cx + 1, 37 - dy_kanan, cx + 4, 38 - dy_kanan], fill=p["selop"])

    # 2. Badan / Baju
    baju_dasar = p["kebaya_dasar"] if wanita else p["jas_dasar"]
    baju_sorot = p["kebaya_sorot"] if wanita else p["jas_sorot"]
    baju_bayang = p["kebaya_bayang"] if wanita else p["jas_bayang"]
    d.rectangle([cx - 4, 15 + bob, cx + 4, 24 + bob], fill=baju_dasar)
    d.line([(cx - 4, 15 + bob), (cx - 4, 24 + bob)], fill=baju_sorot)
    d.line([(cx + 4, 15 + bob), (cx + 4, 24 + bob)], fill=baju_bayang)

    if arah == "bawah":
        if wanita:
            d.rectangle([cx - 2, 17 + bob, cx + 2, 21 + bob], fill=p["kemben"])
            d.point((cx, 18 + bob), fill=p["bros_emas"])
            # Untaian melati panjang
            for my in range(16 + bob, 24 + bob, 2):
                d.point((cx + 3, my), fill=p["ronce_melati"])
        else:
            # Kancing emas jas tutup
            for ky in range(17 + bob, 23 + bob, 2):
                d.point((cx, ky), fill=p["kancing"])
            # Kalung melati pria
            d.arc([cx - 3, 15 + bob, cx + 3, 21 + bob], 0, 180, fill=p["ronce_melati"])

    # Lengan
    for sx, sisi in ((cx - 6, -1), (cx + 5, 1)):
        layun = ayun * sisi
        d.rectangle([sx, 16 + bob + layun, sx + 1, 23 + bob + layun], fill=baju_dasar)
        d.point((sx, 24 + bob + layun), fill=p["kulit_dasar"])

    # 3. Kepala & Leher
    d.rectangle([cx - 1, 13 + bob, cx + 1, 15 + bob], fill=p["kulit_dasar"])
    d.rectangle([cx - 4, 5 + bob, cx + 4, 13 + bob], fill=p["kulit_dasar"])

    if arah == "bawah":
        gambar_mata_stardew(d, cx - 3, 9 + bob, arah="bawah")
        gambar_mata_stardew(d, cx + 1, 9 + bob, arah="bawah")
        d.line([(cx - 1, 12 + bob), (cx + 1, 12 + bob)], fill=_w(216, 112, 110)) # Bibir
    elif arah in ("kiri", "kanan"):
        mx = cx - 2 if arah == "kiri" else cx + 1
        gambar_mata_stardew(d, mx, 9 + bob, arah="kiri")

    # 4. Hiasan Kepala (Bendo Sunda vs Siger Sunda)
    if wanita:
        # Sanggul & Siger Sunda
        d.rectangle([cx - 5, 4 + bob, cx + 5, 7 + bob], fill=p["rambut"])
        d.ellipse([cx - 3, 2 + bob, cx + 3, 6 + bob], fill=p["rambut"])
        # Mahkota Siger Emas
        d.line([(cx - 5, 6 + bob), (cx + 5, 6 + bob)], fill=p["siger_emas"])
        d.polygon([(cx, 3 + bob), (cx - 2, 6 + bob), (cx + 2, 6 + bob)], fill=p["siger_kilau"])
        # Kembang goyang di sanggul
        for gx in (cx - 4, cx, cx + 4):
            d.point((gx, 2 + bob), fill=p["siger_kilau"])
    else:
        # Bendo Sunda (Khas kerutan di dahi dan sayap di belakang)
        d.rectangle([cx - 5, 4 + bob, cx + 5, 7 + bob], fill=p["bendo_dasar"])
        d.line([(cx - 4, 6 + bob), (cx + 4, 6 + bob)], fill=p["bendo_batik"])
        d.point((cx + 4, 3 + bob), fill=p["bendo_emas"]) # Lipatan pucuk bendo

    hasil = garis_luar(img)
    return hasil.resize((LEBAR_FRAME * SKALA, TINGGI_FRAME * SKALA), Image.NEAREST)

def buat_sprite_sheet_karakter(palet, nama_berkas, wanita=False):
    arah_list = ["bawah", "kiri", "kanan", "atas"]
    lembar = Image.new("RGBA", (LEBAR_FRAME * SKALA * 4, TINGGI_FRAME * SKALA * 4), (0, 0, 0, 0))
    for baris, arah in enumerate(arah_list):
        for kolom in range(4):
            frame = frame_karakter_sunda(palet, arah, kolom, wanita=wanita)
            lembar.paste(frame, (kolom * LEBAR_FRAME * SKALA, baris * TINGGI_FRAME * SKALA))
    lembar.save(KELUARAN / nama_berkas)

def prop_pengantin_duduk(palet, wanita=False):
    """Sprite pengantin duduk bersanding untuk dipajang di pelaminan."""
    img = frame_karakter_sunda(palet, "bawah", 0, wanita=wanita)
    return img

# ==============================================================================
# ATRAKSI TAMBAHAN PEDESAAN (PEMUSIK, PENARI, TAMU, KOLAM, BEBEK, LENTERA)
# ==============================================================================
def prop_pemusik():
    """Saung bambu dengan pemusik kecapi & suling Sunda."""
    w, h = 96, 76
    img, d = kanvas(w, h)
    # Panggung bambu
    d.rectangle([10, 48, 86, 68], fill=KAYU_MADU)
    d.line([(10, 68), (86, 68)], fill=KAYU_MADU_PEKAT, width=2)
    # Tiang & atap saung
    for x in (14, 80):
        d.rectangle([x, 14, x + 3, 50], fill=KAYU_MADU_PEKAT)
    d.polygon([(48, 4), (92, 20), (88, 24), (48, 10), (8, 24), (4, 20)], fill=KAYU_MADU_PEKAT)
    d.polygon([(48, 8), (88, 20), (8, 20)], fill=_w(120, 78, 42))
    # Pemusik 1: Pemain Kecapi (kiri)
    cx1 = 30
    d.rectangle([cx1 - 6, 32, cx1 + 6, 48], fill=_w(60, 44, 76)) # Baju ungu pangsi
    d.ellipse([cx1 - 4, 24, cx1 + 4, 32], fill=_w(244, 208, 182)) # Kepala
    d.rectangle([cx1 - 5, 23, cx1 + 5, 26], fill=KAYU_MADU_PEKAT) # Bendo ikat kepala
    # Kecapi kayu di pangkuan
    d.polygon([(cx1 - 12, 42), (cx1 + 12, 42), (cx1 + 10, 48), (cx1 - 10, 48)], fill=KAYU_MADU_TERANG)
    for kx in range(cx1 - 8, cx1 + 8, 3):
        d.line([(kx, 42), (kx, 47)], fill=EMAS_TERANG) # Senar
    # Pemusik 2: Pemain Suling (kanan)
    cx2 = 66
    d.rectangle([cx2 - 5, 32, cx2 + 5, 48], fill=_w(48, 64, 52)) # Baju hijau pangsi
    d.ellipse([cx2 - 4, 24, cx2 + 4, 32], fill=_w(244, 208, 182))
    d.rectangle([cx2 - 5, 23, cx2 + 5, 26], fill=KAYU_MADU_PEKAT)
    # Suling bambu miring
    d.line([(cx2 - 2, 32), (cx2 + 10, 44)], fill=EMAS_TERANG, width=3)
    # Ronce melati di atap saung
    for x in range(20, 78, 8):
        d.point((x, 22), fill=MELATI_PUTIH)
        d.point((x + 1, 24), fill=MELATI_KUNING)
    return garis_luar(img)

def prop_penari():
    """Dua penari Sunda Jaipong berbusana selendang merak meliuk."""
    w, h = 88, 74
    img, d = kanvas(w, h)
    for idx, cx in enumerate((28, 60)):
        # Selendang meliuk di belakang
        warna_selendang = _w(238, 54, 64) if idx == 0 else _w(248, 196, 52)
        d.arc([cx - 16, 26, cx + 18, 56], 30, 240, fill=warna_selendang, width=3)
        # Kain batik bawahan
        d.rectangle([cx - 5, 42, cx + 5, 62], fill=_w(156, 106, 68))
        d.line([(cx - 4, 44), (cx + 4, 48)], fill=_w(88, 54, 32))
        d.line([(cx - 4, 52), (cx + 4, 56)], fill=_w(88, 54, 32))
        # Kemben anggun
        d.rectangle([cx - 5, 28, cx + 5, 42], fill=_w(196, 44, 76) if idx == 0 else _w(44, 112, 140))
        d.point((cx, 32), fill=EMAS_KILAU) # Bros dada
        # Lengan gemulai menari
        ayun_tangan = -6 if idx == 0 else 6
        d.line([(cx - 5, 30), (cx - 10, 24 + ayun_tangan)], fill=_w(248, 214, 190), width=2)
        d.line([(cx + 5, 30), (cx + 12, 26 - ayun_tangan)], fill=_w(248, 214, 190), width=2)
        # Kepala & Mahkota Merak Kembang Goyang
        d.ellipse([cx - 4, 18, cx + 4, 27], fill=_w(248, 214, 190))
        d.line([(cx - 3, 22), (cx - 1, 22)], fill=GARIS_LUAR)
        d.line([(cx + 1, 22), (cx + 3, 22)], fill=GARIS_LUAR)
        d.point((cx - 2, 24), fill=_w(246, 154, 148)) # Blush
        d.point((cx + 2, 24), fill=_w(246, 154, 148))
        # Mahkota Emas & Kembang Goyang
        d.polygon([(cx, 11), (cx - 6, 18), (cx + 6, 18)], fill=EMAS_KILAU)
        d.point((cx - 4, 10), fill=EMAS_TERANG)
        d.point((cx + 4, 10), fill=EMAS_TERANG)
        d.point((cx, 8), fill=_w(248, 64, 82))
    return garis_luar(img)

def prop_tamu_desa():
    """Tamu warga desa pria & wanita mengobrol di dekat kebun."""
    w, h = 68, 64
    img, d = kanvas(w, h)
    # Pria (kiri)
    cx1 = 20
    d.rectangle([cx1 - 5, 34, cx1 + 5, 54], fill=_w(118, 76, 42)) # Celana
    d.rectangle([cx1 - 6, 22, cx1 + 6, 36], fill=_w(188, 136, 82)) # Kemeja batik
    for y in range(24, 36, 4):
        d.point((cx1, y), fill=EMAS_TERANG)
    d.ellipse([cx1 - 4, 12, cx1 + 4, 21], fill=_w(244, 208, 182))
    d.rectangle([cx1 - 5, 11, cx1 + 5, 14], fill=GARIS_LUAR) # Peci
    # Wanita (kanan)
    cx2 = 48
    d.rectangle([cx2 - 5, 32, cx2 + 5, 56], fill=_w(156, 106, 68)) # Kain batik
    d.rectangle([cx2 - 6, 20, cx2 + 6, 34], fill=_w(238, 178, 196)) # Kebaya pink
    d.ellipse([cx2 - 4, 10, cx2 + 4, 19], fill=_w(248, 214, 190))
    d.ellipse([cx2 - 5, 8, cx2 + 5, 14], fill=GARIS_LUAR) # Kerudung/sanggul
    # Balon obrolan kecil di antara mereka
    d.polygon([(30, 14), (38, 14), (38, 8), (30, 8)], fill=_w(255, 255, 255))
    d.point((32, 16), fill=_w(255, 255, 255))
    d.point((33, 11), fill=_w(228, 50, 60)) # Hati / emoji kecil
    return garis_luar(img)

def prop_kolam_ikan():
    """Kolam batu kali dengan pancuran air bambu & ikan mas koi."""
    w, h = 80, 64
    img, d = kanvas(w, h)
    # Lingkar batu kali kolam
    d.ellipse([2, 14, 78, 58], fill=BATU_PEKAT)
    d.ellipse([6, 18, 74, 54], fill=BATU_DASAR)
    d.ellipse([10, 22, 70, 50], fill=AIR_DASAR)
    d.ellipse([14, 25, 66, 47], fill=AIR_TERANG)
    # Ikan koi oranye & putih berenang
    d.ellipse([24, 30, 36, 36], fill=_w(248, 120, 38))
    d.point((34, 33), fill=_w(255, 255, 255)) # Ekor koi
    d.ellipse([46, 36, 56, 42], fill=_w(255, 248, 240))
    d.point((47, 39), fill=_w(238, 64, 48))
    # Pancuran bambu di kiri atas kolam
    d.rectangle([8, 6, 12, 28], fill=KAYU_MADU_PEKAT) # Tiang bambu
    d.polygon([(10, 10), (28, 16), (28, 20), (10, 14)], fill=KAYU_MADU) # Pipa bambu
    d.line([(28, 18), (32, 34)], fill=AIR_KILAU, width=2) # Air memancur
    # Teratai & daun di air
    d.ellipse([34, 40, 44, 46], fill=RUMPUT_DASAR)
    d.point((38, 41), fill=_w(254, 150, 190)) # Bunga teratai pink
    return garis_luar(img)

def prop_kincir():
    """Kincir air / bambu pedesaan tepi sawah."""
    w, h = 48, 70
    img, d = kanvas(w, h)
    # Tiang penyangga A-frame kayu
    d.line([(14, 64), (24, 28)], fill=KAYU_MADU_PEKAT, width=3)
    d.line([(34, 64), (24, 28)], fill=KAYU_MADU_PEKAT, width=3)
    d.line([(16, 50), (32, 50)], fill=KAYU_MADU, width=2)
    # Kincir berbaling 6
    cx, cy = 24, 28
    r = 18
    for deg in range(0, 360, 60):
        rad = math.radians(deg)
        bx = cx + int(math.cos(rad) * r)
        by = cy + int(math.sin(rad) * r)
        d.line([(cx, cy), (bx, by)], fill=KAYU_MADU, width=2)
        # Tabung bambu penampung air di ujung baling
        d.rectangle([bx - 2, by - 2, bx + 2, by + 2], fill=KAYU_MADU_TERANG)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=BATU_PEKAT)
    d.point((cx, cy), fill=EMAS_TERANG)
    return garis_luar(img)

def prop_lentera():
    """Tiang lentera kayu rustic bercahaya hangat pesta kebun."""
    w, h = 28, 66
    img, d = kanvas(w, h)
    # Tiang kayu
    d.rectangle([12, 16, 15, 62], fill=KAYU_MADU_PEKAT)
    d.line([(12, 16), (12, 62)], fill=KAYU_MADU)
    # Gantungan lengkung besi
    d.line([(14, 16), (22, 12)], fill=BATU_PEKAT, width=2)
    d.line([(22, 12), (22, 18)], fill=BATU_PEKAT, width=2)
    # Lentera kaca segi enam
    d.polygon([(18, 18), (26, 18), (28, 22), (26, 30), (18, 30), (16, 22)], fill=EMAS_DASAR)
    d.rectangle([19, 20, 25, 28], fill=_w(255, 246, 170)) # Kaca kuning bercahaya
    d.point((22, 24), fill=_w(255, 255, 255)) # Titik lampu
    return garis_luar(img)

def prop_bangku():
    """Bangku kayu rustic pedesaan dengan pot bunga kamboja."""
    w, h = 54, 38
    img, d = kanvas(w, h)
    # Kaki bangku
    for x in (6, 38):
        d.rectangle([x, 18, x + 3, 34], fill=KAYU_MADU_PEKAT)
    # Papan sandaran & dudukan
    d.rectangle([4, 12, 42, 16], fill=KAYU_MADU)
    d.rectangle([2, 18, 44, 24], fill=KAYU_MADU_TERANG)
    d.line([(2, 24), (44, 24)], fill=KAYU_MADU_PEKAT, width=2)
    # Pot bunga marigold di samping
    d.rectangle([44, 22, 52, 34], fill=_w(176, 94, 52)) # Pot terakota
    d.ellipse([42, 14, 54, 24], fill=RUMPUT_TERANG)
    d.point((46, 18), fill=_w(254, 168, 64))
    d.point((50, 16), fill=_w(238, 54, 64))
    return garis_luar(img)

def buat_sprite_bebek():
    """Sprite sheet bebek pedesaan berenang (4 frame 32x32 per frame)."""
    w, h = 32 * 4, 32
    img, d = kanvas(w, h)
    for f in range(4):
        ox = f * 32
        cx, cy = ox + 16, 18
        # Riak air di belakang bebek
        riak_x = cx - 12 - (f % 2) * 2
        d.arc([riak_x, cy + 2, riak_x + 8, cy + 6], 0, 180, fill=AIR_KILAU, width=2)
        # Badan bebek mengapung
        d.ellipse([cx - 8, cy - 4, cx + 6, cy + 4], fill=_w(252, 250, 242))
        d.ellipse([cx - 5, cy - 2, cx + 2, cy + 2], fill=_w(232, 224, 206)) # Sayap
        # Kepala bebek menoleh ke depan
        d.ellipse([cx + 2, cy - 8, cx + 8, cy - 2], fill=_w(252, 250, 242))
        d.point((cx + 5, cy - 6), fill=GARIS_LUAR) # Mata
        d.polygon([(cx + 7, cy - 5), (cx + 12, cy - 4), (cx + 7, cy - 3)], fill=EMAS_TERANG) # Paruh kuning
    return garis_luar(img).save(KELUARAN / "bebek.png")

# ==============================================================================
# MAIN FUNCTION
# ==============================================================================
def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    print("=== Menghasilkan Aset Tema Desa Asri Parahyangan (Gaya Stardew Valley) ===")

    print("[1] Membuat Tileset & Tepi...")
    buat_tileset()
    buat_tepi()

    print("[2] Membuat Properti Lingkungan & Pernikahan Utama...")
    prop_pelaminan().save(KELUARAN / "pelaminan.png")
    prop_papan().save(KELUARAN / "papan.png")
    prop_galeri().save(KELUARAN / "galeri.png")
    prop_buku_tamu().save(KELUARAN / "buku_tamu.png")
    prop_hadiah().save(KELUARAN / "hadiah.png")
    prop_gerbang().save(KELUARAN / "gerbang.png")
    prop_pohon_buah().save(KELUARAN / "pohon_buah.png")
    prop_saung_lumbung().save(KELUARAN / "saung_lumbung.png")

    print("[3] Membuat Atraksi Baru (Pemusik, Penari, Tamu, Kolam, Kincir, Lentera, Bangku)...")
    prop_pemusik().save(KELUARAN / "pemusik.png")
    prop_penari().save(KELUARAN / "penari.png")
    prop_tamu_desa().save(KELUARAN / "tamu_desa.png")
    prop_kolam_ikan().save(KELUARAN / "kolam_ikan.png")
    prop_kincir().save(KELUARAN / "kincir.png")
    prop_lentera().save(KELUARAN / "lentera.png")
    prop_bangku().save(KELUARAN / "bangku.png")

    print("[4] Membuat Hewan Pedesaan (Ayam, Kucing, Bebek)...")
    buat_sprite_ayam()
    buat_sprite_kucing()
    buat_sprite_bebek()

    print("[5] Membuat Karakter Tamu & Pengantin Sunda...")
    buat_sprite_sheet_karakter(PALET_SUNDA_PRIA, "karakter_pria.png", wanita=False)
    buat_sprite_sheet_karakter(PALET_SUNDA_WANITA, "karakter_wanita.png", wanita=True)
    prop_pengantin_duduk(PALET_SUNDA_PRIA, wanita=False).save(KELUARAN / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_SUNDA_WANITA, wanita=True).save(KELUARAN / "pengantin_wanita.png")

    print(f"\n[SUKSES] Seluruh aset lengkap tersimpan di {KELUARAN}")

if __name__ == "__main__":
    main()

