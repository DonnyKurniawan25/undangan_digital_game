import datetime
from functools import wraps

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import (
    Acara,
    FotoGaleri,
    Pembayaran,
    Pengaturan,
    Rekening,
    Tamu,
    Ucapan,
    Undangan,
)


def superadmin_diperlukan(view_func):
    """
    Decorator khusus untuk memastikan hanya akun dengan status `is_superuser = True`
    yang dapat mengakses controller dashboard superadmin ini.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Silakan masuk terlebih dahulu dengan akun Superadmin.")
            return redirect(f"/masuk/?next={request.path}")
        if not request.user.is_superuser:
            return HttpResponseForbidden(
                "<h1>403 Terlarang</h1>"
                "<p>Halaman ini merupakan Pusat Kendali Superadmin dan hanya dapat diakses oleh Administrator Sistem.</p>"
                "<p><a href='/dashboard/'>&larr; Kembali ke Dashboard Pengguna</a></p>"
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


# ==========================================
# 1. PUSAT RINGKASAN & ANALITIK SUPERADMIN
# ==========================================

@superadmin_diperlukan
def superadmin_index(request):
    total_users = User.objects.count()
    user_biasa = User.objects.filter(is_superuser=False).count()
    total_undangan = Undangan.objects.count()
    total_tamu = Tamu.objects.count()
    total_ucapan = Ucapan.objects.count()
    total_foto = FotoGaleri.objects.count()

    # Statistik Keuangan & Langganan
    total_pembayaran = Pembayaran.objects.count()
    menunggu_verifikasi = Pembayaran.objects.filter(status=Pembayaran.STATUS_MENUNGGU).count()
    total_pendapatan = (
        Pembayaran.objects.filter(status=Pembayaran.STATUS_DISETUJUI).aggregate(total=Sum("nominal"))["total"]
        or 0
    )
    undangan_aktif_bayar = Undangan.objects.filter(
        status_langganan=Undangan.STATUS_AKTIF, aktif_berakhir__gt=timezone.now()
    ).count()

    # Distribusi Tema Game
    distribusi_tema = {}
    for kode, label in Pengaturan.TEMA:
        distribusi_tema[kode] = {
            "label": label,
            "jumlah": Undangan.objects.filter(tema=kode).count(),
        }

    # 5 User Terbaru
    users_terbaru = User.objects.all().order_by("-date_joined")[:5]

    # 5 Undangan Terbaru
    undangan_terbaru = Undangan.objects.select_related("user").all().order_by("-dibuat")[:5]

    # 5 Ucapan Masuk Terbaru
    ucapan_terbaru = Ucapan.objects.select_related("undangan", "tamu").all().order_by("-dibuat")[:5]

    # 5 Transaksi Terbaru
    transaksi_terbaru = Pembayaran.objects.select_related("undangan", "user").all().order_by("-dibuat")[:5]

    konteks = {
        "menu_aktif": "beranda",
        "total_users": total_users,
        "user_biasa": user_biasa,
        "total_undangan": total_undangan,
        "total_tamu": total_tamu,
        "total_ucapan": total_ucapan,
        "total_foto": total_foto,
        "total_pembayaran": total_pembayaran,
        "menunggu_verifikasi": menunggu_verifikasi,
        "total_pendapatan": total_pendapatan,
        "undangan_aktif_bayar": undangan_aktif_bayar,
        "distribusi_tema": distribusi_tema,
        "users_terbaru": users_terbaru,
        "undangan_terbaru": undangan_terbaru,
        "ucapan_terbaru": ucapan_terbaru,
        "transaksi_terbaru": transaksi_terbaru,
    }
    return render(request, "superadmin/index.html", konteks)


# ==========================================
# 2. MANAJEMEN PENGGUNA (USERS CONTROL)
# ==========================================

@superadmin_diperlukan
def superadmin_users(request):
    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "semua")

    qs = User.objects.annotate(jumlah_undangan=Count("daftar_undangan")).order_by("-date_joined")

    if q:
        qs = qs.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q)
        )

    if status_filter == "aktif":
        qs = qs.filter(is_active=True)
    elif status_filter == "nonaktif":
        qs = qs.filter(is_active=False)
    elif status_filter == "admin":
        qs = qs.filter(is_superuser=True)

    konteks = {
        "menu_aktif": "users",
        "daftar_user": qs,
        "q": q,
        "status_filter": status_filter,
        "total_hasil": qs.count(),
    }
    return render(request, "superadmin/users.html", konteks)


@superadmin_diperlukan
def superadmin_user_toggle(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    # Cegah admin memblokir akunnya sendiri
    if target_user.pk == request.user.pk:
        messages.error(request, "Anda tidak dapat menonaktifkan akun Anda sendiri!")
        return redirect("undangan:superadmin_users")

    if request.method == "POST":
        target_user.is_active = not target_user.is_active
        target_user.save(update_fields=["is_active"])
        status_teks = "diaktifkan kembali" if target_user.is_active else "dinonaktifkan (diblokir)"
        messages.success(request, f"Akun pengguna '{target_user.username}' berhasil {status_teks}.")

    return redirect("undangan:superadmin_users")


@superadmin_diperlukan
def superadmin_user_hapus(request, pk):
    target_user = get_object_or_404(User, pk=pk)

    if target_user.pk == request.user.pk:
        messages.error(request, "Anda tidak dapat menghapus akun Anda sendiri!")
        return redirect("undangan:superadmin_users")

    if request.method == "POST":
        username = target_user.username
        target_user.delete()
        messages.success(request, f"Akun pengguna '{username}' beserta seluruh data undangannya telah berhasil dihapus permanen.")

    return redirect("undangan:superadmin_users")


# ==========================================
# 3. MANAJEMEN SEMUA PROYEK UNDANGAN
# ==========================================

@superadmin_diperlukan
def superadmin_undangan(request):
    q = request.GET.get("q", "").strip()
    tema_filter = request.GET.get("tema", "")
    status_filter = request.GET.get("status", "semua")

    qs = Undangan.objects.select_related("user").annotate(
        jml_tamu=Count("tamu_list", distinct=True),
        jml_foto=Count("galeri_list", distinct=True),
        jml_ucapan=Count("ucapan_list", distinct=True),
    ).order_by("-dibuat")

    if q:
        qs = qs.filter(
            Q(judul__icontains=q) |
            Q(slug__icontains=q) |
            Q(user__username__icontains=q)
        )

    if tema_filter:
        qs = qs.filter(tema=tema_filter)

    semua_list = list(qs)
    # Hitung metrik status
    jml_aktif = sum(1 for u in semua_list if u.status_langganan == Undangan.STATUS_AKTIF and u.is_online_aktif)
    jml_trial = sum(1 for u in semua_list if u.status_langganan == Undangan.STATUS_TRIAL and u.is_online_aktif)
    jml_tenggang = sum(1 for u in semua_list if u.is_masa_tenggang)
    jml_siap_bersih = sum(1 for u in semua_list if u.is_siap_dibersihkan)

    # Filter berdasarkan tab status
    if status_filter == "aktif":
        daftar_tampil = [u for u in semua_list if u.status_langganan == Undangan.STATUS_AKTIF and u.is_online_aktif]
    elif status_filter == "trial":
        daftar_tampil = [u for u in semua_list if u.status_langganan == Undangan.STATUS_TRIAL and u.is_online_aktif]
    elif status_filter == "tenggang":
        daftar_tampil = [u for u in semua_list if u.is_masa_tenggang]
    elif status_filter == "siap_bersih":
        daftar_tampil = [u for u in semua_list if u.is_siap_dibersihkan]
    else:
        daftar_tampil = semua_list

    konteks = {
        "menu_aktif": "undangan",
        "daftar_undangan": daftar_tampil,
        "q": q,
        "tema_filter": tema_filter,
        "status_filter": status_filter,
        "daftar_tema": Pengaturan.TEMA,
        "total_undangan": len(semua_list),
        "jml_aktif": jml_aktif,
        "jml_trial": jml_trial,
        "jml_tenggang": jml_tenggang,
        "jml_siap_bersih": jml_siap_bersih,
    }
    return render(request, "superadmin/undangan.html", konteks)


@superadmin_diperlukan
def superadmin_undangan_bersihkan(request, pk):
    """
    Menghapus total undangan beserta seluruh file foto galeri, mempelai,
    QR rekening, musik, dan bukti bayar dari harddisk server.
    """
    undangan_obj = get_object_or_404(Undangan, pk=pk)

    if request.method == "POST":
        judul, slug, jml_berkas = undangan_obj.bersihkan_total()
        messages.success(
            request,
            f"Pembersihan tuntas! Undangan '{judul}' ({slug}) beserta {jml_berkas} file foto/media telah dihapus permanen dari server."
        )

    return redirect("undangan:superadmin_undangan")


@superadmin_diperlukan
def superadmin_bersihkan_server_massal(request):
    """
    Pembersihan massal otomatis untuk seluruh undangan yang telah kedaluwarsa
    lebih dari 1 bulan dan tidak diperpanjang.
    """
    if request.method == "POST":
        semua = Undangan.objects.all()
        siap = [u for u in semua if u.is_siap_dibersihkan]
        total_berkas = 0
        total_undangan = len(siap)

        for u in siap:
            _, _, jml = u.bersihkan_total()
            total_berkas += jml

        if total_undangan > 0:
            messages.success(
                request,
                f"Pembersihan massal berhasil! Sebanyak {total_undangan} undangan kedaluwarsa > 1 bulan dan {total_berkas} berkas media telah dibersihkan dari server."
            )
        else:
            messages.info(request, "Tidak ada undangan yang kedaluwarsa > 1 bulan. Server Anda dalam kondisi bersih!")

    return redirect("undangan:superadmin_undangan")


@superadmin_diperlukan
def superadmin_undangan_hapus(request, pk):
    undangan_obj = get_object_or_404(Undangan, pk=pk)

    if request.method == "POST":
        judul, slug, jml_berkas = undangan_obj.bersihkan_total()
        messages.success(request, f"Undangan '{judul}' ({slug}) beserta {jml_berkas} file medianya telah berhasil dihapus dari sistem.")

    return redirect("undangan:superadmin_undangan")


@superadmin_diperlukan
def superadmin_undangan_aktifkan_manual(request, pk):
    """
    Fitur bagi Superadmin untuk memperpanjang / mengaktifkan masa aktif undangan
    selama 30 hari secara manual tanpa proses pembayaran formal.
    """
    undangan_obj = get_object_or_404(Undangan, pk=pk)

    if request.method == "POST":
        undangan_obj.aktifkan_satu_bulan()
        messages.success(
            request,
            f"Masa aktif undangan '{undangan_obj.judul}' ({undangan_obj.slug}) berhasil diaktifkan / ditambah 30 hari (1 bulan)!"
        )

    # Redirect kembali ke halaman asal (bisa dari superadmin_undangan atau transaksi)
    return redirect(request.META.get("HTTP_REFERER", "undangan:superadmin_undangan"))


@superadmin_diperlukan
def superadmin_undangan_tambah_durasi(request, pk):
    """
    Fitur fleksibel bagi Superadmin untuk menambah durasi undangan:
    - Opsi cepat: +1 Hari, +7 Hari, +30 Hari, +90 Hari, +365 Hari.
    - Opsi kustom: Input jumlah hari bebas oleh admin.
    - Opsi set tanggal: Menentukan tanggal kedaluwarsa secara spesifik.
    """
    undangan_obj = get_object_or_404(Undangan, pk=pk)

    if request.method == "POST":
        mode = request.POST.get("mode", "hari")

        if mode == "tanggal":
            tanggal_str = request.POST.get("tanggal_berakhir", "").strip()
            try:
                from django.utils.dateparse import parse_datetime, parse_date
                dt = parse_datetime(tanggal_str)
                if not dt:
                    d = parse_date(tanggal_str)
                    if d:
                        dt = timezone.make_aware(datetime.datetime.combine(d, datetime.time(23, 59, 59)))
                if dt:
                    undangan_obj.aktif_berakhir = dt
                    undangan_obj.status_langganan = Undangan.STATUS_AKTIF
                    undangan_obj.save(update_fields=["aktif_berakhir", "status_langganan"])
                    messages.success(
                        request,
                        f"Masa aktif undangan '{undangan_obj.judul}' berhasil diatur hingga {dt.strftime('%d %b %Y, %H:%M')} WIB."
                    )
                else:
                    messages.error(request, "Format tanggal tidak dikenali.")
            except Exception as e:
                messages.error(request, f"Gagal mengatur tanggal: {e}")

        else:
            try:
                jumlah_hari = int(request.POST.get("jumlah_hari", 30))
                if jumlah_hari <= 0:
                    jumlah_hari = 1
                undangan_obj.tambah_durasi(jumlah_hari)
                messages.success(
                    request,
                    f"Masa aktif undangan '{undangan_obj.judul}' berhasil diperpanjang +{jumlah_hari} hari! (Total sisa: {undangan_obj.sisa_hari_aktif} hari)"
                )
            except ValueError:
                messages.error(request, "Jumlah hari harus berupa angka bulat.")

    return redirect(request.META.get("HTTP_REFERER", "undangan:superadmin_undangan"))


# ==========================================
# 4. MODERASI UCAPAN & RSVP GLOBAL
# ==========================================

@superadmin_diperlukan
def superadmin_ucapan(request):
    q = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "semua")
    undangan_filter = request.GET.get("undangan_id", "")

    qs = Ucapan.objects.select_related("undangan", "tamu").order_by("-dibuat")

    if q:
        qs = qs.filter(
            Q(nama__icontains=q) |
            Q(pesan__icontains=q)
        )

    if status_filter == "hadir":
        qs = qs.filter(kehadiran=Ucapan.HADIR)
    elif status_filter == "tidak":
        qs = qs.filter(kehadiran=Ucapan.TIDAK)
    elif status_filter == "ragu":
        qs = qs.filter(kehadiran=Ucapan.RAGU)
    elif status_filter == "sembunyi":
        qs = qs.filter(disetujui=False)

    if undangan_filter:
        qs = qs.filter(undangan_id=undangan_filter)

    konteks = {
        "menu_aktif": "ucapan",
        "daftar_ucapan": qs,
        "q": q,
        "status_filter": status_filter,
        "undangan_filter": undangan_filter,
        "semua_undangan": Undangan.objects.all().order_by("judul"),
        "total_ucapan": qs.count(),
    }
    return render(request, "superadmin/ucapan.html", konteks)


@superadmin_diperlukan
def superadmin_ucapan_toggle(request, pk):
    ucapan = get_object_or_404(Ucapan, pk=pk)
    if request.method == "POST":
        ucapan.disetujui = not ucapan.disetujui
        ucapan.save(update_fields=["disetujui"])
        status_teks = "ditampilkan" if ucapan.disetujui else "disembunyikan"
        messages.success(request, f"Pesan dari '{ucapan.nama}' sekarang {status_teks} pada game.")
    return redirect("undangan:superadmin_ucapan")


@superadmin_diperlukan
def superadmin_ucapan_hapus(request, pk):
    ucapan = get_object_or_404(Ucapan, pk=pk)
    if request.method == "POST":
        nama = ucapan.nama
        ucapan.delete()
        messages.success(request, f"Ucapan dari '{nama}' telah dihapus.")
    return redirect("undangan:superadmin_ucapan")


# ==========================================
# 5. PENGATURAN GLOBAL PLATFORM
# ==========================================

@superadmin_diperlukan
def superadmin_pengaturan(request):
    pengaturan = Pengaturan.ambil()

    if request.method == "POST":
        pengaturan.judul = request.POST.get("judul", "").strip() or pengaturan.judul
        pengaturan.tema = request.POST.get("tema", pengaturan.tema)
        pengaturan.hashtag = request.POST.get("hashtag", "").strip()
        pengaturan.quote = request.POST.get("quote", "").strip()
        pengaturan.sumber_quote = request.POST.get("sumber_quote", "").strip()
        pengaturan.catatan_penutup = request.POST.get("catatan_penutup", "").strip()

        if "musik" in request.FILES:
            pengaturan.musik = request.FILES["musik"]

        if request.POST.get("hapus_musik") == "1":
            pengaturan.musik = None

        pengaturan.save()
        messages.success(request, "Pengaturan global bawaan platform berhasil diperbarui!")
        return redirect("undangan:superadmin_pengaturan")

    konteks = {
        "menu_aktif": "pengaturan",
        "pengaturan": pengaturan,
        "daftar_tema": Pengaturan.TEMA,
    }
    return render(request, "superadmin/pengaturan.html", konteks)


# ==========================================
# 6. MANAJEMEN TRANSAKSI & PEMBAYARAN
# ==========================================

@superadmin_diperlukan
def superadmin_transaksi(request):
    status_filter = request.GET.get("status", "semua")
    q = request.GET.get("q", "").strip()

    qs = Pembayaran.objects.select_related("undangan", "user").order_by("-dibuat")

    if status_filter != "semua":
        qs = qs.filter(status=status_filter)

    if q:
        qs = qs.filter(
            Q(user__username__icontains=q)
            | Q(undangan__judul__icontains=q)
            | Q(undangan__slug__icontains=q)
            | Q(catatan__icontains=q)
        )

    # Hitung ringkasan status
    jml_menunggu = Pembayaran.objects.filter(status=Pembayaran.STATUS_MENUNGGU).count()
    jml_disetujui = Pembayaran.objects.filter(status=Pembayaran.STATUS_DISETUJUI).count()
    jml_ditolak = Pembayaran.objects.filter(status=Pembayaran.STATUS_DITOLAK).count()
    total_pendapatan = (
        Pembayaran.objects.filter(status=Pembayaran.STATUS_DISETUJUI).aggregate(total=Sum("nominal"))["total"]
        or 0
    )

    konteks = {
        "menu_aktif": "transaksi",
        "daftar_transaksi": qs,
        "status_filter": status_filter,
        "q": q,
        "jml_menunggu": jml_menunggu,
        "jml_disetujui": jml_disetujui,
        "jml_ditolak": jml_ditolak,
        "total_pendapatan": total_pendapatan,
    }
    return render(request, "superadmin/transaksi.html", konteks)


@superadmin_diperlukan
def superadmin_transaksi_aksi(request, pk):
    pembayaran = get_object_or_404(Pembayaran.objects.select_related("undangan"), pk=pk)

    if request.method == "POST":
        aksi = request.POST.get("aksi")
        if aksi == "setujui":
            pembayaran.status = Pembayaran.STATUS_DISETUJUI
            pembayaran.diverifikasi_pada = timezone.now()
            pembayaran.save(update_fields=["status", "diverifikasi_pada"])

            # Aktifkan undangan sesuai paket durasi yang dibeli (1, 6, atau 12 bulan)
            pembayaran.undangan.tambah_durasi_bulan(pembayaran.durasi_bulan)

            messages.success(
                request,
                f"Pembayaran #{pembayaran.pk} disetujui! Undangan '{pembayaran.undangan.judul}' kini aktif paket {pembayaran.label_durasi}."
            )
        elif aksi == "tolak":
            alasan = request.POST.get("alasan", "").strip()
            pembayaran.status = Pembayaran.STATUS_DITOLAK
            pembayaran.diverifikasi_pada = timezone.now()
            if alasan:
                catatan_baru = f"{pembayaran.catatan}\n[Ditolak Admin]: {alasan}".strip()
                pembayaran.catatan = catatan_baru
                pembayaran.save(update_fields=["status", "diverifikasi_pada", "catatan"])
            else:
                pembayaran.save(update_fields=["status", "diverifikasi_pada"])

            messages.warning(
                request,
                f"Pembayaran #{pembayaran.pk} telah ditolak."
            )

    return redirect("undangan:superadmin_transaksi")

