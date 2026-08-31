/* =========================================================================
   Undangan pernikahan interaktif — mesin permainan 2D top-down.
   Tanpa pustaka luar: render canvas, tabrakan AABB, analog sentuh,
   peta lokasi + jalan otomatis (BFS pada petak).
   ========================================================================= */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("data-undangan").textContent);
  var TILE = 32;                 // ukuran satu petak dalam piksel dunia
  var LAJU = 96;                 // kecepatan jalan (piksel per detik)
  var DURASI_FRAME = 0.135;      // lama satu frame animasi jalan

  /* ---------------------------------------------------------------------
     Peta. Satu huruf = satu petak.
       #  pagar tanaman      ~  kolam          f  bedeng bunga   (tak bisa dilewati)
       .  rumput             ,  rumput berbunga
       -  jalan setapak      [  ]  karpet tepi kiri/kanan        =  karpet
       w  lantai kayu        m  lantai marmer  t  tanah
     --------------------------------------------------------------------- */
  var PETA = [
    "########################################",
    "########################################",
    "##....................................##",
    "##....ff.......mmmmmmmmmm.......ff....##",
    "##....,........mmmmmmmmmm......,......##",
    "##.............mmmmmmmmmm.............##",
    "##.............mmmm[]mmmm.............##",
    "##.............mmmm[]mmmm.............##",
    "##.............mmmm[]mmmm.............##",
    "##.................[].................##",
    "##...wwwwwww.......[].......wwwwwww...##",
    "##...wwwwwww.......[].......wwwwwww...##",
    "##...wwwwwww.......[].......wwwwwww...##",
    "##...wwwwwww-------[]-------wwwwwww...##",
    "##...wwwwwww.......[].......wwwwwww...##",
    "##...wwwwwww.......[].......wwwwwww...##",
    "##.................[].................##",
    "##....,............[]............,....##",
    "##.................[].................##",
    "##.................[].................##",
    "##..~~~~~..........[].................##",
    "##..~~~~~..---.....[].....---.........##",
    "##..~~~~~..---.....[].....---.........##",
    "##..~~~~~..........[].................##",
    "##.................[].................##",
    "##....,............[]............,....##",
    "##....ff...........[]...........ff....##",
    "##.................[].................##",
    "##################.[].##################",
    "########################################"
  ];

  // Urutan indeks WAJIB sama dengan URUTAN_TILE di tools/buat_aset.py
  var INDEKS_TILE = {
    ".": 0, ",": 3, "-": 4, "=": 5, "[": 6, "]": 7,
    "w": 8, "m": 9, "~": 10, "#": 13, "t": 14, "f": 15
  };
  var VARIAN_RUMPUT = [0, 1, 2];
  var FRAME_AIR = [10, 11, 12];
  var PADAT = { "#": true, "~": true, "f": true };
  var RUMPUT = { ".": true, ",": true };
  // Karpet sengaja tidak diberi tepi rumput supaya lis emasnya tetap tegas.
  var BUTUH_TEPI = { "-": true, "w": true, "m": true, "t": true, "~": true, "f": true };
  var KARPET = { "=": true, "[": true, "]": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * TILE;
  var TINGGI_DUNIA = TINGGI_PETA * TILE;

  var WARNA_PETAK = {
    "#": "#3a6a42", "~": "#68a2c4", ".": "#6ea461", ",": "#7cb06d",
    "-": "#dbcfb9", "=": "#a83e4a", "[": "#a83e4a", "]": "#a83e4a",
    "w": "#ac8258", "m": "#eae5dc", "t": "#bea07c", "f": "#8a6a52"
  };

  /* ---------------------------------------------------------------------
     Objek di peta. x/y dalam satuan petak; y adalah alas (kaki) objek.
     `padat` = [lebar, tinggi] kotak tabrakan dalam satuan petak.
     --------------------------------------------------------------------- */
  var OBJEK = [
    { gambar: "gerbang",   x: 19.5, y: 29.4 },
    { gambar: "pelaminan", x: 19.5, y: 6.5,  padat: [4.0, 0.8], zona: "pengantin" },
    // Sepasang mempelai berdiri di depan gebyok; y-nya lebih besar dari
    // pelaminan supaya urutan gambarnya di depan latar.
    { gambar: "pengantin_pria",   x: 18.95, y: 7.2, padat: [0.55, 0.3] },
    { gambar: "pengantin_wanita", x: 20.05, y: 7.2, padat: [0.55, 0.3] },
    { gambar: "galeri",    x: 8,    y: 12.2, padat: [1.6, 0.6], zona: "galeri" },
    { gambar: "buku_tamu", x: 31,   y: 12.2, padat: [1.2, 0.5], zona: "ucapan" },
    { gambar: "papan",     x: 12,   y: 20.9, padat: [1.4, 0.5], zona: "acara" },
    { gambar: "hadiah",    x: 27,   y: 20.9, padat: [1.3, 0.5], zona: "hadiah" },

    { gambar: "meja_tumpeng",  x: 25.8, y: 7.6, padat: [1.6, 0.5] },
    { gambar: "kembar_mayang", x: 16.2, y: 7.0, padat: [0.7, 0.4] },
    { gambar: "kembar_mayang", x: 22.8, y: 7.0, padat: [0.7, 0.4] },
    { gambar: "air_mancur",    x: 33,   y: 22.6, padat: [1.9, 0.7] },

    { gambar: "teratai", x: 5.0, y: 21.4 },
    { gambar: "teratai", x: 7.4, y: 22.6 },
    { gambar: "teratai", x: 6.2, y: 20.6 },

    { gambar: "bangku", x: 15.4, y: 11.4, padat: [1.7, 0.5] },
    { gambar: "bangku", x: 24.6, y: 11.4, padat: [1.7, 0.5] },
    { gambar: "bangku", x: 15.4, y: 16.4, padat: [1.7, 0.5] },
    { gambar: "bangku", x: 24.6, y: 16.4, padat: [1.7, 0.5] },

    { gambar: "lampu", x: 17.4, y: 9.8,  padat: [0.5, 0.4] },
    { gambar: "lampu", x: 22.6, y: 9.8,  padat: [0.5, 0.4] },
    { gambar: "lampu", x: 17.4, y: 19.8, padat: [0.5, 0.4] },
    { gambar: "lampu", x: 22.6, y: 19.8, padat: [0.5, 0.4] },
    { gambar: "lampu", x: 17.4, y: 26.8, padat: [0.5, 0.4] },
    { gambar: "lampu", x: 22.6, y: 26.8, padat: [0.5, 0.4] },

    { gambar: "umbul_umbul", x: 18.3, y: 11.9, padat: [0.5, 0.3] },
    { gambar: "umbul_umbul", x: 21.7, y: 11.9, padat: [0.5, 0.3] },
    { gambar: "umbul_umbul", x: 18.3, y: 17.9, padat: [0.5, 0.3] },
    { gambar: "umbul_umbul", x: 21.7, y: 17.9, padat: [0.5, 0.3] },
    { gambar: "umbul_umbul", x: 18.3, y: 25.4, padat: [0.5, 0.3] },
    { gambar: "umbul_umbul", x: 21.7, y: 25.4, padat: [0.5, 0.3] },

    { gambar: "pot", x: 18.3, y: 8.9  }, { gambar: "pot", x: 21.7, y: 8.9  },
    { gambar: "pot", x: 18.3, y: 14.9 }, { gambar: "pot", x: 21.7, y: 14.9 },
    { gambar: "pot", x: 18.3, y: 22.9 }, { gambar: "pot", x: 21.7, y: 22.9 },
    { gambar: "pot", x: 18.3, y: 27.8 }, { gambar: "pot", x: 21.7, y: 27.8 },
    { gambar: "pot", x: 16.2, y: 4.4  }, { gambar: "pot", x: 23.8, y: 4.4  },

    { gambar: "pohon_kamboja", x: 13.2, y: 6.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_kamboja", x: 26.8, y: 6.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_kamboja", x: 4.4,  y: 9.4,  padat: [0.9, 0.4] },
    { gambar: "pohon_kamboja", x: 35.6, y: 9.4,  padat: [0.9, 0.4] },
    { gambar: "pohon_kamboja", x: 9.5,  y: 24.4, padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 5.5,  y: 4.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 11.5, y: 3.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 28.5, y: 3.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 34.5, y: 4.6,  padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 4.5,  y: 17.6, padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 36.0, y: 17.6, padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 6.5,  y: 27.4, padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 33.5, y: 27.4, padat: [0.9, 0.4] },
    { gambar: "pohon_palem", x: 30.5, y: 18.6, padat: [0.9, 0.4] },

    { gambar: "semak", x: 3.2,  y: 14.6 }, { gambar: "semak", x: 36.8, y: 14.6 },
    { gambar: "semak", x: 9.5,  y: 18.6 }, { gambar: "semak", x: 29.6, y: 24.6 },
    { gambar: "semak", x: 13.5, y: 24.6 }, { gambar: "semak", x: 26.5, y: 16.6 },
    { gambar: "semak", x: 10.5, y: 8.6  }, { gambar: "semak", x: 29.5, y: 8.6  },
    { gambar: "semak", x: 15.5, y: 25.6 }, { gambar: "semak", x: 24.5, y: 25.6 },
    { gambar: "semak", x: 3.4,  y: 26.6 }, { gambar: "semak", x: 36.6, y: 26.6 }
  ];

  /* `berdiri` = petak tempat karakter berhenti saat menuju lokasi ini. */
  var ZONA = {
    pengantin: {
      judul: "Pelaminan", aksi: "Lihat Mempelai", radius: 3.2,
      berdiri: [19, 9], warna: "#c9718c",
      ket: "Foto & biodata kedua mempelai"
    },
    galeri: {
      judul: "Galeri Foto", aksi: "Buka Galeri", radius: 2.3,
      berdiri: [8, 13], warna: "#5f8f74",
      ket: "Kumpulan foto prewedding"
    },
    ucapan: {
      judul: "Buku Tamu", aksi: "Tulis Ucapan", radius: 2.3,
      berdiri: [31, 13], warna: "#b08340",
      ket: "Kirim doa & konfirmasi kehadiran"
    },
    acara: {
      judul: "Papan Acara", aksi: "Baca Acara", radius: 2.3,
      berdiri: [12, 22], warna: "#6b7fa8",
      ket: "Waktu, tempat, dan hitung mundur"
    },
    hadiah: {
      judul: "Amplop Digital", aksi: "Kirim Hadiah", radius: 2.3,
      berdiri: [27, 22], warna: "#a86a8c",
      ket: "Nomor rekening & QRIS"
    }
  };
  var URUTAN_ZONA = ["pengantin", "galeri", "acara", "ucapan", "hadiah"];

  // Urutan indeks WAJIB sama dengan URUTAN_TEPI di tools/buat_aset.py
  var TEPI = {
    atas: 0, bawah: 1, kiri: 2, kanan: 3,
    kiri_atas: 4, kanan_atas: 5, kiri_bawah: 6, kanan_bawah: 7
  };

  /* =====================================================================
     Elemen halaman
     ===================================================================== */
  var el = {
    sampul: document.getElementById("sampul"),
    tombolBuka: document.getElementById("tombol-buka"),
    permainan: document.getElementById("permainan"),
    kanvas: document.getElementById("kanvas"),
    memuat: document.getElementById("memuat"),
    isiMuat: document.getElementById("isi-muat"),
    lokasi: document.getElementById("hud-lokasi"),
    kemajuan: document.getElementById("hud-kemajuan"),
    analog: document.getElementById("analog"),
    alas: document.getElementById("analog-alas"),
    knop: document.getElementById("analog-tombol"),
    tombolAksi: document.getElementById("tombol-aksi"),
    labelAksi: document.getElementById("label-aksi"),
    lapisPopup: document.getElementById("lapis-popup"),
    tombolPeta: document.getElementById("tombol-peta"),
    tombolMusik: document.getElementById("tombol-musik"),
    tombolPetunjuk: document.getElementById("tombol-petunjuk"),
    bingkaiPetaMini: document.getElementById("bingkai-peta-mini"),
    petaMini: document.getElementById("peta-mini"),
    petaBesar: document.getElementById("peta-besar"),
    daftarLokasi: document.getElementById("daftar-lokasi"),
    pemberitahuan: document.getElementById("pemberitahuan"),
    lightbox: document.getElementById("lightbox"),
    musik: document.getElementById("musik")
  };
  var ctx = el.kanvas.getContext("2d");

  /* =====================================================================
     Pemuatan aset
     ===================================================================== */
  var gambar = {};

  function muatAset() {
    var nama = Object.keys(DATA.aset);
    var selesaiCount = 0;
    return Promise.all(nama.map(function (n) {
      return new Promise(function (selesai) {
        var img = new Image();
        img.onload = img.onerror = function () {
          gambar[n] = img;
          selesaiCount++;
          if (el.isiMuat) el.isiMuat.style.width = Math.round(selesaiCount / nama.length * 100) + "%";
          selesai();
        };
        img.src = DATA.aset[n];
      });
    }));
  }

  /* =====================================================================
     Keadaan permainan
     ===================================================================== */
  var pemain = {
    x: 19.5 * TILE,
    y: 26.5 * TILE,
    arah: 3,              // 0 bawah, 1 kiri, 2 kanan, 3 atas
    frame: 0,
    waktuFrame: 0,
    berjalan: false,
    lembar: "karakter_pria"
  };
  var LEBAR_SPRITE = 48, TINGGI_SPRITE = 80;
  var KOTAK = { w: 22, h: 14, offsetY: -10 };

  var kamera = { x: 0, y: 0, diinisialisasi: false };
  var skala = 1, dpr = 1, lebarCss = 0, tinggiCss = 0;
  var berjalanTerus = false;
  var zonaAktif = null;
  var objekTerurut = [];
  var waktuTotal = 0;
  var dikunjungi = {};
  var kelopak = [];
  var gradasiVignet = null;

  /* =====================================================================
     Ukuran kanvas
     ===================================================================== */
  function aturUkuran() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    lebarCss = el.permainan.clientWidth;
    tinggiCss = el.permainan.clientHeight;
    el.kanvas.width = Math.round(lebarCss * dpr);
    el.kanvas.height = Math.round(tinggiCss * dpr);
    el.kanvas.style.width = lebarCss + "px";
    el.kanvas.style.height = tinggiCss + "px";

    // Zoom Stardew Valley: pandangan luas dari atas seperti tema tropis.
    // Tema tropis (PETAK 48) mematok 11×16 petak = 528×768 px dunia.
    // Dengan TILE 32, setara ~16.5×24 petak agar proporsi pandang identik.
    skala = Math.max(lebarCss / (16.5 * TILE), tinggiCss / (24.0 * TILE));
    skala = Math.max(0.7, Math.min(1.8, skala));
    ctx.imageSmoothingEnabled = false;

    gradasiVignet = ctx.createRadialGradient(
      lebarCss / 2, tinggiCss / 2, Math.min(lebarCss, tinggiCss) * 0.34,
      lebarCss / 2, tinggiCss / 2, Math.max(lebarCss, tinggiCss) * 0.76
    );
    gradasiVignet.addColorStop(0, "rgba(38, 30, 22, 0)");
    gradasiVignet.addColorStop(1, "rgba(38, 30, 22, 0.34)");

    siapkanKelopak();
    aturUkuranPetaMini();
  }

  /* =====================================================================
     Tabrakan
     ===================================================================== */
  function petakPadat(kx, ky) {
    if (kx < 0 || ky < 0 || kx >= LEBAR_PETA || ky >= TINGGI_PETA) return true;
    return !!PADAT[PETA[ky][kx]];
  }

  var kotakObjek = [];
  function siapkanKotakObjek() {
    kotakObjek = OBJEK.filter(function (o) { return o.padat; }).map(function (o) {
      var w = o.padat[0] * TILE, h = o.padat[1] * TILE;
      return { x: o.x * TILE - w / 2, y: o.y * TILE - h, w: w, h: h };
    });
  }

  function bentrok(x, y) {
    var kiri = x - KOTAK.w / 2;
    var atas = y + KOTAK.offsetY;
    var kanan = kiri + KOTAK.w;
    var bawah = atas + KOTAK.h;

    var kx0 = Math.floor(kiri / TILE), kx1 = Math.floor((kanan - 0.01) / TILE);
    var ky0 = Math.floor(atas / TILE), ky1 = Math.floor((bawah - 0.01) / TILE);
    for (var ky = ky0; ky <= ky1; ky++) {
      for (var kx = kx0; kx <= kx1; kx++) {
        if (petakPadat(kx, ky)) return true;
      }
    }
    for (var i = 0; i < kotakObjek.length; i++) {
      var k = kotakObjek[i];
      if (kiri < k.x + k.w && kanan > k.x && atas < k.y + k.h && bawah > k.y) return true;
    }
    return false;
  }

  /* =====================================================================
     Pencarian jalur (BFS pada petak) untuk fitur "pergi ke lokasi"
     ===================================================================== */
  function petakBisaDipijak(kx, ky) {
    if (kx < 0 || ky < 0 || kx >= LEBAR_PETA || ky >= TINGGI_PETA) return false;
    return !bentrok(kx * TILE + TILE / 2, ky * TILE + TILE / 2);
  }

  function petakTerdekatYangBisa(kx, ky) {
    if (petakBisaDipijak(kx, ky)) return { x: kx, y: ky };
    for (var jari = 1; jari <= 3; jari++) {
      for (var dy = -jari; dy <= jari; dy++) {
        for (var dx = -jari; dx <= jari; dx++) {
          if (petakBisaDipijak(kx + dx, ky + dy)) return { x: kx + dx, y: ky + dy };
        }
      }
    }
    return null;
  }

  function garisBebas(a, b) {
    var jarak = Math.hypot(b.x - a.x, b.y - a.y);
    var langkah = Math.max(1, Math.ceil(jarak / 6));
    for (var i = 1; i <= langkah; i++) {
      var t = i / langkah;
      if (bentrok(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t)) return false;
    }
    return true;
  }

  function haluskanJalur(titik) {
    if (titik.length < 3) return titik;
    var hasil = [titik[0]];
    var i = 0;
    while (i < titik.length - 1) {
      var j = titik.length - 1;
      while (j > i + 1 && !garisBebas(titik[i], titik[j])) j--;
      hasil.push(titik[j]);
      i = j;
    }
    return hasil;
  }

  function cariJalur(xAwal, yAwal, kxTujuan, kyTujuan) {
    var awal = petakTerdekatYangBisa(Math.floor(xAwal / TILE), Math.floor(yAwal / TILE));
    var tujuan = petakTerdekatYangBisa(kxTujuan, kyTujuan);
    if (!awal || !tujuan) return null;

    var dari = new Int32Array(LEBAR_PETA * TINGGI_PETA).fill(-1);
    var indeksAwal = awal.y * LEBAR_PETA + awal.x;
    var indeksTujuan = tujuan.y * LEBAR_PETA + tujuan.x;
    dari[indeksAwal] = indeksAwal;

    var antrian = [indeksAwal];
    var kepala = 0;
    var geser = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    while (kepala < antrian.length) {
      var kini = antrian[kepala++];
      if (kini === indeksTujuan) break;
      var cx = kini % LEBAR_PETA, cy = (kini / LEBAR_PETA) | 0;
      for (var g = 0; g < 4; g++) {
        var nx = cx + geser[g][0], ny = cy + geser[g][1];
        if (nx < 0 || ny < 0 || nx >= LEBAR_PETA || ny >= TINGGI_PETA) continue;
        var indeks = ny * LEBAR_PETA + nx;
        if (dari[indeks] !== -1 || !petakBisaDipijak(nx, ny)) continue;
        dari[indeks] = kini;
        antrian.push(indeks);
      }
    }
    if (dari[indeksTujuan] === -1) return null;

    var mundur = [];
    var jalan = indeksTujuan;
    while (jalan !== indeksAwal) {
      mundur.push({
        x: (jalan % LEBAR_PETA) * TILE + TILE / 2,
        y: ((jalan / LEBAR_PETA) | 0) * TILE + TILE / 2
      });
      jalan = dari[jalan];
    }
    mundur.push({ x: xAwal, y: yAwal });
    mundur.reverse();
    return haluskanJalur(mundur).slice(1);
  }

  /* =====================================================================
     Jalan otomatis
     ===================================================================== */
  var jalurOtomatis = null;
  var bukaSetelahSampai = null;
  var sisaWaktuOtomatis = 0;

  function pergiKe(kunci) {
    var z = ZONA[kunci];
    if (!z) return;
    tutupPopup();
    var jalur = cariJalur(pemain.x, pemain.y, z.berdiri[0], z.berdiri[1]);
    if (!jalur || !jalur.length) {
      pemain.x = z.berdiri[0] * TILE + TILE / 2;
      pemain.y = z.berdiri[1] * TILE + TILE / 2;
      jalurOtomatis = null;
      perbaruiZona();
      bukaPopup("popup-" + kunci);
      return;
    }
    jalurOtomatis = jalur;
    bukaSetelahSampai = kunci;
    sisaWaktuOtomatis = 30;
    beriTahu("Menuju " + z.judul + "…");
  }

  function batalkanOtomatis() {
    jalurOtomatis = null;
    bukaSetelahSampai = null;
  }

  /* =====================================================================
     Masukan: papan ketik + analog sentuh
     ===================================================================== */
  var tombol = {};
  var arahKetik = { x: 0, y: 0 };
  var arahAnalog = { x: 0, y: 0 };
  var analogAktif = false;
  var idPointer = null;
  var pusatAnalog = { x: 0, y: 0 };
  var RADIUS_ANALOG = 46;

  var PETA_TOMBOL = {
    ArrowUp: "atas", KeyW: "atas",
    ArrowDown: "bawah", KeyS: "bawah",
    ArrowLeft: "kiri", KeyA: "kiri",
    ArrowRight: "kanan", KeyD: "kanan"
  };

  window.addEventListener("keydown", function (e) {
    if (e.code === "Escape") { tutupPopup(); return; }
    if (e.code === "KeyM" && !popupTerbuka()) { bukaPopup("popup-peta"); return; }
    if ((e.code === "Space" || e.code === "Enter" || e.code === "KeyE") && !popupTerbuka() && zonaAktif) {
      e.preventDefault();
      bukaPopup("popup-" + zonaAktif.zona);
      return;
    }
    if (PETA_TOMBOL[e.code]) { tombol[PETA_TOMBOL[e.code]] = true; e.preventDefault(); hitungKetik(); }
  });
  window.addEventListener("keyup", function (e) {
    if (PETA_TOMBOL[e.code]) { tombol[PETA_TOMBOL[e.code]] = false; hitungKetik(); }
  });
  window.addEventListener("blur", function () { tombol = {}; hitungKetik(); lepasAnalog(); });

  function hitungKetik() {
    arahKetik.x = (tombol.kanan ? 1 : 0) - (tombol.kiri ? 1 : 0);
    arahKetik.y = (tombol.bawah ? 1 : 0) - (tombol.atas ? 1 : 0);
    if (arahKetik.x || arahKetik.y) batalkanOtomatis();
  }

  function posisiAlas(x, y) {
    var kotak = el.analog.getBoundingClientRect();
    var batas = RADIUS_ANALOG + 18;
    x = Math.max(kotak.left + batas, Math.min(kotak.right - batas, x));
    y = Math.max(kotak.top + batas, Math.min(kotak.bottom - batas, y));
    pusatAnalog.x = x;
    pusatAnalog.y = y;
    el.alas.style.left = (x - kotak.left) + "px";
    el.alas.style.bottom = (kotak.bottom - y) + "px";
  }

  el.analog.addEventListener("pointerdown", function (e) {
    if (popupTerbuka()) return;
    idPointer = e.pointerId;
    analogAktif = true;
    batalkanOtomatis();
    el.analog.classList.add("aktif");
    try { el.analog.setPointerCapture(e.pointerId); } catch (err) { /* peramban lama */ }
    posisiAlas(e.clientX, e.clientY);
    gerakAnalog(e.clientX, e.clientY);
    e.preventDefault();
  });
  el.analog.addEventListener("pointermove", function (e) {
    if (!analogAktif || e.pointerId !== idPointer) return;
    gerakAnalog(e.clientX, e.clientY);
    e.preventDefault();
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach(function (jenis) {
    el.analog.addEventListener(jenis, function (e) {
      if (e.pointerId === idPointer) lepasAnalog();
    });
  });

  function gerakAnalog(x, y) {
    var dx = x - pusatAnalog.x;
    var dy = y - pusatAnalog.y;
    var jarak = Math.hypot(dx, dy);
    if (jarak > RADIUS_ANALOG) { dx = dx / jarak * RADIUS_ANALOG; dy = dy / jarak * RADIUS_ANALOG; }
    el.knop.style.transform = "translate(" + dx + "px," + dy + "px)";
    var nx = dx / RADIUS_ANALOG, ny = dy / RADIUS_ANALOG;
    if (Math.hypot(nx, ny) < 0.2) { arahAnalog.x = 0; arahAnalog.y = 0; }
    else { arahAnalog.x = nx; arahAnalog.y = ny; }
  }

  function lepasAnalog() {
    analogAktif = false;
    idPointer = null;
    arahAnalog.x = 0;
    arahAnalog.y = 0;
    el.analog.classList.remove("aktif");
    el.knop.style.transform = "translate(0,0)";
    el.alas.style.left = "";
    el.alas.style.bottom = "";
  }

  /* =====================================================================
     Pembaruan tiap frame
     ===================================================================== */
  function perbarui(dt) {
    var gx = arahAnalog.x || arahKetik.x;
    var gy = arahAnalog.y || arahKetik.y;

    if (jalurOtomatis && jalurOtomatis.length) {
      sisaWaktuOtomatis -= dt;
      var tuj = jalurOtomatis[0];
      var dx = tuj.x - pemain.x, dy = tuj.y - pemain.y;
      var sisa = Math.hypot(dx, dy);
      if (sisa < 5) {
        jalurOtomatis.shift();
        if (!jalurOtomatis.length) selesaikanOtomatis();
      } else if (sisaWaktuOtomatis <= 0) {
        batalkanOtomatis();
      } else {
        gx = dx / sisa;
        gy = dy / sisa;
      }
    }

    var panjang = Math.hypot(gx, gy);
    if (panjang > 1) { gx /= panjang; gy /= panjang; panjang = 1; }

    pemain.berjalan = panjang > 0.01;
    if (pemain.berjalan) {
      var langkah = LAJU * dt;
      var barux = pemain.x + gx * langkah;
      if (!bentrok(barux, pemain.y)) pemain.x = barux;
      var baruy = pemain.y + gy * langkah;
      if (!bentrok(pemain.x, baruy)) pemain.y = baruy;

      if (Math.abs(gx) > Math.abs(gy)) pemain.arah = gx > 0 ? 2 : 1;
      else pemain.arah = gy > 0 ? 0 : 3;

      pemain.waktuFrame += dt;
      if (pemain.waktuFrame >= DURASI_FRAME) {
        pemain.waktuFrame -= DURASI_FRAME;
        pemain.frame = (pemain.frame + 1) % 4;
      }
    } else {
      pemain.frame = 0;
      pemain.waktuFrame = 0;
    }

    pemain.x = Math.max(TILE, Math.min(LEBAR_DUNIA - TILE, pemain.x));
    pemain.y = Math.max(TILE, Math.min(TINGGI_DUNIA - TILE * 0.5, pemain.y));

    perbaruiZona();
    perbaruiKamera(dt);
    perbaruiKelopak(dt);
  }

  function selesaikanOtomatis() {
    var kunci = bukaSetelahSampai;
    jalurOtomatis = null;
    bukaSetelahSampai = null;
    perbaruiZona();
    if (kunci) bukaPopup("popup-" + kunci);
  }

  function perbaruiZona() {
    var terdekat = null, jarakTerdekat = Infinity;
    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona) continue;
      var dx = pemain.x - o.x * TILE;
      var dy = pemain.y - (o.y + 0.4) * TILE;
      var jarak = Math.hypot(dx, dy);
      if (jarak < ZONA[o.zona].radius * TILE && jarak < jarakTerdekat) {
        jarakTerdekat = jarak;
        terdekat = o;
      }
    }
    if (terdekat === zonaAktif) return;
    zonaAktif = terdekat;
    if (zonaAktif) {
      el.labelAksi.textContent = ZONA[zonaAktif.zona].aksi;
      el.tombolAksi.classList.remove("tersembunyi");
      el.tombolAksi.style.setProperty("--warna-zona", ZONA[zonaAktif.zona].warna);
      el.lokasi.textContent = ZONA[zonaAktif.zona].judul;
    } else {
      el.tombolAksi.classList.add("tersembunyi");
      el.lokasi.textContent = "Taman Undangan";
    }
  }

  function perbaruiKamera(dt) {
    var lebarTampak = lebarCss / skala;
    var tinggiTampak = tinggiCss / skala;
    var targetX = lebarTampak >= LEBAR_DUNIA
      ? (LEBAR_DUNIA - lebarTampak) / 2
      : Math.max(0, Math.min(LEBAR_DUNIA - lebarTampak, pemain.x - lebarTampak / 2));
    var targetY = tinggiTampak >= TINGGI_DUNIA
      ? (TINGGI_DUNIA - tinggiTampak) / 2
      : Math.max(0, Math.min(TINGGI_DUNIA - tinggiTampak, pemain.y - tinggiTampak * 0.52));

    if (!kamera.diinisialisasi) {
      kamera.x = targetX;
      kamera.y = targetY;
      kamera.diinisialisasi = true;
    } else {
      var lajuLerp = 1 - Math.exp(-12 * (dt || 0.016));
      kamera.x += (targetX - kamera.x) * lajuLerp;
      kamera.y += (targetY - kamera.y) * lajuLerp;
    }
  }

  function keLayarX(wx) { return (wx - kamera.x) * skala; }
  function keLayarY(wy) { return (wy - kamera.y) * skala; }

  /* =====================================================================
     Kelopak bunga yang beterbangan (ruang layar)
     ===================================================================== */
  var WARNA_KELOPAK = ["rgba(246,196,210,.85)", "rgba(252,246,240,.8)", "rgba(248,226,180,.75)"];

  function siapkanKelopak() {
    var jumlah = Math.round(Math.min(26, Math.max(12, lebarCss / 42)));
    kelopak = [];
    for (var i = 0; i < jumlah; i++) {
      kelopak.push({
        x: Math.random() * lebarCss,
        y: Math.random() * tinggiCss,
        lajuX: 14 + Math.random() * 20,
        lajuY: 16 + Math.random() * 22,
        ukuran: 3 + Math.random() * 3.5,
        fase: Math.random() * Math.PI * 2,
        putar: Math.random() * Math.PI,
        warna: WARNA_KELOPAK[i % WARNA_KELOPAK.length]
      });
    }
  }

  function perbaruiKelopak(dt) {
    for (var i = 0; i < kelopak.length; i++) {
      var k = kelopak[i];
      k.fase += dt * 1.7;
      k.x += (k.lajuX + Math.sin(k.fase) * 12) * dt;
      k.y += k.lajuY * dt;
      k.putar += dt * 1.1;
      if (k.y > tinggiCss + 12) { k.y = -12; k.x = Math.random() * lebarCss; }
      if (k.x > lebarCss + 12) { k.x = -12; k.y = Math.random() * tinggiCss; }
    }
  }

  function gambarKelopak() {
    for (var i = 0; i < kelopak.length; i++) {
      var k = kelopak[i];
      ctx.save();
      ctx.translate(k.x, k.y);
      ctx.rotate(k.putar);
      ctx.fillStyle = k.warna;
      ctx.beginPath();
      ctx.ellipse(0, 0, k.ukuran, k.ukuran * 0.58, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  /* =====================================================================
     Menggambar dunia
     ===================================================================== */
  function acak(x, y) {
    var n = (x * 73856093) ^ (y * 19349663);
    n = (n ^ (n >>> 13)) >>> 0;
    return (n % 997) / 997;
  }

  function indeksTile(huruf, x, y) {
    if (huruf === ".") {
      var r = acak(x, y);
      if (r < 0.07) return INDEKS_TILE[","];
      return VARIAN_RUMPUT[Math.floor(r * 1000) % 3];
    }
    if (huruf === "~") return FRAME_AIR[Math.floor(waktuTotal * 2.2 + x * 0.4 + y * 0.7) % 3];
    return INDEKS_TILE[huruf] !== undefined ? INDEKS_TILE[huruf] : 0;
  }

  function adaRumput(x, y) {
    if (x < 0 || y < 0 || x >= LEBAR_PETA || y >= TINGGI_PETA) return false;
    return !!RUMPUT[PETA[y][x]];
  }

  function gambarPetak(indeks, x, y) {
    ctx.drawImage(gambar.tileset, indeks * TILE, 0, TILE, TILE, x * TILE, y * TILE, TILE, TILE);
  }

  function gambarTepi(indeks, x, y) {
    ctx.drawImage(gambar.tepi, indeks * TILE, 0, TILE, TILE, x * TILE, y * TILE, TILE, TILE);
  }

  function gambarPeta() {
    var lebarTampak = lebarCss / skala;
    var tinggiTampak = tinggiCss / skala;
    var x0 = Math.max(0, Math.floor(kamera.x / TILE));
    var y0 = Math.max(0, Math.floor(kamera.y / TILE));
    var x1 = Math.min(LEBAR_PETA - 1, Math.ceil((kamera.x + lebarTampak) / TILE));
    var y1 = Math.min(TINGGI_PETA - 1, Math.ceil((kamera.y + tinggiTampak) / TILE));

    for (var y = y0; y <= y1; y++) {
      var baris = PETA[y];
      for (var x = x0; x <= x1; x++) {
        var huruf = baris[x];
        gambarPetak(indeksTile(huruf, x, y), x, y);

        if (KARPET[huruf]) taburKelopakKarpet(x, y);

        if (!BUTUH_TEPI[huruf]) continue;
        if (adaRumput(x, y - 1)) gambarTepi(TEPI.atas, x, y);
        if (adaRumput(x, y + 1)) gambarTepi(TEPI.bawah, x, y);
        if (adaRumput(x - 1, y)) gambarTepi(TEPI.kiri, x, y);
        if (adaRumput(x + 1, y)) gambarTepi(TEPI.kanan, x, y);
        if (!adaRumput(x, y - 1) && !adaRumput(x - 1, y) && adaRumput(x - 1, y - 1)) gambarTepi(TEPI.kiri_atas, x, y);
        if (!adaRumput(x, y - 1) && !adaRumput(x + 1, y) && adaRumput(x + 1, y - 1)) gambarTepi(TEPI.kanan_atas, x, y);
        if (!adaRumput(x, y + 1) && !adaRumput(x - 1, y) && adaRumput(x - 1, y + 1)) gambarTepi(TEPI.kiri_bawah, x, y);
        if (!adaRumput(x, y + 1) && !adaRumput(x + 1, y) && adaRumput(x + 1, y + 1)) gambarTepi(TEPI.kanan_bawah, x, y);
      }
    }
  }

  /* Taburan kelopak di atas karpet, posisinya tetap per petak. */
  function taburKelopakKarpet(x, y) {
    var r = acak(x + 7, y + 13);
    if (r > 0.55) return;
    var px = x * TILE + Math.floor(r * 1000) % 26 + 3;
    var py = y * TILE + Math.floor(r * 7919) % 26 + 3;
    ctx.fillStyle = r < 0.2 ? "rgba(250,240,236,.9)" : "rgba(240,190,204,.9)";
    ctx.fillRect(px, py, 2, 2);
    ctx.fillRect(px + 2, py + 1, 1, 1);
  }

  function gambarBayangan(x, y, lebar) {
    ctx.fillStyle = "rgba(28, 22, 18, .28)";
    ctx.beginPath();
    ctx.ellipse(x, y - 2, lebar / 2, lebar / 3.8, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  function gambarCincinAktif(o) {
    var denyut = 0.5 + Math.sin(waktuTotal * 3) * 0.5;
    var jari = 16 + denyut * 5;
    ctx.save();
    ctx.strokeStyle = ZONA[o.zona].warna;
    ctx.globalAlpha = 0.35 + denyut * 0.35;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.ellipse(o.x * TILE, o.y * TILE - 2, jari, jari / 2.2, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  function gambarObjek(o) {
    var img = gambar[o.gambar];
    if (!img || !img.width) return;
    gambarBayangan(o.x * TILE, o.y * TILE, Math.min(img.width * 0.7, 44));
    ctx.drawImage(img, Math.round(o.x * TILE - img.width / 2), Math.round(o.y * TILE - img.height));
  }

  function gambarPemain() {
    var lembar = gambar[pemain.lembar];
    if (!lembar || !lembar.width) return;
    gambarBayangan(pemain.x, pemain.y, 26);
    ctx.drawImage(
      lembar,
      pemain.frame * LEBAR_SPRITE, pemain.arah * TINGGI_SPRITE, LEBAR_SPRITE, TINGGI_SPRITE,
      Math.round(pemain.x - LEBAR_SPRITE / 2), Math.round(pemain.y - TINGGI_SPRITE + 8),
      LEBAR_SPRITE, TINGGI_SPRITE
    );
  }

  /* =====================================================================
     Lapisan layar: papan nama, panah arah, kelopak, vignet
     ===================================================================== */
  function kotakBulat(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function gambarPapanNama(o) {
    var z = ZONA[o.zona];
    var img = gambar[o.gambar];
    var tinggiGambar = img && img.height ? img.height : 40;
    var sx = keLayarX(o.x * TILE);
    var syAsli = keLayarY(o.y * TILE - tinggiGambar) - 14;
    var syAlas = keLayarY(o.y * TILE);
    if (sx < -140 || sx > lebarCss + 140 || syAlas < -60 || syAsli > tinggiCss + 40) return;
    // Objek tinggi seperti pelaminan bisa membuat papan namanya keluar layar,
    // jadi tahan di bawah HUD supaya tetap terbaca.
    var sy = Math.max(96, Math.min(tinggiCss - 40, syAsli));

    var aktif = zonaAktif === o;
    var sudah = !!dikunjungi[o.zona];
    var jarakPetak = Math.hypot(pemain.x - o.x * TILE, pemain.y - o.y * TILE) / TILE;
    var alfa = jarakPetak < 7 ? 1 : Math.max(0.5, 1 - (jarakPetak - 7) / 14);

    var teks = z.judul;
    ctx.save();
    ctx.globalAlpha = alfa;
    ctx.font = "700 12px Nunito, system-ui, sans-serif";
    var lebarTeks = ctx.measureText(teks).width;
    var padKiri = 20, padKanan = sudah ? 22 : 10;
    var w = lebarTeks + padKiri + padKanan;
    var h = 24;
    if (aktif) {
      var denyut = 1 + Math.sin(waktuTotal * 4) * 0.03;
      ctx.translate(sx, sy);
      ctx.scale(denyut, denyut);
      ctx.translate(-sx, -sy);
    }
    var x = sx - w / 2, y = sy - h;

    ctx.shadowColor = "rgba(30, 24, 18, .35)";
    ctx.shadowBlur = 6;
    ctx.shadowOffsetY = 2;
    ctx.fillStyle = aktif ? z.warna : "rgba(255, 250, 244, .94)";
    kotakBulat(x, y, w, h, h / 2);
    ctx.fill();
    ctx.shadowColor = "transparent";
    ctx.shadowBlur = 0;
    ctx.shadowOffsetY = 0;

    // ekor kecil
    ctx.beginPath();
    ctx.moveTo(sx - 5, y + h - 1);
    ctx.lineTo(sx + 5, y + h - 1);
    ctx.lineTo(sx, y + h + 5);
    ctx.closePath();
    ctx.fill();

    // titik warna zona
    ctx.fillStyle = aktif ? "rgba(255,255,255,.9)" : z.warna;
    ctx.beginPath();
    ctx.arc(x + 12, y + h / 2, 4.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillStyle = aktif ? "#fffaf4" : "#45392f";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(teks, x + padKiri, y + h / 2 + 0.5);

    if (sudah) {
      ctx.strokeStyle = aktif ? "#fffaf4" : "#5f8f74";
      ctx.lineWidth = 2;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(x + w - 17, y + h / 2);
      ctx.lineTo(x + w - 13, y + h / 2 + 4);
      ctx.lineTo(x + w - 7, y + h / 2 - 4);
      ctx.stroke();
    }
    ctx.restore();
  }

  function gambarPanahArah() {
    var pusatX = lebarCss / 2, pusatY = tinggiCss / 2;
    var batasKiri = 40, batasKanan = lebarCss - 40;
    var batasAtas = 118, batasBawah = tinggiCss - 120;
    if (batasBawah <= batasAtas) return;

    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona || dikunjungi[o.zona]) continue;
      var sx = keLayarX(o.x * TILE);
      var sy = keLayarY(o.y * TILE);
      if (sx > 20 && sx < lebarCss - 20 && sy > 90 && sy < tinggiCss - 90) continue;

      var dx = sx - pusatX, dy = sy - pusatY;
      if (!dx && !dy) continue;
      var t = Math.min(
        Math.abs(dx) < 0.001 ? Infinity : (dx > 0 ? batasKanan - pusatX : pusatX - batasKiri) / Math.abs(dx),
        Math.abs(dy) < 0.001 ? Infinity : (dy > 0 ? batasBawah - pusatY : pusatY - batasAtas) / Math.abs(dy)
      );
      var ax = pusatX + dx * t, ay = pusatY + dy * t;

      ctx.save();
      ctx.translate(ax, ay);
      ctx.globalAlpha = 0.9;
      ctx.fillStyle = ZONA[o.zona].warna;
      ctx.beginPath();
      ctx.arc(0, 0, 15, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "rgba(255,250,244,.85)";
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.rotate(Math.atan2(dy, dx));
      ctx.fillStyle = "#fffaf4";
      ctx.beginPath();
      ctx.moveTo(6, 0);
      ctx.lineTo(-3, -5);
      ctx.lineTo(-3, 5);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }
  }

  function gambarSemua() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = "#2f3b2c";
    ctx.fillRect(0, 0, lebarCss, tinggiCss);

    // --- lapisan dunia ---
    var f = dpr * skala;
    ctx.setTransform(f, 0, 0, f, -Math.round(kamera.x * f), -Math.round(kamera.y * f));
    gambarPeta();
    if (zonaAktif) gambarCincinAktif(zonaAktif);

    objekTerurut.length = 0;
    for (var i = 0; i < OBJEK.length; i++) objekTerurut.push(OBJEK[i]);
    objekTerurut.push(pemain);
    objekTerurut.sort(function (a, b) {
      return (a === pemain ? a.y : a.y * TILE) - (b === pemain ? b.y : b.y * TILE);
    });
    for (var j = 0; j < objekTerurut.length; j++) {
      if (objekTerurut[j] === pemain) gambarPemain();
      else gambarObjek(objekTerurut[j]);
    }

    // --- lapisan layar (teks tajam, tidak ikut diperbesar) ---
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (gradasiVignet) {
      ctx.fillStyle = gradasiVignet;
      ctx.fillRect(0, 0, lebarCss, tinggiCss);
    }
    for (var k = 0; k < OBJEK.length; k++) {
      if (OBJEK[k].zona) gambarPapanNama(OBJEK[k]);
    }
    gambarPanahArah();
    gambarKelopak();
    gambarPetaMini();
  }

  /* =====================================================================
     Peta: cache latar, minimap, peta besar
     ===================================================================== */
  var cachePeta = {};

  function ambilCachePeta(pxPerPetak) {
    if (cachePeta[pxPerPetak]) return cachePeta[pxPerPetak];
    var c = document.createElement("canvas");
    c.width = LEBAR_PETA * pxPerPetak;
    c.height = TINGGI_PETA * pxPerPetak;
    var m = c.getContext("2d");
    for (var y = 0; y < TINGGI_PETA; y++) {
      for (var x = 0; x < LEBAR_PETA; x++) {
        m.fillStyle = WARNA_PETAK[PETA[y][x]] || "#6ea461";
        m.fillRect(x * pxPerPetak, y * pxPerPetak, pxPerPetak, pxPerPetak);
      }
    }
    cachePeta[pxPerPetak] = c;
    return c;
  }

  var ctxMini = el.petaMini ? el.petaMini.getContext("2d") : null;
  var LEBAR_MINI = 112;

  function aturUkuranPetaMini() {
    if (!el.petaMini) return;
    var tinggi = Math.round(LEBAR_MINI * TINGGI_PETA / LEBAR_PETA);
    el.petaMini.width = Math.round(LEBAR_MINI * dpr);
    el.petaMini.height = Math.round(tinggi * dpr);
    el.petaMini.style.width = LEBAR_MINI + "px";
    el.petaMini.style.height = tinggi + "px";
  }

  function gambarPetaMini() {
    if (!ctxMini) return;
    var lebar = LEBAR_MINI;
    var tinggi = lebar * TINGGI_PETA / LEBAR_PETA;
    ctxMini.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctxMini.clearRect(0, 0, lebar, tinggi);
    ctxMini.imageSmoothingEnabled = false;
    ctxMini.drawImage(ambilCachePeta(4), 0, 0, lebar, tinggi);

    var sk = lebar / LEBAR_DUNIA;
    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona) continue;
      ctxMini.fillStyle = dikunjungi[o.zona] ? "rgba(255,250,244,.95)" : ZONA[o.zona].warna;
      ctxMini.strokeStyle = "rgba(46,38,30,.7)";
      ctxMini.lineWidth = 1;
      ctxMini.beginPath();
      ctxMini.arc(o.x * TILE * sk, o.y * TILE * sk, 3.4, 0, Math.PI * 2);
      ctxMini.fill();
      ctxMini.stroke();
    }
    var denyut = 2.8 + Math.sin(waktuTotal * 4) * 0.7;
    ctxMini.fillStyle = "#2f3b2c";
    ctxMini.beginPath();
    ctxMini.arc(pemain.x * sk, pemain.y * sk, denyut + 1.6, 0, Math.PI * 2);
    ctxMini.fill();
    ctxMini.fillStyle = "#fffaf4";
    ctxMini.beginPath();
    ctxMini.arc(pemain.x * sk, pemain.y * sk, denyut, 0, Math.PI * 2);
    ctxMini.fill();
  }

  var PX_PETA_BESAR = 13;

  function gambarPetaBesar() {
    if (!el.petaBesar) return;
    var lebar = LEBAR_PETA * PX_PETA_BESAR;
    var tinggi = TINGGI_PETA * PX_PETA_BESAR;
    var r = Math.min(window.devicePixelRatio || 1, 2);
    el.petaBesar.width = Math.round(lebar * r);
    el.petaBesar.height = Math.round(tinggi * r);
    el.petaBesar.style.width = "100%";
    var m = el.petaBesar.getContext("2d");
    m.setTransform(r, 0, 0, r, 0, 0);
    m.imageSmoothingEnabled = false;
    m.drawImage(ambilCachePeta(4), 0, 0, lebar, tinggi);

    var sk = lebar / LEBAR_DUNIA;
    m.font = "700 11px Nunito, system-ui, sans-serif";
    m.textAlign = "center";

    for (var n = 0; n < URUTAN_ZONA.length; n++) {
      var kunci = URUTAN_ZONA[n];
      var o = objekZona(kunci);
      if (!o) continue;
      var x = o.x * TILE * sk, y = o.y * TILE * sk;

      m.fillStyle = "rgba(30,24,18,.35)";
      m.beginPath();
      m.arc(x, y + 2, 11, 0, Math.PI * 2);
      m.fill();
      m.fillStyle = ZONA[kunci].warna;
      m.strokeStyle = "#fffaf4";
      m.lineWidth = 2.5;
      m.beginPath();
      m.arc(x, y, 11, 0, Math.PI * 2);
      m.fill();
      m.stroke();

      m.fillStyle = "#fffaf4";
      m.textBaseline = "middle";
      if (dikunjungi[kunci]) {
        m.strokeStyle = "#fffaf4";
        m.lineWidth = 2.2;
        m.lineCap = "round";
        m.beginPath();
        m.moveTo(x - 4, y);
        m.lineTo(x - 1, y + 3.5);
        m.lineTo(x + 4.5, y - 3.5);
        m.stroke();
      } else {
        m.fillText(String(n + 1), x, y + 0.5);
      }

      var teks = ZONA[kunci].judul;
      m.font = "700 11px Nunito, system-ui, sans-serif";
      var w = m.measureText(teks).width + 12;
      m.fillStyle = "rgba(255,250,244,.94)";
      kotakBulatDi(m, x - w / 2, y + 14, w, 17, 8);
      m.fill();
      m.fillStyle = "#45392f";
      m.textBaseline = "middle";
      m.fillText(teks, x, y + 23);
    }

    // posisi pemain
    var px = pemain.x * sk, py = pemain.y * sk;
    m.fillStyle = "#2f3b2c";
    m.beginPath();
    m.arc(px, py, 8, 0, Math.PI * 2);
    m.fill();
    m.fillStyle = "#fffaf4";
    m.beginPath();
    m.arc(px, py, 5, 0, Math.PI * 2);
    m.fill();
    m.fillStyle = "rgba(255,250,244,.94)";
    var lw = m.measureText("Anda").width + 12;
    kotakBulatDi(m, px - lw / 2, py - 30, lw, 17, 8);
    m.fill();
    m.fillStyle = "#45392f";
    m.fillText("Anda", px, py - 21);
  }

  function kotakBulatDi(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

  function objekZona(kunci) {
    for (var i = 0; i < OBJEK.length; i++) if (OBJEK[i].zona === kunci) return OBJEK[i];
    return null;
  }

  if (el.petaBesar) {
    el.petaBesar.addEventListener("click", function (e) {
      var kotak = el.petaBesar.getBoundingClientRect();
      var sk = kotak.width / LEBAR_DUNIA;
      var mx = (e.clientX - kotak.left) / sk;
      var my = (e.clientY - kotak.top) / sk;
      var terdekat = null, jarakTerdekat = Infinity;
      for (var i = 0; i < URUTAN_ZONA.length; i++) {
        var o = objekZona(URUTAN_ZONA[i]);
        if (!o) continue;
        var jarak = Math.hypot(mx - o.x * TILE, my - o.y * TILE);
        if (jarak < jarakTerdekat) { jarakTerdekat = jarak; terdekat = o; }
      }
      if (terdekat && jarakTerdekat < 3 * TILE) pergiKe(terdekat.zona);
    });
  }

  function bangunDaftarLokasi() {
    if (!el.daftarLokasi) return;
    el.daftarLokasi.textContent = "";
    URUTAN_ZONA.forEach(function (kunci, i) {
      var z = ZONA[kunci];
      var tombolLokasi = document.createElement("button");
      tombolLokasi.type = "button";
      tombolLokasi.className = "lokasi";
      tombolLokasi.dataset.zona = kunci;
      tombolLokasi.style.setProperty("--warna-zona", z.warna);

      var nomor = document.createElement("span");
      nomor.className = "lokasi-nomor";
      nomor.textContent = dikunjungi[kunci] ? "✓" : String(i + 1);

      var isi = document.createElement("span");
      isi.className = "lokasi-isi";
      var judul = document.createElement("b");
      judul.textContent = z.judul;
      var ket = document.createElement("small");
      ket.textContent = z.ket;
      isi.append(judul, ket);

      var pergi = document.createElement("span");
      pergi.className = "lokasi-pergi";
      pergi.textContent = "Pergi";

      tombolLokasi.append(nomor, isi, pergi);
      tombolLokasi.addEventListener("click", function () { pergiKe(kunci); });
      el.daftarLokasi.appendChild(tombolLokasi);
    });
  }

  var sudahSelesaiSemua = false;

  function perbaruiKemajuan() {
    var jumlah = 0;
    for (var i = 0; i < URUTAN_ZONA.length; i++) if (dikunjungi[URUTAN_ZONA[i]]) jumlah++;
    if (el.kemajuan) el.kemajuan.textContent = jumlah + "/" + URUTAN_ZONA.length;
    if (jumlah === URUTAN_ZONA.length && !sudahSelesaiSemua) {
      sudahSelesaiSemua = true;
      beriTahu("Semua tempat sudah dikunjungi. Terima kasih!");
    }
  }

  /* =====================================================================
     Pemberitahuan singkat
     ===================================================================== */
  var waktuPemberitahuan = null;
  function beriTahu(teks) {
    if (!el.pemberitahuan) return;
    el.pemberitahuan.textContent = teks;
    el.pemberitahuan.classList.add("tampil");
    clearTimeout(waktuPemberitahuan);
    waktuPemberitahuan = setTimeout(function () {
      el.pemberitahuan.classList.remove("tampil");
    }, 2400);
  }

  /* =====================================================================
     Gelung utama
     ===================================================================== */
  var waktuSebelum = 0;
  var jumlahFrame = 0;
  var idAnimasi = null;
  var pakaiPewaktu = false;

  function gelung(waktu) {
    if (!berjalanTerus) return;
    var dt = Math.min((waktu - waktuSebelum) / 1000, 0.05) || 0;
    waktuSebelum = waktu;
    waktuTotal += dt;
    jumlahFrame++;
    if (!popupTerbuka()) perbarui(dt);
    gambarSemua();
    if (!pakaiPewaktu) idAnimasi = requestAnimationFrame(gelung);
  }

  /* Kita anggap halaman terlihat sampai peramban benar-benar memberi tahu
     sebaliknya. Sebagian webview melaporkan document.hidden = true terus,
     dan mempercayainya begitu saja akan membuat permainan membeku selamanya. */
  var halamanTerlihat = true;
  document.addEventListener("visibilitychange", function () {
    halamanTerlihat = !document.hidden;
  });

  /* Sebagian peramban di dalam aplikasi (WhatsApp, Instagram) tidak
     menjalankan requestAnimationFrame. Bila tidak ada satu frame pun setelah
     700 ms, pindah ke pewaktu biasa supaya permainan tidak membeku. */
  function pasangPengamanGelung() {
    setTimeout(function () {
      if (jumlahFrame > 0 || pakaiPewaktu || !berjalanTerus) return;
      pakaiPewaktu = true;
      if (idAnimasi !== null) cancelAnimationFrame(idAnimasi);
      setInterval(function () {
        if (halamanTerlihat) gelung(performance.now());
      }, 1000 / 30);
    }, 700);
  }

  /* =====================================================================
     Popup
     ===================================================================== */
  function popupTerbuka() { return !el.lapisPopup.hidden; }

  function bukaPopup(id) {
    var target = document.getElementById(id);
    if (!target) return;
    lepasAnalog();
    tombol = {}; hitungKetik();

    var kunci = id.replace("popup-", "");
    if (ZONA[kunci] && !dikunjungi[kunci]) {
      dikunjungi[kunci] = true;
      perbaruiKemajuan();
    }
    if (id === "popup-peta") { gambarPetaBesar(); bangunDaftarLokasi(); }

    Array.prototype.forEach.call(el.lapisPopup.querySelectorAll(".popup"), function (p) { p.hidden = true; });
    el.lapisPopup.hidden = false;
    target.hidden = false;
    target.scrollTop = 0;
    var fokus = target.querySelector(".tombol-tutup");
    if (fokus) fokus.focus({ preventScroll: true });
  }

  function tutupPopup() {
    if (!el.lightbox.hidden) { el.lightbox.hidden = true; return; }
    if (!popupTerbuka()) return;
    el.lapisPopup.hidden = true;
    Array.prototype.forEach.call(el.lapisPopup.querySelectorAll(".popup"), function (p) { p.hidden = true; });
  }

  el.lapisPopup.addEventListener("click", function (e) {
    if (e.target.closest("[data-tutup]")) tutupPopup();
    if (e.target.closest("[data-tutup-lightbox]")) el.lightbox.hidden = true;
  });

  el.tombolAksi.addEventListener("click", function () {
    if (zonaAktif) bukaPopup("popup-" + zonaAktif.zona);
  });
  el.tombolPeta.addEventListener("click", function () { bukaPopup("popup-peta"); });
  el.tombolPetunjuk.addEventListener("click", function () { bukaPopup("popup-petunjuk"); });
  if (el.bingkaiPetaMini) {
    el.bingkaiPetaMini.addEventListener("click", function () { bukaPopup("popup-peta"); });
  }

  /* =====================================================================
     Hitung mundur
     ===================================================================== */
  var wadahMundur = document.getElementById("hitung-mundur");
  if (wadahMundur) {
    var targetWaktu = new Date(wadahMundur.dataset.target).getTime();
    var kotakMundur = {};
    Array.prototype.forEach.call(wadahMundur.querySelectorAll("[data-satuan]"), function (b) {
      kotakMundur[b.dataset.satuan] = b;
    });
    var perbaruiMundur = function () {
      var sisa = Math.max(0, targetWaktu - Date.now());
      var detik = Math.floor(sisa / 1000);
      kotakMundur.hari.textContent = Math.floor(detik / 86400);
      kotakMundur.jam.textContent = Math.floor(detik / 3600) % 24;
      kotakMundur.menit.textContent = Math.floor(detik / 60) % 60;
      kotakMundur.detik.textContent = detik % 60;
    };
    perbaruiMundur();
    setInterval(perbaruiMundur, 1000);
  }

  /* =====================================================================
     Buku tamu
     ===================================================================== */
  var form = document.getElementById("form-ucapan");
  if (form) {
    var status = document.getElementById("status-ucapan");
    var daftar = document.getElementById("daftar-ucapan");
    var jumlahUcapan = document.getElementById("jumlah-ucapan");

    var buatKartuUcapan = function (u) {
      var art = document.createElement("article");
      art.className = "ucapan";
      var pNama = document.createElement("p");
      pNama.className = "nama";
      pNama.textContent = u.nama + " ";
      var lencana = document.createElement("span");
      lencana.className = "badge " + u.kode_kehadiran;
      lencana.textContent = u.kehadiran;
      pNama.appendChild(lencana);
      var pPesan = document.createElement("p");
      pPesan.className = "pesan";
      pPesan.textContent = u.pesan;
      var pWaktu = document.createElement("p");
      pWaktu.className = "waktu";
      pWaktu.textContent = u.waktu;
      art.append(pNama, pPesan, pWaktu);
      return art;
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var kirim = form.querySelector("button[type=submit]");
      var data = new FormData(form);
      kirim.disabled = true;
      status.textContent = "Mengirim…";
      status.className = "";

      fetch("/api/ucapan/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": data.get("csrfmiddlewaretoken")
        },
        body: JSON.stringify({
          nama: data.get("nama"),
          pesan: data.get("pesan"),
          kehadiran: data.get("kehadiran"),
          jumlah_orang: Number(data.get("jumlah_orang")) || 1,
          slug: DATA.slug
        })
      })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (hasil) {
          if (!hasil.ok || !hasil.j.ok) throw new Error(hasil.j.pesan || "Gagal mengirim.");
          status.textContent = "Terima kasih, ucapan Anda sudah terkirim.";
          status.className = "sukses";
          var kosong = document.getElementById("ucapan-kosong");
          if (kosong) kosong.remove();
          daftar.insertBefore(buatKartuUcapan(hasil.j.ucapan), daftar.firstChild);
          jumlahUcapan.textContent = daftar.querySelectorAll(".ucapan").length;
          form.querySelector("[name=pesan]").value = "";
        })
        .catch(function (err) {
          status.textContent = err.message || "Terjadi kesalahan jaringan.";
          status.className = "gagal";
        })
        .finally(function () { kirim.disabled = false; });
    });
  }

  /* =====================================================================
     Salin nomor rekening & lightbox galeri
     ===================================================================== */
  document.addEventListener("click", function (e) {
    var tombolSalin = e.target.closest("[data-salin]");
    if (tombolSalin) {
      var nomor = tombolSalin.dataset.salin;
      var selesai = function () {
        var teksAsli = tombolSalin.textContent;
        tombolSalin.textContent = "Tersalin!";
        setTimeout(function () { tombolSalin.textContent = teksAsli; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(nomor).then(selesai, function () {});
      } else {
        var bantu = document.createElement("textarea");
        bantu.value = nomor;
        document.body.appendChild(bantu);
        bantu.select();
        try { document.execCommand("copy"); selesai(); } catch (err) { /* diabaikan */ }
        bantu.remove();
      }
      return;
    }
    var foto = e.target.closest("[data-perbesar]");
    if (foto) {
      el.lightbox.querySelector("img").src = foto.src;
      el.lightbox.querySelector("img").alt = foto.alt;
      el.lightbox.hidden = false;
    }
  });

  /* =====================================================================
     Musik
     ===================================================================== */
  var musikNyala = false;
  function setelMusik(nyala) {
    if (!el.musik) { el.tombolMusik.style.display = "none"; return; }
    musikNyala = nyala;
    el.tombolMusik.classList.toggle("mati", !nyala);
    if (nyala) { var p = el.musik.play(); if (p && p.catch) p.catch(function () {}); }
    else el.musik.pause();
  }
  el.tombolMusik.addEventListener("click", function () { setelMusik(!musikNyala); });

  /* =====================================================================
     Pemilihan karakter & tombol buka
     ===================================================================== */
  Array.prototype.forEach.call(document.querySelectorAll(".karakter-opsi"), function (opsi) {
    opsi.addEventListener("click", function () {
      Array.prototype.forEach.call(document.querySelectorAll(".karakter-opsi"), function (lain) {
        lain.classList.remove("dipilih");
        lain.setAttribute("aria-pressed", "false");
      });
      opsi.classList.add("dipilih");
      opsi.setAttribute("aria-pressed", "true");
      pemain.lembar = "karakter_" + opsi.dataset.karakter;
    });
  });

  el.tombolBuka.addEventListener("click", function () {
    el.sampul.classList.add("pergi");
    el.permainan.setAttribute("aria-hidden", "false");
    setelMusik(true);
    setTimeout(function () { el.sampul.style.display = "none"; }, 700);
    mulai();
    setTimeout(function () { beriTahu("Buka peta di kanan atas untuk melompat ke lokasi"); }, 1200);
  });

  /* =====================================================================
     Mulai
     ===================================================================== */
  var sudahMulai = false;
  function mulai() {
    if (sudahMulai) return;
    sudahMulai = true;
    berjalanTerus = true;
    waktuSebelum = performance.now();
    idAnimasi = requestAnimationFrame(gelung);
    pasangPengamanGelung();
  }

  window.addEventListener("resize", aturUkuran);
  window.addEventListener("orientationchange", function () { setTimeout(aturUkuran, 250); });

  siapkanKotakObjek();
  aturUkuran();
  perbaruiKemajuan();
  bangunDaftarLokasi();
  muatAset().then(function () {
    aturUkuran();
    el.memuat.classList.add("pergi");
    perbaruiKamera();
    gambarSemua();
  });
})();
