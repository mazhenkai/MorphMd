#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

TMP = ROOT / "Tmp"


def test_add_cover():
    from pypdf import PdfReader
    from core.converter_pdf_chromium import MarkdownToPdfConverter

    fixtures = Path(__file__).parent / "fixtures"
    converter = MarkdownToPdfConverter(fixtures, TMP)
    converter.convert_file(fixtures / "sample.md")

    cover_md = ROOT / "Template/Cover/Samples/示例封面.md"
    content_pdf = TMP / "sample.pdf"
    output_pdf = TMP / "sample_covered.pdf"

    import importlib.util
    spec = importlib.util.spec_from_file_location("add_cover", ROOT / "Bin/add_cover.py")
    mod = importlib.util.module_from_spec(spec)
    sys.argv = ["add_cover.py", str(cover_md.relative_to(ROOT)), str(content_pdf.relative_to(ROOT)), str(output_pdf.relative_to(ROOT))]
    spec.loader.exec_module(mod)
    mod.main()

    assert output_pdf.exists(), "封面 PDF 未生成"
    assert len(PdfReader(str(output_pdf)).pages) > 1, "封面合并页数不足"
    print("[OK] 封面合并")


if __name__ == "__main__":
    TMP.mkdir(exist_ok=True)
    test_add_cover()
