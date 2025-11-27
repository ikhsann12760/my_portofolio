from PIL import Image, ImageDraw, ImageFont
import os

def gradient_bg(width, height, colors):
    img = Image.new('RGB', (width, height), color=colors[0])
    draw = ImageDraw.Draw(img)
    for i in range(height):
        ratio = i / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    return img

def add_overlay(img):
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    # diagonal accent
    draw.polygon([(0, h*0.7), (w*0.6, 0), (w, 0), (0, h)], fill=(255, 179, 0, 40))
    # vignette bottom
    draw.rectangle([0, h*0.6, w, h], fill=(0, 0, 0, 60))
    return Image.alpha_composite(img.convert('RGBA'), overlay)

def draw_text(img, title, subtitle, icon='📡'):
    draw = ImageDraw.Draw(img)
    w, h = img.size
    try:
        title_font = ImageFont.truetype('arial.ttf', 64)
        subtitle_font = ImageFont.truetype('arial.ttf', 28)
        icon_font = ImageFont.truetype('seguiemj.ttf', 72)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        icon_font = ImageFont.load_default()

    # icon
    draw.text((40, 40), icon, font=icon_font, fill=(255, 255, 255, 255))
    # title
    draw.text((140, 50), title, font=title_font, fill=(255, 255, 255, 255))
    # subtitle
    draw.text((140, 120), subtitle, font=subtitle_font, fill=(230, 230, 230, 255))

def rounded_corners(img, radius=24):
    w, h = img.size
    mask = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0,0,w,h], radius=radius, fill=255)
    out = Image.new('RGBA', (w, h))
    out.paste(img, (0, 0), mask)
    return out

def create_thumbnail(path, title, subtitle, colors, icon):
    base = gradient_bg(1200, 675, colors)
    composed = add_overlay(base)
    draw_text(composed, title, subtitle, icon)
    final = rounded_corners(composed)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    final.save(path, 'PNG')
    print(f'Saved: {path}')

if __name__ == '__main__':
    create_thumbnail(
        'static/images/project-plagiarism.png',
        'Website Cek Plagiarisme',
        'Flask • Python • HTML/CSS • NLP',
        ((30, 60, 120), (72, 129, 255)),
        '🔎'
    )
    create_thumbnail(
        'static/images/project-rfid.png',
        'Absensi RFID Berbasis ESP8266',
        'IoT • ESP8266 • RFID • MQTT',
        ((20, 100, 80), (0, 180, 140)),
        '📶'
    )
