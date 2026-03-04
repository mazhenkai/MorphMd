#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown 文档转换工具包

提供统一的接口将 Markdown 文件转换为 HTML、PDF 或 DOCX 格式。

使用示例:
    from md_converter import convert

    # 转换为 HTML
    convert("文件.md", format="html")

    # 转换为 PDF（彩色emoji）
    convert("文件.md", format="pdf")

    # 转换为 DOCX (Word)
    convert("文件.md", format="docx")

    # 指定输出目录
    convert("文件.md", format="pdf", output_dir="./output")

作者: Claude
日期: 2025-12-04
版本: 1.0.0
"""

from pathlib import Path
import sys

# 导入配置
try:
    from .config import config
except ImportError:
    config = None


def convert(input_file, format="html", output_dir=None):
    """
    转换 Markdown 文件为指定格式

    Args:
        input_file (str): 输入的 Markdown 文件路径
        format (str): 输出格式，可选: 'html', 'pdf', 'docx'
        output_dir (str, optional): 输出目录，默认为输入文件所在目录

    Returns:
        str: 输出文件的路径

    Raises:
        ValueError: 不支持的格式
        FileNotFoundError: 输入文件不存在

    Examples:
        >>> convert("test.md", format="html")
        'test.html'

        >>> convert("test.md", format="pdf", output_dir="./output")
        './output/test.pdf'
    """
    # 验证输入文件
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"文件不存在: {input_file}")

    if input_path.suffix.lower() != '.md':
        raise ValueError(f"不是 Markdown 文件: {input_file}")

    # 确定输出目录
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    # 根据格式调用对应的转换器
    format = format.lower()

    if format == "html":
        return _convert_to_html(input_path, output_dir)
    elif format == "pdf":
        return _convert_to_pdf(input_path, output_dir)
    elif format == "docx" or format == "word":
        return _convert_to_docx(input_path, output_dir)
    else:
        raise ValueError(f"不支持的格式: {format}。可选: 'html', 'pdf', 'docx'")


def _convert_to_html(input_file, output_dir):
    """转换为 HTML"""
    from .converter_html import MarkdownToHtmlConverter

    converter = MarkdownToHtmlConverter(input_file.parent, output_dir)
    success = converter.convert_file(input_file)

    if success:
        output_file = output_dir / f"{input_file.stem}.html"
        return str(output_file)
    else:
        raise RuntimeError(f"HTML 转换失败: {input_file}")


def _convert_to_pdf(input_file, output_dir):
    """转换为 PDF（使用 Chromium，支持彩色 emoji）"""
    from .converter_pdf_chromium import MarkdownToPdfConverter

    converter = MarkdownToPdfConverter(input_file.parent, output_dir)
    success = converter.convert_file(input_file)

    if success:
        output_file = output_dir / f"{input_file.stem}.pdf"
        return str(output_file)
    else:
        raise RuntimeError(f"PDF 转换失败: {input_file}")


def _convert_to_docx(input_file, output_dir):
    """转换为 DOCX (Word)"""
    from .converter_docx import MarkdownToDocxConverter

    converter = MarkdownToDocxConverter(input_file.parent, output_dir)
    success = converter.convert_file(input_file)

    if success:
        output_file = output_dir / f"{input_file.stem}.docx"
        return str(output_file)
    else:
        raise RuntimeError(f"DOCX 转换失败: {input_file}")


def batch_convert(input_dir, format="html", output_dir=None):
    """
    批量转换目录下的所有 Markdown 文件

    Args:
        input_dir (str): 输入目录（包含 .md 文件）
        format (str): 输出格式，可选: 'html', 'pdf', 'docx'
        output_dir (str, optional): 输出目录，默认为输入目录

    Returns:
        dict: 转换结果 {'success': [...], 'failed': [...]}

    Examples:
        >>> result = batch_convert("./docs", format="pdf")
        >>> print(f"成功: {len(result['success'])}, 失败: {len(result['failed'])}")
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"目录不存在: {input_dir}")

    if output_dir is None:
        output_dir = input_path

    # 查找所有 Markdown 文件
    md_files = list(input_path.glob("*.md"))

    if not md_files:
        print(f"[WARNING] 在 {input_dir} 中没有找到 Markdown 文件")
        return {'success': [], 'failed': []}

    print(f"找到 {len(md_files)} 个 Markdown 文件")

    # 逐个转换
    results = {'success': [], 'failed': []}

    for idx, md_file in enumerate(md_files, 1):
        print(f"\n[{idx}/{len(md_files)}] 转换: {md_file.name}")
        try:
            output_file = convert(md_file, format=format, output_dir=output_dir)
            results['success'].append(str(output_file))
            print(f"  ✅ 成功: {Path(output_file).name}")
        except Exception as e:
            results['failed'].append(str(md_file))
            print(f"  ❌ 失败: {str(e)}")

    # 输出统计
    print("\n" + "=" * 80)
    print(f"转换完成! 成功: {len(results['success'])}, 失败: {len(results['failed'])}")
    print("=" * 80)

    return results


# 版本信息
__version__ = "0.0.1"
__author__ = "Zhenkai Ma"
__all__ = ['convert', 'batch_convert', 'config']
