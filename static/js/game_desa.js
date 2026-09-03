/* =========================================================================
   Tema 4 — "Desa Asri Parahyangan" (Gaya Stardew Valley Edition)
   Fitur Utama:
   - Keterangan / Floating Nameplate di atas setiap lokasi & karakter
   - Klik/Ketuk langsung pada objek lokasi untuk membuka popup secara instan
     (atau otomatis jalan sendiri jika jauh) TANPA perlu menekan tombol seru pojok
   - Denah Desa Interaktif & Auto-Walk BFS
   - Full-Bleed Map 36x28 tanpa celah samping pada semua ukuran layar
   - Joystick analog virtual selalu tampil (Mouse & Touch HP)
   - Musik latar santai pentatonik pedesaan otomatis
   ========================================================================= */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("data-undangan").textContent);
  var PETAK = 48;                // 48x48 piksel per petak
  var LAJU = 3.2;                // Kecepatan jalan (petak per detik)

  /* Nama mempelai dari database/data-undangan */
  var NAMA_PRIA = DATA.pria_nama || "Budi";
  var NAMA_WANITA = DATA.wanita_nama || "Rina";
  var NAMA_PASANGAN = NAMA_PRIA + " & " + NAMA_WANITA;
  var NAMA_TAMU = DATA.tamu_nama || "Tamu Undangan";

  /* ---------------------------------------------------------------------
     Denah Desa Asri (36 kolom x 28 baris = 1728 x 1344 piksel):
       # = rimba / bukit pembatas (padat)
       ~ = air sungai jernih (padat kecuali jembatan)
       f = pagar kayu peternakan (padat)
       . = rumput hijau asri
       , = rumput berbunga liar
       p = jalan tanah gembur
       b = jalan batu kali / cobblestone
       w = jembatan / panggung kayu
       s = petak sawah terasering berair
       k = kebun sayur gembur
     --------------------------------------------------------------------- */
  var PETA = [
    "####################################",
    "#..................................#",
    "#...,....sssssss....bbbbbbbb....kkk#",
    "#..sssssssssssss....b......b....kkk#",
    "#..sssssssssssss....b......b....kkk#",
    "#..sssssssssssss....b......b....kkk#",
    "#..sssssssssssss....bbbbbbbb....kkk#",
    "#..................................#",
    "#..f.f.f.f.f.f.........pp....f.f.f.#",
    "#~~~~~~~~~~~~~~~.......pp~~~~~~~~~~#",
    "#~~~~~~~~~~~~~~~~......pp~~~~~~~~~~#",
    "#~~~~~~~~~~~~~~~~......ww~~~~~~~~~~#",
    "#~~~~~~~~~~~~~~~~......pp~~~~~~~~~~#",
    "#~~~~~~~~~~~~~~~.......pp~~~~~~~~~~#",
    "#..p.p.....p.p...bbbbbbbbbb..p.p...#",
    "#..p.p.....p.p...b........b..p.p...#",
    "#..ppp.....ppp...b........b..ppp...#",
    "#................b........b........#",
    "#..f...f...f.....b........b....f...#",
    "#..f...f...f.....bbbbbbbbbb....f...#",
    "#..f...f...f...........pp......f...#",
    "#......................pp..........#",
    "#...,..................pp......,...#",
    "#......................pp..........#",
    "#......................pp..........#",
    "#..f.f.f.f.f...........pp....f.f.f.#",
    "#..................................#",
    "####################################"
  ];

  var INDEKS_PETAK = {
    ".": 0, ",": 1, "p": 3, "b": 4, "w": 5, "k": 6,
    "~": 7, "s": 10, "#": 11, "f": 12
  };
  var FRAME_AIR = [7, 8, 9];
  var PADAT = { "#": true, "~": true, "f": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * PETAK;
  var TINGGI_DUNIA = TINGGI_PETA * PETAK;

  /* ---------------------------------------------------------------------
     Titik Tujuan Interaktif (5 Lokasi Utama untuk Navigasi & Auto-Walk)
     --------------------------------------------------------------------- */
  var TITIK_LOKASI = [
    { id: "pengantin", nomor: 1, nama: "Pelaminan Mempelai", x: 20.5, y: 5.6, ikon: "👑" },
    { id: "acara", nomor: 2, nama: "Papan Pengumuman Acara", x: 12.5, y: 15.5, ikon: "📜" },
    { id: "galeri", nomor: 3, nama: "Jemuran Galeri Foto", x: 28.5, y: 15.5, ikon: "📷" },
    { id: "ucapan", nomor: 4, nama: "Meja Jamuan & RSVP", x: 27.5, y: 19.5, ikon: "🍱" },
    { id: "hadiah", nomor: 5, nama: "Peti Kayu Hadiah", x: 13.5, y: 19.5, ikon: "🎁" }
  ];

  /* ---------------------------------------------------------------------
     Daftar Objek di Peta Dunia Lengkap dengan Keterangan / Floating Label
     --------------------------------------------------------------------- */
  var OBJEK = [
    // 1. Pelaminan Saung Rustic (Tengah Atas)
    {
      gambar: "pelaminan", x: 20.5, y: 4.2, padat: [3.4, 1.4],
      zona: "pengantin", label: "Pelaminan Mempelai", sublabel: NAMA_PASANGAN, ikon: "👑"
    },
    {
      gambar: "pengantin_pria", x: 19.8, y: 4.4, padat: [0.5, 0.3],
      label: NAMA_PRIA, sublabel: "Pengantin Pria", ikon: "🤵",
      zona: "pengantin"
    },
    {
      gambar: "pengantin_wanita", x: 21.2, y: 4.4, padat: [0.5, 0.3],
      label: NAMA_WANITA, sublabel: "Pengantin Wanita", ikon: "👰",
      zona: "pengantin"
    },

    // Atraksi Musik & Tarian Sunda di Sekitar Pelaminan
    {
      gambar: "penari", x: 24.5, y: 5.0, padat: [1.6, 0.8],
      label: "Penari Jaipong", sublabel: "Tari Tradisional Sunda", ikon: "💃",
      pesan: "💃 Dua penari Jaipong mempersembahkan tarian selamat datang penuh suka cita!"
    },
    {
      gambar: "pemusik", x: 16.5, y: 5.0, padat: [1.8, 0.9],
      label: "Pemusik Tradisional", sublabel: "Kecapi & Suling", ikon: "🎶",
      pesan: "🎶 Alunan merdu kecapi suling Parahyangan yang damai mengiringi hari bahagia ini."
    },

    // 2. Papan Pengumuman Desa (Stardew Notice Board)
    {
      gambar: "papan", x: 12.5, y: 14.8, padat: [1.1, 0.8],
      zona: "acara", label: "Rangkaian Acara", sublabel: "Akad, Resepsi & Maps", ikon: "📜"
    },

    // 3. Galeri Foto Jemuran Rustic
    {
      gambar: "galeri", x: 28.5, y: 14.8, padat: [1.8, 0.8],
      zona: "galeri", label: "Galeri Foto", sublabel: "Dokumentasi Prewedding", ikon: "📷"
    },

    // 4. Meja Jamuan Kebun & Tumpeng Syukuran
    {
      gambar: "buku_tamu", x: 27.5, y: 18.6, padat: [1.6, 0.9],
      zona: "ucapan", label: "Buku Tamu & RSVP", sublabel: "Kirim Doa Restu & Hadir", ikon: "🍱"
    },

    // 5. Peti Kayu Hadiah (Shipping Box)
    {
      gambar: "hadiah", x: 13.5, y: 18.6, padat: [0.9, 0.8],
      zona: "hadiah", label: "Tanda Kasih", sublabel: "Amplop Digital & QRIS", ikon: "🎁"
    },

    // Tamu Warga Desa Mengobrol & Bangku Kayu
    {
      gambar: "tamu_desa", x: 20.5, y: 18.2, padat: [1.2, 0.6],
      label: "Warga & Kerabat", sublabel: "Tamu Undangan", ikon: "👥",
      pesan: "👥 Para tamu warga desa tersenyum ramah dan turut mendoakan kedua mempelai!"
    },
    { gambar: "bangku", x: 16.5, y: 18.4, padat: [1.1, 0.5] },
    { gambar: "bangku", x: 24.5, y: 18.4, padat: [1.1, 0.5] },

    // Kolam Ikan Koi & Pancuran Bambu dekat Sungai
    {
      gambar: "kolam_ikan", x: 11.5, y: 8.2, padat: [1.6, 1.2],
      label: "Kolam Ikan Koi", sublabel: "Pancuran Bambu", ikon: "🐟",
      pesan: "🐟 Gemericik air pancuran bambu dengan ikan mas koi berenang tenang di air jernih."
    },

    // Kincir Air Bambu Tepi Sawah
    {
      gambar: "kincir", x: 14.5, y: 8.5, padat: [1.0, 1.2],
      label: "Kincir Air Sawah", sublabel: "Irigasi Tradisional", ikon: "🌾",
      pesan: "🌾 Kincir bambu tradisional berputar perlahan mengalirkan air ke petak sawah."
    },

    // Tiang Lentera Malam Romantis
    { gambar: "lentera", x: 19.0, y: 13.5 },
    { gambar: "lentera", x: 22.0, y: 13.5 },
    { gambar: "lentera", x: 19.0, y: 21.5 },
    { gambar: "lentera", x: 22.0, y: 21.5 },

    // Gapura Masuk (Bawah)
    {
      gambar: "gerbang", x: 20.5, y: 24.5,
      label: "Gapura Masuk", sublabel: "Wilujeng Sumping", ikon: "🌸"
    },

    // Dekorasi Lumbung Padi & Pohon Buah
    {
      gambar: "saung_lumbung", x: 31.5, y: 4.8, padat: [1.8, 1.2],
      label: "Saung Lumbung Padi", sublabel: "Padi Parahyangan", ikon: "🏡",
      pesan: "🏡 Saung lumbung padi tradisional Sunda dengan atap sirap kayu."
    },
    { gambar: "pohon_buah", x: 17.0, y: 2.5, padat: [0.8, 0.6] },
    { gambar: "pohon_buah", x: 24.0, y: 2.5, padat: [0.8, 0.6] },
    { gambar: "pohon_buah", x: 7.0, y: 15.0, padat: [0.8, 0.6] },
    { gambar: "pohon_buah", x: 32.5, y: 15.0, padat: [0.8, 0.6] },
    { gambar: "pohon_buah", x: 15.0, y: 23.5, padat: [0.8, 0.6] },
    { gambar: "pohon_buah", x: 26.0, y: 23.5, padat: [0.8, 0.6] }
  ];

  /* Hewan Pedesaan (Ayam, Kucing, & Bebek Berenang di Sungai) */
  var AYAM_LIST = [
    { x: 17.5, y: 16.5, arah: 1, timer: 0, frame: 0, label: "Ayam Kampung", ikon: "🐔" },
    { x: 23.5, y: 17.0, arah: -1, timer: 1.2, frame: 0, label: "Ayam Kampung", ikon: "🐔" },
    { x: 10.5, y: 21.5, arah: 1, timer: 2.8, frame: 0, label: "Ayam Kampung", ikon: "🐔" }
  ];
  var KUCING = { x: 30.2, y: 5.6, frame: 0, timer: 0, label: "Si Manis", ikon: "🐱" };
  var BEBEK_LIST = [
    { x: 7.5, y: 10.5, laju: 0.8, frame: 0, timer: 0, minX: 4, maxX: 14, label: "Bebek Desa", ikon: "🦆" },
    { x: 26.5, y: 11.2, laju: -0.6, frame: 1, timer: 0.5, minX: 23, maxX: 33, label: "Bebek Desa", ikon: "🦆" }
  ];

  /* Partikel Daun Gugur & Kelopak Bunga Melayang */
  var PARTIKEL = [];
  var JUMLAH_PARTIKEL = 36;
  for (var pi = 0; pi < JUMLAH_PARTIKEL; pi++) {
    PARTIKEL.push({
      x: Math.random() * LEBAR_DUNIA,
      y: Math.random() * TINGGI_DUNIA,
      vx: 20 + Math.random() * 26,
      vy: 12 + Math.random() * 18,
      fase: Math.random() * Math.PI * 2,
      ukuran: 3 + Math.random() * 4,
      warna: Math.random() > 0.4 ? "rgba(255, 172, 196, 0.9)" : "rgba(164, 224, 88, 0.9)"
    });
  }

  /* Status Pemain */
  var PEMAIN = {
    x: 20.5,
    y: 23.8,
    arah: "atas",
    frame: 0,
    jalan: false,
    karakter: "pria",
    sedangJalanOtomatis: false,
    jalurOtomatis: [],
    targetZona: null,
    label: NAMA_TAMU,
    sublabel: "Karakter Anda",
    ikon: "✨"
  };

  var STATUS = {
    dikunjungi: {},
    zonaAktif: null,
    waktuRiak: 0,
    waktuAnimasi: 0,
    suaraMusik: false,
    objekHover: null,
    skalaKamera: 1.0,
    kameraX: 0,
    kameraY: 0
  };

  /* Input Controls */
  var INPUT = {
    atas: false, bawah: false, kiri: false, kanan: false,
    analogAktif: false, analogDx: 0, analogDy: 0
  };

  /* Cache Gambar */
  var GAMBAR = {};
  var GAMBAR_DIMUAT = 0;
  var TOTAL_GAMBAR = Object.keys(DATA.aset).length;

  var kanvas = document.getElementById("kanvas");
  var ctx = kanvas.getContext("2d");
  var barMuat = document.getElementById("isi-muat");
  var tiraiMuat = document.getElementById("memuat");
  var toastNotif = document.getElementById("toast-notifikasi");
  var teksToast = document.getElementById("teks-toast");

  function tampilkanToast(teks) {
    if (!toastNotif || !teksToast) return;
    teksToast.textContent = teks;
    toastNotif.hidden = false;
    clearTimeout(toastNotif._timer);
    toastNotif._timer = setTimeout(function () {
      toastNotif.hidden = true;
    }, 3200);
  }

  /* =========================================================================
     Memuat Semua Aset Gambar
     ========================================================================= */
  function muatSemuaAset(selesai) {
    var kunci = Object.keys(DATA.aset);
    kunci.forEach(function (k) {
      var img = new Image();
      img.onload = function () {
        GAMBAR[k] = img;
        GAMBAR_DIMUAT++;
        if (barMuat) {
          barMuat.style.width = Math.round((GAMBAR_DIMUAT / TOTAL_GAMBAR) * 100) + "%";
        }
        if (GAMBAR_DIMUAT >= TOTAL_GAMBAR) {
          if (tiraiMuat) tiraiMuat.classList.add("selesai");
          selesai();
        }
      };
      img.onerror = function () {
        console.warn("Gagal memuat aset:", k, DATA.aset[k]);
        GAMBAR_DIMUAT++;
        if (GAMBAR_DIMUAT >= TOTAL_GAMBAR) selesai();
      };
      img.src = DATA.aset[k];
    });
  }

  /* =========================================================================
     Fisika Gerak, Navigasi BFS, & Tabrakan
     ========================================================================= */
  function bisaDilewati(tx, ty) {
    if (tx < 1.0 || tx >= LEBAR_PETA - 1.0 || ty < 1.0 || ty >= TINGGI_PETA - 1.0) return false;
    var petakX = Math.floor(tx);
    var petakY = Math.floor(ty);
    if (!PETA[petakY] || !PETA[petakY][petakX]) return false;
    var kode = PETA[petakY][petakX];
    if (PADAT[kode]) return false;

    // Cek tabrakan kotak objek
    for (var i = 0; i < OBJEK.length; i++) {
      var obj = OBJEK[i];
      if (!obj.padat) continue;
      var hW = obj.padat[0] / 2;
      var hH = obj.padat[1] / 2;
      if (tx >= obj.x - hW && tx <= obj.x + hW && ty >= obj.y - hH && ty <= obj.y + hH) {
        return false;
      }
    }
    return true;
  }

  /* Breadth-First-Search (BFS) Pathfinding untuk Jalan Otomatis */
  function cariJalur(xAwal, yAwal, xTujuan, yTujuan) {
    var startX = Math.floor(xAwal);
    var startY = Math.floor(yAwal);
    var targetX = Math.floor(xTujuan);
    var targetY = Math.floor(yTujuan);

    if (startX === targetX && startY === targetY) {
      return [{ x: xTujuan, y: yTujuan }];
    }

    var antrean = [[startX, startY]];
    var dikunjungiPeta = {};
    var asal = {};
    var kunciAwal = startX + "," + startY;
    dikunjungiPeta[kunciAwal] = true;

    var arah = [
      [0, -1], [0, 1], [-1, 0], [1, 0]
    ];
    var ditemukan = false;

    while (antrean.length > 0) {
      var saatIni = antrean.shift();
      var cx = saatIni[0];
      var cy = saatIni[1];

      if (cx === targetX && cy === targetY) {
        ditemukan = true;
        break;
      }

      for (var a = 0; a < arah.length; a++) {
        var nx = cx + arah[a][0];
        var ny = cy + arah[a][1];
        var kunciTetangga = nx + "," + ny;

        if (nx >= 0 && nx < LEBAR_PETA && ny >= 0 && ny < TINGGI_PETA) {
          if (!dikunjungiPeta[kunciTetangga] && bisaDilewati(nx + 0.5, ny + 0.5)) {
            dikunjungiPeta[kunciTetangga] = true;
            asal[kunciTetangga] = [cx, cy];
            antrean.push([nx, ny]);
          }
        }
      }
    }

    if (!ditemukan) {
      return [{ x: xTujuan, y: yTujuan }];
    }

    // Rekonstruksi rute
    var rute = [];
    var curr = [targetX, targetY];
    while (curr[0] !== startX || curr[1] !== startY) {
      rute.push({ x: curr[0] + 0.5, y: curr[1] + 0.5 });
      var prev = asal[curr[0] + "," + curr[1]];
      if (!prev) break;
      curr = prev;
    }
    rute.reverse();
    return rute;
  }

  function pergiKe(lokasiId) {
    var titik = null;
    for (var i = 0; i < TITIK_LOKASI.length; i++) {
      if (TITIK_LOKASI[i].id === lokasiId) {
        titik = TITIK_LOKASI[i];
        break;
      }
    }
    if (!titik) return;

    tutupPopup();
    tampilkanToast("🌾 Berjalan menuju " + titik.nama + "…");

    var jalur = cariJalur(PEMAIN.x, PEMAIN.y, titik.x, titik.y);
    PEMAIN.jalurOtomatis = jalur;
    PEMAIN.sedangJalanOtomatis = true;
    PEMAIN.targetZona = lokasiId;
  }

  function gerakPemain(dt) {
    var vx = 0;
    var vy = 0;

    // Jika pengguna menekan tombol manual, batalkan jalan otomatis
    if (INPUT.analogAktif || INPUT.kiri || INPUT.kanan || INPUT.atas || INPUT.bawah) {
      if (PEMAIN.sedangJalanOtomatis) {
        PEMAIN.sedangJalanOtomatis = false;
        PEMAIN.jalurOtomatis = [];
        PEMAIN.targetZona = null;
        if (toastNotif) toastNotif.hidden = true;
      }
    }

    if (PEMAIN.sedangJalanOtomatis && PEMAIN.jalurOtomatis.length > 0) {
      var target = PEMAIN.jalurOtomatis[0];
      var tdx = target.x - PEMAIN.x;
      var tdy = target.y - PEMAIN.y;
      var jarak = Math.hypot(tdx, tdy);

      if (jarak < 0.18) {
        PEMAIN.x = target.x;
        PEMAIN.y = target.y;
        PEMAIN.jalurOtomatis.shift();
        if (PEMAIN.jalurOtomatis.length === 0) {
          var zonaTiba = PEMAIN.targetZona;
          PEMAIN.sedangJalanOtomatis = false;
          PEMAIN.jalan = false;
          PEMAIN.targetZona = null;
          if (toastNotif) toastNotif.hidden = true;
          if (zonaTiba) {
            bukaPopup(zonaTiba);
          }
        }
      } else {
        vx = (tdx / jarak) * LAJU;
        vy = (tdy / jarak) * LAJU;
      }
    } else {
      if (INPUT.analogAktif) {
        vx = INPUT.analogDx * LAJU;
        vy = INPUT.analogDy * LAJU;
      } else {
        if (INPUT.kiri) vx -= LAJU;
        if (INPUT.kanan) vx += LAJU;
        if (INPUT.atas) vy -= LAJU;
        if (INPUT.bawah) vy += LAJU;
        if (vx !== 0 && vy !== 0) {
          vx *= 0.7071;
          vy *= 0.7071;
        }
      }
    }

    if (vx !== 0 || vy !== 0) {
      PEMAIN.jalan = true;
      if (Math.abs(vx) > Math.abs(vy)) {
        PEMAIN.arah = vx > 0 ? "kanan" : "kiri";
      } else {
        PEMAIN.arah = vy > 0 ? "bawah" : "atas";
      }

      var dx = vx * dt;
      var dy = vy * dt;
      var radius = 0.32;

      // Geser X
      if (bisaDilewati(PEMAIN.x + dx + (dx > 0 ? radius : -radius), PEMAIN.y)) {
        PEMAIN.x += dx;
      }
      // Geser Y
      if (bisaDilewati(PEMAIN.x, PEMAIN.y + dy + (dy > 0 ? radius : -radius))) {
        PEMAIN.y += dy;
      }

      STATUS.waktuAnimasi += dt * 6.5;
      PEMAIN.frame = Math.floor(STATUS.waktuAnimasi) % 4;
    } else {
      PEMAIN.jalan = false;
      PEMAIN.frame = 0;
    }

    // Cek Zona Interaksi
    var zonaDitemukan = null;
    for (var i = 0; i < TITIK_LOKASI.length; i++) {
      var titik = TITIK_LOKASI[i];
      var dist = Math.hypot(PEMAIN.x - titik.x, PEMAIN.y - titik.y);
      if (dist < 1.7) {
        zonaDitemukan = titik;
        break;
      }
    }
    STATUS.zonaAktif = zonaDitemukan;

    var btnAksi = document.getElementById("tombol-aksi");
    if (btnAksi) {
      btnAksi.style.transform = zonaDitemukan ? "scale(1.18)" : "scale(1)";
    }
  }

  /* =========================================================================
     Helper Gambar Kotak Bulat
     ========================================================================= */
  function kotakBulat(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

  /* =========================================================================
     Floating Nameplate / Keterangan di Atas Objek & Karakter
     ========================================================================= */
  function gambarLabel(item, xPx, yPx, tinggiSprite) {
    if (!item || !item.label) return;

    var judul = (item.ikon ? item.ikon + " " : "") + item.label;
    var statusTeks = "";
    var warnaStatus = "#ffd678";

    if (item.zona) {
      if (STATUS.dikunjungi[item.zona]) {
        statusTeks = "✓ Selesai";
        warnaStatus = "#8ae650";
      } else {
        statusTeks = "👆 Klik Langsung";
        warnaStatus = "#ffd678";
      }
    } else if (item.sublabel) {
      statusTeks = item.sublabel;
      warnaStatus = "#e8d8b0";
    }

    ctx.font = "bold 11px 'Nunito', sans-serif";
    var lebarJudul = ctx.measureText(judul).width;
    ctx.font = "bold 9px 'Nunito', sans-serif";
    var lebarStatus = statusTeks ? ctx.measureText(statusTeks).width : 0;

    var padX = 8;
    var w = Math.max(lebarJudul, lebarStatus) + padX * 2;
    var h = statusTeks ? 27 : 18;

    // Efek mengapung lembut
    var goyang = Math.sin(STATUS.waktuAnimasi * 2.5 + (item.x || 0) * 3) * 2;
    var lx = xPx - w / 2;
    var ly = yPx - tinggiSprite - h - 8 + goyang;

    // Simpan koordinat label untuk deteksi klik
    item._labelBox = { x: lx, y: ly, w: w, h: h };

    var isHover = (STATUS.objekHover === item);
    var isDekat = (STATUS.zonaAktif && STATUS.zonaAktif.id === item.zona);

    ctx.save();
    if (isHover || isDekat) {
      ctx.shadowColor = "rgba(255, 214, 120, 0.85)";
      ctx.shadowBlur = 10;
    } else {
      ctx.shadowColor = "rgba(0, 0, 0, 0.4)";
      ctx.shadowBlur = 4;
    }

    kotakBulat(ctx, lx, ly, w, h, 6);
    ctx.fillStyle = isHover
      ? "rgba(74, 40, 18, 0.96)"
      : (item.zona ? "rgba(48, 26, 12, 0.92)" : "rgba(36, 20, 10, 0.82)");
    ctx.fill();

    ctx.strokeStyle = isHover || isDekat
      ? "#ffe682"
      : (item.zona ? (STATUS.dikunjungi[item.zona] ? "#74c74a" : "#e8a442") : "#8c5a2b");
    ctx.lineWidth = isHover || isDekat ? 2.2 : 1.5;
    ctx.stroke();

    // Panah kecil penunjuk ke objek
    ctx.fillStyle = ctx.strokeStyle;
    ctx.beginPath();
    ctx.moveTo(xPx - 4, ly + h);
    ctx.lineTo(xPx + 4, ly + h);
    ctx.lineTo(xPx, ly + h + 4);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    // Judul Label
    ctx.fillStyle = "#fffdf6";
    ctx.font = "bold 11px 'Nunito', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(judul, xPx, ly + (statusTeks ? 9 : h / 2));

    // Sublabel / Status
    if (statusTeks) {
      ctx.fillStyle = warnaStatus;
      ctx.font = "bold 9px 'Nunito', sans-serif";
      ctx.fillText(statusTeks, xPx, ly + 19);
    }
  }

  /* =========================================================================
     Render Dunia (Canvas 2D) Tanpa Ruang Kosong Samping
     ========================================================================= */
  function render(dt) {
    if (kanvas.width !== window.innerWidth || kanvas.height !== window.innerHeight) {
      kanvas.width = window.innerWidth;
      kanvas.height = window.innerHeight;
      ctx.imageSmoothingEnabled = false;
    }

    // Skala responsif pixel art
    var skala = window.innerWidth > 1400 ? 1.25 : (window.innerWidth > 900 ? 1.12 : 1.0);
    var lebarTampak = kanvas.width / skala;
    var tinggiTampak = kanvas.height / skala;

    // Kamera halus terpusat
    var kameraX = lebarTampak >= LEBAR_DUNIA
      ? (LEBAR_DUNIA - lebarTampak) / 2
      : Math.max(0, Math.min(LEBAR_DUNIA - lebarTampak, PEMAIN.x * PETAK - lebarTampak / 2));

    var kameraY = tinggiTampak >= TINGGI_DUNIA
      ? (TINGGI_DUNIA - tinggiTampak) / 2
      : Math.max(0, Math.min(TINGGI_DUNIA - tinggiTampak, PEMAIN.y * PETAK - tinggiTampak / 2));

    STATUS.skalaKamera = skala;
    STATUS.kameraX = kameraX;
    STATUS.kameraY = kameraY;

    ctx.save();
    ctx.scale(skala, skala);
    ctx.translate(-Math.round(kameraX), -Math.round(kameraY));

    // 1. Gambar Petak Ubin (Tiles)
    var imgTiles = GAMBAR.tileset;
    var faseAir = Math.floor((STATUS.waktuRiak += dt * 2.5)) % 3;

    var minTX = Math.floor(kameraX / PETAK) - 1;
    var maxTX = Math.ceil((kameraX + lebarTampak) / PETAK) + 1;
    var minTY = Math.floor(kameraY / PETAK) - 1;
    var maxTY = Math.ceil((kameraY + tinggiTampak) / PETAK) + 1;

    for (var ty = minTY; ty <= maxTY; ty++) {
      for (var tx = minTX; tx <= maxTX; tx++) {
        var luar = tx < 0 || ty < 0 || tx >= LEBAR_PETA || ty >= TINGGI_PETA;
        var idx = 11; // Rimba default untuk area luar

        if (!luar) {
          var kode = PETA[ty][tx];
          idx = INDEKS_PETAK[kode] !== undefined ? INDEKS_PETAK[kode] : 0;
          if (kode === "~") idx = FRAME_AIR[faseAir];
        }

        if (imgTiles) {
          ctx.drawImage(imgTiles, idx * PETAK, 0, PETAK, PETAK, tx * PETAK, ty * PETAK, PETAK, PETAK);
        }
      }
    }

    // 2. Kumpulkan Entitas untuk Y-Sorting
    var daftarGambar = [];

    // Objek Statis & Dekorasi
    for (var oi = 0; oi < OBJEK.length; oi++) {
      var ob = OBJEK[oi];
      daftarGambar.push({ tipe: "objek", y: ob.y, data: ob });
    }

    // Ayam Kampung
    for (var ai = 0; ai < AYAM_LIST.length; ai++) {
      var ay = AYAM_LIST[ai];
      ay.timer += dt;
      if (ay.timer > 0.8) {
        ay.timer = 0;
        ay.frame = (ay.frame + 1) % 4;
        if (Math.random() > 0.6) ay.arah = -ay.arah;
      }
      daftarGambar.push({ tipe: "ayam", y: ay.y, data: ay });
    }

    // Kucing Pedesaan
    KUCING.timer += dt;
    if (KUCING.timer > 0.7) {
      KUCING.timer = 0;
      KUCING.frame = (KUCING.frame + 1) % 4;
    }
    daftarGambar.push({ tipe: "kucing", y: KUCING.y, data: KUCING });

    // Bebek Berenang di Sungai
    for (var bi = 0; bi < BEBEK_LIST.length; bi++) {
      var bk = BEBEK_LIST[bi];
      bk.x += bk.laju * dt;
      if (bk.x < bk.minX) { bk.x = bk.minX; bk.laju = Math.abs(bk.laju); }
      if (bk.x > bk.maxX) { bk.x = bk.maxX; bk.laju = -Math.abs(bk.laju); }
      bk.timer += dt;
      if (bk.timer > 0.3) {
        bk.timer = 0;
        bk.frame = (bk.frame + 1) % 4;
      }
      daftarGambar.push({ tipe: "bebek", y: bk.y, data: bk });
    }

    // Pemain
    daftarGambar.push({ tipe: "pemain", y: PEMAIN.y, data: PEMAIN });

    // Urutkan berdasarkan koordinat Y (Depth Sorting)
    daftarGambar.sort(function (a, b) {
      return a.y - b.y;
    });

    // Render Semua Entitas
    for (var di = 0; di < daftarGambar.length; di++) {
      var ent = daftarGambar[di];
      if (ent.tipe === "objek") gambarObjek(ent.data);
      else if (ent.tipe === "pemain") gambarPemain(ent.data);
      else if (ent.tipe === "ayam") gambarAyam(ent.data);
      else if (ent.tipe === "kucing") gambarKucing(ent.data);
      else if (ent.tipe === "bebek") gambarBebek(ent.data);
    }

    // 3. Render Keterangan / Floating Label di Atas Objek & Karakter
    for (var li = 0; li < OBJEK.length; li++) {
      var oItem = OBJEK[li];
      if (oItem.label) {
        var gImg = GAMBAR[oItem.gambar];
        var tSprite = gImg ? gImg.height : 48;
        gambarLabel(oItem, oItem.x * PETAK, oItem.y * PETAK, tSprite);
      }
    }
    // Label Pemain
    gambarLabel(PEMAIN, PEMAIN.x * PETAK, PEMAIN.y * PETAK, 78);

    // 4. Efek Cuaca Partikel Kelopak Bunga & Daun Melayang
    for (var pi = 0; pi < PARTIKEL.length; pi++) {
      var p = PARTIKEL[pi];
      p.x += (p.vx + Math.sin(p.fase += dt * 3) * 12) * dt;
      p.y += p.vy * dt;
      if (p.x > LEBAR_DUNIA) p.x = 0;
      if (p.y > TINGGI_DUNIA) p.y = 0;

      ctx.fillStyle = p.warna;
      ctx.beginPath();
      ctx.ellipse(p.x, p.y, p.ukuran, p.ukuran * 0.5, p.fase, 0, Math.PI * 2);
      ctx.fill();
    }

    ctx.restore();
  }

  function gambarObjek(ob) {
    var img = GAMBAR[ob.gambar];
    if (!img) return;
    var x = ob.x * PETAK - img.width / 2;
    var y = ob.y * PETAK - img.height + 8;
    ctx.drawImage(img, Math.round(x), Math.round(y));
  }

  function gambarPemain(p) {
    var spriteKey = p.karakter === "wanita" ? "karakter_wanita" : "karakter_pria";
    var img = GAMBAR[spriteKey];
    if (!img) return;

    var arahBaris = { bawah: 0, kiri: 1, kanan: 2, atas: 3 }[p.arah] || 0;
    var fw = 48;
    var fh = 80;

    var sx = p.frame * fw;
    var sy = arahBaris * fh;
    var dx = p.x * PETAK - fw / 2;
    var dy = p.y * PETAK - fh + 6;

    // Bayangan Kaki Pemain
    ctx.fillStyle = "rgba(18, 28, 12, 0.4)";
    ctx.beginPath();
    ctx.ellipse(p.x * PETAK, p.y * PETAK, 14, 6, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.drawImage(img, sx, sy, fw, fh, Math.round(dx), Math.round(dy), fw, fh);
  }

  function gambarAyam(ay) {
    var img = GAMBAR.ayam;
    if (!img) return;
    var sx = ay.frame * 32;
    var dx = ay.x * PETAK - 16;
    var dy = ay.y * PETAK - 22;
    ctx.save();
    if (ay.arah < 0) {
      ctx.translate(dx + 32, dy);
      ctx.scale(-1, 1);
      ctx.drawImage(img, sx, 0, 32, 32, 0, 0, 32, 32);
    } else {
      ctx.drawImage(img, sx, 0, 32, 32, Math.round(dx), Math.round(dy), 32, 32);
    }
    ctx.restore();
  }

  function gambarKucing(kc) {
    var img = GAMBAR.kucing;
    if (!img) return;
    var sx = kc.frame * 32;
    var dx = kc.x * PETAK - 16;
    var dy = kc.y * PETAK - 20;
    ctx.drawImage(img, sx, 0, 32, 32, Math.round(dx), Math.round(dy), 32, 32);
  }

  function gambarBebek(bk) {
    var img = GAMBAR.bebek;
    if (!img) return;
    var sx = bk.frame * 32;
    var dx = bk.x * PETAK - 16;
    var dy = bk.y * PETAK - 16;
    ctx.save();
    if (bk.laju < 0) {
      ctx.translate(dx + 32, dy);
      ctx.scale(-1, 1);
      ctx.drawImage(img, sx, 0, 32, 32, 0, 0, 32, 32);
    } else {
      ctx.drawImage(img, sx, 0, 32, 32, Math.round(dx), Math.round(dy), 32, 32);
    }
    ctx.restore();
  }

  /* =========================================================================
     Denah Mini Interaktif di Modal Peta
     ========================================================================= */
  function gambarDenahDesa() {
    var kanvasPeta = document.getElementById("kanvas-peta-desa");
    if (!kanvasPeta) return;
    var mCtx = kanvasPeta.getContext("2d");
    kanvasPeta.width = 460;
    kanvasPeta.height = 240;

    var skalaPetaX = kanvasPeta.width / LEBAR_PETA;
    var skalaPetaY = kanvasPeta.height / TINGGI_PETA;

    // 1. Gambar Ubin Sederhana
    for (var ty = 0; ty < TINGGI_PETA; ty++) {
      for (var tx = 0; tx < LEBAR_PETA; tx++) {
        var kd = PETA[ty][tx];
        var warna = "#5b9e38";
        if (kd === "~") warna = "#42a5d6";
        else if (kd === "p") warna = "#9c6e44";
        else if (kd === "b") warna = "#949088";
        else if (kd === "w") warna = "#bc8440";
        else if (kd === "s") warna = "#68ba60";
        else if (kd === "k") warna = "#6c482c";
        else if (kd === "#") warna = "#2a541e";

        mCtx.fillStyle = warna;
        mCtx.fillRect(tx * skalaPetaX, ty * skalaPetaY, skalaPetaX + 0.5, skalaPetaY + 0.5);
      }
    }

    // 2. Gambar Pin Lokasi Tujuan
    for (var i = 0; i < TITIK_LOKASI.length; i++) {
      var t = TITIK_LOKASI[i];
      var px = t.x * skalaPetaX;
      var py = t.y * skalaPetaY;

      mCtx.fillStyle = STATUS.dikunjungi[t.id] ? "#38b000" : "#d90429";
      mCtx.beginPath();
      mCtx.arc(px, py, 7, 0, Math.PI * 2);
      mCtx.fill();
      mCtx.strokeStyle = "#ffffff";
      mCtx.lineWidth = 1.5;
      mCtx.stroke();

      mCtx.fillStyle = "#ffffff";
      mCtx.font = "bold 9px sans-serif";
      mCtx.textAlign = "center";
      mCtx.textBaseline = "middle";
      mCtx.fillText(t.nomor, px, py);
    }

    // 3. Gambar Posisi Pemain ("Anda di Sini")
    var pemX = PEMAIN.x * skalaPetaX;
    var pemY = PEMAIN.y * skalaPetaY;
    mCtx.fillStyle = "#ffdd00";
    mCtx.beginPath();
    mCtx.arc(pemX, pemY, 6, 0, Math.PI * 2);
    mCtx.fill();
    mCtx.strokeStyle = "#4a2912";
    mCtx.lineWidth = 2;
    mCtx.stroke();
  }

  /* =========================================================================
     Interaksi Modal Popup & Stardew Dialog
     ========================================================================= */
  var tiraiPopup = document.getElementById("tirai-popup");

  function bukaPopup(id) {
    if (!id || !tiraiPopup) return;
    STATUS.dikunjungi[id] = true;
    updateKemajuan();

    var semuaPopup = tiraiPopup.querySelectorAll(".popup");
    semuaPopup.forEach(function (p) { p.hidden = true; });

    var targetPopup = document.getElementById("popup-" + id);
    if (targetPopup) {
      targetPopup.hidden = false;
      tiraiPopup.hidden = false;
      if (id === "peta") {
        setTimeout(gambarDenahDesa, 40);
      }
    }
  }

  function tutupPopup() {
    if (tiraiPopup) tiraiPopup.hidden = true;
  }

  function updateKemajuan() {
    var total = TITIK_LOKASI.length;
    var selesai = Object.keys(STATUS.dikunjungi).length;
    var elKemajuan = document.getElementById("hud-kemajuan-angka");
    if (elKemajuan) elKemajuan.textContent = selesai + "/" + total;
  }

  /* =========================================================================
     Deteksi Klik Langsung pada Objek & Kanvas
     ========================================================================= */
  function hitungKoordinatDunia(clientX, clientY) {
    var rect = kanvas.getBoundingClientRect();
    var sx = clientX - rect.left;
    var sy = clientY - rect.top;
    var wx = (sx / STATUS.skalaKamera + STATUS.kameraX) / PETAK;
    var wy = (sy / STATUS.skalaKamera + STATUS.kameraY) / PETAK;
    var px = sx / STATUS.skalaKamera + STATUS.kameraX;
    var py = sy / STATUS.skalaKamera + STATUS.kameraY;
    return { wx: wx, wy: wy, px: px, py: py };
  }

  function cariObjekKlik(pos) {
    // 1. Cek apakah klik mengenai Floating Label (kotak label di atas objek)
    for (var i = 0; i < OBJEK.length; i++) {
      var o = OBJEK[i];
      if (o._labelBox) {
        var lb = o._labelBox;
        if (pos.px >= lb.x && pos.px <= lb.x + lb.w &&
            pos.py >= lb.y && pos.py <= lb.y + lb.h + 8) {
          return o;
        }
      }
    }

    // 2. Cek apakah klik mengenai Sprite Objek di Dunia
    for (var j = 0; j < OBJEK.length; j++) {
      var ob = OBJEK[j];
      var img = GAMBAR[ob.gambar];
      var wPx = img ? img.width : (ob.padat ? ob.padat[0] * PETAK : 48);
      var hPx = img ? img.height : (ob.padat ? ob.padat[1] * PETAK : 48);

      var ox = ob.x * PETAK;
      var oy = ob.y * PETAK;

      var kiri = ox - wPx / 2 - 8;
      var kanan = ox + wPx / 2 + 8;
      var bawah = oy + 12;
      var atas = oy - hPx - 16;

      if (pos.px >= kiri && pos.px <= kanan && pos.py >= atas && pos.py <= bawah) {
        return ob;
      }
    }

    // 3. Cek apakah klik mengenai hewan
    for (var a = 0; a < AYAM_LIST.length; a++) {
      var ay = AYAM_LIST[a];
      if (Math.hypot(pos.wx - ay.x, pos.wy - ay.y) < 1.0) {
        return {
          nama: "Ayam Kampung",
          pesan: "🐔 Petok petok! Ayam kampung sedang asyik mematuk rumput hijau pedesaan."
        };
      }
    }

    for (var b = 0; b < BEBEK_LIST.length; b++) {
      var bk = BEBEK_LIST[b];
      if (Math.hypot(pos.wx - bk.x, pos.wy - bk.y) < 1.3) {
        return {
          nama: "Bebek Desa",
          pesan: "🦆 Kwek kwek! Bebek berenang riang menikmati sejuknya air sungai Parahyangan."
        };
      }
    }

    if (Math.hypot(pos.wx - KUCING.x, pos.wy - KUCING.y) < 1.2) {
      return {
        nama: "Si Manis",
        pesan: "🐱 Meow! Si manis sedang tidur pulas berjemur di samping teras saung."
      };
    }

    // 4. Toleransi radius jika mengklik sekitar titik tujuan
    for (var t = 0; t < TITIK_LOKASI.length; t++) {
      var tk = TITIK_LOKASI[t];
      if (Math.hypot(pos.wx - tk.x, pos.wy - tk.y) < 1.4) {
        for (var k = 0; k < OBJEK.length; k++) {
          if (OBJEK[k].zona === tk.id) return OBJEK[k];
        }
      }
    }

    return null;
  }

  /* =========================================================================
     Event Listeners: Keyboard, Touch, Virtual Analog Joystick Mouse & HP
     ========================================================================= */
  function inisialisasiInput() {
    // Keyboard WASD & Panah
    window.addEventListener("keydown", function (e) {
      if (tiraiPopup && !tiraiPopup.hidden) {
        if (e.key === "Escape") tutupPopup();
        return;
      }
      var k = e.key.toLowerCase();
      if (k === "w" || k === "arrowup") INPUT.atas = true;
      if (k === "s" || k === "arrowdown") INPUT.bawah = true;
      if (k === "a" || k === "arrowleft") INPUT.kiri = true;
      if (k === "d" || k === "arrowright") INPUT.kanan = true;
      if (k === " " || k === "enter") {
        if (STATUS.zonaAktif) bukaPopup(STATUS.zonaAktif.id);
      }
    });

    window.addEventListener("keyup", function (e) {
      var k = e.key.toLowerCase();
      if (k === "w" || k === "arrowup") INPUT.atas = false;
      if (k === "s" || k === "arrowdown") INPUT.bawah = false;
      if (k === "a" || k === "arrowleft") INPUT.kiri = false;
      if (k === "d" || k === "arrowright") INPUT.kanan = false;
    });

    // Virtual Analog Joystick (Mouse Drag Komputer & Touch HP)
    var alas = document.getElementById("analog-alas");
    var pentol = document.getElementById("analog-pentol");
    var analogAktifPointer = false;
    var pointerIdAktif = null;
    var pusatAnalog = { x: 0, y: 0 };
    var radiusMaks = 36;

    if (alas && pentol) {
      alas.addEventListener("pointerdown", function (e) {
        analogAktifPointer = true;
        pointerIdAktif = e.pointerId;
        alas.setPointerCapture(e.pointerId);
        alas.classList.add("aktif");

        var rect = alas.getBoundingClientRect();
        pusatAnalog.x = rect.left + rect.width / 2;
        pusatAnalog.y = rect.top + rect.height / 2;

        var dx = e.clientX - pusatAnalog.x;
        var dy = e.clientY - pusatAnalog.y;
        var dist = Math.hypot(dx, dy);
        if (dist > radiusMaks) {
          dx = (dx / dist) * radiusMaks;
          dy = (dy / dist) * radiusMaks;
        }
        pentol.style.transform = "translate(" + dx + "px, " + dy + "px)";
        INPUT.analogAktif = true;
        INPUT.analogDx = dx / radiusMaks;
        INPUT.analogDy = dy / radiusMaks;
        e.preventDefault();
      });

      alas.addEventListener("pointermove", function (e) {
        if (!analogAktifPointer || e.pointerId !== pointerIdAktif) return;
        var dx = e.clientX - pusatAnalog.x;
        var dy = e.clientY - pusatAnalog.y;
        var dist = Math.hypot(dx, dy);
        if (dist > radiusMaks) {
          dx = (dx / dist) * radiusMaks;
          dy = (dy / dist) * radiusMaks;
        }
        pentol.style.transform = "translate(" + dx + "px, " + dy + "px)";
        INPUT.analogAktif = true;
        INPUT.analogDx = dx / radiusMaks;
        INPUT.analogDy = dy / radiusMaks;
        e.preventDefault();
      });

      function lepasAnalog(e) {
        if (e.pointerId !== pointerIdAktif) return;
        analogAktifPointer = false;
        pointerIdAktif = null;
        alas.classList.remove("aktif");
        pentol.style.transform = "translate(0px, 0px)";
        INPUT.analogAktif = false;
        INPUT.analogDx = 0;
        INPUT.analogDy = 0;
      }

      alas.addEventListener("pointerup", lepasAnalog);
      alas.addEventListener("pointercancel", lepasAnalog);
    }

    // Interaksi Klik Langsung pada Layar Kanvas (Langsung Buka / Jalan ke Lokasi)
    var pointerAwal = { x: 0, y: 0 };
    kanvas.addEventListener("pointerdown", function (e) {
      pointerAwal.x = e.clientX;
      pointerAwal.y = e.clientY;
    });

    kanvas.addEventListener("pointerup", function (e) {
      // Abaikan jika drag panjang
      if (Math.hypot(e.clientX - pointerAwal.x, e.clientY - pointerAwal.y) > 10) return;

      var pos = hitungKoordinatDunia(e.clientX, e.clientY);
      var target = cariObjekKlik(pos);

      if (target) {
        if (target.zona) {
          // Klik langsung ke lokasi interaktif!
          var jarakPemain = Math.hypot(PEMAIN.x - target.x, PEMAIN.y - target.y);
          if (jarakPemain <= 2.5) {
            // Sudah berada dekat: LANGSUNG BUKA POPUP INSTAN!
            bukaPopup(target.zona);
          } else {
            // Jauh: Otomatis jalan sendiri ke lokasi dan buka popup saat tiba!
            pergiKe(target.zona);
          }
          return;
        }

        if (target.pesan) {
          tampilkanToast(target.pesan);
          return;
        }
      }

      // Klik pada tanah terbuka: melangkah ke titik tersebut
      var tx = Math.floor(pos.wx) + 0.5;
      var ty = Math.floor(pos.wy) + 0.5;
      if (bisaDilewati(tx, ty)) {
        var rute = cariJalur(PEMAIN.x, PEMAIN.y, tx, ty);
        if (rute && rute.length > 0) {
          PEMAIN.jalurOtomatis = rute;
          PEMAIN.sedangJalanOtomatis = true;
          PEMAIN.targetZona = null;
        }
      }
    });

    // Kursor Pointer saat Mouse Mengarah ke Objek / Label
    kanvas.addEventListener("pointermove", function (e) {
      var pos = hitungKoordinatDunia(e.clientX, e.clientY);
      var target = cariObjekKlik(pos);
      if (target && (target.zona || target.pesan)) {
        kanvas.style.cursor = "pointer";
        STATUS.objekHover = target;
      } else {
        kanvas.style.cursor = "default";
        STATUS.objekHover = null;
      }
    });

    // Tombol Aksi HP & Spasi
    var btnAksi = document.getElementById("tombol-aksi");
    if (btnAksi) {
      btnAksi.addEventListener("click", function () {
        if (STATUS.zonaAktif) bukaPopup(STATUS.zonaAktif.id);
      });
    }

    // Tombol Buka Undangan Sampul
    var btnBuka = document.getElementById("tombol-buka");
    var sampul = document.getElementById("sampul");
    if (btnBuka && sampul) {
      btnBuka.addEventListener("click", function () {
        sampul.classList.add("tersembunyi");
        var audio = document.getElementById("musik");
        if (audio) {
          audio.play().then(function () {
            STATUS.suaraMusik = true;
          }).catch(function (e) {
            console.log("Autoplay dicegah browser, butuh interaksi pengguna:", e);
          });
        }
      });
    }

    // Pemilih Karakter Sampul
    var opsiKarakter = document.querySelectorAll(".karakter-opsi");
    opsiKarakter.forEach(function (btn) {
      btn.addEventListener("click", function () {
        opsiKarakter.forEach(function (b) { b.classList.remove("dipilih"); b.setAttribute("aria-pressed", "false"); });
        btn.classList.add("dipilih");
        btn.setAttribute("aria-pressed", "true");
        PEMAIN.karakter = btn.dataset.karakter || "pria";
      });
    });

    // Navigasi Denah Desa & Auto-Walk
    document.querySelectorAll("[data-pergi]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var tujuanId = btn.dataset.pergi;
        if (tujuanId) pergiKe(tujuanId);
      });
    });

    // Klik Langsung di Kanvas Peta Desa
    var kanvasPeta = document.getElementById("kanvas-peta-desa");
    if (kanvasPeta) {
      kanvasPeta.addEventListener("click", function (e) {
        var rect = kanvasPeta.getBoundingClientRect();
        var mx = (e.clientX - rect.left) / rect.width;
        var my = (e.clientY - rect.top) / rect.height;
        var targetTileX = mx * LEBAR_PETA;
        var targetTileY = my * TINGGI_PETA;

        var terdekat = TITIK_LOKASI[0];
        var minDist = 9999;
        for (var i = 0; i < TITIK_LOKASI.length; i++) {
          var t = TITIK_LOKASI[i];
          var d = Math.hypot(t.x - targetTileX, t.y - targetTileY);
          if (d < minDist) {
            minDist = d;
            terdekat = t;
          }
        }
        pergiKe(terdekat.id);
      });
    }

    // Tutup Popup
    document.querySelectorAll("[data-tutup]").forEach(function (b) {
      b.addEventListener("click", tutupPopup);
    });
    if (tiraiPopup) {
      tiraiPopup.addEventListener("click", function (e) {
        if (e.target === tiraiPopup) tutupPopup();
      });
    }

    // Salin Rekening
    document.querySelectorAll("[data-salin]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var teks = btn.dataset.salin;
        navigator.clipboard.writeText(teks).then(function () {
          var asal = btn.textContent;
          btn.textContent = "Tersalin!";
          setTimeout(function () { btn.textContent = asal; }, 2000);
        });
      });
    });

    // Form RSVP Kirim Ucapan
    var formUcapan = document.getElementById("form-ucapan");
    if (formUcapan) {
      formUcapan.addEventListener("submit", function (e) {
        e.preventDefault();
        var nama = document.getElementById("input-nama").value.trim();
        var pesan = document.getElementById("input-pesan").value.trim();
        var kehadiran = document.getElementById("input-kehadiran").value;
        var jumlah = parseInt(document.getElementById("input-jumlah").value, 10) || 1;

        if (!nama || !pesan) return;

        fetch("/api/ucapan/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || ""
          },
          body: JSON.stringify({ nama: nama, pesan: pesan, kehadiran: kehadiran, jumlah: jumlah })
        })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (res.ok) {
            alert("Terima kasih atas doa dan restunya!");
            formUcapan.reset();
            tutupPopup();
          } else {
            alert(res.pesan || "Terjadi kendala saat mengirim.");
          }
        })
        .catch(function () {
          alert("Koneksi bermasalah. Silakan coba lagi.");
        });
      });
    }

    // Tombol Peta
    var btnPeta = document.getElementById("tombol-peta");
    if (btnPeta) {
      btnPeta.addEventListener("click", function () { bukaPopup("peta"); });
    }

    // Tombol Musik (Putar / Jeda)
    var btnMusik = document.getElementById("tombol-musik");
    if (btnMusik) {
      btnMusik.addEventListener("click", function () {
        var audio = document.getElementById("musik");
        if (!audio) return;
        if (audio.paused) {
          audio.play();
          btnMusik.classList.remove("mati");
        } else {
          audio.pause();
          btnMusik.classList.add("mati");
        }
      });
    }

    // Tombol Petunjuk
    var btnPetunjuk = document.getElementById("tombol-petunjuk");
    if (btnPetunjuk) {
      btnPetunjuk.addEventListener("click", function () { bukaPopup("petunjuk"); });
    }
  }

  /* =========================================================================
     Game Loop
     ========================================================================= */
  var waktuLalu = performance.now();

  function loop(sekarang) {
    var dt = (sekarang - waktuLalu) / 1000;
    waktuLalu = sekarang;
    if (dt > 0.1) dt = 0.1;

    gerakPemain(dt);
    render(dt);

    requestAnimationFrame(loop);
  }

  // Mulai
  muatSemuaAset(function () {
    inisialisasiInput();
    updateKemajuan();
    requestAnimationFrame(loop);
  });

})();
