/* =========================================================================
   Tema 6 — "Taman Safari / Kebun Binatang Rimba Tropis" (Safari Zoo Edition)
   Fitur Utama:
   1. Koleksi Satwa Interaktif: Gajah, Jerapah, Singa, Panda, Zebra, Flamingo
   2. Respon animasi dan dialog suara lucu saat mengklik setiap satwa
   3. Pelaminan rustik kayu jati, anggrek hutan, dan kanopi bambu
   4. Bangku kayu gelondongan safari yang BISA DIDUDUKI tamu
   5. Navigasi otomatis klik BFS (Point & Click) + Analog Virtual Joystick
   ========================================================================= */
(function () {
  "use strict";

  var DATA = JSON.parse(document.getElementById("data-undangan").textContent);
  var PETAK = 48;                // 48x48 piksel per petak
  var LAJU = 3.3;                // Kecepatan jalan (petak per detik)

  var NAMA_PRIA = DATA.pria_nama || "Budi";
  var NAMA_WANITA = DATA.wanita_nama || "Rina";
  var NAMA_PASANGAN = NAMA_PRIA + " & " + NAMA_WANITA;
  var NAMA_TAMU = DATA.tamu_nama || "Tamu Undangan";

  /* ---------------------------------------------------------------------
     Denah Taman Safari (36 kolom x 28 baris = 1728 x 1344 piksel):
       . = Rumput rimba tropis hijau segar
       s = Rumput savana emas afrika
       j = Jalur setapak kerikil safari (gravel trail)
       a = Air kolam jernih biru toska
       t = Teratai air kolam dengan bunga teratai pink
       p = Pagar kayu safari horizontal (padat)
       b = Tebing bukit batu karang singa (padat)
       m = Rumpun bambu panda lebat (padat)
       k = Kayu jembatan safari
       o = Pasir oranye savana camp
       # = Batas tepi pohon rimbun (padat)
     --------------------------------------------------------------------- */
  var PETA = [
    "####################################", // 0: Batas rimbun utara (36)
    "##....ssssss...jjjjjj...ssssss....##", // 1: Panggung Pelaminan Utama (36)
    "##....ssssss...jjjjjj...ssssss....##", // 2
    "##....ssssss...jjjjjj...ssssss....##", // 3
    "##..pppppppp...jjjjjj...pppppppp..##", // 4: Pagar habitat atas (36)
    "##..s......s...jjjjjj...s......s..##", // 5: Habitat Gajah & Jerapah (36)
    "##..s......s...jjjjjj...s......s..##", // 6
    "##..s......s...jjjjjj...s......s..##", // 7
    "##..pppppppp...jjjjjj...pppppppp..##", // 8 (36)
    "##.............jjjjjj.............##", // 9: Jalur utama (36)
    "##...bbbbbb....jaaaaj....mmmmmm...##", // 10: Bukit Singa & Bambu Panda (36)
    "##...b....b....jttttj....m....m...##", // 11 (36)
    "##...b....b....jttttj....m....m...##", // 12: Danau Teratai & Flamingo (36)
    "##...bbbbbb....jaaaaj....mmmmmm...##", // 13 (36)
    "##.............jjjjjj.............##", // 14 (36)
    "##..jjjjjjjjjjjjjjjjjjjjjjjjjj..##", // 15: Jalur persimpangan melintang (36)
    "##..jjjjjjjjjjjjjjjjjjjjjjjjjj..##", // 16: Papan Acara & Galeri Foto (36)
    "##.............jjjjjj.............##", // 17 (36)
    "##..pppppppp...jjjjjj...oooooooo..##", // 18: Habitat Zebra & Pos Jeep (36)
    "##..s......s...jjjjjj...o......o..##", // 19 (36)
    "##..s......s...jjjjjj...o......o..##", // 20 (36)
    "##..s......s...jjjjjj...o......o..##", // 21 (36)
    "##..pppppppp...jjjjjj...oooooooo..##", // 22 (36)
    "##.............jjjjjj.............##", // 23 (36)
    "##.............jjjjjj.............##", // 24 (36)
    "##.............jjjjjj.............##", // 25: Gerbang Masuk Safari (36)
    "##.............jjjjjj.............##", // 26 (36)
    "####################################"  // 27: Batas selatan (36)
  ];

  var INDEKS_PETAK = {
    "s": 0, ".": 1, "j": 2, "a": 3, "t": 4, "p": 5,
    "b": 6, "m": 8, "k": 10, "o": 11, "#": 12
  };

  var PADAT = { "p": true, "b": true, "m": true, "a": true, "t": true, "#": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * PETAK;
  var TINGGI_DUNIA = TINGGI_PETA * PETAK;

  /* ---------------------------------------------------------------------
     Titik Lokasi Utama Pernikahan (5 Zona Interaktif)
     --------------------------------------------------------------------- */
  var TITIK_LOKASI = [
    { id: "pengantin", nomor: 1, nama: "Pelaminan Safari Rimba", x: 18.0, y: 3.6, ikon: "👑" },
    { id: "acara",     nomor: 2, nama: "Papan Petunjuk Safari",   x: 14.5, y: 16.0, ikon: "📜" },
    { id: "galeri",    nomor: 3, nama: "Galeri Foto Tali Rami",   x: 21.5, y: 16.0, ikon: "📷" },
    { id: "ucapan",    nomor: 4, nama: "Pos Ranger & RSVP",       x: 21.5, y: 8.5, ikon: "🍱" },
    { id: "hadiah",    nomor: 5, nama: "Peti Koper Petualang",    x: 14.5, y: 8.5, ikon: "🎁" }
  ];

  /* ---------------------------------------------------------------------
     Bangku-Bangku Kayu Gelondongan Safari (BISA DIDUDUKI)
     --------------------------------------------------------------------- */
  var BANGKU_LIST = [
    { id: "bg1", x: 14.8, y: 7.2, arah: "kanan" },
    { id: "bg2", x: 21.2, y: 7.2, arah: "kiri" },
    { id: "bg3", x: 14.8, y: 14.2, arah: "kanan" },
    { id: "bg4", x: 21.2, y: 14.2, arah: "kiri" },
    { id: "bg5", x: 14.8, y: 18.8, arah: "kanan" },
    { id: "bg6", x: 21.2, y: 18.8, arah: "kiri" }
  ];

  /* ---------------------------------------------------------------------
     Daftar Objek Pernikahan & Satwa Kebun Binatang Interaktif
     --------------------------------------------------------------------- */
  var OBJEK = [
    // 1. Pelaminan Safari Rimba Tropis di Utara
    {
      gambar: "pelaminan", x: 18.0, y: 3.4, padat: [3.8, 1.4],
      zona: "pengantin", label: "Pelaminan Safari Rimba", sublabel: NAMA_PASANGAN, ikon: "👑"
    },
    {
      gambar: "pengantin_pria", x: 17.2, y: 3.4, padat: [0.5, 0.3],
      zona: "pengantin"
    },
    {
      gambar: "pengantin_wanita", x: 18.8, y: 3.4, padat: [0.5, 0.3],
      zona: "pengantin"
    },

    // 2. SATWA-SATWA KEBUN BINATANG INTERAKTIF:
    // Gajah Safari di Habitat Kolam Barat Laut
    {
      gambar: "gajah", x: 7.5, y: 6.5, padat: [1.8, 1.4],
      label: "Gajah Safari Berbunga", sublabel: "Habitat Rindang", ikon: "🐘",
      pesan: "🐘 *Barooo!* Gajah belalai bergoyang bahagia mengucapkan selamat menempuh hidup baru kepada mempelai!"
    },

    // Jerapah Tinggi di Padang Savana Timur Laut
    {
      gambar: "jerapah", x: 28.5, y: 6.5, padat: [1.2, 2.0],
      label: "Jerapah Jenjang Savana", sublabel: "Padang Akasia", ikon: "🦒",
      pesan: "🦒 *Nyam nyam!* Jerapah tersenyum ramah mengunyah pucuk daun akasia menyambut kehadiran Anda."
    },

    // Singa Raja Rimba di Bukit Batu Barat Tengah
    {
      gambar: "singa", x: 7.5, y: 12.5, padat: [1.5, 1.2],
      label: "Singa Raja Rimba", sublabel: "Bukit Karang Safari", ikon: "🦁",
      pesan: "🦁 *Roaaar gagah!* Sang raja rimba bersantai di atas batu karang merestui ikatan cinta kedua mempelai."
    },

    // Panda Gemas di Rumpun Bambu Timur Tengah
    {
      gambar: "panda", x: 28.5, y: 12.5, padat: [1.1, 1.1],
      label: "Panda Rebung Bambu", sublabel: "Rumpun Bambu Hijau", ikon: "🐼",
      pesan: "🐼 *Kruyuk nyam!* Panda gemas melambaikan tangannya sambil mengunyah rebung bambu segar."
    },

    // Zebra Belang di Padang Savana Barat Daya
    {
      gambar: "zebra", x: 7.5, y: 20.5, padat: [1.4, 1.1],
      label: "Zebra Belang Safari", sublabel: "Padang Rumput Savana", ikon: "🦓",
      pesan: "🦓 *Hihihi!* Zebra belang melompat riang di padang rumput menyemarakkan pesta pernikahan alam ini."
    },

    // Burung Flamingo Anggun di Danau Teratai Tengah
    {
      gambar: "flamingo", x: 16.8, y: 11.5,
      label: "Flamingo Danau Teratai 1", sublabel: "Danau Tengah", ikon: "🦩",
      pesan: "🦩 *Flap flap!* Burung flamingo anggun berdiri satu kaki mengibaskan sayap merah mudanya yang memukau."
    },
    {
      gambar: "flamingo", x: 19.2, y: 12.0,
      label: "Flamingo Danau Teratai 2", sublabel: "Danau Tengah", ikon: "🦩",
      pesan: "🦩 *Chirp!* Pasangan flamingo menari romantis di atas riak air danau teratai."
    },

    // 3. OBJEK PERNIKAHAN SAFARI:
    // Plang Petunjuk Arah Kayu Safari
    {
      gambar: "papan", x: 14.5, y: 16.0, padat: [1.1, 0.8],
      zona: "acara", label: "Papan Petunjuk Safari", sublabel: "Akad, Resepsi & Rute", ikon: "📜"
    },

    // Galeri Foto Prewedding Tali Rami Safari
    {
      gambar: "galeri", x: 21.5, y: 16.0, padat: [1.8, 0.8],
      zona: "galeri", label: "Galeri Foto Tali Rami", sublabel: "Potret Petualangan", ikon: "📷"
    },

    // Pos Ranger Safari Lodge Buku Tamu & RSVP
    {
      gambar: "buku_tamu", x: 21.5, y: 8.5, padat: [1.6, 0.9],
      zona: "ucapan", label: "Pos Ranger & RSVP", sublabel: "Buku Jurnal Tamu", ikon: "🍱"
    },

    // Peti Koper Petualang Vintage (Amplop & Hadiah)
    {
      gambar: "hadiah", x: 14.5, y: 8.5, padat: [0.9, 0.8],
      zona: "hadiah", label: "Peti Koper Petualang", sublabel: "Amplop Digital & QRIS", ikon: "🎁"
    },

    // Mobil Jeep Safari 4x4 di Pintu Masuk Tenggara
    {
      gambar: "jeep_safari", x: 26.5, y: 20.5, padat: [2.0, 1.0],
      label: "Jeep Safari Petualang 4x4", sublabel: "Kendaraan Ekspedisi", ikon: "🚙",
      pesan: "🚙 Mobil Jeep 4x4 terbuka berhias rangkaian bunga liar, siap mengantar petualangan cinta kedua mempelai!"
    }
  ];

  /* Status Pemain - SPAWN DI GERBANG SELATAN */
  var PEMAIN = {
    x: 18.0,
    y: 24.5, // Pintu masuk selatan di atas jalan kerikil
    arah: "atas",
    frame: 0,
    jalan: false,
    karakter: "pria",
    sedangJalanOtomatis: false,
    jalurOtomatis: [],
    targetZona: null,
    sedangDuduk: false,
    bangkuAktif: null,
    label: NAMA_TAMU,
    sublabel: "Safari Explorer",
    ikon: "🧭"
  };

  var STATUS = {
    dikunjungi: {},
    zonaAktif: null,
    waktuAnimasi: 0,
    suaraMusik: false,
    objekHover: null,
    skalaKamera: 1.0,
    kameraX: 0,
    kameraY: 0,
    hewanDekat: null
  };

  /* Input Controls */
  var INPUT = {
    atas: false, bawah: false, kiri: false, kanan: false,
    analogAktif: false, analogDx: 0, analogDy: 0
  };

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
    }, 3600);
  }

  var tombolTutupToast = document.getElementById("tutup-toast");
  if (tombolTutupToast && toastNotif) {
    tombolTutupToast.addEventListener("click", function (e) {
      e.stopPropagation();
      clearTimeout(toastNotif._timer);
      toastNotif.hidden = true;
    });
  }

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
     Fisika Gerak & Validasi Lintasan
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

    if (PEMAIN.sedangDuduk) {
      PEMAIN.sedangDuduk = false;
      PEMAIN.bangkuAktif = null;
    }

    tutupPopup();
    tampilkanToast("🧭 Menuju " + titik.nama + "…");

    var jalur = cariJalur(PEMAIN.x, PEMAIN.y, titik.x, titik.y);
    PEMAIN.jalurOtomatis = jalur;
    PEMAIN.sedangJalanOtomatis = true;
    PEMAIN.targetZona = lokasiId;
  }

  /* =========================================================================
     Sistem Duduk di Bangku Kayu Safari
     ========================================================================= */
  function dudukkanPemain(bangku) {
    if (!bangku) return;
    PEMAIN.sedangDuduk = true;
    PEMAIN.bangkuAktif = bangku;
    PEMAIN.waktuDuduk = performance.now();
    PEMAIN.x = bangku.x;
    PEMAIN.y = bangku.y - 0.08;
    PEMAIN.arah = bangku.arah || "bawah";
    PEMAIN.jalan = false;
    PEMAIN.sedangJalanOtomatis = false;
    PEMAIN.jalurOtomatis = [];
    tampilkanToast("🪑 Anda sedang duduk santai menikmati semilir angin dan suasana kebun binatang.");
  }

  function berdiriPemain() {
    if (PEMAIN.sedangDuduk) {
      PEMAIN.sedangDuduk = false;
      PEMAIN.bangkuAktif = null;
    }
  }

  function cariBangkuTerdekat(x, y) {
    for (var i = 0; i < BANGKU_LIST.length; i++) {
      var b = BANGKU_LIST[i];
      if (Math.hypot(x - b.x, y - b.y) < 1.1) {
        return b;
      }
    }
    return null;
  }

  function gerakPemain(dt) {
    var vx = 0;
    var vy = 0;

    if (INPUT.analogAktif || INPUT.kiri || INPUT.kanan || INPUT.atas || INPUT.bawah) {
      if (PEMAIN.sedangDuduk) {
        berdiriPemain();
      }
      if (PEMAIN.sedangJalanOtomatis) {
        PEMAIN.sedangJalanOtomatis = false;
        PEMAIN.jalurOtomatis = [];
        PEMAIN.targetZona = null;
        if (toastNotif) toastNotif.hidden = true;
      }
    }

    if (PEMAIN.sedangDuduk) {
      PEMAIN.jalan = false;
      PEMAIN.frame = 0;
      return;
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

      if (bisaDilewati(PEMAIN.x + dx + (dx > 0 ? radius : -radius), PEMAIN.y)) {
        PEMAIN.x += dx;
      }
      if (bisaDilewati(PEMAIN.x, PEMAIN.y + dy + (dy > 0 ? radius : -radius))) {
        PEMAIN.y += dy;
      }

      STATUS.waktuAnimasi += dt * 6.5;
      PEMAIN.frame = Math.floor(STATUS.waktuAnimasi) % 4;
    } else {
      PEMAIN.jalan = false;
      PEMAIN.frame = 0;
    }

    // Cek Interaksi Lokasi
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

    // Cek Satwa Terdekat untuk Notifikasi Habitat
    var hewanDekat = null;
    for (var j = 0; j < OBJEK.length; j++) {
      var ob = OBJEK[j];
      if (ob.pesan && Math.hypot(PEMAIN.x - ob.x, PEMAIN.y - ob.y) < 2.4) {
        hewanDekat = ob;
        break;
      }
    }
    STATUS.hewanDekat = hewanDekat;
    var chipHabitat = document.getElementById("chip-habitat-indikator");
    if (chipHabitat) {
      if (hewanDekat) {
        chipHabitat.innerHTML = "<span>" + (hewanDekat.ikon || "🦁") + "</span> " + hewanDekat.label;
      } else if (zonaDitemukan) {
        chipHabitat.innerHTML = "<span>" + (zonaDitemukan.ikon || "📍") + "</span> " + zonaDitemukan.nama;
      } else {
        chipHabitat.innerHTML = "<span>🌿</span> TAMAN SAFARI NUSANTARA";
      }
    }

    // Tombol Aksi
    var bangkuDekat = cariBangkuTerdekat(PEMAIN.x, PEMAIN.y);
    var btnAksi = document.getElementById("tombol-aksi");
    if (btnAksi) {
      if (PEMAIN.sedangDuduk) {
        btnAksi.textContent = "↑";
        btnAksi.style.transform = "scale(1.15)";
      } else if (bangkuDekat) {
        btnAksi.textContent = "🪑";
        btnAksi.style.transform = "scale(1.15)";
      } else if (hewanDekat) {
        btnAksi.textContent = "🐾";
        btnAksi.style.transform = "scale(1.18)";
      } else {
        btnAksi.textContent = "!";
        btnAksi.style.transform = zonaDitemukan ? "scale(1.18)" : "scale(1)";
      }
    }
  }

  function kotakBulat(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y);
    c.arcTo(x + w, y, x + w, y + h, r);
    c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r);
    c.arcTo(x, y, x + w, y, r);
    c.closePath();
  }

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
      warnaStatus = "#e8dfcc";
    }

    ctx.font = "bold 11px 'Nunito', sans-serif";
    var lebarJudul = ctx.measureText(judul).width;
    ctx.font = "bold 9px 'Nunito', sans-serif";
    var lebarStatus = statusTeks ? ctx.measureText(statusTeks).width : 0;

    var padX = 8;
    var w = Math.max(lebarJudul, lebarStatus) + padX * 2;
    var h = statusTeks ? 27 : 18;

    var goyang = Math.sin(STATUS.waktuAnimasi * 2.5 + (item.x || 0) * 3) * 2;
    var lx = xPx - w / 2;
    var ly = yPx - tinggiSprite - h - 8 + goyang;

    item._labelBox = { x: lx, y: ly, w: w, h: h };

    var isHover = (STATUS.objekHover === item);
    var isDekat = (STATUS.zonaAktif && STATUS.zonaAktif.id === item.zona) || (STATUS.hewanDekat === item);

    ctx.save();
    if (isHover || isDekat) {
      ctx.shadowColor = "rgba(244, 190, 88, 0.9)";
      ctx.shadowBlur = 10;
    } else {
      ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
      ctx.shadowBlur = 4;
    }

    kotakBulat(ctx, lx, ly, w, h, 6);
    ctx.fillStyle = isHover
      ? "rgba(34, 68, 38, 0.96)"
      : (item.zona ? "rgba(20, 48, 24, 0.94)" : "rgba(14, 30, 16, 0.88)");
    ctx.fill();

    ctx.strokeStyle = isHover || isDekat
      ? "#fff2b8"
      : (item.zona ? (STATUS.dikunjungi[item.zona] ? "#74c74a" : "#d49b35") : "#94723a");
    ctx.lineWidth = isHover || isDekat ? 2.2 : 1.5;
    ctx.stroke();

    ctx.fillStyle = ctx.strokeStyle;
    ctx.beginPath();
    ctx.moveTo(xPx - 4, ly + h);
    ctx.lineTo(xPx + 4, ly + h);
    ctx.lineTo(xPx, ly + h + 4);
    ctx.closePath();
    ctx.fill();
    ctx.restore();

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 11px 'Nunito', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(judul, xPx, ly + (statusTeks ? 9 : h / 2));

    if (statusTeks) {
      ctx.fillStyle = warnaStatus;
      ctx.font = "bold 9px 'Nunito', sans-serif";
      ctx.fillText(statusTeks, xPx, ly + 19);
    }
  }

  /* =========================================================================
     Render Dunia (Canvas 2D)
     ========================================================================= */
  function render(dt) {
    if (kanvas.width !== window.innerWidth || kanvas.height !== window.innerHeight) {
      kanvas.width = window.innerWidth;
      kanvas.height = window.innerHeight;
      ctx.imageSmoothingEnabled = false;
    }

    var skala = window.innerWidth > 1400 ? 1.25 : (window.innerWidth > 900 ? 1.12 : 1.0);
    var lebarTampak = kanvas.width / skala;
    var tinggiTampak = kanvas.height / skala;

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

    // 1. Gambar Ubin (Tiles)
    var imgTiles = GAMBAR.tileset;
    var minTX = Math.floor(kameraX / PETAK) - 1;
    var maxTX = Math.ceil((kameraX + lebarTampak) / PETAK) + 1;
    var minTY = Math.floor(kameraY / PETAK) - 1;
    var maxTY = Math.ceil((kameraY + tinggiTampak) / PETAK) + 1;

    for (var ty = minTY; ty <= maxTY; ty++) {
      for (var tx = minTX; tx <= maxTX; tx++) {
        var luar = tx < 0 || ty < 0 || tx >= LEBAR_PETA || ty >= TINGGI_PETA;
        var idx = 1; // Default rumput rimba

        if (!luar) {
          var kode = PETA[ty][tx];
          idx = INDEKS_PETAK[kode] !== undefined ? INDEKS_PETAK[kode] : 1;
        } else {
          idx = 12; // Rimbun batas luar
        }

        if (imgTiles) {
          ctx.drawImage(imgTiles, idx * PETAK, 0, PETAK, PETAK, tx * PETAK, ty * PETAK, PETAK, PETAK);
        }
      }
    }

    // 2. Kumpulkan Entitas untuk Y-Sorting
    var daftarGambar = [];

    for (var oi = 0; oi < OBJEK.length; oi++) {
      var ob = OBJEK[oi];
      daftarGambar.push({ tipe: "objek", y: ob.y, data: ob });
    }

    for (var bi = 0; bi < BANGKU_LIST.length; bi++) {
      var bg = BANGKU_LIST[bi];
      daftarGambar.push({ tipe: "bangku", y: bg.y, data: bg });
    }

    daftarGambar.push({ tipe: "pemain", y: PEMAIN.y, data: PEMAIN });

    daftarGambar.sort(function (a, b) {
      return a.y - b.y;
    });

    for (var di = 0; di < daftarGambar.length; di++) {
      var ent = daftarGambar[di];
      if (ent.tipe === "objek") gambarObjek(ent.data);
      else if (ent.tipe === "bangku") gambarBangku(ent.data);
      else if (ent.tipe === "pemain") gambarPemain(ent.data);
    }

    // 3. Render Floating Nameplate di Atas Objek & Satwa
    for (var li = 0; li < OBJEK.length; li++) {
      var oItem = OBJEK[li];
      if (oItem.label) {
        var gImg = GAMBAR[oItem.gambar];
        var tSprite = gImg ? gImg.height : 48;
        gambarLabel(oItem, oItem.x * PETAK, oItem.y * PETAK, tSprite);
      }
    }

    // Label Pemain (status duduk hanya tampil 3.5 detik pertama, lalu hilang sendiri)
    if (PEMAIN.sedangDuduk) {
      if (performance.now() - (PEMAIN.waktuDuduk || 0) < 3500) {
        gambarLabel({
          label: PEMAIN.label + " (Duduk Santai)",
          sublabel: "Tekan tombol gerak untuk berdiri",
          ikon: "🪑"
        }, PEMAIN.x * PETAK, PEMAIN.y * PETAK, 60);
      }
    } else {
      gambarLabel(PEMAIN, PEMAIN.x * PETAK, PEMAIN.y * PETAK, 78);
    }

    ctx.restore();
  }

  function gambarObjek(ob) {
    var img = GAMBAR[ob.gambar];
    if (!img) return;

    var bernapas = 0;
    // Satwa memiliki animasi bernapas / gerakan halus
    if (["gajah", "jerapah", "singa", "panda", "zebra", "flamingo"].indexOf(ob.gambar) !== -1) {
      bernapas = Math.sin(STATUS.waktuAnimasi * 2.0 + ob.x * 2) * 1.5;
    }

    var x = ob.x * PETAK - img.width / 2;
    var y = ob.y * PETAK - img.height + 8 + bernapas;
    ctx.drawImage(img, Math.round(x), Math.round(y));
  }

  function gambarBangku(bg) {
    var img = GAMBAR.bangku;
    if (!img) return;
    var x = bg.x * PETAK - img.width / 2;
    var y = bg.y * PETAK - img.height + 10;
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

    if (p.sedangDuduk) {
      dy += 12;
      sx = 0;
      sy = 0;
    }

    // Bayangan Kaki
    ctx.fillStyle = "rgba(10, 24, 12, 0.45)";
    ctx.beginPath();
    ctx.ellipse(p.x * PETAK, p.y * PETAK + (p.sedangDuduk ? 4 : 0), 14, 6, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.drawImage(img, sx, sy, fw, fh, Math.round(dx), Math.round(dy), fw, fh);
  }

  /* =========================================================================
     Denah Mini Peta Safari
     ========================================================================= */
  function gambarDenahSafari() {
    var kanvasPeta = document.getElementById("kanvas-peta-safari");
    if (!kanvasPeta) return;
    var mCtx = kanvasPeta.getContext("2d");
    kanvasPeta.width = 460;
    kanvasPeta.height = 240;

    var skalaPetaX = kanvasPeta.width / LEBAR_PETA;
    var skalaPetaY = kanvasPeta.height / TINGGI_PETA;

    for (var ty = 0; ty < TINGGI_PETA; ty++) {
      for (var tx = 0; tx < LEBAR_PETA; tx++) {
        var kd = PETA[ty][tx];
        var warna = "#2e5e34"; // Rumput rimba
        if (kd === "j") warna = "#d4c29c"; // Jalan kerikil
        else if (kd === "s") warna = "#c4af6a"; // Savana emas
        else if (kd === "a" || kd === "t") warna = "#3494a8"; // Air kolam
        else if (kd === "b") warna = "#7a7064"; // Bukit singa
        else if (kd === "m") warna = "#58a442"; // Bambu panda
        else if (kd === "p") warna = "#683e22"; // Pagar kayu
        else if (kd === "o") warna = "#c8945a"; // Pasir safari

        mCtx.fillStyle = warna;
        mCtx.fillRect(tx * skalaPetaX, ty * skalaPetaY, skalaPetaX + 0.5, skalaPetaY + 0.5);
      }
    }

    // Pin Lokasi Tujuan
    for (var i = 0; i < TITIK_LOKASI.length; i++) {
      var t = TITIK_LOKASI[i];
      var px = t.x * skalaPetaX;
      var py = t.y * skalaPetaY;

      mCtx.fillStyle = STATUS.dikunjungi[t.id] ? "#38b000" : "#d49b35";
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

    // Posisi Pemain
    var pemX = PEMAIN.x * skalaPetaX;
    var pemY = PEMAIN.y * skalaPetaY;
    mCtx.fillStyle = "#ffdd00";
    mCtx.beginPath();
    mCtx.arc(pemX, pemY, 6, 0, Math.PI * 2);
    mCtx.fill();
    mCtx.strokeStyle = "#101624";
    mCtx.lineWidth = 2;
    mCtx.stroke();
  }

  /* =========================================================================
     Interaksi Modal Popup
     ========================================================================= */
  var tiraiPopup = document.getElementById("tirai-popup");

  function bukaPopup(id) {
    if (!id || !tiraiPopup) return;
    STATUS.dikunjungi[id] = true;
    updateKemajuan();

    var semuaPopup = tiraiPopup.querySelectorAll(".popup-safari");
    semuaPopup.forEach(function (p) { p.hidden = true; });

    var targetPopup = document.getElementById("popup-" + id);
    if (targetPopup) {
      targetPopup.hidden = false;
      targetPopup.style.display = "block";
      tiraiPopup.hidden = false;
      tiraiPopup.style.display = "flex";
      tiraiPopup.style.pointerEvents = "auto";
      if (id === "peta") {
        setTimeout(gambarDenahSafari, 40);
      }
    }
  }

  function tutupPopup() {
    if (tiraiPopup) {
      tiraiPopup.hidden = true;
      tiraiPopup.style.display = "none";
      tiraiPopup.style.pointerEvents = "none";
      var semuaPopup = tiraiPopup.querySelectorAll(".popup-safari");
      semuaPopup.forEach(function (p) {
        p.hidden = true;
        p.style.display = "none";
      });
    }
  }

  function updateKemajuan() {
    var total = TITIK_LOKASI.length;
    var selesai = Object.keys(STATUS.dikunjungi).length;
    var elKemajuan = document.getElementById("hud-kemajuan-angka");
    if (elKemajuan) elKemajuan.textContent = selesai + "/" + total;
  }

  /* =========================================================================
     Deteksi Klik Langsung pada Satwa, Objek, Bangku & Kanvas
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

    var b = cariBangkuTerdekat(pos.wx, pos.wy);
    if (b) {
      return { tipe: "bangku", data: b };
    }

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

    for (var t = 0; t < TITIK_LOKASI.length; t++) {
      var tk = TITIK_LOKASI[t];
      if (Math.hypot(pos.wx - tk.x, pos.wy - tk.y) < 1.5) {
        for (var k2 = 0; k2 < OBJEK.length; k2++) {
          if (OBJEK[k2].zona === tk.id) return OBJEK[k2];
        }
      }
    }

    return null;
  }

  /* =========================================================================
     Input Listeners & Joystick Virtual
     ========================================================================= */
  function inisialisasiInput() {
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
        if (PEMAIN.sedangDuduk) {
          berdiriPemain();
        } else {
          var bangkuDekat = cariBangkuTerdekat(PEMAIN.x, PEMAIN.y);
          if (bangkuDekat) {
            dudukkanPemain(bangkuDekat);
          } else if (STATUS.hewanDekat && STATUS.hewanDekat.pesan) {
            tampilkanToast(STATUS.hewanDekat.pesan);
          } else if (STATUS.zonaAktif) {
            bukaPopup(STATUS.zonaAktif.id);
          }
        }
      }
    });

    window.addEventListener("keyup", function (e) {
      var k = e.key.toLowerCase();
      if (k === "w" || k === "arrowup") INPUT.atas = false;
      if (k === "s" || k === "arrowdown") INPUT.bawah = false;
      if (k === "a" || k === "arrowleft") INPUT.kiri = false;
      if (k === "d" || k === "arrowright") INPUT.kanan = false;
    });

    // Virtual Joystick Analog
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

    // Klik Kanvas
    var pointerAwal = { x: 0, y: 0 };
    kanvas.addEventListener("pointerdown", function (e) {
      pointerAwal.x = e.clientX;
      pointerAwal.y = e.clientY;
    });

    kanvas.addEventListener("pointerup", function (e) {
      if (Math.hypot(e.clientX - pointerAwal.x, e.clientY - pointerAwal.y) > 10) return;

      var pos = hitungKoordinatDunia(e.clientX, e.clientY);
      var target = cariObjekKlik(pos);

      // Jika klik bangku kayu safari:
      if (target && target.tipe === "bangku") {
        var bg = target.data;
        var jarakBangku = Math.hypot(PEMAIN.x - bg.x, PEMAIN.y - bg.y);
        if (jarakBangku < 1.2) {
          dudukkanPemain(bg);
        } else {
          berdiriPemain();
          tampilkanToast("🪑 Menuju bangku safari…");
          var jalurB = cariJalur(PEMAIN.x, PEMAIN.y, bg.x, bg.y);
          if (jalurB && jalurB.length > 0) {
            PEMAIN.jalurOtomatis = jalurB;
            PEMAIN.sedangJalanOtomatis = true;
            PEMAIN.targetZona = null;
            var cekTiba = setInterval(function () {
              if (!PEMAIN.sedangJalanOtomatis) {
                clearInterval(cekTiba);
                if (Math.hypot(PEMAIN.x - bg.x, PEMAIN.y - bg.y) < 1.2) {
                  dudukkanPemain(bg);
                }
              }
            }, 100);
          }
        }
        return;
      }

      if (PEMAIN.sedangDuduk) {
        berdiriPemain();
      }

      if (target) {
        if (target.zona) {
          var jarakPemain = Math.hypot(PEMAIN.x - target.x, PEMAIN.y - target.y);
          if (jarakPemain <= 2.5) {
            bukaPopup(target.zona);
          } else {
            pergiKe(target.zona);
          }
          return;
        }

        // Jika mengklik hewan:
        if (target.pesan) {
          tampilkanToast(target.pesan);
          return;
        }
      }

      // Klik tanah bebas
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

    kanvas.addEventListener("pointermove", function (e) {
      var pos = hitungKoordinatDunia(e.clientX, e.clientY);
      var target = cariObjekKlik(pos);
      if (target && (target.zona || target.pesan || target.tipe === "bangku")) {
        kanvas.style.cursor = "pointer";
        STATUS.objekHover = target;
      } else {
        kanvas.style.cursor = "default";
        STATUS.objekHover = null;
      }
    });

    var btnAksi = document.getElementById("tombol-aksi");
    if (btnAksi) {
      btnAksi.addEventListener("click", function () {
        if (PEMAIN.sedangDuduk) {
          berdiriPemain();
        } else {
          var bangkuDekat = cariBangkuTerdekat(PEMAIN.x, PEMAIN.y);
          if (bangkuDekat) {
            dudukkanPemain(bangkuDekat);
          } else if (STATUS.hewanDekat && STATUS.hewanDekat.pesan) {
            tampilkanToast(STATUS.hewanDekat.pesan);
          } else if (STATUS.zonaAktif) {
            bukaPopup(STATUS.zonaAktif.id);
          }
        }
      });
    }

    var btnBuka = document.getElementById("tombol-buka");
    var sampul = document.getElementById("sampul");
    if (btnBuka && sampul) {
      btnBuka.addEventListener("click", function () {
        sampul.classList.add("tersembunyi");
        sampul.style.pointerEvents = "none";
        setTimeout(function () {
          sampul.style.display = "none";
        }, 600);
        var audio = document.getElementById("musik");
        if (audio) {
          audio.play().then(function () {
            STATUS.suaraMusik = true;
          }).catch(function (e) {
            console.log("Autoplay dicegah browser:", e);
          });
        }
      });
    }

    var opsiKarakter = document.querySelectorAll(".karakter-opsi");
    opsiKarakter.forEach(function (btn) {
      btn.addEventListener("click", function () {
        opsiKarakter.forEach(function (b) { b.classList.remove("dipilih"); b.setAttribute("aria-pressed", "false"); });
        btn.classList.add("dipilih");
        btn.setAttribute("aria-pressed", "true");
        PEMAIN.karakter = btn.dataset.karakter || "pria";
      });
    });

    document.querySelectorAll("[data-pergi]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var tujuanId = btn.dataset.pergi;
        if (tujuanId) pergiKe(tujuanId);
      });
    });

    var kanvasPeta = document.getElementById("kanvas-peta-safari");
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

    document.querySelectorAll("[data-tutup]").forEach(function (b) {
      b.addEventListener("click", tutupPopup);
    });
    if (tiraiPopup) {
      tiraiPopup.addEventListener("click", function (e) {
        if (e.target === tiraiPopup) tutupPopup();
      });
    }

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
            alert("Terima kasih atas doa restunya di Taman Safari!");
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

    var btnPeta = document.getElementById("tombol-peta");
    if (btnPeta) {
      btnPeta.addEventListener("click", function () { bukaPopup("peta"); });
    }

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

    var btnPetunjuk = document.getElementById("tombol-petunjuk");
    if (btnPetunjuk) {
      btnPetunjuk.addEventListener("click", function () { bukaPopup("petunjuk"); });
    }
  }

  var waktuLalu = performance.now();

  function loop(sekarang) {
    var dt = (sekarang - waktuLalu) / 1000;
    waktuLalu = sekarang;
    if (dt > 0.1) dt = 0.1;

    gerakPemain(dt);
    render(dt);

    requestAnimationFrame(loop);
  }

  muatSemuaAset(function () {
    inisialisasiInput();
    updateKemajuan();
    requestAnimationFrame(loop);
  });

})();
