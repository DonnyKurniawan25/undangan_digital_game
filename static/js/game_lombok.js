/* =========================================================================
   Tema 2 — Pantai Lombok Beach Wedding
   Mesin permainan 2D top-down untuk tema pernikahan pantai Sasak Lombok.
   ========================================================================= */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("data-undangan").textContent);
  var TILE = 32;                 // ukuran satu petak dalam piksel dunia
  var LAJU = 96;                 // kecepatan jalan (piksel per detik)
  var DURASI_FRAME = 0.135;      // lama satu frame animasi jalan

  /* ---------------------------------------------------------------------
     Peta Pantai Sasak Lombok. Satu huruf = satu petak.
       ~  air laut pantai (padat)
       k  karang pesisir  (padat)
       b  tembok bata merah Candi Bentar (padat)
       _  pasir basah tepi pantai
       .  pasir putih halus
       ,  pasir berkerang
       -  jalan batu karang / coral pathway
       w  panggung kayu
       =  karpet tenun songket
       r  rumput pantai
     --------------------------------------------------------------------- */
  var PETA = [
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",
    "~~~~~~________________________~~~~~~",
    "~~~~..wwwwwwwwwwwwwwwwwwwwwwww..~~~~",
    "~~~...wwwwwwwwwwwwwwwwwwwwwwww...~~~",
    "~~~...wwwwwwwwwwwwwwwwwwwwwwww...~~~",
    "~~~...wwwwwwwwwwwwwwwwwwwwwwww...~~~",
    "~~....wwwwwwwww====wwwwwwwwwww....~~",
    "~~....,........====..........,....~~",
    "~~.............====...............~~",
    "~~...r.........====.........r.....~~",
    "~~..rrr........====........rrr....~~",
    "~~..rrr........====........rrr....~~",
    "~~.............====...............~~",
    "~~....,........====..........,....~~",
    "~~....---------====---------......~~",
    "~~....---------====---------......~~",
    "~~.............====...............~~",
    "~~.............====...............~~",
    "~~...r.........====.........r.....~~",
    "~~..rrr........====........rrr....~~",
    "~~.............====...............~~",
    "~~....,........====..........,....~~",
    "~~.............====...............~~",
    "~~.............====...............~~",
    "~~....,........====..........,....~~",
    "~~.............====...............~~",
    "bbbbbbbbbbbbbbb====bbbbbbbbbbbbbbbbb",
    "bbbbbbbbbbbbbbb====bbbbbbbbbbbbbbbbb",
    "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  ];

  var INDEKS_TILE = {
    ".": 0, ",": 1, "_": 2, "-": 3, "w": 4, "=": 5,
    "~": 6, "b": 9, "r": 10, "k": 11
  };
  var VARIAN_PASIR = [0, 1];
  var FRAME_AIR = [6, 7, 8];
  var PADAT = { "~": true, "k": true, "b": true };
  var PASIR = { ".": true, ",": true, "_": true };
  var BUTUH_TEPI = { "-": true, "w": true, "=": true, "~": true, "r": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * TILE;
  var TINGGI_DUNIA = TINGGI_PETA * TILE;

  var WARNA_PETAK = {
    "~": "#40c4ba", "k": "#78747e", "b": "#b04430",
    "_": "#c2a87e", ".": "#f2deb2", ",": "#fceec4",
    "-": "#e8d0ba", "w": "#a87a4e", "=": "#a82636", "r": "#80b266"
  };

  /* ---------------------------------------------------------------------
     Objek di peta Tema 2: Pantai Lombok
     --------------------------------------------------------------------- */
  var OBJEK = [
    // 1. Gerbang Candi Bentar (Pintu masuk di bawah)
    { gambar: "gerbang", x: 17.5, y: 28.5 },

    // 2. Pelaminan Bale Lumbung Sasak di bagian atas tengah
    { gambar: "pelaminan", x: 17.5, y: 6.8, padat: [5.2, 1.2], zona: "pengantin" },
    { gambar: "pengantin_pria",   x: 16.9, y: 7.2, padat: [0.55, 0.3] },
    { gambar: "pengantin_wanita", x: 18.1, y: 7.2, padat: [0.55, 0.3] },

    // 3. Bale Saji di kanan atas
    { gambar: "bale_saji", x: 26.5, y: 6.8, padat: [2.2, 1.0] },

    // 4. Titik Interaksi: Galeri, Buku Tamu, Papan Acara, Hadiah
    { gambar: "galeri",    x: 8.5,  y: 11.5, padat: [1.6, 0.6], zona: "galeri" },
    { gambar: "buku_tamu", x: 27.5, y: 11.5, padat: [1.3, 0.5], zona: "ucapan" },
    { gambar: "papan",     x: 10.5, y: 20.5, padat: [1.4, 0.5], zona: "acara" },
    { gambar: "hadiah",    x: 24.5, y: 20.5, padat: [1.3, 0.5], zona: "hadiah" },

    // 5. Penari Sasak & Pemain Gendang Beleq
    { gambar: "penari_sasak", x: 15.2, y: 13.6, padat: [0.6, 0.3] },
    { gambar: "penari_sasak", x: 19.8, y: 13.6, padat: [0.6, 0.3] },
    { gambar: "pemusik_gendang", x: 29.5, y: 15.5, padat: [1.4, 0.6] },
    { gambar: "pemusik_gendang", x: 6.5,  y: 15.5, padat: [1.4, 0.6] },

    // 6. Obor Bambu di sepanjang karpet & halaman
    { gambar: "obor_bambu", x: 15.2, y: 9.8,  padat: [0.4, 0.3] },
    { gambar: "obor_bambu", x: 19.8, y: 9.8,  padat: [0.4, 0.3] },
    { gambar: "obor_bambu", x: 15.2, y: 17.5, padat: [0.4, 0.3] },
    { gambar: "obor_bambu", x: 19.8, y: 17.5, padat: [0.4, 0.3] },
    { gambar: "obor_bambu", x: 15.2, y: 24.5, padat: [0.4, 0.3] },
    { gambar: "obor_bambu", x: 19.8, y: 24.5, padat: [0.4, 0.3] },

    // 7. Pohon Kelapa Pantai & Pohon Pandan Laut
    { gambar: "pohon_pandan", x: 4.8,  y: 6.8,  padat: [1.2, 0.5] },
    { gambar: "pohon_pandan", x: 31.2, y: 6.8,  padat: [1.2, 0.5] },
    { gambar: "pohon_kelapa", x: 3.5,  y: 12.8, padat: [0.9, 0.4] },
    { gambar: "pohon_kelapa", x: 32.5, y: 12.8, padat: [0.9, 0.4] },
    { gambar: "pohon_kelapa", x: 3.8,  y: 22.8, padat: [0.9, 0.4] },
    { gambar: "pohon_kelapa", x: 32.2, y: 22.8, padat: [0.9, 0.4] },

    // 8. Bangku Santai Rotan
    { gambar: "bangku", x: 6.5,  y: 9.5, padat: [1.4, 0.5] },
    { gambar: "bangku", x: 28.5, y: 9.5, padat: [1.4, 0.5] },

    // 9. Perahu Jukung Tradisional di atas laut
    { gambar: "perahu_jukung", x: 3.5,  y: 2.2 },
    { gambar: "perahu_jukung", x: 32.5, y: 2.2 }
  ];

  var ZONA = {
    pengantin: {
      judul: "Pelaminan Lumbung", aksi: "Lihat Mempelai", radius: 3.4,
      berdiri: [17, 9], warna: "#ab4430",
      ket: "Foto & biodata kedua mempelai Sasak"
    },
    galeri: {
      judul: "Galeri Pantai", aksi: "Buka Galeri", radius: 2.4,
      berdiri: [8, 12], warna: "#2ba8a8",
      ket: "Koleksi foto prewedding tepi pantai"
    },
    ucapan: {
      judul: "Buku Tamu Sasak", aksi: "Tulis Ucapan", radius: 2.4,
      berdiri: [27, 12], warna: "#c48832",
      ket: "Kirim doa restu & konfirmasi kehadiran"
    },
    acara: {
      judul: "Papan Acara", aksi: "Baca Acara", radius: 2.4,
      berdiri: [10, 21], warna: "#9c2838",
      ket: "Waktu, lokasi pantai, dan hitung mundur"
    },
    hadiah: {
      judul: "Amplop Digital", aksi: "Kirim Hadiah", radius: 2.4,
      berdiri: [24, 21], warna: "#a85478",
      ket: "Nomor rekening & QRIS"
    }
  };
  var URUTAN_ZONA = ["pengantin", "galeri", "acara", "ucapan", "hadiah"];

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
    x: 17.5 * TILE,
    y: 26.0 * TILE,
    arah: 3,              // 0 bawah, 1 kiri, 2 kanan, 3 atas
    frame: 0,
    waktuFrame: 0,
    berjalan: false,
    lembar: "karakter_pria"
  };
  var LEBAR_SPRITE = 48, TINGGI_SPRITE = 80;
  var KOTAK = { w: 22, h: 14, offsetY: -10 };

  var kamera = { x: 0, y: 0, diinisialisasi: false };
  var skala = 2, dpr = 1, lebarCss = 0, tinggiCss = 0;
  var zonaAktif = null;
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

    // Zoom Stardew Valley: luas pandang ideal dari atas (~14 petak mendatar, ~11 petak menurun)
    skala = Math.max(lebarCss / (14.0 * TILE), tinggiCss / (11.0 * TILE));
    skala = Math.max(1.5, Math.min(3.2, skala));
    ctx.imageSmoothingEnabled = false;

    gradasiVignet = ctx.createRadialGradient(
      lebarCss / 2, tinggiCss / 2, Math.min(lebarCss, tinggiCss) * 0.36,
      lebarCss / 2, tinggiCss / 2, Math.max(lebarCss, tinggiCss) * 0.78
    );
    gradasiVignet.addColorStop(0, "rgba(235, 120, 60, 0)");
    gradasiVignet.addColorStop(1, "rgba(24, 18, 28, 0.32)");

    siapkanPartikelPantai();
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
     Pencarian jalur (BFS pada petak)
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
     Masukan: keyboard + analog sentuh
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
    try { el.analog.setPointerCapture(e.pointerId); } catch (err) { /* noop */ }
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
    perbaruiPartikelPantai(dt);
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
      el.lokasi.textContent = "Pantai Sasak Lombok";
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
     Partikel Kelopak Bunga Kamboja & Kilau Pantai
     ===================================================================== */
  var WARNA_PARTIKEL = ["rgba(255,255,240,.9)", "rgba(255,210,120,.85)", "rgba(248,180,196,.8)", "rgba(100,230,220,.7)"];

  function siapkanPartikelPantai() {
    var jumlah = Math.round(Math.min(24, Math.max(10, lebarCss / 45)));
    kelopak = [];
    for (var i = 0; i < jumlah; i++) {
      kelopak.push({
        x: Math.random() * lebarCss,
        y: Math.random() * tinggiCss,
        lajuX: 12 + Math.random() * 18,
        lajuY: 14 + Math.random() * 20,
        ukuran: 3 + Math.random() * 3,
        fase: Math.random() * Math.PI * 2,
        putar: Math.random() * Math.PI,
        warna: WARNA_PARTIKEL[i % WARNA_PARTIKEL.length]
      });
    }
  }

  function perbaruiPartikelPantai(dt) {
    for (var i = 0; i < kelopak.length; i++) {
      var k = kelopak[i];
      k.fase += dt * 1.8;
      k.x += (k.lajuX + Math.sin(k.fase) * 14) * dt;
      k.y += k.lajuY * dt;
      k.putar += dt * 1.2;
      if (k.y > tinggiCss + 12) { k.y = -12; k.x = Math.random() * lebarCss; }
      if (k.x > lebarCss + 12) { k.x = -12; k.y = Math.random() * tinggiCss; }
    }
  }

  function gambarPartikelPantai() {
    for (var i = 0; i < kelopak.length; i++) {
      var k = kelopak[i];
      ctx.save();
      ctx.translate(k.x, k.y);
      ctx.rotate(k.putar);
      ctx.fillStyle = k.warna;
      ctx.beginPath();
      ctx.ellipse(0, 0, k.ukuran, k.ukuran * 0.6, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  /* =====================================================================
     Menggambar dunia pantai
     ===================================================================== */
  function acak(x, y) {
    var n = (x * 73856093) ^ (y * 19349663);
    n = (n ^ (n >>> 13)) >>> 0;
    return (n % 997) / 997;
  }

  function indeksTile(huruf, x, y) {
    if (huruf === ".") {
      var r = acak(x, y);
      if (r < 0.08) return INDEKS_TILE[","];
      return 0;
    }
    if (huruf === "~") return FRAME_AIR[Math.floor(waktuTotal * 2.2 + x * 0.4 + y * 0.7) % 3];
    return INDEKS_TILE[huruf] !== undefined ? INDEKS_TILE[huruf] : 0;
  }

  function adaPasir(x, y) {
    if (x < 0 || y < 0 || x >= LEBAR_PETA || y >= TINGGI_PETA) return false;
    return !!PASIR[PETA[y][x]];
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

        if (!BUTUH_TEPI[huruf]) continue;
        if (adaPasir(x, y - 1)) gambarTepi(TEPI.atas, x, y);
        if (adaPasir(x, y + 1)) gambarTepi(TEPI.bawah, x, y);
        if (adaPasir(x - 1, y)) gambarTepi(TEPI.kiri, x, y);
        if (adaPasir(x + 1, y)) gambarTepi(TEPI.kanan, x, y);
        if (!adaPasir(x, y - 1) && !adaPasir(x - 1, y) && adaPasir(x - 1, y - 1)) gambarTepi(TEPI.kiri_atas, x, y);
        if (!adaPasir(x, y - 1) && !adaPasir(x + 1, y) && adaPasir(x + 1, y - 1)) gambarTepi(TEPI.kanan_atas, x, y);
        if (!adaPasir(x, y + 1) && !adaPasir(x - 1, y) && adaPasir(x - 1, y + 1)) gambarTepi(TEPI.kiri_bawah, x, y);
        if (!adaPasir(x, y + 1) && !adaPasir(x + 1, y) && adaPasir(x + 1, y + 1)) gambarTepi(TEPI.kanan_bawah, x, y);
      }
    }
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
     Lapisan layar: papan nama, panah arah, vignet
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

    // ekor
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
      ctx.strokeStyle = aktif ? "#fffaf4" : "#2ba8a8";
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
      if (sx >= batasKiri && sx <= batasKanan && sy >= batasAtas && sy <= batasBawah) continue;

      var dx = sx - pusatX, dy = sy - pusatY;
      var tMin = Infinity;
      if (dx > 0) tMin = Math.min(tMin, (batasKanan - pusatX) / dx);
      if (dx < 0) tMin = Math.min(tMin, (batasKiri - pusatX) / dx);
      if (dy > 0) tMin = Math.min(tMin, (batasBawah - pusatY) / dy);
      if (dy < 0) tMin = Math.min(tMin, (batasAtas - pusatY) / dy);

      var px = pusatX + dx * tMin;
      var py = pusatY + dy * tMin;
      var sudut = Math.atan2(dy, dx);
      var denyut = 1 + Math.sin(waktuTotal * 4 + i) * 0.12;

      ctx.save();
      ctx.translate(px, py);
      ctx.scale(denyut, denyut);
      ctx.rotate(sudut);
      ctx.fillStyle = ZONA[o.zona].warna;
      ctx.beginPath();
      ctx.moveTo(10, 0);
      ctx.lineTo(-8, -7);
      ctx.lineTo(-4, 0);
      ctx.lineTo(-8, 7);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }
  }

  /* =====================================================================
     Loop utama render
     ===================================================================== */
  var waktuLalu = 0;

  function render(waktu) {
    if (!waktuLalu) waktuLalu = waktu;
    var dt = Math.min((waktu - waktuLalu) / 1000, 0.1);
    waktuLalu = waktu;
    waktuTotal += dt;

    perbarui(dt);

    ctx.save();
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, lebarCss, tinggiCss);

    ctx.save();
    ctx.scale(skala, skala);
    ctx.translate(-kamera.x, -kamera.y);

    gambarPeta();

    // Urutkan objek & pemain berdasarkan sumbu Y untuk depth sorting
    var urut = OBJEK.slice();
    urut.push({ pemain: true, y: pemain.y / TILE });
    urut.sort(function (a, b) { return a.y - b.y; });

    for (var i = 0; i < urut.length; i++) {
      var item = urut[i];
      if (item.pemain) {
        gambarPemain();
      } else {
        if (item.zona && zonaAktif === item) gambarCincinAktif(item);
        gambarObjek(item);
      }
    }

    ctx.restore();

    for (var j = 0; j < OBJEK.length; j++) {
      if (OBJEK[j].zona) gambarPapanNama(OBJEK[j]);
    }
    gambarPanahArah();
    gambarPartikelPantai();

    if (gradasiVignet) {
      ctx.fillStyle = gradasiVignet;
      ctx.fillRect(0, 0, lebarCss, tinggiCss);
    }

    ctx.restore();

    gambarPetaMini();
    requestAnimationFrame(render);
  }

  /* =====================================================================
     Minimap & Peta Besar
     ===================================================================== */
  var ctxPetaMini = el.petaMini.getContext("2d");
  var ctxPetaBesar = el.petaBesar ? el.petaBesar.getContext("2d") : null;

  function aturUkuranPetaMini() {
    var pmini = 72;
    el.petaMini.width = pmini;
    el.petaMini.height = Math.round(pmini * (TINGGI_PETA / LEBAR_PETA));
  }

  function gambarPetaMini() {
    var w = el.petaMini.width, h = el.petaMini.height;
    ctxPetaMini.clearRect(0, 0, w, h);
    var tw = w / LEBAR_PETA, th = h / TINGGI_PETA;

    for (var y = 0; y < TINGGI_PETA; y++) {
      for (var x = 0; x < LEBAR_PETA; x++) {
        var huruf = PETA[y][x];
        ctxPetaMini.fillStyle = WARNA_PETAK[huruf] || "#f2deb2";
        ctxPetaMini.fillRect(x * tw, y * th, tw + 0.5, th + 0.5);
      }
    }

    // Gambar titik zona
    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona) continue;
      ctxPetaMini.fillStyle = dikunjungi[o.zona] ? "#2ba8a8" : ZONA[o.zona].warna;
      ctxPetaMini.beginPath();
      ctxPetaMini.arc(o.x * tw, o.y * th, 2.8, 0, Math.PI * 2);
      ctxPetaMini.fill();
    }

    // Titik posisi pemain
    ctxPetaMini.fillStyle = "#fff";
    ctxPetaMini.strokeStyle = "#45392f";
    ctxPetaMini.lineWidth = 1;
    ctxPetaMini.beginPath();
    ctxPetaMini.arc((pemain.x / TILE) * tw, (pemain.y / TILE) * th, 3.2, 0, Math.PI * 2);
    ctxPetaMini.fill();
    ctxPetaMini.stroke();
  }

  function perbaruiKemajuan() {
    var total = URUTAN_ZONA.length;
    var sudah = Object.keys(dikunjungi).length;
    if (el.kemajuan) el.kemajuan.textContent = sudah + "/" + total;
  }

  function gambarPetaBesar() {
    if (!el.petaBesar || !ctxPetaBesar) return;
    var w = 320, h = Math.round(320 * (TINGGI_PETA / LEBAR_PETA));
    el.petaBesar.width = w;
    el.petaBesar.height = h;
    var tw = w / LEBAR_PETA, th = h / TINGGI_PETA;

    for (var y = 0; y < TINGGI_PETA; y++) {
      for (var x = 0; x < LEBAR_PETA; x++) {
        var huruf = PETA[y][x];
        ctxPetaBesar.fillStyle = WARNA_PETAK[huruf] || "#f2deb2";
        ctxPetaBesar.fillRect(x * tw, y * th, tw + 0.5, th + 0.5);
      }
    }

    // Garis jalan
    for (var i = 0; i < URUTAN_ZONA.length; i++) {
      var z = ZONA[URUTAN_ZONA[i]];
      var obj = OBJEK.find(function (o) { return o.zona === URUTAN_ZONA[i]; });
      if (!obj) continue;
      ctxPetaBesar.fillStyle = z.warna;
      ctxPetaBesar.beginPath();
      ctxPetaBesar.arc(obj.x * tw, obj.y * th, 7, 0, Math.PI * 2);
      ctxPetaBesar.fill();

      ctxPetaBesar.fillStyle = "#fff";
      ctxPetaBesar.font = "bold 9px sans-serif";
      ctxPetaBesar.textAlign = "center";
      ctxPetaBesar.textBaseline = "middle";
      ctxPetaBesar.fillText(i + 1, obj.x * tw, obj.y * th);
    }

    // Posisi pemain
    ctxPetaBesar.fillStyle = "#fff";
    ctxPetaBesar.strokeStyle = "#000";
    ctxPetaBesar.lineWidth = 2;
    ctxPetaBesar.beginPath();
    ctxPetaBesar.arc((pemain.x / TILE) * tw, (pemain.y / TILE) * th, 5.5, 0, Math.PI * 2);
    ctxPetaBesar.fill();
    ctxPetaBesar.stroke();
  }

  function isiDaftarLokasi() {
    if (!el.daftarLokasi) return;
    el.daftarLokasi.innerHTML = "";
    URUTAN_ZONA.forEach(function (kunci, idx) {
      var z = ZONA[kunci];
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "lokasi";
      btn.style.setProperty("--warna-zona", z.warna);
      btn.innerHTML = '<span class="lokasi-nomor">' + (idx + 1) + '</span>' +
                      '<div class="lokasi-isi"><b>' + z.judul + '</b><small>' + z.ket + '</small></div>' +
                      '<span class="lokasi-pergi">Pergi</span>';
      btn.addEventListener("click", function () { pergiKe(kunci); });
      el.daftarLokasi.appendChild(btn);
    });
  }

  /* =====================================================================
     Popup & UI Interaktif
     ===================================================================== */
  function popupTerbuka() {
    return el.lapisPopup && !el.lapisPopup.hidden;
  }

  function bukaPopup(id) {
    if (!el.lapisPopup) return;
    var semua = el.lapisPopup.querySelectorAll(".popup");
    semua.forEach(function (p) { p.hidden = true; });
    var target = document.getElementById(id);
    if (!target) return;
    target.hidden = false;
    el.lapisPopup.hidden = false;

    var kunci = id.replace("popup-", "");
    if (ZONA[kunci]) {
      dikunjungi[kunci] = true;
      perbaruiKemajuan();
    }
    if (id === "popup-peta") {
      gambarPetaBesar();
      isiDaftarLokasi();
    }
  }

  function tutupPopup() {
    if (el.lapisPopup) el.lapisPopup.hidden = true;
  }

  function beriTahu(pesan) {
    if (!el.pemberitahuan) return;
    el.pemberitahuan.textContent = pesan;
    el.pemberitahuan.classList.add("tampil");
    setTimeout(function () {
      el.pemberitahuan.classList.remove("tampil");
    }, 2400);
  }

  /* =====================================================================
     Buku Tamu / Form Ucapan AJAX
     ===================================================================== */
  function initFormUcapan() {
    var form = document.getElementById("form-ucapan");
    if (!form) return;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var payload = {
        nama: fd.get("nama"),
        pesan: fd.get("pesan"),
        kehadiran: fd.get("kehadiran"),
        jumlah_orang: fd.get("jumlah_orang"),
        slug: DATA.slug || ""
      };
      var status = document.getElementById("status-ucapan");
      if (status) status.textContent = "Mengirim…";

      fetch("/api/ucapan/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": (form.querySelector("[name=csrfmiddlewaretoken]") || {}).value || ""
        },
        body: JSON.stringify(payload)
      })
      .then(function (res) { return res.json(); })
      .then(function (res) {
        if (res.ok) {
          if (status) {
            status.textContent = "Ucapan berhasil dikirim! Terima kasih.";
            status.className = "sukses";
          }
          form.reset();
          muatUlangUcapan();
        } else {
          if (status) {
            status.textContent = res.pesan || "Gagal mengirim ucapan.";
            status.className = "gagal";
          }
        }
      })
      .catch(function () {
        if (status) {
          status.textContent = "Terjadi kesalahan jaringan.";
          status.className = "gagal";
        }
      });
    });
  }

  function muatUlangUcapan() {
    fetch("/api/ucapan/")
      .then(function (res) { return res.json(); })
      .then(function (res) {
        var daftar = document.getElementById("daftar-ucapan");
        var jumlah = document.getElementById("jumlah-ucapan");
        if (!daftar || !res.ucapan) return;
        if (jumlah) jumlah.textContent = res.ucapan.length;
        daftar.innerHTML = "";
        res.ucapan.forEach(function (u) {
          var art = document.createElement("article");
          art.className = "ucapan";
          art.innerHTML = '<p class="nama">' + u.nama + ' <span class="badge ' + u.kode_kehadiran + '">' + u.kehadiran + '</span></p>' +
                          '<p class="pesan">' + u.pesan.replace(/\n/g, "<br>") + '</p>' +
                          '<p class="waktu">' + u.waktu + '</p>';
          daftar.appendChild(art);
        });
      });
  }

  /* =====================================================================
     Hitung Mundur Acara
     ===================================================================== */
  function initHitungMundur() {
    var hm = document.getElementById("hitung-mundur");
    if (!hm) return;
    var target = new Date(hm.getAttribute("data-target")).getTime();
    if (isNaN(target)) return;

    function hitung() {
      var sekarang = new Date().getTime();
      var sisa = Math.max(0, target - sekarang);
      var hari = Math.floor(sisa / (1000 * 60 * 60 * 24));
      var jam = Math.floor((sisa % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      var menit = Math.floor((sisa % (1000 * 60 * 60)) / (1000 * 60));
      var detik = Math.floor((sisa % (1000 * 60)) / 1000);

      var elHari = hm.querySelector('[data-satuan="hari"]');
      var elJam = hm.querySelector('[data-satuan="jam"]');
      var elMenit = hm.querySelector('[data-satuan="menit"]');
      var elDetik = hm.querySelector('[data-satuan="detik"]');
      if (elHari) elHari.textContent = hari;
      if (elJam) elJam.textContent = jam;
      if (elMenit) elMenit.textContent = menit;
      if (elDetik) elDetik.textContent = detik;
    }
    hitung();
    setInterval(hitung, 1000);
  }

  /* =====================================================================
     Tombol Salin Nomor Rekening
     ===================================================================== */
  function initSalinRekening() {
    document.querySelectorAll("[data-salin]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var rek = btn.getAttribute("data-salin");
        if (navigator.clipboard) {
          navigator.clipboard.writeText(rek).then(function () {
            btn.textContent = "Tersalin!";
            setTimeout(function () { btn.textContent = "Salin nomor"; }, 2000);
          });
        }
      });
    });
  }

  /* =====================================================================
     Lightbox Galeri
     ===================================================================== */
  function initLightbox() {
    document.querySelectorAll("[data-perbesar]").forEach(function (img) {
      img.addEventListener("click", function () {
        if (!el.lightbox) return;
        var t = el.lightbox.querySelector("img");
        if (t) t.src = img.src;
        el.lightbox.hidden = false;
      });
    });
    if (el.lightbox) {
      el.lightbox.addEventListener("click", function () {
        el.lightbox.hidden = true;
      });
    }
  }

  /* =====================================================================
     Inisialisasi Permainan
     ===================================================================== */
  function mulai() {
    siapkanKotakObjek();
    aturUkuran();
    window.addEventListener("resize", aturUkuran);

    // Pemilih karakter di layar sampul
    document.querySelectorAll(".karakter-opsi").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".karakter-opsi").forEach(function (b) {
          b.classList.remove("dipilih");
          b.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("dipilih");
        btn.setAttribute("aria-pressed", "true");
        pemain.lembar = "karakter_" + btn.getAttribute("data-karakter");
      });
    });

    // Tombol Buka Undangan
    if (el.tombolBuka) {
      el.tombolBuka.addEventListener("click", function () {
        if (el.sampul) el.sampul.classList.add("pergi");
        if (el.permainan) el.permainan.removeAttribute("aria-hidden");
        if (el.musik) {
          el.musik.play().catch(function () { /* autoplay policy */ });
        }
      });
    }

    // Tombol Aksi
    if (el.tombolAksi) {
      el.tombolAksi.addEventListener("click", function () {
        if (zonaAktif) bukaPopup("popup-" + zonaAktif.zona);
      });
    }

    // Tombol HUD
    if (el.tombolPeta) el.tombolPeta.addEventListener("click", function () { bukaPopup("popup-peta"); });
    if (el.bingkaiPetaMini) el.bingkaiPetaMini.addEventListener("click", function () { bukaPopup("popup-peta"); });
    if (el.tombolPetunjuk) el.tombolPetunjuk.addEventListener("click", function () { bukaPopup("popup-petunjuk"); });
    if (el.tombolMusik && el.musik) {
      el.tombolMusik.addEventListener("click", function () {
        if (el.musik.paused) {
          el.musik.play();
          el.tombolMusik.classList.remove("mati");
        } else {
          el.musik.pause();
          el.tombolMusik.classList.add("mati");
        }
      });
    }

    // Tombol Tutup Popup
    document.querySelectorAll("[data-tutup]").forEach(function (btn) {
      btn.addEventListener("click", tutupPopup);
    });

    initFormUcapan();
    initHitungMundur();
    initSalinRekening();
    initLightbox();

    muatAset().then(function () {
      if (el.memuat) el.memuat.classList.add("pergi");
      requestAnimationFrame(render);
    });
  }

  document.addEventListener("DOMContentLoaded", mulai);
})();
