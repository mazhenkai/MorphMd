#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Markdown转HTML工具

功能: 将process目录下的所有Markdown文件转换为HTML静态文件
输出: 保存到output目录，支持数学公式渲染

依赖:
    pip install markdown2

作者: Claude
日期: 2025-10-20
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import markdown2
except ImportError:
    print("=" * 80)
    print("错误: 缺少必要的依赖库")
    print("=" * 80)
    print("\n请安装以下依赖:")
    print("  pip install markdown2")
    print("=" * 80)
    sys.exit(1)


class MarkdownToHtmlConverter:
    """Markdown转HTML转换器"""

    def __init__(self, input_dir, output_dir):
        """
        初始化转换器

        Args:
            input_dir: 输入目录(包含Markdown文件)
            output_dir: 输出目录(保存HTML文件)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # CSS样式
        self.css_style = """
        <style>
            @charset "UTF-8";

            body {
                font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "SimSun", "宋体", Arial, sans-serif;
                font-size: 16px;
                line-height: 1.8;
                color: #333;
                max-width: 1000px;
                margin: 0 auto;
                padding: 40px 20px;
                background: #fafafa;
            }

            .container {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            h1 {
                font-size: 32px;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 12px;
                margin-top: 40px;
                margin-bottom: 24px;
            }

            h1:first-child {
                margin-top: 0;
            }

            h2 {
                font-size: 26px;
                font-weight: bold;
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 10px;
                margin-top: 35px;
                margin-bottom: 20px;
            }

            h3 {
                font-size: 22px;
                font-weight: bold;
                color: #555;
                margin-top: 28px;
                margin-bottom: 16px;
            }

            h4 {
                font-size: 18px;
                font-weight: bold;
                color: #666;
                margin-top: 24px;
                margin-bottom: 12px;
            }

            p {
                margin: 12px 0;
                text-align: justify;
                line-height: 1.8;
            }

            /* 数学公式样式 */
            mjx-container {
                margin: 20px 0 !important;
                overflow-x: auto;
            }

            mjx-container[display="true"] {
                margin: 30px 0 !important;
                text-align: center;
            }

            /* 行内公式 */
            mjx-container[jax="SVG"][display="false"] {
                margin: 0 4px !important;
                vertical-align: middle;
            }

            code {
                font-family: "Consolas", "Courier New", "Microsoft YaHei Mono", monospace;
                font-size: 14px;
                background-color: #f4f4f4;
                padding: 3px 6px;
                border-radius: 3px;
                color: #c7254e;
            }

            pre {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-left: 4px solid #3498db;
                border-radius: 4px;
                padding: 16px;
                overflow-x: auto;
                margin: 20px 0;
                line-height: 1.5;
            }

            pre code {
                background-color: transparent;
                padding: 0;
                color: #333;
                font-size: 13px;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                margin: 24px 0;
                font-size: 14px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }

            table th {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px;
                text-align: left;
                border: 1px solid #2980b9;
            }

            table td {
                padding: 10px 12px;
                border: 1px solid #ddd;
                vertical-align: top;
            }

            table tr:nth-child(even) {
                background-color: #f9f9f9;
            }

            table tr:hover {
                background-color: #f5f5f5;
            }

            ul, ol {
                margin: 16px 0;
                padding-left: 32px;
            }

            li {
                margin: 8px 0;
                line-height: 1.6;
            }

            blockquote {
                border-left: 4px solid #3498db;
                background-color: #f9f9f9;
                padding: 12px 20px;
                margin: 20px 0;
                color: #555;
                font-style: italic;
            }

            hr {
                border: none;
                border-top: 2px solid #ddd;
                margin: 35px 0;
            }

            a {
                color: #3498db;
                text-decoration: none;
                transition: color 0.2s;
            }

            a:hover {
                color: #2980b9;
                text-decoration: underline;
            }

            img {
                max-width: 100%;
                height: auto;
                display: block;
                margin: 20px auto;
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }

            strong {
                font-weight: bold;
                color: #2c3e50;
            }

            em {
                font-style: italic;
                color: #555;
            }

            /* 页脚样式 */
            .footer {
                margin-top: 60px;
                padding-top: 20px;
                border-top: 2px solid #eee;
                text-align: center;
                color: #999;
                font-size: 14px;
            }

            /* 返回顶部按钮 */
            .back-to-top {
                position: fixed;
                bottom: 30px;
                right: 30px;
                background-color: #3498db;
                color: white;
                padding: 12px 16px;
                border-radius: 4px;
                text-decoration: none;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                transition: background-color 0.3s;
                display: none;
                z-index: 1000;
            }

            .back-to-top:hover {
                background-color: #2980b9;
            }

            /* 左上角浮动导航 */
            .toc-nav {
                position: fixed;
                top: 20px;
                left: 20px;
                max-width: 280px;
                max-height: calc(100vh - 100px);
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                box-shadow: 0 2px 12px rgba(0,0,0,0.1);
                overflow-y: auto;
                padding: 15px;
                font-size: 13px;
                z-index: 999;
                transition: opacity 0.3s, transform 0.3s;
            }

            .toc-nav.hidden {
                opacity: 0;
                transform: translateX(-100%);
                pointer-events: none;
            }

            .toc-nav-header {
                font-weight: bold;
                font-size: 14px;
                color: #2c3e50;
                margin-bottom: 10px;
                padding-bottom: 8px;
                border-bottom: 2px solid #3498db;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .toc-toggle {
                cursor: pointer;
                color: #3498db;
                font-size: 18px;
                user-select: none;
            }

            .toc-nav ul {
                list-style: none;
                padding-left: 0;
                margin: 0;
            }

            .toc-nav ul ul {
                padding-left: 15px;
            }

            .toc-nav li {
                margin: 5px 0;
                line-height: 1.4;
            }

            .toc-nav a {
                color: #555;
                text-decoration: none;
                display: block;
                padding: 3px 0;
                transition: color 0.2s;
            }

            .toc-nav a:hover {
                color: #3498db;
            }

            .toc-nav a.active {
                color: #3498db;
                font-weight: bold;
            }

            .toc-nav::-webkit-scrollbar {
                width: 6px;
            }

            .toc-nav::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 3px;
            }

            .toc-nav::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 3px;
            }

            .toc-nav::-webkit-scrollbar-thumb:hover {
                background: #555;
            }

            /* 响应式设计 */
            @media (max-width: 768px) {
                body {
                    padding: 20px 10px;
                    font-size: 14px;
                }

                .container {
                    padding: 20px;
                }

                h1 {
                    font-size: 24px;
                }

                h2 {
                    font-size: 20px;
                }

                h3 {
                    font-size: 18px;
                }

                table {
                    font-size: 12px;
                }

                pre {
                    font-size: 12px;
                }

                .toc-nav {
                    display: none;
                }
            }
        </style>
        """

    def fix_multiline_formulas(self, html_content):
        """
        修复HTML中的多行公式渲染问题
        
        Args:
            html_content: HTML文件内容
            
        Returns:
            修复后的HTML内容
        """
        # 1. 修复cases环境 - 移除$$内的<br/>标签并保持正确的换行
        def fix_cases_environment(match):
            formula_content = match.group(1)
            # 移除<br/>标签，保持原始换行
            formula_content = re.sub(r'<br\s*/?>', '\n', formula_content)
            # 移除HTML转义的符号
            formula_content = formula_content.replace('&amp;', '&')
            formula_content = formula_content.replace('&lt;', '<')
            formula_content = formula_content.replace('&gt;', '>')
            
            # 修复LaTeX换行符 - 只在cases环境内修复
            if '\\begin{cases}' in formula_content:
                # 在cases环境内，将单个反斜杠替换为双反斜杠
                formula_content = formula_content.replace('\\', '\\\\')
                # 修复过度替换的问题，恢复正确的LaTeX命令
                latex_commands = [
                    '\\\\begin', '\\\\end', '\\\\text', '\\\\times', '\\\\times',
                    '\\\\frac', '\\\\left', '\\\\right', '\\\\leq', '\\\\geq',
                    '\\\\lt', '\\\\gt', '\\\\sqrt', '\\\\pi', '\\\\exp',
                    '\\\\sum', '\\\\in', '\\\\to', '\\\\infty', '\\\\approx',
                    '\\\\mu', '\\\\sigma', '\\\\alpha', '\\\\beta', '\\\\gamma',
                    '\\\\delta', '\\\\epsilon', '\\\\theta', '\\\\lambda',
                    '\\\\phi', '\\\\psi', '\\\\omega', '\\\\mathbf', '\\\\mathcal',
                    '\\\\mathbb', '\\\\mathrm', '\\\\mathit', '\\\\mathbfit',
                    '\\\\boldsymbol', '\\\\hat', '\\\\tilde', '\\\\bar',
                    '\\\\vec', '\\\\dot', '\\\\ddot', '\\\\prime', '\\\\partial',
                    '\\\\nabla', '\\\\infty', '\\\\emptyset', '\\\\subset',
                    '\\\\supset', '\\\\subseteq', '\\\\supseteq', '\\\\in',
                    '\\\\ni', '\\\\notin', '\\\\cup', '\\\\cap', '\\\\setminus',
                    '\\\\oplus', '\\\\otimes', '\\\\cdot', '\\\\bullet',
                    '\\\\ast', '\\\\star', '\\\\circ', '\\\\wedge', '\\\\vee',
                    '\\\\neg', '\\\\land', '\\\\lor', '\\\\rightarrow',
                    '\\\\leftarrow', '\\\\leftrightarrow', '\\\\Rightarrow',
                    '\\\\Leftarrow', '\\\\Leftrightarrow', '\\\\mapsto', '\\\\to',
                    '\\\\sim', '\\\\simeq', '\\\\cong', '\\\\equiv', '\\\\propto',
                    '\\\\approx', '\\\\neq', '\\\\leq', '\\\\geq', '\\\\ll',
                    '\\\\gg', '\\\\subset', '\\\\supset', '\\\\subseteq',
                    '\\\\supseteq', '\\\\in', '\\\\ni', '\\\\notin',
                    '\\\\cup', '\\\\cap', '\\\\Delta'
                ]
                
                for cmd in latex_commands:
                    formula_content = formula_content.replace(cmd, cmd[1:])  # 移除多余的反斜杠
            
            # 重新构建公式
            return f'$$\n{formula_content}\n$$'
        
        # 匹配$$...$$格式的公式
        pattern = r'\$\$(.*?)\$\$'
        html_content = re.sub(pattern, fix_cases_environment, html_content, flags=re.DOTALL)
        
        return html_content

    def convert_file(self, md_file):
        """
        转换单个Markdown文件为HTML

        Args:
            md_file: Markdown文件路径

        Returns:
            bool: 转换是否成功
        """
        try:
            # 读取Markdown文件
            print(f"\n[1/3] 读取文件: {md_file.name}")
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            # 转换Markdown为HTML
            print(f"[2/3] 转换为HTML...")
            html_content = markdown2.markdown(
                md_content,
                extras=[
                    'tables',
                    'fenced-code-blocks',
                    'code-friendly',
                    'break-on-newline',
                    'header-ids',
                    'toc',  # 目录
                ]
            )

            # 修复多行公式渲染问题
            html_content = self.fix_multiline_formulas(html_content)

            # 构建完整的HTML文档
            full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{md_file.stem}</title>

    <!-- MathJax配置 - 用于渲染LaTeX数学公式 -->
    <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true,
        tags: 'none'
      }},
      svg: {{
        fontCache: 'global',
        scale: 1.15
      }},
      startup: {{
        ready: () => {{
          console.log('MathJax加载完成');
          MathJax.startup.defaultReady();
        }}
      }}
    }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js" async></script>

    {self.css_style}
</head>
<body>
    <!-- 左上角浮动导航 -->
    <div class="toc-nav" id="tocNav">
        <div class="toc-nav-header">
            <span>📑 目录导航</span>
            <span class="toc-toggle" id="tocToggle">×</span>
        </div>
        <div id="tocContent"></div>
    </div>

    <div class="container">
        {html_content}

        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>原始文件: {md_file.name}</p>
        </div>
    </div>

    <a href="#" class="back-to-top" id="backToTop">↑ 返回顶部</a>

    <!-- 目录导航功能 -->
    <script>
    (function() {{
        // 生成目录
        function generateTOC() {{
            const headers = document.querySelectorAll('.container h2, .container h3, .container h4');
            if (headers.length === 0) return;

            const tocContent = document.getElementById('tocContent');
            const ul = document.createElement('ul');

            let currentH2 = null;
            let currentH3 = null;

            headers.forEach((header, index) => {{
                const level = header.tagName;
                const text = header.textContent;
                const id = header.id || 'header-' + index;

                if (!header.id) {{
                    header.id = id;
                }}

                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = '#' + id;
                a.textContent = text;
                a.setAttribute('data-target', id);
                li.appendChild(a);

                if (level === 'H2') {{
                    ul.appendChild(li);
                    currentH2 = document.createElement('ul');
                    li.appendChild(currentH2);
                    currentH3 = null;
                }} else if (level === 'H3' && currentH2) {{
                    currentH2.appendChild(li);
                    currentH3 = document.createElement('ul');
                    li.appendChild(currentH3);
                }} else if (level === 'H4' && currentH3) {{
                    currentH3.appendChild(li);
                }}
            }});

            tocContent.appendChild(ul);

            // 点击目录项平滑滚动
            const links = tocContent.querySelectorAll('a');
            links.forEach(link => {{
                link.addEventListener('click', function(e) {{
                    e.preventDefault();
                    const targetId = this.getAttribute('data-target');
                    const targetElement = document.getElementById(targetId);
                    if (targetElement) {{
                        targetElement.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }}
                }});
            }});
        }}

        // 高亮当前章节
        function highlightCurrentSection() {{
            const headers = document.querySelectorAll('.container h2, .container h3, .container h4');
            const tocLinks = document.querySelectorAll('.toc-nav a');

            let current = '';
            const scrollPos = window.pageYOffset + 100;

            headers.forEach(header => {{
                const sectionTop = header.offsetTop;
                if (scrollPos >= sectionTop) {{
                    current = header.id;
                }}
            }});

            tocLinks.forEach(link => {{
                link.classList.remove('active');
                if (link.getAttribute('data-target') === current) {{
                    link.classList.add('active');
                }}
            }});
        }}

        // 切换导航显示/隐藏
        const tocToggle = document.getElementById('tocToggle');
        const tocNav = document.getElementById('tocNav');
        let tocVisible = true;

        tocToggle.addEventListener('click', function() {{
            tocVisible = !tocVisible;
            if (tocVisible) {{
                tocNav.classList.remove('hidden');
                tocToggle.textContent = '×';
            }} else {{
                tocNav.classList.add('hidden');
                tocToggle.textContent = '📑';
            }}
        }});

        // 初始化
        generateTOC();

        // 滚动时高亮
        window.addEventListener('scroll', highlightCurrentSection);

        // 初始高亮
        highlightCurrentSection();
    }})();
    </script>

    <!-- 返回顶部功能 -->
    <script>
    window.addEventListener('scroll', function() {{
        const backToTop = document.getElementById('backToTop');
        if (window.pageYOffset > 300) {{
            backToTop.style.display = 'block';
        }} else {{
            backToTop.style.display = 'none';
        }}
    }});

    document.getElementById('backToTop').addEventListener('click', function(e) {{
        e.preventDefault();
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }});
    </script>
</body>
</html>"""

            # 输出HTML文件路径
            html_file = self.output_dir / f"{md_file.stem}.html"

            # 保存HTML文件
            print(f"[3/3] 保存HTML文件...")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(full_html)

            print(f"      [OK] 成功: {html_file.name}")
            return True

        except Exception as e:
            print(f"      [ERROR] [FAIL] 失败: {str(e)}")
            return False

    def convert_all(self):
        """转换目录下的所有Markdown文件"""
        # 查找所有Markdown文件
        md_files = list(self.input_dir.glob("*.md"))

        if not md_files:
            print(f"[WARNING] 在 {self.input_dir} 中没有找到Markdown文件")
            return

        print("=" * 80)
        print(f"Markdown转HTML工具")
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
        print(f"\nHTML文件保存在: {self.output_dir}")
        print("\n提示: 可以直接在浏览器中打开HTML文件查看效果")
        print("=" * 80)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='将Markdown文件转换为HTML')
    parser.add_argument('-i', '--input', type=str, help='输入目录路径（包含.md文件）')
    parser.add_argument('-o', '--output', type=str, help='输出目录路径（保存.html文件）')
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
        converter = MarkdownToHtmlConverter(input_dir, output_dir)

        # 转换单个文件
        print("=" * 80)
        print(f"Markdown转HTML工具 - 单文件模式")
        print("=" * 80)
        print(f"\n输入文件: {md_file}")
        print(f"输出目录: {output_dir}\n")

        success = converter.convert_file(md_file)

        if success:
            print("\n" + "=" * 80)
            print("[OK] 转换成功!")
            print("=" * 80)
        else:
            print("\n" + "=" * 80)
            print("[FAIL] 转换失败")
            print("=" * 80)
            sys.exit(1)

    # 否则处理整个目录
    else:
        if args.input:
            input_dir = Path(args.input)
        else:
            input_dir = script_dir / "process"

        if args.output:
            output_dir = Path(args.output)
        else:
            output_dir = input_dir  # 默认输出到输入目录

        # 检查输入目录是否存在
        if not input_dir.exists():
            print(f"[ERROR] 输入目录不存在: {input_dir}")
            sys.exit(1)

        # 创建转换器
        converter = MarkdownToHtmlConverter(input_dir, output_dir)

        # 执行转换
        converter.convert_all()


if __name__ == "__main__":
    main()
