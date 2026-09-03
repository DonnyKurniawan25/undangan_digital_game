"""Membuat gambar pratinjau landing page untuk Tema 5: Grand Ballroom Gedung Mewah."""

from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
DIR_ASET = AKAR / "static" / "game_gedung"
TUJUAN = AKAR / "static" / "img" / "preview_gedung.png"

W, H = 960, 540
canvas = Image.new("RGBA", (W, H), (14, 18, 28, 255))
d = ImageDraw.Draw(canvas)

# 1. Gradien Latar Belakang Midnight Navy & Royal Ballroom
for y in range(H):
    r = y / H
    if y < 360:
        # Indoor Grand Ballroom (atas)
        warna = (
            int(24 * (1 - r) + 52 * r),
            int(14 * (1 - r) + 20 * r),
            int(34 * (1 - r) + 28 * r),
            255
        )
    else:
        # Outdoor Plaza Malam (bawah)
        warna = (
            int(36 * (1 - r) + 58 * r),
            int(42 * (1 - r) + 64 * r),
            int(54 * (1 - r) + 78 * r),
            255
        )
    d.line([(0, y), (W, y)], fill=warna)

# 2. Pola Karpet Ballroom & Plaza Luar
tileset = Image.open(DIR_ASET / "tileset.png")
tile_size = 48
for ty in range(0, H, tile_size):
    for tx in range(0, W, tile_size):
        if ty >= 450:
            idx = 3 # Jalan raya aspal marka putih (bebas karpet!)
        elif ty >= 380:
            if 432 <= tx <= 528:
                idx = 5 # Red carpet di pedestrian porch
            else:
                idx = 1 # Paving block
        elif ty >= 336:
            idx = 7 # Dinding kaca fasad gedung
        elif 432 <= tx <= 528:
            idx = 9 # Marmer dansa lorong
        else:
            idx = 8 # Karpet ballroom marun emas
        canvas.paste(tileset.crop((idx * tile_size, 0, (idx + 1) * tile_size, tile_size)), (tx, ty))

# 3. Tempelkan Objek-Objek Grand Ballroom
def pasang(nama, x, y, scale=1.0):
    img = Image.open(DIR_ASET / f"{nama}.png")
    if scale != 1.0:
        nw = int(img.width * scale)
        nh = int(img.height * scale)
        img = img.resize((nw, nh), Image.NEAREST)
    canvas.paste(img, (x, y), img)

# Pelaminan Grand Ballroom di tengah atas
pasang("pelaminan", 390, 50, scale=1.5)

# Mempelai Berdiri di Pelaminan
pasang("pengantin_pria", 440, 130, scale=1.3)
pasang("pengantin_wanita", 510, 130, scale=1.3)

# Grand Piano & Pianis di kiri dalam ballroom
pasang("grand_piano", 120, 160, scale=1.4)

# Menara Kue Pengantin di samping pelaminan
pasang("kue_pengantin", 680, 150, scale=1.4)

# Kursi-kursi Chiavari Emas Tamu
for kx in (320, 360):
    for ky in (200, 240, 280):
        pasang("kursi", kx, ky, scale=1.2)
for kx in (560, 600):
    for ky in (200, 240, 280):
        pasang("kursi", kx, ky, scale=1.2)

# Meja Jamuan & Buku Tamu VIP di kanan ballroom
pasang("buku_tamu", 740, 240, scale=1.4)

# Papan LED Display Acara
pasang("papan", 220, 240, scale=1.3)

# Meja VIP Banquet
pasang("meja_vip", 80, 250, scale=1.3)

# Kotak Hadiah Akrilik
pasang("hadiah", 310, 270, scale=1.3)

# Grand Entrance Pintu Masuk Gedung (Pemisah Luar & Dalam)
pasang("pintu_gedung", 426, 300, scale=1.3)

# Luar Gedung: Mobil Pengantin Mewah di Jalan Raya Luar
pasang("mobil_pengantin", 80, 440, scale=1.4)

# Tamu Tuxedo di Red Carpet Luar
pasang("karakter_pria", 470, 390, scale=1.3)

# 4. Vignette Emas Elegan
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
vd.rectangle([0, 0, W, H], outline=(218, 168, 46, 200), width=8)
vd.rectangle([8, 8, W - 8, H - 8], outline=(255, 248, 180, 120), width=2)

hasil = Image.alpha_composite(canvas, vignette)
hasil.convert("RGB").save(TUJUAN, "PNG", optimize=True)
print(f"Pratinjau Grand Ballroom berhasil disimpan di {TUJUAN}")
