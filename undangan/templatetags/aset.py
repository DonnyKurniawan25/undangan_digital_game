"""Tag `{% aset %}`: seperti {% static %} tetapi menambahkan penanda versi.

Tanpa ini peramban gemar menyimpan game.css / game.js / gambar tile di cache,
sehingga perubahan aset tidak terlihat sampai pengguna melakukan hard reload.
Penandanya adalah waktu ubah berkas, jadi URL hanya berubah saat isinya berubah.

Saat DEBUG hasilnya tidak disimpan supaya aset yang baru dibuat ulang langsung
terpakai tanpa perlu menyalakan ulang server.
"""

import os

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static

register = template.Library()

_singgahan = {}


def _cari_berkas(path):
    berkas = finders.find(path)
    if berkas:
        return berkas
    try:
        return staticfiles_storage.path(path)
    except (NotImplementedError, ValueError):
        return None


@register.simple_tag
def aset(path):
    url = static(path)
    if not settings.DEBUG and path in _singgahan:
        return f"{url}?v={_singgahan[path]}"
    try:
        versi = int(os.path.getmtime(_cari_berkas(path)))
    except (OSError, TypeError):
        return url
    _singgahan[path] = versi
    return f"{url}?v={versi}"
