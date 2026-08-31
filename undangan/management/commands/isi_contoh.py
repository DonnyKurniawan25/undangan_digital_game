"""Mengisi database dengan data contoh supaya undangan langsung bisa dilihat.

    python manage.py isi_contoh

Jalankan dengan --bersih untuk menghapus data contoh lama lebih dulu.
"""

import secrets
from datetime import timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw

from undangan.models import (
    Acara,
    FotoGaleri,
    Pengantin,
    Pengaturan,
    Rekening,
    Tamu,
    Ucapan,
)

WARNA_CONTOH = [
    ((246, 226, 214), (214, 178, 186)),
    ((226, 234, 220), (170, 196, 168)),
    ((244, 236, 216), (222, 200, 156)),
    ((232, 226, 238), (192, 180, 210)),
    ((246, 232, 222), (226, 190, 172)),
    ((222, 234, 238), (176, 204, 214)),
]


def gambar_contoh(teks, ukuran, indeks):
    """Kartu gradien polos sebagai pengganti foto yang belum diunggah."""
    atas, bawah = WARNA_CONTOH[indeks % len(WARNA_CONTOH)]
    lebar, tinggi = ukuran
    img = Image.new("RGB", ukuran, atas)
    d = ImageDraw.Draw(img)
    for y in range(tinggi):
        rasio = y / max(1, tinggi - 1)
        d.line(
            [(0, y), (lebar, y)],
            fill=tuple(round(atas[i] + (bawah[i] - atas[i]) * rasio) for i in range(3)),
        )
    d.rectangle([12, 12, lebar - 13, tinggi - 13], outline=(255, 255, 255), width=3)
    kotak = d.textbbox((0, 0), teks)
    d.text(
        ((lebar - (kotak[2] - kotak[0])) / 2, (tinggi - (kotak[3] - kotak[1])) / 2),
        teks,
        fill=(90, 74, 66),
    )
    penyangga = BytesIO()
    img.save(penyangga, format="JPEG", quality=88)
    return ContentFile(penyangga.getvalue())


class Command(BaseCommand):
    help = "Mengisi database dengan data contoh undangan."

    def add_arguments(self, parser):
        parser.add_argument(
            "--bersih",
            action="store_true",
            help="Hapus isi tabel undangan lebih dulu.",
        )

    def handle(self, *args, **opsi):
        if opsi["bersih"]:
            for model in (Ucapan, Tamu, Rekening, FotoGaleri, Acara, Pengantin, Pengaturan):
                model.objects.all().delete()
            self.stdout.write("Data lama dihapus.")

        pengaturan = Pengaturan.ambil()
        pengaturan.judul = "Undangan Pernikahan Rina & Budi"
        pengaturan.hashtag = "#RinaBudiForever"
        pengaturan.quote = (
            "Dan di antara tanda-tanda kekuasaan-Nya diciptakan-Nya untukmu "
            "pasangan hidup dari jenismu sendiri, supaya kamu mendapat ketenangan "
            "dan dijadikan-Nya di antaramu rasa kasih dan sayang."
        )
        pengaturan.sumber_quote = "QS. Ar-Rum: 21"
        pengaturan.save()

        pria, _ = Pengantin.objects.update_or_create(
            peran=Pengantin.PRIA,
            defaults={
                "nama_lengkap": "Budi Santoso, S.Kom.",
                "nama_panggilan": "Budi",
                "anak_ke": "Putra pertama",
                "nama_ayah": "Hendra Santoso",
                "nama_ibu": "Sri Wahyuni",
                "instagram": "budisantoso",
            },
        )
        wanita, _ = Pengantin.objects.update_or_create(
            peran=Pengantin.WANITA,
            defaults={
                "nama_lengkap": "Rina Kartika Sari, S.Ds.",
                "nama_panggilan": "Rina",
                "anak_ke": "Putri kedua",
                "nama_ayah": "Ahmad Suryana",
                "nama_ibu": "Dewi Lestari",
                "instagram": "rinakartika",
            },
        )
        for i, orang in enumerate((pria, wanita)):
            if not orang.foto:
                orang.foto.save(
                    f"contoh-{orang.peran}.jpg",
                    gambar_contoh(f"Foto {orang.nama_panggilan}", (600, 750), i),
                    save=True,
                )

        hari_h = (timezone.localtime() + timedelta(days=45)).replace(
            hour=8, minute=0, second=0, microsecond=0
        )
        Acara.objects.update_or_create(
            nama="Akad Nikah",
            defaults={
                "waktu_mulai": hari_h,
                "waktu_selesai": hari_h + timedelta(hours=2),
                "nama_tempat": "Masjid Agung Al-Falah",
                "alamat": "Jl. Merdeka No. 12, Bandung, Jawa Barat",
                "url_maps": "https://maps.google.com/?q=Masjid+Agung",
                "urutan": 1,
            },
        )
        Acara.objects.update_or_create(
            nama="Resepsi",
            defaults={
                "waktu_mulai": hari_h + timedelta(hours=5),
                "waktu_selesai": hari_h + timedelta(hours=9),
                "nama_tempat": "Gedung Serbaguna Puri Anggrek",
                "alamat": "Jl. Cendana Raya No. 45, Bandung, Jawa Barat",
                "url_maps": "https://maps.google.com/?q=Puri+Anggrek",
                "urutan": 2,
            },
        )

        if not FotoGaleri.objects.exists():
            for i in range(6):
                foto = FotoGaleri(keterangan=f"Momen {i + 1}", urutan=i)
                foto.gambar.save(
                    f"galeri-contoh-{i + 1}.jpg",
                    gambar_contoh(f"Foto Galeri {i + 1}", (700, 933), i),
                    save=False,
                )
                foto.save()

        Rekening.objects.update_or_create(
            nama_bank="BCA",
            defaults={"nomor": "1234567890", "atas_nama": "Rina Kartika Sari", "urutan": 1},
        )
        Rekening.objects.update_or_create(
            nama_bank="Mandiri",
            defaults={"nomor": "0987654321", "atas_nama": "Budi Santoso", "urutan": 2},
        )

        for nama, sapaan, jumlah in [
            ("Andi Pratama", "Bapak", 2),
            ("Siti Nurhaliza", "Ibu", 1),
            ("Keluarga Wijaya", "Bapak/Ibu", 4),
        ]:
            Tamu.objects.get_or_create(
                nama=nama, defaults={"sapaan": sapaan, "jumlah_undangan": jumlah}
            )

        if not Ucapan.objects.exists():
            contoh_ucapan = [
                ("Andi Pratama", "Selamat menempuh hidup baru! Semoga samawa selalu.", Ucapan.HADIR, 2),
                ("Siti Nurhaliza", "Barakallahu lakuma wa baraka alaikuma. Bahagia selalu ya!", Ucapan.HADIR, 1),
                ("Dimas Arya", "Maaf belum bisa hadir, doa terbaik dari jauh untuk kalian berdua.", Ucapan.TIDAK, 1),
            ]
            for nama, pesan, kehadiran, jumlah in contoh_ucapan:
                Ucapan.objects.create(
                    nama=nama, pesan=pesan, kehadiran=kehadiran, jumlah_orang=jumlah
                )

        self.stdout.write(self.style.SUCCESS("Data contoh siap."))

        Pengguna = get_user_model()
        if not Pengguna.objects.filter(is_superuser=True).exists():
            sandi = secrets.token_urlsafe(12)
            Pengguna.objects.create_superuser("admin", "", sandi)
            self.stdout.write(
                self.style.WARNING(
                    f"\nAkun admin dibuat -> pengguna: admin | sandi: {sandi}\n"
                    "Simpan sandi ini dan ganti sebelum dipakai di server."
                )
            )

        self.stdout.write("\nTautan contoh:")
        for tamu in Tamu.objects.all():
            self.stdout.write(f"  /undangan/{tamu.slug}/   ({tamu.nama})")
