#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
转换器测试
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils import setup_logger


def test_html_conversion():
    """测试 HTML 转换"""
    from core.converter_html import MarkdownToHtmlConverter

    input_dir = Path(__file__).parent / "fixtures"
    output_dir = Path(__file__).parent.parent / "Tmp"

    converter = MarkdownToHtmlConverter(input_dir, output_dir)
    success = converter.convert_file(input_dir / "sample.md")

    assert success, "HTML 转换失败"
    print("✅ HTML 转换测试通过")


if __name__ == "__main__":
    logger = setup_logger()
    test_html_conversion()
