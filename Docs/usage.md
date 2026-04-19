# 使用指南

## 安装依赖

```bash
# 基础依赖
pip install -r requirements.txt

# PDF 转换（Chromium）
playwright install chromium

# DOCX 转换（Pandoc）
# Windows: choco install pandoc
# macOS: brew install pandoc
# Linux: apt install pandoc
```

## 基本使用

### 转换单个文件

```bash
# 转换为 PDF
python Bin/convert.py Samples/test.md -f pdf

# 转换为 HTML
python Bin/convert.py Samples/test.md -f html

# 转换为 DOCX
python Bin/convert.py Samples/test.md -f docx
```

### 批量转换

```bash
# 批量转换文件夹下所有 .md 文件
python Bin/convert.py Samples -f pdf
```

### 合并为一个 PDF

```bash
# 合并目录下所有 md 为一个 PDF
python Bin/merge_convert.py Samples

# 自定义输出文件名
python Bin/merge_convert.py Samples --name 合并文档
```

### 添加封面

```bash
# 为 PDF 添加封面（输出为 *_covered.pdf）
python Bin/add_cover.py Template/Cover/Samples/示例封面.md Output/pdf/Samples/Samples.pdf
```

## 输出说明

- 输入文件：`Input/Samples/test.md`
- 输出文件：`Output/pdf/Samples/test.pdf`

输出目录会自动保持与输入相同的子目录结构。

## 支持格式

| 格式 | 特点 | 适用场景 |
|------|------|----------|
| **HTML** | 交互式导航，完美支持 emoji | 在线查看、分享 |
| **PDF** | 彩色 emoji，精美排版 | 正式文档、演示 |
| **DOCX** | 可编辑，彩色 emoji | 协作编辑、审阅 |

## 配置文件

编辑 `.env` 文件自定义配置：

```env
# PDF 页面大小
PDF_PAGE_SIZE=A4

# PDF 边距（单位：mm）
PDF_MARGIN_TOP=15
PDF_MARGIN_RIGHT=15
PDF_MARGIN_BOTTOM=15
PDF_MARGIN_LEFT=15
```

更多配置请参考 `.env.example`
