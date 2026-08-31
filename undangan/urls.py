from django.urls import path

from . import views

app_name = "undangan"

urlpatterns = [
    path("", views.undangan, name="beranda"),
    path("undangan/<slug:slug>/", views.undangan, name="tamu"),
    path("api/ucapan/", views.api_ucapan, name="api_ucapan"),
]
