# Markdown 文档转换工具

将 Markdown 文件转换为 **HTML**、**PDF** 或 **DOCX (Word)** 格式，完美支持彩色 Emoji。

## 目录结构

```
md_converter/
├── .env                          # 配置文件
├── README.md                     # 本文件
├── __init__.py                   # 模块入口（支持导入）
├── config.py                     # 配置加载模块
├── example_usage.py              # 使用示例脚本
├── md_to_html.py                 # Markdown → HTML
├── md_to_pdf_wkhtmltopdf.py      # Markdown → PDF (wkhtmltopdf)
├── md_to_pdf_chromium.py         # Markdown → PDF (Chromium, 彩色emoji)
└── md_to_docx.py                 # Markdown → DOCX (Word, 彩色emoji)
```

---

## 快速开始

### 1. 安装依赖

#### 基础依赖（必需）
```bash
pip install markdown2
```

#### HTML 转换（已包含在基础依赖）
无需额外安装

#### PDF 转换 - wkhtmltopdf 版本（可选）
```bash
pip install pdfkit
# 下载安装 wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
```

#### PDF 转换 - Chromium 版本（推荐，支持彩色emoji）
```bash
pip install playwright
playwright install chromium
```

#### DOCX 转换（推荐，支持彩色emoji）
```bash
pip install pypandoc
# 安装 Pandoc
# Windows: choco install pandoc
# 或下载: https://pandoc.org/installing.html
```

---

### 2. 配置文件

编辑 `.env` 文件，根据需要修改配置：

```env
# 页面大小
PDF_PAGE_SIZE=A4

# 边距（单位：mm）
PDF_MARGIN_TOP=15

# 字体
FONT_FAMILY=Segoe UI Emoji, Apple Color Emoji, ...

# 更多配置请参阅 .env 文件注释
```

---

## 使用方法

### 方式A: 作为 Python 模块导入（推荐） 🆕

**适用场景**：在其他 Python 脚本中批量处理或自动化转换

```python
# 从 tools 目录导入
import sys
sys.path.insert(0, 'path/to/tools')

from md_converter import convert, batch_convert

# 转换单个文件
convert("文件.md", format="html")    # 转换为 HTML
convert("文件.md", format="pdf")     # 转换为 PDF（彩色emoji）
convert("文件.md", format="docx")    # 转换为 DOCX (Word)

# 指定输出目录
convert("文件.md", format="pdf", output_dir="./output")

# 批量转换目录下所有文件
results = batch_convert("./docs", format="pdf")
print(f"成功: {len(results['success'])}, 失败: {len(results['failed'])}")
```

**示例脚本**：查看 `example_usage.py` 获取完整示例

**优点**：
- ✅ 简洁的 API 接口
- ✅ 统一的错误处理
- ✅ 适合集成到其他项目
- ✅ 支持批量处理

---

### 方式B: 命令行脚本

**适用场景**：手动转换单个或多个文件

#### 方式1: Markdown → HTML

```bash
# 单文件转换
python md_to_html.py -f "文件路径.md"

# 批量转换目录
python md_to_html.py -i "输入目录" -o "输出目录"
```

**特点：**
- ✅ 完美支持彩色 emoji
- ✅ 交互式导航目录
- ✅ 支持数学公式（MathJax）
- ✅ 响应式设计
- ✅ 在线查看最佳选择

---

#### 方式2: Markdown → PDF (wkhtmltopdf)

```bash
# 单文件转换
python md_to_pdf_wkhtmltopdf.py -f "文件路径.md"

# 批量转换
python md_to_pdf_wkhtmltopdf.py -i "输入目录" -o "输出目录"
```

**特点：**
- ✅ 文件小（~100KB）
- ✅ 渲染快速
- ✅ 支持简单 emoji（✅ ❌ ⚠ ⭐ ➡）
- ⚠️ 彩色 emoji 显示为黑白
- 📄 适合打印和快速生成

---

#### 方式3: Markdown → PDF (Chromium，推荐)

```bash
# 单文件转换
python md_to_pdf_chromium.py -f "文件路径.md"

# 批量转换
python md_to_pdf_chromium.py -i "输入目录" -o "输出目录"
```

**特点：**
- ✅ **完美支持彩色 emoji** 😊 🎉 🔥 💡
- ✅ 现代网页渲染
- ✅ 更好的字体渲染
- ⚠️ 文件较大（~2-3MB）
- ⚠️ 渲染稍慢
- 📄 适合正式文档、演示

---

#### 方式4: Markdown → DOCX (Word，推荐) 🆕

```bash
# 单文件转换
python md_to_docx.py -f "文件路径.md"

# 批量转换
python md_to_docx.py -i "输入目录" -o "输出目录"
```

**特点：**
- ✅ **完美支持彩色 emoji** 😊 🎉 🔥 💡
- ✅ **可编辑**的 Word 文档
- ✅ 保留所有格式（表格、代码块、列表等）
- ✅ 自动生成目录
- ✅ 文件大小适中（~50-200KB）
- 📝 适合需要二次编辑的文档

---

## 命令行参数

所有脚本支持以下参数：

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--file` | `-f` | 单个文件路径 | `-f "test.md"` |
| `--input` | `-i` | 输入目录 | `-i "../Proposal"` |
| `--output` | `-o` | 输出目录 | `-o "./output"` |

**优先级：** `-f` > `-i` > 配置文件

---

## 使用示例

### 示例1: 转换为HTML（在线查看）
```bash
python md_to_html.py -f "../Proposal/emoji测试.md"
```

### 示例2: 转换为PDF（彩色emoji，正式文档）
```bash
python md_to_pdf_chromium.py -f "../Proposal/部署实施手册v5.md"
```

### 示例3: 转换为Word（可编辑）
```bash
python md_to_docx.py -f "../Proposal/部署实施手册v5.md"
```

### 示例4: 批量转换整个目录为Word
```bash
python md_to_docx.py -i "../Proposal" -o "../Proposal"
```

---

## 格式对比

| 功能 | HTML | PDF (wkhtmltopdf) | PDF (Chromium) | **DOCX (Word)** |
|------|------|-------------------|----------------|-----------------|
| 彩色 Emoji | ✅ 完美 | ❌ 黑白 | ✅ 完美 | ✅ **完美** |
| 可编辑性 | ❌ 否 | ❌ 否 | ❌ 否 | ✅ **完全可编辑** |
| 文件大小 | 中等 | 小 (~100KB) | 大 (~2-3MB) | 中等 (~50-200KB) |
| 渲染速度 | 快 | 快 | 中等 | 快 |
| 表格支持 | ✅ 完美 | ✅ 良好 | ✅ 完美 | ✅ 完美 |
| 代码高亮 | ✅ 支持 | ⚠️ 有限 | ✅ 支持 | ✅ 支持 |
| 数学公式 | ✅ MathJax | ⚠️ 有限 | ✅ 支持 | ⚠️ 有限 |
| 目录生成 | ✅ 交互式 | ❌ 无 | ❌ 无 | ✅ **Word目录** |
| 适用场景 | 在线查看 | 打印/传阅 | 精美文档 | **编辑/审阅** |

---

## 推荐使用场景

### 📱 在线分享 → 使用 HTML
- 发送链接给同事查看
- 需要搜索和导航
- 需要交互功能

### 📄 正式文档 → 使用 PDF (Chromium)
- 公司对外文档
- 演示材料
- 需要精美排版

### 📝 协作编辑 → 使用 DOCX
- 需要多人修改
- 需要添加批注
- 需要修改格式
- **推荐用于日常工作文档**

### 🖨️ 打印输出 → 使用 PDF (wkhtmltopdf)
- 快速生成
- 文件体积小
- 不需要彩色 emoji

---

## 常见问题

### Q: 如何安装 Pandoc（用于DOCX转换）？
**A:**
```bash
# Windows (使用 Chocolatey)
choco install pandoc

# 或下载安装包
# https://github.com/jgm/pandoc/releases
```

### Q: DOCX 中的 emoji 是彩色的吗？
**A:** 是的！使用 Pandoc 转换，emoji 在 Word 中完美显示为彩色。

### Q: 我应该用哪个工具？
**A:**
- 需要**在线查看** → `md_to_html.py`
- 需要**编辑修改** → `md_to_docx.py` ⭐ 推荐
- 需要**精美PDF** → `md_to_pdf_chromium.py`
- 需要**快速打印** → `md_to_pdf_wkhtmltopdf.py`

### Q: 如何修改PDF的页边距？
**A:** 编辑 `.env` 文件中的 `PDF_MARGIN_*` 配置项。

### Q: Word文档可以修改样式吗？
**A:** 可以！生成的DOCX是标准Word格式，可以在Word中自由编辑格式、字体、颜色等。

---

## 技术栈

- **Markdown解析**: markdown2
- **PDF引擎**:
  - wkhtmltopdf (QtWebKit)
  - Playwright (Chromium)
- **DOCX转换**: pypandoc + Pandoc
- **配置管理**: 自定义 .env 解析器

---

## 许可证

内部工具，仅供项目使用。

---

## 更新日志

### v1.1.0 (2025-12-04)
- ✅ **新增 DOCX (Word) 转换支持**
- ✅ 支持可编辑的 Word 文档
- ✅ Word 中完美显示彩色 Emoji

### v1.0.0 (2025-12-04)
- ✅ 初始版本发布
- ✅ 支持 HTML 和 PDF 转换
- ✅ 完美支持彩色 Emoji
- ✅ 可配置的 .env 文件

---

**作者**: Claude
**日期**: 2025-12-04
**项目**: 一龄健康指数系统
