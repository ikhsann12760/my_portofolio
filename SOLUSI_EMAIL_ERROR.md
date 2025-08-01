# 🚨 SOLUSI ERROR: Authentication Required

**ERROR YANG ANDA ALAMI:**
```
530, b'5.7.0 Authentication Required
```

## ✅ SOLUSI LANGSUNG (Ikuti step by step):

### STEP 1: Buka Gmail Security Settings
1. Buka browser dan pergi ke: https://myaccount.google.com/security
2. Login dengan akun gus.ikhsann12@gmail.com

### STEP 2: Aktifkan 2-Factor Authentication
1. Scroll ke bagian "Signing in to Google"
2. Klik "2-Step Verification"
3. Ikuti semua langkah untuk mengaktifkan 2FA
4. **PENTING:** 2FA harus aktif dulu sebelum bisa membuat App Password

### STEP 3: Buat App Password
1. Setelah 2FA aktif, kembali ke https://myaccount.google.com/security
2. Cari "App passwords" (akan muncul setelah 2FA aktif)
3. Klik "App passwords"
4. Pilih "Mail" sebagai aplikasi
5. Pilih "Other (Custom name)" dan ketik "Portfolio Website"
6. Klik "Generate"
7. **COPY password 16 karakter yang muncul** (contoh: abcd efgh ijkl mnop)

### STEP 4: Update app.py
1. Buka file `app.py`
2. Cari baris 20: `app.config['MAIL_PASSWORD'] = ''`
3. Ganti menjadi: `app.config['MAIL_PASSWORD'] = 'PASTE_APP_PASSWORD_DI_SINI'`

**Contoh:**
```python
# Sebelum:
app.config['MAIL_PASSWORD'] = ''

# Sesudah (contoh):
app.config['MAIL_PASSWORD'] = 'abcd efgh ijkl mnop'
```

### STEP 5: Restart Aplikasi
1. Tekan `Ctrl+C` di terminal untuk stop aplikasi
2. Jalankan lagi: `python app.py`
3. Test contact form di website

## ⚠️ CATATAN PENTING:
- App Password BERBEDA dengan password Gmail biasa
- App Password berformat 16 karakter dengan spasi
- Jangan share App Password ke siapapun
- Simpan App Password di tempat aman

## 🧪 CARA TEST:
1. Buka http://127.0.0.1:5000
2. Scroll ke bagian "Hubungi Saya"
3. Isi form dan klik "Kirim Pesan"
4. Jika berhasil, akan muncul pesan "Pesan berhasil dikirim!"
5. Cek email gus.ikhsann12@gmail.com untuk melihat pesan yang masuk

---
**Jika masih error, pastikan:**
- 2FA sudah aktif
- App Password sudah di-copy dengan benar (16 karakter)
- Tidak ada typo saat paste password
- Aplikasi sudah di-restart setelah update password