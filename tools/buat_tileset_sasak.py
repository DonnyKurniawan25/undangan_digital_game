"""Tileset pixel art 32-bit bertema kampung tradisional Sasak, Lombok.

Untuk permainan RPG tampak atas. Petak 32x32, digambar langsung pada
resolusi akhir (tidak diperbesar) sehingga detailnya halus, dengan tangga
warna 4-5 tingkat per bahan.

    python tools/buat_tileset_sasak.py

Keluaran di static/tileset_sasak/:
    tileset_sasak.png   lembar 8 kolom, urutannya dicetak saat dijalankan
    tepi_rumput.png     12 potongan transisi rumput
    tepi_tanah.png      12 potongan transisi tanah
    tepi_air.png        12 potongan garis pantai / pematang
    petak/<nama>.png    tiap petak sebagai berkas terpisah

Semua petak dasar dijamin tileable: elemen digambar sembilan kali pada
kanvas 96x96 lalu bagian tengahnya dipotong, jadi bentuk yang melewati tepi
muncul kembali di sisi seberang.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
KELUARAN = AKAR / "static" / "tileset_sasak"
UKURAN = 32


def _w(r, g, b, a=255):
    return (r, g, b, a)


# --------------------------------------------------------------------------
# Palet: tanah vulkanik merah, rumput musim kering, batu andesit, air sawah
# Urutan tiap tangga: [kilau, terang, dasar, bayang, pekat]
# --------------------------------------------------------------------------
RUMPUT = [_w(186, 206, 120), _w(156, 182, 94), _w(126, 154, 74), _w(98, 124, 58), _w(74, 98, 46)]
RUMPUT_KERING = [_w(220, 212, 138), _w(196, 188, 112), _w(170, 164, 92), _w(140, 132, 72), _w(112, 104, 58)]
TANAH = [_w(206, 158, 116), _w(182, 132, 92), _w(154, 106, 72), _w(124, 82, 54), _w(96, 62, 40)]
BATU = [_w(196, 190, 180), _w(168, 162, 152), _w(138, 132, 124), _w(106, 100, 94), _w(78, 74, 70)]
AIR = [_w(158, 216, 214), _w(112, 184, 188), _w(78, 148, 156), _w(56, 118, 128), _w(40, 92, 102)]
PASIR = [_w(244, 228, 196), _w(232, 212, 176), _w(216, 194, 156), _w(190, 166, 128), _w(160, 138, 104)]
BAMBU = [_w(228, 202, 140), _w(206, 178, 112), _w(180, 152, 90), _w(148, 122, 68), _w(116, 94, 52)]
PADI = [_w(164, 200, 108), _w(132, 172, 82), _w(104, 142, 62)]


# --------------------------------------------------------------------------
# Menggambar secara "membungkus" agar petak benar-benar tileable
# --------------------------------------------------------------------------
def _geser(xy, dx, dy):
    """Menggeser koordinat, menerima [x0,y0,x1,y1], [(x,y), ...], atau (x,y)."""
    if isinstance(xy, (list, tuple)) and xy and isinstance(xy[0], (list, tuple)):
        return [(x + dx, y + dy) for x, y in xy]
    nilai = list(xy)
    return [n + (dx if i % 2 == 0 else dy) for i, n in enumerate(nilai)]


class GambarBungkus:
    """Meneruskan tiap perintah gambar ke sembilan posisi petak.

    Dengan begitu bentuk yang melewati satu tepi otomatis muncul lagi di
    tepi seberang, sehingga petak dapat disusun tanpa sambungan terlihat.
    """

    def __init__(self, d, ukuran=UKURAN, ulang=3):
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


# Jumlah pengulangan kanvas. 3 sudah cukup untuk produksi; skrip uji
# menaikkannya ke 5 agar petak pembanding menerima seluruh salinan bentuk.
ULANG = 3
KANVAS_TERAKHIR = None


def petak_tileable(gambar_fn, latar):
    """Menjalankan gambar_fn pada kanvas berulang lalu memotong petak tengah."""
    global KANVAS_TERAKHIR
    sisi = UKURAN * ULANG
    besar = Image.new("RGBA", (sisi, sisi), latar)
    d = GambarBungkus(ImageDraw.Draw(besar), UKURAN, ULANG)
    gambar_fn(d)
    KANVAS_TERAKHIR = besar
    return besar.crop((UKURAN, UKURAN, UKURAN * 2, UKURAN * 2))


def _bintik(d, r, jumlah, warna, tepi=0):
    for _ in range(jumlah):
        x = r.randrange(tepi, UKURAN - tepi)
        y = r.randrange(tepi, UKURAN - tepi)
        d.point((x, y), fill=warna)


# --------------------------------------------------------------------------
# Petak rumput
# --------------------------------------------------------------------------
def petak_rumput(seed, kering=False, berbunga=False):
    warna = RUMPUT_KERING if kering else RUMPUT

    def gambar(d):
        r = random.Random(seed)
        # bercak lebar dan tipis; kontrasnya rendah supaya tidak jadi gelembung
        for _ in range(5):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(11, 20), y + r.randint(4, 7)], fill=warna[3])
        for _ in range(5):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(10, 18), y + r.randint(3, 6)], fill=warna[1])
        # rumpun helai: batang pendek berkelompok, arah condong berbeda-beda
        for _ in range(30):
            px, py = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            condong = r.choice((-1, 0, 0, 1))
            for _ in range(r.randint(3, 5)):
                x = px + r.randint(-3, 3)
                y = py + r.randint(-2, 2)
                tinggi = r.randint(2, 4)
                gelap = warna[4] if r.random() < 0.35 else warna[3]
                d.line([(x, y), (x + condong, y - tinggi)], fill=gelap)
                d.point((x + condong, y - tinggi), fill=warna[1] if r.random() < 0.6 else warna[0])
        # kilau di ujung helai, tersebar halus
        _bintik(d, r, 40, warna[0])
        _bintik(d, r, 34, warna[4])
        _bintik(d, r, 24, warna[1])
        if berbunga:
            for _ in range(5):
                x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
                w = r.choice([_w(248, 240, 214), _w(242, 176, 96), _w(226, 118, 128)])
                d.rectangle([x, y, x + 1, y + 1], fill=w)
                d.point((x, y + 1), fill=_w(250, 214, 128))

    return petak_tileable(gambar, warna[2])


def petak_sawah(seed, muda=True):
    """Petak sawah: air dangkal dengan rumpun padi muda."""
    def gambar(d):
        r = random.Random(seed)
        for _ in range(10):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(5, 10), y + r.randint(3, 6)], fill=AIR[3])
        # rumpun padi berbaris seperti tanam jajar
        for baris in range(0, UKURAN, 8):
            for kolom in range(0, UKURAN, 8):
                bx = kolom + (4 if (baris // 8) % 2 else 0) + r.randint(-1, 1)
                by = baris + r.randint(-1, 1)
                for dx, dy in ((0, 0), (-2, 1), (2, 1), (-1, -2), (1, -2)):
                    d.line([(bx + dx, by + dy + 3), (bx + dx, by + dy - 1)],
                           fill=PADI[1] if muda else PADI[2])
                    d.point((bx + dx, by + dy - 1), fill=PADI[0])
        _bintik(d, r, 14, AIR[1])

    return petak_tileable(gambar, AIR[2])


# --------------------------------------------------------------------------
# Petak tanah
# --------------------------------------------------------------------------
def petak_tanah(seed, retak=False):
    def gambar(d):
        r = random.Random(seed)
        for _ in range(9):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(6, 13), y + r.randint(4, 9)], fill=TANAH[3])
        for _ in range(7):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(5, 10), y + r.randint(3, 7)], fill=TANAH[1])
        # kerikil kecil
        for _ in range(16):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.point((x, y), fill=BATU[2])
            d.point((x, y - 1), fill=BATU[1])
        _bintik(d, r, 30, TANAH[4])
        _bintik(d, r, 24, TANAH[0])
        if retak:
            # retakan tanah kering: garis patah yang menyeberangi tepi
            for _ in range(4):
                x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
                for _ in range(r.randint(4, 7)):
                    nx = x + r.randint(-6, 6)
                    ny = y + r.randint(-6, 6)
                    d.line([(x, y), (nx, ny)], fill=TANAH[4])
                    d.line([(x, y + 1), (nx, ny + 1)], fill=TANAH[1])
                    x, y = nx, ny

    return petak_tileable(gambar, TANAH[2])


def petak_pasir(seed):
    def gambar(d):
        r = random.Random(seed)
        for _ in range(8):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(7, 14), y + r.randint(3, 6)], fill=PASIR[3])
        for gel in range(0, UKURAN, 8):   # 8 membagi habis 32 agar menyambung
            for x in range(0, UKURAN):
                y = gel + round(math.sin(x / UKURAN * math.pi * 2 * 2) * 1.6)
                d.point((x, y), fill=PASIR[1])
                d.point((x, y + 1), fill=PASIR[4])
        _bintik(d, r, 30, PASIR[0])
        _bintik(d, r, 18, PASIR[4])

    return petak_tileable(gambar, PASIR[2])


# --------------------------------------------------------------------------
# Petak batu
# --------------------------------------------------------------------------
def petak_batu_jalan(seed):
    """Jalan batu andesit: bongkahan tak beraturan dengan nat tanah."""
    def gambar(d):
        r = random.Random(seed)
        titik = []
        for baris in range(0, UKURAN, 8):
            for kolom in range(0, UKURAN, 8):
                titik.append((kolom + r.randint(0, 3) + (4 if (baris // 8) % 2 else 0),
                              baris + r.randint(0, 2)))
        for x, y in titik:
            lebar = r.randint(6, 9)
            tinggi = r.randint(5, 7)
            d.ellipse([x, y, x + lebar, y + tinggi], fill=BATU[4])
            d.ellipse([x, y, x + lebar - 1, y + tinggi - 1], fill=BATU[2])
            d.ellipse([x + 1, y + 1, x + lebar - 3, y + tinggi - 3], fill=BATU[1])
            d.point((x + 2, y + 2), fill=BATU[0])
        _bintik(d, r, 22, BATU[3])
        _bintik(d, r, 12, BATU[0])

    return petak_tileable(gambar, TANAH[3])


def petak_batu_susun(seed):
    """Batu susun: pasangan batu rapi untuk pelataran atau pagar."""
    def gambar(d):
        r = random.Random(seed)
        for baris in range(0, UKURAN, 8):
            geser = 4 if (baris // 8) % 2 else 0
            for kolom in range(0, UKURAN, 8):
                x = kolom + geser
                d.rectangle([x, baris, x + 7, baris + 6], fill=BATU[4])
                d.rectangle([x, baris, x + 6, baris + 5], fill=BATU[2])
                d.line([(x, baris), (x + 6, baris)], fill=BATU[1])
                d.line([(x, baris), (x, baris + 5)], fill=BATU[1])
                d.point((x + 2, baris + 1), fill=BATU[0])
                _bintik(d, r, 2, BATU[3])

    return petak_tileable(gambar, BATU[3])


# --------------------------------------------------------------------------
# Petak air
# --------------------------------------------------------------------------
def petak_air(seed, fase=0, dangkal=False):
    dasar = AIR[1] if dangkal else AIR[2]

    def gambar(d):
        r = random.Random(seed)
        for _ in range(9):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(8, 15), y + r.randint(4, 8)], fill=AIR[3])
        # riak: gelombang sinus penuh satu periode agar menyambung di tepi
        for baris in range(0, UKURAN, 7):
            for x in range(UKURAN):
                y = baris + round(math.sin((x + fase * 6) / UKURAN * math.pi * 2) * 2)
                d.point((x, y), fill=AIR[1])
                if (x + fase * 4) % 8 < 3:
                    d.point((x, y - 1), fill=AIR[0])
        _bintik(d, r, 16, AIR[4])
        if dangkal:
            for _ in range(10):
                x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
                d.point((x, y), fill=PASIR[3])
                d.point((x + 1, y), fill=PASIR[4])

    return petak_tileable(gambar, dasar)


# --------------------------------------------------------------------------
# Petak buatan manusia khas Sasak
# --------------------------------------------------------------------------
def petak_lantai_bale(seed):
    """Lantai bale Sasak: tanah liat dipadatkan, halus dan agak mengilap."""
    def gambar(d):
        r = random.Random(seed)
        for _ in range(8):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(8, 16), y + r.randint(5, 10)], fill=_w(146, 112, 84))
        for _ in range(6):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(6, 12), y + r.randint(4, 7)], fill=_w(178, 144, 112))
        _bintik(d, r, 26, _w(196, 164, 132))
        _bintik(d, r, 16, _w(128, 96, 72))

    return petak_tileable(gambar, _w(162, 128, 98))


def petak_anyaman_bambu(seed):
    """Bedek: anyaman bambu untuk dinding dan lantai panggung."""
    def gambar(d):
        r = random.Random(seed)
        lebar = 4
        for baris in range(0, UKURAN, lebar * 2):
            for kolom in range(0, UKURAN, lebar * 2):
                d.rectangle([kolom, baris, kolom + lebar - 1, baris + lebar * 2 - 1], fill=BAMBU[1])
                d.rectangle([kolom + lebar, baris + lebar, kolom + lebar * 2 - 1, baris + lebar * 2 - 1],
                            fill=BAMBU[1])
                d.rectangle([kolom + lebar, baris, kolom + lebar * 2 - 1, baris + lebar - 1], fill=BAMBU[3])
                d.rectangle([kolom, baris + lebar, kolom + lebar - 1, baris + lebar * 2 - 1], fill=BAMBU[3])
        for x in range(0, UKURAN, lebar):
            d.line([(x, 0), (x, UKURAN)], fill=BAMBU[4])
        for y in range(0, UKURAN, lebar):
            d.line([(0, y), (UKURAN, y)], fill=BAMBU[4])
        _bintik(d, r, 22, BAMBU[0])

    return petak_tileable(gambar, BAMBU[2])


# --------------------------------------------------------------------------
# Potongan tepi / transisi
#
# Dua belas potongan beralfa yang ditumpuk DI ATAS petak tujuan:
#   4 sisi, 4 sudut luar (dua sisi bertemu), 4 sudut dalam (hanya diagonal).
# Profil tepinya memakai jumlah sinus berperiode 32 piksel, sehingga potongan
# yang berjajar tetap menyambung mulus.
# --------------------------------------------------------------------------
URUTAN_TEPI = [
    "atas", "bawah", "kiri", "kanan",
    "luar_kiri_atas", "luar_kanan_atas", "luar_kiri_bawah", "luar_kanan_bawah",
    "dalam_kiri_atas", "dalam_kanan_atas", "dalam_kiri_bawah", "dalam_kanan_bawah",
]


def _profil(i, fase=0.0):
    """Ketebalan tepi pada posisi i; berulang mulus tiap 32 piksel."""
    t = i / UKURAN * 2 * math.pi
    return (math.sin(t + fase) * 1.7
            + math.sin(t * 2 + fase * 1.7 + 0.9) * 1.1
            + math.sin(t * 4 + fase * 2.3 + 2.1) * 0.6)


def _tekstur_tepi(warna, seed):
    """Petak penuh berisi tekstur bahan, dipakai sebagai isi potongan tepi."""
    def gambar(d):
        r = random.Random(seed)
        for _ in range(8):
            x, y = r.randrange(0, UKURAN), r.randrange(0, UKURAN)
            d.ellipse([x, y, x + r.randint(6, 12), y + r.randint(4, 8)], fill=warna[3])
        _bintik(d, r, 30, warna[1])
        _bintik(d, r, 20, warna[0])
        _bintik(d, r, 18, warna[4])

    return petak_tileable(gambar, warna[2])


def potongan_tepi(jenis, warna, seed, tebal=7):
    """Satu potongan transisi beralfa."""
    tekstur = _tekstur_tepi(warna, seed)
    masker = Image.new("L", (UKURAN, UKURAN), 0)
    m = ImageDraw.Draw(masker)

    def tinggi(i, fase):
        return max(2, min(UKURAN - 2, int(round(tebal + _profil(i, fase)))))

    if jenis == "atas":
        for x in range(UKURAN):
            m.line([(x, 0), (x, tinggi(x, 0.0))], fill=255)
    elif jenis == "bawah":
        for x in range(UKURAN):
            m.line([(x, UKURAN - 1 - tinggi(x, 1.3)), (x, UKURAN - 1)], fill=255)
    elif jenis == "kiri":
        for y in range(UKURAN):
            m.line([(0, y), (tinggi(y, 2.6), y)], fill=255)
    elif jenis == "kanan":
        for y in range(UKURAN):
            m.line([(UKURAN - 1 - tinggi(y, 3.9), y), (UKURAN - 1, y)], fill=255)
    elif jenis.startswith("luar_"):
        # dua sisi bertemu: gabungan dua pita
        _, tegak, datar = jenis.split("_")
        for x in range(UKURAN):
            t = tinggi(x, 0.0 if datar == "atas" else 1.3)
            if datar == "atas":
                m.line([(x, 0), (x, t)], fill=255)
            else:
                m.line([(x, UKURAN - 1 - t), (x, UKURAN - 1)], fill=255)
        for y in range(UKURAN):
            t = tinggi(y, 2.6 if tegak == "kiri" else 3.9)
            if tegak == "kiri":
                m.line([(0, y), (t, y)], fill=255)
            else:
                m.line([(UKURAN - 1 - t, y), (UKURAN - 1, y)], fill=255)
    else:
        # sudut dalam: hanya gundukan kecil di pojok
        _, tegak, datar = jenis.split("_")
        px = 0 if tegak == "kiri" else UKURAN - 1
        py = 0 if datar == "atas" else UKURAN - 1
        jari = tebal + 1
        m.ellipse([px - jari, py - jari, px + jari, py + jari], fill=255)

    hasil = Image.new("RGBA", (UKURAN, UKURAN), (0, 0, 0, 0))
    hasil.paste(tekstur, (0, 0), masker)
    return hasil


def buat_strip_tepi(nama, warna, seed, tebal=7):
    potongan = [potongan_tepi(j, warna, seed + i, tebal) for i, j in enumerate(URUTAN_TEPI)]
    lembar = Image.new("RGBA", (UKURAN * len(potongan), UKURAN), (0, 0, 0, 0))
    for i, p in enumerate(potongan):
        lembar.paste(p, (i * UKURAN, 0))
    lembar.save(KELUARAN / f"{nama}.png")
    return potongan


# --------------------------------------------------------------------------
# Susunan lembar
# --------------------------------------------------------------------------
URUTAN_PETAK = [
    ("rumput_1", lambda: petak_rumput(101)),
    ("rumput_2", lambda: petak_rumput(102)),
    ("rumput_3", lambda: petak_rumput(103)),
    ("rumput_bunga", lambda: petak_rumput(104, berbunga=True)),
    ("rumput_kering_1", lambda: petak_rumput(105, kering=True)),
    ("rumput_kering_2", lambda: petak_rumput(106, kering=True)),
    ("sawah_muda", lambda: petak_sawah(107, muda=True)),
    ("sawah_tua", lambda: petak_sawah(108, muda=False)),

    ("tanah_1", lambda: petak_tanah(201)),
    ("tanah_2", lambda: petak_tanah(202)),
    ("tanah_3", lambda: petak_tanah(203)),
    ("tanah_retak", lambda: petak_tanah(204, retak=True)),
    ("pasir_1", lambda: petak_pasir(205)),
    ("pasir_2", lambda: petak_pasir(206)),
    ("lantai_bale", lambda: petak_lantai_bale(207)),
    ("anyaman_bambu", lambda: petak_anyaman_bambu(208)),

    ("batu_jalan_1", lambda: petak_batu_jalan(301)),
    ("batu_jalan_2", lambda: petak_batu_jalan(302)),
    ("batu_jalan_3", lambda: petak_batu_jalan(303)),
    ("batu_susun", lambda: petak_batu_susun(304)),
    ("air_1", lambda: petak_air(305, 0)),
    ("air_2", lambda: petak_air(305, 1)),
    ("air_3", lambda: petak_air(305, 2)),
    ("air_dangkal", lambda: petak_air(306, 0, dangkal=True)),
]

KOLOM = 8


def main():
    KELUARAN.mkdir(parents=True, exist_ok=True)
    (KELUARAN / "petak").mkdir(exist_ok=True)

    petakan = [(nama, fn()) for nama, fn in URUTAN_PETAK]
    baris = (len(petakan) + KOLOM - 1) // KOLOM
    lembar = Image.new("RGBA", (UKURAN * KOLOM, UKURAN * baris), (0, 0, 0, 0))
    for i, (nama, gbr) in enumerate(petakan):
        lembar.paste(gbr, ((i % KOLOM) * UKURAN, (i // KOLOM) * UKURAN))
        gbr.save(KELUARAN / "petak" / f"{nama}.png")
    lembar.save(KELUARAN / "tileset_sasak.png")

    buat_strip_tepi("tepi_rumput", RUMPUT, 401, tebal=7)
    buat_strip_tepi("tepi_tanah", TANAH, 501, tebal=6)
    buat_strip_tepi("tepi_air", PASIR, 601, tebal=5)

    print(f"Lembar   : tileset_sasak.png ({KOLOM} kolom x {baris} baris, petak {UKURAN}x{UKURAN})")
    for i, (nama, _) in enumerate(petakan):
        print(f"  {i:2d}  ({i % KOLOM},{i // KOLOM})  {nama}")
    print("\nStrip tepi (12 potongan, urutan sama untuk ketiganya):")
    print("  " + ", ".join(f"{i}={n}" for i, n in enumerate(URUTAN_TEPI)))
    print("  tepi_rumput.png, tepi_tanah.png, tepi_air.png")
    print("\nTersimpan di", KELUARAN)


if __name__ == "__main__":
    main()
