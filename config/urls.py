from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("favicon.ico", RedirectView.as_view(url="/static/img/favicon.ico", permanent=True)),
    path("admin/", admin.site.urls),
    path("", include("undangan.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "undangan.views.custom_404"
handler500 = "undangan.views.custom_500"
