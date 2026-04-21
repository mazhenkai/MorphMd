#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
clean_metadata.py - 清除 MorphMd 生成的内部元数据
用法: python Bin/clean_metadata.py <pdf_path>
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from pypdf import PdfWriter, PdfReader


def main():
    import argparse
    parser = argparse.ArgumentParser(description='清除 PDF 中的 MorphMd 内部元数据')
    parser.add_argument('pdf_path', help='PDF 文件路径（相对于项目根目录）')
    args = parser.parse_args()

    pdf_path = ROOT / args.pdf_path
    if not pdf_path.exists():
        print(f"[ERROR] 文件不存在: {pdf_path}")
        sys.exit(1)

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    writer.append(reader)

    meta = dict(reader.metadata or {})
    meta.pop('/MorphMdSections', None)
    meta.pop('/MorphMdPages', None)
    if meta:
        writer.add_metadata(meta)

    with open(pdf_path, 'wb') as f:
        writer.write(f)

    print(f"[OK] 元数据已清除: {pdf_path}")


if __name__ == '__main__':
    main()
