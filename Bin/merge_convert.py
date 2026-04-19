#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
merge_convert.py - 将目录下所有 md 合并为一个 PDF
用法: python Bin/merge_convert.py <dir>
  dir 为 Input/ 目录下的子目录
"""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from core.utils import setup_logger, ensure_dir
from core.config import Config


def main():
    parser = argparse.ArgumentParser(description='MorphMd - 合并多个 md 为一个 PDF')
    parser.add_argument('path', help='Input 目录下的子目录')
    parser.add_argument('--name', '-n', help='输出文件名（默认使用目录名）')
    args = parser.parse_args()

    logger = setup_logger()
    Config()

    input_path = ROOT / "Input" / args.path
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"目录不存在: {input_path}")
        sys.exit(1)

    output_dir = ROOT / "Output" / "pdf" / args.path
    ensure_dir(output_dir)

    from core.converter_pdf_chromium import MarkdownToPdfConverter
    converter = MarkdownToPdfConverter(input_path, output_dir)
    converter.convert_merged(output_filename=args.name or input_path.name)


if __name__ == '__main__':
    main()
