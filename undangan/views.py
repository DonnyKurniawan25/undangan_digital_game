import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Acara, FotoGaleri, Pengantin, Pengaturan, Rekening, Tamu, Ucapan

BATAS_UCAPAN_TAMPIL = 60

TEMPLATE_TEMA = {
    Pengaturan.TEMA_KLASIK: "undangan/game.html",
    Pengaturan.TEMA_TROPIS: "undangan/game_tropis.html",
    Pengaturan.TEMA_LOMBOK: "undangan/game_lombok.html",
}


def _serialisasi(ucapan):
    return {
        "nama": ucapan.nama,
        "pesan": ucapan.pesan,
        "kehadiran": ucapan.get_kehadiran_display(),
        "kode_kehadiran": ucapan.kehadiran,
        "waktu": timezone.localtime(ucapan.dibuat).strftime("%d %b %Y, %H:%M"),
    }


def landing(request):
    pengaturan = Pengaturan.ambil()
    pria = Pengantin.objects.filter(peran=Pengantin.PRIA).first()
    wanita = Pengantin.objects.filter(peran=Pengantin.WANITA).first()
    acara_list = list(Acara.objects.all())

    konteks = {
        "pengaturan": pengaturan,
        "pria": pria,
        "wanita": wanita,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all()[:6],
        "jumlah_tamu": Tamu.objects.count(),
        "jumlah_ucapan": Ucapan.objects.filter(disetujui=True).count(),
    }
    return render(request, "undangan/landing.html", konteks)


def undangan(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    pengaturan = Pengaturan.ambil()
    acara_list = list(Acara.objects.all())
    pria = Pengantin.objects.filter(peran=Pengantin.PRIA).first()
    wanita = Pengantin.objects.filter(peran=Pengantin.WANITA).first()

    konteks = {
        "pengaturan": pengaturan,
        "tamu": tamu,
        "pria": pria,
        "wanita": wanita,
        "mempelai": [orang for orang in (pria, wanita) if orang],
        "acara_list": acara_list,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all(),
        "rekening_list": Rekening.objects.all(),
        "ucapan_list": Ucapan.objects.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL],
        "jumlah_hadir": Ucapan.objects.filter(disetujui=True, kehadiran=Ucapan.HADIR).count(),
    }
    # Parameter tema pada URL dipakai untuk pratinjau tanpa mengubah pengaturan.
    tema = request.GET.get("tema") or pengaturan.tema
    template = TEMPLATE_TEMA.get(tema, TEMPLATE_TEMA[Pengaturan.TEMA_KLASIK])
    return render(request, template, konteks)


def undangan_lombok(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    pengaturan = Pengaturan.ambil()
    acara_list = list(Acara.objects.all())
    pria = Pengantin.objects.filter(peran=Pengantin.PRIA).first()
    wanita = Pengantin.objects.filter(peran=Pengantin.WANITA).first()

    konteks = {
        "pengaturan": pengaturan,
        "tamu": tamu,
        "pria": pria,
        "wanita": wanita,
        "mempelai": [orang for orang in (pria, wanita) if orang],
        "acara_list": acara_list,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all(),
        "rekening_list": Rekening.objects.all(),
        "ucapan_list": Ucapan.objects.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL],
        "jumlah_hadir": Ucapan.objects.filter(disetujui=True, kehadiran=Ucapan.HADIR).count(),
    }
    return render(request, "undangan/game_lombok.html", konteks)


def undangan_tropis(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    pengaturan = Pengaturan.ambil()
    acara_list = list(Acara.objects.all())
    pria = Pengantin.objects.filter(peran=Pengantin.PRIA).first()
    wanita = Pengantin.objects.filter(peran=Pengantin.WANITA).first()

    konteks = {
        "pengaturan": pengaturan,
        "tamu": tamu,
        "pria": pria,
        "wanita": wanita,
        "mempelai": [orang for orang in (pria, wanita) if orang],
        "acara_list": acara_list,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all(),
        "rekening_list": Rekening.objects.all(),
        "ucapan_list": Ucapan.objects.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL],
        "jumlah_hadir": Ucapan.objects.filter(disetujui=True, kehadiran=Ucapan.HADIR).count(),
    }
    return render(request, "undangan/game_tropis.html", konteks)


@require_http_methods(["GET", "POST"])
def api_ucapan(request):
    if request.method == "GET":
        antrian = Ucapan.objects.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL]
        return JsonResponse({"ucapan": [_serialisasi(u) for u in antrian]})

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "pesan": "Format data tidak dikenali."}, status=400)

    nama = str(data.get("nama", "")).strip()[:120]
    pesan = str(data.get("pesan", "")).strip()[:1000]
    kehadiran = str(data.get("kehadiran", Ucapan.HADIR)).strip()
    kode_sah = {kode for kode, _ in Ucapan.KEHADIRAN}

    if not nama:
        return JsonResponse({"ok": False, "pesan": "Nama belum diisi."}, status=400)
    if not pesan:
        return JsonResponse({"ok": False, "pesan": "Ucapan belum diisi."}, status=400)
    if kehadiran not in kode_sah:
        kehadiran = Ucapan.HADIR

    try:
        jumlah_orang = max(1, min(20, int(data.get("jumlah_orang", 1))))
    except (TypeError, ValueError):
        jumlah_orang = 1

    tamu = None
    slug = str(data.get("slug", "")).strip()
    if slug:
        tamu = Tamu.objects.filter(slug=slug).first()

    ucapan = Ucapan.objects.create(
        tamu=tamu,
        nama=nama,
        pesan=pesan,
        kehadiran=kehadiran,
        jumlah_orang=jumlah_orang,
    )
    return JsonResponse({"ok": True, "ucapan": _serialisasi(ucapan)}, status=201)
