#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志美化模块
提供优雅、醒目、易读的输出格式
"""

import sys
import time
from typing import Optional, List, Dict, Any
from enum import Enum


class Color(Enum):
    """颜色枚举"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # 前景色
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # 亮色
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


class Icons:
    """图标常量"""
    # 状态图标
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    
    # 功能图标
    ROCKET = "🚀"
    GEAR = "🔧"
    MAGNIFYING_GLASS = "🔍"
    FOLDER = "📁"
    SAVE = "💾"
    NETWORK = "🌐"
    CHAIN = "⛓️"
    COIN = "💰"
    CHART = "📊"
    CLOCK = "⏱️"
    LIST = "📋"
    SEARCH = "🔎"
    DONE = "🎉"
    WORKING = "🔄"


class Logger:
    """美化日志输出器"""
    
    def __init__(self, enable_colors: bool = True):
        self.enable_colors = enable_colors and self._supports_color()
        self.start_time = time.time()
    
    def _supports_color(self) -> bool:
        """检查终端是否支持颜色"""
        return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    
    def _colorize(self, text: str, color: Color, bold: bool = False) -> str:
        """为文本添加颜色"""
        if not self.enable_colors:
            return text
        
        result = color.value
        if bold:
            result += Color.BOLD.value
        result += text + Color.RESET.value
        return result
    
    def header(self, title: str, subtitle: Optional[str] = None):
        """打印标题"""
        print()
        print(self._colorize("=" * 60, Color.BRIGHT_CYAN, bold=True))
        print(self._colorize(f"  {Icons.ROCKET} {title}", Color.BRIGHT_WHITE, bold=True))
        if subtitle:
            print(self._colorize(f"  {subtitle}", Color.CYAN))
        print(self._colorize("=" * 60, Color.BRIGHT_CYAN, bold=True))
        print()
    
    def section(self, title: str, icon: str = Icons.GEAR):
        """打印章节标题"""
        print()
        print(self._colorize(f"{icon} {title}", Color.BRIGHT_BLUE, bold=True))
        print(self._colorize("-" * 40, Color.BLUE))
    
    def success(self, message: str, icon: str = Icons.SUCCESS):
        """成功消息"""
        print(self._colorize(f"{icon} {message}", Color.BRIGHT_GREEN))
    
    def error(self, message: str, icon: str = Icons.ERROR):
        """错误消息"""
        print(self._colorize(f"{icon} {message}", Color.BRIGHT_RED))
    
    def warning(self, message: str, icon: str = Icons.WARNING):
        """警告消息"""
        print(self._colorize(f"{icon} {message}", Color.BRIGHT_YELLOW))
    
    def info(self, message: str, icon: str = Icons.INFO):
        """信息消息"""
        print(self._colorize(f"{icon} {message}", Color.BRIGHT_CYAN))
    
    def progress(self, current: int, total: int, message: str = "", width: int = 30):
        """进度条"""
        percentage = current / total if total > 0 else 0
        filled = int(width * percentage)
        bar = "█" * filled + "░" * (width - filled)
        
        progress_text = f"[{bar}] {current}/{total} ({percentage:.1%})"
        if message:
            progress_text += f" - {message}"
        
        print(f"\r{self._colorize(progress_text, Color.BRIGHT_GREEN)}", end="", flush=True)
        if current == total:
            print()
    
    def key_value(self, key: str, value: Any, icon: str = ""):
        """键值对显示"""
        if icon:
            key = f"{icon} {key}"
        print(f"  {self._colorize(key, Color.BRIGHT_WHITE)}: {value}")
    
    def list_item(self, item: str, icon: str = "•"):
        """列表项显示"""
        print(f"  {self._colorize(icon, Color.BRIGHT_CYAN)} {item}")
    
    def summary(self, title: str, data: Dict[str, Any]):
        """摘要显示"""
        print()
        print(self._colorize(f"{Icons.CHART} {title}", Color.BRIGHT_MAGENTA, bold=True))
        print(self._colorize("=" * 50, Color.MAGENTA))
        
        for key, value in data.items():
            if isinstance(value, (int, float)) and value > 0:
                color = Color.BRIGHT_GREEN
            elif isinstance(value, str) and "错误" in value:
                color = Color.BRIGHT_RED
            else:
                color = Color.WHITE
            
            print(f"  {self._colorize(key, Color.BRIGHT_WHITE)}: {self._colorize(str(value), color)}")
        
        print(self._colorize("=" * 50, Color.MAGENTA))
    
    def footer(self, message: str = "操作完成"):
        """页脚"""
        print()
        print(self._colorize("=" * 60, Color.BRIGHT_CYAN, bold=True))
        print(self._colorize(f"  {Icons.DONE} {message}", Color.BRIGHT_GREEN, bold=True))
        print(self._colorize("=" * 60, Color.BRIGHT_CYAN, bold=True))
        print()


# 全局日志器实例
logger = Logger()
