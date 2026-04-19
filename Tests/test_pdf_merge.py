#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).parent / "fixtures"
TMP = ROOT / "Tmp"


def test_pdf_merge():
    from core.converter_pdf_chromium import MarkdownToPdfConverter
    converter = MarkdownToPdfConverter(FIXTURES, TMP)
    assert converter.convert_merged(output_filename="sample_merged"), "PDF 合并失败"
    assert (TMP / "sample_merged.pdf").exists(), "合并 PDF 未生成"
    print("[OK] PDF 合并")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    test_pdf_merge()
