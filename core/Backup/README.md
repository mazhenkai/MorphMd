# Backup 目录说明

此目录用于保存暂不使用但保留备份的代码文件。

## 文件列表

### converter_pdf_wkhtmltopdf.py
- **功能**: 使用 wkhtmltopdf 将 Markdown 转换为 PDF
- **状态**: 已弃用，保留备份
- **原因**:
  - 项目默认使用 `converter_pdf_chromium.py`（支持彩色 emoji）
  - wkhtmltopdf 基于旧的 QtWebKit，只能显示黑白 emoji
  - 渲染效果不如 Chromium 现代
- **保留原因**: 作为备选方案，某些环境可能无法安装 Chromium/Playwright
- **使用方法**: 如需使用，将文件移回 `core/` 目录，并修改 `main.py` 中的导入

## 注意事项

- 此目录下的文件不会被项目主代码调用
- 不会提交到 Git（已在 .gitignore 中配置）
- 如需恢复使用，请联系维护者
