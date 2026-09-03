"""Generator Aset Pixel Art Lengkap untuk Tema 5: "Grand Ballroom Gedung Mewah" (Modern Indoor-Outdoor).

Penyempurnaan Utama:
- HILANGKAN KOTAK-KOTAK KUNING PADA DINDING / BORDER (diganti panel marmer akustik mewah)
- JALAN RAYA ASPAL DENGAN MARKA PUTIH (Karpet merah TIDAK memotong jalan raya)
- KURSI CHIAVARI EMAS & MEJA BUNDAR BANQUET (Banyak kursi yang bisa diduduki)
- POT BUNGA EMAS & PILAR MEWAH
- TILESET DIPERHALUS
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "game_gedung"
UKURAN_PETAK = 48

def _w(r, g, b, a=255):
    return (r, g, b, a)

# Palet Modern Luxury
EMAS_KILAU = _w(255, 248, 180)
EMAS_TERANG = _w(246, 212, 86)
EMAS_DASAR = _w(218, 168, 46)
EMAS_BAYANG = _w(160, 116, 28)
EMAS_PEKAT = _w(96, 68, 16)

BELUDRU_MARUN = _w(128, 22, 42)
BELUDRU_GELAP = _w(82, 12, 26)
BELUDRU_TERANG = _w(168, 36, 62)

MARMER_PUTIH = _w(248, 246, 242)
MARMER_ABU = _w(226, 224, 218)
MARMER_URAT = _w(204, 200, 192)

PLAZA_ASPAL = _w(52, 56, 66)
PLAZA_TERANG = _w(68, 74, 88)
PLAZA_GELAP = _w(38, 42, 50)
JALAN_RAYA = _w(32, 36, 44)

DINDING_NAVY = _w(18, 24, 38)
DINDING_KACA = _w(32, 54, 78)

GARIS_LUAR = _w(24, 22, 28)

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
# 1. TILESET (48x48 Pixel Per Tile)
# ==============================================================================
def buat_tileset():
    # 17 tile x 48px = 816 x 48
    img, d = kanvas(UKURAN_PETAK * 17, UKURAN_PETAK)

    # Petak 0: Plaza Luar Aspal Halus
    ox = 0 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=PLAZA_ASPAL)
    for y in range(0, 48, 8):
        for x in range(0, 48, 8):
            if (x + y) % 16 == 0: d.point((ox + x, y), fill=PLAZA_TERANG)
            elif (x + y) % 24 == 0: d.point((ox + x, y), fill=PLAZA_GELAP)

    # Petak 1: Paving Block Plaza Interlocking Mewah
    ox = 1 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(92, 100, 116))
    for y in range(0, 48, 12):
        d.line([(ox, y), (ox + 47, y)], fill=_w(72, 78, 92))
    for x in range(0, 48, 12):
        d.line([(ox + x, 0), (ox + x, 47)], fill=_w(72, 78, 92))
    d.line([(ox, 0), (ox + 47, 0)], fill=_w(110, 118, 134))

    # Petak 2: Taman Plaza Hijau Rapi
    ox = 2 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(62, 116, 48))
    d.rectangle([ox + 4, 4, ox + 43, 43], fill=_w(74, 136, 56))
    for p in [(12, 12), (32, 16), (20, 32), (36, 36)]:
        d.point((ox + p[0], p[1]), fill=_w(255, 230, 120))

    # Petak 3: Jalan Raya Aspal dengan Marka Putih Putus-Putus
    ox = 3 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=JALAN_RAYA)
    for y in range(0, 48, 6):
        for x in range(0, 48, 6):
            if (x * 7 + y * 13) % 11 == 0:
                d.point((ox + x, y), fill=_w(44, 48, 58))
    # Marka putih di tengah (horizontal)
    d.rectangle([ox + 6, 22, ox + 42, 26], fill=_w(255, 255, 255))

    # Petak 4: Trotoar Granit / Raised Curb
    ox = 4 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=MARMER_ABU)
    d.line([(ox, 0), (ox + 47, 0)], fill=_w(255, 255, 255), width=2)
    d.line([(ox, 47), (ox + 47, 47)], fill=_w(140, 136, 128), width=2)
    for x in range(0, 48, 16):
        d.line([(ox + x, 0), (ox + x, 47)], fill=_w(180, 176, 168))

    # Petak 5: Karpet Merah Kiri (Red Carpet Sisi Kiri berlis emas kiri saja)
    ox = 5 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_MARUN)
    d.rectangle([ox + 6, 0, ox + 47, 47], fill=BELUDRU_TERANG)
    # Lis Bordir Emas HANYA di Kiri
    d.rectangle([ox, 0, ox + 4, 47], fill=EMAS_TERANG)
    d.line([(ox + 6, 0), (ox + 6, 47)], fill=EMAS_DASAR)

    # Petak 6: Pilar Eksterior Marmer Silinder
    ox = 6 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=PLAZA_GELAP)
    d.rectangle([ox + 8, 0, ox + 39, 47], fill=MARMER_ABU)
    d.rectangle([ox + 12, 0, ox + 35, 47], fill=MARMER_PUTIH)
    d.line([(ox + 8, 4), (ox + 39, 4)], fill=EMAS_TERANG, width=2)
    d.line([(ox + 8, 43), (ox + 39, 43)], fill=EMAS_TERANG, width=2)

    # Petak 7: Kaca Fasad Gedung Modern
    ox = 7 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=DINDING_KACA)
    d.line([(ox, 0), (ox + 47, 47)], fill=_w(74, 128, 168, 140), width=3)
    d.rectangle([ox, 0, ox + 47, 47], outline=_w(20, 30, 44), width=2)

    # Petak 8: Karpet Ballroom Beludru Marun Mewah Ornamen Emas
    ox = 8 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_GELAP)
    d.rectangle([ox + 2, 2, ox + 45, 45], fill=BELUDRU_MARUN)
    d.polygon([(ox + 24, 6), (ox + 42, 24), (ox + 24, 42), (ox + 6, 24)], outline=EMAS_TERANG)
    d.point((ox + 24, 24), fill=EMAS_KILAU)

    # Petak 9: Lantai Dansa Marmer Kilau Putih
    ox = 9 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=MARMER_PUTIH)
    d.line([(ox, 24), (ox + 47, 24)], fill=MARMER_URAT)
    d.line([(ox + 24, 0), (ox + 24, 47)], fill=MARMER_URAT)
    d.point((ox + 12, 12), fill=_w(255, 255, 255))
    d.point((ox + 36, 36), fill=_w(255, 255, 255))

    # Petak 10: Panggung Kayu Ballroom Polished
    ox = 10 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(64, 38, 22))
    for y in range(0, 48, 8):
        d.line([(ox, y), (ox + 47, y)], fill=_w(84, 50, 30))
        d.line([(ox, y + 7), (ox + 47, y + 7)], fill=_w(48, 26, 14))

    # Petak 11: Dinding Ballroom Panel Kayu Akustik & Marmer Krem (BEBAS KOTAK KUNING)
    ox = 11 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=_w(36, 20, 28))
    for x in range(0, 48, 8):
        d.line([(ox + x, 0), (ox + x, 47)], fill=_w(48, 26, 36))
    d.line([(ox, 2), (ox + 47, 2)], fill=EMAS_DASAR, width=2)
    d.line([(ox, 45), (ox + 47, 45)], fill=EMAS_DASAR, width=2)

    # Petak 12: Pilar Ballroom Marmer Kepala Emas
    ox = 12 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_GELAP)
    d.rectangle([ox + 6, 0, ox + 41, 47], fill=MARMER_PUTIH)
    d.rectangle([ox + 12, 0, ox + 35, 47], fill=_w(255, 255, 255))
    d.rectangle([ox + 4, 0, ox + 43, 6], fill=EMAS_TERANG)
    d.rectangle([ox + 4, 41, ox + 43, 47], fill=EMAS_TERANG)

    # Petak 13: Semak Hias / Boxwood Topiary Plaza Kota
    ox = 13 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=PLAZA_GELAP)
    d.rectangle([ox + 4, 4, ox + 43, 43], fill=_w(36, 78, 30))
    d.rectangle([ox + 8, 8, ox + 39, 39], fill=_w(48, 104, 38))
    for p in [(16, 16), (32, 20), (22, 30)]:
        d.point((ox + p[0], p[1]), fill=_w(88, 164, 68))

    # Petak 14: Karpet Merah Tengah (Beludru Merah Murni Tanpa Lis Samping)
    ox = 14 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_TERANG)
    for y in range(0, 48, 12):
        d.line([(ox, y), (ox + 47, y)], fill=_w(156, 28, 52))

    # Petak 15: Karpet Merah Kanan (Red Carpet Sisi Kanan berlis emas kanan saja)
    ox = 15 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_MARUN)
    d.rectangle([ox, 0, ox + 41, 47], fill=BELUDRU_TERANG)
    # Lis Bordir Emas HANYA di Kanan
    d.rectangle([ox + 43, 0, ox + 47, 47], fill=EMAS_TERANG)
    d.line([(ox + 41, 0), (ox + 41, 47)], fill=EMAS_DASAR)

    # Petak 16: Ujung Karpet Merah di Curb Berhias Rumbai Emas
    ox = 16 * UKURAN_PETAK
    d.rectangle([ox, 0, ox + 47, 47], fill=BELUDRU_TERANG)
    # Rumbai-rumbai emas di bawah (curb threshold)
    d.rectangle([ox, 40, ox + 47, 44], fill=EMAS_TERANG)
    for x in range(0, 48, 4):
        d.line([(ox + x, 44), (ox + x, 47)], fill=EMAS_KILAU, width=1)

    img.save(KELUARAN / "tileset.png")

# ==============================================================================
# 2. PROPERTI KURSI CHIAVARI EMAS (BISA DIDUDUKI)
# ==============================================================================
def prop_kursi():
    w, h = 36, 44
    img, d = kanvas(w, h)
    cx = 18
    # Kaki-kaki kursi emas
    d.line([(cx - 8, 26), (cx - 8, 42)], fill=EMAS_DASAR, width=2)
    d.line([(cx + 8, 26), (cx + 8, 42)], fill=EMAS_DASAR, width=2)
    d.line([(cx - 10, 24), (cx - 10, 38)], fill=EMAS_BAYANG, width=1)
    d.line([(cx + 10, 24), (cx + 10, 38)], fill=EMAS_BAYANG, width=1)
    # Penyangga horizontal kaki
    d.line([(cx - 8, 36), (cx + 8, 36)], fill=EMAS_TERANG, width=1)

    # Bantalan Kursi Beludru Marun Mewah
    d.rectangle([cx - 11, 20, cx + 11, 27], fill=BELUDRU_MARUN)
    d.rectangle([cx - 9, 21, cx + 9, 25], fill=BELUDRU_TERANG)
    d.line([(cx - 11, 27), (cx + 11, 27)], fill=EMAS_TERANG, width=1)

    # Sandaran Kursi Chiavari Emas
    d.line([(cx - 10, 4), (cx - 10, 21)], fill=EMAS_TERANG, width=2)
    d.line([(cx + 10, 4), (cx + 10, 21)], fill=EMAS_TERANG, width=2)
    # Batang lengkung atas
    d.arc([cx - 10, 2, cx + 10, 10], 180, 360, fill=EMAS_KILAU, width=2)
    # Jeruji vertikal Chiavari
    for sx in (-6, -2, 2, 6):
        d.line([(cx + sx, 6), (cx + sx, 20)], fill=EMAS_TERANG, width=1)
    # Palang horizontal sandaran
    d.line([(cx - 10, 12), (cx + 10, 12)], fill=EMAS_TERANG, width=1)

    return garis_luar(img)

# ==============================================================================
# 3. PROPERTI MEJA BUNDAR BANQUET DENGAN 4 KURSI
# ==============================================================================
def prop_meja_vip():
    w, h = 80, 72
    img, d = kanvas(w, h)
    cx, cy = 40, 36

    # 4 Kursi Chiavari di sekeliling meja (Belakang, Kiri, Kanan, Depan)
    # Kursi Belakang
    d.arc([cx - 8, 4, cx + 8, 16], 180, 360, fill=EMAS_TERANG, width=2)
    # Kursi Kiri
    d.line([(cx - 28, cy - 8), (cx - 28, cy + 8)], fill=EMAS_TERANG, width=2)
    # Kursi Kanan
    d.line([(cx + 28, cy - 8), (cx + 28, cy + 8)], fill=EMAS_TERANG, width=2)

    # Meja Bundar Taplak Putih Bersih
    d.ellipse([cx - 28, cy - 18, cx + 28, cy + 18], fill=MARMER_ABU)
    d.ellipse([cx - 26, cy - 17, cx + 26, cy + 16], fill=MARMER_PUTIH)
    d.ellipse([cx - 22, cy - 14, cx + 22, cy + 13], fill=_w(255, 255, 255))

    # Centerpiece Bunga Mawar Merah di Tengah Meja
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=EMAS_TERANG)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=_w(220, 32, 54))
    d.point((cx - 2, cy - 2), fill=_w(255, 255, 255))
    d.point((cx + 2, cy + 1), fill=_w(255, 214, 80))

    # Gelas Sampanye Kristal di Meja
    d.point((cx - 14, cy - 4), fill=_w(255, 240, 180))
    d.point((cx + 14, cy - 4), fill=_w(255, 240, 180))
    d.point((cx - 12, cy + 4), fill=_w(255, 240, 180))
    d.point((cx + 12, cy + 4), fill=_w(255, 240, 180))

    # Kursi Depan (Bantalan terlihat)
    d.rectangle([cx - 8, cy + 18, cx + 8, cy + 26], fill=BELUDRU_MARUN)
    d.line([(cx - 8, cy + 26), (cx + 8, cy + 26)], fill=EMAS_TERANG, width=1)

    return garis_luar(img)

# ==============================================================================
# 4. POT BUNGA EMAS PLAZA & BALLROOM
# ==============================================================================
def prop_pot_bunga():
    w, h = 36, 52
    img, d = kanvas(w, h)
    cx = 18
    # Pot Guci Emas
    d.rectangle([cx - 8, 30, cx + 8, 48], fill=EMAS_DASAR)
    d.rectangle([cx - 10, 28, cx + 10, 32], fill=EMAS_TERANG)
    d.line([(cx - 8, 48), (cx + 8, 48)], fill=EMAS_PEKAT, width=2)
    # Tanaman Hias Ficus / Palem Hijau Segar
    for dy, r in [(22, 10), (14, 12), (6, 8)]:
        d.ellipse([cx - r, dy - r // 2, cx + r, dy + r // 2], fill=_w(44, 98, 36))
        d.ellipse([cx - r + 2, dy - r // 2 + 1, cx + r - 2, dy + r // 2 - 1], fill=_w(60, 134, 48))
    d.point((cx, 10), fill=_w(120, 200, 80))
    return garis_luar(img)

# ==============================================================================
# 5. GRAND ENTRANCE PINTU MASUK
# ==============================================================================
def prop_pintu_gedung():
    w, h = 108, 96
    img, d = kanvas(w, h)
    # Kanopi drop-off atap lengkung emas
    d.rectangle([4, 6, 104, 22], fill=_w(24, 32, 46))
    d.rectangle([2, 18, 106, 26], fill=EMAS_DASAR)
    d.rectangle([6, 22, 102, 26], fill=EMAS_KILAU)
    # Lampu kristal kanopi bawah
    for x in range(16, 94, 12):
        d.point((x, 28), fill=EMAS_KILAU)
        d.line([(x, 28), (x, 32)], fill=EMAS_TERANG)
    # Tiang pilar marmer kiri dan kanan
    d.rectangle([8, 24, 20, 94], fill=MARMER_PUTIH)
    d.rectangle([10, 24, 18, 94], fill=_w(255, 255, 255))
    d.rectangle([6, 22, 22, 30], fill=EMAS_TERANG)
    d.rectangle([6, 88, 22, 94], fill=EMAS_TERANG)

    d.rectangle([88, 24, 100, 94], fill=MARMER_PUTIH)
    d.rectangle([90, 24, 98, 94], fill=_w(255, 255, 255))
    d.rectangle([86, 22, 102, 30], fill=EMAS_TERANG)
    d.rectangle([86, 88, 102, 94], fill=EMAS_TERANG)

    # Frame Pintu Kaca Geser Otomatis
    d.rectangle([22, 26, 86, 94], fill=DINDING_KACA)
    d.rectangle([24, 28, 84, 94], fill=_w(46, 78, 108, 180))
    # Pintu kaca tengah
    d.line([(54, 26), (54, 94)], fill=EMAS_TERANG, width=2)
    # Handle pintu emas
    d.rectangle([48, 52, 51, 74], fill=EMAS_KILAU)
    d.rectangle([57, 52, 60, 74], fill=EMAS_KILAU)
    # Karpet merah di depan pintu
    d.rectangle([32, 90, 76, 95], fill=BELUDRU_MARUN)
    d.line([(32, 90), (76, 90)], fill=EMAS_TERANG)

    return garis_luar(img)

# ==============================================================================
# 6. PELAMINAN GRAND BALLROOM
# ==============================================================================
def prop_pelaminan():
    w, h = 168, 104
    img, d = kanvas(w, h)
    # Panggung dasar kayu polished
    d.rectangle([8, 80, 160, 100], fill=_w(78, 46, 28))
    d.rectangle([12, 80, 156, 94], fill=_w(104, 62, 38))
    d.line([(8, 100), (160, 100)], fill=EMAS_TERANG, width=2)

    # Backdrop panel lengkung emas & marmer putih
    d.rectangle([20, 14, 148, 82], fill=MARMER_PUTIH)
    d.arc([48, 6, 120, 70], 180, 360, fill=EMAS_TERANG, width=3)
    d.rectangle([48, 38, 120, 82], outline=EMAS_TERANG, width=2)

    # Rangkaian Bunga Mawar Putih & Daun Eucalyptus di atas & samping
    for x in range(24, 146, 6):
        d.ellipse([x - 4, 10, x + 4, 18], fill=_w(255, 255, 250))
        d.point((x, 14), fill=_w(255, 226, 160))
        d.ellipse([x - 3, 16, x + 3, 22], fill=_w(108, 156, 114))

    # Chandelier Kristal Gantung di Tengah
    cx, cy = 84, 26
    d.line([(cx, 8), (cx, cy)], fill=EMAS_TERANG, width=2)
    for r, n in [(12, 8), (20, 12), (28, 16)]:
        d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=EMAS_KILAU, width=2)
    for dx in range(-20, 21, 6):
        d.line([(cx + dx, cy + 4), (cx + dx, cy + 12 + abs(dx) // 3)], fill=_w(255, 255, 255))
        d.point((cx + dx, cy + 13 + abs(dx) // 3), fill=EMAS_KILAU)

    # Standing Lamp Kristal di Kiri & Kanan Pelaminan
    for lx in (28, 140):
        d.rectangle([lx - 2, 36, lx + 2, 82], fill=EMAS_DASAR)
        d.ellipse([lx - 10, 30, lx + 10, 44], fill=EMAS_KILAU)
        d.point((lx, 37), fill=_w(255, 255, 255))

    # Sofa Pelaminan Beludru Putih Krem & Emas
    d.rectangle([54, 58, 114, 82], fill=_w(242, 238, 228))
    d.rectangle([50, 68, 118, 86], fill=_w(250, 248, 242))
    d.rectangle([50, 68, 56, 84], fill=EMAS_TERANG)
    d.rectangle([112, 68, 118, 84], fill=EMAS_TERANG)
    d.rectangle([60, 64, 72, 74], fill=EMAS_TERANG)
    d.rectangle([96, 64, 108, 74], fill=EMAS_TERANG)

    return garis_luar(img)

# ==============================================================================
# 7. PROPERTI LAINNYA (PAPAN, GALERI, BUKU TAMU, HADIAH, MOBIL, PIANO, KUE)
# ==============================================================================
def prop_papan():
    w, h = 48, 72
    img, d = kanvas(w, h)
    d.line([(14, 70), (24, 46)], fill=EMAS_PEKAT, width=2)
    d.line([(34, 70), (24, 46)], fill=EMAS_PEKAT, width=2)
    d.rectangle([6, 10, 42, 54], fill=EMAS_DASAR)
    d.rectangle([8, 12, 40, 52], fill=_w(14, 20, 32))
    d.rectangle([12, 16, 36, 20], fill=EMAS_KILAU)
    d.rectangle([14, 24, 34, 26], fill=_w(100, 200, 255))
    d.rectangle([14, 30, 34, 32], fill=_w(255, 255, 255))
    d.rectangle([16, 36, 32, 38], fill=_w(255, 255, 255))
    d.rectangle([18, 44, 30, 48], fill=EMAS_TERANG)
    d.ellipse([4, 6, 12, 14], fill=_w(255, 255, 255))
    d.ellipse([36, 48, 44, 56], fill=_w(255, 255, 255))
    return garis_luar(img)

def prop_galeri():
    w, h = 88, 74
    img, d = kanvas(w, h)
    d.rectangle([4, 8, 84, 70], fill=_w(48, 24, 36))
    d.rectangle([6, 10, 82, 68], fill=_w(32, 16, 24))
    for fx in (12, 36, 60):
        d.rectangle([fx, 18, fx + 16, 46], fill=EMAS_TERANG)
        d.rectangle([fx + 2, 20, fx + 14, 44], fill=_w(248, 242, 230))
        d.ellipse([fx + 5, 24, fx + 11, 30], fill=_w(140, 80, 96))
        d.rectangle([fx + 4, 32, fx + 12, 42], fill=_w(60, 40, 50))
        d.rectangle([fx + 6, 10, fx + 10, 14], fill=EMAS_KILAU)
        d.polygon([(fx + 8, 14), (fx + 2, 24), (fx + 14, 24)], fill=_w(255, 246, 170, 70))
    return garis_luar(img)

def prop_buku_tamu():
    w, h = 84, 64
    img, d = kanvas(w, h)
    d.rectangle([6, 32, 78, 62], fill=BELUDRU_GELAP)
    d.rectangle([4, 30, 80, 40], fill=BELUDRU_MARUN)
    d.line([(4, 40), (80, 40)], fill=EMAS_TERANG, width=2)
    d.rectangle([14, 20, 32, 32], fill=GARIS_LUAR)
    d.rectangle([16, 22, 30, 30], fill=_w(220, 240, 255))
    d.point((23, 26), fill=_w(60, 120, 200))
    d.rectangle([56, 24, 66, 34], fill=MARMER_PUTIH)
    d.ellipse([54, 14, 68, 26], fill=_w(255, 255, 255))
    d.point((58, 18), fill=_w(238, 48, 64))
    d.point((64, 20), fill=_w(255, 210, 80))
    d.rectangle([38, 26, 48, 33], fill=EMAS_TERANG)
    d.line([(43, 26), (43, 33)], fill=_w(255, 255, 255))
    return garis_luar(img)

def prop_hadiah():
    w, h = 52, 58
    img, d = kanvas(w, h)
    d.rectangle([18, 44, 34, 56], fill=EMAS_PEKAT)
    d.ellipse([10, 40, 42, 48], fill=EMAS_DASAR)
    d.rectangle([12, 14, 40, 42], fill=_w(140, 200, 240, 140))
    d.rectangle([12, 14, 40, 42], outline=EMAS_TERANG, width=2)
    d.point((26, 28), fill=_w(255, 255, 255))
    d.ellipse([22, 24, 30, 32], fill=_w(255, 230, 110, 160))
    d.line([(12, 28), (40, 28)], fill=EMAS_KILAU, width=2)
    d.line([(26, 14), (26, 42)], fill=EMAS_KILAU, width=2)
    d.polygon([(26, 14), (20, 8), (26, 11), (32, 8)], fill=EMAS_TERANG)
    return garis_luar(img)

def prop_mobil_pengantin():
    w, h = 104, 52
    img, d = kanvas(w, h)
    for rx in (24, 80):
        d.ellipse([rx - 8, 36, rx + 8, 50], fill=GARIS_LUAR)
        d.ellipse([rx - 4, 40, rx + 4, 46], fill=MARMER_ABU)
    d.rectangle([10, 24, 94, 44], fill=MARMER_PUTIH)
    d.polygon([(24, 24), (36, 10), (74, 10), (84, 24)], fill=MARMER_PUTIH)
    d.polygon([(38, 22), (40, 12), (52, 12), (52, 22)], fill=DINDING_KACA)
    d.polygon([(56, 22), (56, 12), (72, 12), (78, 22)], fill=DINDING_KACA)
    d.rectangle([92, 28, 96, 36], fill=EMAS_KILAU)
    d.rectangle([8, 28, 12, 34], fill=_w(238, 48, 52))
    d.polygon([(82, 16), (92, 26), (84, 28)], fill=_w(255, 120, 160))
    d.ellipse([84, 22, 92, 28], fill=_w(255, 255, 255))
    d.point((88, 25), fill=_w(255, 214, 80))
    d.rectangle([44, 36, 64, 42], fill=_w(255, 255, 255))
    d.point((54, 39), fill=BELUDRU_MARUN)
    return garis_luar(img)

def prop_grand_piano():
    w, h = 76, 70
    img, d = kanvas(w, h)
    for kx in (18, 56, 38):
        d.rectangle([kx, 42, kx + 3, 64], fill=GARIS_LUAR)
    d.polygon([(14, 26), (58, 14), (66, 32), (58, 46), (14, 46)], fill=_w(22, 22, 28))
    d.line([(18, 26), (48, 8)], fill=_w(44, 44, 52), width=3)
    d.line([(48, 8), (44, 28)], fill=EMAS_TERANG, width=1)
    d.rectangle([14, 42, 42, 48], fill=_w(255, 255, 255))
    for tx in range(16, 40, 4):
        d.line([(tx, 42), (tx, 45)], fill=GARIS_LUAR)
    d.rectangle([48, 48, 60, 62], fill=GARIS_LUAR)
    d.rectangle([50, 32, 58, 48], fill=_w(28, 32, 44))
    d.ellipse([51, 24, 57, 32], fill=_w(244, 208, 182))
    d.ellipse([50, 22, 58, 27], fill=_w(40, 28, 20))
    return garis_luar(img)

def prop_kue_pengantin():
    w, h = 48, 76
    img, d = kanvas(w, h)
    d.rectangle([18, 54, 30, 72], fill=EMAS_PEKAT)
    d.ellipse([10, 50, 38, 58], fill=MARMER_PUTIH)
    tingkat = [
        (12, 42, 36, 52),
        (15, 33, 33, 42),
        (18, 25, 30, 33),
        (21, 18, 27, 25),
        (23, 12, 25, 18)
    ]
    for x1, y1, x2, y2 in tingkat:
        d.rectangle([x1, y1, x2, y2], fill=_w(255, 252, 246))
        d.line([(x1, y2), (x2, y2)], fill=EMAS_TERANG, width=2)
        d.point((x1 + 1, y1 + 1), fill=_w(255, 140, 170))
        d.point((x2 - 1, y1 + 1), fill=_w(255, 140, 170))
    d.point((23, 9), fill=GARIS_LUAR)
    d.point((25, 9), fill=_w(255, 255, 255))
    d.point((24, 7), fill=EMAS_KILAU)
    return garis_luar(img)

# ==============================================================================
# 8. SPRITE SHEET KARAKTER (48x80 4 Arah 4 Frame)
# ==============================================================================
LEBAR_FRAME = 24
TINGGI_FRAME = 40
SKALA = 2

def frame_karakter_modern(arah, kolom, wanita=False):
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    cx = 12
    langkah = 0
    if kolom == 1: langkah = -1
    elif kolom == 3: langkah = 1

    kulit = _w(248, 214, 190)
    rambut = _w(36, 26, 22)

    if not wanita:
        # Kaki & Celana Formal Tuxedo
        d.rectangle([cx - 4 + langkah, 28, cx - 1 + langkah, 38], fill=_w(22, 24, 32))
        d.rectangle([cx + 1 - langkah, 28, cx + 4 - langkah, 38], fill=_w(22, 24, 32))
        d.rectangle([cx - 5 + langkah, 37, cx - 1 + langkah, 39], fill=GARIS_LUAR)
        d.rectangle([cx + 1 - langkah, 37, cx + 5 - langkah, 39], fill=GARIS_LUAR)
        d.rectangle([cx - 5, 17, cx + 5, 28], fill=_w(26, 28, 38))
        if arah == "bawah":
            d.polygon([(cx - 2, 17), (cx + 2, 17), (cx, 23)], fill=_w(255, 255, 255))
            d.point((cx, 19), fill=GARIS_LUAR)
            d.point((cx, 22), fill=EMAS_TERANG)
        elif arah in ("kiri", "kanan"):
            d.line([(cx, 17), (cx, 27)], fill=GARIS_LUAR)
        d.ellipse([cx - 4, 9, cx + 4, 17], fill=kulit)
        d.ellipse([cx - 5, 7, cx + 5, 13], fill=rambut)
        if arah != "atas":
            d.point((cx - 2, 13), fill=GARIS_LUAR)
            d.point((cx + 2, 13), fill=GARIS_LUAR)
    else:
        gaun = BELUDRU_MARUN
        gaun_terang = _w(188, 44, 76)
        d.polygon([(cx - 7 + langkah, 38), (cx + 7 - langkah, 38), (cx + 3, 23), (cx - 3, 23)], fill=gaun)
        d.line([(cx - 2, 24), (cx - 4 + langkah, 38)], fill=gaun_terang)
        d.line([(cx + 2, 24), (cx + 4 - langkah, 38)], fill=gaun_terang)
        d.rectangle([cx - 4, 17, cx + 4, 23], fill=gaun)
        if arah == "bawah":
            d.ellipse([cx - 3, 16, cx + 3, 19], fill=kulit)
            d.arc([cx - 3, 17, cx + 3, 20], 0, 180, fill=EMAS_KILAU, width=1)
        d.line([(cx - 4, 18), (cx - 6, 24)], fill=kulit)
        d.line([(cx + 4, 18), (cx + 6, 24)], fill=kulit)
        d.ellipse([cx - 4, 9, cx + 4, 17], fill=kulit)
        d.ellipse([cx - 5, 6, cx + 5, 13], fill=rambut)
        d.ellipse([cx - 3, 4, cx + 3, 9], fill=rambut)
        d.point((cx, 5), fill=EMAS_KILAU)
        if arah != "atas":
            d.point((cx - 2, 13), fill=GARIS_LUAR)
            d.point((cx + 2, 13), fill=GARIS_LUAR)
            d.point((cx - 3, 14), fill=_w(255, 140, 160))
            d.point((cx + 3, 14), fill=_w(255, 140, 160))

    img = garis_luar(img)
    return img.resize((LEBAR_FRAME * SKALA, TINGGI_FRAME * SKALA), Image.NEAREST)

def buat_sprite_sheet_karakter(nama_berkas, wanita=False):
    arah_urutan = ["bawah", "kiri", "kanan", "atas"]
    lembar = Image.new("RGBA", (4 * LEBAR_FRAME * SKALA, 4 * TINGGI_FRAME * SKALA), (0, 0, 0, 0))
    for baris, arah in enumerate(arah_urutan):
        for kolom in range(4):
            frame = frame_karakter_modern(arah, kolom, wanita=wanita)
            lembar.paste(frame, (kolom * LEBAR_FRAME * SKALA, baris * TINGGI_FRAME * SKALA))
    lembar.save(KELUARAN / nama_berkas)

def prop_pengantin_modern(wanita=False):
    img = frame_karakter_modern("bawah", 0, wanita=wanita)
    if wanita:
        w, h = img.size
        d = ImageDraw.Draw(img)
        d.polygon([(4, h - 4), (w - 4, h - 4), (w // 2 + 8, 48), (w // 2 - 8, 48)], fill=_w(255, 255, 255))
        d.line([(w // 2 - 4, 50), (12, h - 4)], fill=_w(232, 230, 224), width=2)
        d.line([(w // 2 + 4, 50), (w - 12, h - 4)], fill=_w(232, 230, 224), width=2)
        cx = w // 2
        d.polygon([(cx, 8), (cx - 8, 16), (cx + 8, 16)], fill=EMAS_KILAU)
        d.point((cx, 6), fill=_w(255, 255, 255))
        d.point((cx - 5, 10), fill=EMAS_TERANG)
        d.point((cx + 5, 10), fill=EMAS_TERANG)
    return garis_luar(img)

# ==============================================================================
# MAIN FUNCTION
# ==============================================================================
def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    print("=== Menghasilkan Aset Grand Ballroom Gedung Mewah v2 ===")

    print("[1] Membuat Tileset Modern Luxury Tanpa Kotak-Kotak...")
    buat_tileset()

    print("[2] Membuat Properti Ballroom & Eksterior...")
    prop_pintu_gedung().save(KELUARAN / "pintu_gedung.png")
    prop_pelaminan().save(KELUARAN / "pelaminan.png")
    prop_papan().save(KELUARAN / "papan.png")
    prop_galeri().save(KELUARAN / "galeri.png")
    prop_buku_tamu().save(KELUARAN / "buku_tamu.png")
    prop_hadiah().save(KELUARAN / "hadiah.png")
    prop_mobil_pengantin().save(KELUARAN / "mobil_pengantin.png")
    prop_grand_piano().save(KELUARAN / "grand_piano.png")
    prop_kue_pengantin().save(KELUARAN / "kue_pengantin.png")
    prop_meja_vip().save(KELUARAN / "meja_vip.png")
    prop_kursi().save(KELUARAN / "kursi.png")
    prop_pot_bunga().save(KELUARAN / "pot_bunga.png")

    print("[3] Membuat Karakter Tamu Tuxedo & Gaun Malam...")
    buat_sprite_sheet_karakter("karakter_pria.png", wanita=False)
    buat_sprite_sheet_karakter("karakter_wanita.png", wanita=True)
    prop_pengantin_modern(wanita=False).save(KELUARAN / "pengantin_pria.png")
    prop_pengantin_modern(wanita=True).save(KELUARAN / "pengantin_wanita.png")

    print(f"\n[SUKSES] Seluruh aset Grand Ballroom tersimpan di {KELUARAN}")

if __name__ == "__main__":
    main()
