import os
from flask import Flask, render_template    

app = Flask(__name__)
app = Flask(__name__, template_folder="static/templates")

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

if __name__ == "__main__":
    app.run(debug=True)
