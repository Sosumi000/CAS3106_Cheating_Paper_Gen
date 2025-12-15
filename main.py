#!/usr/bin/env python3
"""
main.py

Will generate PDF file from set of images with each image 
being vertically ordered and its width being 1/5 of 
the width of A4 paper.
You can edit configurations (what is right under '# Config')

How To Use
python3 main.py
"""

import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Config
COLS = 5 # Number of columns
MARGIN_MM = 0.5 # Margin (in millimeters)
A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297 # Paper size (in millimeters)
folder, output = "images", "output.pdf" # Folder where images are located / output file name


def mm_to_pt(mm):
    return mm * 72.0 / 25.4


def list_images(folder):
    exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    return sorted([os.path.join(folder, f) for f in os.listdir(folder)
                   if f.lower().endswith(exts)])


def create_pdf_fixed_width(image_files, output):
    page_w, page_h = A4
    margin = mm_to_pt(MARGIN_MM)
    usable_w = page_w - 2 * margin

    cell_w = usable_w / COLS  

    c = canvas.Canvas(output, pagesize=A4)

    col = 0
    y_cursor = page_h - margin

    for i, img_path in enumerate(image_files):
        try:
            img = Image.open(img_path)
        except Exception as e:
            print(f"Failed to open image: {img_path} ({e})", file=sys.stderr)
            continue

        iw, ih = img.size
        ir = iw / ih
        cell_h = cell_w / ir  

        # If filled one column then proceed to next column
        if y_cursor - cell_h < margin:
            col += 1
            y_cursor = page_h - margin

        # If filled one page then proceed to next page
        if col >= COLS:
            c.showPage()
            col = 0
            y_cursor = page_h - margin

        x = margin + col * cell_w
        y = y_cursor - cell_h

        c.drawImage(ImageReader(img), x, y, cell_w, cell_h, preserveAspectRatio=True)

        y_cursor -= cell_h  # set cursor under the image

    c.save()
    print(f"Saved PDF: {output}")


def main():
    global folder, output
    if not os.path.isdir(folder):
        print(f"Folder doesn't exist: {folder}")
        sys.exit(1)

    imgs = list_images(folder)
    if not imgs:
        print("No image found")
        sys.exit(1)

    create_pdf_fixed_width(imgs, output)


if __name__ == "__main__":
    main()
