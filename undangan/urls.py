from django.urls import path

from . import views, views_dashboard, views_superadmin

app_name = "undangan"

urlpatterns = [
    # Landing & Autentikasi Pengguna
    path("", views.landing, name="landing"),
    path("masuk/", views_dashboard.masuk_view, name="login"),
    path("daftar/", views_dashboard.daftar_view, name="register"),
    path("keluar/", views_dashboard.keluar_view, name="logout"),

    # Dashboard Pengguna
    path("dashboard/", views_dashboard.dashboard_index, name="dashboard"),
    path("dashboard/pengaturan/", views_dashboard.dashboard_pengaturan, name="dashboard_pengaturan"),
    path("dashboard/mempelai/", views_dashboard.dashboard_mempelai, name="dashboard_mempelai"),
    path("dashboard/acara/", views_dashboard.dashboard_acara, name="dashboard_acara"),
    path("dashboard/acara/<int:pk>/hapus/", views_dashboard.dashboard_acara_hapus, name="dashboard_acara_hapus"),
    path("dashboard/galeri/", views_dashboard.dashboard_galeri, name="dashboard_galeri"),
    path("dashboard/galeri/<int:pk>/hapus/", views_dashboard.dashboard_galeri_hapus, name="dashboard_galeri_hapus"),
    path("dashboard/rekening/", views_dashboard.dashboard_rekening, name="dashboard_rekening"),
    path("dashboard/rekening/<int:pk>/hapus/", views_dashboard.dashboard_rekening_hapus, name="dashboard_rekening_hapus"),
    path("dashboard/tamu/", views_dashboard.dashboard_tamu, name="dashboard_tamu"),
    path("dashboard/tamu/<int:pk>/hapus/", views_dashboard.dashboard_tamu_hapus, name="dashboard_tamu_hapus"),
    path("dashboard/ucapan/", views_dashboard.dashboard_ucapan, name="dashboard_ucapan"),
    path("dashboard/ucapan/<int:pk>/toggle/", views_dashboard.dashboard_ucapan_toggle, name="dashboard_ucapan_toggle"),
    path("dashboard/ucapan/<int:pk>/hapus/", views_dashboard.dashboard_ucapan_hapus, name="dashboard_ucapan_hapus"),
    path("dashboard/pembayaran/", views_dashboard.dashboard_pembayaran, name="dashboard_pembayaran"),

    # Pusat Kendali & Dashboard Superadmin
    path("superadmin/", views_superadmin.superadmin_index, name="superadmin_index"),
    path("superadmin/users/", views_superadmin.superadmin_users, name="superadmin_users"),
    path("superadmin/users/<int:pk>/toggle/", views_superadmin.superadmin_user_toggle, name="superadmin_user_toggle"),
    path("superadmin/users/<int:pk>/hapus/", views_superadmin.superadmin_user_hapus, name="superadmin_user_hapus"),
    path("superadmin/undangan/", views_superadmin.superadmin_undangan, name="superadmin_undangan"),
    path("superadmin/undangan/bersihkan-massal/", views_superadmin.superadmin_bersihkan_server_massal, name="superadmin_bersihkan_server_massal"),
    path("superadmin/undangan/<int:pk>/hapus/", views_superadmin.superadmin_undangan_hapus, name="superadmin_undangan_hapus"),
    path("superadmin/undangan/<int:pk>/bersihkan/", views_superadmin.superadmin_undangan_bersihkan, name="superadmin_undangan_bersihkan"),
    path("superadmin/undangan/<int:pk>/aktifkan/", views_superadmin.superadmin_undangan_aktifkan_manual, name="superadmin_undangan_aktifkan_manual"),
    path("superadmin/undangan/<int:pk>/durasi/", views_superadmin.superadmin_undangan_tambah_durasi, name="superadmin_undangan_tambah_durasi"),
    path("superadmin/transaksi/", views_superadmin.superadmin_transaksi, name="superadmin_transaksi"),
    path("superadmin/transaksi/<int:pk>/aksi/", views_superadmin.superadmin_transaksi_aksi, name="superadmin_transaksi_aksi"),
    path("superadmin/ucapan/", views_superadmin.superadmin_ucapan, name="superadmin_ucapan"),
    path("superadmin/ucapan/<int:pk>/toggle/", views_superadmin.superadmin_ucapan_toggle, name="superadmin_ucapan_toggle"),
    path("superadmin/ucapan/<int:pk>/hapus/", views_superadmin.superadmin_ucapan_hapus, name="superadmin_ucapan_hapus"),
    path("superadmin/pengaturan/", views_superadmin.superadmin_pengaturan, name="superadmin_pengaturan"),

    # Rute Khusus Masa Uji Coba (Trial 1 Hari): /trial/<slug>/ (misal: jelajah.biz.id/trial/rana&cahyo)
    path("trial/<str:slug_undangan>/", views.undangan_publik_trial, name="undangan_publik_trial"),
    path("trial/<str:slug_undangan>/<str:slug_tamu>/", views.undangan_publik_trial, name="undangan_publik_trial_tamu"),

    # Rute Kompatibilitas Warisan /u/<slug>/
    path("u/<str:slug_undangan>/", views.u_undangan, name="u_undangan"),
    path("u/<str:slug_undangan>/<str:slug_tamu>/", views.u_undangan, name="u_undangan_tamu"),

    # Rute Bawaan & Kompatibilitas Demo
    path("game/", views.undangan, name="beranda"),
    path("game-lombok/", views.undangan_lombok, name="beranda_lombok"),
    path("game-tropis/", views.undangan_tropis, name="beranda_tropis"),
    path("game-desa/", views.undangan_desa, name="beranda_desa"),
    path("game-gedung/", views.undangan_gedung, name="beranda_gedung"),
    path("game-safari/", views.undangan_safari, name="beranda_safari"),
    path("undangan/<slug:slug>/", views.undangan, name="tamu"),
    path("undangan-lombok/<slug:slug>/", views.undangan_lombok, name="tamu_lombok"),
    path("undangan-tropis/<slug:slug>/", views.undangan_tropis, name="tamu_tropis"),
    path("undangan-desa/<slug:slug>/", views.undangan_desa, name="tamu_desa"),
    path("undangan-gedung/<slug:slug>/", views.undangan_gedung, name="tamu_gedung"),
    path("undangan-safari/<slug:slug>/", views.undangan_safari, name="tamu_safari"),

    # API Endpoint
    path("api/ucapan/", views.api_ucapan, name="api_ucapan"),

    # Pratinjau Halaman Error Kustom
    path("404/", views.custom_404, name="error_404"),
    path("500/", views.custom_500, name="error_500"),

    # Rute Langsung Kustom (Berbayar Penuh): /<slug>/ (misal: jelajah.biz.id/rana&cahyo)
    # Diletakkan paling akhir agar rute sistem lainnya di atas dievaluasi terlebih dahulu
    path("<str:slug_undangan>/", views.undangan_publik_root, name="undangan_publik_root"),
    path("<str:slug_undangan>/<str:slug_tamu>/", views.undangan_publik_root, name="undangan_publik_root_tamu"),
]
