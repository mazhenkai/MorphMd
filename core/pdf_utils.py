#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
from pathlib import Path


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
    """给 PDF 每页加页码，跳过前 skip_first 页"""
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


def find_section_pages(pdf_bytes: bytes, count: int, page_offset: int = 0) -> dict:
    """
    从 PDF bytes 中定位每个 section 的起始页（1-based）。
    标记格式：§§SECTION-i§§，需在 HTML 中以白色小字嵌入。
    page_offset: 目录页等前置页数，加到页码上。
    """
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(pdf_bytes))
    section_pages = {}
    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        for i in range(count):
            if f'§§SECTION-{i}§§' in text and i not in section_pages:
                section_pages[i] = page_idx + 1 + page_offset
    return section_pages


def build_toc_pdf_bytes(toc_items: list, title: str, css_style: str, toc_css: str) -> bytes:
    """
    生成目录页 PDF bytes。
    toc_items: list of (label, page_number_str)
    """
    from playwright.sync_api import sync_playwright

    items_html = "".join(
        f'<li><span>{label}</span><span class="pg">{pg}</span></li>'
        for label, pg in toc_items
    )
    toc_html = f'<div class="toc"><h1>{title}</h1><ol>{items_html}</ol></div>'
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">{css_style}{toc_css}</head>
<body>{toc_html}</body></html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.set_content(full_html, wait_until='networkidle')
        pdf_bytes = pg.pdf(format='A4',
            margin={'top':'15mm','right':'15mm','bottom':'15mm','left':'15mm'},
            print_background=True)
        browser.close()
    return pdf_bytes
