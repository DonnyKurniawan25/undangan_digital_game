@echo off
setlocal enabledelayedexpansion

title Undangan Digital Game - Django Server

:: Pindah ke direktori file .bat berada
cd /d "%~dp0"

echo ================================================================
echo             UNDANGAN DIGITAL GAME - DJANGO SERVER
echo ================================================================
echo.

:: 1. Cek Virtual Environment atau Python sistem
set "PY_CMD="

if exist "%~dp0venv\Scripts\python.exe" (
    echo [INFO] Mengaktifkan virtual environment: venv
    call "%~dp0venv\Scripts\activate.bat"
    set "PY_CMD=python"
) else if exist "%~dp0.venv\Scripts\python.exe" (
    echo [INFO] Mengaktifkan virtual environment: .venv
    call "%~dp0.venv\Scripts\activate.bat"
    set "PY_CMD=python"
) else if exist "%~dp0env\Scripts\python.exe" (
    echo [INFO] Mengaktifkan virtual environment: env
    call "%~dp0env\Scripts\activate.bat"
    set "PY_CMD=python"
) else (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Menggunakan Python sistem
        set "PY_CMD=python"
    ) else (
        where py >nul 2>&1
        if !errorlevel! equ 0 (
            echo [INFO] Menggunakan Python Launcher: py
            set "PY_CMD=py"
        )
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python tidak ditemukan di sistem!
    echo Pastikan Python sudah terinstal dan opsi "Add Python to PATH" dicentang.
    echo Unduh Python di: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Tampilkan versi Python yang digunakan
echo [INFO] Versi Python:
%PY_CMD% --version
echo.

:: 2. Cek database SQLite, buat & isi contoh jika belum ada
if not exist "%~dp0db.sqlite3" (
    echo [INFO] Database belum ditemukan. Menjalankan migrasi awal...
    %PY_CMD% manage.py migrate
    echo [INFO] Mengisi database dengan data contoh...
    %PY_CMD% manage.py isi_contoh
    echo.
)

:: 3. Informasi URL akses
echo ================================================================
echo  Aplikasi siap dijalankan!
echo.
echo  - Beranda / Landing Page : http://127.0.0.1:8000/
echo  - Contoh Undangan Tamu   : http://127.0.0.1:8000/undangan/andi-pratama/
echo  - Panel Admin            : http://127.0.0.1:8000/admin/
echo.

:: 4. Jalankan perintah atau mulai server
if "%~1"=="" (
    echo   Browser akan terbuka secara otomatis.
    echo   Tekan [CTRL + C] di jendela ini untuk menghentikan server.
    echo ================================================================
    echo.
    start "" "http://127.0.0.1:8000/"
    %PY_CMD% manage.py runserver 127.0.0.1:8000
) else (
    echo   Menjalankan perintah: manage.py %*
    echo ================================================================
    echo.
    %PY_CMD% manage.py %*
)

echo.
echo Selesai.
pause
