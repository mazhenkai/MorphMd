#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_pipeline.py - 测试完整 PDF 生成流程：
  1. merge_convert  — 合并 md → PDF（含元数据）
  2. add_toc_pages  — 重建带页码目录 + 底部页码
  3. add_cover      — 加封面
  4. clean_metadata — 清除内部元数据
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

PIPLINE_DIR = Path(__file__).parent / "pipline"
TMP = ROOT / "Tmp" / "pipline_test"
COVER_MD = PIPLINE_DIR / "cover" / "cover.md"


def setup():
    TMP.mkdir(parents=True, exist_ok=True)


def test_step1_merge():
    from core.converter_pdf_chromium import MarkdownToPdfConverter
    from pypdf import PdfReader
    import json

    converter = MarkdownToPdfConverter(PIPLINE_DIR, TMP)
    assert converter.convert_merged(output_filename="test_doc"), "合并失败"

    pdf = TMP / "test_doc.pdf"
    assert pdf.exists(), "PDF 未生成"

    meta = PdfReader(str(pdf)).metadata or {}
    assert meta.get("/MorphMdSections"), "元数据 MorphMdSections 缺失"
    assert meta.get("/MorphMdPages"), "元数据 MorphMdPages 缺失"

    pages = json.loads(meta["/MorphMdPages"])
    assert pages["0"] == 1, f"第一章页码应为1，实际为 {pages['0']}"
    print(f"[OK] Step1: 合并完成，章节页码: {pages}")


def test_step2_add_toc_pages():
    from pypdf import PdfReader
    from core.pdf_utils import add_page_numbers
    import subprocess

    pdf = TMP / "test_doc.pdf"
    result = subprocess.run(
        [sys.executable, str(ROOT / "Bin/add_toc_pages.py"), str(pdf.relative_to(ROOT))],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    assert result.returncode == 0, f"add_toc_pages 失败: {result.stderr}"

    reader = PdfReader(str(pdf))
    assert len(reader.pages) >= 2, "PDF 页数不足"
    print(f"[OK] Step2: 目录页码添加完成，总页数: {len(reader.pages)}")


def test_step3_add_cover():
    import subprocess
    from pypdf import PdfReader

    pdf = TMP / "test_doc.pdf"
    pages_before = len(PdfReader(str(pdf)).pages)

    result = subprocess.run(
        [sys.executable, str(ROOT / "Bin/add_cover.py"),
         str(COVER_MD.relative_to(ROOT)),
         str(pdf.relative_to(ROOT)),
         str(pdf.relative_to(ROOT)),
         "--mode", "overwrite"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    assert result.returncode == 0, f"add_cover 失败: {result.stderr}"

    pages_after = len(PdfReader(str(pdf)).pages)
    assert pages_after > pages_before, "封面未添加"
    print(f"[OK] Step3: 封面添加完成，页数 {pages_before} → {pages_after}")


def test_step4_clean_metadata():
    import subprocess
    from pypdf import PdfReader

    pdf = TMP / "test_doc.pdf"
    result = subprocess.run(
        [sys.executable, str(ROOT / "Bin/clean_metadata.py"), str(pdf.relative_to(ROOT))],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    assert result.returncode == 0, f"clean_metadata 失败: {result.stderr}"

    meta = PdfReader(str(pdf)).metadata or {}
    assert "/MorphMdSections" not in meta, "MorphMdSections 未清除"
    assert "/MorphMdPages" not in meta, "MorphMdPages 未清除"
    print("[OK] Step4: 元数据清除完成")


if __name__ == "__main__":
    setup()
    test_step1_merge()
    test_step2_add_toc_pages()
    test_step3_add_cover()
    test_step4_clean_metadata()
    print("\n[OK] 完整流程测试通过")
