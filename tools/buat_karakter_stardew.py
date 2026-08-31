"""Generator Karakter Pixel Art Stardew Valley Edition untuk Undangan Digital Game.

Menghasilkan sprite sheet berkualitas tinggi dengan proporsi dan detail ala Stardew Valley:
- 4 Arah (Bawah, Kiri, Kanan, Atas)
- 4 Frame Walk Cycle (Idle, Langkah Kiri, Passing, Langkah Kanan) dengan bobbing & arm swing
- Detail realistis: mata ekspresif berglint, pipi blush, sanggul & cunduk mentul, ronce melati,
  blangkon mondholan, sapuk sasak, mahkota lambung emas, beskap/kebaya/songket, sabuk pending, dan keris.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw

AKAR = Path(__file__).resolve().parent.parent
LEBAR_FRAME = 24
TINGGI_FRAME = 40
SKALA = 2  # Menghasilkan sprite 48x80 pixel per frame

# Outline & Shadow
GARIS = (40, 30, 34, 255)
GARIS_TERANG = (65, 48, 52, 255)

def kanvas(w=LEBAR_FRAME, h=TINGGI_FRAME, latar=(0, 0, 0, 0)):
    img = Image.new("RGBA", (w, h), latar)
    return img, ImageDraw.Draw(img)

def garis_luar(img, warna=GARIS):
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
                if 0 <= nx < w and 0 <= ny < h and sumber[nx, ny][3] > 64:
                    tujuan[x, y] = warna
                    break
    return hasil

# ==============================================================================
# PALET WARNA DETAIL (Multi-tone shading)
# ==============================================================================
KULIT = {
    "sorot": (255, 238, 224, 255),
    "dasar": (246, 212, 186, 255),
    "bayang": (222, 174, 142, 255),
    "gelap": (192, 140, 110, 255),
    "blush": (248, 154, 150, 255),
    "bibir": (216, 112, 110, 255),
}

MATA = {
    "putih": (250, 250, 252, 255),
    "pupil": (36, 28, 32, 255),
    "iris_cokelat": (94, 60, 48, 255),
    "kilau": (255, 255, 255, 255),
    "alis": (48, 36, 38, 255),
}

EMAS = {
    "sorot": (255, 244, 180, 255),
    "terang": (244, 214, 104, 255),
    "dasar": (218, 172, 54, 255),
    "gelap": (168, 122, 32, 255),
}

PERAK_PUTIH = {
    "sorot": (255, 255, 255, 255),
    "terang": (244, 244, 248, 255),
    "dasar": (220, 222, 230, 255),
    "gelap": (178, 182, 194, 255),
}

MELATI = {
    "putih": (255, 255, 250, 255),
    "kuning": (255, 230, 110, 255),
    "daun": (78, 142, 70, 255),
}

# ---------------- Tema Jawa ----------------
PALET_PRIA_JAWA = {
    "tipe": "jawa_pria",
    "rambut": (42, 34, 36, 255),
    "blangkon_dasar": (120, 78, 52, 255),
    "blangkon_motif": (64, 40, 28, 255),
    "blangkon_lis": EMAS["terang"],
    "beskap_sorot": (68, 58, 66, 255),
    "beskap_dasar": (38, 32, 38, 255),
    "beskap_gelap": (24, 20, 24, 255),
    "kancing": EMAS["terang"],
    "kancing_rantai": EMAS["dasar"],
    "kerah_putih": (246, 246, 250, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "pending": EMAS["terang"],
    "jarik_dasar": (158, 110, 72, 255),
    "jarik_motif": (88, 54, 34, 255),
    "jarik_sorot": (210, 172, 126, 255),
    "keris_gagang": EMAS["terang"],
    "keris_sarung": (148, 102, 60, 255),
    "selop": (28, 24, 28, 255),
    "selop_emas": EMAS["dasar"],
}

PALET_WANITA_JAWA = {
    "tipe": "jawa_wanita",
    "rambut": (38, 30, 32, 255),
    "rambut_sorot": (68, 54, 56, 255),
    "paes": (32, 26, 28, 255),
    "paes_emas": EMAS["terang"],
    "kebaya_sorot": (255, 246, 240, 255),
    "kebaya_dasar": (242, 226, 218, 255),
    "kebaya_gelap": (208, 186, 178, 255),
    "kebaya_renda": (255, 255, 255, 255),
    "kemben": (180, 54, 72, 255),
    "bros": EMAS["terang"],
    "bros_permata": (216, 40, 60, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "jarik_dasar": (152, 104, 68, 255),
    "jarik_motif": (78, 48, 30, 255),
    "jarik_sorot": (206, 168, 122, 255),
    "cunduk_mentul": EMAS["sorot"],
    "cunduk_batang": EMAS["terang"],
    "selop": (168, 52, 68, 255),
    "selop_emas": EMAS["terang"],
}

# ---------------- Tema Sasak Lombok ----------------
PALET_PRIA_SASAK = {
    "tipe": "sasak_pria",
    "rambut": (40, 32, 34, 255),
    "sapuk_dasar": (34, 30, 36, 255),
    "sapuk_songket": (178, 44, 60, 255),
    "sapuk_emas": EMAS["terang"],
    "baju_sorot": (58, 50, 58, 255),
    "baju_dasar": (32, 28, 34, 255),
    "baju_gelap": (20, 18, 22, 255),
    "rompi_bordir": EMAS["terang"],
    "kerah_putih": (246, 246, 250, 255),
    "dodot_dasar": (168, 38, 54, 255),
    "dodot_motif": EMAS["terang"],
    "dodot_sorot": (210, 70, 86, 255),
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "celana_dasar": (36, 32, 38, 255),
    "selop": (28, 24, 28, 255),
    "selop_emas": EMAS["dasar"],
}

PALET_WANITA_SASAK = {
    "tipe": "sasak_wanita",
    "rambut": (38, 30, 32, 255),
    "rambut_sorot": (66, 52, 54, 255),
    "mahkota_sorot": EMAS["sorot"],
    "mahkota_dasar": EMAS["terang"],
    "mahkota_gelap": EMAS["gelap"],
    "mahkota_permata": (224, 40, 58, 255),
    "lambung_sorot": (214, 64, 82, 255),
    "lambung_dasar": (178, 38, 54, 255),
    "lambung_gelap": (132, 24, 38, 255),
    "lambung_bordir": EMAS["terang"],
    "kalung": EMAS["sorot"],
    "sabuk_dasar": EMAS["dasar"],
    "sabuk_sorot": EMAS["sorot"],
    "songket_dasar": (158, 34, 52, 255),
    "songket_motif": EMAS["terang"],
    "songket_sorot": (208, 68, 88, 255),
    "anting": EMAS["sorot"],
    "selop": (158, 34, 52, 255),
    "selop_emas": EMAS["terang"],
}


# ==============================================================================
# DETAIL PENGGAMBARAN SPRITE (Stardew Valley Quality)
# ==============================================================================

def gambar_mata_stardew(d, x, y, arah="bawah", alis_tinggi=0):
    """Mata khas RPG/Stardew Valley dengan iris berwarna, pupil, dan catchlight."""
    # Alis
    d.line([(x, y - 2 + alis_tinggi), (x + 2, y - 2 + alis_tinggi)], fill=MATA["alis"])
    # Putih mata & iris
    d.rectangle([x, y, x + 2, y + 2], fill=MATA["putih"])
    d.rectangle([x + 1, y, x + 2, y + 2], fill=MATA["iris_cokelat"])
    d.point((x + 1, y + 1), fill=MATA["pupil"])
    # Catchlight glint putih di sudut atas
    d.point((x, y), fill=MATA["kilau"])
    # Garis kelopak atas
    d.line([(x, y - 1), (x + 2, y - 1)], fill=(70, 50, 54, 255))


def render_karakter_frame(tipe_palet, arah, frame_idx):
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    p = tipe_palet
    jenis = p["tipe"]
    is_wanita = "wanita" in jenis

    # Walk cycle offsets
    bob_y = 1 if frame_idx in (1, 3) else 0
    ayun = [0, 1, 0, -1][frame_idx]

    cx = 12
    cy_kepala = 11 + bob_y
    cy_badan = 20 + bob_y
    cy_kaki = 31

    # --------------------------------------------------------------------------
    # 1. KAKI & SEPATU
    # --------------------------------------------------------------------------
    if is_wanita:
        x_kaki_kiri = cx - 4
        x_kaki_kanan = cx + 2
        y_kaki_kiri = cy_kaki + 4 + (ayun if arah == "bawah" else (-ayun if arah == "atas" else ayun))
        y_kaki_kanan = cy_kaki + 4 - (ayun if arah == "bawah" else (-ayun if arah == "atas" else ayun))

        if arah in ("bawah", "atas"):
            d.rectangle([x_kaki_kiri, cy_kaki + 3, x_kaki_kiri + 2, min(37, y_kaki_kiri)], fill=KULIT["bayang"])
            d.rectangle([x_kaki_kiri, min(37, y_kaki_kiri), x_kaki_kiri + 2, min(38, y_kaki_kiri + 1)], fill=p["selop"])
            d.point((x_kaki_kiri + 1, min(37, y_kaki_kiri)), fill=p["selop_emas"])
            d.rectangle([x_kaki_kanan, cy_kaki + 3, x_kaki_kanan + 2, min(37, y_kaki_kanan)], fill=KULIT["bayang"])
            d.rectangle([x_kaki_kanan, min(37, y_kaki_kanan), x_kaki_kanan + 2, min(38, y_kaki_kanan + 1)], fill=p["selop"])
            d.point((x_kaki_kanan + 1, min(37, y_kaki_kanan)), fill=p["selop_emas"])
        else:
            x_kaki = cx - 1 + ayun * 2
            d.rectangle([x_kaki, cy_kaki + 3, x_kaki + 3, 37], fill=KULIT["bayang"])
            d.rectangle([x_kaki, 37, x_kaki + 4, 38], fill=p["selop"])
            d.point((x_kaki + 1, 37), fill=p["selop_emas"])
    else:
        if arah in ("bawah", "atas"):
            for x0, maju in ((cx - 4, ayun > 0), (cx + 2, ayun < 0)):
                offset_kaki = 1 if maju else 0
                d.rectangle([x0, cy_kaki + 2, x0 + 2, 35 - offset_kaki], fill=p.get("celana_dasar", p.get("jarik_dasar", (50, 50, 50, 255))))
                d.line([(x0, cy_kaki + 2), (x0, 35 - offset_kaki)], fill=p.get("beskap_gelap", p.get("jarik_motif", (30, 30, 30, 255))))
                d.rectangle([x0 - 1, 36 - offset_kaki, x0 + 3, 38 - offset_kaki], fill=p["selop"])
                d.point((x0 + 1, 36 - offset_kaki), fill=p["selop_emas"])
                d.line([(x0 - 1, 38 - offset_kaki), (x0 + 3, 38 - offset_kaki)], fill=GARIS)
        else:
            for x0, maju in ((cx - 2 - ayun * 2, ayun > 0), (cx + ayun * 2, ayun < 0)):
                d.rectangle([x0, cy_kaki + 2, x0 + 3, 35], fill=p.get("celana_dasar", p.get("jarik_dasar", (50, 50, 50, 255))))
                d.rectangle([x0 - 1, 36, x0 + 4, 38], fill=p["selop"])
                d.point((x0 + 1, 36), fill=p["selop_emas"])

    # --------------------------------------------------------------------------
    # 2. ROK / JARIK / DODOT (BAWAHAN)
    # --------------------------------------------------------------------------
    if is_wanita:
        jarik = p.get("jarik_dasar", p.get("songket_dasar"))
        motif = p.get("jarik_motif", p.get("songket_motif"))
        sorot = p.get("jarik_sorot", p.get("songket_sorot"))

        d.polygon([(cx - 5, cy_badan + 7), (cx + 5, cy_badan + 7),
                    (cx + 7, cy_kaki + 4), (cx - 7, cy_kaki + 4)], fill=jarik)
        for y in range(cy_badan + 8, cy_kaki + 4, 3):
            d.line([(cx - 4, y), (cx - 4, y + 1)], fill=sorot)
            d.line([(cx + 1, y), (cx + 1, y + 1)], fill=sorot)
            for x in (cx - 2, cx + 4):
                d.point((x, y), fill=motif)
        if arah == "bawah":
            d.line([(cx - 1, cy_badan + 7), (cx - 1, cy_kaki + 4)], fill=motif)
            d.line([(cx, cy_badan + 7), (cx, cy_kaki + 4)], fill=sorot)
    else:
        if "jarik_dasar" in p:
            d.polygon([(cx - 4, cy_badan + 7), (cx + 4, cy_badan + 7),
                        (cx + 5, cy_kaki + 3), (cx - 5, cy_kaki + 3)], fill=p["jarik_dasar"])
            for y in range(cy_badan + 8, cy_kaki + 3, 3):
                d.point((cx - 2, y), fill=p["jarik_motif"])
                d.point((cx + 2, y), fill=p["jarik_motif"])
                d.point((cx, y + 1), fill=p["jarik_sorot"])
            if arah == "bawah":
                d.line([(cx, cy_badan + 7), (cx, cy_kaki + 3)], fill=p["jarik_motif"])
        elif "dodot_dasar" in p:
            d.rectangle([cx - 5, cy_badan + 6, cx + 5, cy_badan + 10], fill=p["dodot_dasar"])
            d.line([(cx - 5, cy_badan + 8), (cx + 5, cy_badan + 8)], fill=p["dodot_motif"])
            d.polygon([(cx - 2, cy_badan + 10), (cx + 2, cy_badan + 10), (cx, cy_badan + 13)], fill=p["dodot_dasar"])

    # --------------------------------------------------------------------------
    # 3. BADAN & BUSANA ATAS
    # --------------------------------------------------------------------------
    if is_wanita:
        baju_dasar = p.get("kebaya_dasar", p.get("lambung_dasar"))
        baju_sorot = p.get("kebaya_sorot", p.get("lambung_sorot"))
        baju_gelap = p.get("kebaya_gelap", p.get("lambung_gelap"))

        d.rectangle([cx - 5, cy_badan, cx + 5, cy_badan + 7], fill=baju_dasar)
        d.line([(cx - 5, cy_badan), (cx - 5, cy_badan + 7)], fill=baju_sorot)
        d.line([(cx + 5, cy_badan), (cx + 5, cy_badan + 7)], fill=baju_gelap)

        if arah == "bawah":
            if "kemben" in p:
                d.rectangle([cx - 2, cy_badan, cx + 2, cy_badan + 2], fill=p["kemben"])
            d.polygon([(cx - 3, cy_badan), (cx, cy_badan + 4), (cx + 3, cy_badan)], fill=KULIT["dasar"])
            d.rectangle([cx - 1, cy_badan + 2, cx + 1, cy_badan + 4], fill=p.get("bros", EMAS["terang"]))
            d.point((cx, cy_badan + 3), fill=p.get("bros_permata", EMAS["sorot"]))
            if "kalung" in p:
                d.line([(cx - 2, cy_badan), (cx + 2, cy_badan)], fill=p["kalung"])
        elif arah == "atas":
            d.line([(cx, cy_badan), (cx, cy_badan + 7)], fill=baju_gelap)

        d.rectangle([cx - 5, cy_badan + 6, cx + 5, cy_badan + 7], fill=p["sabuk_dasar"])
        d.point((cx, cy_badan + 6), fill=p["sabuk_sorot"])
        d.point((cx, cy_badan + 7), fill=EMAS["sorot"])
    else:
        baju_dasar = p.get("beskap_dasar", p.get("baju_dasar"))
        baju_sorot = p.get("beskap_sorot", p.get("baju_sorot"))
        baju_gelap = p.get("beskap_gelap", p.get("baju_gelap"))

        d.rectangle([cx - 6, cy_badan, cx + 6, cy_badan + 8], fill=baju_dasar)
        d.line([(cx - 6, cy_badan), (cx - 6, cy_badan + 8)], fill=baju_sorot)
        d.line([(cx + 6, cy_badan), (cx + 6, cy_badan + 8)], fill=baju_gelap)

        if arah == "bawah":
            d.rectangle([cx - 2, cy_badan, cx + 2, cy_badan + 2], fill=p["kerah_putih"])
            d.line([(cx - 3, cy_badan), (cx - 3, cy_badan + 2)], fill=baju_sorot)
            d.line([(cx + 3, cy_badan), (cx + 3, cy_badan + 2)], fill=baju_gelap)
            for yk in (cy_badan + 3, cy_badan + 5, cy_badan + 7):
                d.point((cx, yk), fill=p.get("kancing", EMAS["terang"]))
            if "kancing_rantai" in p:
                d.line([(cx - 2, cy_badan + 5), (cx + 2, cy_badan + 5)], fill=p["kancing_rantai"])
        elif arah == "atas":
            d.line([(cx, cy_badan + 1), (cx, cy_badan + 7)], fill=baju_gelap)
            if "keris_gagang" in p:
                d.line([(cx + 2, cy_badan + 4), (cx + 5, cy_badan + 1)], fill=p["keris_gagang"], width=2)
                d.point((cx + 5, cy_badan + 1), fill=EMAS["sorot"])
                d.rectangle([cx + 1, cy_badan + 5, cx + 3, cy_badan + 8], fill=p["keris_sarung"])

        d.rectangle([cx - 5, cy_badan + 7, cx + 5, cy_badan + 8], fill=p["sabuk_dasar"])
        d.point((cx, cy_badan + 7), fill=p["pending"] if "pending" in p else EMAS["sorot"])

    # --------------------------------------------------------------------------
    # 4. LENGAN & TANGAN
    # --------------------------------------------------------------------------
    warna_lengan = p.get("kebaya_dasar", p.get("beskap_dasar", p.get("baju_dasar", p.get("lambung_dasar"))))
    warna_lengan_sorot = p.get("kebaya_sorot", p.get("beskap_sorot", p.get("baju_sorot", p.get("lambung_sorot"))))

    if arah in ("bawah", "atas"):
        for x0, sisi, ayun_lengan in ((cx - 8, -1, -ayun), (cx + 6, 1, ayun)):
            y_lengan = cy_badan + 1 + ayun_lengan
            d.rectangle([x0, y_lengan, x0 + 2, y_lengan + 6], fill=warna_lengan)
            d.point((x0 if sisi == -1 else x0 + 2, y_lengan), fill=warna_lengan_sorot)
            d.rectangle([x0, y_lengan + 7, x0 + 2, y_lengan + 8], fill=KULIT["dasar"])
            d.point((x0 + 1, y_lengan + 8), fill=KULIT["sorot"])
    else:
        x_lengan = cx - 1 - ayun * 3
        y_lengan = cy_badan + 1
        d.rectangle([x_lengan, y_lengan, x_lengan + 3, y_lengan + 6], fill=warna_lengan)
        d.rectangle([x_lengan, y_lengan + 7, x_lengan + 3, y_lengan + 8], fill=KULIT["dasar"])

    # --------------------------------------------------------------------------
    # 5. KEPALA & WAJAH
    # --------------------------------------------------------------------------
    d.rectangle([cx - 2, cy_kepala + 6, cx + 2, cy_badan], fill=KULIT["bayang"])
    d.line([(cx - 2, cy_badan), (cx + 2, cy_badan)], fill=KULIT["gelap"])

    d.rectangle([cx - 5, cy_kepala - 4, cx + 5, cy_kepala + 5], fill=KULIT["dasar"])
    d.line([(cx - 5, cy_kepala - 4), (cx - 5, cy_kepala + 4)], fill=KULIT["sorot"])
    d.line([(cx + 5, cy_kepala - 4), (cx + 5, cy_kepala + 4)], fill=KULIT["bayang"])
    d.line([(cx - 4, cy_kepala + 5), (cx + 4, cy_kepala + 5)], fill=KULIT["bayang"])

    if arah == "bawah":
        d.rectangle([cx - 5, cy_kepala + 2, cx - 3, cy_kepala + 3], fill=KULIT["blush"])
        d.rectangle([cx + 3, cy_kepala + 2, cx + 5, cy_kepala + 3], fill=KULIT["blush"])

        gambar_mata_stardew(d, cx - 4, cy_kepala, arah="bawah")
        gambar_mata_stardew(d, cx + 2, cy_kepala, arah="bawah")

        d.point((cx, cy_kepala + 2), fill=KULIT["bayang"])
        d.line([(cx - 1, cy_kepala + 4), (cx + 1, cy_kepala + 4)], fill=KULIT["bibir"])
        d.point((cx, cy_kepala + 4), fill=KULIT["sorot"])

        d.rectangle([cx - 6, cy_kepala, cx - 6, cy_kepala + 2], fill=KULIT["dasar"])
        d.rectangle([cx + 6, cy_kepala, cx + 6, cy_kepala + 2], fill=KULIT["dasar"])
        if is_wanita:
            d.point((cx - 6, cy_kepala + 2), fill=p.get("anting", EMAS["sorot"]))
            d.point((cx + 6, cy_kepala + 2), fill=p.get("anting", EMAS["sorot"]))

    elif arah in ("kiri", "kanan"):
        mata_x = cx - 3 if arah == "kiri" else cx + 1
        gambar_mata_stardew(d, mata_x, cy_kepala, arah=arah)
        hidung_x = cx - 5 if arah == "kiri" else cx + 5
        d.point((hidung_x, cy_kepala + 2), fill=KULIT["dasar"])
        bibir_x = cx - 4 if arah == "kiri" else cx + 4
        d.point((bibir_x, cy_kepala + 4), fill=KULIT["bibir"])
        telinga_x = cx + 4 if arah == "kiri" else cx - 4
        d.rectangle([telinga_x, cy_kepala, telinga_x, cy_kepala + 2], fill=KULIT["bayang"])
        if is_wanita:
            d.point((telinga_x, cy_kepala + 2), fill=p.get("anting", EMAS["sorot"]))

    # --------------------------------------------------------------------------
    # 6. HIASAN KEPALA
    # --------------------------------------------------------------------------
    if jenis == "jawa_pria":
        d.polygon([(cx - 6, cy_kepala - 3), (cx, cy_kepala - 7), (cx + 6, cy_kepala - 3)], fill=p["blangkon_dasar"])
        d.rectangle([cx - 6, cy_kepala - 4, cx + 6, cy_kepala - 2], fill=p["blangkon_dasar"])
        d.line([(cx - 5, cy_kepala - 2), (cx + 5, cy_kepala - 2)], fill=p["blangkon_lis"])
        for x in range(cx - 4, cx + 5, 2):
            d.point((x, cy_kepala - 4), fill=p["blangkon_motif"])
        if arah in ("atas", "kiri", "kanan"):
            mx = cx if arah == "atas" else (cx + 5 if arah == "kiri" else cx - 5)
            d.ellipse([mx - 2, cy_kepala - 2, mx + 2, cy_kepala + 2], fill=p["blangkon_dasar"])
            d.point((mx, cy_kepala), fill=p["blangkon_motif"])

    elif jenis == "jawa_wanita":
        d.polygon([(cx - 6, cy_kepala - 3), (cx, cy_kepala - 6), (cx + 6, cy_kepala - 3)], fill=p["rambut"])
        d.rectangle([cx - 6, cy_kepala - 4, cx + 6, cy_kepala - 2], fill=p["rambut"])
        d.line([(cx - 4, cy_kepala - 4), (cx + 4, cy_kepala - 4)], fill=p["rambut_sorot"])

        if arah == "bawah":
            d.polygon([(cx - 4, cy_kepala - 3), (cx - 2, cy_kepala - 1), (cx, cy_kepala - 3),
                        (cx + 2, cy_kepala - 1), (cx + 4, cy_kepala - 3)], fill=p["paes"])
            d.point((cx - 2, cy_kepala - 1), fill=p["paes_emas"])
            d.point((cx + 2, cy_kepala - 1), fill=p["paes_emas"])

        d.ellipse([cx - 4, cy_kepala - 8, cx + 4, cy_kepala - 4], fill=p["rambut"])
        d.line([(cx - 2, cy_kepala - 6), (cx + 2, cy_kepala - 6)], fill=p["rambut_sorot"])

        for offset_x in (-4, -2, 0, 2, 4):
            tinggi_mentul = 10 if offset_x == 0 else (9 if abs(offset_x) == 2 else 8)
            d.line([(cx + offset_x, cy_kepala - 6), (cx + offset_x, cy_kepala - tinggi_mentul)], fill=p["cunduk_batang"])
            d.point((cx + offset_x, cy_kepala - tinggi_mentul), fill=p["cunduk_mentul"])

        if arah in ("bawah", "kiri", "kanan"):
            rx = cx + 4 if arah != "kiri" else cx - 4
            for ym in range(cy_kepala + 2, cy_badan + 7, 2):
                d.point((rx, ym), fill=MELATI["putih"])
                d.point((rx + 1, ym), fill=MELATI["kuning"])
            d.point((rx, cy_badan + 7), fill=MELATI["putih"])

    elif jenis == "sasak_pria":
        d.rectangle([cx - 6, cy_kepala - 4, cx + 6, cy_kepala - 1], fill=p["sapuk_dasar"])
        d.line([(cx - 5, cy_kepala - 2), (cx + 5, cy_kepala - 2)], fill=p["sapuk_emas"])
        d.line([(cx - 5, cy_kepala - 3), (cx + 5, cy_kepala - 3)], fill=p["sapuk_songket"])
        d.polygon([(cx + 3, cy_kepala - 4), (cx + 7, cy_kepala - 8), (cx + 5, cy_kepala - 2)], fill=p["sapuk_dasar"])
        d.line([(cx + 4, cy_kepala - 5), (cx + 6, cy_kepala - 7)], fill=p["sapuk_emas"])

    elif jenis == "sasak_wanita":
        d.rectangle([cx - 6, cy_kepala - 4, cx + 6, cy_kepala - 2], fill=p["mahkota_dasar"])
        d.polygon([(cx - 5, cy_kepala - 4), (cx, cy_kepala - 9), (cx + 5, cy_kepala - 4)], fill=p["mahkota_sorot"])
        d.polygon([(cx - 7, cy_kepala - 6), (cx - 4, cy_kepala - 3), (cx - 4, cy_kepala - 7)], fill=p["mahkota_dasar"])
        d.polygon([(cx + 7, cy_kepala - 6), (cx + 4, cy_kepala - 3), (cx + 4, cy_kepala - 7)], fill=p["mahkota_dasar"])
        d.point((cx, cy_kepala - 5), fill=p["mahkota_permata"])
        d.point((cx, cy_kepala - 8), fill=EMAS["sorot"])
        d.point((cx - 6, cy_kepala - 1), fill=(255, 255, 240, 255))
        d.point((cx - 5, cy_kepala - 1), fill=(255, 220, 80, 255))
        d.point((cx + 6, cy_kepala - 1), fill=(255, 255, 240, 255))
        d.point((cx + 5, cy_kepala - 1), fill=(255, 220, 80, 255))

    return garis_luar(img, GARIS)


def buat_sprite_sheet(palet, nama_file, direktori_tujuan):
    """Membuat sprite sheet 4 arah x 4 frame (192 x 320 px jika skala=2)."""
    ARAH = ["bawah", "kiri", "kanan", "atas"]
    lembar = Image.new("RGBA", (LEBAR_FRAME * 4, TINGGI_FRAME * 4), (0, 0, 0, 0))

    for baris, arah in enumerate(ARAH):
        for kolom in range(4):
            if arah == "kanan":
                frame_img = render_karakter_frame(palet, "kiri", kolom)
                frame_img = frame_img.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                frame_img = render_karakter_frame(palet, arah, kolom)

            lembar.paste(frame_img, (kolom * LEBAR_FRAME, baris * TINGGI_FRAME))

    hasil = lembar.resize((lembar.width * SKALA, lembar.height * SKALA), Image.NEAREST)
    direktori_tujuan.mkdir(parents=True, exist_ok=True)
    hasil.save(direktori_tujuan / nama_file)
    print(f"  -> Tersimpan {direktori_tujuan / nama_file} ({hasil.size[0]}x{hasil.size[1]} px)")


def prop_pengantin_duduk(palet):
    """Mempelai duduk megah di kursi pelaminan dengan pose anggun."""
    img, d = kanvas(LEBAR_FRAME, TINGGI_FRAME)
    # Render frame bawah (idle duduk)
    frame_duduk = render_karakter_frame(palet, "bawah", 0)
    img.paste(frame_duduk, (0, 0))
    hasil = img.resize((img.width * SKALA, img.height * SKALA), Image.NEAREST)
    return hasil


def prop_penari_sasak():
    """Penari Gandrung Sasak dinamis dengan selendang emas."""
    img, d = kanvas(LEBAR_FRAME + 4, TINGGI_FRAME)
    p = PALET_WANITA_SASAK
    cx = 14
    # Badan meliuk menari
    d.rectangle([cx - 4, 18, cx + 4, 25], fill=p["lambung_dasar"])
    d.line([(cx - 4, 18), (cx - 4, 25)], fill=p["lambung_sorot"])
    # Selendang emas melingkar di bahu dan melambai ke samping
    d.polygon([(cx - 10, 16), (cx - 4, 20), (cx - 8, 28), (cx - 12, 22)], fill=EMAS["terang"])
    d.polygon([(cx + 4, 20), (cx + 11, 16), (cx + 13, 22), (cx + 8, 28)], fill=EMAS["terang"])
    # Kain songket melingkar
    d.polygon([(cx - 5, 25), (cx + 5, 25), (cx + 6, 36), (cx - 6, 36)], fill=p["songket_dasar"])
    for y in (27, 30, 33):
        d.line([(cx - 5, y), (cx + 5, y)], fill=p["songket_motif"])
    # Lengan menari lentik
    d.line([(cx - 4, 20), (cx - 11, 15)], fill=KULIT["dasar"], width=2)
    d.line([(cx + 4, 20), (cx + 11, 15)], fill=KULIT["dasar"], width=2)
    d.point((cx - 12, 14), fill=KULIT["sorot"])
    d.point((cx + 12, 14), fill=KULIT["sorot"])
    # Kepala & Mahkota Emas
    d.rectangle([cx - 4, 7, cx + 4, 16], fill=KULIT["dasar"])
    gambar_mata_stardew(d, cx - 3, 11, arah="bawah")
    gambar_mata_stardew(d, cx + 1, 11, arah="bawah")
    d.point((cx, 13), fill=KULIT["bayang"])
    d.line([(cx - 1, 15), (cx + 1, 15)], fill=KULIT["bibir"])
    # Mahkota Tajuk Emas Gandrung
    d.polygon([(cx - 5, 7), (cx, 1), (cx + 5, 7)], fill=EMAS["sorot"])
    d.rectangle([cx - 5, 7, cx + 5, 9], fill=EMAS["terang"])
    d.point((cx, 4), fill=p["mahkota_permata"])
    # Kamboja putih di samping
    d.point((cx - 5, 9), fill=(255, 255, 240, 255))
    d.point((cx + 5, 9), fill=(255, 255, 240, 255))
    hasil = garis_luar(img, GARIS)
    return hasil.resize((hasil.width * SKALA, hasil.height * SKALA), Image.NEAREST)


def prop_pemusik_gendang():
    """Penabuh Gendang Beleq Sasak berdiri dengan instrumen drum megah."""
    img, d = kanvas(32, TINGGI_FRAME)
    p = PALET_PRIA_SASAK
    cx = 10
    # Gendang Beleq besar di samping kanan
    d.ellipse([14, 14, 30, 36], fill=(154, 84, 46, 255))
    d.ellipse([26, 15, 30, 35], fill=(244, 226, 192, 255))  # Kulit drum
    d.line([(14, 25), (26, 25)], fill=EMAS["terang"], width=2)
    d.line([(16, 18), (28, 18)], fill=p["dodot_dasar"], width=2)
    d.line([(16, 32), (28, 32)], fill=p["dodot_dasar"], width=2)
    # Tubuh Pemusik
    d.rectangle([cx - 5, 18, cx + 4, 27], fill=p["baju_dasar"])
    d.rectangle([cx - 4, 27, cx + 3, 36], fill=p["celana_dasar"])
    d.rectangle([cx - 4, 36, cx - 1, 38], fill=p["selop"])
    d.rectangle([cx + 1, 36, cx + 4, 38], fill=p["selop"])
    # Lengan memukul gendang
    d.line([(cx + 3, 20), (18, 23)], fill=KULIT["dasar"], width=2)
    d.point((19, 23), fill=EMAS["terang"])  # Stik pemukul
    # Kepala & Sapuk
    d.rectangle([cx - 4, 7, cx + 4, 16], fill=KULIT["dasar"])
    gambar_mata_stardew(d, cx - 3, 11, arah="bawah")
    gambar_mata_stardew(d, cx + 1, 11, arah="bawah")
    d.point((cx, 13), fill=KULIT["bayang"])
    d.line([(cx - 1, 15), (cx + 1, 15)], fill=KULIT["bibir"])
    # Sapuk ikat kepala
    d.rectangle([cx - 5, 6, cx + 5, 9], fill=p["sapuk_dasar"])
    d.line([(cx - 4, 8), (cx + 4, 8)], fill=p["sapuk_emas"])
    d.polygon([(cx + 2, 6), (cx + 6, 2), (cx + 4, 7)], fill=p["sapuk_dasar"])
    hasil = garis_luar(img, GARIS)
    return hasil.resize((hasil.width * SKALA, hasil.height * SKALA), Image.NEAREST)


def main():
    print("=== Membuat Sprite Karakter Stardew Valley Edition ===")
    
    # 1. Tema Jawa
    dir_jawa = AKAR / "static" / "game"
    print("\n[1] Tema Jawa (Taman Keraton):")
    buat_sprite_sheet(PALET_PRIA_JAWA, "karakter_pria.png", dir_jawa)
    buat_sprite_sheet(PALET_WANITA_JAWA, "karakter_wanita.png", dir_jawa)
    prop_pengantin_duduk(PALET_PRIA_JAWA).save(dir_jawa / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_WANITA_JAWA).save(dir_jawa / "pengantin_wanita.png")
    print("  -> Tersimpan pengantin_pria.png & pengantin_wanita.png (Jawa)")

    # 2. Tema Lombok
    dir_lombok = AKAR / "static" / "game_lombok"
    print("\n[2] Tema Lombok (Pantai Sasak):")
    buat_sprite_sheet(PALET_PRIA_SASAK, "karakter_pria.png", dir_lombok)
    buat_sprite_sheet(PALET_WANITA_SASAK, "karakter_wanita.png", dir_lombok)
    prop_pengantin_duduk(PALET_PRIA_SASAK).save(dir_lombok / "pengantin_pria.png")
    prop_pengantin_duduk(PALET_WANITA_SASAK).save(dir_lombok / "pengantin_wanita.png")
    prop_penari_sasak().save(dir_lombok / "penari_sasak.png")
    prop_pemusik_gendang().save(dir_lombok / "pemusik_gendang.png")
    print("  -> Tersimpan pengantin duduk, penari_sasak.png & pemusik_gendang.png (Lombok)")

    # 3. Tema Tropis
    dir_tropis = AKAR / "static" / "game_tropis"
    print("\n[3] Tema Tropis:")
    buat_sprite_sheet(PALET_PRIA_JAWA, "karakter_pria.png", dir_tropis)
    buat_sprite_sheet(PALET_WANITA_JAWA, "karakter_wanita.png", dir_tropis)

    print("\n=== Selesai Membuat Seluruh Karakter Stardew Valley! ===")


if __name__ == "__main__":
    main()

