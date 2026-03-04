# MorphMd - Markdown 转换工具

将 Markdown 文件转换为 HTML、PDF 或 DOCX 格式，完美支持彩色 Emoji。

📖 **[项目文档](Docs/README.md)** | [使用指南](Docs/usage.md) | [示例](Docs/examples.md) | [更新日志](Docs/CHANGELOG.md)

## 快速开始

### 1. 配置环境

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env

# 根据需要修改 .env 中的配置
```

### 2. 安装依赖

```bash
pip install -r requirements.txt

# 安装 Chromium (用于 PDF 转换)
playwright install chromium

# 安装 Pandoc (用于 DOCX 转换)
# Windows: choco install pandoc
# 或访问: https://pandoc.org/installing.html
```

### 3. 使用方法

**所有待转换文件必须放在 `Input/` 目录下**

```bash
# 转换单个文件
python main.py Samples/test.md -f pdf
# 输出: Output/pdf/Samples/test.pdf

# 批量转换文件夹
python main.py Samples -f html
# 输出: Output/html/Samples/*.html

# 转换为 DOCX
python main.py Tests/sample.md -f docx
# 输出: Output/docx/Tests/sample.docx
```

## 目录结构

```
MorphMd/
├── Input/              # 输入目录（放置待转换的 .md 文件）
│   ├── Tests/         # 测试文件
│   └── Samples/       # 样例文件
│
├── Output/            # 输出目录（按格式自动分类）
│   ├── html/
│   │   ├── Tests/
│   │   └── Samples/
│   ├── pdf/
│   │   ├── Tests/
│   │   └── Samples/
│   └── docx/
│       ├── Tests/
│       └── Samples/
│
├── Tmp/               # 临时文件
├── Logs/              # 转换日志
├── Docs/              # 项目文档
└── core/              # 核心转换代码
```

## 支持格式

- **HTML** - 在线查看，交互式导航
- **PDF** - 正式文档，完美支持彩色 emoji (Chromium)
- **DOCX** - Word 文档，可编辑

## 命令参数

```bash
python main.py <路径> -f <格式>
```

- `<路径>`: Input 目录下的文件或文件夹（相对路径）
- `-f, --format`: 输出格式，可选 `html`, `pdf`, `docx`（默认: pdf）

## 示例

```bash
# 转换单个样例文件为 PDF
python main.py Samples/test.md -f pdf

# 批量转换所有测试文件为 HTML
python main.py Tests -f html

# 转换为 Word 文档
python main.py Samples/test.md -f docx
```

## 联系方式

如果这个项目对你有帮助，欢迎：

- 📧 **邮箱**: ma.zhenkai@foxmail.com
- 💬 **微信**: 扫码加好友交流，报bug或者纯交个朋友都行，加好友麻烦备注MorphMd

<img src="assets/微信二维码.jpg" width="200" alt="微信二维码">

- ☕ **赞赏支持**:
- 💬 哈哈，无最低和最高限额，也不强制，纯图一乐

<img src="assets/支付宝收款码.jpg" width="200" alt="支付宝收款码">

## License

MIT License - 详见 [LICENSE](LICENSE)
