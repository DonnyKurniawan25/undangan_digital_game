from django.contrib import admin
from django.utils.html import format_html

from .models import Acara, FotoGaleri, Pengantin, Pengaturan, Rekening, Tamu, Ucapan


@admin.register(Pengaturan)
class PengaturanAdmin(admin.ModelAdmin):
    list_display = ["judul", "hashtag"]

    def has_add_permission(self, request):
        return not Pengaturan.objects.exists()


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
