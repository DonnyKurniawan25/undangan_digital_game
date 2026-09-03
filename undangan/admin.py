from django.contrib import admin
from django.utils.html import format_html

from .models import Acara, FotoGaleri, Pengantin, Pengaturan, Rekening, Tamu, Ucapan


@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    list_display = ["judul", "tema", "hashtag", "status_musik"]
    fieldsets = [
        ("Tampilan & Informasi Utama", {
            "fields": ["judul", "tema", "hashtag"]
        }),
        ("Musik Latar Undangan (Semua Template)", {
            "fields": ["musik", "pratinjau_audio"],
            "description": "Unggah file musik (.mp3 atau .wav). Musik ini akan diputar otomatis di SEMUA template setelah tamu membuka undangan. Jika kosong, sistem otomatis memakai musik santai pedesaan bawaan."
        }),
        ("Kutipan / Doa & Catatan", {
            "fields": ["quote", "sumber_quote", "catatan_penutup"]
        }),
    ]
    readonly_fields = ["pratinjau_audio"]

    def has_add_permission(self, request):
        return not Pengaturan.objects.exists()

    @admin.display(description="Status Musik")
    def status_musik(self, obj):
        if obj.musik:
            return format_html('<span style="color:#2b8a3e;font-weight:bold;">✓ Musik Kustom</span>')
        return format_html('<span style="color:#b87418;">♫ Musik Bawaan (Default)</span>')

    @admin.display(description="Dengarkan Musik Saat Ini")
    def pratinjau_audio(self, obj):
        url = obj.musik.url if obj.musik else "/static/musik/desa_asri.wav"
        label = f"File Terpasang: {obj.musik.name}" if obj.musik else "Musik Bawaan: static/musik/desa_asri.wav"
        return format_html(
            '<div style="margin-top:6px;"><p style="margin:0 0 6px;color:#555;"><b>{}</b></p><audio controls src="{}" style="height:36px;"></audio></div>',
            label, url
        )


@admin.register(Pengantin)
class PengantinAdmin(admin.ModelAdmin):
    list_display = ["peran", "nama_panggilan", "nama_lengkap"]


@admin.register(Acara)
class AcaraAdmin(admin.ModelAdmin):
    list_display = ["nama", "waktu_mulai", "nama_tempat"]
    list_editable = ["waktu_mulai"]


@admin.register(FotoGaleri)
class FotoGaleriAdmin(admin.ModelAdmin):
    list_display = ["pratinjau", "keterangan", "urutan"]
    list_editable = ["keterangan", "urutan"]

    @admin.display(description="Pratinjau")
    def pratinjau(self, obj):
        if obj.gambar:
            return format_html('<img src="{}" style="height:56px;border-radius:4px">', obj.gambar.url)
        return "-"


@admin.register(Rekening)
class RekeningAdmin(admin.ModelAdmin):
    list_display = ["nama_bank", "nomor", "atas_nama", "urutan"]


@admin.register(Tamu)
class TamuAdmin(admin.ModelAdmin):
    list_display = ["nama", "sapaan", "tautan", "jumlah_dibuka", "pertama_dibuka"]
    search_fields = ["nama", "slug"]
    readonly_fields = ["pertama_dibuka", "jumlah_dibuka"]

    @admin.display(description="Link undangan")
    def tautan(self, obj):
        url = f"/undangan/{obj.slug}/"
        return format_html('<a href="{}" target="_blank">{}</a>', url, url)


@admin.register(Ucapan)
class UcapanAdmin(admin.ModelAdmin):
    list_display = ["nama", "kehadiran", "jumlah_orang", "disetujui", "dibuat"]
    list_filter = ["kehadiran", "disetujui"]
    list_editable = ["disetujui"]
    search_fields = ["nama", "pesan"]


admin.site.site_header = "Panel Undangan Pernikahan"
admin.site.site_title = "Undangan"
admin.site.index_title = "Kelola isi undangan"
