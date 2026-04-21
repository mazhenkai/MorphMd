#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_all.py - 运行所有测试
运行: python Tests/run_all.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

TMP = ROOT / "Tmp"
TMP.mkdir(exist_ok=True)

from test_html import test_html_conversion
from test_pdf import test_pdf_conversion
from test_pdf_merge import test_pdf_merge
from test_add_cover import test_add_cover
from test_page_number import test_add_page_numbers
from test_code_wrap import test_code_wrap_css, test_code_wrap_pdf_generated
from test_pipeline import test_step1_merge, test_step2_add_toc_pages, test_step3_add_cover, test_step4_clean_metadata

TESTS = [
    test_html_conversion, test_pdf_conversion, test_pdf_merge,
    test_add_cover, test_add_page_numbers,
    test_code_wrap_css, test_code_wrap_pdf_generated,
    test_step1_merge, test_step2_add_toc_pages, test_step3_add_cover, test_step4_clean_metadata,
]

if __name__ == "__main__":
    passed = failed = 0
    for t in TESTS:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"[FAIL] {t.__name__}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过 / {failed} 失败")
    sys.exit(0 if failed == 0 else 1)
