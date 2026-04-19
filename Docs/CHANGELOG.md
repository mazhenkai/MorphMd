# 更新日志

## v0.2.1 (2026-04-19)

#### 新功能
- `add_cover.py` 新增 `--page-number / -p` 参数，封面后各页自动加页码
- 新增 `Tests/test_page_number.py` 页码功能测试

#### 改进
- `requirements.txt` 新增 `reportlab` 依赖
- `Docs/examples.md` 补充页码用例

---

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

## v0.1.0 (2026-03-04)

**首次发布**

#### 核心功能
- Markdown 转 HTML（完美支持彩色 emoji）
- Markdown 转 PDF（Chromium 引擎，彩色 emoji）
- Markdown 转 DOCX（Word 文档，可编辑）

#### 特性
- 命令行工具（`main.py`）
- 批量转换支持
- 自动保持目录结构
- 可配置的 .env 文件
- 日志记录功能

#### 技术栈
- Python 3.12+
- markdown2、playwright、pypandoc

---

## 开发计划

### TODO

#### 高优先级
- [ ] 添加进度条显示
- [ ] 支持自定义 CSS 样式
- [ ] 添加更多测试用例

#### 中优先级
- [ ] 支持批量转换时的并发处理
- [ ] 添加转换失败重试机制
- [ ] 支持更多 Markdown 扩展语法

#### 低优先级
- [ ] GUI 图形界面
- [ ] Web 服务模式
- [ ] Docker 支持

---

## 已知问题

暂无

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

如有问题或建议，请联系主页微信或者邮箱：ma.zhenkai@foxmail.com
