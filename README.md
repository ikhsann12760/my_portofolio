# Web Portofolio Agus Ikhsan N

Portofolio berbasis Flask dengan UI modern menggunakan Bootstrap dan Swiper untuk carousel. Berisi profil, proyek, sertifikasi, serta form kontak yang terhubung ke email.

## Fitur
- Hero dengan animasi mengetik pada subtitle
- Sertifikasi dalam carousel (Swiper)
- Proyek dengan deskripsi toggle per kartu
- Pengalaman kerja dengan toggle per item dan dukungan slide
- Form kontak (SMTP Gmail, App Password)
- Halaman CV (`/cv`) dan unduh PDF langsung (`/cv/download`)
- Penyajian gambar via route khusus: `GET /images/<filename>` (stabil untuk nama file dengan spasi)
- Meta SEO (description, og tags, twitter card)

## Prasyarat
- Python 3.10+
- Pip

## Instalasi
1. Clone repository ini
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Atur variabel lingkungan (lihat bagian Environment Variables)

## Menjalankan Secara Lokal
```bash
python app.py
```
Lalu akses `http://localhost:5000`.

## Environment Variables
Konfigurasi email dan keamanan diatur melalui environment variables:
- `SECRET_KEY`
- `MAIL_SERVER` (contoh: `smtp.gmail.com`)
- `MAIL_PORT` (contoh: `587`)
- `MAIL_USE_TLS` (`True`/`False`)
- `MAIL_USERNAME` (email pembuat App Password)
- `MAIL_PASSWORD` (Gmail App Password 16 karakter, tanpa spasi)
- `MAIL_DEFAULT_SENDER` (alamat pengirim default)

Catatan:
- Gunakan Gmail App Password (bukan password akun). Pastikan `MAIL_USERNAME` sesuai akun yang membuat App Password.
- Jangan commit file `.env` ke repository publik.

## Rute Penting
- `/` halaman utama
- `/send_message` menerima POST form kontak
- `/images/<filename>` menyajikan gambar dari `static/images`
- `/cv` menampilkan CV, `/cv/download` mengunduh PDF

## Deployment (Vercel)
- File `vercel.json` mengatur deployment Flask di Vercel
- Set environment variables di dashboard Vercel (Project Settings → Environment Variables)
- Hindari dependensi yang sulit build di Vercel; PDF menggunakan `reportlab`

## Gambar & Sertifikasi
- Simpan gambar di `static/images`
- Nama file disarankan huruf kecil dan tanpa spasi untuk konsistensi lintas OS
- Untuk file PDF sertifikasi, link unduh disediakan langsung

## Keamanan & Privasi
- Jangan unggah sertifikat/ foto beresolusi penuh jika tidak diperlukan
- Hapus metadata EXIF sebelum upload jika diperlukan
- Pertimbangkan menambahkan header untuk membatasi indeks gambar dan embedding lintas origin pada route `/images/<filename>`

## Troubleshooting
- Error 500 saat kirim email: cek App Password dan environment variables
- Gambar tidak tampil di Vercel: cek penamaan file (case‑sensitive) dan gunakan route `/images/<filename>`

## Struktur Kode
- `app.py` rute utama dan konfigurasi
- `static/templates/index.html` template halaman utama
- `static/images/` aset gambar dan sertifikasi

---

Untuk pengembangan lebih lanjut, lihat `app.py` dan folder `static/`. 
