"""Membuat gambar pratinjau landing page untuk Tema Desa Asri (Gaya Stardew Valley)."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

AKAR = Path(__file__).resolve().parent.parent
DIR_ASET = AKAR / "static" / "game_desa"
TUJUAN = AKAR / "static" / "img" / "preview_desa.png"

W, H = 960, 540
canvas = Image.new("RGBA", (W, H), (32, 64, 24, 255))
d = ImageDraw.Draw(canvas)

# 1. Gradien Latar Belakang Bukit & Sawah Pedesaan
for y in range(H):
    r = y / H
    warna = (
        int(120 * (1 - r) + 54 * r),
        int(185 * (1 - r) + 120 * r),
        int(75 * (1 - r) + 38 * r),
        255
    )
    d.line([(0, y), (W, y)], fill=warna)

# 2. Pola Petak Tanah & Sawah
tileset = Image.open(DIR_ASET / "tileset.png")
tile_size = 48
for ty in range(0, H, tile_size):
    for tx in range(0, W, tile_size):
        # Pilih tile rumput, jalan, sawah
        if 240 <= tx <= 380:
            idx = 4 # Batu kali
        elif 620 <= tx <= 740 and 100 <= ty <= 420:
            idx = 6 # Kebun gembur
        elif 60 <= tx <= 200 and 120 <= ty <= 420:
            idx = 10 # Sawah
        elif 220 <= ty <= 290 and not (240 <= tx <= 380):
            idx = 7 # Air sungai
        elif 220 <= ty <= 290 and (240 <= tx <= 380):
            idx = 5 # Jembatan kayu
        else:
            idx = (tx // tile_size + ty // tile_size) % 3 # Rumput varian
        canvas.paste(tileset.crop((idx * tile_size, 0, (idx + 1) * tile_size, tile_size)), (tx, ty))

# 3. Tempelkan Objek-Objek Khas Stardew Valley
def pasang(nama, x, y, scale=1.0):
    img = Image.open(DIR_ASET / f"{nama}.png")
    if scale != 1.0:
        nw = int(img.width * scale)
        nh = int(img.height * scale)
        img = img.resize((nw, nh), Image.NEAREST)
    canvas.paste(img, (x, y), img)

# Saung Lumbung di kiri atas
pasang("saung_lumbung", 80, 50, scale=1.4)

# Pelaminan Saung Gazebo di tengah atas
pasang("pelaminan", 380, 70, scale=1.6)

# Mempelai Duduk di Pelaminan
pasang("pengantin_pria", 440, 160, scale=1.3)
pasang("pengantin_wanita", 510, 160, scale=1.3)

# Notice Board Stardew
pasang("papan", 230, 310, scale=1.3)

# Meja Jamuan Tumpeng
pasang("buku_tamu", 580, 320, scale=1.4)

# Peti Kayu Hadiah
pasang("hadiah", 320, 370, scale=1.3)

# Gapura di depan
pasang("gerbang", 430, 410, scale=1.4)

# Karakter Pria Sunda Berjalan
pasang("karakter_pria", 460, 340, scale=1.3)

# Hewan Pedesaan: Ayam & Kucing
ayam = Image.open(DIR_ASET / "ayam.png").crop((0, 0, 32, 32))
canvas.paste(ayam.resize((48, 48), Image.NEAREST), (380, 360), ayam.resize((48, 48), Image.NEAREST))
canvas.paste(ayam.resize((48, 48), Image.NEAREST), (680, 380), ayam.resize((48, 48), Image.NEAREST))

kucing = Image.open(DIR_ASET / "kucing.png").crop((0, 0, 32, 32))
canvas.paste(kucing.resize((44, 44), Image.NEAREST), (160, 150), kucing.resize((44, 44), Image.NEAREST))

# Pohon Buah di sudut-sudut
pasang("pohon_buah", 20, 260, scale=1.5)
pasang("pohon_buah", 800, 200, scale=1.6)
pasang("pohon_buah", 820, 360, scale=1.5)

# 4. Ornamen Stardew HUD & Overlay
# Vignette bayangan halus di tepi
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
vd.rectangle([0, 0, W, H], outline=(30, 20, 12, 180), width=12)

hasil = Image.alpha_composite(canvas, vignette)
hasil.convert("RGB").save(TUJUAN, "PNG", optimize=True)
print(f"Pratinjau berhasil disimpan di {TUJUAN}")
