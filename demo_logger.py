#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志美化演示脚本
展示优化后的输出效果
"""

from EVM_native_checker.logger import logger, Icons
from EVM_native_checker import EVMChains
import time


def demo_basic_output():
    """演示基本输出"""
    logger.header("日志美化演示", "展示优化后的输出效果")
    
    logger.section("基本消息类型", Icons.INFO)
    logger.success("这是一个成功消息")
    logger.error("这是一个错误消息")
    logger.warning("这是一个警告消息")
    logger.info("这是一个信息消息")


def demo_progress_bar():
    """演示进度条"""
    logger.section("进度条演示", Icons.WORKING)
    
    total = 10
    for i in range(1, total + 1):
        logger.progress(i, total, f"处理第 {i} 个任务")
        time.sleep(0.2)
    
    logger.success("进度条演示完成")


def demo_summary():
    """演示摘要显示"""
    logger.section("摘要显示演示", Icons.CHART)
    
    summary_data = {
        "总地址数": 100,
        "查询成功": 95,
        "无效地址": 3,
        "查询错误": 2,
        "总ETH余额": "1234.567890 ETH"
    }
    
    logger.summary("查询结果摘要", summary_data)


def demo_chain_list():
    """演示链列表显示"""
    logger.section("链列表演示", Icons.LIST)
    
    chains = EVMChains.list_available_chains()
    
    logger.info("主网:", Icons.NETWORK)
    for name, info in list(chains.items())[:3]:
        if not info['is_testnet']:
            logger.list_item(f"{name}: {info['name']} ({info['symbol']})")
    
    logger.info("测试网:", Icons.WARNING)
    for name, info in list(chains.items())[:2]:
        if info['is_testnet']:
            logger.list_item(f"{name}: {info['name']} ({info['symbol']})")


def demo_key_value():
    """演示键值对显示"""
    logger.section("键值对显示演示", Icons.GEAR)
    
    logger.key_value("项目名称", "EVM链批量地址余额查询工具", Icons.ROCKET)
    logger.key_value("版本", "0.1.0", Icons.INFO)
    logger.key_value("作者", "ylx", Icons.INFO)
    logger.key_value("支持链数", "10", Icons.CHAIN)
    logger.key_value("状态", "开发中", Icons.WORKING)


def demo_error_handling():
    """演示错误处理"""
    logger.section("错误处理演示", Icons.ERROR)
    
    try:
        # 模拟一个错误
        raise ValueError("这是一个模拟的错误")
    except Exception as e:
        logger.error(f"捕获到错误: {e}")
    
    logger.warning("这是一个警告信息")
    logger.info("程序继续执行")


def main():
    """主函数"""
    try:
        # 演示各种输出效果
        demo_basic_output()
        demo_progress_bar()
        demo_summary()
        demo_chain_list()
        demo_key_value()
        demo_error_handling()
        
        logger.footer("所有演示完成！")
        
    except Exception as e:
        logger.error(f"演示过程中出错: {e}")


if __name__ == "__main__":
    main()
