# 使用示例

## 命令行模式

### 1. 转换单个文件

```bash
# 转换为 PDF（默认格式）
python main.py -i Input/test.md -o Output/pdf

# 转换为 HTML
python main.py -i Input/test.md -o Output/html -f html

# 转换为 DOCX
python main.py -i Input/test.md -o Output/docx -f docx
```

### 2. 批量转换目录

```bash
# 批量转换 Input 目录所有 .md 文件为 PDF
python main.py -i Input -o Output/pdf -f pdf

# 批量转换为 HTML
python main.py -i Input -o Output/html -f html
```

### 3. 快速调试（使用 Tmp 目录）

```bash
# 单文件快速测试
python main.py -i test.md -o Tmp -f pdf

# 查看结果
ls Tmp/
```

## 作为 Python 模块使用

```python
from core import convert, batch_convert

# 转换单个文件
convert("Input/test.md", format="pdf", output_dir="Output/pdf")

# 批量转换
results = batch_convert("Input", format="html", output_dir="Output/html")
print(f"成功: {len(results['success'])}, 失败: {len(results['failed'])}")
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
