import os
import urllib.parse
import pkgutil
import importlib.util

# Compatibility shim: restore `pkgutil.get_loader` if removed (Python 3.14+)
if not hasattr(pkgutil, 'get_loader'):
    def _compat_get_loader(name):
        if not name:
            return None
        if name == '__main__':
            return None
        try:
            spec = importlib.util.find_spec(name)
        except Exception:
            return None
        if spec is None:
            return None
        return getattr(spec, 'loader', None)
    pkgutil.get_loader = _compat_get_loader

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_mail import Mail, Message

app = Flask(__name__)
app = Flask(__name__, template_folder="static/templates")

# Jinja filter to URL-encode filenames (handles spaces/special chars in image names)
def _urlencode(s):
    if s is None:
        return ''
    return urllib.parse.quote(s)

app.jinja_env.filters['urlencode'] = _urlencode

# Configuration for Flask-Mail
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  # Your email
# PENTING: Ganti dengan App Password Gmail Anda (16 karakter)
# Cara mendapatkan App Password:
# 1. Buka https://myaccount.google.com/security
# 2. Aktifkan "2-Step Verification" dulu
# 3. Cari "App passwords" dan buat password baru untuk "Mail"
# 4. Copy 16 karakter password dan paste di bawah ini
app.config['MAIL_PASSWORD'] = ''  # Contoh: 'abcd efgh ijkl mnop'
app.config['MAIL_DEFAULT_SENDER'] = ''

mail = Mail(app)

@app.route("/")
def home():
    projects = [
        {"title": "Website Cek Plagiarisme", "image": "project3 (2).png", "desc": " Web untuk mendeteksi plagiarisme dengan algoritma liguistic dan "
        "di dalam web yang saya buat saya menggunakan framwork flask untuk bahasa pemrograman berisikan python, html, dan juga CSS ."},
        {"title": "Absensi RFID berbasi ESP8266", "image": "project2.jpg", "desc": "Alat untuk absensi menggunakan teknologi RFID yang dapat di gunakan di dalam instansi pekerjaan baik itu pun instansi sekolah"}
    ]

    certifications = [
        {"title": "IoT Engineer", "issuer": "Median Talenta Raya", "year": 2022, "image": "Sertifikat PKL SMK Maarif Grt-Agus Ikhsan-1.png"},
        {"title": "Kerlink Sertification", "issuer": "Kerlink", "year": 2023, "image": "IKHSAN - CERTIFACTE KERLINK-1.png"},
        {"title": "sertifikasi IoT PPTIK ITB", "issuer": "PPTIK ITB", "year": 2021, "image": "44d50f5a-df37-44ee-af10-0a6a6095a501-1.png"}
    ]
    print("Files in templates folder:", os.listdir("static/templates"))
    return render_template("index.html", projects=projects, certifications=certifications)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_content = request.form.get('message')
        
        # Create email message
        msg = Message(
            subject=f"Pesan dari Portfolio: {subject}",
            recipients=['gus.ikhsann12@gmail.com'],
            body=f"""
            Pesan baru dari portfolio website:
            
            Nama: {name}
            Email: {email}
            Subjek: {subject}
            
            Pesan:
            {message_content}
            """
        )
        
        # Send email
        mail.send(msg)
        
        return jsonify({'success': True, 'message': 'Pesan berhasil dikirim!'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Gagal mengirim pesan: {str(e)}'})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
