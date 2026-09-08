import datetime
import re
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


def konversi_url_gambar(url):
    """
    Mengonversi URL eksternal (terutama Google Drive sharing link)
    menjadi URL direct embed gambar yang kompatibel dengan tag <img>.
    """
    if not url:
        return ""
    url = url.strip()

    # Deteksi Google Drive link
    # Format 1: drive.google.com/file/d/<FILE_ID>/view...
    # Format 2: drive.google.com/open?id=<FILE_ID>
    # Format 3: drive.google.com/uc?id=<FILE_ID>
    gdrive_match = re.search(r"drive\.google\.com/(?:file/d/|open\?id=|uc\?(?:export=view&)?id=)([\w-]+)", url)
    if gdrive_match:
        file_id = gdrive_match.group(1)
        return f"https://lh3.googleusercontent.com/d/{file_id}"

    # Deteksi Dropbox link (dl=0 -> raw=1)
    if "dropbox.com" in url:
        return url.replace("dl=0", "raw=1")

    return url


class Pengaturan(models.Model):
    """Pengaturan global / bawaan undangan."""

    TEMA_KLASIK = "klasik"
    TEMA_TROPIS = "tropis"
    TEMA_LOMBOK = "lombok"
    TEMA_DESA = "desa"
    TEMA_GEDUNG = "gedung"
    TEMA_SAFARI = "safari"
    TEMA = [
        (TEMA_KLASIK, "Taman Pixel Jawa - tampak atas"),
        (TEMA_TROPIS, "Taman Tropis - isometrik"),
        (TEMA_LOMBOK, "Pantai Lombok Sasak Wedding"),
        (TEMA_DESA, "Desa Asri Parahyangan - Gaya Stardew Valley"),
        (TEMA_GEDUNG, "Grand Ballroom Gedung Mewah - Modern Indoor-Outdoor"),
        (TEMA_SAFARI, "Taman Safari Kebun Binatang Rimba Tropis"),
    ]

    tema = models.CharField(
        max_length=20,
        choices=TEMA,
        default=TEMA_KLASIK,
        help_text="Tampilan undangan. Tema lain bisa dicoba lewat parameter tema pada URL.",
    )
    judul = models.CharField(max_length=120, default="Undangan Pernikahan")
    hashtag = models.CharField(max_length=60, blank=True, help_text="Contoh: #RinaDanBudi")
    quote = models.TextField(
        blank=True,
        help_text="Kutipan / ayat yang tampil di layar pembuka.",
    )
    sumber_quote = models.CharField(max_length=120, blank=True)
    musik = models.FileField(
        upload_to="musik/",
        blank=True,
        help_text="Lagu latar (.mp3). Diputar setelah tamu menekan tombol Buka Undangan.",
    )
    catatan_penutup = models.TextField(
        blank=True,
        default="Merupakan suatu kehormatan dan kebahagiaan bagi kami "
        "apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.",
    )

    class Meta:
        verbose_name = "Pengaturan"
        verbose_name_plural = "Pengaturan"

    def __str__(self):
        return self.judul

    @classmethod
    def ambil(cls):
        obj = cls.objects.first()
        return obj or cls.objects.create()


class Undangan(models.Model):
    """Model utama undangan yang dimiliki oleh pengguna terdaftar."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="daftar_undangan"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="Tautan unik undangan. Contoh: budi-dan-ani -> domain.com/u/budi-dan-ani",
    )
    judul = models.CharField(max_length=120, default="Undangan Pernikahan")
    tema = models.CharField(
        max_length=20,
        choices=Pengaturan.TEMA,
        default=Pengaturan.TEMA_KLASIK,
        help_text="Pilihan tema visual game interaktif.",
    )
    hashtag = models.CharField(max_length=60, blank=True, help_text="Contoh: #BudiAniWedding")
    quote = models.TextField(
        blank=True,
        help_text="Kutipan ayat / kata mutiara di layar awal.",
    )
    sumber_quote = models.CharField(max_length=120, blank=True, help_text="Contoh: QS. Ar-Rum: 21")
    musik = models.FileField(
        upload_to="musik/",
        blank=True,
        help_text="Unggah file musik (.mp3 / .wav).",
    )
    musik_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Atau tempel link file audio eksternal jika tidak ingin upload berkas.",
    )
    catatan_penutup = models.TextField(
        blank=True,
        default="Merupakan suatu kehormatan dan kebahagiaan bagi kami "
        "apabila Bapak/Ibu/Saudara/i berkenan hadir untuk memberikan doa restu.",
    )
    STATUS_TRIAL = "trial"
    STATUS_MENUNGGU = "menunggu"
    STATUS_AKTIF = "aktif"
    STATUS_KADALUARSA = "kadaluarsa"
    STATUS_LANGGANAN = [
        (STATUS_TRIAL, "Masa Uji Coba (1 Bulan)"),
        (STATUS_MENUNGGU, "Menunggu Konfirmasi Pembayaran"),
        (STATUS_AKTIF, "Aktif Penuh (Berbayar)"),
        (STATUS_KADALUARSA, "Masa Aktif Habis"),
    ]

    status_langganan = models.CharField(
        max_length=20,
        choices=STATUS_LANGGANAN,
        default=STATUS_TRIAL,
        help_text="Status keaktifan & masa berlangganan undangan.",
    )
    trial_berakhir = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Batas waktu uji coba gratis 1 bulan (30 hari) sejak dibuat.",
    )
    aktif_berakhir = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Batas waktu online aktif berbayar (30 hari / fleksibel).",
    )
    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Undangan"
        verbose_name_plural = "Daftar Undangan"
        ordering = ["-dibuat"]

    def __str__(self):
        return f"{self.judul} ({self.slug})"

    def save(self, *args, **kwargs):
        if not self.trial_berakhir:
            self.trial_berakhir = timezone.now() + datetime.timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def is_online_aktif(self):
        """Menentukan apakah tamu umum diizinkan melihat isi game undangan."""
        skrg = timezone.now()
        # Jika berbayar aktif
        if self.status_langganan == self.STATUS_AKTIF:
            return bool(self.aktif_berakhir and self.aktif_berakhir > skrg)
        # Jika masih dalam masa uji coba 1 bulan
        if self.status_langganan == self.STATUS_TRIAL:
            return bool(self.trial_berakhir and self.trial_berakhir > skrg)
        # Jika menunggu verifikasi pembayaran
        if self.status_langganan == self.STATUS_MENUNGGU:
            if self.aktif_berakhir and self.aktif_berakhir > skrg:
                return True
            if self.trial_berakhir and self.trial_berakhir > skrg:
                return True
            return False
        return False

    PAKET_1_BULAN = 1
    PAKET_6_BULAN = 6
    PAKET_12_BULAN = 12

    PAKET_PILIHAN = [
        (1, "1 Bulan (30 Hari)", 30000, "Paket Standar 1 Bulan"),
        (6, "6 Bulan (180 Hari)", 150000, "Paket 6 Bulan — Hemat Rp 30.000"),
        (12, "1 Tahun (365 Hari)", 250000, "Paket 1 Tahun — Diskon Rp 110.000 (Paling Hemat)"),
    ]

    @property
    def status_label(self):
        skrg = timezone.now()
        if self.status_langganan == self.STATUS_AKTIF:
            if self.aktif_berakhir and self.aktif_berakhir > skrg:
                return f"Aktif Penuh ({self.sisa_hari_aktif} Hari)"
            if self.is_masa_tenggang:
                return f"Masa Aktif Habis — Tenggang ({self.sisa_hari_tenggang} Hari Lagi)"
            return "Kedaluwarsa > 1 Bulan (Siap Dibersihkan)"
        if self.status_langganan == self.STATUS_MENUNGGU:
            return "Menunggu Verifikasi Pembayaran"
        if self.status_langganan == self.STATUS_TRIAL:
            if self.trial_berakhir and self.trial_berakhir > skrg:
                return f"Masa Uji Coba Gratis ({self.sisa_waktu_trial})"
            if self.is_masa_tenggang:
                return f"Uji Coba Berakhir — Tenggang ({self.sisa_hari_tenggang} Hari Lagi)"
            return "Trial Kedaluwarsa (Siap Dibersihkan)"
        return "Tidak Aktif"

    @property
    def sisa_waktu_trial(self):
        if not self.trial_berakhir:
            return "Habis"
        skrg = timezone.now()
        if self.trial_berakhir <= skrg:
            return "Habis"
        selisih = self.trial_berakhir - skrg
        if selisih.days > 0:
            jam = int(selisih.seconds // 3600)
            return f"{selisih.days} hari {jam} jam lagi"
        if selisih.total_seconds() >= 3600:
            jam = int(selisih.total_seconds() // 3600)
            return f"{jam} jam lagi"
        menit = int(selisih.total_seconds() // 60)
        return f"{menit} menit lagi"

    @property
    def sisa_hari_aktif(self):
        if not self.aktif_berakhir:
            return 0
        skrg = timezone.now()
        if self.aktif_berakhir <= skrg:
            return 0
        return (self.aktif_berakhir - skrg).days

    @property
    def batas_tenggang_berakhir(self):
        """Batas akhir kesempatan perpanjangan 1 bulan (30 hari) setelah masa aktif/trial berakhir."""
        if self.aktif_berakhir:
            return self.aktif_berakhir + datetime.timedelta(days=30)
        if self.trial_berakhir:
            return self.trial_berakhir + datetime.timedelta(days=30)
        return None

    @property
    def is_masa_tenggang(self):
        """
        Menentukan apakah undangan saat ini berada dalam masa tenggang 1 bulan (30 hari).
        Selama tenggang, undangan offline bagi tamu umum, tapi pemilik diberi kesempatan memperpanjang.
        """
        if self.is_online_aktif:
            return False
        skrg = timezone.now()
        bts = self.batas_tenggang_berakhir
        if bts and bts > skrg:
            return True
        return False

    @property
    def is_siap_dibersihkan(self):
        """
        Jika masa tenggang 1 bulan telah lewat dan tidak kunjung diperpanjang,
        undangan dinyatakan kedaluwarsa permanen dan siap dibersihkan total oleh superadmin
        hingga file foto-fotonya terhapus di server.
        """
        if self.is_online_aktif:
            return False
        skrg = timezone.now()
        bts = self.batas_tenggang_berakhir
        if bts and bts <= skrg:
            return True
        return False

    @property
    def sisa_hari_tenggang(self):
        """Sisa hari kesempatan perpanjangan dalam masa tenggang 1 bulan."""
        if not self.is_masa_tenggang:
            return 0
        bts = self.batas_tenggang_berakhir
        skrg = timezone.now()
        if bts and bts > skrg:
            return max(1, (bts - skrg).days)
        return 0

    def tambah_durasi(self, jumlah_hari=30):
        """Menambah atau memperpanjang masa aktif online sebesar jumlah_hari (default 30 hari)."""
        skrg = timezone.now()
        dasar_waktu = self.aktif_berakhir if (self.aktif_berakhir and self.aktif_berakhir > skrg) else skrg
        self.aktif_berakhir = dasar_waktu + datetime.timedelta(days=int(jumlah_hari))
        self.status_langganan = self.STATUS_AKTIF
        self.save(update_fields=["aktif_berakhir", "status_langganan"])

    def tambah_durasi_bulan(self, durasi_bulan=1):
        """Menambah masa aktif sesuai pilihan paket bulan (1 bulan = 30 hari, 6 bulan = 180 hari, 12 bulan = 365 hari)."""
        durasi_bulan = int(durasi_bulan)
        if durasi_bulan == 12:
            hari = 365
        elif durasi_bulan == 6:
            hari = 180
        else:
            hari = durasi_bulan * 30
        self.tambah_durasi(hari)

    def aktifkan_satu_bulan(self):
        """Menambah atau memperpanjang masa aktif online 30 hari."""
        self.tambah_durasi_bulan(1)

    def bersihkan_total(self):
        """
        Menghapus seluruh berkas media fisik di harddisk server (foto galeri, foto pengantin,
        QR rekening, musik upload, dan bukti transfer), lalu menghapus objek undangan dari database
        agar beban server benar-benar bersih dan ringan.
        Mengembalikan tuple: (judul, slug, jumlah_berkas_dihapus)
        """
        berkas_dihapus = 0

        # 1. Foto Galeri Prewedding
        for foto in self.galeri_list.all():
            if foto.gambar:
                try:
                    foto.gambar.delete(save=False)
                    berkas_dihapus += 1
                except Exception:
                    pass

        # 2. Foto Pengantin Pria & Wanita
        for p in self.mempelai_list.all():
            if p.foto:
                try:
                    p.foto.delete(save=False)
                    berkas_dihapus += 1
                except Exception:
                    pass

        # 3. Berkas Gambar QR Rekening
        for r in self.rekening_list.all():
            if r.qr:
                try:
                    r.qr.delete(save=False)
                    berkas_dihapus += 1
                except Exception:
                    pass

        # 4. Berkas Musik Undangan
        if self.musik:
            try:
                self.musik.delete(save=False)
                berkas_dihapus += 1
            except Exception:
                pass

        # 5. Berkas Bukti Pembayaran
        for bayar in self.riwayat_pembayaran.all():
            if bayar.bukti_bayar:
                try:
                    bayar.bukti_bayar.delete(save=False)
                    berkas_dihapus += 1
                except Exception:
                    pass

        judul = self.judul
        slug = self.slug
        self.delete()
        return judul, slug, berkas_dihapus

    @property
    def path_publik(self):
        """
        Path URL publik:
        - Saat masih uji coba (belum bayar): /trial/<slug>/ (misal: jelajah.biz.id/trial/rana&cahyo)
        - Saat sudah bayar (aktif): /<slug>/ (misal: jelajah.biz.id/rana&cahyo)
        """
        if self.status_langganan == self.STATUS_AKTIF:
            return f"/{self.slug}/"
        return f"/trial/{self.slug}/"

    def get_tamu_path(self, slug_tamu):
        """Path URL personal tamu sesuai status pembayaran."""
        if self.status_langganan == self.STATUS_AKTIF:
            return f"/{self.slug}/{slug_tamu}/"
        return f"/trial/{self.slug}/{slug_tamu}/"

    def get_url_publik(self, request=None):
        """Membangun tautan publik lengkap menggunakan domain saat ini atau jelajah.biz.id."""
        path = self.path_publik
        if request:
            return request.build_absolute_uri(path)
        return f"https://jelajah.biz.id{path}"

    def get_tamu_url(self, slug_tamu, request=None):
        """Membangun tautan personal tamu lengkap."""
        path = self.get_tamu_path(slug_tamu)
        if request:
            return request.build_absolute_uri(path)
        return f"https://jelajah.biz.id{path}"

    @property
    def url_musik(self):
        if self.musik:
            try:
                return self.musik.url
            except ValueError:
                pass
        if self.musik_url:
            return self.musik_url
        return "/static/musik/desa_asri.wav"


class Pengantin(models.Model):
    PRIA = "pria"
    WANITA = "wanita"
    PERAN = [(PRIA, "Mempelai Pria"), (WANITA, "Mempelai Wanita")]

    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="mempelai_list",
    )
    peran = models.CharField(max_length=10, choices=PERAN)
    nama_lengkap = models.CharField(max_length=120)
    nama_panggilan = models.CharField(max_length=60)
    anak_ke = models.CharField(max_length=40, blank=True, help_text="Contoh: Putra pertama")
    nama_ayah = models.CharField(max_length=120, blank=True)
    nama_ibu = models.CharField(max_length=120, blank=True)
    instagram = models.CharField(max_length=60, blank=True, help_text="Tanpa tanda @")
    foto = models.ImageField(upload_to="pengantin/", blank=True)
    foto_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Atau tempel tautan gambar eksternal (Google Drive, Imgur, Web URL).",
    )

    class Meta:
        verbose_name = "Mempelai"
        verbose_name_plural = "Mempelai"
        ordering = ["peran"]

    def __str__(self):
        return f"{self.get_peran_display()} - {self.nama_panggilan}"

    @property
    def url_tampil(self):
        if self.foto:
            try:
                return self.foto.url
            except ValueError:
                pass
        if self.foto_url:
            return konversi_url_gambar(self.foto_url)
        return ""


class Acara(models.Model):
    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="acara_list",
    )
    nama = models.CharField(max_length=60, help_text="Contoh: Akad Nikah / Resepsi")
    waktu_mulai = models.DateTimeField()
    waktu_selesai = models.DateTimeField(null=True, blank=True)
    nama_tempat = models.CharField(max_length=160)
    alamat = models.TextField(blank=True)
    url_maps = models.URLField(blank=True, help_text="Link Google Maps lokasi acara.")
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Acara"
        verbose_name_plural = "Acara"
        ordering = ["urutan", "waktu_mulai"]

    def __str__(self):
        return f"{self.nama} - {self.waktu_mulai:%d %b %Y}"


class FotoGaleri(models.Model):
    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="galeri_list",
    )
    gambar = models.ImageField(upload_to="galeri/", blank=True)
    gambar_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Tautan gambar eksternal (Google Drive, Imgur, Cloudinary, dll).",
    )
    keterangan = models.CharField(max_length=160, blank=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Foto Galeri"
        verbose_name_plural = "Foto Galeri"
        ordering = ["urutan", "id"]

    def __str__(self):
        return self.keterangan or f"Foto #{self.pk}"

    @property
    def url_tampil(self):
        if self.gambar:
            try:
                return self.gambar.url
            except ValueError:
                pass
        if self.gambar_url:
            return konversi_url_gambar(self.gambar_url)
        return ""


class Rekening(models.Model):
    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="rekening_list",
    )
    nama_bank = models.CharField(max_length=60, help_text="Contoh: BCA, Mandiri, GoPay")
    nomor = models.CharField(max_length=60)
    atas_nama = models.CharField(max_length=120)
    qr = models.ImageField(upload_to="qr/", blank=True, help_text="Opsional: unggah gambar QRIS.")
    qr_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="Atau tempel tautan gambar QRIS.",
    )
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Rekening Hadiah"
        verbose_name_plural = "Rekening Hadiah"
        ordering = ["urutan", "id"]

    def __str__(self):
        return f"{self.nama_bank} - {self.nomor}"

    @property
    def url_tampil(self):
        if self.qr:
            try:
                return self.qr.url
            except ValueError:
                pass
        if self.qr_url:
            return konversi_url_gambar(self.qr_url)
        return ""


class Tamu(models.Model):
    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="tamu_list",
    )
    nama = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    sapaan = models.CharField(
        max_length=40, blank=True, help_text="Contoh: Bapak, Ibu, Saudara/i."
    )
    jumlah_undangan = models.PositiveIntegerField(default=1)
    catatan = models.CharField(max_length=200, blank=True)
    pertama_dibuka = models.DateTimeField(null=True, blank=True)
    jumlah_dibuka = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Tamu"
        verbose_name_plural = "Daftar Tamu"
        ordering = ["nama"]

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.slug:
            dasar = slugify(self.nama) or "tamu"
            calon, n = dasar, 2
            qs = Tamu.objects.all()
            if self.undangan:
                qs = qs.filter(undangan=self.undangan)
            while qs.filter(slug=calon).exclude(pk=self.pk).exists():
                calon = f"{dasar}-{n}"
                n += 1
            self.slug = calon
        super().save(*args, **kwargs)

    def catat_kunjungan(self):
        if self.pertama_dibuka is None:
            self.pertama_dibuka = timezone.now()
        self.jumlah_dibuka += 1
        self.save(update_fields=["pertama_dibuka", "jumlah_dibuka"])

    @property
    def sapaan_lengkap(self):
        return f"{self.sapaan} {self.nama}".strip()


class Ucapan(models.Model):
    HADIR = "hadir"
    TIDAK = "tidak"
    RAGU = "ragu"
    KEHADIRAN = [
        (HADIR, "Insya Allah hadir"),
        (TIDAK, "Maaf, tidak dapat hadir"),
        (RAGU, "Masih ragu"),
    ]

    undangan = models.ForeignKey(
        Undangan,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="ucapan_list",
    )
    tamu = models.ForeignKey(
        Tamu, null=True, blank=True, on_delete=models.SET_NULL, related_name="ucapan"
    )
    nama = models.CharField(max_length=120)
    pesan = models.TextField()
    kehadiran = models.CharField(max_length=10, choices=KEHADIRAN, default=HADIR)
    jumlah_orang = models.PositiveIntegerField(default=1)
    disetujui = models.BooleanField(
        default=True, help_text="Hilangkan centang untuk menyembunyikan dari papan ucapan."
    )
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ucapan & RSVP"
        verbose_name_plural = "Ucapan & RSVP"
        ordering = ["-dibuat"]

    def __str__(self):
        return f"{self.nama}: {self.pesan[:40]}"


class Pembayaran(models.Model):
    STATUS_MENUNGGU = "menunggu"
    STATUS_DISETUJUI = "disetujui"
    STATUS_DITOLAK = "ditolak"
    STATUS = [
        (STATUS_MENUNGGU, "Menunggu Verifikasi"),
        (STATUS_DISETUJUI, "Disetujui / Aktif"),
        (STATUS_DITOLAK, "Ditolak"),
    ]

    undangan = models.ForeignKey(
        Undangan, on_delete=models.CASCADE, related_name="riwayat_pembayaran"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="daftar_pembayaran"
    )
    nominal = models.PositiveIntegerField(
        default=30000, help_text="Biaya aktivasi Rp 30.000 / bulan."
    )
    durasi_bulan = models.PositiveIntegerField(default=1)
    metode = models.CharField(max_length=60, default="Transfer Bank / QRIS")
    bukti_bayar = models.ImageField(upload_to="bukti_bayar/")
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS_MENUNGGU)
    catatan = models.TextField(blank=True, help_text="Catatan transfer dari user / alasan penolakan.")
    dibuat = models.DateTimeField(auto_now_add=True)
    diverifikasi_pada = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Pembayaran"
        verbose_name_plural = "Daftar Pembayaran"
        ordering = ["-dibuat"]

    def __str__(self):
        return f"Pembayaran #{self.pk} - {self.undangan.slug} ({self.get_status_display()})"

    @property
    def label_durasi(self):
        if self.durasi_bulan == 12:
            return "1 Tahun (365 Hari)"
        elif self.durasi_bulan == 6:
            return "6 Bulan (180 Hari)"
        return f"{self.durasi_bulan} Bulan (30 Hari)"

