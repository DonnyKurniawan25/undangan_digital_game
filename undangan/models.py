from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Pengaturan(models.Model):
    """Pengaturan global undangan. Cukup buat satu baris saja."""

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


class Pengantin(models.Model):
    PRIA = "pria"
    WANITA = "wanita"
    PERAN = [(PRIA, "Mempelai Pria"), (WANITA, "Mempelai Wanita")]

    peran = models.CharField(max_length=10, choices=PERAN, unique=True)
    nama_lengkap = models.CharField(max_length=120)
    nama_panggilan = models.CharField(max_length=60)
    anak_ke = models.CharField(max_length=40, blank=True, help_text="Contoh: Putra pertama")
    nama_ayah = models.CharField(max_length=120, blank=True)
    nama_ibu = models.CharField(max_length=120, blank=True)
    instagram = models.CharField(max_length=60, blank=True, help_text="Tanpa tanda @")
    foto = models.ImageField(upload_to="pengantin/", blank=True)

    class Meta:
        verbose_name = "Mempelai"
        verbose_name_plural = "Mempelai"
        ordering = ["peran"]

    def __str__(self):
        return f"{self.get_peran_display()} - {self.nama_panggilan}"


class Acara(models.Model):
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
    gambar = models.ImageField(upload_to="galeri/")
    keterangan = models.CharField(max_length=160, blank=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Foto Galeri"
        verbose_name_plural = "Foto Galeri"
        ordering = ["urutan", "id"]

    def __str__(self):
        return self.keterangan or f"Foto #{self.pk}"


class Rekening(models.Model):
    nama_bank = models.CharField(max_length=60, help_text="Contoh: BCA, Mandiri, GoPay")
    nomor = models.CharField(max_length=60)
    atas_nama = models.CharField(max_length=120)
    qr = models.ImageField(upload_to="qr/", blank=True, help_text="Opsional: gambar QRIS.")
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Rekening Hadiah"
        verbose_name_plural = "Rekening Hadiah"
        ordering = ["urutan", "id"]

    def __str__(self):
        return f"{self.nama_bank} - {self.nomor}"


class Tamu(models.Model):
    nama = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
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
            while Tamu.objects.filter(slug=calon).exclude(pk=self.pk).exists():
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
