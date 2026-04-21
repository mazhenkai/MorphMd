# 项目文档

## 项目初衷

我在用claude开发生成项目markdown时候，很多时候需要给非技术背景的人提供pdf或者word，亦或是一个html小型的静态文档网站，市面上符合我想用的功能的比较少。就用python自己开发了一个，本来在那个项目中想着临时使用，没想到变成了一个使用频次颇高的模块，因此这里开源出来，大家一起交个朋友。我自己也会使用，不定期更新，希望能兼职维护这个项目。

## 开发环境

- **操作系统**: Windows (开发和测试环境)
- **Python**: 3.12+
- **跨平台**: 理论上支持 macOS 和 Linux，但未经充分测试

> 如果你在 macOS 或 Linux 上使用遇到问题，欢迎提 Issue 或 PR！

## 目录

<!-- CHANGELOG_LATEST_START -->
## v0.2.2 (2026-04-21)

#### 新功能
- 新增 `Bin/add_toc_pages.py`：独立步骤，为合并 PDF 重建带页码目录并加底部页码
- 新增 `Bin/clean_metadata.py`：清除 MorphMd 生成的内部元数据
- 新增 `core/pdf_utils.py`：抽离通用 PDF 工具函数（merge_pdfs、add_page_numbers、find_section_pages）
- `add_cover.py` 新增 `--mode` 参数（`overwrite` 覆盖 / `timestamp` 带时间戳新文件，默认 timestamp）
- `add_cover.py` 封面 `{{最后更新}}` 自动取系统时间，无需手动维护 json

#### 改进
- `convert_merged` 改为逐 section 单独渲染，精确记录页码存入 PDF 元数据，目录页码准确
- 修复 `pre` 块 CSS：`overflow-x:auto` 改为 `white-space:pre-wrap` + `word-break:break-all`，修复 PDF 长代码行不换行问题
- `add_cover.py` 重构，复用 `core/pdf_utils`，去除重复代码

#### 测试
- 新增 `Tests/test_code_wrap.py`：验证长代码行换行修复
- 新增 `Tests/test_pipeline.py`：完整四步流程集成测试
- 新增 `Tests/pipline/` 测试 fixtures

---
<!-- CHANGELOG_LATEST_END -->

- [使用指南](usage.md) - 详细的使用文档
- [示例](examples.md) - 使用示例
- [更新日志](CHANGELOG.md) - 版本说明和开发计划
