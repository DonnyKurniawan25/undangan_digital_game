from django.urls import path

from . import views

app_name = "undangan"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("game/", views.undangan, name="beranda"),
    path("game-lombok/", views.undangan_lombok, name="beranda_lombok"),
    path("game-tropis/", views.undangan_tropis, name="beranda_tropis"),
    path("game-desa/", views.undangan_desa, name="beranda_desa"),
    path("game-gedung/", views.undangan_gedung, name="beranda_gedung"),
    path("undangan/<slug:slug>/", views.undangan, name="tamu"),
    path("undangan-lombok/<slug:slug>/", views.undangan_lombok, name="tamu_lombok"),
    path("undangan-tropis/<slug:slug>/", views.undangan_tropis, name="tamu_tropis"),
    path("undangan-desa/<slug:slug>/", views.undangan_desa, name="tamu_desa"),
    path("undangan-gedung/<slug:slug>/", views.undangan_gedung, name="tamu_gedung"),
    path("api/ucapan/", views.api_ucapan, name="api_ucapan"),
]
