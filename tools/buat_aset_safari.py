"""Generator Aset Pixel Art Lengkap untuk Tema 6: "Taman Safari / Kebun Binatang Rimba Tropis".

Aset yang dihasilkan:
- tileset.png (13 ubin 48x48: rumput savana, rumput hutan, jalur kerikil, air kolam, teratai, pagar kayu, dll)
- gajah.png (Gajah safari dengan kalung bunga nusantara)
- jerapah.png (Jerapah tinggi leher jenjang totol safari)
- singa.png (Singa raja rimba bersurai di bukit batu)
- panda.png (Panda gemas duduk makan rebung bambu)
- zebra.png (Zebra belang hitam putih)
- flamingo.png (Burung flamingo pink anggun di air)
- pelaminan.png (Pelaminan kayu rustik safari, anggrek hutan, kanopi bambu)
- papan.png (Plang kayu petunjuk arah safari acara)
- galeri.png (Jemuran foto tali rami safari)
- buku_tamu.png (Pos ranger safari lodge RSVP)
- hadiah.png (Peti koper kulit petualang vintage)
- bangku.png (Bangku kayu gelondongan safari yang bisa diduduki)
- jeep_safari.png (Mobil jeep safari petualang 4x4)
- karakter_pria.png & karakter_wanita.png (Sprite sheet karakter safari explorer)
- pengantin_pria.png & pengantin_wanita.png
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game_safari"
UKURAN_PETAK = 48

def _w(r, g, b, a=255):
    return (r, g, b, a)

# Palet Safari Nature & Earth
HIJAU_RIMBA = _w(34, 76, 38)
HIJAU_TERANG = _w(58, 128, 54)
HIJAU_LUMUT = _w(44, 92, 48)
HIJAU_SAGE = _w(108, 156, 114)

SAVANA_EMAS = _w(206, 178, 108)
SAVANA_TERANG = _w(228, 204, 134)
SAVANA_GELAP = _w(172, 144, 82)

KERIKIL_DASAR = _w(216, 202, 172)
KERIKIL_TERANG = _w(236, 226, 204)
KERIKIL_GELAP = _w(180, 164, 134)

KAYU_JATI = _w(108, 64, 38)
KAYU_TERANG = _w(148, 92, 54)
KAYU_GELAP = _w(72, 40, 22)
KAYU_KULIT = _w(56, 32, 18)

AIR_TOSKA = _w(52, 154, 172)
AIR_KILAU = _w(112, 204, 218)
AIR_DALAM = _w(32, 112, 132)

EMAS_SAFARI = _w(224, 168, 48)
PUTIH_KREM = _w(250, 246, 238)
GARIS_LUAR = _w(28, 24, 20)

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

# ==============================================================================
# 1. TILESET SAFARI (48x48 Pixel Per Tile)
# ==============================================================================
def buat_tileset():
    # 13 tile x 48px = 624 x 48
    img, d = kanvas(UKURAN_PETAK * 13, UKURAN_PETAK)

    # Petak 0: Rumput Savana Emas Afrika
    ox = 0 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=SAVANA_EMAS)
    for y in range(0, 48, 6):
        for x in range(0, 48, 6):
            if (x + y * 3) % 7 == 0: d.point((ox + x, y), fill=SAVANA_TERANG)
            elif (x * 3 + y) % 11 == 0: d.point((ox + x, y), fill=SAVANA_GELAP)

    # Petak 1: Rumput Rimba Tropis Hijau Segar
    ox = 1 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=HIJAU_RIMBA)
    for y in range(0, 48, 6):
        for x in range(0, 48, 6):
            if (x * 5 + y) % 8 == 0: d.point((ox + x, y), fill=HIJAU_TERANG)
            elif (x + y * 7) % 9 == 0: d.point((ox + x, y), fill=HIJAU_LUMUT)
    # Bunga hutan kecil
    d.point((ox + 12, 14), fill=_w(255, 220, 100))
    d.point((ox + 34, 32), fill=_w(255, 160, 180))

    # Petak 2: Jalur Setapak Kerikil Safari (Gravel Trail)
    ox = 2 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=KERIKIL_DASAR)
    for y in range(0, 48, 4):
        for x in range(0, 48, 4):
            if (x * 7 + y * 5) % 6 == 0: d.point((ox + x, y), fill=KERIKIL_TERANG)
            elif (x * 3 + y * 9) % 7 == 0: d.point((ox + x, y), fill=KERIKIL_GELAP)
    # Batu kerikil kecil lonjong
    for bx, by in [(8, 12), (24, 28), (38, 10), (16, 38)]:
        d.ellipse([ox + bx, by, ox + bx + 3, by + 2], fill=KERIKIL_GELAP)

    # Petak 3: Air Kolam Jernih Biru Toska
    ox = 3 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=AIR_TOSKA)
    for y in range(0, 48, 8):
        for x in range(0, 48, 12):
            d.line([(ox + x, y), (ox + x + 6, y)], fill=AIR_KILAU)
            d.line([(ox + x + 6, y + 4), (ox + x + 10, y + 4)], fill=AIR_DALAM)

    # Petak 4: Air Kolam dengan Daun Teratai & Bunga Teratai Pink
    ox = 4 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=AIR_TOSKA)
    # Daun Teratai bulat dengan celah
    d.ellipse([ox + 10, 12, ox + 36, 36], fill=HIJAU_TERANG)
    d.polygon([(ox + 23, 24), (ox + 36, 18), (ox + 36, 30)], fill=AIR_TOSKA)
    # Bunga Teratai Pink di atasnya
    d.ellipse([ox + 20, 18, ox + 28, 26], fill=_w(255, 140, 180))
    d.point((ox + 24, 22), fill=_w(255, 240, 120))

    # Petak 5: Pagar Kayu Safari Alami Horizontal
    ox = 5 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=HIJAU_RIMBA)
    # Tiang pagar
    d.rectangle([ox + 4, 8, ox + 10, 44], fill=KAYU_JATI)
    d.rectangle([ox + 38, 8, ox + 44, 44], fill=KAYU_JATI)
    # Palang ganda kayu
    d.rectangle([ox, 14, ox + 47, 20], fill=KAYU_TERANG)
    d.rectangle([ox, 28, ox + 47, 34], fill=KAYU_TERANG)
    d.line([(ox, 14), (ox + 47, 14)], fill=KAYU_KULIT)
    d.line([(ox, 28), (ox + 47, 28)], fill=KAYU_KULIT)

    # Petak 6: Tebing Batu Safari / Bukit Karang
    ox = 6 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(118, 108, 98))
    for y in range(0, 48, 8):
        d.line([(ox, y), (ox + 47, y)], fill=_w(148, 138, 126))
        d.line([(ox, y + 1), (ox + 47, y + 1)], fill=_w(88, 78, 70))

    # Petak 7: Paving Batu Kali Bundar (Riverstone Court)
    ox = 7 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(140, 132, 120))
    for cy in (8, 24, 40):
        for cx in (8, 24, 40):
            d.ellipse([ox + cx - 6, cy - 6, ox + cx + 6, cy + 6], fill=_w(176, 168, 154))
            d.ellipse([ox + cx - 4, cy - 4, ox + cx + 4, cy + 4], fill=_w(198, 190, 178))

    # Petak 8: Rumpun Bambu Hijau Lebat
    ox = 8 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=HIJAU_RIMBA)
    for bx in (10, 24, 38):
        d.rectangle([ox + bx - 3, 0, ox + bx + 3, 47], fill=_w(92, 168, 64))
        for by in range(0, 48, 12):
            d.line([(ox + bx - 3, by), (ox + bx + 3, by)], fill=HIJAU_LUMUT, width=2)
        # Daun bambu lancip
        d.polygon([(ox + bx, 16), (ox + bx - 8, 22), (ox + bx, 20)], fill=HIJAU_TERANG)
        d.polygon([(ox + bx, 32), (ox + bx + 8, 38), (ox + bx, 36)], fill=HIJAU_TERANG)

    # Petak 9: Semak Rimbun Hutan Tropis
    ox = 9 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=HIJAU_RIMBA)
    d.ellipse([ox + 4, 4, ox + 43, 43], fill=HIJAU_LUMUT)
    d.ellipse([ox + 8, 8, ox + 39, 39], fill=HIJAU_TERANG)
    for p in [(16, 16), (30, 20), (22, 32)]:
        d.point((ox + p[0], p[1]), fill=_w(255, 120, 140)) # Bunga liar

    # Petak 10: Jembatan Kayu Papan Log
    ox = 10 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=KAYU_JATI)
    for y in range(0, 48, 8):
        d.line([(ox, y), (ox + 47, y)], fill=KAYU_TERANG)
        d.line([(ox, y + 7), (ox + 47, y + 7)], fill=KAYU_KULIT)
    # Tali rami di sisi kiri-kanan
    d.line([(ox + 2, 0), (ox + 2, 47)], fill=SAVANA_EMAS, width=2)
    d.line([(ox + 45, 0), (ox + 45, 47)], fill=SAVANA_EMAS, width=2)

    # Petak 11: Pasir Oranye Savana Camp
    ox = 11 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(214, 154, 94))
    for y in range(0, 48, 6):
        for x in range(0, 48, 6):
            if (x * 3 + y * 7) % 8 == 0: d.point((ox + x, y), fill=_w(236, 178, 116))

    # Petak 12: Batas Tepi Pohon Rimbun Gelap
    ox = 12 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(22, 44, 24))
    for y in range(0, 48, 8):
        for x in range(0, 48, 8):
            if (x + y) % 12 == 0: d.point((ox + x, y), fill=_w(32, 64, 34))

    img.save(KELUARAN / "tileset.png")

# ==============================================================================
# 2. SATWA-SATWA KEBUN BINATANG (ZOO ANIMALS PIXEL ART)
# ==============================================================================
def prop_gajah():
    w, h = 88, 70
    img, d = kanvas(w, h)
    cx = 44
    abu = _w(126, 134, 144)
    abu_terang = _w(156, 164, 176)
    abu_gelap = _w(96, 102, 112)

    # 4 Kaki Gajah Kokoh
    for kx in (18, 30, 56, 68):
        d.rectangle([kx, 42, kx + 10, 66], fill=abu_gelap)
        d.rectangle([kx + 2, 42, kx + 8, 64], fill=abu)
        d.ellipse([kx + 1, 62, kx + 9, 67], fill=_w(220, 220, 225)) # Kuku

    # Badan Gajah Bulat Besar
    d.ellipse([16, 16, 76, 56], fill=abu)
    d.ellipse([20, 18, 72, 50], fill=abu_terang)

    # Ekor Gajah
    d.line([(16, 32), (10, 48)], fill=abu_gelap, width=2)
    d.point((9, 49), fill=GARIS_LUAR)

    # Kepala & Belalai
    d.ellipse([54, 10, 84, 40], fill=abu)
    # Telinga Lebar Khas Gajah
    d.ellipse([46, 14, 62, 38], fill=abu_terang)
    d.arc([46, 14, 62, 38], 90, 270, fill=_w(200, 160, 170), width=2)

    # Belalai Melengkung Ramah ke Atas
    d.arc([72, 22, 88, 52], 270, 90, fill=abu, width=7)
    d.arc([76, 20, 84, 36], 180, 360, fill=abu_terang, width=5)

    # Gading Putih Gajah
    d.polygon([(74, 30), (84, 32), (76, 34)], fill=_w(255, 252, 240))

    # Mata Gajah Ramah
    d.point((68, 20), fill=GARIS_LUAR)
    d.point((69, 19), fill=_w(255, 255, 255))

    # Kalung Rangkaian Bunga Melati & Anggrek Pernikahan
    for bx in range(48, 70, 4):
        d.ellipse([bx, 34, bx + 4, 38], fill=_w(255, 255, 240))
        d.point((bx + 2, 36), fill=_w(255, 120, 160)) # Aksen pink

    return garis_luar(img)

def prop_jerapah():
    w, h = 56, 104
    img, d = kanvas(w, h)
    emas = _w(236, 184, 76)
    emas_terang = _w(252, 212, 114)
    totol = _w(156, 92, 34)

    # Kaki-kaki Panjang Jerapah
    for kx in (16, 22, 34, 40):
        d.line([(kx, 66), (kx, 98)], fill=emas, width=3)
        d.rectangle([kx - 2, 96, kx + 2, 100], fill=GARIS_LUAR) # Kuku

    # Badan Jerapah Miring
    d.polygon([(14, 52), (44, 46), (42, 68), (16, 68)], fill=emas)
    d.ellipse([18, 50, 28, 58], fill=totol)
    d.ellipse([30, 54, 40, 64], fill=totol)

    # Ekor Jerapah
    d.line([(14, 54), (10, 74)], fill=emas, width=2)
    d.ellipse([8, 72, 12, 78], fill=totol)

    # Leher Sangat Jenjang ke Atas
    d.polygon([(36, 48), (44, 46), (36, 16), (30, 18)], fill=emas)
    d.polygon([(34, 46), (42, 44), (35, 18), (31, 20)], fill=emas_terang)
    # Totol di leher
    for ty in (22, 30, 38):
        d.ellipse([31, ty, 38, ty + 6], fill=totol)
    # Surai kecil di belakang leher
    for my in range(18, 46, 4):
        d.line([(29, my), (31, my)], fill=totol, width=2)

    # Kepala Jerapah
    d.ellipse([26, 8, 42, 20], fill=emas)
    d.ellipse([24, 12, 30, 18], fill=emas_terang) # Moncong
    d.point((25, 14), fill=totol) # Hidung
    d.point((34, 11), fill=GARIS_LUAR) # Mata
    d.point((35, 10), fill=_w(255, 255, 255))

    # Tanduk Lucu Kecil
    d.line([(34, 8), (34, 3)], fill=emas, width=2)
    d.ellipse([32, 2, 36, 6], fill=totol)
    d.line([(38, 8), (39, 4)], fill=emas, width=2)
    d.ellipse([37, 3, 41, 7], fill=totol)

    # Bunga Tropis Terselip di Telinga
    d.ellipse([40, 10, 46, 16], fill=_w(255, 90, 120))
    d.point((43, 13), fill=_w(255, 240, 80))

    return garis_luar(img)

def prop_singa():
    w, h = 68, 64
    img, d = kanvas(w, h)
    cokelat = _w(228, 164, 72)
    surai = _w(148, 72, 28)
    surai_gelap = _w(104, 46, 18)

    # Bukit Batu Singa
    d.polygon([(6, 60), (20, 44), (54, 44), (64, 60)], fill=_w(128, 118, 106))
    d.line([(6, 60), (64, 60)], fill=_w(96, 88, 78), width=2)

    # Badan Singa Sedang Bersantai
    d.ellipse([14, 30, 46, 48], fill=cokelat)
    d.rectangle([16, 42, 24, 52], fill=cokelat)
    d.rectangle([34, 42, 42, 52], fill=cokelat)

    # Ekor Berumbai
    d.arc([8, 24, 18, 44], 90, 270, fill=cokelat, width=2)
    d.ellipse([6, 24, 11, 29], fill=surai)

    # Surai Lebat Raja Rimba
    d.ellipse([32, 10, 60, 42], fill=surai)
    d.ellipse([34, 12, 58, 40], fill=surai_gelap)
    d.ellipse([36, 14, 56, 38], fill=surai)

    # Wajah Singa Gagah
    d.ellipse([40, 16, 54, 32], fill=cokelat)
    d.ellipse([42, 22, 50, 30], fill=_w(248, 230, 190))
    d.polygon([(45, 24), (47, 24), (46, 26)], fill=surai_gelap) # Hidung segitiga
    d.point((43, 19), fill=GARIS_LUAR) # Mata
    d.point((49, 19), fill=GARIS_LUAR)

    # Mahkota Bunga Kecil Romantis
    d.ellipse([41, 10, 45, 14], fill=_w(255, 230, 80))
    d.ellipse([47, 10, 51, 14], fill=_w(255, 120, 160))

    return garis_luar(img)

def prop_panda():
    w, h = 50, 54
    img, d = kanvas(w, h)
    putih = _w(248, 246, 242)
    hitam = _w(36, 34, 38)

    # Kaki Belakang Duduk
    d.ellipse([6, 34, 20, 48], fill=hitam)
    d.ellipse([30, 34, 44, 48], fill=hitam)

    # Badan Bulat Gembul
    d.ellipse([10, 20, 40, 46], fill=putih)

    # Tangan Panda Memegang Bambu
    d.ellipse([8, 24, 20, 36], fill=hitam)
    d.ellipse([30, 24, 42, 36], fill=hitam)

    # Batang Rebung Bambu Hijau
    d.rectangle([22, 14, 26, 44], fill=HIJAU_TERANG)
    d.line([(22, 24), (26, 24)], fill=HIJAU_LUMUT)
    d.line([(22, 34), (26, 34)], fill=HIJAU_LUMUT)
    d.polygon([(26, 18), (32, 14), (26, 16)], fill=_w(120, 210, 80))

    # Kepala Panda Bulat
    d.ellipse([12, 6, 38, 28], fill=putih)

    # Telinga Hitam Bulat
    d.ellipse([10, 4, 18, 12], fill=hitam)
    d.ellipse([32, 4, 40, 12], fill=hitam)

    # Lingkaran Mata Hitam Khas Panda
    d.ellipse([16, 12, 23, 20], fill=hitam)
    d.ellipse([27, 12, 34, 20], fill=hitam)
    d.point((19, 15), fill=_w(255, 255, 255))
    d.point((29, 15), fill=_w(255, 255, 255))

    # Hidung & Senyum Panda
    d.ellipse([23, 19, 27, 23], fill=hitam)
    d.arc([22, 20, 28, 25], 0, 180, fill=GARIS_LUAR)

    # Pita Kupu-Kupu Merah di Leher
    d.polygon([(21, 27), (25, 29), (21, 31)], fill=_w(238, 42, 64))
    d.polygon([(29, 27), (25, 29), (29, 31)], fill=_w(238, 42, 64))
    d.ellipse([23, 27, 27, 31], fill=_w(255, 214, 80))

    return garis_luar(img)

def prop_zebra():
    w, h = 66, 58
    img, d = kanvas(w, h)
    putih = _w(250, 250, 252)
    hitam = _w(30, 28, 34)

    # Kaki-Kaki Berbelang
    for kx in (18, 25, 42, 49):
        d.rectangle([kx, 36, kx + 4, 54], fill=putih)
        d.line([(kx, 42), (kx + 4, 42)], fill=hitam, width=1)
        d.line([(kx, 48), (kx + 4, 48)], fill=hitam, width=1)
        d.rectangle([kx - 1, 52, kx + 5, 56], fill=hitam) # Kuku

    # Badan Belang Zebra
    d.ellipse([14, 22, 50, 42], fill=putih)
    for zx in range(20, 46, 6):
        d.line([(zx, 22), (zx - 4, 42)], fill=hitam, width=2)

    # Ekor Berumbai
    d.line([(14, 26), (8, 42)], fill=putih, width=2)
    d.ellipse([6, 40, 10, 46], fill=hitam)

    # Leher & Kepala
    d.polygon([(40, 28), (52, 14), (58, 22), (46, 36)], fill=putih)
    d.line([(44, 22), (54, 26)], fill=hitam, width=2)
    d.line([(48, 16), (56, 20)], fill=hitam, width=2)

    # Surai Tegak Zebra
    for my in range(12, 30, 3):
        d.line([(46 - (my - 12) // 3, my), (49 - (my - 12) // 3, my)], fill=hitam, width=2)

    # Kepala & Moncong
    d.ellipse([48, 10, 62, 22], fill=putih)
    d.ellipse([56, 14, 64, 22], fill=hitam) # Moncong hitam
    d.point((54, 13), fill=GARIS_LUAR) # Mata
    d.point((55, 12), fill=_w(255, 255, 255))
    d.ellipse([49, 6, 53, 11], fill=putih) # Telinga

    return garis_luar(img)

def prop_flamingo():
    w, h = 38, 62
    img, d = kanvas(w, h)
    pink = _w(255, 128, 168)
    pink_terang = _w(255, 168, 198)
    pink_tua = _w(228, 78, 124)

    # Kaki Kurus Jenjang (Berdiri Satu Kaki di Air)
    d.line([(20, 34), (20, 58)], fill=_w(248, 156, 172), width=2)
    # Kaki satunya ditekuk khas flamingo
    d.line([(20, 38), (14, 44)], fill=_w(248, 156, 172), width=2)
    d.line([(14, 44), (20, 46)], fill=_w(248, 156, 172), width=2)
    # Riak air di kaki
    d.ellipse([14, 56, 26, 60], fill=_w(112, 204, 218, 180))

    # Badan Anggun Bulat
    d.ellipse([12, 20, 30, 36], fill=pink)
    d.ellipse([14, 22, 28, 34], fill=pink_terang)
    d.arc([14, 22, 26, 32], 0, 180, fill=pink_tua, width=1) # Sayap

    # Leher Melengkung Indah S-Shape
    d.arc([18, 6, 32, 26], 270, 90, fill=pink, width=3)
    d.arc([14, 2, 26, 16], 90, 270, fill=pink, width=3)

    # Kepala Flamingo
    d.ellipse([12, 4, 20, 12], fill=pink)
    d.point((15, 6), fill=GARIS_LUAR) # Mata
    # Paruh Melengkung ke Bawah Khas Flamingo
    d.polygon([(12, 8), (6, 14), (10, 14)], fill=_w(255, 230, 140))
    d.polygon([(6, 14), (7, 18), (10, 14)], fill=GARIS_LUAR) # Ujung paruh hitam

    return garis_luar(img)

# ==============================================================================
# 3. PROPERTI PERNIKAHAN SAFARI TROPIS
# ==============================================================================
def prop_pelaminan_safari():
    w, h = 168, 104
    img, d = kanvas(w, h)
    # Panggung dasar kayu jati gelondongan
    d.rectangle([8, 80, 160, 100], fill=KAYU_GELAP)
    d.rectangle([12, 80, 156, 94], fill=KAYU_JATI)
    d.line([(8, 100), (160, 100)], fill=SAVANA_EMAS, width=2)

    # Tiang-tiang batang pohon jati alami
    for px in (18, 146):
        d.rectangle([px, 12, px + 8, 82], fill=KAYU_JATI)
        d.rectangle([px + 2, 12, px + 6, 82], fill=KAYU_TERANG)

    # Lengkungan Ranting Kayu Hutan & Daun Palem Tropis di Atas
    d.arc([24, 6, 144, 56], 180, 360, fill=KAYU_TERANG, width=5)
    # Daun monstera & palem tropis rimbun
    for dx in range(24, 146, 10):
        d.ellipse([dx - 6, 10, dx + 6, 24], fill=HIJAU_RIMBA)
        d.ellipse([dx - 4, 12, dx + 4, 22], fill=HIJAU_TERANG)
        # Bunga anggrek hutan warna-warni
        d.ellipse([dx - 3, 20, dx + 3, 26], fill=_w(255, 120, 180)) # Pink anggrek
        d.point((dx, 23), fill=_w(255, 230, 80))

    # Tirai Kanopi Kain Linen Safari Putih Krem
    d.rectangle([40, 22, 128, 80], fill=_w(248, 244, 234))
    d.rectangle([46, 26, 122, 78], fill=_w(255, 252, 246))

    # Lentera Bambu Gantung Hangat
    for lx in (36, 132):
        d.line([(lx, 20), (lx, 34)], fill=SAVANA_EMAS, width=2)
        d.rectangle([lx - 5, 34, lx + 5, 48], fill=KAYU_TERANG)
        d.ellipse([lx - 3, 36, lx + 3, 44], fill=_w(255, 240, 120)) # Lampu hangat

    # Sofa Kayu Rustik Beludru Hijau Lumut Safari
    d.rectangle([52, 58, 116, 82], fill=HIJAU_LUMUT)
    d.rectangle([50, 68, 118, 86], fill=HIJAU_SAGE)
    d.rectangle([50, 68, 56, 84], fill=KAYU_JATI)
    d.rectangle([112, 68, 118, 84], fill=KAYU_JATI)
    d.rectangle([58, 64, 72, 74], fill=_w(240, 234, 218)) # Bantal etnik
    d.rectangle([96, 64, 110, 74], fill=_w(240, 234, 218))

    return garis_luar(img)

def prop_papan_safari():
    w, h = 56, 76
    img, d = kanvas(w, h)
    # Tiang kayu gelondongan
    d.rectangle([25, 36, 31, 74], fill=KAYU_GELAP)
    d.rectangle([26, 36, 30, 74], fill=KAYU_TERANG)

    # 3 Plang Kayu Arah Bertingkat
    plang = [
        (6, 8, 48, 22, "AKAD & RESEPSI", True),
        (10, 24, 52, 38, "HABITAT SATWA", False),
        (8, 40, 46, 54, "PETA SAFARI", True)
    ]
    for x1, y1, x2, y2, teks, kiri in plang:
        d.rectangle([x1, y1, x2, y2], fill=KAYU_JATI)
        d.rectangle([x1 + 2, y1 + 2, x2 - 2, y2 - 2], fill=KAYU_TERANG)
        d.point((x1 + 4, y1 + 4), fill=GARIS_LUAR) # Paku
        d.point((x2 - 4, y1 + 4), fill=GARIS_LUAR)
        # Garis teks simbolis
        d.line([(x1 + 8, (y1 + y2) // 2), (x2 - 8, (y1 + y2) // 2)], fill=_w(250, 244, 230), width=2)
        # Ujung panah
        if kiri:
            d.polygon([(x1, y1), (x1 - 4, (y1 + y2) // 2), (x1, y2)], fill=KAYU_TERANG)
        else:
            d.polygon([(x2, y1), (x2 + 4, (y1 + y2) // 2), (x2, y2)], fill=KAYU_TERANG)

    # Daun tanaman merambat di tiang
    for my in (14, 30, 48):
        d.ellipse([21, my, 27, my + 6], fill=HIJAU_TERANG)

    return garis_luar(img)

def prop_galeri_safari():
    w, h = 88, 76
    img, d = kanvas(w, h)
    # 2 Tiang Batang Bambu
    for bx in (8, 76):
        d.rectangle([bx, 8, bx + 5, 72], fill=_w(118, 172, 74))
        for by in range(8, 72, 14):
            d.line([(bx, by), (bx + 5, by)], fill=HIJAU_LUMUT, width=2)

    # Tali Rami Pembentang Foto
    d.line([(12, 22), (76, 26)], fill=SAVANA_EMAS, width=2)
    d.line([(12, 48), (76, 52)], fill=SAVANA_EMAS, width=2)

    # Foto-foto Prewedding Bergantung
    pos_foto = [(18, 18), (38, 20), (58, 22), (28, 44), (48, 46)]
    for fx, fy in pos_foto:
        d.rectangle([fx, fy, fx + 16, fy + 22], fill=KAYU_JATI)
        d.rectangle([fx + 2, fy + 2, fx + 14, fy + 20], fill=PUTIH_KREM)
        # Gambar siluet pengantin di foto
        d.ellipse([fx + 5, fy + 5, fx + 11, fy + 11], fill=_w(160, 110, 80))
        d.rectangle([fx + 4, fy + 12, fx + 12, fy + 18], fill=_w(60, 90, 60))
        # Jepitan kayu
        d.rectangle([fx + 6, fy - 2, fx + 10, fy + 2], fill=KAYU_TERANG)

    return garis_luar(img)

def prop_buku_tamu_safari():
    w, h = 84, 68
    img, d = kanvas(w, h)
    # Tenda Kanopi Safari Terpal Krem
    d.polygon([(4, 24), (42, 6), (80, 24)], fill=_w(238, 228, 208))
    d.line([(4, 24), (80, 24)], fill=SAVANA_GELAP, width=2)
    d.line([(42, 6), (42, 24)], fill=SAVANA_GELAP)

    # Tiang Penyangga Meja Jati
    d.rectangle([8, 24, 12, 64], fill=KAYU_JATI)
    d.rectangle([72, 24, 76, 64], fill=KAYU_JATI)

    # Meja Jati Pos Ranger
    d.rectangle([6, 36, 78, 64], fill=KAYU_GELAP)
    d.rectangle([4, 34, 80, 42], fill=KAYU_TERANG)
    d.line([(4, 42), (80, 42)], fill=KAYU_KULIT, width=2)

    # Buku Jurnal Tamu Terbuka
    d.rectangle([14, 26, 34, 36], fill=_w(248, 242, 230))
    d.line([(24, 26), (24, 36)], fill=KAYU_GELAP)
    for ly in (29, 33):
        d.line([(16, ly), (22, ly)], fill=_w(120, 110, 100))
        d.line([(26, ly), (32, ly)], fill=_w(120, 110, 100))

    # Topi Ranger Safari di Meja
    d.ellipse([54, 28, 70, 36], fill=_w(188, 154, 104))
    d.ellipse([58, 24, 66, 32], fill=_w(156, 124, 80))

    # Vas Bunga Liar & Daun Palem
    d.rectangle([40, 26, 46, 36], fill=_w(180, 100, 60)) # Pot tembikar
    d.ellipse([38, 18, 48, 28], fill=HIJAU_TERANG)
    d.point((43, 20), fill=_w(255, 180, 60))

    return garis_luar(img)

def prop_hadiah_safari():
    w, h = 54, 58
    img, d = kanvas(w, h)
    # Peti Koper Kulit Petualang Vintage (Explorer Trunk)
    d.rectangle([8, 20, 46, 52], fill=_w(118, 68, 38))
    d.rectangle([10, 22, 44, 50], fill=_w(148, 88, 50))
    # Tali sabuk kulit penutup & gesper kuningan
    for sx in (16, 36):
        d.rectangle([sx, 18, sx + 4, 52], fill=_w(78, 42, 22))
        d.rectangle([sx, 32, sx + 4, 36], fill=EMAS_SAFARI) # Gesper kuningan
    # Sudut pelindung kuningan peti
    for cx in (8, 42):
        for cy in (20, 48):
            d.rectangle([cx, cy, cx + 4, cy + 4], fill=EMAS_SAFARI)
    # Gagang jinjing kulit di atas
    d.arc([22, 14, 32, 24], 180, 360, fill=_w(78, 42, 22), width=2)

    # Bukaan amplop digital & QRIS kecil elegan
    d.rectangle([21, 26, 33, 30], fill=_w(248, 246, 240))
    d.line([(21, 28), (33, 28)], fill=EMAS_SAFARI)

    # Pita Daun & Anggrek Safari
    d.ellipse([23, 16, 31, 22], fill=HIJAU_TERANG)
    d.point((27, 19), fill=_w(255, 100, 140))

    return garis_luar(img)

def prop_bangku_safari():
    w, h = 48, 44
    img, d = kanvas(w, h)
    # Kaki Bangku Kayu Gelondongan
    d.rectangle([8, 24, 14, 40], fill=KAYU_GELAP)
    d.rectangle([34, 24, 40, 40], fill=KAYU_GELAP)
    d.ellipse([8, 38, 14, 42], fill=KAYU_KULIT)
    d.ellipse([34, 38, 40, 42], fill=KAYU_KULIT)

    # Dudukan Kayu Log Alami Rata
    d.rectangle([4, 20, 44, 28], fill=KAYU_JATI)
    d.rectangle([6, 21, 42, 26], fill=KAYU_TERANG)
    d.line([(4, 28), (44, 28)], fill=KAYU_KULIT, width=2)

    # Sandaran Kayu Alami
    d.rectangle([6, 6, 42, 16], fill=KAYU_JATI)
    d.rectangle([8, 8, 40, 14], fill=KAYU_TERANG)
    # Tiang sandaran
    d.line([(10, 16), (10, 22)], fill=KAYU_GELAP, width=3)
    d.line([(38, 16), (38, 22)], fill=KAYU_GELAP, width=3)

    return garis_luar(img)

def prop_jeep_safari():
    w, h = 100, 60
    img, d = kanvas(w, h)
    khaki = _w(168, 146, 104)
    khaki_terang = _w(196, 174, 128)
    zaitun = _w(96, 108, 72)
    ban = _w(36, 36, 40)

    # 2 Roda Besar Off-Road
    for rx in (24, 76):
        d.ellipse([rx - 10, 36, rx + 10, 56], fill=ban)
        d.ellipse([rx - 6, 40, rx + 6, 52], fill=_w(180, 180, 185))
        d.ellipse([rx - 3, 43, rx + 3, 49], fill=ban)

    # Bodi Jeep 4x4 Terbuka
    d.rectangle([10, 24, 88, 46], fill=khaki)
    d.rectangle([12, 26, 86, 44], fill=khaki_terang)
    # Bemper depan & grill
    d.rectangle([84, 30, 94, 46], fill=zaitun)
    d.rectangle([92, 34, 96, 42], fill=_w(255, 230, 120)) # Lampu depan
    # Kaca Depan Miring Safari
    d.polygon([(64, 24), (72, 8), (76, 8), (72, 24)], fill=_w(120, 180, 210, 160))
    d.line([(64, 24), (72, 8)], fill=zaitun, width=3)
    # Roll-bar Tenda Terbuka Safari
    d.line([(20, 24), (20, 8), (68, 8)], fill=zaitun, width=3)
    d.line([(44, 24), (44, 8)], fill=zaitun, width=2)
    # Ban Cadangan di Belakang
    d.ellipse([4, 22, 16, 42], fill=ban)
    d.ellipse([7, 26, 13, 38], fill=_w(160, 160, 165))

    # Karangan Bunga Pernikahan di Kap Mesir
    for bx in range(66, 84, 5):
        d.ellipse([bx, 22, bx + 5, 27], fill=_w(255, 140, 170))
        d.point((bx + 2, 24), fill=_w(255, 240, 100))

    return garis_luar(img)

# ==============================================================================
# 4. KARAKTER SAFARI EXPLORER SPRITE SHEET (48x80 4 Arah 4 Frame)
# ==============================================================================
LEBAR_FRAME = 24
TINGGI_FRAME = 40
SKALA = 2

def frame_karakter_safari(arah, kolom, wanita=False):
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    cx = 12
    langkah = 0
    if kolom == 1: langkah = -1
    elif kolom == 3: langkah = 1

    kulit = _w(246, 212, 186)
    rambut = _w(44, 32, 24)

    if not wanita:
        # Pria: Busana Safari Explorer Casual Chic
        # Celana khaki safari
        d.rectangle([cx - 4 + langkah, 28, cx - 1 + langkah, 38], fill=_w(168, 142, 102))
        d.rectangle([cx + 1 - langkah, 28, cx + 4 - langkah, 38], fill=_w(168, 142, 102))
        d.rectangle([cx - 5 + langkah, 37, cx - 1 + langkah, 39], fill=_w(68, 44, 26)) # Sepatu bot cokelat
        d.rectangle([cx + 1 - langkah, 37, cx + 5 - langkah, 39], fill=_w(68, 44, 26))
        # Kemeja Safari Linen Krem dengan Saku
        d.rectangle([cx - 5, 17, cx + 5, 28], fill=_w(242, 234, 214))
        d.rectangle([cx - 5, 27, cx + 5, 29], fill=_w(96, 60, 34)) # Sabuk kulit
        if arah == "bawah":
            d.polygon([(cx - 2, 17), (cx + 2, 17), (cx, 22)], fill=kulit)
            # Saku kemeja safari
            d.rectangle([cx - 4, 21, cx - 2, 24], fill=_w(218, 208, 186))
            d.rectangle([cx + 2, 21, cx + 4, 24], fill=_w(218, 208, 186))
        d.ellipse([cx - 4, 9, cx + 4, 17], fill=kulit)
        d.ellipse([cx - 5, 6, cx + 5, 12], fill=rambut)
        # Topi Petualang Safari Fedor
        d.ellipse([cx - 6, 7, cx + 6, 11], fill=_w(188, 154, 104))
        d.ellipse([cx - 4, 4, cx + 4, 8], fill=_w(164, 130, 84))
        if arah != "atas":
            d.point((cx - 2, 14), fill=GARIS_LUAR)
            d.point((cx + 2, 14), fill=GARIS_LUAR)
    else:
        # Wanita: Gaun Safari Chic Warna Hijau Sage & Syal Sutra Terracotta
        gaun = HIJAU_SAGE
        gaun_terang = _w(138, 186, 144)
        d.polygon([(cx - 7 + langkah, 38), (cx + 7 - langkah, 38), (cx + 3, 22), (cx - 3, 22)], fill=gaun)
        d.line([(cx - 2, 23), (cx - 4 + langkah, 38)], fill=gaun_terang)
        d.line([(cx + 2, 23), (cx + 4 - langkah, 38)], fill=gaun_terang)
        d.rectangle([cx - 4, 17, cx + 4, 22], fill=gaun)
        # Syal sutra terracotta di leher
        if arah == "bawah":
            d.ellipse([cx - 3, 16, cx + 3, 20], fill=_w(214, 94, 68))
        d.line([(cx - 4, 18), (cx - 6, 24)], fill=kulit)
        d.line([(cx + 4, 18), (cx + 6, 24)], fill=kulit)
        d.ellipse([cx - 4, 9, cx + 4, 17], fill=kulit)
        d.ellipse([cx - 5, 6, cx + 5, 13], fill=rambut)
        d.ellipse([cx - 3, 4, cx + 3, 9], fill=rambut)
        # Hiasan bunga anggrek safari di rambut
        d.point((cx + 4, 7), fill=_w(255, 110, 160))
        d.point((cx + 3, 8), fill=_w(255, 230, 80))
        if arah != "atas":
            d.point((cx - 2, 13), fill=GARIS_LUAR)
            d.point((cx + 2, 13), fill=GARIS_LUAR)
            d.point((cx - 3, 14), fill=_w(255, 140, 160))
            d.point((cx + 3, 14), fill=_w(255, 140, 160))

    img = garis_luar(img)
    return img.resize((LEBAR_FRAME * SKALA, TINGGI_FRAME * SKALA), Image.NEAREST)

def buat_sprite_sheet_safari(nama_berkas, wanita=False):
    arah_urutan = ["bawah", "kiri", "kanan", "atas"]
    lembar = Image.new("RGBA", (4 * LEBAR_FRAME * SKALA, 4 * TINGGI_FRAME * SKALA), (0, 0, 0, 0))
    for baris, arah in enumerate(arah_urutan):
        for kolom in range(4):
            frame = frame_karakter_safari(arah, kolom, wanita=wanita)
            lembar.paste(frame, (kolom * LEBAR_FRAME * SKALA, baris * TINGGI_FRAME * SKALA))
    lembar.save(KELUARAN / nama_berkas)

def prop_pengantin_safari(wanita=False):
    img = frame_karakter_safari("bawah", 0, wanita=wanita)
    if wanita:
        w, h = img.size
        d = ImageDraw.Draw(img)
        d.polygon([(4, h - 4), (w - 4, h - 4), (w // 2 + 8, 48), (w // 2 - 8, 48)], fill=PUTIH_KREM)
        d.line([(w // 2 - 4, 50), (12, h - 4)], fill=_w(228, 222, 210), width=2)
        d.line([(w // 2 + 4, 50), (w - 12, h - 4)], fill=_w(228, 222, 210), width=2)
        # Mahkota bunga tropis safari
        cx = w // 2
        d.ellipse([cx - 8, 6, cx + 8, 14], outline=_w(255, 120, 160), width=2)
        d.point((cx, 6), fill=_w(255, 230, 80))
    return garis_luar(img)

# ==============================================================================
# MAIN
# ==============================================================================
def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    print("=== Menghasilkan Aset Pixel Art Tema 6: Taman Safari Kebun Binatang ===")

    print("[1] Membuat Tileset Safari...")
    buat_tileset()

    print("[2] Membuat Koleksi Satwa Kebun Binatang...")
    prop_gajah().save(KELUARAN / "gajah.png")
    prop_jerapah().save(KELUARAN / "jerapah.png")
    prop_singa().save(KELUARAN / "singa.png")
    prop_panda().save(KELUARAN / "panda.png")
    prop_zebra().save(KELUARAN / "zebra.png")
    prop_flamingo().save(KELUARAN / "flamingo.png")

    print("[3] Membuat Properti Safari...")
    prop_pelaminan_safari().save(KELUARAN / "pelaminan.png")
    prop_papan_safari().save(KELUARAN / "papan.png")
    prop_galeri_safari().save(KELUARAN / "galeri.png")
    prop_buku_tamu_safari().save(KELUARAN / "buku_tamu.png")
    prop_hadiah_safari().save(KELUARAN / "hadiah.png")
    prop_bangku_safari().save(KELUARAN / "bangku.png")
    prop_jeep_safari().save(KELUARAN / "jeep_safari.png")

    print("[4] Membuat Karakter Safari Explorer...")
    buat_sprite_sheet_safari("karakter_pria.png", wanita=False)
    buat_sprite_sheet_safari("karakter_wanita.png", wanita=True)
    prop_pengantin_safari(wanita=False).save(KELUARAN / "pengantin_pria.png")
    prop_pengantin_safari(wanita=True).save(KELUARAN / "pengantin_wanita.png")

    print(f"\n[SUKSES] Seluruh 16 aset Safari tersimpan di {KELUARAN}")

if __name__ == "__main__":
    main()
