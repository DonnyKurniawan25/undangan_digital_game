/* =========================================================================
   Tema 5 — "Grand Ballroom Gedung Mewah" (Modern Indoor-Outdoor Edition v4)
   Penyempurnaan Total Presisi & Simetri:
   1. 100% SIMETRIS SEMPURNA di sumbu x = 18.0
   2. Panggung pelaminan, piano, dan kue pengantin berposisi pas & proporsional
   3. Aisle marmer putih tengah lurus dan bersih tanpa tonjolan / lekukan tidak rata
   4. 16 Kursi Upacara simetris di atas karpet marun, bebas dari lorong putih
   5. Meja Bundar VIP 1 dan VIP 2 beserta 8 kursi simetris sempurna di sayap kiri & kanan
   6. Papan Acara & Dinding Galeri, serta Kotak Hadiah & Meja Resepsionis simetris
   7. Pot bunga emas tertata rapi berpasangan sejajar di kiri & kanan
   8. Dinding pembatas kokoh tanpa celah (HANYA BISA MASUK LEWAT PINTU)
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
     Denah Gedung Mewah 100% SIMETRIS (36 kolom x 28 baris = 1728 x 1344 px)
     Pusat simetri tepat di garis tengah x = 18.0 (antara kolom 17 dan 18).
     Semua elemen sisi kiri (kolom 0-15) adalah cerminan sisi kanan (kolom 20-35).
     --------------------------------------------------------------------- */
  var PETA = [
    "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww", // 0: Dinding belakang ballroom (36)
    "w.mmmmmmmmmmm..gggggg..mmmmmmmmmmm.w", // 1: Panggung pelaminan simetris (15 + 6 + 15 = 36)
    "w.mmmmmmmmmmm..gggggg..mmmmmmmmmmm.w", // 2
    "w.mmmmmmmmmmm..gggggg..mmmmmmmmmmm.w", // 3
    "w.mmmmmmmmmmm..gggggg..mmmmmmmmmmm.w", // 4
    "w.mmmmmmmmmmm..gggggg..mmmmmmmmmmm.w", // 5
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 6: Aisle marmer lurus sempurna (16 + 4 + 16 = 36)
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 7: Kursi tamu simetris kiri-kanan
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 8
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 9: Meja VIP banquet bundar
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 10
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 11
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 12: Papan LED & Galeri
    "w.mmmmmmmmmmmm..llll..mmmmmmmmmmmm.w", // 13: Meja resepsionis & hadiah
    "wwwwwwwwwwwwwwwwllllwwwwwwwwwwwwwwww", // 14: Dinding selatan solid (16 + 4 + 16 = 36)
    "kkkkkkkkkkkkkkkk[==]kkkkkkkkkkkkkkkk", // 15: Grand Entrance Pintu Kaca (16 + 4 + 16 = 36)
    "................[==]................", // 16: Lobby Porch Luar (16 + 4 + 16 = 36)
    "................[==]................", // 17: Karpet merah rapi 4 petak
    "................[==]................", // 18
    "cccccccccccccccc____cccccccccccccccc", // 19: Curb trotoar berhias rumbai emas (16 + 4 + 16 = 36)
    "pppppppppppppppppppppppppppppppppppp", // 20: Drop-off Lane Mobil (100% Aspal Bersih - 36)
    "jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj", // 21: Jalan Raya Marka Putih (100% Aspal Bersih - 36)
    "pppppppppppppppppppppppppppppppppppp", // 22: Jalan Raya Lajur Bawah (100% Aspal Bersih - 36)
    "cccccccccccccccccccccccccccccccccccc", // 23: Curb seberang jalan (36)
    "tttttttttttttt........tttttttttttttt", // 24: Taman Plaza Seberang (14 + 8 + 14 = 36)
    "tttttttttttttt........tttttttttttttt", // 25
    "ssssssssssssss........ssssssssssssss", // 26: Semak hias taman (14 + 8 + 14 = 36)
    "cccccccccccccccccccccccccccccccccccc"  // 27: Batas pedestrian bersih (36)
  ];

  var INDEKS_PETAK = {
    "p": 0, ".": 1, "t": 2, "j": 3, "c": 4,
    "[": 5,  // Karpet merah sisi kiri (lis emas kiri)
    "k": 7,  // Dinding kaca fasad gedung
    "m": 8,  // Karpet ballroom beludru marun
    "l": 9,  // Lantai dansa marmer kilau
    "g": 10, // Panggung kayu polished
    "w": 11, // Dinding panel akustik marmer (bebas kotak)
    "b": 12, // Pilar marmer
    "s": 13, // Semak boxwood
    "=": 14, // Karpet merah tengah (beludru murni halus)
    "]": 15, // Karpet merah sisi kanan (lis emas kanan)
    "_": 16  // Ujung karpet rumbai emas di curb
  };

  var PADAT = { "w": true, "k": true, "s": true };

  var LEBAR_PETA = PETA[0].length;
  var TINGGI_PETA = PETA.length;
  var LEBAR_DUNIA = LEBAR_PETA * PETAK;
  var TINGGI_DUNIA = TINGGI_PETA * PETAK;

  /* Garis Y transisi pintu gedung */
  var BATAS_PINTU_Y = 15.6;

  /* ---------------------------------------------------------------------
     Titik Tujuan Interaktif (5 Lokasi Utama - 100% Simetris Sempurna)
     Pusat = 18.0. Selisih jarak kiri dan kanan sama persis!
     --------------------------------------------------------------------- */
  var TITIK_LOKASI = [
    { id: "pengantin", nomor: 1, nama: "Pelaminan Grand Ballroom", x: 18.0, y: 4.8, ikon: "👑" },
    { id: "acara",     nomor: 2, nama: "Papan LED Acara",          x: 6.5,  y: 12.8, ikon: "📜" }, // 18.0 - 11.5 = 6.5
    { id: "galeri",    nomor: 3, nama: "Dinding Galeri Emas",       x: 29.5, y: 12.8, ikon: "📷" }, // 18.0 + 11.5 = 29.5
    { id: "hadiah",    nomor: 4, nama: "Kotak Hadiah Akrilik",      x: 10.0, y: 14.0, ikon: "🎁" }, // 18.0 - 8.0 = 10.0
    { id: "ucapan",    nomor: 5, nama: "Meja Resepsionis & RSVP",   x: 26.0, y: 14.0, ikon: "🍱" }  // 18.0 + 8.0 = 26.0
  ];

  /* ---------------------------------------------------------------------
     24 Kursi Chiavari Emas Tertata Rapi, Presisi & Simetris (BISA DIDUDUKI)
     Semua kursi berada di atas karpet beludru, TIDAK MENGENAI lorong marmer!
     --------------------------------------------------------------------- */
  var KURSI_LIST = [
    // Sayap Kiri Lorong - 8 Kursi Upacara (Ceremony Seating)
    // Berada di x = 12.5 dan x = 14.2 (lorong marmer baru mulai di x = 16.0)
    { id: "k1", x: 12.5, y: 7.2, arah: "bawah" },
    { id: "k2", x: 14.2, y: 7.2, arah: "bawah" },
    { id: "k3", x: 12.5, y: 8.8, arah: "bawah" },
    { id: "k4", x: 14.2, y: 8.8, arah: "bawah" },
    { id: "k5", x: 12.5, y: 10.4, arah: "bawah" },
    { id: "k6", x: 14.2, y: 10.4, arah: "bawah" },
    { id: "k7", x: 12.5, y: 12.0, arah: "bawah" },
    { id: "k8", x: 14.2, y: 12.0, arah: "bawah" },

    // Sayap Kanan Lorong - 8 Kursi Upacara (Ceremony Seating)
    // Berada di x = 21.8 dan x = 23.5 (cerminan sempurna: 18.0 + 3.8 dan 18.0 + 5.5)
    { id: "k9",  x: 21.8, y: 7.2, arah: "bawah" },
    { id: "k10", x: 23.5, y: 7.2, arah: "bawah" },
    { id: "k11", x: 21.8, y: 8.8, arah: "bawah" },
    { id: "k12", x: 23.5, y: 8.8, arah: "bawah" },
    { id: "k13", x: 21.8, y: 10.4, arah: "bawah" },
    { id: "k14", x: 23.5, y: 10.4, arah: "bawah" },
    { id: "k15", x: 21.8, y: 12.0, arah: "bawah" },
    { id: "k16", x: 23.5, y: 12.0, arah: "bawah" },

    // Meja Bundar VIP 1 (Sayap Kiri di x = 6.5, y = 9.2 - 4 Kursi Rapi)
    { id: "k17", x: 6.5, y: 7.9, arah: "bawah" },
    { id: "k18", x: 6.5, y: 10.5, arah: "atas" },
    { id: "k19", x: 5.1, y: 9.2, arah: "kanan" },
    { id: "k20", x: 7.9, y: 9.2, arah: "kiri" },

    // Meja Bundar VIP 2 (Sayap Kanan di x = 29.5, y = 9.2 - 4 Kursi Rapi)
    { id: "k21", x: 29.5, y: 7.9, arah: "bawah" },
    { id: "k22", x: 29.5, y: 10.5, arah: "atas" },
    { id: "k23", x: 28.1, y: 9.2, arah: "kanan" },
    { id: "k24", x: 30.9, y: 9.2, arah: "kiri" }
  ];

  /* ---------------------------------------------------------------------
     Daftar Objek di Peta Dunia (100% Simetris & Proporsional)
     --------------------------------------------------------------------- */
  var OBJEK = [
    // 1. Pelaminan Grand Ballroom (Pusat Panggung di x = 18.0)
    {
      gambar: "pelaminan", x: 18.0, y: 3.8, padat: [3.8, 1.4],
      zona: "pengantin", label: "Pelaminan Mempelai", sublabel: NAMA_PASANGAN, ikon: "👑"
    },
    {
      gambar: "pengantin_pria", x: 17.2, y: 3.8, padat: [0.5, 0.3],
      zona: "pengantin"
    },
    {
      gambar: "pengantin_wanita", x: 18.8, y: 3.8, padat: [0.5, 0.3],
      zona: "pengantin"
    },

    // Grand Piano (Kiri Panggung x = 11.5) & Wedding Cake (Kanan Panggung x = 24.5)
    // Jarak dari pusat 18.0: sama-sama 6.5 petak!
    {
      gambar: "grand_piano", x: 11.5, y: 4.2, padat: [1.6, 1.2],
      label: "Grand Piano Akustik", sublabel: "Pianis & Live Music", ikon: "🎹",
      pesan: "🎹 Alunan piano klasik nan romantis menggema syahdu di seluruh ruangan ballroom."
    },
    {
      gambar: "kue_pengantin", x: 24.5, y: 4.2, padat: [1.0, 1.2],
      label: "Wedding Cake 5 Tingkat", sublabel: "Menara Kue Pengantin", ikon: "🎂",
      pesan: "🎂 Menara kue pengantin 5 tingkat megah bertabur hiasan bunga gula dan emas murni."
    },

    // 2. Papan LED Digital (x = 6.5) & 3. Dinding Galeri Emas (x = 29.5)
    // Jarak dari pusat 18.0: sama-sama 11.5 petak!
    {
      gambar: "papan", x: 6.5, y: 12.8, padat: [1.1, 0.8],
      zona: "acara", label: "Papan LED Acara", sublabel: "Akad, Resepsi & Maps", ikon: "📜"
    },
    {
      gambar: "galeri", x: 29.5, y: 12.8, padat: [1.8, 0.8],
      zona: "galeri", label: "Dinding Galeri Emas", sublabel: "Foto-foto Prewedding", ikon: "📷"
    },

    // 4. Kotak Hadiah Akrilik (x = 10.0) & 5. Meja Resepsionis VIP (x = 26.0)
    // Jarak dari pusat 18.0: sama-sama 8.0 petak!
    {
      gambar: "hadiah", x: 10.0, y: 14.0, padat: [0.9, 0.8],
      zona: "hadiah", label: "Kotak Tanda Kasih", sublabel: "Amplop Digital & QRIS", ikon: "🎁"
    },
    {
      gambar: "buku_tamu", x: 26.0, y: 14.0, padat: [1.6, 0.9],
      zona: "ucapan", label: "Meja Resepsionis & RSVP", sublabel: "Buku Tamu Digital", ikon: "🍱"
    },

    // Meja VIP Banquet Bundar (x = 6.5 dan x = 29.5 - Simetris 11.5 petak)
    { gambar: "meja_vip", x: 6.5, y: 9.2, padat: [1.5, 1.0], label: "Meja Tamu VIP 1", ikon: "🍷" },
    { gambar: "meja_vip", x: 29.5, y: 9.2, padat: [1.5, 1.0], label: "Meja Tamu VIP 2", ikon: "🍷" },

    // Pot Bunga Emas Pembatas (Pasangan Simetris di x = 15.0 dan x = 21.0)
    { gambar: "pot_bunga", x: 15.0, y: 6.2 },
    { gambar: "pot_bunga", x: 21.0, y: 6.2 },
    { gambar: "pot_bunga", x: 15.0, y: 12.5 },
    { gambar: "pot_bunga", x: 21.0, y: 12.5 },
    { gambar: "pot_bunga", x: 15.0, y: 15.2 },
    { gambar: "pot_bunga", x: 21.0, y: 15.2 },
    { gambar: "pot_bunga", x: 15.0, y: 17.5 },
    { gambar: "pot_bunga", x: 21.0, y: 17.5 },

    // PINTU MASUK GEDUNG (Tepat di tengah x = 18.0)
    {
      gambar: "pintu_gedung", x: 18.0, y: 15.0,
      label: "Grand Entrance Gedung", sublabel: "Pintu Masuk Ballroom", ikon: "🚪",
      pesan: "🚪 Pintu masuk megah Grand Ballroom. Melangkahlah ke dalam untuk melihat kemewahan pesta!"
    },

    // MOBIL PENGANTIN DI JALUR DROP-OFF LUAR
    {
      gambar: "mobil_pengantin", x: 9.0, y: 20.4, padat: [2.0, 0.9],
      label: "Mobil Pengantin Mewah", sublabel: "Drop-off Plaza Luar", ikon: "🚗",
      pesan: "🚗 Mobil pernikahan mewah berhias pita mawar putih terparkir di jalur drop-off."
    }
  ];

  /* Partikel Kilau Kristal Emas Chandelier */
  var KILAU_PARTIKEL = [];
  for (var ki = 0; ki < 36; ki++) {
    KILAU_PARTIKEL.push({
      x: 3 * PETAK + Math.random() * (30 * PETAK),
      y: 2 * PETAK + Math.random() * (12 * PETAK),
      ukuran: 2 + Math.random() * 4,
      fase: Math.random() * Math.PI * 2,
      kecepatan: 1.5 + Math.random() * 2
    });
  }

  /* Status Pemain - SPAWN DI LUAR GEDUNG DI ATAS RED CARPET */
  var PEMAIN = {
    x: 18.0,
    y: 18.0, // Tepat di atas Red Carpet di lobi pedestrian luar gedung
    arah: "atas",
    frame: 0,
    jalan: false,
    karakter: "pria",
    sedangJalanOtomatis: false,
    jalurOtomatis: [],
    targetZona: null,
    sedangDuduk: false,
    kursiAktif: null,
    label: NAMA_TAMU,
    sublabel: "Karakter Anda",
    ikon: "✨"
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
    isIndoor: false,
    pernahMasuk: false
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
     Fisika Gerak & Validasi PINTU MASUK GEDUNG (HANYA BISA MASUK LEWAT PINTU)
     ========================================================================= */
  function bisaDilewati(tx, ty) {
    if (tx < 1.0 || tx >= LEBAR_PETA - 1.0 || ty < 1.0 || ty >= TINGGI_PETA - 1.0) return false;
    var petakX = Math.floor(tx);
    var petakY = Math.floor(ty);
    if (!PETA[petakY] || !PETA[petakY][petakX]) return false;
    var kode = PETA[petakY][petakX];
    if (PADAT[kode]) return false;

    // ATURAN MUTLAK: DINDING GEDUNG PEMBATAS (y = 13.9 s.d. 15.8)
    // Karakter HANYA BISA masuk atau keluar jika berada di dalam celah pintu (x: 15.8 s.d. 20.2)
    if (ty >= 13.9 && ty <= 15.8) {
      if (tx < 15.8 || tx > 20.2) {
        return false; // Solid wall & glass facade!
      }
    }

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
      PEMAIN.kursiAktif = null;
    }

    tutupPopup();
    tampilkanToast("✨ Melangkah menuju " + titik.nama + "…");

    var jalur = cariJalur(PEMAIN.x, PEMAIN.y, titik.x, titik.y);
    PEMAIN.jalurOtomatis = jalur;
    PEMAIN.sedangJalanOtomatis = true;
    PEMAIN.targetZona = lokasiId;
  }

  /* =========================================================================
     SISTEM DUDUK DI KURSI
     ========================================================================= */
  function dudukkanPemain(kursi) {
    if (!kursi) return;
    PEMAIN.sedangDuduk = true;
    PEMAIN.kursiAktif = kursi;
    PEMAIN.waktuDuduk = performance.now();
    PEMAIN.x = kursi.x;
    PEMAIN.y = kursi.y - 0.08;
    PEMAIN.arah = kursi.arah || "bawah";
    PEMAIN.jalan = false;
    PEMAIN.sedangJalanOtomatis = false;
    PEMAIN.jalurOtomatis = [];
    tampilkanToast("🪑 Anda sedang duduk santai di kursi Grand Ballroom.");
  }

  function berdiriPemain() {
    if (PEMAIN.sedangDuduk) {
      PEMAIN.sedangDuduk = false;
      PEMAIN.kursiAktif = null;
    }
  }

  function cariKursiTerdekat(x, y) {
    for (var i = 0; i < KURSI_LIST.length; i++) {
      var k = KURSI_LIST[i];
      if (Math.hypot(x - k.x, y - k.y) < 1.0) {
        return k;
      }
    }
    return null;
  }

  function gerakPemain(dt) {
    var vx = 0;
    var vy = 0;

    // Jika sedang duduk dan ada input gerak: otomatis berdiri!
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

    // CEK TRANSISI INDOOR VS OUTDOOR
    var statusIndoorBaru = (PEMAIN.y < BATAS_PINTU_Y);
    if (statusIndoorBaru !== STATUS.isIndoor) {
      STATUS.isIndoor = statusIndoorBaru;
      var elChip = document.getElementById("chip-zona-indikator");
      if (elChip) {
        if (STATUS.isIndoor) {
          elChip.innerHTML = "<span>✨</span> GRAND BALLROOM UTAMA";
          elChip.classList.add("indoor");
          if (!STATUS.pernahMasuk) {
            STATUS.pernahMasuk = true;
            tampilkanToast("✨ Selamat datang di Grand Ballroom!");
          }
        } else {
          elChip.innerHTML = "<span>🏛️</span> LOBBY PLAZA LUAR";
          elChip.classList.remove("indoor");
        }
      }
    }

    // Cek Zona Interaksi Lokasi
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

    // Cek apakah dekat dengan kursi untuk tombol aksi
    var kursiDekat = cariKursiTerdekat(PEMAIN.x, PEMAIN.y);
    var btnAksi = document.getElementById("tombol-aksi");
    if (btnAksi) {
      if (PEMAIN.sedangDuduk) {
        btnAksi.textContent = "↑";
        btnAksi.style.transform = "scale(1.15)";
      } else if (kursiDekat) {
        btnAksi.textContent = "🪑";
        btnAksi.style.transform = "scale(1.15)";
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
      warnaStatus = "#e2d8c4";
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
    var isDekat = (STATUS.zonaAktif && STATUS.zonaAktif.id === item.zona);

    ctx.save();
    if (isHover || isDekat) {
      ctx.shadowColor = "rgba(246, 211, 101, 0.9)";
      ctx.shadowBlur = 10;
    } else {
      ctx.shadowColor = "rgba(0, 0, 0, 0.5)";
      ctx.shadowBlur = 4;
    }

    kotakBulat(ctx, lx, ly, w, h, 6);
    ctx.fillStyle = isHover
      ? "rgba(24, 34, 58, 0.96)"
      : (item.zona ? "rgba(18, 26, 46, 0.94)" : "rgba(10, 14, 26, 0.85)");
    ctx.fill();

    ctx.strokeStyle = isHover || isDekat
      ? "#fff2b8"
      : (item.zona ? (STATUS.dikunjungi[item.zona] ? "#74c74a" : "#d4af37") : "#8c6e2b");
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
     Render Dunia (Canvas 2D) - 100% SIMETRIS & BEBAS KOTAK KUNING
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
        var idx = 0; // Default plaza aspal luar

        if (!luar) {
          var kode = PETA[ty][tx];
          idx = INDEKS_PETAK[kode] !== undefined ? INDEKS_PETAK[kode] : 0;
        } else {
          // Area di luar peta: bersih tanpa kotak kuning!
          idx = (ty < 15) ? 11 : 0;
        }

        if (imgTiles) {
          ctx.drawImage(imgTiles, idx * PETAK, 0, PETAK, PETAK, tx * PETAK, ty * PETAK, PETAK, PETAK);
        }
      }
    }

    // 2. Kumpulkan Entitas untuk Y-Sorting
    var daftarGambar = [];

    // Objek Utama
    for (var oi = 0; oi < OBJEK.length; oi++) {
      var ob = OBJEK[oi];
      daftarGambar.push({ tipe: "objek", y: ob.y, data: ob });
    }

    // Kursi-kursi Chiavari Emas
    for (var ki = 0; ki < KURSI_LIST.length; ki++) {
      var kr = KURSI_LIST[ki];
      daftarGambar.push({ tipe: "kursi", y: kr.y, data: kr });
    }

    // Pemain
    daftarGambar.push({ tipe: "pemain", y: PEMAIN.y, data: PEMAIN });

    // Depth Sorting Berdasarkan Koordinat Y
    daftarGambar.sort(function (a, b) {
      return a.y - b.y;
    });

    // Render Semua Entitas
    for (var di = 0; di < daftarGambar.length; di++) {
      var ent = daftarGambar[di];
      if (ent.tipe === "objek") gambarObjek(ent.data);
      else if (ent.tipe === "kursi") gambarKursi(ent.data);
      else if (ent.tipe === "pemain") gambarPemain(ent.data);
    }

    // 3. Render Floating Nameplate di Atas Objek Penting
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

    // 4. Efek Fasad Tertutup Saat di Luar vs Kilau Kristal di Dalam
    if (!STATUS.isIndoor) {
      ctx.save();
      var gradienFasad = ctx.createLinearGradient(0, 0, 0, 15 * PETAK);
      gradienFasad.addColorStop(0, "rgba(8, 12, 22, 0.98)");
      gradienFasad.addColorStop(0.7, "rgba(12, 18, 32, 0.94)");
      gradienFasad.addColorStop(1, "rgba(18, 26, 44, 0.80)");

      ctx.fillStyle = gradienFasad;
      ctx.fillRect(0, 0, LEBAR_DUNIA, 15 * PETAK);

      // Papan ucapan selamat datang berlampu emas di atas kanopi entrance
      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 13px 'Cinzel', serif";
      ctx.textAlign = "center";
      ctx.shadowColor = "rgba(212, 175, 55, 0.9)";
      ctx.shadowBlur = 10;
      ctx.fillText("GRAND BALLROOM WEDDING CELEBRATION", 18 * PETAK, 14.2 * PETAK);
      ctx.restore();
    } else {
      // Partikel Kilau Emas Chandelier di dalam Ballroom
      ctx.save();
      for (var pi = 0; pi < KILAU_PARTIKEL.length; pi++) {
        var kp = KILAU_PARTIKEL[pi];
        kp.fase += dt * kp.kecepatan;
        var denyut = (Math.sin(kp.fase) + 1) / 2;

        ctx.fillStyle = "rgba(255, 242, 184, " + (0.3 + denyut * 0.6) + ")";
        ctx.beginPath();
        ctx.arc(kp.x, kp.y, kp.ukuran * (0.8 + denyut * 0.4), 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
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

  function gambarKursi(kr) {
    var img = GAMBAR.kursi;
    if (!img) return;
    var x = kr.x * PETAK - img.width / 2;
    var y = kr.y * PETAK - img.height + 12;
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
    ctx.fillStyle = "rgba(8, 12, 20, 0.45)";
    ctx.beginPath();
    ctx.ellipse(p.x * PETAK, p.y * PETAK + (p.sedangDuduk ? 4 : 0), 14, 6, 0, 0, Math.PI * 2);
    ctx.fill();

    ctx.drawImage(img, sx, sy, fw, fh, Math.round(dx), Math.round(dy), fw, fh);
  }

  /* =========================================================================
     Denah Mini Interaktif di Modal Peta
     ========================================================================= */
  function gambarDenahGedung() {
    var kanvasPeta = document.getElementById("kanvas-peta-gedung");
    if (!kanvasPeta) return;
    var mCtx = kanvasPeta.getContext("2d");
    kanvasPeta.width = 460;
    kanvasPeta.height = 240;

    var skalaPetaX = kanvasPeta.width / LEBAR_PETA;
    var skalaPetaY = kanvasPeta.height / TINGGI_PETA;

    for (var ty = 0; ty < TINGGI_PETA; ty++) {
      for (var tx = 0; tx < LEBAR_PETA; tx++) {
        var kd = PETA[ty][tx];
        var warna = "#2c3240";
        if (kd === "m") warna = "#7a1426";
        else if (kd === "l") warna = "#e2ddd5";
        else if (kd === "[" || kd === "=" || kd === "]" || kd === "_") warna = "#a81b32";
        else if (kd === "g") warna = "#58321a";
        else if (kd === "t") warna = "#38662c";
        else if (kd === "j") warna = "#222630";
        else if (kd === "p") warna = "#2e3442";
        else if (kd === "k") warna = "#1c324a";
        else if (kd === "w") warna = "#141c28";

        mCtx.fillStyle = warna;
        mCtx.fillRect(tx * skalaPetaX, ty * skalaPetaY, skalaPetaX + 0.5, skalaPetaY + 0.5);
      }
    }

    // Garis Pemisah Dinding Pintu Masuk
    mCtx.strokeStyle = "#d4af37";
    mCtx.lineWidth = 2;
    mCtx.beginPath();
    mCtx.moveTo(0, BATAS_PINTU_Y * skalaPetaY);
    mCtx.lineTo(kanvasPeta.width, BATAS_PINTU_Y * skalaPetaY);
    mCtx.stroke();

    // Pin Lokasi Tujuan
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

    var semuaPopup = tiraiPopup.querySelectorAll(".popup");
    semuaPopup.forEach(function (p) { p.hidden = true; });

    var targetPopup = document.getElementById("popup-" + id);
    if (targetPopup) {
      targetPopup.hidden = false;
      tiraiPopup.hidden = false;
      if (id === "peta") {
        setTimeout(gambarDenahGedung, 40);
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
     Deteksi Klik Langsung pada Objek, Kursi, & Kanvas
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
    // 1. Cek Floating Label
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

    // 2. Cek Kursi Chiavari Emas
    var k = cariKursiTerdekat(pos.wx, pos.wy);
    if (k) {
      return { tipe: "kursi", data: k };
    }

    // 3. Cek Sprite Objek
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

    // 4. Titik tujuan
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
     Event Listeners: Keyboard, Touch, Virtual Analog Joystick Mouse & HP
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
          var kursiDekat = cariKursiTerdekat(PEMAIN.x, PEMAIN.y);
          if (kursiDekat) {
            dudukkanPemain(kursiDekat);
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

    // Klik Langsung di Kanvas
    var pointerAwal = { x: 0, y: 0 };
    kanvas.addEventListener("pointerdown", function (e) {
      pointerAwal.x = e.clientX;
      pointerAwal.y = e.clientY;
    });

    kanvas.addEventListener("pointerup", function (e) {
      if (Math.hypot(e.clientX - pointerAwal.x, e.clientY - pointerAwal.y) > 10) return;

      var pos = hitungKoordinatDunia(e.clientX, e.clientY);
      var target = cariObjekKlik(pos);

      // Jika klik kursi:
      if (target && target.tipe === "kursi") {
        var kr = target.data;
        var jarakKursi = Math.hypot(PEMAIN.x - kr.x, PEMAIN.y - kr.y);
        if (jarakKursi < 1.2) {
          dudukkanPemain(kr);
        } else {
          berdiriPemain();
          tampilkanToast("🪑 Menuju kursi…");
          var jalurK = cariJalur(PEMAIN.x, PEMAIN.y, kr.x, kr.y);
          if (jalurK && jalurK.length > 0) {
            PEMAIN.jalurOtomatis = jalurK;
            PEMAIN.sedangJalanOtomatis = true;
            PEMAIN.targetZona = null;
            var cekTiba = setInterval(function () {
              if (!PEMAIN.sedangJalanOtomatis) {
                clearInterval(cekTiba);
                if (Math.hypot(PEMAIN.x - kr.x, PEMAIN.y - kr.y) < 1.2) {
                  dudukkanPemain(kr);
                }
              }
            }, 100);
          }
        }
        return;
      }

      // Jika sedang duduk dan klik tempat lain: berdiri!
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

        if (target.pesan) {
          tampilkanToast(target.pesan);
          return;
        }
      }

      // Klik pada lantai terbuka
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
      if (target && (target.zona || target.pesan || target.tipe === "kursi")) {
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
          var kursiDekat = cariKursiTerdekat(PEMAIN.x, PEMAIN.y);
          if (kursiDekat) {
            dudukkanPemain(kursiDekat);
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

    var kanvasPeta = document.getElementById("kanvas-peta-gedung");
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
