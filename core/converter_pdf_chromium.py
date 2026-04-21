#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown转PDF工具（使用Playwright/Chromium，支持彩色Emoji）

功能: 将Markdown文件转换为PDF格式，完美支持彩色emoji
输出: 保存到指定目录

依赖:
    pip install markdown2 playwright
    playwright install chromium

优势:
    - 完美支持彩色 emoji 😊 🎉 🔥
    - 基于现代 Chromium 引擎
    - 更好的网页标准支持

作者: Claude
日期: 2025-12-04
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import markdown2
    from playwright.sync_api import sync_playwright
except ImportError:
    print("=" * 80)
    print("错误: 缺少必要的依赖库")
    print("=" * 80)
    print("\n请安装以下依赖:")
    print("  pip install markdown2 playwright")
    print("  playwright install chromium")
    print("=" * 80)
    sys.exit(1)


class MarkdownToPdfConverter:
    """Markdown转PDF转换器（Chromium版本）"""

    def __init__(self, input_dir, output_dir):
        """
        初始化转换器

        Args:
            input_dir: 输入目录(包含Markdown文件)
            output_dir: 输出目录(保存PDF文件)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # CSS样式
        self.css_style = """
        <style>
            @charset "UTF-8";

            body {
                /* 优先使用支持彩色emoji的系统字体 */
                font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }

            h1 {
                font-size: 24pt;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
                margin-top: 30px;
                margin-bottom: 20px;
                page-break-before: auto;
            }

            h2 {
                font-size: 20pt;
                font-weight: bold;
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 8px;
                margin-top: 25px;
                margin-bottom: 15px;
                page-break-after: avoid;
            }

            h3 {
                font-size: 16pt;
                font-weight: bold;
                color: #555;
                margin-top: 20px;
                margin-bottom: 12px;
                page-break-after: avoid;
            }

            h4, h5, h6 {
                font-size: 14pt;
                font-weight: bold;
                color: #666;
                margin-top: 15px;
                margin-bottom: 10px;
                page-break-after: avoid;
            }

            p {
                margin: 8px 0;
                text-align: justify;
            }

            code {
                font-family: "Consolas", "Courier New", monospace;
                font-size: 10pt;
                background-color: #f4f4f4;
                padding: 2px 5px;
                border-radius: 3px;
                color: #c7254e;
            }

            pre {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 12px;
                white-space: pre-wrap;
                word-break: break-all;
                margin: 15px 0;
                page-break-inside: avoid;
            }

            pre code {
                background-color: transparent;
                padding: 0;
                color: #333;
                font-size: 9pt;
                line-height: 1.4;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
                font-size: 10pt;
                page-break-inside: avoid;
            }

            table th {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: left;
                border: 1px solid #2980b9;
            }

            table td {
                padding: 8px;
                border: 1px solid #ddd;
            }

            table tr:nth-child(even) {
                background-color: #f9f9f9;
            }

            table tr:hover {
                background-color: #f5f5f5;
            }

            ul, ol {
                margin: 10px 0;
                padding-left: 30px;
            }

            li {
                margin: 5px 0;
            }

            blockquote {
                border-left: 4px solid #3498db;
                background-color: #f9f9f9;
                padding: 10px 15px;
                margin: 15px 0;
                color: #555;
                font-style: italic;
            }

            hr {
                border: none;
                border-top: 2px solid #ddd;
                margin: 25px 0;
            }

            a {
                color: #3498db;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }

            img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 15px auto;
            }

            /* 打印优化 */
            @media print {
                body {
                    font-size: 11pt;
                }

                h1 {
                    page-break-before: always;
                }

                h1:first-child {
                    page-break-before: avoid;
                }

                h2, h3, h4, h5, h6 {
                    page-break-after: avoid;
                }

                pre, table, img {
                    page-break-inside: avoid;
                }

                a {
                    color: #3498db;
                }
            }
        </style>
        """

    def convert_file(self, md_file):
        """
        转换单个Markdown文件为PDF

        Args:
            md_file: Markdown文件路径

        Returns:
            bool: 转换是否成功
        """
        try:
            # 读取Markdown文件
            print(f"\n[1/4] 读取文件: {md_file.name}")
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # 转换Markdown为HTML
            print(f"[2/4] 转换为HTML...")
            html_content = markdown2.markdown(
                md_content,
                extras=[
                    'tables',
                    'fenced-code-blocks',
                    'code-friendly',
                    'break-on-newline',
                    'header-ids',
                ]
            )

            # 构建完整的HTML文档
            full_html = f"""
            <!DOCTYPE html>
            <html lang="zh-CN">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{md_file.stem}</title>
                {self.css_style}
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """

            # 输出PDF文件路径
            pdf_file = self.output_dir / f"{md_file.stem}.pdf"

            # 使用Playwright转换为PDF
            print(f"[3/4] 生成PDF（使用Chromium引擎）...")

            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()

                # 加载HTML内容
                page.set_content(full_html, wait_until='networkidle')

                # 生成PDF
                page.pdf(
                    path=str(pdf_file),
                    format='A4',
                    margin={
                        'top': '15mm',
                        'right': '15mm',
                        'bottom': '15mm',
                        'left': '15mm'
                    },
                    print_background=True,
                    prefer_css_page_size=False
                )

                browser.close()

            print(f"[4/4] [OK] 成功: {pdf_file.name}")
            return True

        except Exception as e:
            print(f"[ERROR] [FAIL] 失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def convert_all(self):
        """转换目录下的所有Markdown文件"""
        # 查找所有Markdown文件
        md_files = list(self.input_dir.glob("*.md"))

        if not md_files:
            print(f"[WARNING] 在 {self.input_dir} 中没有找到Markdown文件")
            return

        print("=" * 80)
        print(f"Markdown转PDF工具（Chromium版 - 支持彩色Emoji）")
        print("=" * 80)
        print(f"\n输入目录: {self.input_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"找到文件: {len(md_files)} 个\n")

        # 逐个转换
        success_count = 0
        fail_count = 0

        for idx, md_file in enumerate(md_files, 1):
            print(f"\n{'=' * 80}")
            print(f"[{idx}/{len(md_files)}] 处理: {md_file.name}")
            print('=' * 80)

            if self.convert_file(md_file):
                success_count += 1
            else:
                fail_count += 1

        # 输出统计
        print("\n" + "=" * 80)
        print("转换完成!")
        print("=" * 80)
        print(f"\n[OK] 成功: {success_count} 个")
        print(f"[FAIL] 失败: {fail_count} 个")
        print(f"\nPDF文件保存在: {self.output_dir}")
        print("=" * 80)


    def convert_merged(self, output_filename=None):
        """将目录下所有 Markdown 文件合并为一个 PDF。每个 section 单独渲染以精确记录页码，存入元数据供 add_toc_pages 使用。"""
        import io
        from pypdf import PdfWriter, PdfReader

        md_files = sorted(self.input_dir.glob("*.md"))
        if not md_files:
            print(f"[WARNING] 在 {self.input_dir} 中没有找到Markdown文件")
            return False

        if output_filename is None:
            output_filename = self.input_dir.name

        print(f"找到 {len(md_files)} 个文件，合并为: {output_filename}.pdf")

        margin = {'top':'15mm','right':'15mm','bottom':'15mm','left':'15mm'}

        # 先渲染简单目录页，数出占几页，作为内容页码的 offset
        toc_items = "".join(f'<li>{md_file.stem}</li>' for md_file in md_files)
        toc_css = "<style>.toc{padding:40px 0}.toc h1{font-size:28pt;border-bottom:3px solid #3498db;padding-bottom:10px}.toc ol{font-size:13pt;line-height:2}</style>"
        toc_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">{self.css_style}{toc_css}</head>
<body><div class="toc"><h1>目录</h1><ol>{toc_items}</ol></div></body></html>"""

        with sync_playwright() as p:
            browser = p.chromium.launch()
            pg = browser.new_page()
            pg.set_content(toc_html, wait_until='networkidle')
            toc_bytes = pg.pdf(format='A4', margin=margin, print_background=True)
            browser.close()

        toc_page_count = len(PdfReader(io.BytesIO(toc_bytes)).pages)

        # 每个 section 单独渲染，记录起始页码
        section_pdf_bytes = []
        section_start_pages = {}
        current_page = toc_page_count + 1

        with sync_playwright() as p:
            browser = p.chromium.launch()
            for i, md_file in enumerate(md_files):
                print(f"  [{i+1}/{len(md_files)}] {md_file.name}")
                with open(md_file, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                html_body = markdown2.markdown(
                    md_content,
                    extras=['tables', 'fenced-code-blocks', 'code-friendly', 'break-on-newline', 'header-ids']
                )
                full_html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">{self.css_style}</head>
<body>{html_body}</body></html>"""
                pg = browser.new_page()
                pg.set_content(full_html, wait_until='networkidle')
                pdf_bytes = pg.pdf(format='A4', margin=margin, print_background=True)
                pg.close()
                section_pdf_bytes.append(pdf_bytes)
                section_start_pages[i] = current_page - toc_page_count  # 相对页码，从1开始
                current_page += len(PdfReader(io.BytesIO(pdf_bytes)).pages)
            browser.close()

        # 拼合目录页 + 所有 section
        writer = PdfWriter()
        for page in PdfReader(io.BytesIO(toc_bytes)).pages:
            writer.add_page(page)
        for pdf_bytes in section_pdf_bytes:
            for page in PdfReader(io.BytesIO(pdf_bytes)).pages:
                writer.add_page(page)

        # 写入元数据：文件名列表 + 精确页码
        import json
        writer.add_metadata({
            '/MorphMdSections': '|'.join(f.stem for f in md_files),
            '/MorphMdPages': json.dumps(section_start_pages),
        })

        pdf_file = self.output_dir / f"{output_filename}.pdf"
        with open(pdf_file, 'wb') as f:
            writer.write(f)

        print(f"[OK] 合并完成: {pdf_file}")
        return True

        print(f"[OK] 合并完成: {pdf_file}")
        return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='将Markdown文件转换为PDF（支持彩色Emoji）')
    parser.add_argument('-i', '--input', type=str, help='输入目录路径（包含.md文件）')
    parser.add_argument('-o', '--output', type=str, help='输出目录路径（保存.pdf文件）')
    parser.add_argument('-f', '--file', type=str, help='单个Markdown文件路径（优先级高于-i参数）')

    args = parser.parse_args()

    # 设置路径
    script_dir = Path(__file__).parent

    # 如果指定了单个文件
    if args.file:
        md_file = Path(args.file)

        # 检查文件是否存在
        if not md_file.exists():
            print(f"[ERROR] 文件不存在: {md_file}")
            sys.exit(1)

        # 检查是否为.md文件
        if md_file.suffix.lower() != '.md':
            print(f"[ERROR] 不是Markdown文件: {md_file}")
            sys.exit(1)

        # 确定输出目录
        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = md_file.parent  # 默认输出到文件所在目录

        # 创建转换器
        input_dir = md_file.parent
        converter = MarkdownToPdfConverter(input_dir, output_dir)

        # 转换单个文件
        print("=" * 80)
        print(f"Markdown转PDF工具（Chromium版） - 单文件模式")
        print("=" * 80)
        print(f"\n输入文件: {md_file}")
        print(f"输出目录: {output_dir}\n")

        success = converter.convert_file(md_file)

        if success:
            print("\n" + "=" * 80)
            print("[OK] 转换成功! 彩色emoji已完美支持!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("[FAIL] 转换失败")
            print("=" * 80)
            sys.exit(1)

    # 否则处理整个目录
    else:
        if args.input:
            input_dir = Path(args.input)
        else:
            input_dir = script_dir / "process"

        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = input_dir  # 默认输出到输入目录

        # 检查输入目录是否存在
        if not input_dir.exists():
            print(f"[ERROR] 输入目录不存在: {input_dir}")
            sys.exit(1)

        # 创建转换器
        converter = MarkdownToPdfConverter(input_dir, output_dir)

        # 执行转换
        converter.convert_all()


if __name__ == "__main__":
    main()
