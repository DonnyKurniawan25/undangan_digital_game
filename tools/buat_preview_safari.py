"""Generator Gambar Pratinjau untuk Tema 6: "Taman Safari Kebun Binatang" (preview_safari.png).
Ukuran kartu: 960x540 px.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

AKAR = Path(__file__).resolve().parent.parent
DIR_ASET = AKAR / "static" / "game_safari"
KELUARAN = AKAR / "static" / "img" / "preview_safari.png"

W, H = 960, 540
canvas = Image.new("RGBA", (W, H), (34, 76, 38, 255))
d = ImageDraw.Draw(canvas)

# 1. Gradasi Latar Belakang Alam Rimba Safari
for y in range(H):
    r = y / H
    warna = (
        int(26 * (1 - r) + 54 * r),
        int(64 * (1 - r) + 116 * r),
        int(32 * (1 - r) + 48 * r),
        255
    )
    d.line([(0, y), (W, y)], fill=warna)

# 2. Ubin Lantai (Tiles)
tileset = Image.open(DIR_ASET / "tileset.png")
tile_size = 48
for ty in range(0, H, tile_size):
    for tx in range(0, W, tile_size):
        if 400 <= tx <= 560 and ty >= 120:
            idx = 2 # Jalan kerikil tengah
        elif tx < 240 and ty > 320:
            idx = 3 # Kolam air barat daya
        elif tx > 720 and ty < 240:
            idx = 0 # Savana emas timur laut
        elif tx < 200 and ty < 200:
            idx = 8 # Rumpun bambu
        else:
            idx = 1 # Rumput rimba tropis
        canvas.paste(tileset.crop((idx * tile_size, 0, (idx + 1) * tile_size, tile_size)), (tx, ty))

# 3. Tempelkan Objek & Satwa
def pasang(nama, x, y, scale=1.0):
    img = Image.open(DIR_ASET / f"{nama}.png")
    if scale != 1.0:
        nw = int(img.width * scale)
        nh = int(img.height * scale)
        img = img.resize((nw, nh), Image.NEAREST)
    canvas.paste(img, (x, y), img)

# Pelaminan Safari di Tengah Atas
pasang("pelaminan", 396, 40, scale=1.5)
pasang("pengantin_pria", 446, 120, scale=1.3)
pasang("pengantin_wanita", 516, 120, scale=1.3)

# Gajah Safari di Kiri
pasang("gajah", 100, 140, scale=1.5)

# Jerapah Tinggi di Kanan
pasang("jerapah", 740, 100, scale=1.4)

# Singa di Bukit Batu Kiri Bawah
pasang("singa", 120, 320, scale=1.4)

# Panda Mengunyah Bambu di Kanan
pasang("panda", 760, 320, scale=1.4)

# Zebra di Padang Rumput
pasang("zebra", 260, 240, scale=1.3)

# Burung Flamingo di Kolam Air
pasang("flamingo", 80, 420, scale=1.3)
pasang("flamingo", 150, 430, scale=1.2)

# Bangku-Bangku Kayu Safari
pasang("bangku", 340, 280, scale=1.2)
pasang("bangku", 580, 280, scale=1.2)

# Plang Kayu Papan Acara
pasang("papan", 280, 160, scale=1.3)

# Pos Ranger Buku Tamu
pasang("buku_tamu", 640, 220, scale=1.3)

# Peti Koper Petualang Hadiah
pasang("hadiah", 340, 360, scale=1.3)

# Jeep Safari 4x4 Terbuka di Pintu Masuk Bawah
pasang("jeep_safari", 620, 400, scale=1.4)

# Tamu Safari Explorer di Jalan Kerikil
pasang("karakter_pria", 460, 340, scale=1.4)

# 4. Vignette Rimba Tropis
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
vd.rectangle([0, 0, W, H], outline=(20, 52, 28, 180), width=18)
canvas.paste(Image.alpha_composite(canvas, vignette))

# 5. Badge Tema
badge = Image.new("RGBA", (440, 56), (18, 44, 24, 230))
bd = ImageDraw.Draw(badge)
bd.rectangle([0, 0, 439, 55], outline=(224, 168, 48, 255), width=2)
canvas.paste(badge, (W // 2 - 220, H - 76), badge)

d = ImageDraw.Draw(canvas)
d.text((W // 2, H - 48), "TEMA 6: TAMAN SAFARI KEBUN BINATANG", fill=(255, 246, 214), anchor="mm")

canvas.convert("RGB").save(KELUARAN, "PNG", quality=95)
print(f"Pratinjau Safari berhasil disimpan di {KELUARAN}")
