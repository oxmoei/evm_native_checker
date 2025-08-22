#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令行界面模块
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .checker import EthereumBalanceChecker
from .utils import quick_check_balance, export_results_to_csv
from .chains import EVMChains
from .logger import logger, Icons


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="EVM链批量地址余额查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s --file addresses.txt
  %(prog)s --address 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
  %(prog)s --file addresses.txt --chain ethereum
  %(prog)s --file addresses.txt --chain bsc --rpc https://bsc-dataseed1.binance.org
  %(prog)s --file addresses.txt --output results.json --format json
  %(prog)s --file addresses.txt --all-results --output all_results.json
  %(prog)s --list-chains
        """
    )
    
    # 输入选项
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file', '-f',
        type=str,
        help='包含以太坊地址的文件路径'
    )
    input_group.add_argument(
        '--address', '-a',
        type=str,
        help='单个以太坊地址'
    )
    
    # 输出选项
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='balance_results.json',
        help='输出文件路径 (默认: balance_results.json)'
    )
    
    parser.add_argument(
        '--format', '-fmt',
        choices=['json', 'csv'],
        default='json',
        help='输出格式 (默认: json)'
    )
    
    parser.add_argument(
        '--all-results', '-a',
        action='store_true',
        help='保存所有查询结果（默认只保存有余额的地址）'
    )
    
    # 网络选项
    parser.add_argument(
        '--chain', '-c',
        type=str,
        help='链名称 (ethereum, bsc, polygon, arbitrum, optimism, avalanche, fantom, base, linea)'
    )
    
    parser.add_argument(
        '--rpc', '-r',
        type=str,
        help='自定义RPC节点URL (如果不指定chain参数)'
    )
    
    # 性能选项
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=0.2,
        help='请求间隔时间(秒) (默认: 0.2)'
    )
    
    # 其他选项
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出'
    )
    
    parser.add_argument(
        '--list-chains',
        action='store_true',
        help='列出所有支持的链'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    logger.header("EVM链批量地址余额查询工具", "支持多种EVM兼容链的原生代币余额查询")
    
    # 列出支持的链
    if args.list_chains:
        logger.section("支持的链", Icons.LIST)
        chains = EVMChains.list_available_chains()
        for name, info in chains.items():
            logger.key_value(f"{name}: {info['name']} ({info['symbol']})", f"Chain ID: {info['chain_id']}")
        return
    
    try:
        # 确定RPC URL
        rpc_url = None
        if args.chain:
            chain_config = EVMChains.get_chain_by_name(args.chain)
            if not chain_config:
                logger.error(f"不支持的链: {args.chain}")
                logger.info("使用 --list-chains 查看支持的链")
                return
            rpc_url = chain_config.rpc_url
        elif args.rpc:
            rpc_url = args.rpc
        else:
            # 默认使用以太坊
            rpc_url = EVMChains.get_chain_by_name("ethereum").rpc_url
        
        # 创建余额查询器
        checker = EthereumBalanceChecker(rpc_url, args.chain)
        
        if args.address:
            # 查询单个地址
            logger.section("查询单个地址", Icons.MAGNIFYING_GLASS)
            logger.info(f"地址: {args.address}")
            result = quick_check_balance(args.address, args.rpc)
            
            if "error" in result:
                logger.error(f"错误: {result['error']}")
                sys.exit(1)
            else:
                logger.success(f"地址: {result['address']}")
                logger.key_value("余额", f"{result['balance_native']:.6f} {result['symbol']}", Icons.COIN)
                logger.key_value("Wei", result['balance_wei'])
                
                # 保存结果
                results = [result]
                if args.format == 'json':
                    checker.save_results(results, args.output)
                elif args.format == 'csv':
                    export_results_to_csv(results, args.output.replace('.json', '.csv'))
        
        elif args.file:
            # 批量查询
            logger.section("批量查询", Icons.FOLDER)
            logger.info(f"从文件加载地址: {args.file}")
            addresses = checker.load_addresses_from_file(args.file)
            
            if not addresses:
                logger.error("没有找到有效的地址")
                sys.exit(1)
            
            # 批量查询余额
            results = checker.batch_check_balances(addresses, delay=args.delay)
            
            # 打印摘要
            checker.print_summary(results)
            
            # 保存结果
            only_with_balance = not args.all_results  # 默认只保存有余额的地址
            if args.format == 'json':
                checker.save_results(results, args.output, only_with_balance)
            elif args.format == 'csv':
                csv_output = args.output.replace('.json', '.csv')
                export_results_to_csv(results, csv_output, only_with_balance)
        
        logger.footer("查询完成！")
        
    except KeyboardInterrupt:
        logger.error("用户中断操作")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
