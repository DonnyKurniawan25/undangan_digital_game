# Undangan Pernikahan Interaktif

Undangan digital berbentuk game bernuansa pernikahan adat Indonesia. Tamu
memilih karakter, berjalan mengelilingi taman, lalu mendekati objek untuk
membuka isi undangan.

## Dua template

Keduanya memakai data yang sama (mempelai, acara, galeri, tamu, ucapan,
rekening) — yang berbeda hanya tampilannya.

| Tema | Tampilan | Kendali |
|---|---|---|
| **Taman Pixel** (`klasik`) | Tampak atas, taman pernikahan Jawa dengan pelaminan gebyok | Analog geser |
| **Taman Tropis** (`tropis`) | Tampak atas gaya Stardew Valley, taman tropis rimbun dengan kolam, gapura janur, dan umbul-umbul | Analog geser |

Tema dipilih di **admin → Pengaturan → Tema**. Untuk mencoba tanpa mengubah
pengaturan, tambahkan parameter pada URL:

```bash
http://127.0.0.1:8000/undangan/andi-pratama/?tema=tropis
```

Berkas tiap tema terpisah penuh, jadi mengubah satu tema tidak memengaruhi yang
lain:

| | Taman Pixel | Taman Tropis |
|---|---|---|
| Template | `templates/undangan/game.html` | `templates/undangan/game_tropis.html` |
| Mesin | `static/js/game.js` | `static/js/game_tropis.js` |
| Gaya | `static/css/game.css` | `game.css` + `static/css/game_tropis.css` |
| Aset | `static/game/` | `static/game_tropis/` |
| Generator aset | `tools/buat_aset.py` | `tools/buat_aset_tropis.py` |

### Tentang tema Taman Tropis

Kendalinya analog geser: sentuh di mana saja pada sisi kiri layar, alasnya
mengikuti titik sentuh. Vektor analog dipakai dalam ruang layar lalu diubah
ke sumbu petak oleh mesin, dan **besaran dorongan menentukan kecepatan** —
dorong sedikit untuk berjalan pelan, dorong penuh untuk berlari. Papan ketik
dan fitur "Pergi" selalu memakai kecepatan penuh.

Kamera lurus dari atas dengan petak persegi 48x48: `sx = tx x 48`, `sy = ty x 48`.
Objek diurutkan menurut sumbu y saja, sehingga yang lebih ke bawah layar
menutupi yang di belakangnya. Pohon dan bangunan tinggi otomatis menjadi
tembus pandang saat menutupi karakter, jadi pemain tidak pernah hilang di
balik kanopi. Di luar batas peta digambar petak rimba gelap agar layar selalu
terisi penuh.

Isinya: pelaminan ukir dengan sepasang mempelai duduk di singgasana, gapura
janur kuning, umbul-umbul empat warna di sepanjang jalan batu, kolam berair
mancur dengan jembatan dan teratai, meja buku tamu berkanopi, serta rimba
kelapa dan pisang di sekeliling taman.

| Objek di peta | Isi popup |
|---|---|
| Pelaminan gebyok | Foto & biodata mempelai pria dan wanita |
| Papan lukis | Galeri foto prewedding |
| Papan kayu | Rangkaian acara, hitung mundur, tautan Google Maps |
| Meja buku tamu | Form ucapan + konfirmasi kehadiran (RSVP) |
| Kotak angpao | Nomor rekening / QRIS |

## Nuansa adat

Seluruh aset digambar mengikuti pernikahan adat Indonesia:

- **Pelaminan** berupa gebyok jati berukir dengan mahkota gunungan, ceruk
  melengkung berhias roncean melati, dan janur kuning di kedua sudut atas.
- **Sepasang mempelai** berdiri di dalam ceruk: pria berblangkon, beskap gading,
  kain jarik batik, dan keris di pinggang; wanita berkebaya dengan sanggul,
  cunduk mentul, paes di dahi, roncean melati, dan kain songket.
- **Kembar mayang** mengapit pelaminan, **umbul-umbul** berjajar di sepanjang
  karpet, dan pintu masuk berupa **gapura janur kuning** dari bambu.
- **Meja tumpeng** (nasi kuning di atas daun pisang) menggantikan kue pengantin,
  dan kotak hadiah berbentuk **kotak angpao kayu bermotif batik kawung**.
- **Tanaman tropis**: pohon kelapa, kamboja, dan bugenvil dalam pot.
- **Tamu** pun berbusana Indonesia — kemeja batik untuk pria, kebaya dengan kain
  batik untuk wanita.

## Menemukan lokasi

Supaya tamu tidak tersesat, ada empat lapis bantuan arah:

- **Papan nama** melayang di atas setiap tempat, lengkap dengan tanda centang
  bila sudah dikunjungi. Papan nama ditahan di dalam layar sehingga tetap
  terbaca walau objeknya tinggi.
- **Minimap** di pojok kanan atas menunjukkan posisi karakter dan kelima titik,
  beserta penghitung kemajuan (mis. `3/5`).
- **Panah tepi layar** menunjuk ke tempat yang belum dikunjungi dan berada di
  luar pandangan. Warnanya sama dengan penanda di peta.
- **Peta penuh** (tombol peta di kanan atas, tombol <kbd>M</kbd>, atau ketuk
  minimap) memuat denah bernomor dan daftar lokasi. Menekan sebuah tempat
  membuat karakter **berjalan sendiri** ke sana lewat jalur terpendek, lalu
  popupnya terbuka begitu tiba. Menggerakkan analog membatalkan jalan otomatis.

## Menjalankan

```bash
venv/Scripts/python.exe manage.py runserver
```

Buka `http://127.0.0.1:8000/`. Untuk undangan yang menyebut nama tamu, pakai
`http://127.0.0.1:8000/undangan/<slug-tamu>/`.

Perintah lain:

```bash
venv/Scripts/python.exe manage.py isi_contoh
```

Mengisi database dengan data contoh (mempelai, acara, galeri, rekening, tamu,
ucapan) dan membuat akun admin bila belum ada. Tambahkan `--bersih` untuk
menghapus data lama lebih dulu.

## Mengelola isi undangan

Semua isi diatur lewat `http://127.0.0.1:8000/admin/`:

- **Pengaturan** — judul, hashtag, kutipan pembuka, file musik latar, catatan penutup.
- **Mempelai** — dua baris: mempelai pria dan wanita, lengkap dengan foto.
- **Acara** — akad, resepsi, dan seterusnya. Acara pertama dipakai untuk hitung mundur.
- **Foto Galeri** — foto prewedding beserta urutannya.
- **Rekening Hadiah** — nama bank, nomor, atas nama, dan QRIS opsional.
- **Daftar Tamu** — setiap tamu punya tautan pribadi `/undangan/<slug>/`. Kolom
  "Link undangan" di daftar tamu bisa langsung disalin dan dikirim.
- **Ucapan & RSVP** — ucapan yang masuk. Hilangkan centang *disetujui* untuk
  menyembunyikan sebuah ucapan dari papan ucapan.

## Aset gambar

Seluruh pixel art dibuat dari kode, tanpa mengunduh aset pihak ketiga, sehingga
bebas dipakai. Untuk mengubah warna, bentuk, atau menambah properti baru, sunting
`tools/buat_aset.py` lalu jalankan:

```bash
venv/Scripts/python.exe tools/buat_aset.py
```

Hasilnya menimpa berkas di `static/game/`. Jika ingin memakai aset gambar sendiri,
cukup timpa berkas PNG di folder tersebut dengan ukuran yang sama.

Dua berkas punya aturan khusus karena urutannya dibaca oleh kode:

- `tileset.png` — deretan tile lantai. Urutannya harus sama dengan `INDEKS_TILE`
  di `static/js/game.js`.
- `tepi.png` — potongan tepi rumput yang digambar di atas tile lantai supaya
  batas rumput dengan jalan/marmer/kayu tidak berupa kotak kaku. Urutannya harus
  sama dengan `TEPI` di `static/js/game.js`.

Template memakai tag `{% aset %}` (bukan `{% static %}`) untuk berkas yang sering
berubah. Tag itu menambahkan penanda versi dari waktu ubah berkas, sehingga
perubahan aset langsung terlihat tanpa perlu hard reload di peramban.

## Mengubah denah taman

Peta ada di `static/js/game.js`:

- `PETA` — denah petak, satu huruf per petak (`#` pagar tanaman, `~` kolam,
  `f` bedeng bunga, `.` rumput, `,` rumput berbunga, `-` jalan, `[` `]` karpet,
  `w` kayu, `m` marmer, `t` tanah). Tiga huruf pertama tidak bisa dilewati.
- `OBJEK` — daftar properti beserta posisi (satuan petak), kotak tabrakan
  `padat`, dan `zona` bila objek itu bisa dibuka.
- `ZONA` — judul, teks tombol, dan radius jangkauan tiap titik interaksi.

Menambah titik baru berarti empat langkah:

1. Tambah entri di `OBJEK` dengan `zona: "namabaru"`.
2. Tambah entri di `ZONA` berisi `judul`, `aksi`, `radius`, `warna`, `ket`, dan
   `berdiri` (petak tempat karakter berhenti saat menuju lokasi itu — pastikan
   petaknya bisa dipijak dan berada di dalam `radius`).
3. Masukkan kuncinya ke `URUTAN_ZONA` supaya muncul di peta dan daftar lokasi.
4. Buat `<section class="popup" id="popup-namabaru">` di
   `templates/undangan/game.html`.

## Tileset Sasak Lombok

Aset terpisah di `static/tileset_sasak/`, belum terpasang ke tema mana pun —
siap dipakai untuk peta baru bertema kampung tradisional Sasak.

```bash
venv/Scripts/python.exe tools/buat_tileset_sasak.py
```

Petak **32x32**, digambar langsung pada resolusi akhir (tidak diperbesar)
dengan tangga warna 4-5 tingkat per bahan.

| Berkas | Isi |
|---|---|
| `tileset_sasak.png` | Lembar 8 kolom x 3 baris, 24 petak |
| `tepi_rumput.png` | 12 potongan transisi rumput |
| `tepi_tanah.png` | 12 potongan transisi tanah |
| `tepi_air.png` | 12 potongan garis pantai / pematang |
| `petak/<nama>.png` | Tiap petak sebagai berkas terpisah |

**Isi lembar** (indeks 0-23, dibaca kiri ke kanan):
rumput 1-3, rumput berbunga, rumput kering 1-2, sawah muda, sawah tua,
tanah 1-3, tanah retak, pasir 1-2, lantai bale, anyaman bambu,
batu jalan 1-3, batu susun, air 1-3 (tiga fase riak), air dangkal.

**Urutan 12 potongan tepi** (sama untuk ketiga strip): atas, bawah, kiri,
kanan, lalu empat sudut luar (kiri-atas, kanan-atas, kiri-bawah,
kanan-bawah), lalu empat sudut dalam dengan urutan yang sama. Potongan ini
beralfa dan ditumpuk **di atas** petak tujuan, jadi satu set bisa dipakai
untuk transisi ke bahan apa pun.

**Tentang sifat tileable.** Setiap petak digambar sembilan kali pada kanvas
besar lalu bagian tengahnya dipotong, sehingga bentuk yang melewati satu tepi
otomatis muncul lagi di tepi seberang. Semua pola beraturan memakai periode
yang membagi habis 32. Profil tepi pada potongan transisi memakai jumlah
sinus berperiode 32 piksel, jadi potongan yang berjajar tetap menyambung.

## Sebelum dipasang di server

1. Ganti `SECRET_KEY` di `config/settings.py` dengan nilai rahasia baru.
2. Setel `DEBUG = False` dan isi `ALLOWED_HOSTS` dengan domain sebenarnya.
3. Ganti sandi akun admin.
4. Jalankan `manage.py collectstatic` dan siapkan penyajian `static/` serta
   `media/` lewat web server.
