# MorphMd - Markdown 转换工具

将 Markdown 文件转换为 HTML、PDF 或 DOCX 格式，完美支持彩色 Emoji。

📖 **[项目文档](Docs/cover.md)** | [使用指南](Docs/usage.md) | [示例](Docs/examples.md) | [更新日志](Docs/CHANGELOG.md)

<!-- COVER_START -->
# 项目文档

## 项目初衷

我在用claude开发生成项目markdown时候，很多时候需要给非技术背景的人提供pdf或者word，亦或是一个html小型的静态文档网站，市面上符合我想用的功能的比较少。就用python自己开发了一个，本来在那个项目中想着临时使用，没想到变成了一个使用频次颇高的模块，因此这里开源出来，大家一起交个朋友。我自己也会使用，不定期更新，希望能兼职维护这个项目。

## 开发环境

- **操作系统**: Windows (开发和测试环境)
- **Python**: 3.12+
- **跨平台**: 理论上支持 macOS 和 Linux，但未经充分测试

> 如果你在 macOS 或 Linux 上使用遇到问题，欢迎提 Issue 或 PR！

## 目录



- [使用指南](usage.md) - 详细的使用文档
- [示例](examples.md) - 使用示例
- [更新日志](CHANGELOG.md) - 版本说明和开发计划
<!-- COVER_END -->

## 最新更新

<!-- CHANGELOG_LATEST_START -->
## v0.2.1 (2026-04-19)

#### 新功能
- `add_cover.py` 新增 `--page-number / -p` 参数，封面后各页自动加页码
- 新增 `Tests/test_page_number.py` 页码功能测试

#### 改进
- `requirements.txt` 新增 `reportlab` 依赖
- `Docs/examples.md` 补充页码用例

---
<!-- CHANGELOG_LATEST_END -->

## 快速开始

### 1. 配置环境

```bash
# Windows
copy Config\.env.example Config\.env

# macOS / Linux
cp Config/.env.example Config/.env
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
python Bin/convert.py Samples/test.md -f pdf
# 输出: Output/pdf/Samples/test.pdf

# 批量转换文件夹
python Bin/convert.py Samples -f html
# 输出: Output/html/Samples/*.html

# 合并目录下所有 md 为一个 PDF
python Bin/merge_convert.py Samples
# 输出: Output/pdf/Samples/Samples.pdf

# 为 PDF 添加封面
python Bin/add_cover.py Template/Cover/Samples/示例封面.md Output/pdf/Samples/Samples.pdf
# 输出: Output/pdf/Samples/Samples_covered.pdf
```

## 目录结构

```
MorphMd/
├── Bin/               # 入口脚本
│   ├── convert.py     # 单文件/批量转换
│   ├── merge_convert.py # 合并多 md 为一个 PDF
│   └── add_cover.py   # 添加封面
│
├── Config/            # 配置文件
│   ├── .env           # 环境配置（本地，不提交）
│   ├── .env.example   # 配置示例
│   └── settings.json  # 全局设置
│
├── Input/             # 输入目录（放置待转换的 .md 文件）
│   ├── Tests/
│   └── Samples/
│
├── Output/            # 输出目录（按格式自动分类）
│   ├── html/
│   ├── pdf/
│   └── docx/
│
├── Template/          # 模板目录
│   └── Cover/         # 封面模板
│       └── Samples/   # 示例封面
│
├── Tests/             # 测试代码
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
# 单文件或批量转换
python Bin/convert.py <路径> -f <格式>

# 合并为一个 PDF
python Bin/merge_convert.py <目录> [--name <输出文件名>]

# 添加封面
python Bin/add_cover.py <封面md> <内容pdf>
```

## 示例

```bash
# 转换单个样例文件为 PDF
python Bin/convert.py Samples/test.md -f pdf

# 批量转换所有测试文件为 HTML
python Bin/convert.py Tests -f html

# 合并技术文档为一个 PDF
python Bin/merge_convert.py Samples

# 添加封面
python Bin/add_cover.py Template/Cover/Samples/示例封面.md Output/pdf/Samples/Samples.pdf
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
