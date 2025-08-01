# Setup Email untuk Contact Form

**ERROR YANG MUNCUL:** `530, b'5.7.0 Authentication Required`

Error ini terjadi karena Gmail memerlukan App Password untuk aplikasi pihak ketiga. Ikuti langkah berikut:

## Langkah-langkah WAJIB:

### 1. **Aktifkan 2-Factor Authentication di Gmail:**
   - Buka https://myaccount.google.com/security
   - Scroll ke "Signing in to Google"
   - Klik "2-Step Verification" dan aktifkan
   - Ikuti semua langkah verifikasi

### 2. **Buat App Password (PENTING!):**
   - Setelah 2FA aktif, kembali ke https://myaccount.google.com/security
   - Cari "App passwords" (muncul setelah 2FA aktif)
   - Klik "App passwords"
   - Pilih "Mail" sebagai app
   - Pilih "Other (Custom name)" dan ketik "Portfolio Website"
   - **COPY password 16 karakter yang muncul** (contoh: abcd efgh ijkl mnop)

### 3. **Update app.py (Pilih salah satu metode):**

**Metode A - Langsung di kode (untuk testing):**
```python
# Ganti baris ini:
app.config['MAIL_PASSWORD'] = ''

# Menjadi:
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'  # Paste app password di sini
```

**Metode B - Menggunakan Environment Variable (RECOMMENDED):**
```python
# Ganti baris ini:
app.config['MAIL_PASSWORD'] = ''

# Menjadi:
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_APP_PASSWORD', '')
```

Jika pilih Metode B, set environment variable:
```bash
# Windows (PowerShell)
$env:GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"

# Windows (Command Prompt)
set GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

### 4. **Restart aplikasi:**
   - Tekan Ctrl+C di terminal untuk stop
   - Jalankan lagi: `python app.py`

## Fitur yang sudah ditambahkan:

- ✅ Contact form dengan validasi
- ✅ Pengiriman email ke gus.ikhsann12@gmail.com
- ✅ Loading state saat mengirim
- ✅ Notifikasi sukses/error
- ✅ Form reset otomatis setelah berhasil

## Catatan Keamanan:

- Jangan commit app password ke repository
- Gunakan environment variables untuk production
- App password hanya untuk aplikasi, bukan untuk login manual

## Testing:

Setelah setup selesai, coba isi form contact di website dan periksa email Anda!