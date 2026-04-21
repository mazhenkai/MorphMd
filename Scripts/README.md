# Scripts 目录说明

本目录存放组合 `Bin/` 下各工具的批处理脚本，用于自动化执行多步骤流程。

## 目录结构

```
Scripts/
  SelfRunningFiles/
    run_pipeline.py   # 一龄主动健康文档批量生成脚本
```

## 使用方式

```bash
python Scripts/SelfRunningFiles/run_pipeline.py
```

## 完整流程说明

每个脚本依次调用以下四个步骤：

| 步骤 | 脚本 | 说明 |
|------|------|------|
| 1 | `Bin/merge_convert.py` | 合并 md → PDF（含元数据） |
| 2 | `Bin/add_toc_pages.py` | 重建带页码目录 + 底部页码 |
| 3 | `Bin/add_cover.py` | 添加封面 |
| 4 | `Bin/clean_metadata.py` | 清除内部元数据 |

## 新增脚本

在脚本文件的 `JOBS` 配置区添加新条目即可：

```python
JOBS = [
    {
        "input":  "SelfRunningFiles/项目名/文档目录",
        "name":   "输出文件名",
        "cover":  "Template/Cover/封面.md",
    },
]
```
