#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
add_toc_pages.py - 为合并后的 PDF 重建带页码的目录页，并加底部页码
用法: python Bin/add_toc_pages.py <pdf_path> [--toc-pages N] [--skip-page-number]
"""

import argparse
import sys
import io
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from pypdf import PdfWriter, PdfReader
from playwright.sync_api import sync_playwright
from core.pdf_utils import add_page_numbers, find_section_pages


TOC_CSS = """
<style>
    body { font-family: "Microsoft YaHei", Arial, sans-serif; font-size: 12pt; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }
    .toc { padding: 40px 0; }
    .toc h1 { font-size: 28pt; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
    .toc ol { font-size: 13pt; line-height: 2; padding-left: 20px; }
    .toc li { display: flex; align-items: baseline; }
    .toc .label { white-space: nowrap; }
    .toc .dots { flex: 1; border-bottom: 1px dotted #aaa; margin: 0 6px 4px 6px; }
    .toc .pg { white-space: nowrap; color: #555; padding-right: 30px; }
</style>
"""


def build_toc_pdf_bytes(labels: list, section_pages: dict) -> bytes:
    items_html = "".join(
        f'<li><span class="label">{label}</span><span class="dots"></span><span class="pg">{section_pages.get(i, "")}</span></li>'
        for i, label in enumerate(labels)
    )
    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">{TOC_CSS}</head>
<body><div class="toc"><h1>目录</h1><ol>{items_html}</ol></div></body></html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page()
        pg.set_content(full_html, wait_until='networkidle')
        pdf_bytes = pg.pdf(format='A4',
            margin={'top':'15mm','right':'15mm','bottom':'15mm','left':'15mm'},
            print_background=True)
        browser.close()
    return pdf_bytes


def main():
    parser = argparse.ArgumentParser(description='为合并 PDF 重建带页码目录并加底部页码')
    parser.add_argument('pdf_path', help='PDF 文件路径（相对于项目根目录）')
    parser.add_argument('--toc-pages', type=int, default=1, help='目录页占几页（默认1）')
    parser.add_argument('--skip-page-number', action='store_true', help='不加底部页码')
    args = parser.parse_args()

    pdf_path = ROOT / args.pdf_path
    if not pdf_path.exists():
        print(f"[ERROR] 文件不存在: {pdf_path}")
        sys.exit(1)

    print(f"读取 PDF: {pdf_path}")
    reader = PdfReader(str(pdf_path))
    meta = reader.metadata or {}
    sections_meta = meta.get('/MorphMdSections', '')
    pages_meta = meta.get('/MorphMdPages', '')
    if not sections_meta or not pages_meta:
        print("[ERROR] PDF 元数据中没有章节信息，请用 merge_convert.py 重新生成")
        sys.exit(1)
    labels = sections_meta.split('|')
    import json
    section_pages = {int(k): v for k, v in json.loads(pages_meta).items()}
    print(f"找到 {len(labels)} 个章节")

    print("生成新目录页...")
    toc_bytes = build_toc_pdf_bytes(labels, section_pages)

    # 提取内容页（跳过旧目录页）
    content_buf = io.BytesIO()
    content_writer = PdfWriter()
    for page in reader.pages[args.toc_pages:]:
        content_writer.add_page(page)
    content_writer.write(content_buf)
    content_bytes = content_buf.getvalue()

    print("拼合 PDF...")
    final_writer = PdfWriter()
    for page in PdfReader(io.BytesIO(toc_bytes)).pages:
        final_writer.add_page(page)
    for page in PdfReader(io.BytesIO(content_bytes)).pages:
        final_writer.add_page(page)
    # 保留原始元数据
    if reader.metadata:
        final_writer.add_metadata(dict(reader.metadata))
    with open(pdf_path, 'wb') as f:
        final_writer.write(f)

    if not args.skip_page_number:
        print("添加底部页码...")
        add_page_numbers(pdf_path, skip_first=args.toc_pages)

    print(f"[OK] 完成: {pdf_path}")


if __name__ == '__main__':
    main()
