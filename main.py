#!/usr/bin/env python3
"""
images_to_pdf_5x13_fixed_width.py

각 이미지의 가로 크기를 A4 가로 길이의 1/5로 고정하고,
세로 크기는 원본 비율에 맞게 자동 조정하여 세로로 나열한 PDF를 만듭니다.

사용법:
    python images_to_pdf_5x13_fixed_width.py
"""

import os
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# 설정
COLS = 5
MARGIN_MM = 0.5
A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297


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

    cell_w = usable_w / COLS  # 고정 가로 폭 (A4의 1/5)

    c = canvas.Canvas(output, pagesize=A4)

    col = 0
    y_cursor = page_h - margin

    for i, img_path in enumerate(image_files):
        try:
            img = Image.open(img_path)
        except Exception as e:
            print(f"⚠️ 이미지 열기 실패: {img_path} ({e})", file=sys.stderr)
            continue

        iw, ih = img.size
        ir = iw / ih
        cell_h = cell_w / ir  # 비율에 따라 세로 결정

        # 다음 이미지가 페이지 아래로 넘어가면 다음 열로
        if y_cursor - cell_h < margin:
            col += 1
            y_cursor = page_h - margin

        # 5열을 모두 채우면 새 페이지
        if col >= COLS:
            c.showPage()
            col = 0
            y_cursor = page_h - margin

        x = margin + col * cell_w
        y = y_cursor - cell_h

        c.drawImage(ImageReader(img), x, y, cell_w, cell_h, preserveAspectRatio=True)

        y_cursor -= cell_h  # 다음 이미지 아래로

    c.save()
    print(f"✅ PDF 저장 완료: {output}")


def main():
    folder, output = "temp", "output_fixed_width.pdf"
    if not os.path.isdir(folder):
        print(f"폴더가 존재하지 않음: {folder}")
        sys.exit(1)

    imgs = list_images(folder)
    if not imgs:
        print("이미지 파일이 없습니다.")
        sys.exit(1)

    create_pdf_fixed_width(imgs, output)


if __name__ == "__main__":
    main()
