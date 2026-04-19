#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).parent / "fixtures"
TMP = ROOT / "Tmp"


def test_html_conversion():
    from core.converter_html import MarkdownToHtmlConverter
    converter = MarkdownToHtmlConverter(FIXTURES, TMP)
    assert converter.convert_file(FIXTURES / "sample.md"), "HTML 转换失败"
    assert (TMP / "sample.html").exists(), "HTML 文件未生成"
    print("[OK] HTML 转换")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    test_html_conversion()
