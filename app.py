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
from flask import send_from_directory
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

_raw_username = os.environ.get('MAIL_USERNAME') or os.environ.get('GMAIL_USERNAME') or ''
_raw_password = os.environ.get('MAIL_PASSWORD') or os.environ.get('GMAIL_APP_PASSWORD') or ''
_raw_sender = os.environ.get('MAIL_DEFAULT_SENDER', '') or ''

def _sanitize_env(s, remove_spaces=False):
    s = (s or '').strip()
    s = s.strip('"').strip("'")
    if remove_spaces:
        s = s.replace(' ', '')
    return s

_username = _sanitize_env(_raw_username)
_password = _sanitize_env(_raw_password, remove_spaces=True)
_sender = _sanitize_env(_raw_sender) or _username

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

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join('static', 'images'), filename)

def get_certifications():
    items = []
    files = []
    try:
        files = os.listdir(os.path.join('static', 'images'))
    except Exception:
        files = []
    for f in files:
        if not f.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        if f.startswith('sertifikat-pkl-smk-maarif'):
            items.append({"title": "IoT Engineer", "issuer": "Median Talenta Raya", "year": 2022, "image": f})
        elif f.startswith('ikhsan-certifakte-kerlink'):
            items.append({"title": "Kerlink Sertification", "issuer": "Kerlink", "year": 2023, "image": f})
        elif f.startswith('44d50f5a'):
            items.append({"title": "Sertifikasi IoT PPTIK ITB", "issuer": "PPTIK ITB", "year": 2021, "image": f})
        elif f.startswith('8934557'):
            items.append({"title": "Sertifikat Pelatihan IoT", "issuer": "SkillUP", "year": 2025, "image": f})
        elif f.startswith('8955497'):
            items.append({"title": "Sertifikat IoT AWS", "issuer": "AWS", "year": 2025, "image": f})
    return items

@app.route("/")
def home():
    projects = [
        {"title": "Website Cek Plagiarisme", "image": "Pengertian-Phyton.jpg", "desc": " Web untuk mendeteksi plagiarisme dengan algoritma liguistic dan "
        "di dalam web yang saya buat saya menggunakan framwork flask untuk bahasa pemrograman berisikan python, html, dan juga CSS ."},
        {"title": "Absensi RFID berbasi ESP8266", "image": "project2.jpg", "desc": "Alat untuk absensi menggunakan teknologi RFID yang dapat di gunakan di dalam instansi pekerjaan baik itu pun instansi sekolah"},
        {"title" : "MODERENISASI SPAN2024, SPAN 2025", "image" : "Project_Postman.png", "desc": "Project ini bertujuan untuk menguji layanan berbasis Oracle Java menggunakan Postman sebagai tools utama. Pengujian dilakukan untuk memastikan setiap endpoint berjalan sesuai fungsi, format data valid, serta sistem autentikasi dan respons layanan sesuai standar"}
    ]

    certifications = get_certifications()

    # Auto-detect certificate image files in static/images
    try:
        imgs = os.listdir(os.path.join('static', 'images'))
    except Exception:
        imgs = []

    # heuristics: include files that look like certificates (contain 'sert' or 'cert') and are images
    lower_existing = {c['image'].lower() for c in certifications if c.get('image')}
    for f in imgs:
        fl = f.lower()
        if fl in lower_existing:
            continue
        if any(fl.endswith(ext) for ext in ('.png', '.jpg', '.jpeg')) and ('sert' in fl or 'cert' in fl):
            # create a friendly title from filename
            name = os.path.splitext(f)[0]
            title = name.replace('-', ' ').replace('_', ' ').title()
            certifications.append({"title": title, "issuer": "", "year": "", "image": f})
    # Also include specific uploaded certificate images provided by user
    manual_add = [
        "8934557_91720741757314421586_page-0001.jpg",
        "8955497_91720741757649379217_page-0001.jpg"
    ]
    for f in manual_add:
        if f.lower() not in lower_existing and os.path.exists(os.path.join('static', 'images', f)):
            title = f.split('_')[0]
            certifications.append({"title": f"Sertifikat {title}", "issuer": "", "year": "", "image": f})
    print("Files in templates folder:", os.listdir("static/templates"))
    return render_template("index.html", projects=projects, certifications=certifications)

@app.route('/cv')
def cv():
    projects = [
        {"title": "Website Cek Plagiarisme", "image": "project3-2.png", "desc": " Web untuk mendeteksi plagiarisme dengan algoritma liguistic dan di dalam web yang saya buat saya menggunakan framwork flask untuk bahasa pemrograman berisikan python, html, dan juga CSS ."},
        {"title": "Absensi RFID berbasi ESP8266", "image": "project2.jpg", "desc": "Alat untuk absensi menggunakan teknologi RFID yang dapat di gunakan di dalam instansi pekerjaan baik itu pun instansi sekolah"}
    ]
    certifications = get_certifications()
    return render_template('cv.html', projects=projects, certifications=certifications)

@app.route('/cv/download')
def cv_download():
    projects = [
        {"title": "Website Cek Plagiarisme", "image": "project3-2.png", "desc": " Web untuk mendeteksi plagiarisme dengan algoritma liguistic dan di dalam web yang saya buat saya menggunakan framwork flask untuk bahasa pemrograman berisikan python, html, dan juga CSS ."},
        {"title": "Absensi RFID berbasi ESP8266", "image": "project2.jpg", "desc": "Alat untuk absensi menggunakan teknologi RFID yang dapat di gunakan di dalam instansi pekerjaan baik itu pun instansi sekolah"}
    ]
    certifications = [{"title": c.get("title"), "issuer": c.get("issuer"), "year": c.get("year")} for c in get_certifications()]
    from io import BytesIO
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Agus Ikhsan Nurrohman", styles['Title']))
    content.append(Paragraph("IoT Engineer | Quality Assurance | AI Enthusiast", styles['Heading3']))
    content.append(Paragraph("Email: gus.ikhsann12@gmail.com | Telp: +62 838-1611-2959 | Indonesia, Jawa Barat", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Ringkasan", styles['Heading2']))
    content.append(Paragraph("Saya adalah seorang IoT Engineer yang passionate dalam mengembangkan solusi teknologi yang inovatif. Dengan pengalaman di bidang Quality Assurance dan antusiasme terhadap AI, saya berkomitmen untuk menciptakan produk yang berkualitas tinggi.", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Skills", styles['Heading2']))
    skills = [["IoT & Hardware", "ESP8266, RFID, Arduino, Sensor Networks, Raspberry Pi, ESP32"],
              ["Programming", "Python, Flask, HTML/CSS, JavaScript, C++, MQTT"],
              ["Tools & Platforms", "GitHub, Postman, K6, Katalon, JMeter, Arduino IDE, VS Code, MQTT Explorer"]]
    t = Table(skills, colWidths=[140, 380])
    t.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.whitesmoke)
    ]))
    content.append(t)
    content.append(Spacer(1, 12))
    content.append(Paragraph("Pengalaman Kerja", styles['Heading2']))
    content.append(Paragraph("IoT Engineer — PT. Median Talenta Raya (2022 - Sekarang)", styles['Heading4']))
    content.append(Paragraph("Mengembangkan sistem monitoring sensor real-time; Implementasi protokol komunikasi IoT (MQTT, HTTP); Optimasi performa dan keamanan sistem.", styles['Normal']))
    content.append(Spacer(1, 6))
    content.append(Paragraph("Quality Assurance Engineer — Kementrian Keuangan Negara Republik Indonesia (2021 - 2022)", styles['Heading4']))
    content.append(Paragraph("Manual testing menggunakan Postman; Performance testing menggunakan K6 dan JMeter; Bug reporting dan tracking Dengan Postman.", styles['Normal']))
    content.append(Spacer(1, 6))
    content.append(Paragraph("IoT Intern — PPTIK ITB (2020 - 2021)", styles['Heading4']))
    content.append(Paragraph("Pengembangan sensor RFID dan alat Absensi RFID; Implementasi MQTT untuk pengiriman data dengan RabbitMQ; Dokumentasi proyek IoT.", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Proyek Pilihan", styles['Heading2']))
    for p in projects:
        content.append(Paragraph(f"{p['title']} — {p['desc']}", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Sertifikasi", styles['Heading2']))
    for c in certifications:
        content.append(Paragraph(f"{c['title']} — {c['issuer']} ({c['year']})", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Ringkasan Pencapaian", styles['Heading2']))
    content.append(Paragraph("3+ Tahun Pengalaman; 10+ Project Selesai; 5+ Sertifikasi.", styles['Normal']))
    doc.build(content)
    pdf = buf.getvalue()
    from flask import Response
    return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename="Agus_Ikhsan_Nurrohman_CV.pdf"'})


@app.route('/_debug_env')
def _debug_env():
    # Debug helper: returns whether mail env vars are present (masked). Local-only.
    host = request.remote_addr
    allow_remote = os.environ.get('DEBUG_ENV_ENABLE', 'False').lower() in ('1', 'true', 'yes')
    if not allow_remote and host not in ('127.0.0.1', '::1', 'localhost'):
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
