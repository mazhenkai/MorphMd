#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置加载模块
从 .env 文件加载配置
"""

import os
from pathlib import Path


class Config:
    """配置类"""

    def __init__(self, env_file=None):
        """
        初始化配置

        Args:
            env_file: .env文件路径，默认为当前目录下的.env
        """
        if env_file is None:
            # .env 在项目根目录
            env_file = Path(__file__).parent.parent / 'Config' / '.env'

        self.env_file = Path(env_file)
        self._config = {}
        self._load_env()

    def _load_env(self):
        """加载.env文件"""
        if not self.env_file.exists():
            print(f"[WARNING] 配置文件不存在: {self.env_file}")
            print(f"[WARNING] 将使用默认配置")
            return

        with open(self.env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # 跳过注释和空行
                if not line or line.startswith('#'):
                    continue

                # 解析配置项
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # 移除值两端的引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    self._config[key] = value

    def get(self, key, default=None):
        """
        获取配置项

        Args:
            key: 配置项键名
            default: 默认值

        Returns:
            配置项值
        """
        return self._config.get(key, default)

    def get_bool(self, key, default=False):
        """
        获取布尔型配置项

        Args:
            key: 配置项键名
            default: 默认值

        Returns:
            布尔值
        """
        value = self.get(key, str(default))
        return value.lower() in ('true', 'yes', '1', 'on')

    def get_int(self, key, default=0):
        """
        获取整型配置项

        Args:
            key: 配置项键名
            default: 默认值

        Returns:
            整数值
        """
        value = self.get(key, str(default))
        try:
            return int(value)
        except ValueError:
            return default

    def get_float(self, key, default=0.0):
        """
        获取浮点型配置项

        Args:
            key: 配置项键名
            default: 默认值

        Returns:
            浮点数值
        """
        value = self.get(key, str(default))
        try:
            return float(value)
        except ValueError:
            return default

    def get_list(self, key, default=None, separator=','):
        """
        获取列表型配置项

        Args:
            key: 配置项键名
            default: 默认值（列表）
            separator: 分隔符

        Returns:
            列表
        """
        if default is None:
            default = []

        value = self.get(key, '')
        if not value:
            return default

        return [item.strip() for item in value.split(separator) if item.strip()]


# 创建全局配置实例
config = Config()


if __name__ == '__main__':
    # 测试配置加载
    print("配置文件路径:", config.env_file)
    print("\n所有配置项:")
    for key, value in config._config.items():
        print(f"  {key} = {value}")

    print("\n示例配置读取:")
    print(f"  PDF_PAGE_SIZE = {config.get('PDF_PAGE_SIZE', 'A4')}")
    print(f"  PDF_ENABLE_JAVASCRIPT = {config.get_bool('PDF_ENABLE_JAVASCRIPT', True)}")
    print(f"  PDF_MARGIN_TOP = {config.get_int('PDF_MARGIN_TOP', 15)}")
    print(f"  MARKDOWN_EXTRAS = {config.get_list('MARKDOWN_EXTRAS')}")
