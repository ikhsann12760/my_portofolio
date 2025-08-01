from PIL import Image, ImageDraw
import os

def create_circular_favicon(input_path, output_path, size=32):
    """
    Membuat favicon bulat dari gambar input
    """
    # Buka gambar asli
    img = Image.open(input_path)
    
    # Resize ke ukuran favicon
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    
    # Buat mask lingkaran
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    
    # Terapkan mask
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    
    # Simpan favicon
    output.save(output_path, 'PNG')
    print(f"Favicon bulat berhasil dibuat: {output_path}")

# Buat favicon bulat
if __name__ == "__main__":
    input_file = "static/images/favicon.png"
    output_file = "static/images/favicon_circular.png"
    
    if os.path.exists(input_file):
        create_circular_favicon(input_file, output_file)
    else:
        print(f"File {input_file} tidak ditemukan!") 