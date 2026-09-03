"""Generator Musik Latar Tradisional / Cozy Pentatonic Loop (WAV 16-bit Stereo).

Menghasilkan alunan musik gamelan degung / kecapi suling santai berdurasi ~16 detik yang
bisa di-loop tanpa henti dengan nada pentatonik Sunda yang damai dan romantis.
"""

import math
import struct
import wave
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
DIR_MUSIK = AKAR / "static" / "musik"
DIR_MUSIK.mkdir(parents=True, exist_ok=True)
FILE_KELUARAN = DIR_MUSIK / "desa_asri.wav"

SAMPLE_RATE = 44100
DURASI = 16.0 # 16 detik looping
TOTAL_SAMPLES = int(SAMPLE_RATE * DURASI)

# Frekuensi nada pentatonik Sunda (Da-Mi-Na-Ti-La) lembut
# C4, D4, E4, G4, A4, C5, D5, E5, G5
NOTASI = {
    "C3": 130.81, "G3": 196.00, "A3": 220.00,
    "C4": 261.63, "D4": 293.66, "E4": 329.63, "G4": 392.00, "A4": 440.00,
    "C5": 523.25, "D5": 587.33, "E5": 659.25, "G5": 783.99, "A5": 880.00,
    "C6": 1046.50
}

# Melodi kecapi/kalimba: (waktu_mulai_detik, durasi, nada, volume, pan)
MELODI = [
    # Baris 1 (0 - 4s)
    (0.0, 1.8, "C4", 0.45, -0.2),
    (0.0, 3.5, "C3", 0.35, -0.4),
    (0.5, 1.5, "E4", 0.40, 0.2),
    (1.0, 1.5, "G4", 0.45, -0.1),
    (1.5, 2.0, "C5", 0.50, 0.3),
    (2.0, 1.5, "A4", 0.40, -0.3),
    (2.5, 1.5, "G4", 0.45, 0.1),
    (3.0, 1.8, "E4", 0.40, -0.2),
    (3.5, 1.5, "D4", 0.35, 0.2),

    # Baris 2 (4 - 8s)
    (4.0, 1.8, "G3", 0.38, -0.4),
    (4.0, 1.8, "E4", 0.45, 0.1),
    (4.5, 1.5, "G4", 0.40, -0.2),
    (5.0, 2.0, "D5", 0.50, 0.3),
    (5.5, 1.5, "C5", 0.45, -0.1),
    (6.0, 1.5, "A4", 0.40, 0.2),
    (6.5, 1.8, "G4", 0.48, -0.3),
    (7.0, 1.5, "E4", 0.42, 0.1),
    (7.5, 1.5, "G4", 0.38, -0.2),

    # Baris 3 (8 - 12s)
    (8.0, 3.5, "A3", 0.35, -0.4),
    (8.0, 1.8, "C4", 0.42, 0.2),
    (8.5, 1.5, "E4", 0.45, -0.1),
    (9.0, 2.0, "E5", 0.52, 0.3),
    (9.5, 1.5, "D5", 0.45, -0.2),
    (10.0, 1.8, "C5", 0.50, 0.1),
    (10.5, 1.5, "A4", 0.40, -0.3),
    (11.0, 1.8, "G4", 0.45, 0.2),
    (11.5, 1.5, "E4", 0.38, -0.1),

    # Baris 4 (12 - 16s)
    (12.0, 3.5, "G3", 0.35, -0.4),
    (12.0, 1.8, "D4", 0.42, 0.1),
    (12.5, 1.5, "G4", 0.45, -0.2),
    (13.0, 2.2, "C5", 0.55, 0.3),
    (13.5, 1.5, "D5", 0.45, -0.1),
    (14.0, 2.0, "E5", 0.50, 0.2),
    (14.5, 1.5, "D5", 0.42, -0.2),
    (15.0, 2.0, "C5", 0.48, 0.0),
]

# Suling bambu lembut mengalun
SULING = [
    (1.0, 3.0, "G4", 0.18, 0.2),
    (4.5, 3.0, "C5", 0.20, -0.2),
    (8.5, 3.0, "D5", 0.22, 0.2),
    (12.5, 3.2, "C5", 0.20, -0.1),
]

def buat_gelombang():
    buffer_kiri = [0.0] * TOTAL_SAMPLES
    buffer_kanan = [0.0] * TOTAL_SAMPLES

    # Render Melodi Kalimba / Kecapi
    for t_mulai, dur, nada, vol, pan in MELODI:
        freq = NOTASI[nada]
        idx_mulai = int(t_mulai * SAMPLE_RATE)
        panjang = int(dur * SAMPLE_RATE)
        decay = 3.5 / dur

        for i in range(panjang):
            idx = (idx_mulai + i) % TOTAL_SAMPLES
            t = i / SAMPLE_RATE
            # Harmonisasi nada bell / kalimba kayu
            env = math.exp(-decay * t) * vol
            gel = (
                math.sin(2 * math.pi * freq * t) * 0.65 +
                math.sin(2 * math.pi * freq * 2.0 * t) * 0.22 * math.exp(-decay * 1.5 * t) +
                math.sin(2 * math.pi * freq * 3.01 * t) * 0.10 * math.exp(-decay * 2.5 * t) +
                math.sin(2 * math.pi * freq * 4.04 * t) * 0.05 * math.exp(-decay * 3.5 * t)
            ) * env

            vol_l = 0.5 * (1.0 - pan)
            vol_r = 0.5 * (1.0 + pan)
            buffer_kiri[idx] += gel * vol_l
            buffer_kanan[idx] += gel * vol_r

    # Render Suling Bambu
    for t_mulai, dur, nada, vol, pan in SULING:
        freq = NOTASI[nada]
        idx_mulai = int(t_mulai * SAMPLE_RATE)
        panjang = int(dur * SAMPLE_RATE)

        for i in range(panjang):
            idx = (idx_mulai + i) % TOTAL_SAMPLES
            t = i / SAMPLE_RATE
            # Attack & release halus
            env = math.sin(math.pi * (i / panjang)) * vol
            # Vibrato suling
            vibrato = math.sin(2 * math.pi * 5.0 * t) * 2.5
            gel = (
                math.sin(2 * math.pi * (freq + vibrato) * t) * 0.7 +
                math.sin(2 * math.pi * (freq * 2.0) * t) * 0.2 +
                math.sin(2 * math.pi * (freq * 3.0) * t) * 0.1
            ) * env

            vol_l = 0.5 * (1.0 - pan)
            vol_r = 0.5 * (1.0 + pan)
            buffer_kiri[idx] += gel * vol_l
            buffer_kanan[idx] += gel * vol_r

    # Normalisasi agar tidak clipping
    puncak = max(max(abs(s) for s in buffer_kiri), max(abs(s) for s in buffer_kanan), 0.001)
    skala_vol = 0.85 / puncak

    with wave.open(str(FILE_KELUARAN), "wb") as wav:
        wav.setnchannels(2) # Stereo
        wav.setsampwidth(2) # 16-bit
        wav.setframerate(SAMPLE_RATE)
        
        frames = bytearray()
        for i in range(TOTAL_SAMPLES):
            sl = int(max(-32767, min(32767, buffer_kiri[i] * skala_vol * 32767)))
            sr = int(max(-32767, min(32767, buffer_kanan[i] * skala_vol * 32767)))
            frames.extend(struct.pack("<hh", sl, sr))
        wav.writeframes(frames)

    print(f"Musik berhasil dibuat di: {FILE_KELUARAN}")

if __name__ == "__main__":
    buat_gelombang()
