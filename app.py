import os
import urllib.parse
import pkgutil
import importlib.util
import traceback
from dotenv import load_dotenv

# Compatibility shim: restore `pkgutil.get_loader` if removed (Python 3.14+)
load_dotenv()

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

# Configuration for Flask-Mail (read from environment or .env)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-for-prod')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')

_raw_username = os.environ.get('MAIL_USERNAME', '') or ''
_raw_password = os.environ.get('MAIL_PASSWORD', '') or ''
_raw_sender = os.environ.get('MAIL_DEFAULT_SENDER', '') or ''

_username = _raw_username.strip()
_password = _raw_password.strip().replace(' ', '')
_sender = (_raw_sender.strip() or _username)

app.config['MAIL_USERNAME'] = _username
app.config['MAIL_PASSWORD'] = _password
app.config['MAIL_DEFAULT_SENDER'] = _sender

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    app.logger.warning('MAIL_USERNAME or MAIL_PASSWORD not set. Sending email will fail until configured.')
if len(app.config['MAIL_PASSWORD']) != 16:
    app.logger.warning('MAIL_PASSWORD length is not 16. Gmail App Password should be 16 characters.')
if app.config['MAIL_DEFAULT_SENDER'] != app.config['MAIL_USERNAME']:
    app.logger.warning('MAIL_DEFAULT_SENDER differs from MAIL_USERNAME. Using a different From may be rejected by Gmail.')

mail = Mail(app)

@app.route("/")
def home():
    projects = [
        {"title": "Website Cek Plagiarisme", "image": "project3-2.png", "desc": " Web untuk mendeteksi plagiarisme dengan algoritma liguistic dan "
        "di dalam web yang saya buat saya menggunakan framwork flask untuk bahasa pemrograman berisikan python, html, dan juga CSS ."},
        {"title": "Absensi RFID berbasi ESP8266", "image": "project2.jpg", "desc": "Alat untuk absensi menggunakan teknologi RFID yang dapat di gunakan di dalam instansi pekerjaan baik itu pun instansi sekolah"}
    ]

    certifications = [
        {"title": "IoT Engineer", "issuer": "Median Talenta Raya", "year": 2022, "image": "sertifikat-pkl-smk-maarif-grt-agus-ikhsan-1.png"},
        {"title": "Kerlink Sertification", "issuer": "Kerlink", "year": 2023, "image": "ikhsan-certifakte-kerlink-1.png"},
        {"title": "sertifikasi IoT PPTIK ITB", "issuer": "PPTIK ITB", "year": 2021, "image": "44d50f5a-df37-44ee-af10-0a6a6095a501-1.png"}
    ]
    print("Files in templates folder:", os.listdir("static/templates"))
    return render_template("index.html", projects=projects, certifications=certifications)


@app.route('/_debug_env')
def _debug_env():
    # Debug helper: returns whether mail env vars are present (masked). Local-only.
    host = request.remote_addr
    if host not in ('127.0.0.1', '::1', 'localhost'):
        return jsonify({'error': 'Forbidden'}), 403
    username = app.config.get('MAIL_USERNAME') or ''
    has_username = bool(username)
    has_password = bool(app.config.get('MAIL_PASSWORD'))
    masked_user = (username[:3] + '...' + username[-3:]) if len(username) > 6 else ('***' if username else '')
    return jsonify({
        'mail_server': app.config.get('MAIL_SERVER'),
        'mail_port': app.config.get('MAIL_PORT'),
        'mail_use_tls': app.config.get('MAIL_USE_TLS'),
        'mail_username_present': has_username,
        'mail_username_masked': masked_user,
        'mail_password_present': has_password,
        'mail_password_length': len(app.config.get('MAIL_PASSWORD') or ''),
        'mail_default_sender': app.config.get('MAIL_DEFAULT_SENDER'),
        'sender_equals_username': app.config.get('MAIL_DEFAULT_SENDER') == app.config.get('MAIL_USERNAME')
    })

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_content = request.form.get('message')
        
        # Create email message (use default sender, set reply-to to pengirim)
        msg = Message(
            subject=f"Pesan dari Portfolio: {subject}",
            recipients=['gus.ikhsann12@gmail.com'],
            sender=app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME'),
            reply_to=email,
            body=f"""
            Pesan baru dari portfolio website:
            
            Nama: {name}
            Email: {email}
            Subjek: {subject}
            
            Pesan:
            {message_content}
            """
        )
        
        # Check mail config before sending
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            msg = 'Mail server not configured (MAIL_USERNAME or MAIL_PASSWORD missing).'
            app.logger.error(msg)
            return jsonify({'success': False, 'message': msg}), 500

        # Send email
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Pesan berhasil dikirim!'})

    except Exception as e:
        # Log full traceback to console/server log to help debugging
        tb = traceback.format_exc()
        app.logger.error('Error sending message: %s', tb)
        print(tb)
        err_str = str(e)
        if ('5.7.8' in err_str) or ('BadCredentials' in err_str) or ('Username and Password not accepted' in err_str) or ('535' in err_str):
            return jsonify({'success': False, 'message': 'Autentikasi Gmail gagal. Pastikan MAIL_USERNAME sesuai akun yang membuat App Password dan MAIL_PASSWORD terdiri dari 16 karakter tanpa spasi.'}), 500
        return jsonify({'success': False, 'message': f'Gagal mengirim pesan: {err_str}'}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
