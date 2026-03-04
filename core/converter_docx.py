#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown转DOCX工具（使用Pandoc）

功能: 将Markdown文件转换为Word DOCX格式
输出: 保存到指定目录，完美支持emoji、表格、格式

依赖:
    pip install pypandoc
    安装 Pandoc: https://pandoc.org/installing.html
    或者: choco install pandoc (Windows)

优势:
    - 完美支持彩色 emoji 😊 🎉 🔥
    - 保留所有 Markdown 格式
    - 支持表格、代码块、公式
    - 可编辑的 Word 文档

作者: Claude
日期: 2025-12-04
"""

import os
import sys
from pathlib import Path
from datetime import datetime

try:
    import pypandoc
except ImportError:
    print("=" * 80)
    print("错误: 缺少必要的依赖库")
    print("=" * 80)
    print("\n请安装以下依赖:")
    print("  pip install pypandoc")
    print("\n还需要安装 Pandoc:")
    print("  下载地址: https://pandoc.org/installing.html")
    print("  Windows: choco install pandoc")
    print("  或下载安装包: https://github.com/jgm/pandoc/releases")
    print("=" * 80)
    sys.exit(1)

# 尝试导入配置模块
try:
    from config import config
    USE_CONFIG = True
except ImportError:
    USE_CONFIG = False
    print("[WARNING] 未找到config.py，将使用默认配置")


class MarkdownToDocxConverter:
    """Markdown转DOCX转换器（Pandoc版本）"""

    def __init__(self, input_dir, output_dir):
        """
        初始化转换器

        Args:
            input_dir: 输入目录(包含Markdown文件)
            output_dir: 输出目录(保存DOCX文件)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 检查 Pandoc 是否安装
        self._check_pandoc()

        # Pandoc 额外参数
        self.extra_args = [
            '--standalone',
            # '--toc',  # 生成目录（可能导致Word提示更新引用）
            '--syntax-highlighting=tango',  # 代码高亮样式
        ]

    def _check_pandoc(self):
        """检查 Pandoc 是否已安装"""
        try:
            version = pypandoc.get_pandoc_version()
            print(f"[INFO] 找到 Pandoc 版本: {version}")
        except OSError:
            print("=" * 80)
            print("[ERROR] 未找到 Pandoc!")
            print("=" * 80)
            print("\n请安装 Pandoc:")
            print("  下载地址: https://pandoc.org/installing.html")
            print("  Windows: choco install pandoc")
            print("  或下载安装包: https://github.com/jgm/pandoc/releases")
            print("=" * 80)
            sys.exit(1)

    def convert_file(self, md_file):
        """
        转换单个Markdown文件为DOCX

        Args:
            md_file: Markdown文件路径

        Returns:
            bool: 转换是否成功
        """
        try:
            # 输出DOCX文件路径
            docx_file = self.output_dir / f"{md_file.stem}.docx"

            print(f"\n[1/3] 读取文件: {md_file.name}")
            print(f"[2/3] 使用 Pandoc 转换为 DOCX...")

            # 使用 Pandoc 转换
            pypandoc.convert_file(
                str(md_file),
                'docx',
                outputfile=str(docx_file),
                extra_args=self.extra_args
            )

            print(f"[3/3] [OK] 成功: {docx_file.name}")
            return True

        except Exception as e:
            print(f"[ERROR] [FAIL] 失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def convert_all(self):
        """转换目录下的所有Markdown文件"""
        # 查找所有Markdown文件
        md_files = list(self.input_dir.glob("*.md"))

        if not md_files:
            print(f"[WARNING] 在 {self.input_dir} 中没有找到Markdown文件")
            return

        print("=" * 80)
        print(f"Markdown转DOCX工具（Pandoc版 - 支持Emoji）")
        print("=" * 80)
        print(f"\n输入目录: {self.input_dir}")
        print(f"输出目录: {self.output_dir}")
        print(f"找到文件: {len(md_files)} 个\n")

        # 逐个转换
        success_count = 0
        fail_count = 0

        for idx, md_file in enumerate(md_files, 1):
            print(f"\n{'=' * 80}")
            print(f"[{idx}/{len(md_files)}] 处理: {md_file.name}")
            print('=' * 80)

            if self.convert_file(md_file):
                success_count += 1
            else:
                fail_count += 1

        # 输出统计
        print("\n" + "=" * 80)
        print("转换完成!")
        print("=" * 80)
        print(f"\n[OK] 成功: {success_count} 个")
        print(f"[FAIL] 失败: {fail_count} 个")
        print(f"\nDOCX文件保存在: {self.output_dir}")
        print("\n提示: 可以在 Microsoft Word 或 WPS 中打开编辑")
        print("=" * 80)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='将Markdown文件转换为DOCX（支持Emoji）')
    parser.add_argument('-i', '--input', type=str, help='输入目录路径（包含.md文件）')
    parser.add_argument('-o', '--output', type=str, help='输出目录路径（保存.docx文件）')
    parser.add_argument('-f', '--file', type=str, help='单个Markdown文件路径（优先级高于-i参数）')

    args = parser.parse_args()

    # 设置路径
    script_dir = Path(__file__).parent

    # 如果指定了单个文件
    if args.file:
        md_file = Path(args.file)

        # 检查文件是否存在
        if not md_file.exists():
            print(f"[ERROR] 文件不存在: {md_file}")
            sys.exit(1)

        # 检查是否为.md文件
        if md_file.suffix.lower() != '.md':
            print(f"[ERROR] 不是Markdown文件: {md_file}")
            sys.exit(1)

        # 确定输出目录
        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = md_file.parent  # 默认输出到文件所在目录

        # 创建转换器
        input_dir = md_file.parent
        converter = MarkdownToDocxConverter(input_dir, output_dir)

        # 转换单个文件
        print("=" * 80)
        print(f"Markdown转DOCX工具（Pandoc版） - 单文件模式")
        print("=" * 80)
        print(f"\n输入文件: {md_file}")
        print(f"输出目录: {output_dir}\n")

        success = converter.convert_file(md_file)

        if success:
            print("\n" + "=" * 80)
            print("[OK] 转换成功! Emoji已完美支持!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("[FAIL] 转换失败")
            print("=" * 80)
            sys.exit(1)

    # 否则处理整个目录
    else:
        # 从配置文件读取默认路径
        if USE_CONFIG:
            default_input = config.get('DEFAULT_INPUT_DIR', '../Proposal')
            default_output = config.get('DEFAULT_OUTPUT_DIR', '../Proposal')
        else:
            default_input = '../Proposal'
            default_output = '../Proposal'

        if args.input:
            input_dir = Path(args.input)
        else:
            input_dir = script_dir / default_input

        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = input_dir  # 默认输出到输入目录

        # 检查输入目录是否存在
        if not input_dir.exists():
            print(f"[ERROR] 输入目录不存在: {input_dir}")
            sys.exit(1)

        # 创建转换器
        converter = MarkdownToDocxConverter(input_dir, output_dir)

        # 执行转换
        converter.convert_all()


if __name__ == "__main__":
    main()
