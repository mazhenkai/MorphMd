#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
add_cover.py - 为已有 PDF 添加封面，可选加页码
用法: python Bin/add_cover.py <cover_md> <content_pdf> [output_pdf] [-p]
"""

import argparse
import sys
import io
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import markdown2
from playwright.sync_api import sync_playwright


CSS = """
<style>
    @charset "UTF-8";
    body {
        font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Microsoft YaHei", Arial, sans-serif;
        font-size: 12pt; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px;
    }
    h1 { font-size: 24pt; color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 30px; }
    h2 { font-size: 20pt; color: #34495e; border-bottom: 2px solid #95a5a6; padding-bottom: 8px; margin-top: 25px; }
    table { border-collapse: collapse; width: 100%; margin: 15px 0; font-size: 10pt; }
    table th { background-color: #3498db; color: white; padding: 10px; border: 1px solid #2980b9; }
    table td { padding: 8px; border: 1px solid #ddd; }
</style>
"""


def md_to_pdf_bytes(md_path: Path) -> bytes:
    import json
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    json_path = md_path.with_suffix('.json')
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key, value in data.items():
            content = content.replace(f'{{{{{key}}}}}', str(value))
    html_body = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks', 'header-ids'])
    full_html = f"<!DOCTYPE html><html lang='zh-CN'><head><meta charset='UTF-8'>{CSS}</head><body>{html_body}</body></html>"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(full_html, wait_until='networkidle')
        pdf_bytes = page.pdf(format='A4', margin={'top':'15mm','right':'15mm','bottom':'15mm','left':'15mm'}, print_background=True)
        browser.close()
    return pdf_bytes


def merge_pdfs(cover_bytes: bytes, content_pdf: Path, output_pdf: Path):
    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    for page in PdfReader(io.BytesIO(cover_bytes)).pages:
        writer.add_page(page)
    for page in PdfReader(str(content_pdf)).pages:
        writer.add_page(page)
    with open(output_pdf, 'wb') as f:
        writer.write(f)


def add_page_numbers(pdf_path: Path, skip_first: int = 1):
    """给 PDF 每页加页码，跳过前 skip_first 页（封面）"""
    from pypdf import PdfWriter, PdfReader
    from reportlab.pdfgen import canvas

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i < skip_first:
            writer.add_page(page)
            continue
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, h))
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawCentredString(w / 2, 20, str(i - skip_first + 1))
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
        writer.add_page(page)

    with open(pdf_path, 'wb') as f:
        writer.write(f)


def main():
    parser = argparse.ArgumentParser(description='为 PDF 添加封面')
    parser.add_argument('cover_md', help='封面 md 文件路径（相对于项目根目录）')
    parser.add_argument('content_pdf', help='内容 PDF 文件路径（相对于项目根目录）')
    parser.add_argument('output_pdf', nargs='?', help='输出 PDF 路径')
    parser.add_argument('--page-number', '-p', action='store_true', help='添加页码（跳过封面页）')
    args = parser.parse_args()

    cover_md = ROOT / args.cover_md
    content_pdf = ROOT / args.content_pdf
    output_pdf = ROOT / args.output_pdf if args.output_pdf else content_pdf.parent / f"{content_pdf.stem}_covered.pdf"

    if not cover_md.exists():
        print(f"[ERROR] 封面文件不存在: {cover_md}")
        sys.exit(1)
    if not content_pdf.exists():
        print(f"[ERROR] 内容 PDF 不存在: {content_pdf}")
        sys.exit(1)

    print(f"封面: {cover_md}")
    print(f"内容: {content_pdf}")
    print("生成封面 PDF...")
    cover_bytes = md_to_pdf_bytes(cover_md)

    print("合并 PDF...")
    merge_pdfs(cover_bytes, content_pdf, output_pdf)

    if args.page_number:
        print("添加页码...")
        add_page_numbers(output_pdf, skip_first=1)

    print(f"[OK] 输出: {output_pdf}")


if __name__ == '__main__':
    main()
