#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EVM链批量地址余额查询脚本
支持从文件读取地址列表，批量查询原生代币余额
"""

import sys
from EVM_native_checker.checker import EthereumBalanceChecker
from EVM_native_checker import EVMChains
from EVM_native_checker.logger import logger, Icons


def show_available_chains():
    """显示可用的链"""
    chains = EVMChains.list_available_chains()
    
    # 按类型分组显示
    mainnets = []
    testnets = []
    
    for name, info in chains.items():
        if info['is_testnet']:
            testnets.append((name, info))
        else:
            mainnets.append((name, info))
    
    logger.section("可用的链", Icons.LIST)
    
    logger.info("主网:", Icons.NETWORK)
    for i, (name, info) in enumerate(mainnets, 1):
        logger.list_item(f"{i}. {name}: {info['name']} ({info['symbol']})")
    
    if testnets:
        logger.info("测试网:", Icons.WARNING)
        for i, (name, info) in enumerate(testnets, 1):
            logger.list_item(f"{len(mainnets) + i}. {name}: {info['name']} ({info['symbol']})")
    
    return chains


def select_chain():
    """交互式选择链"""
    chains = show_available_chains()
    chain_list = list(chains.items())
    
    while True:
        try:
            choice = input(f"\n请选择链 (1-{len(chain_list)}) 或输入链名称: ").strip()
            
            # 如果输入的是数字
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(chain_list):
                    chain_name, chain_info = chain_list[index]
                    return chain_name, chain_info
                else:
                    logger.error(f"无效的选择，请输入 1-{len(chain_list)} 之间的数字")
                    continue
            
            # 如果输入的是链名称
            if choice in chains:
                return choice, chains[choice]
            else:
                logger.error(f"不支持的链: {choice}")
                logger.info(f"支持的链名称: {', '.join(chains.keys())}")
                continue
                
        except KeyboardInterrupt:
            print("\n\n⏹️ 用户中断操作")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 输入错误: {e}")


def configure_rpc():
    """交互式配置RPC节点"""
    logger.section("RPC节点配置", Icons.GEAR)
    
    # 选择配置方式
    logger.info("请选择配置方式:")
    logger.list_item("1. 使用预定义链配置")
    logger.list_item("2. 输入自定义RPC URL")
    
    while True:
        try:
            choice = input("请选择 (1-2): ").strip()
            
            if choice == "1":
                # 使用预定义链
                chain_name, chain_info = select_chain()
                chain_config = EVMChains.get_chain_by_name(chain_name)
                logger.success(f"已选择: {chain_info['name']} ({chain_info['symbol']})")
                logger.info(f"RPC URL: {chain_config.rpc_url}")
                return chain_config.rpc_url, chain_name
                
            elif choice == "2":
                # 自定义RPC URL
                rpc_url = input("请输入RPC URL: ").strip()
                if not rpc_url:
                    logger.error("RPC URL不能为空")
                    continue
                
                # 验证URL格式
                if not rpc_url.startswith(('http://', 'https://')):
                    logger.error("RPC URL必须以 http:// 或 https:// 开头")
                    continue
                
                logger.success(f"已设置自定义RPC URL: {rpc_url}")
                return rpc_url, None
                
            else:
                logger.error("无效的选择，请输入 1 或 2")
                continue
                
        except KeyboardInterrupt:
            print("\n\n⏹️ 用户中断操作")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 配置错误: {e}")


def configure_delay():
    """配置查询延迟"""
    logger.section("查询延迟配置", Icons.CLOCK)
    logger.info("延迟时间用于避免触发RPC节点的频率限制")
    logger.info("建议值: 0.1-0.5秒")
    
    while True:
        try:
            delay_input = input("请输入延迟时间(秒，默认0.2): ").strip()
            
            if not delay_input:
                return 0.2
            
            delay = float(delay_input)
            if delay < 0:
                logger.error("延迟时间不能为负数")
                continue
                
            if delay > 5:
                logger.warning("延迟时间较长，可能影响查询速度")
                confirm = input("是否继续? (y/N): ").strip().lower()
                if confirm != 'y':
                    continue
            
            return delay
            
        except ValueError:
            logger.error("请输入有效的数字")
        except KeyboardInterrupt:
            logger.error("用户中断操作")
            sys.exit(1)


def main():
    """主函数"""
    logger.header("EVM链批量地址余额查询工具", "支持多种EVM兼容链的原生代币余额查询")
    
    # 如果提供了命令行参数，使用自定义RPC URL
    if len(sys.argv) > 1:
        rpc_url = sys.argv[1]
        chain_name = None
        logger.info(f"使用命令行参数RPC URL: {rpc_url}")
    else:
        # 交互式配置RPC节点
        rpc_url, chain_name = configure_rpc()
    
    try:
        # 创建余额查询器
        checker = EthereumBalanceChecker(rpc_url, chain_name)
        
        # 配置查询延迟
        delay = configure_delay()
        
        # 输入文件路径
        logger.section("地址文件配置", Icons.FOLDER)
        input_file = input("请输入地址文件路径 (默认: addresses.txt): ").strip()
        if not input_file:
            input_file = "addresses.txt"
        
        # 加载地址列表
        addresses = checker.load_addresses_from_file(input_file)
        
        if not addresses:
            logger.error("没有找到有效的地址")
            return
        
        # 批量查询余额
        results = checker.batch_check_balances(addresses, delay=delay)
        
        # 打印摘要
        checker.print_summary(results)
        
        # 保存结果
        logger.section("结果保存配置", Icons.SAVE)
        logger.info("自动保存有余额的地址结果", Icons.MAGNIFYING_GLASS)
        
        output_file = input("请输入输出文件路径 (默认: balance_results.json): ").strip()
        if not output_file:
            output_file = "balance_results.json"
        
        # 直接保存有余额的结果
        checker.save_results(results, output_file, only_with_balance=True)
        
        logger.footer("批量查询完成！")
        
    except KeyboardInterrupt:
        logger.error("用户中断操作")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()
