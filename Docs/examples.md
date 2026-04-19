# 使用示例

## 命令行模式

### 1. 转换单个文件

```bash
# 转换为 PDF（默认格式）
python Bin/convert.py Samples/test.md -f pdf

# 转换为 HTML
python Bin/convert.py Samples/test.md -f html

# 转换为 DOCX
python Bin/convert.py Samples/test.md -f docx
```

### 2. 批量转换目录

```bash
# 批量转换 Input/Samples 目录所有 .md 文件为 PDF
python Bin/convert.py Samples -f pdf

# 批量转换为 HTML
python Bin/convert.py Samples -f html
```

### 3. 合并为一个 PDF

```bash
# 合并目录下所有 md 为一个 PDF（文件名默认用目录名）
python Bin/merge_convert.py Samples

# 自定义输出文件名
python Bin/merge_convert.py Samples --name 技术文档合集
```

### 4. 添加封面

```bash
# 为 PDF 添加封面，输出为 *_covered.pdf
python Bin/add_cover.py Template/Cover/Samples/示例封面.md Output/pdf/Samples/Samples.pdf
```

## 配置文件

编辑 `.env` 文件自定义配置：

```env
# 默认目录
INPUT_DIR=Input
OUTPUT_DIR=Output

# PDF 配置
PDF_PAGE_SIZE=A4
PDF_MARGIN_TOP=15
```
