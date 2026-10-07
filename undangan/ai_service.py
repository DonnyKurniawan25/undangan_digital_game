"""
Service AI untuk Ekstraksi Undangan Otomatis dan Multi-Provider AI.
Mendukung:
- 9Router (Local AI Router / OpenAI-Compatible)
- Anthropic (Claude Messages API)
- OpenAI (GPT Chat Completions)
- Google Gemini (OpenAI compat)
- OpenRouter
- Groq
- DeepSeek
- Custom OpenAI-compatible (Ollama, LM Studio, vLLM, dll.)
"""

import json
import logging
import re
import time
from datetime import datetime
from io import BytesIO

from django.utils import timezone
from pypdf import PdfReader
import requests

from .models import Acara, KonfigurasiAI, Pengantin, Rekening, Undangan

logger = logging.getLogger(__name__)

# URL bawaan provider jika base_url tidak diisi oleh Superadmin
DEFAULT_BASE_URLS = {
    KonfigurasiAI.PROVIDER_9ROUTER: "http://localhost:20000/v1",
    KonfigurasiAI.PROVIDER_ANTHROPIC: "https://api.anthropic.com/v1",
    KonfigurasiAI.PROVIDER_OPENAI: "https://api.openai.com/v1",
    KonfigurasiAI.PROVIDER_GEMINI: "https://generativelanguage.googleapis.com/v1beta/openai",
    KonfigurasiAI.PROVIDER_OPENROUTER: "https://openrouter.ai/api/v1",
    KonfigurasiAI.PROVIDER_GROQ: "https://api.groq.com/openai/v1",
    KonfigurasiAI.PROVIDER_DEEPSEEK: "https://api.deepseek.com/v1",
    KonfigurasiAI.PROVIDER_CUSTOM: "http://localhost:11434/v1",
}


def ambil_base_url(konfig: KonfigurasiAI) -> str:
    """Mengembalikan base URL yang siap digunakan (tanpa trailing slash)."""
    if konfig.base_url and konfig.base_url.strip():
        return konfig.base_url.strip().rstrip("/")
    return DEFAULT_BASE_URLS.get(konfig.provider, "http://localhost:20000/v1").rstrip("/")


def ekstrak_teks_pdf(file_input) -> str:
    """
    Mengekstrak seluruh teks dari file PDF yang diunggah.
    Menerima file object dari Django UploadedFile atau BytesIO.
    """
    try:
        reader = PdfReader(file_input)
        teks_halaman = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text() or ""
            if txt.strip():
                teks_halaman.append(f"--- HALAMAN {i + 1} ---\n{txt}")
        
        gabungan = "\n\n".join(teks_halaman).strip()
        return gabungan
    except Exception as e:
        logger.error(f"Gagal membaca PDF: {e}")
        raise ValueError(f"Tidak dapat membaca file PDF: {str(e)}")


def bersihkan_json(teks: str) -> dict:
    """
    Membersihkan markdown code blocks (```json ... ```) dan mem-parse string menjadi dict Python.
    """
    if not teks:
        raise ValueError("Respon dari AI kosong.")
    
    bersih = teks.strip()
    # Hapus blok pembungkus ```json ... ``` atau ``` ... ```
    pola_codeblock = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", bersih, re.IGNORECASE)
    if pola_codeblock:
        bersih = pola_codeblock.group(1).strip()
    else:
        # Cari kurung kurawal terluar jika ada teks pengantar
        awal = bersih.find("{")
        akhir = bersih.rfind("}")
        if awal != -1 and akhir != -1 and akhir > awal:
            bersih = bersih[awal : akhir + 1]

    try:
        return json.loads(bersih)
    except json.JSONDecodeError as e:
        logger.warning(f"Gagal parse JSON mentah: {bersih[:200]}...")
        raise ValueError(f"AI tidak menghasilkan format JSON yang valid: {str(e)}")


def panggil_ai(konfig: KonfigurasiAI, prompt: str, system_prompt: str = "") -> str:
    """
    Mengirim prompt ke provider AI yang ditentukan dan mengembalikan teks balasan AI.
    Mendukung format Anthropic Messages API dan OpenAI-Compatible Chat Completions.
    """
    base_url = ambil_base_url(konfig)
    timeout = konfig.timeout_detik or 120

    if konfig.provider == KonfigurasiAI.PROVIDER_ANTHROPIC:
        # Format Anthropic Claude Messages API
        url = f"{base_url}/messages"
        headers = {
            "x-api-key": konfig.api_key or "",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": konfig.model or "claude-sonnet-4-5",
            "max_tokens": konfig.max_tokens or 4096,
            "temperature": konfig.temperature if konfig.temperature is not None else 0.2,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            payload["system"] = system_prompt

        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if not resp.ok:
            error_msg = f"Anthropic HTTP {resp.status_code}: {resp.text}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        data = resp.json()
        teks_konten = []
        for c in data.get("content", []):
            if c.get("type") == "text":
                teks_konten.append(c.get("text", ""))
        return "".join(teks_konten)

    else:
        # Format OpenAI-Compatible (9Router, OpenAI, Gemini, OpenRouter, Groq, DeepSeek, Custom)
        url = f"{base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        if konfig.api_key:
            headers["Authorization"] = f"Bearer {konfig.api_key}"
        
        # OpenRouter header rekomendasi
        if konfig.provider == KonfigurasiAI.PROVIDER_OPENROUTER:
            headers["HTTP-Referer"] = "https://jelajah.biz.id"
            headers["X-Title"] = "Undangan Digital Game"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": konfig.model or "gpt-4o-mini",
            "messages": messages,
            "temperature": konfig.temperature if konfig.temperature is not None else 0.2,
            "max_tokens": konfig.max_tokens or 4096,
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if not resp.ok:
            error_msg = f"{konfig.get_provider_display()} HTTP {resp.status_code}: {resp.text}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as err:
            raise RuntimeError(f"Format respon AI tidak terduga: {resp.text[:300]}")


def uji_koneksi_ai(konfig: KonfigurasiAI) -> tuple[bool, str, int]:
    """
    Menguji koneksi ke endpoint AI dengan prompt singkat 'Halo!'.
    Mengukur waktu respon (latensi dalam milidetik) dan memperbarui kolom status pada model KonfigurasiAI.
    Mengembalikan (sukses: bool, pesan: str, latensi_ms: int).
    """
    prompt = "Jawab hanya dengan satu kata: SIAP"
    system_prompt = "Kamu adalah asisten tes koneksi."
    
    t_mulai = time.time()
    try:
        jawaban = panggil_ai(konfig, prompt=prompt, system_prompt=system_prompt)
        latensi = int((time.time() - t_mulai) * 1000)
        pesan = f"Koneksi berhasil! Respon AI: '{jawaban.strip()[:60]}' (latensi {latensi} ms)."
        
        konfig.status_tes = KonfigurasiAI.STATUS_BERHASIL
        konfig.pesan_tes = pesan
        konfig.latensi_tes_ms = latensi
        konfig.terakhir_dites = timezone.now()
        konfig.save(update_fields=["status_tes", "pesan_tes", "latensi_tes_ms", "terakhir_dites"])
        return True, pesan, latensi

    except Exception as e:
        latensi = int((time.time() - t_mulai) * 1000)
        pesan = f"Koneksi gagal: {str(e)}"
        
        konfig.status_tes = KonfigurasiAI.STATUS_GAGAL
        konfig.pesan_tes = pesan
        konfig.latensi_tes_ms = latensi
        konfig.terakhir_dites = timezone.now()
        konfig.save(update_fields=["status_tes", "pesan_tes", "latensi_tes_ms", "terakhir_dites"])
        return False, pesan, latensi


SYSTEM_PROMPT_EKSTRAKSI = """Kamu adalah asisten AI ahli ekstrak data undangan pernikahan digital.
Tugasmu adalah menganalisis teks dari brosur/undangan fisik/PDF pernikahan dan mengubahnya menjadi format data JSON yang terstruktur.

PANDUAN PENTING:
1. Kembalikan HANYA format JSON valid tanpa penjelasan tambahan dan tanpa markdown tambahan di luar JSON.
2. Nama orang tua: HANYA tuliskan nama aslinya TANPA awalan "Bpk.", "Bapak", "Ibu", atau "Haji", karena sistem aplikasi akan otomatis menambahkan gelar sapaan "Bapak " dan "Ibu ". Contoh: jika di teks tertulis "Bpk. H. Ahmad Subagio", tulis "H. Ahmad Subagio".
3. Peran anak: tulis contoh "Putra pertama dari" atau "Putri kedua dari" jika tertera.
4. Tanggal acara: ubah menjadi format ISO "YYYY-MM-DD" (misal "2026-10-25"). Jika tahun tidak ada di teks, gunakan tahun saat ini (2026).
5. Waktu acara: ubah menjadi format 24 jam "HH:MM" (misal "08:00", "13:00").
6. Tema rekomendasi: pilih salah satu dari: "klasik", "tropis", "lombok", "desa", "gedung", "safari".
7. Rekening / Hadiah Digital: jika tertera nomor rekening bank atau e-wallet (BCA, Mandiri, BRI, BNI, Dana, dll), masukkan ke daftar rekening.
8. Kutipan / Doa: jika ada kutipan ayat (misal QS. Ar-Rum: 21, Matius, dll) atau kata mutiara cinta, masukkan ke kolom quote dan sumber_quote.
"""

CONTOH_FORMAT_JSON = """{
  "judul": "Pernikahan Rina & Budi",
  "hashtag": "#RinaBudiLove",
  "tema_rekomendasi": "desa",
  "quote": "Dan di antara tanda-tanda (kebesaran)-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya...",
  "sumber_quote": "QS. Ar-Rum: 21",
  "catatan_penutup": "Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu kepada kedua mempelai.",
  "mempelai_pria": {
    "nama_lengkap": "Budi Santoso, S.Kom.",
    "nama_panggilan": "Budi",
    "anak_ke": "Putra pertama dari",
    "nama_ayah": "Ahmad Subagio",
    "nama_ibu": "Siti Aminah",
    "instagram": "budisantoso"
  },
  "mempelai_wanita": {
    "nama_lengkap": "Rina Kartika, S.E.",
    "nama_panggilan": "Rina",
    "anak_ke": "Putri kedua dari",
    "nama_ayah": "Hartono",
    "nama_ibu": "Endang Rahayu",
    "instagram": "rinakartika"
  },
  "acara": [
    {
      "nama": "Akad Nikah",
      "tanggal": "2026-10-25",
      "waktu_mulai": "08:00",
      "waktu_selesai": "10:00",
      "nama_tempat": "Masjid Agung Al-Falah",
      "alamat": "Jl. Raya Darmo No. 100, Surabaya",
      "url_maps": ""
    },
    {
      "nama": "Resepsi Pernikahan",
      "tanggal": "2026-10-25",
      "waktu_mulai": "11:00",
      "waktu_selesai": "14:00",
      "nama_tempat": "Grand Ballroom Hotel Majapahit",
      "alamat": "Jl. Tunjungan No. 65, Surabaya",
      "url_maps": ""
    }
  ],
  "rekening": [
    {
      "nama_bank": "BCA",
      "nomor": "1234567890",
      "atas_nama": "Budi Santoso"
    }
  ]
}"""


def ekstrak_undangan_dari_pdf(file_input, konfig: KonfigurasiAI = None) -> tuple[dict, str, int]:
    """
    Mengekstrak data undangan pernikahan dari berkas PDF menggunakan AI yang sedang aktif.
    Mengembalikan tuple: (hasil_json_dict, teks_pdf_mentah, durasi_ms).
    """
    if konfig is None:
        konfig = KonfigurasiAI.ambil_aktif()
    
    if not konfig:
        raise ValueError(
            "Belum ada Konfigurasi AI yang aktif. Silakan hubungi Superadmin untuk mengaktifkan AI di menu Pengaturan AI."
        )

    t_awal = time.time()
    
    # 1. Ekstrak teks dari PDF
    teks_pdf = ekstrak_teks_pdf(file_input)
    if not teks_pdf or len(teks_pdf.strip()) < 20:
        raise ValueError(
            "Teks di dalam PDF tidak terdeteksi atau terlalu sedikit. "
            "Pastikan PDF berisi teks undangan atau ekspor dari Canva/Word yang teksnya dapat disalin."
        )

    # 2. Susun prompt untuk model
    prompt_user = (
        f"Berikut adalah isi teks dari brosur/undangan pernikahan digital:\n\n"
        f"\"\"\"\n{teks_pdf}\n\"\"\"\n\n"
        f"Silakan analisis teks di atas dan ekstrak informasi pernikahan ke dalam format JSON berikut:\n"
        f"{CONTOH_FORMAT_JSON}\n\n"
        f"Kembalikan HANYA JSON tersebut tanpa teks lain."
    )

    # 3. Panggil AI
    jawaban_ai = panggil_ai(konfig, prompt=prompt_user, system_prompt=SYSTEM_PROMPT_EKSTRAKSI)
    
    # 4. Parse JSON
    hasil_json = bersihkan_json(jawaban_ai)
    durasi_ms = int((time.time() - t_awal) * 1000)

    return hasil_json, teks_pdf, durasi_ms


def terapkan_hasil_ai_ke_undangan(
    undangan: Undangan,
    data_ai: dict,
    update_mempelai: bool = True,
    update_acara: bool = True,
    update_rekening: bool = True,
) -> dict:
    """
    Menerapkan data JSON hasil ekstraksi AI langsung ke objek Undangan dan relasinya:
    - Judul, Hashtag, Tema, Quote, Sumber Quote, Catatan Penutup
    - Mempelai Pria & Mempelai Wanita
    - Daftar Acara (Akad, Resepsi, dll)
    - Rekening Hadiah
    """
    ringkasan = {"diperbarui": []}

    # 1. Update informasi dasar undangan
    if data_ai.get("judul"):
        undangan.judul = str(data_ai["judul"])[:120]
        ringkasan["diperbarui"].append("Judul Undangan")
    
    if data_ai.get("hashtag"):
        undangan.hashtag = str(data_ai["hashtag"])[:60]
        ringkasan["diperbarui"].append("Hashtag")

    if data_ai.get("quote"):
        undangan.quote = str(data_ai["quote"])
        ringkasan["diperbarui"].append("Quote")

    if data_ai.get("sumber_quote"):
        undangan.sumber_quote = str(data_ai["sumber_quote"])[:120]
        ringkasan["diperbarui"].append("Sumber Quote")

    if data_ai.get("catatan_penutup"):
        undangan.catatan_penutup = str(data_ai["catatan_penutup"])
        ringkasan["diperbarui"].append("Catatan Penutup")

    tema_rek = str(data_ai.get("tema_rekomendasi", "")).lower().strip()
    daftar_tema_valid = [t[0] for t in Undangan._meta.get_field("tema").choices]
    if tema_rek in daftar_tema_valid:
        undangan.tema = tema_rek
        ringkasan["diperbarui"].append(f"Tema ({undangan.get_tema_display()})")

    undangan.save()

    # 2. Update Mempelai Pria & Wanita
    if update_mempelai:
        # Pria
        pria_data = data_ai.get("mempelai_pria") or {}
        if pria_data:
            pria, _ = Pengantin.objects.get_or_create(undangan=undangan, peran=Pengantin.PRIA)
            if pria_data.get("nama_lengkap"):
                pria.nama_lengkap = str(pria_data["nama_lengkap"])[:120]
            if pria_data.get("nama_panggilan"):
                pria.nama_panggilan = str(pria_data["nama_panggilan"])[:60]
            if pria_data.get("anak_ke"):
                pria.anak_ke = str(pria_data["anak_ke"])[:40]
            if pria_data.get("nama_ayah"):
                pria.nama_ayah = str(pria_data["nama_ayah"])[:120]
            if pria_data.get("nama_ibu"):
                pria.nama_ibu = str(pria_data["nama_ibu"])[:120]
            if pria_data.get("instagram"):
                pria.instagram = str(pria_data["instagram"]).lstrip("@")[:60]
            pria.save()
            ringkasan["diperbarui"].append("Profil Mempelai Pria")

        # Wanita
        wanita_data = data_ai.get("mempelai_wanita") or {}
        if wanita_data:
            wanita, _ = Pengantin.objects.get_or_create(undangan=undangan, peran=Pengantin.WANITA)
            if wanita_data.get("nama_lengkap"):
                wanita.nama_lengkap = str(wanita_data["nama_lengkap"])[:120]
            if wanita_data.get("nama_panggilan"):
                wanita.nama_panggilan = str(wanita_data["nama_panggilan"])[:60]
            if wanita_data.get("anak_ke"):
                wanita.anak_ke = str(wanita_data["anak_ke"])[:40]
            if wanita_data.get("nama_ayah"):
                wanita.nama_ayah = str(wanita_data["nama_ayah"])[:120]
            if wanita_data.get("nama_ibu"):
                wanita.nama_ibu = str(wanita_data["nama_ibu"])[:120]
            if wanita_data.get("instagram"):
                wanita.instagram = str(wanita_data["instagram"]).lstrip("@")[:60]
            wanita.save()
            ringkasan["diperbarui"].append("Profil Mempelai Wanita")

    # 3. Update Acara
    acara_list = data_ai.get("acara") or []
    if update_acara and isinstance(acara_list, list) and acara_list:
        # Hapus acara lama untuk digantikan dengan susunan hasil PDF AI
        undangan.acara_list.all().delete()
        for idx, item in enumerate(acara_list):
            nama_acara = item.get("nama") or f"Acara #{idx + 1}"
            tgl_str = item.get("tanggal") or timezone.now().strftime("%Y-%m-%d")
            mulai_str = item.get("waktu_mulai") or "09:00"
            selesai_str = item.get("waktu_selesai") or ""

            # Parsing tanggal dan waktu mulai
            try:
                dt_mulai_str = f"{tgl_str} {mulai_str}"
                dt_mulai = datetime.strptime(dt_mulai_str, "%Y-%m-%d %H:%M")
                dt_mulai = timezone.make_aware(dt_mulai)
            except Exception:
                dt_mulai = timezone.now()

            dt_selesai = None
            if selesai_str:
                try:
                    dt_selesai_str = f"{tgl_str} {selesai_str}"
                    dt_selesai = datetime.strptime(dt_selesai_str, "%Y-%m-%d %H:%M")
                    dt_selesai = timezone.make_aware(dt_selesai)
                except Exception:
                    dt_selesai = None

            Acara.objects.create(
                undangan=undangan,
                nama=str(nama_acara)[:60],
                waktu_mulai=dt_mulai,
                waktu_selesai=dt_selesai,
                nama_tempat=str(item.get("nama_tempat", ""))[:160],
                alamat=str(item.get("alamat", "")),
                url_maps=str(item.get("url_maps", ""))[:200],
                urutan=idx,
            )
        ringkasan["diperbarui"].append(f"{len(acara_list)} Agenda Acara")

    # 4. Update Rekening
    rek_list = data_ai.get("rekening") or []
    if update_rekening and isinstance(rek_list, list) and rek_list:
        # Tambahkan rekening baru yang belum ada
        rekening_ditambah = 0
        for idx, r in enumerate(rek_list):
            nama_bank = str(r.get("nama_bank", "")).strip()[:60]
            nomor = str(r.get("nomor", "")).strip()[:60]
            atas_nama = str(r.get("atas_nama", "")).strip()[:120]
            if nama_bank and nomor:
                Rekening.objects.create(
                    undangan=undangan,
                    nama_bank=nama_bank,
                    nomor=nomor,
                    atas_nama=atas_nama,
                    urutan=idx,
                )
                rekening_ditambah += 1
        if rekening_ditambah:
            ringkasan["diperbarui"].append(f"{rekening_ditambah} Rekening Hadiah")

    return ringkasan
