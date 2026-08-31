"""Membuat seluruh aset pixel art Tema 2: Pantai Lombok Beach Wedding dari kode.

Keluaran di static/game_lombok/:
  tileset.png          deretan tile lantai (pasir, pasir basah, air laut, jalan karang, kayu, karpet songket, dsb)
  tepi.png             lapisan tepi pasir ke air/karang
  karakter_pria.png    lembar sprite 4 arah x 4 frame pria Sasak (Sapuk hitam, rompi/baju Sasak)
  karakter_wanita.png  lembar sprite 4 arah x 4 frame wanita Sasak (mahkota Lambung emas, kebaya/songket merah)
  <properti>.png       pelaminan Lumbung, candi bentar, bale saji, obor, pohon kelapa/pandan, perahu, penari, dll
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game_lombok"
SKALA = 2
UKURAN_TILE = 16

GARIS = (42, 32, 40, 255)

# Palet Pantai & Budaya Sasak
PASIR_DASAR = (242, 222, 178, 255)
PASIR_TERANG = (252, 238, 204, 255)
PASIR_GELAP = (220, 196, 150, 255)
PASIR_BASAH = (194, 168, 126, 255)

LAUT_1 = (64, 196, 186, 255)
LAUT_2 = (42, 168, 166, 255)
LAUT_DALAM = (32, 132, 148, 255)
BUSA_LAUT = (230, 252, 250, 255)

BATA_MERAH = (176, 68, 48, 255)
BATA_GELAP = (136, 48, 34, 255)
BATA_TERANG = (204, 94, 68, 255)

JERAMI_ATAP = (202, 168, 108, 255)
JERAMI_GELAP = (162, 128, 76, 255)
JERAMI_TERANG = (232, 202, 142, 255)

KAYU_BAMBU = (196, 160, 106, 255)
KAYU_GELAP = (138, 98, 58, 255)
KAYU_COKLAT = (168, 122, 78, 255)

SONGKET_MERAH = (168, 38, 54, 255)
SONGKET_EMAS = (228, 184, 76, 255)
SONGKET_UNGU = (128, 52, 98, 255)
SONGKET_HIJAU = (48, 138, 108, 255)

DAUN_PALEM = (58, 134, 62, 255)
DAUN_TERANG = (84, 168, 78, 255)
DAUN_GELAP = (38, 96, 48, 255)


def kanvas(lebar, tinggi, latar=(0, 0, 0, 0)):
    img = Image.new("RGBA", (lebar, tinggi), latar)
    return img, ImageDraw.Draw(img)


def perbesar(img, skala=SKALA):
    return img.resize((img.width * skala, img.height * skala), Image.NEAREST)


def garis_luar(img, warna=GARIS):
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
# Tile Lantai / Alam Pantai Lombok
# --------------------------------------------------------------------------
def tile_pasir(seed=1, ada_kerang=False):
    img, d = kanvas(16, 16, PASIR_DASAR)
    r = random.Random(seed)
    bintik(d, r, 24, PASIR_GELAP)
    bintik(d, r, 18, PASIR_TERANG)
    for _ in range(3):
        x, y = r.randrange(2, 14), r.randrange(2, 14)
        d.point((x, y), fill=(236, 210, 162, 255))
    if ada_kerang:
        # kerang kecil merah muda / putih
        d.point((4, 5), fill=(248, 196, 206, 255))
        d.point((5, 5), fill=(255, 240, 244, 255))
        d.point((12, 11), fill=(210, 230, 242, 255))
        d.point((11, 12), fill=(244, 248, 252, 255))
    return img


def tile_pasir_basah(seed=2):
    img, d = kanvas(16, 16, PASIR_BASAH)
    r = random.Random(seed)
    bintik(d, r, 20, (178, 150, 110, 255))
    bintik(d, r, 16, (214, 188, 148, 255))
    # kilau air tipis di atas pasir basah
    d.line([(2, 4), (6, 4)], fill=(218, 238, 236, 180))
    d.line([(9, 11), (13, 11)], fill=(218, 238, 236, 180))
    return img


def tile_jalan_karang(seed=3):
    """Jalan setapak batu karang/koral pantai bermotif bulat halus."""
    img, d = kanvas(16, 16, (232, 208, 186, 255))
    r = random.Random(seed)
    nat = (194, 166, 142, 255)
    # batas-batas batu koral bulat
    d.ellipse([1, 1, 7, 7], outline=nat, fill=(244, 224, 206, 255))
    d.ellipse([8, 0, 15, 6], outline=nat, fill=(238, 214, 194, 255))
    d.ellipse([0, 8, 8, 15], outline=nat, fill=(240, 218, 198, 255))
    d.ellipse([8, 7, 15, 15], outline=nat, fill=(248, 230, 212, 255))
    bintik(d, r, 12, (218, 190, 166, 255))
    return img


def tile_air_laut(seed=4, fase=0):
    """Air laut pantai turquoise berombak lembut."""
    img, d = kanvas(16, 16, LAUT_1)
    r = random.Random(seed)
    bintik(d, r, 18, LAUT_2)
    bintik(d, r, 10, LAUT_DALAM)
    geser = (fase * 5) % 16
    for i, y in enumerate((2, 7, 12)):
        x = (r.randrange(0, 10) + geser + i * 4) % 16
        panjang = 5
        d.line([(x, y), (min(15, x + panjang), y)], fill=BUSA_LAUT)
        if x + panjang > 15:
            d.line([(0, y), (x + panjang - 16, y)], fill=BUSA_LAUT)
    # kilau karang bawah air
    d.point(((3 + geser) % 16, 10), fill=(80, 226, 212, 255))
    d.point(((11 + geser) % 16, 4), fill=(80, 226, 212, 255))
    return img


def tile_kayu_panggung(seed=5):
    """Papan kayu panggung Lumbung."""
    img, d = kanvas(16, 16, KAYU_COKLAT)
    r = random.Random(seed)
    for y in (0, 5, 10, 15):
        d.line([(0, y), (15, y)], fill=KAYU_GELAP)
    d.line([(5, 1), (5, 4)], fill=KAYU_GELAP)
    d.line([(12, 6), (12, 9)], fill=KAYU_GELAP)
    d.line([(4, 11), (4, 14)], fill=KAYU_GELAP)
    bintik(d, r, 12, (188, 142, 98, 255))
    return img


def tile_karpet_songket(seed=6):
    """Karpet tenun Sasak warna merah marun dengan motif emas."""
    img, d = kanvas(16, 16, SONGKET_MERAH)
    r = random.Random(seed)
    # tepian emas
    d.rectangle([0, 0, 15, 0], fill=SONGKET_EMAS)
    d.rectangle([0, 15, 15, 15], fill=SONGKET_EMAS)
    # motif wajik Sasak
    d.polygon([(7, 3), (12, 8), (7, 13), (2, 8)], outline=SONGKET_EMAS, fill=SONGKET_UNGU)
    d.point((7, 8), fill=SONGKET_EMAS)
    bintik(d, r, 8, (142, 28, 42, 255))
    return img


def tile_tembok_bata(seed=7):
    """Tembok bata merah Candi Bentar khas Lombok."""
    img, d = kanvas(16, 16, BATA_MERAH)
    r = random.Random(seed)
    nat = BATA_GELAP
    d.line([(0, 4), (15, 4)], fill=nat)
    d.line([(0, 9), (15, 9)], fill=nat)
    d.line([(0, 14), (15, 14)], fill=nat)
    d.line([(7, 0), (7, 4)], fill=nat)
    d.line([(3, 5), (3, 9)], fill=nat)
    d.line([(11, 5), (11, 9)], fill=nat)
    d.line([(8, 10), (8, 14)], fill=nat)
    bintik(d, r, 16, BATA_TERANG)
    return img


def tile_rumput_pantai(seed=8):
    """Rumput tropis tepi pantai berseling pasir."""
    img, d = kanvas(16, 16, (128, 178, 102, 255))
    r = random.Random(seed)
    bintik(d, r, 20, (108, 158, 86, 255))
    bintik(d, r, 16, (148, 198, 118, 255))
    # bunga kamboja putih kecil
    d.point((5, 6), fill=(255, 255, 240, 255))
    d.point((6, 6), fill=(255, 220, 100, 255))
    d.point((12, 10), fill=(255, 255, 240, 255))
    return img


def tile_karang_batu(seed=9):
    """Batu karang pesisir pantai tidak bisa dilewati."""
    img, d = kanvas(16, 16, (120, 116, 126, 255))
    r = random.Random(seed)
    d.ellipse([1, 1, 14, 14], fill=(140, 136, 148, 255))
    d.ellipse([3, 3, 12, 12], fill=(160, 156, 168, 255))
    bintik(d, r, 24, (98, 92, 104, 255))
    bintik(d, r, 12, (200, 240, 236, 255)) # lumut laut
    return img


URUTAN_TILE_LOMBOK = [
    ("pasir", lambda: tile_pasir(11)),
    ("pasir_kerang", lambda: tile_pasir(23, ada_kerang=True)),
    ("pasir_basah", lambda: tile_pasir_basah(31)),
    ("jalan_karang", tile_jalan_karang),
    ("kayu", tile_kayu_panggung),
    ("karpet", tile_karpet_songket),
    ("air1", lambda: tile_air_laut(51, 0)),
    ("air2", lambda: tile_air_laut(51, 1)),
    ("air3", lambda: tile_air_laut(51, 2)),
    ("bata_merah", tile_tembok_bata),
    ("rumput", tile_rumput_pantai),
    ("karang", tile_karang_batu),
]


def buat_tileset():
    tiles = [fungsi() for _, fungsi in URUTAN_TILE_LOMBOK]
    lembar, _ = kanvas(16 * len(tiles), 16)
    for i, t in enumerate(tiles):
        lembar.paste(t, (i * 16, 0))
    perbesar(lembar).save(KELUARAN / "tileset.png")
    return [nama for nama, _ in URUTAN_TILE_LOMBOK]


# --------------------------------------------------------------------------
# Tepi Pasir ke Air / Karang
# --------------------------------------------------------------------------
def tepi_sisi(sisi, seed):
    pasir = tile_pasir(seed)
    masker = Image.new("L", (16, 16), 0)
    dm = ImageDraw.Draw(masker)
    r = random.Random(seed + 800)
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
    hasil.paste(pasir, (0, 0), masker)
    return hasil


def tepi_sudut(sudut, seed):
    pasir = tile_pasir(seed)
    masker = Image.new("L", (16, 16), 0)
    dm = ImageDraw.Draw(masker)
    jari = 5
    pusat = {
        "kiri_atas": (0, 0),
        "kanan_atas": (15, 0),
        "kiri_bawah": (0, 15),
        "kanan_bawah": (15, 15),
    }[sudut]
    dm.ellipse([pusat[0] - jari, pusat[1] - jari, pusat[0] + jari, pusat[1] + jari], fill=255)
    hasil = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    hasil.paste(pasir, (0, 0), masker)
    return hasil


URUTAN_TEPI_LOMBOK = [
    ("atas", lambda: tepi_sisi("atas", 201)),
    ("bawah", lambda: tepi_sisi("bawah", 202)),
    ("kiri", lambda: tepi_sisi("kiri", 203)),
    ("kanan", lambda: tepi_sisi("kanan", 204)),
    ("kiri_atas", lambda: tepi_sudut("kiri_atas", 205)),
    ("kanan_atas", lambda: tepi_sudut("kanan_atas", 206)),
    ("kiri_bawah", lambda: tepi_sudut("kiri_bawah", 207)),
    ("kanan_bawah", lambda: tepi_sudut("kanan_bawah", 208)),
]


def buat_tepi():
    potongan = [fungsi() for _, fungsi in URUTAN_TEPI_LOMBOK]
    lembar, _ = kanvas(16 * len(potongan), 16)
    for i, t in enumerate(potongan):
        lembar.paste(t, (i * 16, 0))
    perbesar(lembar).save(KELUARAN / "tepi.png")
    return [nama for nama, _ in URUTAN_TEPI_LOMBOK]


# --------------------------------------------------------------------------
# Karakter Adat Sasak Lombok (Sprite Sheet 4 Arah x 4 Frame)
# --------------------------------------------------------------------------
PALET_PRIA_SASAK = {
    "kulit": (240, 196, 156, 255),
    "kulit_gelap": (210, 164, 126, 255),
    "rambut": (48, 38, 42, 255),
    "rambut_terang": (76, 60, 64, 255),
    "sapuk": (36, 32, 40, 255),           # Ikat kepala Sapuk hitam
    "sapuk_emas": (224, 182, 72, 255),
    "baju": (36, 32, 40, 255),            # Rompi Pegon hitam
    "baju_dalam": (248, 244, 236, 255),   # Baju putih dalam
    "dodot": (168, 38, 54, 255),          # Kain bebet/dodot songket merah
    "dodot_emas": (224, 182, 72, 255),
    "bawahan": (48, 44, 52, 255),
    "sepatu": (42, 38, 42, 255),
}

PALET_WANITA_SASAK = {
    "kulit": (246, 206, 170, 255),
    "kulit_gelap": (216, 172, 138, 255),
    "rambut": (48, 38, 42, 255),
    "rambut_terang": (76, 60, 64, 255),
    "mahkota": (228, 186, 76, 255),       # Mahkota Lambung emas khas Sasak
    "mahkota_terang": (252, 224, 128, 255),
    "baju": (168, 38, 54, 255),           # Kebaya/Lambung merah khas Sasak
    "baju_gelap": (132, 28, 42, 255),
    "motif": (224, 182, 72, 255),
    "bawahan": (168, 38, 54, 255),        # Kain Songket Sasak
    "sepatu": (118, 82, 58, 255),
    "aksen": (224, 182, 72, 255),
}

ARAH = ["bawah", "kiri", "kanan", "atas"]


def karakter_frame_sasak(arah, frame, p, wanita=False):
    img, d = kanvas(18, 28)
    ayun = [0, 1, 0, -1][frame]

    # --- Kaki ---
    y_kaki = 21 if wanita else 19
    for x0, sisi in ((5, ayun), (10, -ayun)):
        atas = y_kaki + (1 if sisi > 0 else 0)
        bawah = 24 - (1 if sisi > 0 else 0)
        d.rectangle([x0, atas, x0 + 2, bawah], fill=p["kulit"] if wanita else p["bawahan"])
        d.rectangle([x0, bawah - 1, x0 + 2, bawah], fill=p["sepatu"])

    # --- Badan ---
    if wanita:
        # Kain Songket Sasak menjuntai
        d.polygon([(5, 14), (12, 14), (14, 21), (3, 21)], fill=p["bawahan"])
        for y in (16, 18, 20):
            for x in range(4, 13, 3):
                d.point((x, y), fill=p["motif"])
        # Baju Lambung merah
        d.rectangle([5, 12, 12, 17], fill=p["baju"])
        d.line([(5, 17), (12, 17)], fill=p["baju_gelap"])
        # Sabuk pending emas
        d.line([(5, 15), (12, 15)], fill=p["aksen"])
    else:
        # Pria: Rompi hitam Pegon di atas baju putih + kain songket dodot di pinggang
        d.rectangle([5, 12, 12, 18], fill=p["baju"])
        d.rectangle([8, 12, 9, 16], fill=p["baju_dalam"])
        # Kain dodot songket merah di pinggang
        d.rectangle([5, 16, 12, 18], fill=p["dodot"])
        d.line([(5, 17), (12, 17)], fill=p["dodot_emas"])

    # --- Lengan ---
    for x0, sisi in ((3, -ayun), (13, ayun)):
        atas = 13 + (1 if sisi > 0 else 0)
        d.rectangle([x0, atas, x0 + 1, atas + 4], fill=p["baju"])
        d.rectangle([x0, atas + 5, x0 + 1, atas + 5], fill=p["kulit"])

    # --- Kepala & Wajah ---
    d.rectangle([5, 4, 12, 11], fill=p["kulit"])
    d.line([(5, 11), (12, 11)], fill=p["kulit_gelap"])

    if wanita:
        # Mahkota Lambung Sasak: tinggi melengkung dengan hiasan emas
        d.rectangle([4, 4, 13, 8], fill=p["rambut"])
        d.polygon([(4, 4), (9, 0), (13, 4)], fill=p["mahkota"])
        d.polygon([(6, 3), (9, 1), (12, 3)], fill=p["mahkota_terang"])
        d.rectangle([4, 4, 13, 5], fill=p["mahkota"])
        # Anting & hiasan melati
        d.point((4, 8), fill=p["mahkota_terang"])
        d.point((13, 8), fill=p["mahkota_terang"])
        d.point((3, 9), fill=(255, 255, 240, 255))
        d.point((14, 9), fill=(255, 255, 240, 255))
    else:
        # Sapuk Sasak: ikat kepala hitam melingkar dengan lipatan segitiga khas di samping
        d.rectangle([5, 3, 12, 6], fill=p["sapuk"])
        d.line([(5, 5), (12, 5)], fill=p["sapuk_emas"])
        # Ujung sapuk tegak di kanan atas
        d.polygon([(11, 3), (14, 0), (13, 4)], fill=p["sapuk"])
        d.point((13, 1), fill=p["sapuk_emas"])

    # Mata & ekspresi
    mata = (48, 38, 42, 255)
    if arah == "bawah":
        d.point((7, 8), fill=mata)
        d.point((10, 8), fill=mata)
        d.line([(8, 10), (9, 10)], fill=(204, 122, 116, 255))
    elif arah == "kiri":
        d.point((6, 8), fill=mata)
        d.point((8, 8), fill=mata)
    elif arah == "kanan":
        d.point((9, 8), fill=mata)
        d.point((11, 8), fill=mata)
    elif arah == "atas":
        # Belakang kepala
        if wanita:
            d.rectangle([5, 3, 12, 10], fill=p["rambut"])
            d.polygon([(4, 4), (9, 0), (13, 4)], fill=p["mahkota"])
        else:
            d.rectangle([5, 3, 12, 10], fill=p["sapuk"])

    return garis_luar(img)


def buat_karakter_sasak(nama, palet, wanita):
    lembar, _ = kanvas(18 * 4, 28 * 4)
    for baris, arah in enumerate(ARAH):
        for kolom in range(4):
            lembar.paste(karakter_frame_sasak(arah, kolom, palet, wanita), (kolom * 18, baris * 28))
    perbesar(lembar).save(KELUARAN / f"{nama}.png")


# --------------------------------------------------------------------------
# Properti & Dekorasi Pantai Sasak Lombok (Sesuai Gambar Tema 2)
# --------------------------------------------------------------------------
def prop_pelaminan_lumbung():
    """Pelaminan Bale Lumbung Sasak atap melengkung runcing seperti perahu."""
    img, d = kanvas(96, 68)

    # 1. Panggung Kayu bertingkat
    d.rectangle([8, 54, 87, 67], fill=KAYU_GELAP)
    d.rectangle([9, 55, 86, 63], fill=KAYU_COKLAT)
    d.line([(9, 63), (86, 63)], fill=KAYU_GELAP)
    # Karpet songket di atas panggung
    d.rectangle([18, 55, 77, 61], fill=SONGKET_MERAH)
    for x in range(20, 76, 6):
        d.rectangle([x, 56, x + 3, 58], fill=SONGKET_EMAS)

    # 2. Tiang Penyangga Lumbung (4 tiang bambu/kayu kokoh)
    for x in (14, 30, 64, 80):
        d.rectangle([x, 26, x + 3, 55], fill=KAYU_GELAP)
        d.rectangle([x + 1, 26, x + 2, 54], fill=KAYU_COKLAT)

    # 3. Tirai Songket Latar Belakang (Merah, Emas, Toska)
    d.rectangle([18, 28, 77, 54], fill=SONGKET_UNGU)
    # Panel songket merah & emas
    d.rectangle([20, 30, 36, 52], fill=SONGKET_MERAH)
    d.rectangle([38, 30, 57, 52], fill=SONGKET_EMAS)
    d.rectangle([59, 30, 75, 52], fill=SONGKET_HIJAU)
    for y in range(32, 52, 4):
        d.line([(22, y), (34, y)], fill=SONGKET_EMAS)
        d.line([(40, y), (55, y)], fill=SONGKET_MERAH)
        d.line([(61, y), (73, y)], fill=SONGKET_EMAS)

    # 4. Spanduk "SELAMAT MENIKAH - SASAK WEDDING"
    d.rectangle([22, 19, 73, 27], fill=SONGKET_UNGU)
    d.rectangle([23, 20, 72, 26], fill=SONGKET_MERAH)
    d.rectangle([22, 19, 73, 20], fill=SONGKET_EMAS)
    d.rectangle([22, 26, 73, 27], fill=SONGKET_EMAS)
    # Teks simulasi pixel
    for x in range(26, 70, 3):
        d.point((x, 22), fill=SONGKET_EMAS)
        d.point((x + 1, 24), fill=SONGKET_EMAS)

    # 5. Atap Lumbung Sasak Melengkung (Bentuk perahu khas dengan ujung melengkung naik tinggi)
    # Titik kurva atap jerami
    kurva_atap = [
        (2, 6), (12, 14), (28, 20), (48, 22), (68, 20), (84, 14), (94, 6),
        (88, 16), (72, 24), (48, 26), (24, 24), (8, 16)
    ]
    d.polygon(kurva_atap, fill=JERAMI_ATAP)
    # Detail tekstur jerami
    for x in range(6, 90, 4):
        tinggi_atap = 10 + int(math.sin(x / 90 * math.pi) * 14)
        d.line([(x, 8), (x, tinggi_atap)], fill=JERAMI_GELAP)
        d.line([(x + 1, 8), (x + 1, tinggi_atap)], fill=JERAMI_TERANG)

    # Ujung runcing puncak atap lumbung (kiri & kanan)
    d.polygon([(0, 2), (5, 8), (2, 9)], fill=JERAMI_TERANG)
    d.polygon([(95, 2), (90, 8), (93, 9)], fill=JERAMI_TERANG)

    # 6. Roncean Bunga Kamboja & Melati menjuntai di bawah atap
    for x in range(16, 81, 5):
        d.rectangle([x, 27, x + 2, 29], fill=(255, 255, 240, 255))
        d.point((x + 1, 28), fill=(255, 220, 80, 255))
        d.point((x + 1, 30), fill=(255, 255, 240, 255))

    # 7. Sesaji & Buah-buahan di depan panggung
    for x in (24, 38, 54, 68):
        d.rectangle([x, 50, x + 6, 54], fill=(220, 180, 110, 255))
        d.point((x + 1, 51), fill=(220, 60, 50, 255)) # buah merah
        d.point((x + 3, 51), fill=(240, 210, 60, 255)) # pisang
        d.point((x + 5, 51), fill=(80, 160, 70, 255))

    return garis_luar(img)


def prop_pengantin_sasak_pria():
    """Mempelai Pria Sasak duduk di pelaminan."""
    img, d = kanvas(20, 32)
    kulit = (240, 196, 156, 255)
    d.rectangle([4, 18, 15, 30], fill=SONGKET_MERAH) # Kain songket duduk
    d.rectangle([5, 10, 14, 20], fill=(36, 32, 40, 255)) # Rompi hitam
    d.rectangle([8, 11, 11, 16], fill=(250, 246, 238, 255)) # Kemeja putih
    # Kalung emas
    d.line([(7, 12), (12, 12)], fill=SONGKET_EMAS)
    d.point((9, 13), fill=SONGKET_EMAS)
    # Kepala & Sapuk
    d.rectangle([6, 5, 13, 11], fill=kulit)
    d.rectangle([5, 2, 14, 6], fill=(36, 32, 40, 255))
    d.line([(5, 5), (14, 5)], fill=SONGKET_EMAS)
    d.polygon([(12, 2), (15, 0), (14, 4)], fill=(36, 32, 40, 255))
    # Wajah
    d.point((8, 8), fill=(40, 30, 36, 255))
    d.point((11, 8), fill=(40, 30, 36, 255))
    d.line([(9, 10), (10, 10)], fill=(200, 120, 110, 255))
    return garis_luar(img)


def prop_pengantin_sasak_wanita():
    """Mempelai Wanita Sasak dengan mahkota Lambung emas agung."""
    img, d = kanvas(20, 32)
    kulit = (246, 206, 170, 255)
    d.rectangle([4, 18, 15, 30], fill=SONGKET_MERAH) # Songket
    for y in range(20, 30, 3):
        for x in (6, 10, 13):
            d.point((x, y), fill=SONGKET_EMAS)
    d.rectangle([5, 11, 14, 19], fill=SONGKET_MERAH) # Lambung merah
    d.line([(5, 16), (14, 16)], fill=SONGKET_EMAS)
    # Kepala
    d.rectangle([6, 6, 13, 12], fill=kulit)
    # Mahkota Lambung Emas Megah bertingkat
    d.polygon([(4, 5), (9, 0), (14, 5)], fill=SONGKET_EMAS)
    d.polygon([(6, 4), (9, 1), (12, 4)], fill=(255, 230, 130, 255))
    d.rectangle([4, 5, 14, 7], fill=SONGKET_EMAS)
    for x in (5, 7, 9, 11, 13):
        d.point((x, 1), fill=(255, 230, 130, 255))
    # Anting & melati
    d.point((4, 9), fill=SONGKET_EMAS)
    d.point((14, 9), fill=SONGKET_EMAS)
    d.point((3, 10), fill=(255, 255, 240, 255))
    d.point((15, 10), fill=(255, 255, 240, 255))
    # Wajah
    d.point((8, 8), fill=(40, 30, 36, 255))
    d.point((11, 8), fill=(40, 30, 36, 255))
    d.line([(9, 10), (10, 10)], fill=(210, 100, 110, 255))
    return garis_luar(img)


def prop_candi_bentar():
    """Gerbang terbelah Candi Bentar bata merah khas Lombok."""
    img, d = kanvas(64, 52)
    # Sisi Kiri
    d.rectangle([4, 20, 24, 50], fill=BATA_MERAH)
    d.rectangle([2, 14, 22, 20], fill=BATA_MERAH)
    d.rectangle([0, 8, 20, 14], fill=BATA_TERANG)
    d.rectangle([2, 2, 18, 8], fill=BATA_MERAH)
    d.polygon([(4, 2), (16, 2), (10, 0)], fill=BATA_TERANG)
    # Nat bata kiri
    for y in range(4, 50, 4):
        d.line([(4, y), (24, y)], fill=BATA_GELAP)

    # Sisi Kanan (simetris terbelah)
    d.rectangle([40, 20, 60, 50], fill=BATA_MERAH)
    d.rectangle([42, 14, 62, 20], fill=BATA_MERAH)
    d.rectangle([44, 8, 64, 14], fill=BATA_TERANG)
    d.rectangle([46, 2, 62, 8], fill=BATA_MERAH)
    d.polygon([(48, 2), (60, 2), (54, 0)], fill=BATA_TERANG)
    # Nat bata kanan
    for y in range(4, 50, 4):
        d.line([(40, y), (60, y)], fill=BATA_GELAP)

    # Ukiran hiasan emas di pilar gerbang
    d.rectangle([8, 24, 20, 28], fill=SONGKET_EMAS)
    d.rectangle([44, 24, 56, 28], fill=SONGKET_EMAS)

    return garis_luar(img)


def prop_bale_saji():
    """Gubuk jerami tradisional berisi tumpukan sesaji kue Sasak & jajanan pasar."""
    img, d = kanvas(44, 48)
    # Tiang gubuk
    d.rectangle([6, 20, 9, 44], fill=KAYU_GELAP)
    d.rectangle([34, 20, 37, 44], fill=KAYU_GELAP)
    # Meja saji
    d.rectangle([4, 28, 39, 44], fill=KAYU_COKLAT)
    d.rectangle([2, 26, 41, 29], fill=KAYU_GELAP)
    # Susunan piring sesaji bertingkat (kue cerorot, kelemben, renggi)
    for x, y in ((8, 20), (18, 18), (28, 20)):
        d.ellipse([x, y, x + 8, y + 6], fill=(236, 188, 110, 255))
        d.polygon([(x + 4, y - 4), (x + 1, y + 2), (x + 7, y + 2)], fill=(244, 214, 140, 255))
    # Atap jerami piramida
    d.polygon([(2, 20), (22, 2), (41, 20)], fill=JERAMI_ATAP)
    for x in range(4, 40, 4):
        d.line([(x, 19), (22, 3)], fill=JERAMI_GELAP)
    return garis_luar(img)


def prop_pohon_kelapa():
    """Pohon kelapa meliuk khas pesisir pantai."""
    img, d = kanvas(44, 58)
    # Batang melengkung
    for i, y in enumerate(range(20, 56)):
        x = 22 + round(math.sin(i * 0.12) * 5.0)
        d.rectangle([x, y, x + 4, y], fill=(160, 126, 86, 255))
        if i % 3 == 0:
            d.point((x, y), fill=(120, 90, 56, 255))

    # Daun kelapa menjuntai
    for sudut in (170, 200, 230, 270, 310, 340, 10):
        t = math.radians(sudut)
        ux, uy = math.cos(t), math.sin(t)
        for j in range(4, 20):
            x = round(22 + ux * j)
            y = round(20 + uy * j + j * j * 0.038)
            warna = DAUN_PALEM if j > 10 else DAUN_TERANG
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=warna)

    # Buah kelapa hijau/emas
    d.ellipse([18, 18, 22, 22], fill=(188, 154, 60, 255))
    d.ellipse([24, 19, 28, 23], fill=(148, 178, 60, 255))
    return garis_luar(img)


def prop_pohon_pandan():
    """Pohon pandan laut dengan akar gantung seperti di kiri gambar."""
    img, d = kanvas(36, 44)
    # Akar tunjang / stilt roots
    for dx in (-10, -6, 0, 6, 10):
        d.line([(18, 24), (18 + dx, 42)], fill=(142, 108, 72, 255), width=2)
    # Batang utama
    d.rectangle([16, 14, 20, 26], fill=(158, 122, 84, 255))
    # Daun pandan berduri panjang melengkung
    for sudut in range(160, 381, 25):
        t = math.radians(sudut)
        for j in range(3, 16):
            x = round(18 + math.cos(t) * j)
            y = round(14 + math.sin(t) * j + j * 0.2)
            d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=DAUN_TERANG if j < 9 else DAUN_GELAP)
    return garis_luar(img)


def prop_obor_bambu():
    """Obor bambu pantai menyala."""
    img, d = kanvas(12, 38)
    # Tiang bambu
    d.rectangle([5, 12, 7, 36], fill=KAYU_BAMBU)
    d.rectangle([5, 12, 5, 36], fill=KAYU_GELAP)
    for y in (18, 24, 30):
        d.line([(5, y), (7, y)], fill=KAYU_GELAP)
    # Wadah tempurung api
    d.polygon([(3, 12), (9, 12), (7, 16), (5, 16)], fill=(110, 78, 48, 255))
    # Lidah api
    d.polygon([(4, 11), (8, 11), (6, 2)], fill=(255, 130, 40, 255))
    d.polygon([(5, 10), (7, 10), (6, 5)], fill=(255, 230, 90, 255))
    return garis_luar(img)


def prop_penari_sasak():
    """Penari adat Sasak (Gandrung/Presean) memeriahkan suasana pantai."""
    img, d = kanvas(22, 30)
    kulit = (240, 196, 156, 255)
    # Kain songket melilit
    d.polygon([(6, 16), (15, 16), (17, 26), (4, 26)], fill=SONGKET_MERAH)
    d.line([(4, 20), (17, 20)], fill=SONGKET_EMAS)
    # Badan telanjang dada / rompi dengan selendang
    d.rectangle([7, 11, 14, 16], fill=kulit)
    d.line([(7, 11), (14, 16)], fill=SONGKET_EMAS, width=2)
    # Tangan merentang menari
    d.line([(7, 12), (2, 8)], fill=kulit, width=2)
    d.line([(14, 12), (19, 8)], fill=kulit, width=2)
    # Kepala & Sapuk ikat
    d.rectangle([7, 4, 14, 10], fill=kulit)
    d.rectangle([6, 2, 15, 6], fill=(36, 32, 40, 255))
    d.line([(6, 5), (15, 5)], fill=SONGKET_EMAS)
    # Wajah ceria
    d.point((9, 7), fill=(40, 30, 36, 255))
    d.point((12, 7), fill=(40, 30, 36, 255))
    d.point((10, 9), fill=(210, 110, 100, 255))
    return garis_luar(img)


def prop_pemusik_gendang():
    """Pemain Gendang Beleq Sasak dengan drum besar."""
    img, d = kanvas(32, 32)
    kulit = (240, 196, 156, 255)
    # Gendang Beleq kayu bergaris merah & emas
    d.ellipse([12, 10, 30, 28], fill=(168, 88, 48, 255))
    d.ellipse([25, 11, 30, 27], fill=(244, 224, 184, 255)) # Kulit gendang
    d.line([(12, 19), (25, 19)], fill=SONGKET_EMAS, width=2)
    d.line([(14, 14), (27, 14)], fill=SONGKET_MERAH, width=2)
    d.line([(14, 24), (27, 24)], fill=SONGKET_MERAH, width=2)
    # Pemusik berdiri di samping gendang
    d.rectangle([2, 14, 11, 26], fill=(36, 32, 40, 255))
    d.rectangle([4, 6, 10, 12], fill=kulit)
    d.rectangle([3, 3, 11, 7], fill=(36, 32, 40, 255))
    d.line([(3, 6), (11, 6)], fill=SONGKET_EMAS)
    # Tangan memukul gendang
    d.line([(8, 12), (18, 16)], fill=kulit, width=2)
    return garis_luar(img)


def prop_perahu_jukung():
    """Perahu cadik tradisional Jukung di atas air laut pantai."""
    img, d = kanvas(44, 24)
    # Lambung perahu kayu warna-warni
    d.polygon([(2, 12), (40, 12), (36, 18), (6, 18)], fill=(248, 244, 236, 255))
    d.line([(3, 13), (39, 13)], fill=SONGKET_MERAH, width=2)
    d.line([(5, 16), (37, 16)], fill=LAUT_DALAM, width=2)
    # Cadik bambu penyangga
    d.line([(8, 8), (8, 20)], fill=KAYU_BAMBU, width=2)
    d.line([(32, 8), (32, 20)], fill=KAYU_BAMBU, width=2)
    d.line([(4, 20), (38, 20)], fill=KAYU_BAMBU, width=2)
    # Tiang layar kecil
    d.line([(20, 2), (20, 12)], fill=KAYU_GELAP, width=2)
    return garis_luar(img)


def prop_buku_tamu():
    """Meja buku tamu pantai bernuansa kayu & anyaman bambu."""
    img, d = kanvas(28, 30)
    d.rectangle([4, 14, 23, 27], fill=KAYU_COKLAT)
    d.rectangle([2, 12, 25, 15], fill=KAYU_GELAP)
    # Buku tamu terbuka dengan motif songket
    d.polygon([(4, 8), (23, 8), (24, 13), (3, 13)], fill=(255, 250, 242, 255))
    d.line([(13, 8), (13, 13)], fill=(210, 190, 170, 255))
    # Bunga kamboja di sudut meja
    d.rectangle([19, 10, 22, 13], fill=(255, 255, 240, 255))
    d.point((20, 11), fill=(255, 220, 90, 255))
    # Pena bulu
    d.line([(7, 4), (10, 10)], fill=SONGKET_MERAH, width=1)
    return garis_luar(img)


def prop_galeri():
    """Papan galeri foto kayu pantai dengan bingkai anyaman & songket."""
    img, d = kanvas(32, 34)
    d.line([(6, 33), (14, 12)], fill=KAYU_GELAP, width=2)
    d.line([(25, 33), (17, 12)], fill=KAYU_GELAP, width=2)
    d.line([(15, 18), (15, 33)], fill=KAYU_GELAP, width=2)
    d.rectangle([4, 3, 27, 24], fill=SONGKET_EMAS)
    d.rectangle([6, 5, 25, 22], fill=(250, 246, 238, 255))
    # Foto pasangan berlatar pantai Lombok
    d.rectangle([6, 5, 25, 13], fill=LAUT_1)
    d.rectangle([9, 14, 14, 21], fill=(42, 38, 42, 255)) # Pria
    d.rectangle([16, 14, 21, 21], fill=SONGKET_MERAH) # Wanita
    d.ellipse([10, 10, 13, 14], fill=(240, 196, 156, 255))
    d.ellipse([17, 10, 20, 14], fill=(246, 206, 170, 255))
    return garis_luar(img)


def prop_papan():
    """Papan jadwal acara pantai dari kayu jati & hiasan kerang."""
    img, d = kanvas(30, 34)
    d.rectangle([13, 18, 16, 32], fill=KAYU_GELAP)
    d.rectangle([3, 4, 26, 20], fill=KAYU_COKLAT)
    d.rectangle([5, 6, 24, 18], fill=(255, 248, 236, 255))
    d.rectangle([6, 7, 23, 9], fill=SONGKET_MERAH)
    for y in (11, 13, 15):
        d.line([(7, y), (22, y)], fill=(160, 140, 120, 255))
    # Hiasan kerang
    d.point((4, 5), fill=(255, 220, 120, 255))
    d.point((25, 5), fill=(255, 220, 120, 255))
    return garis_luar(img)


def prop_hadiah():
    """Kotak amplop digital anyaman bambu & ukiran motif Sasak."""
    img, d = kanvas(28, 30)
    d.rectangle([3, 11, 24, 26], fill=KAYU_COKLAT)
    d.rectangle([2, 7, 25, 12], fill=KAYU_GELAP)
    d.rectangle([3, 8, 24, 10], fill=SONGKET_EMAS)
    # Lubang amplop
    d.rectangle([8, 9, 19, 10], fill=(42, 32, 30, 255))
    # Motif songket wajik di kotak
    for y in range(14, 24, 4):
        for x in range(6, 22, 5):
            d.point((x, y), fill=SONGKET_MERAH)
            d.point((x + 1, y), fill=SONGKET_EMAS)
    return garis_luar(img)


def prop_bangku():
    """Kursi santai rotan pantai."""
    img, d = kanvas(28, 20)
    d.rectangle([3, 3, 24, 6], fill=KAYU_BAMBU)
    d.rectangle([2, 8, 25, 12], fill=KAYU_COKLAT)
    d.rectangle([4, 12, 6, 18], fill=KAYU_GELAP)
    d.rectangle([21, 12, 23, 18], fill=KAYU_GELAP)
    return garis_luar(img)


PROPERTI_LOMBOK = {
    "pelaminan": prop_pelaminan_lumbung,
    "pengantin_pria": prop_pengantin_sasak_pria,
    "pengantin_wanita": prop_pengantin_sasak_wanita,
    "gerbang": prop_candi_bentar,
    "bale_saji": prop_bale_saji,
    "buku_tamu": prop_buku_tamu,
    "galeri": prop_galeri,
    "papan": prop_papan,
    "hadiah": prop_hadiah,
    "pohon_kelapa": prop_pohon_kelapa,
    "pohon_pandan": prop_pohon_pandan,
    "obor_bambu": prop_obor_bambu,
    "penari_sasak": prop_penari_sasak,
    "pemusik_gendang": prop_pemusik_gendang,
    "perahu_jukung": prop_perahu_jukung,
    "bangku": prop_bangku,
}


def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    nama_tile = buat_tileset()
    nama_tepi = buat_tepi()
    buat_karakter_sasak("karakter_pria", PALET_PRIA_SASAK, wanita=False)
    buat_karakter_sasak("karakter_wanita", PALET_WANITA_SASAK, wanita=True)
    for nama, fungsi in PROPERTI_LOMBOK.items():
        perbesar(fungsi()).save(KELUARAN / f"{nama}.png")

    print("=== Sukses Membuat Aset Tema 2: Pantai Lombok ===")
    print("Tileset :", ", ".join(f"{i}={n}" for i, n in enumerate(nama_tile)))
    print("Tepi    :", ", ".join(f"{i}={n}" for i, n in enumerate(nama_tepi)))
    print("Karakter: karakter_pria.png, karakter_wanita.png")
    print("Properti:", ", ".join(PROPERTI_LOMBOK.keys()))
    print("Disimpan di:", KELUARAN)


if __name__ == "__main__":
    main()
