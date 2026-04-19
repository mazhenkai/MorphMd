#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
convert.py - 单文件或批量转换
用法:
  python Bin/convert.py <path> -f [html|pdf|docx]
  path 为 Input/ 目录下的文件或子目录
"""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from core.utils import setup_logger, ensure_dir
from core.config import Config


def convert_file(input_file, output_dir, format_type, logger):
    input_path = Path(input_file)
    if not input_path.exists():
        logger.error(f"文件不存在: {input_file}")
        return False
    if input_path.suffix.lower() != '.md':
        logger.error(f"不是 Markdown 文件: {input_file}")
        return False
    try:
        if format_type == 'html':
            from core.converter_html import MarkdownToHtmlConverter
            converter = MarkdownToHtmlConverter(input_path.parent, output_dir)
        elif format_type == 'pdf':
            from core.converter_pdf_chromium import MarkdownToPdfConverter
            converter = MarkdownToPdfConverter(input_path.parent, output_dir)
        elif format_type == 'docx':
            from core.converter_docx import MarkdownToDocxConverter
            converter = MarkdownToDocxConverter(input_path.parent, output_dir)
        else:
            logger.error(f"不支持的格式: {format_type}")
            return False
        success = converter.convert_file(input_path)
        if success:
            logger.info(f"转换成功: {Path(output_dir) / f'{input_path.stem}.{format_type}'}")
        return success
    except Exception as e:
        logger.error(f"转换失败: {e}")
        return False


def batch_convert(input_dir, output_dir, format_type, logger):
    md_files = list(Path(input_dir).glob("*.md"))
    if not md_files:
        logger.warning(f"在 {input_dir} 中没有找到 Markdown 文件")
        return
    logger.info(f"找到 {len(md_files)} 个文件")
    success_count = sum(
        convert_file(f, output_dir, format_type, logger)
        for f in md_files
    )
    logger.info(f"完成! 成功: {success_count}/{len(md_files)}")


def main():
    parser = argparse.ArgumentParser(description='MorphMd - 单文件/批量转换')
    parser.add_argument('path', help='Input 目录下的文件或子目录')
    parser.add_argument('--format', '-f', choices=['html', 'pdf', 'docx'], default='pdf')
    args = parser.parse_args()

    logger = setup_logger()
    Config()

    input_path = ROOT / "Input" / args.path
    if not input_path.exists():
        logger.error(f"路径不存在: {input_path}")
        sys.exit(1)

    relative_path = Path(args.path)
    if input_path.is_file():
        output_dir = ROOT / "Output" / args.format / relative_path.parent
    else:
        output_dir = ROOT / "Output" / args.format / relative_path
    ensure_dir(output_dir)

    if input_path.is_file():
        convert_file(input_path, output_dir, args.format, logger)
    else:
        batch_convert(input_path, output_dir, args.format, logger)


if __name__ == '__main__':
    main()
