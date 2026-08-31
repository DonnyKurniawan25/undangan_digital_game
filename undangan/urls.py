from django.urls import path

from . import views

app_name = "undangan"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("game/", views.undangan, name="beranda"),
    path("game-lombok/", views.undangan_lombok, name="beranda_lombok"),
    path("undangan/<slug:slug>/", views.undangan, name="tamu"),
    path("undangan-lombok/<slug:slug>/", views.undangan_lombok, name="tamu_lombok"),
    path("api/ucapan/", views.api_ucapan, name="api_ucapan"),
]
