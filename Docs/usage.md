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

### 批量转换

```bash
# 批量转换 Input/Samples 目录所有 .md 文件为 PDF
python Bin/convert.py Samples -f pdf

# 批量转换为 HTML
python Bin/convert.py Samples -f html
```

### 合并为一个 PDF（完整流程）

```bash
# 第一步：合并 md → PDF（含元数据）
python Bin/merge_convert.py SelfRunningFiles/项目名/文档目录 --name 输出文件名

# 第二步：重建带页码目录 + 底部页码
python Bin/add_toc_pages.py Output/pdf/SelfRunningFiles/项目名/文档目录/输出文件名.pdf

# 第三步：加封面（默认输出带时间戳新文件）
python Bin/add_cover.py Template/Cover/封面.md Output/pdf/.../输出文件名.pdf

# 第四步：清除内部元数据
python Bin/clean_metadata.py Output/pdf/.../输出文件名.pdf
```

**add_cover.py 参数说明：**
- `--mode overwrite`：覆盖原文件
- `--mode timestamp`（默认）：输出带 `_YYYYMMDD_HHmm` 后缀的新文件
- `-p`：加底部页码（跳过封面页）

**add_toc_pages.py 参数说明：**
- `--toc-pages N`：目录页占几页（默认1）
- `--skip-page-number`：不加底部页码

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

## 测试

```bash
# 运行全部测试（11个）
python Tests/run_all.py
```

| 测试文件 | 覆盖内容 |
|----------|----------|
| `test_html.py` | HTML 转换 |
| `test_pdf.py` | PDF 单文件转换 |
| `test_pdf_merge.py` | PDF 合并 |
| `test_add_cover.py` | 封面添加 |
| `test_page_number.py` | 底部页码 |
| `test_code_wrap.py` | 长代码行换行修复 |
| `test_pipeline.py` | 完整四步流程集成测试 |

