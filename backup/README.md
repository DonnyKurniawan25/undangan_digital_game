# Backup Database & Media Jelajah

Backup ini diambil pada tanggal 7 November 2026 sebelum pembersihan server.

## Struktur Backup:
- `database/jelajah_db_backup.sql`: Full MySQL dump database `jelajah_db`
- `database/jelajah_db_backup.sql.gz`: Dump terkompresi
- `media/`: Semua file media upload (galeri, pengantin)
- `configs/`: Template konfigurasi systemd, nginx, dan env

## Cara Restore:
1. Buat database di MySQL:
   ```bash
   mysql -u root -e "CREATE DATABASE jelajah_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   mysql -u root -e "CREATE USER 'jelajah_app'@'127.0.0.1' IDENTIFIED BY 'password-anda';"
   mysql -u root -e "GRANT ALL PRIVILEGES ON jelajah_db.* TO 'jelajah_app'@'127.0.0.1'; FLUSH PRIVILEGES;"
   mysql -u root jelajah_db < backup/database/jelajah_db_backup.sql
   ```
2. Copy media:
   ```bash
   cp -r backup/media/* media/
   ```
3. Sesuaikan file `.env` mengikuti `backup/configs/jelajah.env.example`.
