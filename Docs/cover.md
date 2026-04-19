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
## v0.2.0 (2026-04-19)

#### 新功能
- 入口拆分为 `Bin/convert.py`、`Bin/merge_convert.py`、`Bin/add_cover.py`
- 新增多 md 合并为单 PDF 功能（含目录页）
- 新增封面模板系统（md 模板 + json 数据，`{{占位符}}` 渲染）
- 新增 `Config/settings.json` 全局配置
- `.env` 迁移至 `Config/` 目录

#### 改进
- 所有入口支持从任意目录运行（基于 ROOT 路径定位）
- `gitignore` 新增 `SelfRunningFiles/` 全局忽略
- 新增 `Template/Cover/Samples/` 封面示例

---
<!-- CHANGELOG_LATEST_END -->

- [使用指南](usage.md) - 详细的使用文档
- [示例](examples.md) - 使用示例
- [更新日志](CHANGELOG.md) - 版本说明和开发计划
