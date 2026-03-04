#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MorphMd - Markdown 转换工具
支持命令行和批处理模式
"""

import argparse
from pathlib import Path
import sys

from core.utils import setup_logger, ensure_dir
from core.config import Config


def convert_file(input_file, output_dir, format_type, logger):
    """转换单个文件"""
    input_path = Path(input_file)

    if not input_path.exists():
        logger.error(f"文件不存在: {input_file}")
        return False

    if input_path.suffix.lower() != '.md':
        logger.error(f"不是 Markdown 文件: {input_file}")
        return False

    try:
        if format_type == 'html':
            from core.converter_html import MarkdownToHtmlConverter
            converter = MarkdownToHtmlConverter(input_path.parent, output_dir)
        elif format_type == 'pdf':
            from core.converter_pdf_chromium import MarkdownToPdfConverter
            converter = MarkdownToPdfConverter(input_path.parent, output_dir)
        elif format_type == 'docx':
            from core.converter_docx import MarkdownToDocxConverter
            converter = MarkdownToDocxConverter(input_path.parent, output_dir)
        else:
            logger.error(f"不支持的格式: {format_type}")
            return False

        success = converter.convert_file(input_path)
        if success:
            output_file = Path(output_dir) / f"{input_path.stem}.{format_type}"
            logger.info(f"✅ 转换成功: {output_file}")
        return success
    except Exception as e:
        logger.error(f"❌ 转换失败: {str(e)}")
        return False


def batch_convert(input_dir, output_dir, format_type, logger):
    """批量转换目录"""
    input_path = Path(input_dir)
    md_files = list(input_path.glob("*.md"))

    if not md_files:
        logger.warning(f"在 {input_dir} 中没有找到 Markdown 文件")
        return

    logger.info(f"找到 {len(md_files)} 个文件")
    success_count = 0

    for idx, md_file in enumerate(md_files, 1):
        logger.info(f"[{idx}/{len(md_files)}] 转换: {md_file.name}")
        if convert_file(md_file, output_dir, format_type, logger):
            success_count += 1

    logger.info(f"完成! 成功: {success_count}/{len(md_files)}")


def main():
    parser = argparse.ArgumentParser(description='MorphMd - Markdown 转换工具')
    parser.add_argument('--input', '-i', help='输入文件或目录')
    parser.add_argument('--output', '-o', help='输出目录')
    parser.add_argument('--format', '-f', choices=['html', 'pdf', 'docx'],
                       default='pdf', help='输出格式 (默认: pdf)')
    parser.add_argument('--batch', '-b', action='store_true',
                       help='批量处理模式')

    args = parser.parse_args()

    # 设置日志
    logger = setup_logger()

    # 加载配置
    config = Config()

    # 确定输入输出目录
    input_path = args.input or config.get('INPUT_DIR', 'Input')
    output_path = args.output or config.get('OUTPUT_DIR', f'Output/{args.format}')

    ensure_dir(output_path)

    logger.info("=" * 60)
    logger.info("MorphMd - Markdown 转换工具")
    logger.info("=" * 60)

    # 判断是文件还是目录
    path = Path(input_path)

    if path.is_file():
        convert_file(input_path, output_path, args.format, logger)
    elif path.is_dir():
        batch_convert(input_path, output_path, args.format, logger)
    else:
        logger.error(f"路径不存在: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
