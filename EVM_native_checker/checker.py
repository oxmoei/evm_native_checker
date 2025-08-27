#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
以太坊余额查询器核心模块
"""

import json
import time
import sys
from pathlib import Path
from typing import List, Dict, Optional
from web3 import Web3
from web3.exceptions import Web3Exception
from .chains import EVMChains, ChainConfig, detect_chain_from_rpc
from .logger import logger, Icons


class EthereumBalanceChecker:
    """EVM链余额查询器"""
    
    def __init__(self, rpc_url: str = "https://withered-patient-glade.hemi-mainnet.quiknode.pro/0155507fe08fe4d1e2457a85f65b4bc7e6ed522f", chain_name: Optional[str] = None):
        """
        初始化余额查询器
        
        Args:
            rpc_url: EVM链RPC节点URL
            chain_name: 链名称，如果提供则使用预定义配置
        """
        self.rpc_url = rpc_url
        self.chain_config = None
        self.w3 = None
        
        # 如果提供了链名称，使用预定义配置
        if chain_name:
            self.chain_config = EVMChains.get_chain_by_name(chain_name)
            if self.chain_config:
                self.rpc_url = self.chain_config.rpc_url
        
        # 自动检测链类型
        if not self.chain_config:
            self.chain_config = detect_chain_from_rpc(self.rpc_url)
        
        self._connect()
    
    def _connect(self):
        """连接到EVM网络"""
        try:
            self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
            if not self.w3.is_connected():
                raise Exception("无法连接到EVM网络")
            
            # 显示连接信息
            if self.chain_config:
                logger.success(f"成功连接到 {self.chain_config.name} ({self.chain_config.symbol})")
                logger.info(f"RPC URL: {self.rpc_url}")
            else:
                logger.success("成功连接到EVM网络")
                logger.info(f"RPC URL: {self.rpc_url}")
                
        except Exception as e:
            logger.error(f"连接失败: {e}")
            sys.exit(1)
    
    def is_valid_address(self, address: str) -> bool:
        """验证以太坊地址是否有效"""
        try:
            return self.w3.is_address(address)
        except:
            return False
    
    def get_balance(self, address: str) -> Dict:
        """获取单个地址的原生代币余额"""
        try:
            normalized_address = self.w3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(normalized_address)
            balance_native = self.w3.from_wei(balance_wei, 'ether')
            
            # 获取代币符号
            symbol = self.chain_config.symbol if self.chain_config else "ETH"
            
            return {
                'address': normalized_address,
                'balance_wei': balance_wei,
                'balance_native': float(balance_native),
                'symbol': symbol,
                'status': 'success'
            }
        except Web3Exception as e:
            return {
                'address': address,
                'balance_wei': 0,
                'balance_native': 0,
                'symbol': self.chain_config.symbol if self.chain_config else "ETH",
                'status': 'error',
                'error': str(e)
            }
    
    def batch_check_balances(self, addresses: List[str], delay: float = 0.1) -> List[Dict]:
        """批量查询地址余额"""
        results = []
        total = len(addresses)
        
        logger.section("开始批量查询", Icons.MAGNIFYING_GLASS)
        logger.info(f"总计 {total} 个地址，延迟 {delay} 秒")
        
        for i, address in enumerate(addresses, 1):
            clean_address = address.strip()
            
            if not clean_address:
                continue
            
            # 显示进度
            logger.progress(i, total, clean_address)
            
            if not self.is_valid_address(clean_address):
                result = {
                    'address': clean_address,
                    'balance_wei': 0,
                    'balance_native': 0,
                    'symbol': self.chain_config.symbol if self.chain_config else "ETH",
                    'status': 'invalid_address',
                    'error': '无效的EVM地址格式'
                }
            else:
                result = self.get_balance(clean_address)
            
            results.append(result)
            
            if i < total:
                time.sleep(delay)
        
        return results
    
    def load_addresses_from_file(self, file_path: str) -> List[str]:
        """从文件加载地址列表"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        addresses = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        addresses.append(line)
            
            logger.info(f"从文件加载了 {len(addresses)} 个地址", Icons.FOLDER)
            return addresses
            
        except Exception as e:
            raise Exception(f"读取文件失败: {e}")
    
    def save_results(self, results: List[Dict], output_file: str, only_with_balance: bool = True):
        """保存查询结果到文件"""
        output_path = Path(output_file)
        
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
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(filtered_results, f, indent=2, ensure_ascii=False)
            
            logger.success(f"结果已保存到: {output_path}", Icons.SAVE)
            
        except Exception as e:
            logger.error(f"保存结果失败: {e}")
    
    def save_addresses_with_balance(self, results: List[Dict], output_file: str = "addrs_results.txt"):
        """保存有余额的地址到文本文件"""
        output_path = Path(output_file)
        
        try:
            # 过滤有余额的地址
            addresses_with_balance = [
                result for result in results 
                if result['status'] == 'success' and result['balance_native'] > 0
            ]
            
            if not addresses_with_balance:
                logger.warning("没有找到有余额的地址")
                return
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for result in addresses_with_balance:
                    f.write(f'  - "{result["address"]}"\n')
            
            logger.success(f"有余额的地址已保存到: {output_path}", Icons.SAVE)
            logger.info(f"共保存了 {len(addresses_with_balance)} 个有余额的地址")
            
        except Exception as e:
            logger.error(f"保存地址列表失败: {e}")
    
    def print_summary(self, results: List[Dict]):
        """打印查询结果摘要"""
        total_addresses = len(results)
        successful = sum(1 for r in results if r['status'] == 'success')
        invalid = sum(1 for r in results if r['status'] == 'invalid_address')
        errors = sum(1 for r in results if r['status'] == 'error')
        
        total_balance = sum(r['balance_native'] for r in results if r['status'] == 'success')
        symbol = results[0]['symbol'] if results else "ETH"
        
        # 准备摘要数据
        summary_data = {
            "总地址数": total_addresses,
            "查询成功": successful,
            "无效地址": invalid,
            "查询错误": errors,
            f"总{symbol}余额": f"{total_balance:.6f} {symbol}"
        }
        
        logger.summary("查询结果摘要", summary_data)
        
        # 显示有余额的地址
        addresses_with_balance = [r for r in results if r['status'] == 'success' and r['balance_native'] > 0]
        if addresses_with_balance:
            logger.section("有余额的地址", Icons.COIN)
            for result in addresses_with_balance:
                logger.list_item(
                    f"{result['address']}: {result['balance_native']:.6f} {result['symbol']}",
                    Icons.COIN
                )
