import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .models import Acara, FotoGaleri, Pengantin, Pengaturan, Rekening, Tamu, Ucapan, Undangan

BATAS_UCAPAN_TAMPIL = 60

TEMPLATE_TEMA = {
    Pengaturan.TEMA_KLASIK: "undangan/game.html",
    Pengaturan.TEMA_TROPIS: "undangan/game_tropis.html",
    Pengaturan.TEMA_LOMBOK: "undangan/game_lombok.html",
    Pengaturan.TEMA_DESA: "undangan/game_desa.html",
    Pengaturan.TEMA_GEDUNG: "undangan/game_gedung.html",
    Pengaturan.TEMA_SAFARI: "undangan/game_safari.html",
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

    user_undangan = None
    if request.user.is_authenticated:
        user_undangan = Undangan.objects.filter(user=request.user).first()

    konteks = {
        "pengaturan": pengaturan,
        "user_undangan": user_undangan,
        "pria": pria,
        "wanita": wanita,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all()[:6],
        "jumlah_tamu": Tamu.objects.count(),
        "jumlah_ucapan": Ucapan.objects.filter(disetujui=True).count(),
    }
    return render(request, "undangan/landing.html", konteks)


def _tampilkan_undangan_game(request, undangan_obj, slug_tamu=None):
    """
    Fungsi pembantu internal untuk merender dunia game interaktif per undangan.
    Memeriksa masa aktif online (trial 1 hari / aktif penuh).
    """
    is_owner_or_admin = request.user.is_authenticated and (
        request.user == undangan_obj.user or request.user.is_superuser
    )

    if not undangan_obj.is_online_aktif and not is_owner_or_admin:
        return render(request, "undangan/trial_expired.html", {
            "undangan": undangan_obj,
            "tamu": None,
        })

    tamu = None
    if slug_tamu:
        tamu = get_object_or_404(Tamu, undangan=undangan_obj, slug=slug_tamu)
        tamu.catat_kunjungan()

    acara_list = list(undangan_obj.acara_list.all())
    pria = undangan_obj.mempelai_list.filter(peran=Pengantin.PRIA).first()
    wanita = undangan_obj.mempelai_list.filter(peran=Pengantin.WANITA).first()

    konteks = {
        "pengaturan": undangan_obj,
        "undangan": undangan_obj,
        "musik_url": undangan_obj.url_musik,
        "tamu": tamu,
        "pria": pria,
        "wanita": wanita,
        "pengantin_pria": pria,
        "pengantin_wanita": wanita,
        "mempelai": [orang for orang in (pria, wanita) if orang],
        "acara_list": acara_list,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": undangan_obj.galeri_list.all(),
        "rekening_list": undangan_obj.rekening_list.all(),
        "ucapan_list": undangan_obj.ucapan_list.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL],
        "jumlah_hadir": undangan_obj.ucapan_list.filter(disetujui=True, kehadiran=Ucapan.HADIR).count(),
        "undangan_slug": undangan_obj.slug,
        "is_owner_or_admin": is_owner_or_admin,
        "is_online_aktif": undangan_obj.is_online_aktif,
        "is_trial_link": (undangan_obj.status_langganan != Undangan.STATUS_AKTIF),
    }

    tema = request.GET.get("tema") or undangan_obj.tema
    template = TEMPLATE_TEMA.get(tema, TEMPLATE_TEMA[Pengaturan.TEMA_KLASIK])
    return render(request, template, konteks)


def undangan_publik_trial(request, slug_undangan, slug_tamu=None):
    """
    Rute Khusus Uji Coba: /trial/<slug>/ (misal: jelajah.biz.id/trial/rana&cahyo)
    Jika pengguna sudah membayar/aktif penuh, dialihkan otomatis ke tautan langsung /<slug>/.
    """
    undangan_obj = get_object_or_404(Undangan, slug=slug_undangan)

    if undangan_obj.status_langganan == Undangan.STATUS_AKTIF:
        target = f"/{undangan_obj.slug}/"
        if slug_tamu:
            target = f"/{undangan_obj.slug}/{slug_tamu}/"
        return redirect(target)

    return _tampilkan_undangan_game(request, undangan_obj, slug_tamu)


def undangan_publik_root(request, slug_undangan, slug_tamu=None):
    """
    Rute Langsung Kustom (Berbayar): /<slug>/ (misal: jelajah.biz.id/rana&cahyo)
    Jika belum membayar (masih masa trial), dialihkan otomatis ke /trial/<slug>/.
    """
    undangan_obj = get_object_or_404(Undangan, slug=slug_undangan)

    if undangan_obj.status_langganan != Undangan.STATUS_AKTIF:
        target = f"/trial/{undangan_obj.slug}/"
        if slug_tamu:
            target = f"/trial/{undangan_obj.slug}/{slug_tamu}/"
        return redirect(target)

    return _tampilkan_undangan_game(request, undangan_obj, slug_tamu)


def u_undangan(request, slug_undangan, slug_tamu=None):
    """
    Rute warisan /u/<slug_undangan>/ untuk kompatibilitas.
    Dialihkan ke rute kanonikal yang sesuai (trial atau langsung).
    """
    undangan_obj = get_object_or_404(Undangan, slug=slug_undangan)
    if slug_tamu:
        return redirect(undangan_obj.get_tamu_path(slug_tamu))
    return redirect(undangan_obj.path_publik)


def _buat_konteks_undangan(tamu=None):
    pengaturan = Pengaturan.ambil()
    acara_list = list(Acara.objects.all())
    pria = Pengantin.objects.filter(peran=Pengantin.PRIA).first()
    wanita = Pengantin.objects.filter(peran=Pengantin.WANITA).first()
    musik_url = pengaturan.musik.url if pengaturan.musik else "/static/musik/desa_asri.wav"

    return {
        "pengaturan": pengaturan,
        "musik_url": musik_url,
        "tamu": tamu,
        "pria": pria,
        "wanita": wanita,
        "pengantin_pria": pria,
        "pengantin_wanita": wanita,
        "mempelai": [orang for orang in (pria, wanita) if orang],
        "acara_list": acara_list,
        "acara_utama": acara_list[0] if acara_list else None,
        "galeri": FotoGaleri.objects.all(),
        "rekening_list": Rekening.objects.all(),
        "ucapan_list": Ucapan.objects.filter(disetujui=True)[:BATAS_UCAPAN_TAMPIL],
        "jumlah_hadir": Ucapan.objects.filter(disetujui=True, kehadiran=Ucapan.HADIR).count(),
    }


def undangan(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    tema = request.GET.get("tema") or konteks["pengaturan"].tema
    template = TEMPLATE_TEMA.get(tema, TEMPLATE_TEMA[Pengaturan.TEMA_KLASIK])
    return render(request, template, konteks)


def undangan_lombok(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    return render(request, "undangan/game_lombok.html", konteks)


def undangan_tropis(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    return render(request, "undangan/game_tropis.html", konteks)


def undangan_desa(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    return render(request, "undangan/game_desa.html", konteks)


def undangan_gedung(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    return render(request, "undangan/game_gedung.html", konteks)


def undangan_safari(request, slug=None):
    tamu = None
    if slug:
        tamu = get_object_or_404(Tamu, slug=slug)
        tamu.catat_kunjungan()

    konteks = _buat_konteks_undangan(tamu)
    return render(request, "undangan/game_safari.html", konteks)


@require_http_methods(["GET", "POST"])
def api_ucapan(request):
    undangan_slug = request.GET.get("undangan_slug") or request.GET.get("u")

    if request.method == "GET":
        qs = Ucapan.objects.filter(disetujui=True)
        if undangan_slug:
            qs = qs.filter(undangan__slug=undangan_slug)
        antrian = qs[:BATAS_UCAPAN_TAMPIL]
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
    undangan_req_slug = str(data.get("undangan_slug", "")).strip() or undangan_slug
    undangan_target = None

    if slug:
        tamu = Tamu.objects.filter(slug=slug).first()
        if tamu:
            undangan_target = tamu.undangan

    if not undangan_target and undangan_req_slug:
        undangan_target = Undangan.objects.filter(slug=undangan_req_slug).first()

    if not undangan_target:
        undangan_target = Undangan.objects.first()

    ucapan = Ucapan.objects.create(
        undangan=undangan_target,
        tamu=tamu,
        nama=nama,
        pesan=pesan,
        kehadiran=kehadiran,
        jumlah_orang=jumlah_orang,
    )
    return JsonResponse({"ok": True, "ucapan": _serialisasi(ucapan)}, status=201)


def custom_404(request, exception=None):
    """Tampilan kustom 404 berdesain game yang cantik saat halaman tidak ditemukan."""
    return render(request, "404.html", status=404)


def custom_500(request):
    """Tampilan kustom 500 saat terjadi kendala teknis internal pada server."""
    return render(request, "500.html", status=500)
