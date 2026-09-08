import re
import urllib.parse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .models import Acara, FotoGaleri, Pembayaran, Pengantin, Pengaturan, Rekening, Tamu, Ucapan, Undangan, konversi_url_gambar


def _ambil_undangan_user(user):
    """
    Mengambil atau membuat undangan utama milik user yang sedang aktif.
    Setiap user terdaftar otomatis memiliki minimal 1 proyek undangan.
    """
    undangan = Undangan.objects.filter(user=user).first()
    if not undangan:
        # Inisialisasi undangan perdana dengan nilai awal yang elegan
        dasar_slug = slugify(user.username) or f"undangan-{user.pk}"
        slug_calon = dasar_slug
        counter = 2
        while Undangan.objects.filter(slug=slug_calon).exists():
            slug_calon = f"{dasar_slug}-{counter}"
            counter += 1

        undangan = Undangan.objects.create(
            user=user,
            slug=slug_calon,
            judul=f"Pernikahan {user.first_name or user.username}",
            tema=Pengaturan.TEMA_KLASIK,
            hashtag=f"#{slugify(user.username).capitalize()}Wedding",
            quote="Dan di antara tanda-tanda (kebesaran)-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang.",
            sumber_quote="QS. Ar-Rum: 21",
        )

        # Buat placeholder Mempelai Pria dan Wanita
        Pengantin.objects.create(
            undangan=undangan,
            peran=Pengantin.PRIA,
            nama_lengkap=f"{user.first_name or 'Pengantin Pria'}",
            nama_panggilan="Mempelai Pria",
        )
        Pengantin.objects.create(
            undangan=undangan,
            peran=Pengantin.WANITA,
            nama_lengkap="Mempelai Wanita",
            nama_panggilan="Mempelai Wanita",
        )

        # Buat placeholder Acara Akad & Resepsi
        from django.utils import timezone
        import datetime
        besok = timezone.now() + datetime.timedelta(days=30)
        Acara.objects.create(
            undangan=undangan,
            nama="Akad Nikah",
            waktu_mulai=besok.replace(hour=8, minute=0, second=0),
            waktu_selesai=besok.replace(hour=10, minute=0, second=0),
            nama_tempat="Masjid Agung / Rumah Mempelai",
            alamat="Jl. Bahagia Selalu No. 1, Kota Impian",
            urutan=1,
        )
        Acara.objects.create(
            undangan=undangan,
            nama="Resepsi Pernikahan",
            waktu_mulai=besok.replace(hour=11, minute=0, second=0),
            waktu_selesai=besok.replace(hour=14, minute=0, second=0),
            nama_tempat="Gedung Pernikahan Asri",
            alamat="Jl. Bahagia Selalu No. 1, Kota Impian",
            urutan=2,
        )

    return undangan


# ==========================================
# 1. AUTENTIKASI PENGGUNA (REGISTER & LOGIN)
# ==========================================

def daftar_view(request):
    if request.user.is_authenticated:
        return redirect("undangan:dashboard")

    if request.method == "POST":
        nama = request.POST.get("nama", "").strip()
        username = request.POST.get("username", "").strip().lower()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not username or not password:
            messages.error(request, "Username dan password wajib diisi.")
            return render(request, "auth/register.html")

        if password != password_confirm:
            messages.error(request, "Konfirmasi kata sandi tidak cocok.")
            return render(request, "auth/register.html")

        if len(password) < 6:
            messages.error(request, "Kata sandi minimal terdiri dari 6 karakter.")
            return render(request, "auth/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username tersebut sudah digunakan. Silakan pilih username lain.")
            return render(request, "auth/register.html")

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nama,
            )
            # Inisialisasi undangan awal secara otomatis
            _ambil_undangan_user(user)

        login(request, user)
        messages.success(request, f"Selamat datang, {user.first_name or user.username}! Undangan Anda siap dikustomisasi.")
        return redirect("undangan:dashboard")

    return render(request, "auth/register.html")


def masuk_view(request):
    if request.user.is_authenticated:
        return redirect("undangan:dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is None and "@" in username:
            user_by_email = User.objects.filter(email__iexact=username).first()
            if user_by_email:
                user = authenticate(request, username=user_by_email.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang kembali, {user.first_name or user.username}!")
            next_url = request.GET.get("next") or request.POST.get("next") or "undangan:dashboard"
            return redirect(next_url)
        else:
            messages.error(request, "Username atau kata sandi tidak sesuai. Silakan periksa kembali.")

    return render(request, "auth/login.html")


def keluar_view(request):
    logout(request)
    messages.info(request, "Anda telah berhasil keluar dari sistem.")
    return redirect("undangan:landing")


# ==========================================
# 2. DASHBOARD UTAMA & STATISTIK
# ==========================================

@login_required
def dashboard_index(request):
    undangan = _ambil_undangan_user(request.user)

    total_tamu = undangan.tamu_list.count()
    tamu_buka = undangan.tamu_list.filter(jumlah_dibuka__gt=0).count()
    
    ucapan_semua = undangan.ucapan_list.all()
    total_ucapan = ucapan_semua.count()
    total_hadir = ucapan_semua.filter(kehadiran=Ucapan.HADIR).count()
    total_ragu = ucapan_semua.filter(kehadiran=Ucapan.RAGU).count()
    total_tidak = ucapan_semua.filter(kehadiran=Ucapan.TIDAK).count()

    total_orang_hadir = sum(u.jumlah_orang for u in ucapan_semua if u.kehadiran == Ucapan.HADIR)

    url_lengkap = undangan.get_url_publik(request)

    konteks = {
        "tab_aktif": "beranda",
        "undangan": undangan,
        "url_lengkap": url_lengkap,
        "total_tamu": total_tamu,
        "tamu_buka": tamu_buka,
        "total_ucapan": total_ucapan,
        "total_hadir": total_hadir,
        "total_ragu": total_ragu,
        "total_tidak": total_tidak,
        "total_orang_hadir": total_orang_hadir,
        "ucapan_terbaru": ucapan_semua.order_by("-dibuat")[:5],
        "galeri_count": undangan.galeri_list.count(),
    }
    return render(request, "dashboard/index.html", konteks)


# ==========================================
# 3. PENGATURAN UMUM & TEMA GAME
# ==========================================

@login_required
def dashboard_pengaturan(request):
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        judul = request.POST.get("judul", "").strip()
        slug_input = request.POST.get("slug", "").strip()
        tema = request.POST.get("tema", undangan.tema)
        hashtag = request.POST.get("hashtag", "").strip()
        quote = request.POST.get("quote", "").strip()
        sumber_quote = request.POST.get("sumber_quote", "").strip()
        musik_url = request.POST.get("musik_url", "").strip()
        catatan_penutup = request.POST.get("catatan_penutup", "").strip()

        # Validasi Kustomisasi Slug / Domain:
        # Sesuai aturan bisnis: domain kustom langsung (tanpa awalan /trial/) hanya bisa disesuaikan jika sudah berbayar aktif.
        RESERVED_SLUGS = {
            "admin", "superadmin", "dashboard", "masuk", "daftar", "keluar",
            "trial", "u", "game", "api", "media", "static", "undangan",
            "game-lombok", "game-tropis", "game-desa", "game-gedung", "game-safari",
        }

        if slug_input and slug_input.lower() != undangan.slug.lower():
            if undangan.status_langganan != Undangan.STATUS_AKTIF:
                messages.warning(
                    request,
                    "Kustomisasi nama tautan langsung (tanpa kata /trial/) hanya dapat diubah setelah melakukan aktivasi pembayaran. Selama masa uji coba gratis 1 bulan, nama tautan tetap menggunakan awalan /trial/."
                )
            else:
                # Sanitasi slug baru (mendukung huruf, angka, strip, dan simbol &)
                slug_raw = slug_input.replace(" ", "-").lower()
                slug_bersih = re.sub(r"[^a-zA-Z0-9_\-&]", "", slug_raw) or undangan.slug

                if slug_bersih in RESERVED_SLUGS:
                    messages.error(request, f"Nama tautan '{slug_bersih}' merupakan kata khusus sistem. Silakan gunakan nama lain.")
                    return redirect("undangan:dashboard_pengaturan")

                if Undangan.objects.filter(slug__iexact=slug_bersih).exclude(pk=undangan.pk).exists():
                    messages.error(request, f"Tautan '{slug_bersih}' sudah digunakan oleh pengguna lain. Pilih yang lain.")
                    return redirect("undangan:dashboard_pengaturan")

                undangan.slug = slug_bersih

        undangan.judul = judul or undangan.judul
        undangan.tema = tema
        undangan.hashtag = hashtag
        undangan.quote = quote
        undangan.sumber_quote = sumber_quote
        undangan.musik_url = musik_url
        undangan.catatan_penutup = catatan_penutup

        # Periksa file upload musik jika ada (hanya boleh untuk user berbayar)
        if "musik" in request.FILES:
            if undangan.status_langganan == Undangan.STATUS_AKTIF:
                undangan.musik = request.FILES["musik"]
            else:
                messages.warning(request, "Upload file musik hanya tersedia untuk pengguna berbayar. Gunakan opsi tautan URL musik online.")

        # Opsi hapus file musik lokal jika diminta
        if request.POST.get("hapus_musik") == "1":
            undangan.musik = None

        undangan.save()
        messages.success(request, "Pengaturan Jelajah Undangan berhasil diperbarui!")
        return redirect("undangan:dashboard_pengaturan")

    konteks = {
        "tab_aktif": "pengaturan",
        "undangan": undangan,
        "daftar_tema": Pengaturan.TEMA,
    }
    return render(request, "dashboard/pengaturan.html", konteks)


# ==========================================
# 4. DATA MEMPELAI (PRIA & WANITA)
# ==========================================

@login_required
def dashboard_mempelai(request):
    undangan = _ambil_undangan_user(request.user)
    pria = undangan.mempelai_list.filter(peran=Pengantin.PRIA).first()
    wanita = undangan.mempelai_list.filter(peran=Pengantin.WANITA).first()

    if request.method == "POST":
        # Simpan Mempelai Pria
        pria.nama_lengkap = request.POST.get("pria_nama_lengkap", "").strip()
        pria.nama_panggilan = request.POST.get("pria_nama_panggilan", "").strip()
        pria.anak_ke = request.POST.get("pria_anak_ke", "").strip()
        pria.nama_ayah = request.POST.get("pria_nama_ayah", "").strip()
        pria.nama_ibu = request.POST.get("pria_nama_ibu", "").strip()
        pria.instagram = request.POST.get("pria_instagram", "").replace("@", "").strip()
        pria.foto_url = request.POST.get("pria_foto_url", "").strip()
        if "pria_foto" in request.FILES:
            if undangan.status_langganan == Undangan.STATUS_AKTIF:
                pria.foto = request.FILES["pria_foto"]
            else:
                messages.warning(request, "Upload file foto hanya tersedia untuk pengguna berbayar. Gunakan opsi tempel link URL gambar.")
        pria.save()

        # Simpan Mempelai Wanita
        wanita.nama_lengkap = request.POST.get("wanita_nama_lengkap", "").strip()
        wanita.nama_panggilan = request.POST.get("wanita_nama_panggilan", "").strip()
        wanita.anak_ke = request.POST.get("wanita_anak_ke", "").strip()
        wanita.nama_ayah = request.POST.get("wanita_nama_ayah", "").strip()
        wanita.nama_ibu = request.POST.get("wanita_nama_ibu", "").strip()
        wanita.instagram = request.POST.get("wanita_instagram", "").replace("@", "").strip()
        wanita.foto_url = request.POST.get("wanita_foto_url", "").strip()
        if "wanita_foto" in request.FILES:
            if undangan.status_langganan == Undangan.STATUS_AKTIF:
                wanita.foto = request.FILES["wanita_foto"]
            else:
                messages.warning(request, "Upload file foto hanya tersedia untuk pengguna berbayar. Gunakan opsi tempel link URL gambar.")
        wanita.save()

        messages.success(request, "Data mempelai pria & wanita berhasil disimpan!")
        return redirect("undangan:dashboard_mempelai")

    konteks = {
        "tab_aktif": "mempelai",
        "undangan": undangan,
        "pria": pria,
        "wanita": wanita,
    }
    return render(request, "dashboard/mempelai.html", konteks)


# ==========================================
# 5. AGENDA ACARA (AKAD & RESEPSI)
# ==========================================

@login_required
def dashboard_acara(request):
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        nama = request.POST.get("nama", "").strip()
        waktu_mulai = request.POST.get("waktu_mulai", "").strip()
        waktu_selesai = request.POST.get("waktu_selesai", "").strip() or None
        nama_tempat = request.POST.get("nama_tempat", "").strip()
        alamat = request.POST.get("alamat", "").strip()
        url_maps = request.POST.get("url_maps", "").strip()
        urutan = int(request.POST.get("urutan", 0) or 0)

        if nama and waktu_mulai and nama_tempat:
            Acara.objects.create(
                undangan=undangan,
                nama=nama,
                waktu_mulai=waktu_mulai,
                waktu_selesai=waktu_selesai,
                nama_tempat=nama_tempat,
                alamat=alamat,
                url_maps=url_maps,
                urutan=urutan,
            )
            messages.success(request, f"Acara '{nama}' berhasil ditambahkan!")
        else:
            messages.error(request, "Nama acara, waktu mulai, dan tempat wajib diisi.")
        return redirect("undangan:dashboard_acara")

    acara_list = undangan.acara_list.all()
    konteks = {
        "tab_aktif": "acara",
        "undangan": undangan,
        "acara_list": acara_list,
    }
    return render(request, "dashboard/acara.html", konteks)


@login_required
def dashboard_acara_hapus(request, pk):
    undangan = _ambil_undangan_user(request.user)
    acara = get_object_or_404(Acara, pk=pk, undangan=undangan)
    if request.method == "POST":
        nama = acara.nama
        acara.delete()
        messages.success(request, f"Acara '{nama}' berhasil dihapus.")
    return redirect("undangan:dashboard_acara")


# ==========================================
# 6. GALERI FOTO (UPLOAD BERKAS / TEMPEL LINK)
# ==========================================

@login_required
def dashboard_galeri(request):
    """
    Fitur utama permintaan user:
    "Tinggal upload-upload aja oleh user itu gitu,
     foto-fotonya itu bisa pake link atau bisa juga upload di website jadi bebas disesuaikan."
    """
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        sumber = request.POST.get("sumber", "upload")  # "upload" atau "link"
        keterangan = request.POST.get("keterangan", "").strip()
        urutan = int(request.POST.get("urutan", 0) or 0)

        if sumber == "upload":
            if undangan.status_langganan != Undangan.STATUS_AKTIF:
                messages.warning(request, "Upload file foto ke server hanya tersedia untuk pengguna berbayar. Selama masa uji coba, silakan gunakan opsi tempel link URL gambar online.")
                return redirect("undangan:dashboard_galeri")
            berkas = request.FILES.get("gambar")
            if berkas:
                FotoGaleri.objects.create(
                    undangan=undangan,
                    gambar=berkas,
                    keterangan=keterangan,
                    urutan=urutan,
                )
                messages.success(request, "Foto berhasil diunggah ke galeri!")
            else:
                messages.error(request, "Silakan pilih berkas foto untuk diunggah.")

        elif sumber == "link":
            url_link = request.POST.get("gambar_url", "").strip()
            if url_link:
                FotoGaleri.objects.create(
                    undangan=undangan,
                    gambar_url=url_link,
                    keterangan=keterangan,
                    urutan=urutan,
                )
                messages.success(request, "Foto dari tautan online berhasil ditambahkan ke galeri!")
            else:
                messages.error(request, "Silakan masukkan URL tautan gambar.")

        return redirect("undangan:dashboard_galeri")

    galeri_list = undangan.galeri_list.all()
    konteks = {
        "tab_aktif": "galeri",
        "undangan": undangan,
        "galeri_list": galeri_list,
    }
    return render(request, "dashboard/galeri.html", konteks)


@login_required
def dashboard_galeri_hapus(request, pk):
    undangan = _ambil_undangan_user(request.user)
    foto = get_object_or_404(FotoGaleri, pk=pk, undangan=undangan)
    if request.method == "POST":
        foto.delete()
        messages.success(request, "Foto berhasil dihapus dari galeri.")
    return redirect("undangan:dashboard_galeri")


# ==========================================
# 7. REKENING & QRIS HADIAH
# ==========================================

@login_required
def dashboard_rekening(request):
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        nama_bank = request.POST.get("nama_bank", "").strip()
        nomor = request.POST.get("nomor", "").strip()
        atas_nama = request.POST.get("atas_nama", "").strip()
        qr_url = request.POST.get("qr_url", "").strip()
        urutan = int(request.POST.get("urutan", 0) or 0)

        if nama_bank and nomor and atas_nama:
            rek = Rekening(
                undangan=undangan,
                nama_bank=nama_bank,
                nomor=nomor,
                atas_nama=atas_nama,
                qr_url=qr_url,
                urutan=urutan,
            )
            if "qr" in request.FILES:
                if undangan.status_langganan == Undangan.STATUS_AKTIF:
                    rek.qr = request.FILES["qr"]
                else:
                    messages.warning(request, "Upload file QRIS hanya tersedia untuk pengguna berbayar. Gunakan opsi tempel link URL gambar.")
            rek.save()
            messages.success(request, f"Rekening / E-Wallet {nama_bank} berhasil ditambahkan!")
        else:
            messages.error(request, "Nama bank, nomor rekening, dan atas nama wajib diisi.")
        return redirect("undangan:dashboard_rekening")

    rekening_list = undangan.rekening_list.all()
    konteks = {
        "tab_aktif": "rekening",
        "undangan": undangan,
        "rekening_list": rekening_list,
    }
    return render(request, "dashboard/rekening.html", konteks)


@login_required
def dashboard_rekening_hapus(request, pk):
    undangan = _ambil_undangan_user(request.user)
    rek = get_object_or_404(Rekening, pk=pk, undangan=undangan)
    if request.method == "POST":
        rek.delete()
        messages.success(request, "Informasi rekening berhasil dihapus.")
    return redirect("undangan:dashboard_rekening")


# ==========================================
# 8. DAFTAR TAMU & BROADCAST WHATSAPP
# ==========================================

@login_required
def dashboard_tamu(request):
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        nama = request.POST.get("nama", "").strip()
        sapaan = request.POST.get("sapaan", "Bapak/Ibu/Saudara/i").strip()
        catatan = request.POST.get("catatan", "").strip()

        if nama:
            tamu = Tamu.objects.create(
                undangan=undangan,
                nama=nama,
                sapaan=sapaan,
                catatan=catatan,
            )
            messages.success(request, f"Tamu '{nama}' berhasil ditambahkan! Link personal siap disebar.")
        else:
            messages.error(request, "Nama tamu tidak boleh kosong.")
        return redirect("undangan:dashboard_tamu")

    daftar_tamu = undangan.tamu_list.all()

    # Siapkan URL dan teks pesan WhatsApp untuk tiap tamu
    tamu_items = []
    
    for t in daftar_tamu:
        link_tamu = undangan.get_tamu_url(t.slug, request)
        pesan_wa = (
            f"Kepada Yth. {t.sapaan_lengkap},\n\n"
            f"Tanpa mengurangi rasa hormat, perkenankan kami mengundang Anda untuk menghadiri acara {undangan.judul}.\n\n"
            f"Buka dan jelajahi undangan digital interaktif Anda pada tautan berikut:\n{link_tamu}\n\n"
            f"Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Anda berkenan hadir dan memberikan doa restu.\n\n"
            f"Terima kasih."
        )
        wa_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(pesan_wa)}"

        tamu_items.append({
            "obj": t,
            "link": link_tamu,
            "wa_url": wa_url,
        })

    konteks = {
        "tab_aktif": "tamu",
        "undangan": undangan,
        "tamu_items": tamu_items,
        "total_tamu": len(tamu_items),
    }
    return render(request, "dashboard/tamu.html", konteks)


@login_required
def dashboard_tamu_hapus(request, pk):
    undangan = _ambil_undangan_user(request.user)
    tamu = get_object_or_404(Tamu, pk=pk, undangan=undangan)
    if request.method == "POST":
        nama = tamu.nama
        tamu.delete()
        messages.success(request, f"Tamu '{nama}' telah dihapus.")
    return redirect("undangan:dashboard_tamu")


# ==========================================
# 9. BUKU UCAPAN & RSVP
# ==========================================

@login_required
def dashboard_ucapan(request):
    undangan = _ambil_undangan_user(request.user)

    filter_status = request.GET.get("status", "semua")
    qs = undangan.ucapan_list.all()

    if filter_status == "hadir":
        qs = qs.filter(kehadiran=Ucapan.HADIR)
    elif filter_status == "tidak":
        qs = qs.filter(kehadiran=Ucapan.TIDAK)
    elif filter_status == "ragu":
        qs = qs.filter(kehadiran=Ucapan.RAGU)

    konteks = {
        "tab_aktif": "ucapan",
        "undangan": undangan,
        "ucapan_list": qs.order_by("-dibuat"),
        "filter_status": filter_status,
        "total_ucapan": undangan.ucapan_list.count(),
        "total_hadir": undangan.ucapan_list.filter(kehadiran=Ucapan.HADIR).count(),
        "total_ragu": undangan.ucapan_list.filter(kehadiran=Ucapan.RAGU).count(),
        "total_tidak": undangan.ucapan_list.filter(kehadiran=Ucapan.TIDAK).count(),
    }
    return render(request, "dashboard/ucapan.html", konteks)


@login_required
def dashboard_ucapan_toggle(request, pk):
    undangan = _ambil_undangan_user(request.user)
    ucapan = get_object_or_404(Ucapan, pk=pk, undangan=undangan)
    if request.method == "POST":
        ucapan.disetujui = not ucapan.disetujui
        ucapan.save(update_fields=["disetujui"])
        status_teks = "ditampilkan" if ucapan.disetujui else "disembunyikan"
        messages.success(request, f"Ucapan dari {ucapan.nama} sekarang {status_teks} di game.")
    return redirect("undangan:dashboard_ucapan")


@login_required
def dashboard_ucapan_hapus(request, pk):
    undangan = _ambil_undangan_user(request.user)
    ucapan = get_object_or_404(Ucapan, pk=pk, undangan=undangan)
    if request.method == "POST":
        ucapan.delete()
        messages.success(request, "Ucapan berhasil dihapus.")
    return redirect("undangan:dashboard_ucapan")


# ==========================================
# 10. AKTIVASI & PEMBAYARAN (RP 30.000 / BULAN)
# ==========================================

@login_required
def dashboard_pembayaran(request):
    undangan = _ambil_undangan_user(request.user)

    if request.method == "POST":
        bukti = request.FILES.get("bukti_bayar")
        metode = request.POST.get("metode", "Transfer Bank / QRIS").strip()
        catatan = request.POST.get("catatan", "").strip()

        try:
            durasi_bulan = int(request.POST.get("durasi_bulan", 1))
        except (ValueError, TypeError):
            durasi_bulan = 1

        if durasi_bulan not in [1, 6, 12]:
            durasi_bulan = 1

        nominal_map = {1: 30000, 6: 150000, 12: 250000}
        nominal = nominal_map.get(durasi_bulan, 30000)

        if not bukti:
            messages.error(request, "Silakan unggah foto bukti transfer terlebih dahulu.")
            return redirect("undangan:dashboard_pembayaran")

        Pembayaran.objects.create(
            undangan=undangan,
            user=request.user,
            nominal=nominal,
            durasi_bulan=durasi_bulan,
            metode=metode,
            bukti_bayar=bukti,
            catatan=catatan,
            status=Pembayaran.STATUS_MENUNGGU,
        )

        undangan.status_langganan = Undangan.STATUS_MENUNGGU
        undangan.save(update_fields=["status_langganan"])

        label_durasi = {1: "1 Bulan", 6: "6 Bulan", 12: "1 Tahun"}.get(durasi_bulan, f"{durasi_bulan} Bulan")
        messages.success(
            request,
            f"Bukti pembayaran paket {label_durasi} (Rp {nominal:,}) berhasil dikirim! Admin akan segera memverifikasi dan "
            f"mengaktifkan undangan online Anda."
        )
        return redirect("undangan:dashboard_pembayaran")

    riwayat_pembayaran = undangan.riwayat_pembayaran.all().order_by("-dibuat")
    konteks = {
        "tab_aktif": "pembayaran",
        "undangan": undangan,
        "riwayat_pembayaran": riwayat_pembayaran,
        "paket_pilihan": Undangan.PAKET_PILIHAN,
    }
    return render(request, "dashboard/pembayaran.html", konteks)
