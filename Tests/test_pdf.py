#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).parent / "fixtures"
TMP = ROOT / "Tmp"


def test_pdf_conversion():
    from core.converter_pdf_chromium import MarkdownToPdfConverter
    converter = MarkdownToPdfConverter(FIXTURES, TMP)
    assert converter.convert_file(FIXTURES / "sample.md"), "PDF 转换失败"
    assert (TMP / "sample.pdf").exists(), "PDF 文件未生成"
    print("[OK] PDF 转换")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    test_pdf_conversion()
