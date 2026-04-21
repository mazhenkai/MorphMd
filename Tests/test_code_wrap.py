#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).parent / "fixtures"
TMP = ROOT / "Tmp"


def test_code_wrap_css():
    """验证 pre 块包含 white-space: pre-wrap，确保长代码行在 PDF 中自动换行"""
    from core.converter_pdf_chromium import MarkdownToPdfConverter
    converter = MarkdownToPdfConverter(FIXTURES, TMP)
    assert "white-space: pre-wrap" in converter.css_style, \
        "BUG: pre 块缺少 white-space: pre-wrap，长代码行在 PDF 中不会换行"
    assert "word-break: break-all" in converter.css_style, \
        "BUG: pre 块缺少 word-break: break-all"
    print("[OK] pre 块包含换行 CSS")


def test_code_wrap_pdf_generated():
    """验证含长代码行的 md 能成功生成 PDF"""
    from core.converter_pdf_chromium import MarkdownToPdfConverter
    TMP.mkdir(exist_ok=True)
    converter = MarkdownToPdfConverter(FIXTURES, TMP)
    assert converter.convert_file(FIXTURES / "long_code_lines.md"), "PDF 转换失败"
    assert (TMP / "long_code_lines.pdf").exists(), "PDF 文件未生成"
    print("[OK] 长代码行 PDF 生成成功")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    test_code_wrap_css()
    test_code_wrap_pdf_generated()
