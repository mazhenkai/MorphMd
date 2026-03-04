# MorphMd - Markdown 转换工具

将 Markdown 文件转换为 HTML、PDF 或 DOCX 格式，完美支持彩色 Emoji。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt

# 安装 Chromium (用于 PDF 转换)
playwright install chromium

# 安装 Pandoc (用于 DOCX 转换)
# Windows: choco install pandoc
# 或访问: https://pandoc.org/installing.html
```

### 2. 使用方法

```bash
# 转换单个文件到 Tmp 目录（调试）
python main.py -i test.md -o Tmp -f pdf

# 批量转换 Input 目录所有文件
python main.py -i Input -o Output/pdf -f pdf

# 使用默认配置（Input -> Output）
python main.py -f html
```

## 目录说明

- `Input/` - 放置待转换的 .md 文件
- `Output/` - 转换结果（按格式分类）
- `Tmp/` - 临时文件和调试输出
- `Logs/` - 转换日志
- `Docs/` - 项目文档
- `Tests/` - 测试用例
- `core/` - 核心转换代码

## 支持格式

- **HTML** - 在线查看，交互式导航
- **PDF** - 正式文档，完美支持彩色 emoji
- **DOCX** - Word 文档，可编辑

更多详情请查看 `Docs/usage.md`
