#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

from web3 import Web3
import json
from typing import Dict, List
from .chains import EVMChains, detect_chain_from_rpc
from .logger import logger, Icons


def quick_check_balance(address: str, rpc_url: str = "https://mainnet.infura.io/v3/YOUR-PROJECT-ID") -> Dict:
    """
    快速查询单个地址的原生代币余额
    
    Args:
        address: EVM地址
        rpc_url: RPC节点URL
    
    Returns:
        dict: 余额信息
    """
    try:
        # 连接到EVM网络
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            return {"error": "无法连接到EVM网络"}
        
        # 验证地址格式
        if not w3.is_address(address):
            return {"error": "无效的EVM地址格式"}
        
        # 标准化地址
        normalized_address = w3.to_checksum_address(address)
        
        # 获取余额
        balance_wei = w3.eth.get_balance(normalized_address)
        balance_native = w3.from_wei(balance_wei, 'ether')
        
        # 检测链类型
        chain_config = detect_chain_from_rpc(rpc_url)
        symbol = chain_config.symbol if chain_config else "ETH"
        
        return {
            "address": normalized_address,
            "balance_wei": str(balance_wei),
            "balance_native": float(balance_native),
            "symbol": symbol,
            "status": "success"
        }
        
    except Exception as e:
        return {"error": str(e)}


def validate_ethereum_address(address: str) -> bool:
    """
    验证EVM地址格式
    
    Args:
        address: 要验证的地址
        
    Returns:
        bool: 地址是否有效
    """
    try:
        w3 = Web3()
        return w3.is_address(address)
    except:
        return False


def format_balance(balance_wei: int, decimals: int = 6) -> str:
    """
    格式化余额显示
    
    Args:
        balance_wei: 以wei为单位的余额
        decimals: 小数位数
        
    Returns:
        str: 格式化后的余额字符串
    """
    try:
        w3 = Web3()
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return f"{float(balance_eth):.{decimals}f}"
    except:
        return "0.000000"


def load_addresses_from_text(text: str) -> List[str]:
    """
    从文本中提取EVM地址
    
    Args:
        text: 包含地址的文本
        
    Returns:
        List[str]: 地址列表
    """
    addresses = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            # 简单的地址提取逻辑
            if line.startswith('0x') and len(line) == 42:
                addresses.append(line)
    
    return addresses


def export_results_to_csv(results: List[Dict], output_file: str, only_with_balance: bool = True):
    """
    将结果导出为CSV格式
    
    Args:
        results: 查询结果列表
        output_file: 输出文件路径
        only_with_balance: 是否只导出有余额的结果
    """
    import csv
    
    try:
        # 根据only_with_balance参数过滤结果
        if only_with_balance:
            filtered_results = [
                result for result in results 
                if result['status'] == 'success' and result['balance_native'] > 0
            ]
            logger.info(f"过滤后保留 {len(filtered_results)} 个有余额的地址（共 {len(results)} 个）")
        else:
            filtered_results = results
            logger.info(f"保存所有 {len(results)} 个查询结果")
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # 写入表头
            writer.writerow(['地址', '余额(原生代币)', '余额(Wei)', '代币符号', '状态', '错误信息'])
            
            # 写入数据
            for result in filtered_results:
                writer.writerow([
                    result.get('address', ''),
                    result.get('balance_native', 0),
                    result.get('balance_wei', 0),
                    result.get('symbol', 'ETH'),
                    result.get('status', ''),
                    result.get('error', '')
                ])
        
        logger.success(f"CSV结果已保存到: {output_file}", Icons.SAVE)
        
    except Exception as e:
        logger.error(f"保存CSV失败: {e}")
