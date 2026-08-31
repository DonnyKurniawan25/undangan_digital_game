/* =========================================================================
   Tema "Taman Tropis" — mesin permainan tampak atas.
   Petak persegi 48x48, kamera lurus dari atas seperti Stardew Valley:
       sx = tx * 48        sy = ty * 48
   Objek diurutkan menurut sumbu y saja, sehingga yang lebih ke bawah layar
   menutupi yang di belakangnya.
   ========================================================================= */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("data-undangan").textContent);
  var PETAK = 48;                // sisi petak di layar
  var LAJU = 3.1;                // petak per detik
  var DURASI_FRAME = 0.135;

  /* ---------------------------------------------------------------------
     Denah. PETA[ty][tx] — satu huruf per petak.
       #  rimba (tak bisa dilewati)   ~  kolam (tak bisa dilewati)
       f  bedeng bunga (tak bisa dilewati)
       .  rumput   ,  rumput berbunga   b  jalan batu
       t  bibir kolam   w  panggung kayu   p  tanah
     --------------------------------------------------------------------- */
  var PETA = [
    "##########################",
    "#........................#",
    "#..,.....b......wwwww....#",
    "#........b......wwwww....#",
    "#........b......wwwww....#",
    "#..ttttt.b......wwwww....#",
    "#..t~~~t.b........b......#",
    "#..t~~~t.b........b......#",
    "#..t~~~t.bbbbbbbbbb......#",
    "#..t~~~t.b........b......#",
    "#..ttttt.b........b......#",
    "#........b........b......#",
    "#..,.....b........b...,..#",
    "#........b........b......#",
    "#........b........b......#",
    "#..f.....b........b......#",
    "#........b........b......#",
    "#........b........b......#",
    "#........b........b......#",
    "#..bbbbbbbbbbbbbbbb......#",
    "#........b........b......#",
    "#........b........b......#",
    "#..,.....b........b...,..#",
    "#........bbbbbbbbbb......#",
    "#........................#",
    "##########################"
  ];

  // Urutan WAJIB sama dengan URUTAN_PETAK di tools/buat_aset_tropis.py
  var INDEKS_PETAK = {
    ".": 0, ",": 3, "b": 4, "w": 5, "p": 6, "~": 7, "t": 10, "f": 11, "#": 12
  };
  var PETAK_RIMBA = 12;
  var VARIAN_RUMPUT = [0, 1, 2];
  var FRAME_AIR = [7, 8, 9];
  var PADAT = { "#": true, "~": true, "f": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * PETAK;
  var TINGGI_DUNIA = TINGGI_PETA * PETAK;

  var WARNA_PETAK = {
    "#": "#2f6b30", "~": "#4aaad0", ".": "#60aa44", ",": "#74be58",
    "b": "#98968c", "t": "#b0aea2", "w": "#a5763c", "f": "#8a5c3a", "p": "#926c4a"
  };

  /* ---------------------------------------------------------------------
     Objek. x/y dalam satuan petak (titik pijak). `padat` = [lebar, tinggi]
     kotak tabrakan dalam satuan petak, berpusat pada titik pijak.
     --------------------------------------------------------------------- */
  var OBJEK = [
    { gambar: "pelaminan", x: 18, y: 3.4, padat: [3.2, 1.4], zona: "pengantin", tinggiLabel: 1 },
    // Mempelai berdiri di depan pelaminan; y-nya sedikit lebih besar supaya
    // urutan kedalaman menempatkannya di depan latar.
    { gambar: "pengantin_pria", x: 17.4, y: 3.5, padat: [0.5, 0.3] },
    { gambar: "pengantin_wanita", x: 18.6, y: 3.5, padat: [0.5, 0.3] },
    { gambar: "gapura", x: 9, y: 20.2 },
    { gambar: "galeri", x: 10.6, y: 5, padat: [1, 0.8], zona: "galeri" },
    { gambar: "meja_tamu", x: 19.6, y: 12, padat: [1.2, 0.9], zona: "ucapan" },
    { gambar: "papan_acara", x: 7.5, y: 16, padat: [1, 0.8], zona: "acara" },
    { gambar: "kotak_angpao", x: 19.6, y: 21, padat: [0.9, 0.8], zona: "hadiah" },

    { gambar: "air_mancur", x: 5, y: 8, padat: [1.4, 1.2] },
    { gambar: "jembatan", x: 5, y: 11.6 },
    { gambar: "teratai", x: 4, y: 7 }, { gambar: "teratai", x: 6.2, y: 9.2 },
    { gambar: "teratai", x: 4.4, y: 9.6 }, { gambar: "teratai", x: 6, y: 6.6 },
    { gambar: "batu_besar", x: 2.4, y: 6.4, padat: [0.8, 0.7] },
    { gambar: "batu_besar", x: 7.6, y: 10.6, padat: [0.8, 0.7] },
    { gambar: "ember", x: 8.4, y: 6.6 },

    { gambar: "pagar_bambu", x: 2, y: 2 }, { gambar: "pagar_bambu", x: 3, y: 2 },
    { gambar: "pagar_bambu", x: 4, y: 2 }, { gambar: "pagar_bambu", x: 2, y: 3 },
    { gambar: "pagar_bambu", x: 2, y: 4 },

    { gambar: "rumpun_bunga", x: 3, y: 15 }, { gambar: "rumpun_bunga", x: 4, y: 15 },
    { gambar: "rumpun_bunga", x: 3.5, y: 15.6 },
    { gambar: "rumpun_bunga", x: 21.6, y: 12.4 }, { gambar: "rumpun_bunga", x: 21.6, y: 22.4 },
    { gambar: "rumpun_bunga", x: 3.4, y: 12.4 }, { gambar: "rumpun_bunga", x: 3.4, y: 22.4 }
  ];

  /* Umbul-umbul berjajar di sepanjang jalan utama. */
  var WARNA_UMBUL = ["umbul_merah", "umbul_kuning", "umbul_biru", "umbul_hijau"];
  (function pasangUmbul() {
    var n = 0;
    for (var ty = 3; ty <= 22; ty += 3) {
      OBJEK.push({ gambar: WARNA_UMBUL[n % 4], x: 8.1, y: ty, padat: [0.35, 0.35] });
      OBJEK.push({ gambar: WARNA_UMBUL[(n + 2) % 4], x: 9.9, y: ty, padat: [0.35, 0.35] });
      n++;
    }
    for (var ty2 = 7; ty2 <= 22; ty2 += 3) {
      OBJEK.push({ gambar: WARNA_UMBUL[(n + 1) % 4], x: 17.1, y: ty2, padat: [0.35, 0.35] });
      OBJEK.push({ gambar: WARNA_UMBUL[n % 4], x: 18.9, y: ty2, padat: [0.35, 0.35] });
      n++;
    }
    for (var tx = 11; tx <= 16; tx += 2) {
      OBJEK.push({ gambar: WARNA_UMBUL[n % 4], x: tx, y: 7.1, padat: [0.35, 0.35] });
      n++;
    }
  })();

  /* Rimba tropis: pohon dan semak rapat di sekeliling taman. */
  (function tanamRimba() {
    var jenis = ["palem", "pisang", "palem", "pakis", "semak_bunga", "palem", "pisang"];
    var n = 0;
    function tanam(x, y) {
      OBJEK.push({ gambar: jenis[n % jenis.length], x: x, y: y, padat: [0.7, 0.6] });
      n++;
    }
    for (var i = 1; i < TINGGI_PETA - 1; i++) {
      tanam(0.6, i); tanam(LEBAR_PETA - 1.6, i);
    }
    for (var j = 1; j < LEBAR_PETA - 1; j++) {
      tanam(j, 0.6); tanam(j, TINGGI_PETA - 1.6);
    }
    // rumpun di dalam taman
    var titik = [
      [13, 2], [15, 3], [12, 10], [14, 12], [15, 16], [13, 20], [12, 22],
      [22, 4], [23, 8], [22, 16], [23, 19], [6, 2], [2, 9], [2, 13],
      [6, 18], [4, 19], [6, 21], [22, 10], [15, 9], [11, 15], [11, 18]
    ];
    for (var k = 0; k < titik.length; k++) tanam(titik[k][0], titik[k][1]);
    // pakis kecil sebagai penutup tanah
    var kecil = [[11, 3], [14, 6], [12, 13], [16, 13], [11, 21], [21, 6],
                 [21, 14], [7, 14], [7, 18], [4, 16], [16, 20], [20, 17]];
    for (var m = 0; m < kecil.length; m++) {
      OBJEK.push({ gambar: m % 2 ? "pakis" : "semak_bunga", x: kecil[m][0], y: kecil[m][1], padat: [0.6, 0.5] });
    }
  })();

  var ZONA = {
    pengantin: { judul: "Pelaminan", aksi: "Lihat Mempelai", radius: 2.8, berdiri: [18, 5], warna: "#c9483f", ket: "Foto & biodata kedua mempelai" },
    galeri: { judul: "Galeri Foto", aksi: "Buka Galeri", radius: 2.1, berdiri: [9, 5], warna: "#3f8f5a", ket: "Kumpulan foto prewedding" },
    acara: { judul: "Papan Acara", aksi: "Baca Acara", radius: 2.1, berdiri: [8, 16], warna: "#3f74b0", ket: "Waktu, tempat, dan hitung mundur" },
    ucapan: { judul: "Buku Tamu", aksi: "Tulis Ucapan", radius: 2.1, berdiri: [18, 12], warna: "#b07a2a", ket: "Kirim doa & konfirmasi kehadiran" },
    hadiah: { judul: "Amplop Digital", aksi: "Kirim Hadiah", radius: 2.1, berdiri: [18, 21], warna: "#a4508c", ket: "Nomor rekening & QRIS" }
  };
  var URUTAN_ZONA = ["pengantin", "galeri", "acara", "ucapan", "hadiah"];

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
     Aset
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
     Keadaan
     ===================================================================== */
  var pemain = { x: 9, y: 21.6, arah: 3, frame: 0, waktuFrame: 0, berjalan: false, lembar: "karakter_pria" };
  var LEBAR_SPRITE = 48, TINGGI_SPRITE = 80;   // sprite Stardew Valley 48x80
  var KOTAK = 0.46;              // sisi kotak tabrakan pemain (petak)

  var kamera = { x: 0, y: 0 };
  var skala = 1, dpr = 1, lebarCss = 0, tinggiCss = 0;
  var berjalanTerus = false;
  var zonaAktif = null;
  var waktuTotal = 0;
  var dikunjungi = {};
  var objekTerurut = [];

  function layarX(tx) { return tx * PETAK; }
  function layarY(tx, ty) { return ty * PETAK; }

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
    // Sasaran: sekitar 11 petak melintang, 16 petak menurun.
    skala = Math.max(lebarCss / (11 * PETAK), tinggiCss / (16 * PETAK));
    skala = Math.max(0.7, Math.min(1.8, skala));
    ctx.imageSmoothingEnabled = false;
    aturUkuranPetaMini();
  }

  /* =====================================================================
     Tabrakan
     ===================================================================== */
  function petakPadat(tx, ty) {
    if (tx < 0 || ty < 0 || tx >= LEBAR_PETA || ty >= TINGGI_PETA) return true;
    return !!PADAT[PETA[ty][tx]];
  }

  var kotakObjek = [];
  function siapkanKotakObjek() {
    kotakObjek = OBJEK.filter(function (o) { return o.padat; }).map(function (o) {
      return {
        x0: o.x - o.padat[0] / 2, x1: o.x + o.padat[0] / 2,
        y0: o.y - o.padat[1] / 2, y1: o.y + o.padat[1] / 2
      };
    });
  }

  function bentrok(x, y, margin) {
    var s = KOTAK / 2 + (margin || 0);
    var kiri = x - s, kanan = x + s, atas = y - s, bawah = y + s;
    for (var ty = Math.floor(atas); ty <= Math.floor(bawah - 0.001); ty++) {
      for (var tx = Math.floor(kiri); tx <= Math.floor(kanan - 0.001); tx++) {
        if (petakPadat(tx, ty)) return true;
      }
    }
    for (var i = 0; i < kotakObjek.length; i++) {
      var k = kotakObjek[i];
      if (kiri < k.x1 && kanan > k.x0 && atas < k.y1 && bawah > k.y0) return true;
    }
    return false;
  }

  /* =====================================================================
     Pencarian jalur (BFS) untuk fitur "pergi ke lokasi"
     ===================================================================== */
  function bisaDipijak(tx, ty) {
    return !bentrok(tx + 0.5, ty + 0.5);
  }

  function petakTerdekatYangBisa(tx, ty) {
    if (bisaDipijak(tx, ty)) return { x: tx, y: ty };
    for (var jari = 1; jari <= 3; jari++) {
      for (var dy = -jari; dy <= jari; dy++) {
        for (var dx = -jari; dx <= jari; dx++) {
          if (bisaDipijak(tx + dx, ty + dy)) return { x: tx + dx, y: ty + dy };
        }
      }
    }
    return null;
  }

  /* Margin membuat garis potong menjaga jarak dari properti, sehingga
     langkah per sumbu tidak tersangkut di sudut kotak tabrakan. */
  var MARGIN_JALUR = 0.14;

  function garisBebas(a, b) {
    var jarak = Math.hypot(b.x - a.x, b.y - a.y);
    var langkah = Math.max(1, Math.ceil(jarak / 0.15));
    for (var i = 1; i <= langkah; i++) {
      var t = i / langkah;
      if (bentrok(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t, MARGIN_JALUR)) return false;
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

  function cariJalur(xAwal, yAwal, txTujuan, tyTujuan, tanpaHalus) {
    var awal = petakTerdekatYangBisa(Math.floor(xAwal), Math.floor(yAwal));
    var tujuan = petakTerdekatYangBisa(txTujuan, tyTujuan);
    if (!awal || !tujuan) return null;

    var dari = new Int32Array(LEBAR_PETA * TINGGI_PETA).fill(-1);
    var iAwal = awal.y * LEBAR_PETA + awal.x;
    var iTujuan = tujuan.y * LEBAR_PETA + tujuan.x;
    dari[iAwal] = iAwal;
    var antrian = [iAwal], kepala = 0;
    var geser = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    while (kepala < antrian.length) {
      var kini = antrian[kepala++];
      if (kini === iTujuan) break;
      var cx = kini % LEBAR_PETA, cy = (kini / LEBAR_PETA) | 0;
      for (var g = 0; g < 4; g++) {
        var nx = cx + geser[g][0], ny = cy + geser[g][1];
        if (nx < 0 || ny < 0 || nx >= LEBAR_PETA || ny >= TINGGI_PETA) continue;
        var idx = ny * LEBAR_PETA + nx;
        if (dari[idx] !== -1 || !bisaDipijak(nx, ny)) continue;
        dari[idx] = kini;
        antrian.push(idx);
      }
    }
    if (dari[iTujuan] === -1) return null;

    var mundur = [], jalan = iTujuan;
    while (jalan !== iAwal) {
      mundur.push({ x: (jalan % LEBAR_PETA) + 0.5, y: ((jalan / LEBAR_PETA) | 0) + 0.5 });
      jalan = dari[jalan];
    }
    mundur.push({ x: xAwal, y: yAwal });
    mundur.reverse();
    return (tanpaHalus ? mundur : haluskanJalur(mundur)).slice(1);
  }

  /* =====================================================================
     Jalan otomatis
     ===================================================================== */
  var jalurOtomatis = null, bukaSetelahSampai = null, sisaWaktuOtomatis = 0;
  var diamOtomatis = 0, percobaanUlang = 0;
  var posisiSebelum = { x: 0, y: 0 };

  function pergiKe(kunci) {
    var z = ZONA[kunci];
    if (!z) return;
    tutupPopup();
    var jalur = cariJalur(pemain.x, pemain.y, z.berdiri[0], z.berdiri[1]);
    if (!jalur || !jalur.length) {
      pemain.x = z.berdiri[0] + 0.5;
      pemain.y = z.berdiri[1] + 0.5;
      jalurOtomatis = null;
      perbaruiZona();
      bukaPopup("popup-" + kunci);
      return;
    }
    jalurOtomatis = jalur;
    bukaSetelahSampai = kunci;
    sisaWaktuOtomatis = 40;
    diamOtomatis = 0;
    percobaanUlang = 0;
    posisiSebelum.x = pemain.x;
    posisiSebelum.y = pemain.y;
    beriTahu("Menuju " + z.judul + "…");
  }

  function rencanakanUlang() {
    if (!bukaSetelahSampai) { batalkanOtomatis(); return; }
    var z = ZONA[bukaSetelahSampai];
    percobaanUlang++;
    if (percobaanUlang > 3) {
      // Sudah dicoba beberapa kali: antarkan langsung ke titik berdiri.
      pemain.x = z.berdiri[0] + 0.5;
      pemain.y = z.berdiri[1] + 0.5;
      selesaikanOtomatis();
      return;
    }
    var jalur = cariJalur(pemain.x, pemain.y, z.berdiri[0], z.berdiri[1], true);
    if (jalur && jalur.length) jalurOtomatis = jalur;
    else {
      pemain.x = z.berdiri[0] + 0.5;
      pemain.y = z.berdiri[1] + 0.5;
      selesaikanOtomatis();
    }
  }

  function batalkanOtomatis() { jalurOtomatis = null; bukaSetelahSampai = null; }

  /* =====================================================================
     Masukan: papan ketik + analog geser

     Analog memberi vektor menerus; pada tampak atas arah layar sama dengan
     arah petak, jadi vektornya dipakai apa adanya.
     ===================================================================== */
  var tombol = {};
  var arahKetik = { x: 0, y: 0 };
  var arahAnalog = { x: 0, y: 0 };
  var analogAktif = false;
  var idPointer = null;
  var pusatAnalog = { x: 0, y: 0 };
  var RADIUS_ANALOG = 48;

  var PETA_TOMBOL = {
    ArrowUp: "atas", KeyW: "atas", ArrowDown: "bawah", KeyS: "bawah",
    ArrowLeft: "kiri", KeyA: "kiri", ArrowRight: "kanan", KeyD: "kanan"
  };

  window.addEventListener("keydown", function (e) {
    if (e.code === "Escape") { tutupPopup(); return; }
    if (e.code === "KeyM" && !popupTerbuka()) { bukaPopup("popup-peta"); return; }
    if ((e.code === "Space" || e.code === "Enter" || e.code === "KeyE") && !popupTerbuka() && zonaAktif) {
      e.preventDefault();
      bukaPopup("popup-" + zonaAktif.zona);
      return;
    }
    if (PETA_TOMBOL[e.code]) { tombol[PETA_TOMBOL[e.code]] = true; e.preventDefault(); hitungArah(); }
  });
  window.addEventListener("keyup", function (e) {
    if (PETA_TOMBOL[e.code]) { tombol[PETA_TOMBOL[e.code]] = false; hitungArah(); }
  });
  window.addEventListener("blur", function () { tombol = {}; hitungArah(); lepasAnalog(); });

  function hitungArah() {
    arahKetik.x = (tombol.kanan ? 1 : 0) - (tombol.kiri ? 1 : 0);
    arahKetik.y = (tombol.bawah ? 1 : 0) - (tombol.atas ? 1 : 0);
    if (arahKetik.x || arahKetik.y) batalkanOtomatis();
  }

  function posisiAlas(x, y) {
    var kotak = el.analog.getBoundingClientRect();
    var batas = RADIUS_ANALOG + 20;
    x = Math.max(kotak.left + batas, Math.min(kotak.right - batas, x));
    y = Math.max(kotak.top + batas, Math.min(kotak.bottom - batas, y));
    pusatAnalog.x = x;
    pusatAnalog.y = y;
    el.alas.style.left = (x - kotak.left) + "px";
    el.alas.style.bottom = (kotak.bottom - y) + "px";
  }

  function gerakAnalog(x, y) {
    var dx = x - pusatAnalog.x;
    var dy = y - pusatAnalog.y;
    var jarak = Math.hypot(dx, dy);
    if (jarak > RADIUS_ANALOG) {
      dx = dx / jarak * RADIUS_ANALOG;
      dy = dy / jarak * RADIUS_ANALOG;
    }
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
    if (!el.analog) return;
    el.analog.classList.remove("aktif");
    el.knop.style.transform = "translate(0,0)";
    el.alas.style.left = "";
    el.alas.style.bottom = "";
  }

  if (el.analog) {
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
  }

  /* =====================================================================
     Pembaruan
     ===================================================================== */
  function perbarui(dt) {
    var sx = arahAnalog.x || arahKetik.x;
    var sy = arahAnalog.y || arahKetik.y;

    if (jalurOtomatis && jalurOtomatis.length) {
      sisaWaktuOtomatis -= dt;
      var tuj = jalurOtomatis[0];
      var dx = tuj.x - pemain.x, dy = tuj.y - pemain.y;
      var sisa = Math.hypot(dx, dy);
      if (sisa < 0.14) {
        jalurOtomatis.shift();
        if (!jalurOtomatis.length) selesaikanOtomatis();
      } else if (sisaWaktuOtomatis <= 0) {
        batalkanOtomatis();
      } else {
        // ubah arah petak menjadi arah layar supaya jalur & kendali sejalan
        sx = (dx - dy) / sisa;
        sy = (dx + dy) / sisa;
      }
    }

    var panjang = Math.hypot(sx, sy);
    pemain.berjalan = panjang > 0.01;
    if (pemain.berjalan) {
      // Besaran dorongan analog menentukan kecepatan; papan ketik dan jalan
      // otomatis selalu bernilai penuh setelah dibatasi ke 1.
      var kuat = Math.min(1, panjang);
      // Tampak atas: arah layar sama dengan arah petak.
      var gx = sx / panjang * LAJU * kuat * dt;
      var gy = sy / panjang * LAJU * kuat * dt;

      if (!bentrok(pemain.x + gx, pemain.y)) pemain.x += gx;
      if (!bentrok(pemain.x, pemain.y + gy)) pemain.y += gy;

      if (Math.abs(sx) > Math.abs(sy)) pemain.arah = sx > 0 ? 2 : 1;
      else pemain.arah = sy > 0 ? 0 : 3;

      pemain.waktuFrame += dt;
      if (pemain.waktuFrame >= DURASI_FRAME) {
        pemain.waktuFrame -= DURASI_FRAME;
        pemain.frame = (pemain.frame + 1) % 4;
      }
    } else {
      pemain.frame = 0;
      pemain.waktuFrame = 0;
    }

    if (jalurOtomatis) {
      var pindah = Math.hypot(pemain.x - posisiSebelum.x, pemain.y - posisiSebelum.y);
      diamOtomatis = pindah < LAJU * dt * 0.4 ? diamOtomatis + dt : 0;
      posisiSebelum.x = pemain.x;
      posisiSebelum.y = pemain.y;
      if (diamOtomatis > 0.35) { diamOtomatis = 0; rencanakanUlang(); }
    }

    perbaruiZona();
    perbaruiKamera();
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
      var jarak = Math.hypot(pemain.x - o.x, pemain.y - o.y);
      if (jarak < ZONA[o.zona].radius && jarak < jarakTerdekat) {
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
      el.lokasi.textContent = "Taman Tropis";
    }
  }

  function perbaruiKamera() {
    var lebarTampak = lebarCss / skala;
    var tinggiTampak = tinggiCss / skala;
    var px = layarX(pemain.x);
    var py = layarY(pemain.x, pemain.y);
    kamera.x = lebarTampak >= LEBAR_DUNIA
      ? (LEBAR_DUNIA - lebarTampak) / 2
      : Math.max(0, Math.min(LEBAR_DUNIA - lebarTampak, px - lebarTampak / 2));
    kamera.y = tinggiTampak >= TINGGI_DUNIA
      ? (TINGGI_DUNIA - tinggiTampak) / 2
      : Math.max(0, Math.min(TINGGI_DUNIA - tinggiTampak, py - tinggiTampak / 2));
  }

  /* =====================================================================
     Menggambar
     ===================================================================== */
  function acak(x, y) {
    var n = (x * 73856093) ^ (y * 19349663);
    n = (n ^ (n >>> 13)) >>> 0;
    return (n % 997) / 997;
  }

  function indeksPetak(huruf, tx, ty) {
    if (huruf === "#") return PETAK_RIMBA;
    if (huruf === ".") {
      var r = acak(tx, ty);
      if (r < 0.06) return INDEKS_PETAK[","];
      return VARIAN_RUMPUT[Math.floor(r * 1000) % 3];
    }
    if (huruf === "~") return FRAME_AIR[Math.floor(waktuTotal * 2 + tx * 0.5 + ty * 0.8) % 3];
    return INDEKS_PETAK[huruf] !== undefined ? INDEKS_PETAK[huruf] : 0;
  }

  function gambarPeta() {
    var lebarTampak = lebarCss / skala;
    var tinggiTampak = tinggiCss / skala;
    // Ditelusuri sedikit melebihi layar; di luar batas peta diisi rimba
    // supaya tidak ada sudut kosong.
    var x0 = Math.floor(kamera.x / PETAK) - 1;
    var x1 = Math.ceil((kamera.x + lebarTampak) / PETAK) + 1;
    var y0 = Math.floor(kamera.y / PETAK) - 1;
    var y1 = Math.ceil((kamera.y + tinggiTampak) / PETAK) + 1;

    for (var ty = y0; ty <= y1; ty++) {
      for (var tx = x0; tx <= x1; tx++) {
        var luar = tx < 0 || ty < 0 || tx >= LEBAR_PETA || ty >= TINGGI_PETA;
        var idx = luar ? PETAK_RIMBA : indeksPetak(PETA[ty][tx], tx, ty);
        ctx.drawImage(
          gambar.tileset, idx * PETAK, 0, PETAK, PETAK,
          tx * PETAK, ty * PETAK, PETAK, PETAK
        );
      }
    }
  }

  function gambarBayangan(px, py, lebar) {
    ctx.fillStyle = "rgba(28, 46, 24, .26)";
    ctx.beginPath();
    ctx.ellipse(px, py, lebar / 2, lebar / 4, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  function gambarCincinAktif(o) {
    var denyut = 0.5 + Math.sin(waktuTotal * 3) * 0.5;
    ctx.save();
    ctx.strokeStyle = ZONA[o.zona].warna;
    ctx.globalAlpha = 0.4 + denyut * 0.4;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(layarX(o.x), layarY(o.x, o.y), 30 + denyut * 8, 16 + denyut * 4, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  function gambarObjek(o) {
    var img = gambar[o.gambar];
    if (!img || !img.width) return;
    var px = layarX(o.x), py = layarY(o.x, o.y);
    var kiri = px - img.width / 2;
    var atas = py - img.height + 6;

    // Objek tinggi yang berada di depan pemain (y lebih besar) dibuat
    // tembus pandang bila kanopinya menutupi tubuh pemain, supaya karakter
    // tidak pernah hilang di balik pohon.
    var tembus = false;
    if (o.y > pemain.y && img.height > PETAK * 1.2) {
      var ppx = layarX(pemain.x);
      var ppy = layarY(pemain.x, pemain.y);
      tembus = ppx > kiri - 8 && ppx < kiri + img.width + 8 &&
               ppy > atas && ppy < py + 12;
    }
    if (tembus) ctx.globalAlpha = 0.42;
    gambarBayangan(px, py, Math.min(img.width * 0.6, 54));
    ctx.drawImage(img, Math.round(kiri), Math.round(atas));
    if (tembus) ctx.globalAlpha = 1;
  }

  function gambarPemain() {
    var lembar = gambar[pemain.lembar];
    if (!lembar || !lembar.width) return;
    var px = layarX(pemain.x), py = layarY(pemain.x, pemain.y);
    gambarBayangan(px, py, 24);
    ctx.drawImage(
      lembar, pemain.frame * LEBAR_SPRITE, pemain.arah * TINGGI_SPRITE, LEBAR_SPRITE, TINGGI_SPRITE,
      Math.round(px - LEBAR_SPRITE / 2), Math.round(py - TINGGI_SPRITE + 8), LEBAR_SPRITE, TINGGI_SPRITE
    );
  }

  /* -------- Balon "!" di atas objek yang bisa dibuka -------- */
  function gambarBalon(o) {
    var img = gambar[o.gambar];
    var tinggi = img && img.height ? img.height : 60;
    var sx = (layarX(o.x) - kamera.x) * skala;
    var sy = (layarY(o.x, o.y) - tinggi - 16 - (o.tinggiLabel ? 10 : 0) - kamera.y) * skala;
    if (sx < -80 || sx > lebarCss + 80) return;
    sy = Math.max(74, Math.min(tinggiCss - 60, sy + Math.sin(waktuTotal * 3 + o.x) * 3));

    var sudah = !!dikunjungi[o.zona];
    var w = 34, h = 34;
    ctx.save();
    ctx.shadowColor = "rgba(24, 32, 20, .4)";
    ctx.shadowBlur = 6;
    ctx.shadowOffsetY = 3;
    ctx.fillStyle = "#fffdf6";
    kotakBulat(sx - w / 2, sy - h, w, h, 12);
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(sx - 6, sy - 2);
    ctx.lineTo(sx + 6, sy - 2);
    ctx.lineTo(sx, sy + 9);
    ctx.closePath();
    ctx.fill();
    ctx.shadowColor = "transparent";

    ctx.strokeStyle = "#3a2f24";
    ctx.lineWidth = 2;
    kotakBulat(sx - w / 2, sy - h, w, h, 12);
    ctx.stroke();

    if (sudah) {
      ctx.strokeStyle = ZONA[o.zona].warna;
      ctx.lineWidth = 3.4;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(sx - 7, sy - 17);
      ctx.lineTo(sx - 2, sy - 11);
      ctx.lineTo(sx + 8, sy - 23);
      ctx.stroke();
    } else {
      ctx.fillStyle = "#3a2f24";
      ctx.font = "800 22px Nunito, system-ui, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("!", sx, sy - h / 2 + 1);
    }
    ctx.restore();
  }

  function kotakBulat(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function gambarPanahArah() {
    var pusatX = lebarCss / 2, pusatY = tinggiCss / 2;
    var batasKiri = 44, batasKanan = lebarCss - 44;
    var batasAtas = 118, batasBawah = tinggiCss - 130;
    if (batasBawah <= batasAtas) return;
    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona || dikunjungi[o.zona]) continue;
      var sx = (layarX(o.x) - kamera.x) * skala;
      var sy = (layarY(o.x, o.y) - kamera.y) * skala;
      if (sx > 24 && sx < lebarCss - 24 && sy > 96 && sy < tinggiCss - 96) continue;
      var dx = sx - pusatX, dy = sy - pusatY;
      if (!dx && !dy) continue;
      var t = Math.min(
        Math.abs(dx) < 0.001 ? Infinity : (dx > 0 ? batasKanan - pusatX : pusatX - batasKiri) / Math.abs(dx),
        Math.abs(dy) < 0.001 ? Infinity : (dy > 0 ? batasBawah - pusatY : pusatY - batasAtas) / Math.abs(dy)
      );
      var ax = pusatX + dx * t, ay = pusatY + dy * t;
      ctx.save();
      ctx.translate(ax, ay);
      ctx.fillStyle = ZONA[o.zona].warna;
      ctx.beginPath();
      ctx.arc(0, 0, 15, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "rgba(255,253,246,.9)";
      ctx.lineWidth = 2.5;
      ctx.stroke();
      ctx.rotate(Math.atan2(dy, dx));
      ctx.fillStyle = "#fffdf6";
      ctx.beginPath();
      ctx.moveTo(6, 0); ctx.lineTo(-3, -5); ctx.lineTo(-3, 5);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }
  }

  function gambarSemua() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = "#2d5b28";
    ctx.fillRect(0, 0, lebarCss, tinggiCss);

    var f = dpr * skala;
    ctx.setTransform(f, 0, 0, f, -Math.round(kamera.x * f), -Math.round(kamera.y * f));
    gambarPeta();
    if (zonaAktif) gambarCincinAktif(zonaAktif);

    objekTerurut.length = 0;
    for (var i = 0; i < OBJEK.length; i++) objekTerurut.push(OBJEK[i]);
    objekTerurut.push(pemain);
    objekTerurut.sort(function (a, b) { return a.y - b.y; });
    for (var j = 0; j < objekTerurut.length; j++) {
      if (objekTerurut[j] === pemain) gambarPemain();
      else gambarObjek(objekTerurut[j]);
    }

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    for (var k = 0; k < OBJEK.length; k++) {
      if (OBJEK[k].zona) gambarBalon(OBJEK[k]);
    }
    gambarPanahArah();
    gambarPetaMini();
  }

  /* =====================================================================
     Peta bundar & peta besar
     ===================================================================== */
  var cachePeta = {};

  function ambilCachePeta(px) {
    if (cachePeta[px]) return cachePeta[px];
    var c = document.createElement("canvas");
    c.width = Math.ceil(LEBAR_PETA * px);
    c.height = Math.ceil(TINGGI_PETA * px);
    var m = c.getContext("2d");
    for (var ty = 0; ty < TINGGI_PETA; ty++) {
      for (var tx = 0; tx < LEBAR_PETA; tx++) {
        m.fillStyle = WARNA_PETAK[PETA[ty][tx]] || "#60aa44";
        m.fillRect(tx * px, ty * px, Math.ceil(px), Math.ceil(px));
      }
    }
    cachePeta[px] = c;
    return c;
  }

  function titikPetaMini(px) {
    return function (tx, ty) { return [tx * px, ty * px]; };
  }

  var ctxMini = el.petaMini ? el.petaMini.getContext("2d") : null;
  var DIAMETER_MINI = 108;

  function aturUkuranPetaMini() {
    if (!el.petaMini) return;
    el.petaMini.width = Math.round(DIAMETER_MINI * dpr);
    el.petaMini.height = Math.round(DIAMETER_MINI * dpr);
    el.petaMini.style.width = DIAMETER_MINI + "px";
    el.petaMini.style.height = DIAMETER_MINI + "px";
  }

  function gambarPetaMini() {
    if (!ctxMini) return;
    var px = 2.9;
    var cache = ambilCachePeta(px);
    var ke = titikPetaMini(px);
    ctxMini.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctxMini.clearRect(0, 0, DIAMETER_MINI, DIAMETER_MINI);
    ctxMini.save();
    ctxMini.beginPath();
    ctxMini.arc(DIAMETER_MINI / 2, DIAMETER_MINI / 2, DIAMETER_MINI / 2, 0, Math.PI * 2);
    ctxMini.clip();
    ctxMini.fillStyle = "#3f7a35";
    ctxMini.fillRect(0, 0, DIAMETER_MINI, DIAMETER_MINI);
    var geser = [DIAMETER_MINI / 2 - cache.width / 2, DIAMETER_MINI / 2 - cache.height / 2];
    ctxMini.drawImage(cache, geser[0], geser[1]);

    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (!o.zona) continue;
      var p = ke(o.x, o.y);
      ctxMini.fillStyle = dikunjungi[o.zona] ? "#fffdf6" : ZONA[o.zona].warna;
      ctxMini.strokeStyle = "rgba(32,26,20,.75)";
      ctxMini.lineWidth = 1;
      ctxMini.beginPath();
      ctxMini.arc(p[0] + geser[0], p[1] + geser[1], 3.4, 0, Math.PI * 2);
      ctxMini.fill();
      ctxMini.stroke();
    }
    var pp = ke(pemain.x, pemain.y);
    var denyut = 2.8 + Math.sin(waktuTotal * 4) * 0.7;
    ctxMini.fillStyle = "#2b2119";
    ctxMini.beginPath();
    ctxMini.arc(pp[0] + geser[0], pp[1] + geser[1], denyut + 1.8, 0, Math.PI * 2);
    ctxMini.fill();
    ctxMini.fillStyle = "#fffdf6";
    ctxMini.beginPath();
    ctxMini.arc(pp[0] + geser[0], pp[1] + geser[1], denyut, 0, Math.PI * 2);
    ctxMini.fill();
    ctxMini.restore();
  }

  var PX_PETA_BESAR = 13;

  function gambarPetaBesar() {
    if (!el.petaBesar) return;
    var cache = ambilCachePeta(PX_PETA_BESAR);
    var ke = titikPetaMini(PX_PETA_BESAR);
    var r = Math.min(window.devicePixelRatio || 1, 2);
    el.petaBesar.width = Math.round(cache.width * r);
    el.petaBesar.height = Math.round((cache.height + 40) * r);
    el.petaBesar.style.width = "100%";
    var m = el.petaBesar.getContext("2d");
    m.setTransform(r, 0, 0, r, 0, 20);
    m.clearRect(0, -20, cache.width, cache.height + 40);
    m.drawImage(cache, 0, 0);
    m.font = "700 11px Nunito, system-ui, sans-serif";
    m.textAlign = "center";

    for (var n = 0; n < URUTAN_ZONA.length; n++) {
      var kunci = URUTAN_ZONA[n];
      var o = objekZona(kunci);
      if (!o) continue;
      var p = ke(o.x, o.y);
      m.fillStyle = "rgba(26,34,22,.35)";
      m.beginPath(); m.arc(p[0], p[1] + 2, 11, 0, Math.PI * 2); m.fill();
      m.fillStyle = ZONA[kunci].warna;
      m.strokeStyle = "#fffdf6";
      m.lineWidth = 2.5;
      m.beginPath(); m.arc(p[0], p[1], 11, 0, Math.PI * 2); m.fill(); m.stroke();
      m.fillStyle = "#fffdf6";
      m.textBaseline = "middle";
      if (dikunjungi[kunci]) {
        m.strokeStyle = "#fffdf6"; m.lineWidth = 2.2; m.lineCap = "round";
        m.beginPath();
        m.moveTo(p[0] - 4, p[1]); m.lineTo(p[0] - 1, p[1] + 3.5); m.lineTo(p[0] + 4.5, p[1] - 3.5);
        m.stroke();
      } else {
        m.fillText(String(n + 1), p[0], p[1] + 0.5);
      }
      var teks = ZONA[kunci].judul;
      var w = m.measureText(teks).width + 12;
      m.fillStyle = "rgba(255,253,246,.94)";
      kotakBulatDi(m, p[0] - w / 2, p[1] + 14, w, 17, 8); m.fill();
      m.fillStyle = "#3a2f24";
      m.fillText(teks, p[0], p[1] + 23);
    }

    var pp = ke(pemain.x, pemain.y);
    m.fillStyle = "#2b2119";
    m.beginPath(); m.arc(pp[0], pp[1], 8, 0, Math.PI * 2); m.fill();
    m.fillStyle = "#fffdf6";
    m.beginPath(); m.arc(pp[0], pp[1], 5, 0, Math.PI * 2); m.fill();
    var lw = m.measureText("Anda").width + 12;
    m.fillStyle = "rgba(255,253,246,.94)";
    kotakBulatDi(m, pp[0] - lw / 2, pp[1] - 30, lw, 17, 8); m.fill();
    m.fillStyle = "#3a2f24";
    m.fillText("Anda", pp[0], pp[1] - 21);
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
      var cache = ambilCachePeta(PX_PETA_BESAR);
      var sk = kotak.width / cache.width;
      var mx = (e.clientX - kotak.left) / sk;
      var my = (e.clientY - kotak.top) / sk - 20;
      var ke = titikPetaMini(PX_PETA_BESAR);
      var terdekat = null, jarakTerdekat = Infinity;
      for (var i = 0; i < URUTAN_ZONA.length; i++) {
        var o = objekZona(URUTAN_ZONA[i]);
        if (!o) continue;
        var p = ke(o.x, o.y);
        var jarak = Math.hypot(mx - p[0], my - p[1]);
        if (jarak < jarakTerdekat) { jarakTerdekat = jarak; terdekat = o; }
      }
      if (terdekat && jarakTerdekat < 26) pergiKe(terdekat.zona);
    });
  }

  function bangunDaftarLokasi() {
    if (!el.daftarLokasi) return;
    el.daftarLokasi.textContent = "";
    URUTAN_ZONA.forEach(function (kunci, i) {
      var z = ZONA[kunci];
      var b = document.createElement("button");
      b.type = "button";
      b.className = "lokasi";
      b.dataset.zona = kunci;
      b.style.setProperty("--warna-zona", z.warna);
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
      b.append(nomor, isi, pergi);
      b.addEventListener("click", function () { pergiKe(kunci); });
      el.daftarLokasi.appendChild(b);
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
     Pemberitahuan
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
  var waktuSebelum = 0, jumlahFrame = 0, idAnimasi = null, pakaiPewaktu = false;
  var halamanTerlihat = true;
  document.addEventListener("visibilitychange", function () {
    halamanTerlihat = !document.hidden;
  });

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
    tombol = {}; hitungArah();
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
     Hitung mundur, buku tamu, salin, lightbox, musik, karakter
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
        headers: { "Content-Type": "application/json", "X-CSRFToken": data.get("csrfmiddlewaretoken") },
        body: JSON.stringify({
          nama: data.get("nama"), pesan: data.get("pesan"),
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

  var musikNyala = false;
  function setelMusik(nyala) {
    if (!el.musik) { el.tombolMusik.style.display = "none"; return; }
    musikNyala = nyala;
    el.tombolMusik.classList.toggle("mati", !nyala);
    if (nyala) { var p = el.musik.play(); if (p && p.catch) p.catch(function () {}); }
    else el.musik.pause();
  }
  el.tombolMusik.addEventListener("click", function () { setelMusik(!musikNyala); });

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
