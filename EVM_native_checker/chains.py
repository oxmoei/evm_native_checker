#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EVM链配置模块
支持多种EVM兼容链的配置和识别
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ChainType(Enum):
    """链类型枚举"""
    MAINNET = "mainnet"
    TESTNET = "testnet"
    DEVNET = "devnet"


@dataclass
class ChainConfig:
    """链配置数据类"""
    name: str
    chain_id: int
    symbol: str
    decimals: int
    rpc_url: str
    explorer_url: str
    chain_type: ChainType
    is_testnet: bool = False
    native_currency: str = "ETH"
    block_time: int = 12  # 秒


class EVMChains:
    """EVM链管理器"""
    
    # 预定义的链配置
    CHAINS: Dict[str, ChainConfig] = {
        # 以太坊主网
        "ethereum": ChainConfig(
            name="Ethereum",
            chain_id=1,
            symbol="ETH",
            decimals=18,
            rpc_url="https://mainnet.infura.io/v3/YOUR-PROJECT-ID",
            explorer_url="https://etherscan.io",
            chain_type=ChainType.MAINNET
        ),
        
        # BSC主网
        "bsc": ChainConfig(
            name="BNB Smart Chain",
            chain_id=56,
            symbol="BNB",
            decimals=18,
            rpc_url="https://bsc-dataseed1.binance.org",
            explorer_url="https://bscscan.com",
            chain_type=ChainType.MAINNET,
            native_currency="BNB"
        ),
        
        # Polygon主网
        "polygon": ChainConfig(
            name="Polygon",
            chain_id=137,
            symbol="MATIC",
            decimals=18,
            rpc_url="https://polygon-rpc.com",
            explorer_url="https://polygonscan.com",
            chain_type=ChainType.MAINNET,
            native_currency="MATIC"
        ),
        
        # Arbitrum One
        "arbitrum": ChainConfig(
            name="Arbitrum One",
            chain_id=42161,
            symbol="ETH",
            decimals=18,
            rpc_url="https://arb1.arbitrum.io/rpc",
            explorer_url="https://arbiscan.io",
            chain_type=ChainType.MAINNET
        ),
        
        # Optimism
        "optimism": ChainConfig(
            name="Optimism",
            chain_id=10,
            symbol="ETH",
            decimals=18,
            rpc_url="https://mainnet.optimism.io",
            explorer_url="https://optimistic.etherscan.io",
            chain_type=ChainType.MAINNET
        ),
        
        # Avalanche C-Chain
        "avalanche": ChainConfig(
            name="Avalanche C-Chain",
            chain_id=43114,
            symbol="AVAX",
            decimals=18,
            rpc_url="https://api.avax.network/ext/bc/C/rpc",
            explorer_url="https://snowtrace.io",
            chain_type=ChainType.MAINNET,
            native_currency="AVAX"
        ),
        
        # Fantom Opera
        "fantom": ChainConfig(
            name="Fantom Opera",
            chain_id=250,
            symbol="FTM",
            decimals=18,
            rpc_url="https://rpc.ftm.tools",
            explorer_url="https://ftmscan.com",
            chain_type=ChainType.MAINNET,
            native_currency="FTM"
        ),
        
        # Base
        "base": ChainConfig(
            name="Base",
            chain_id=8453,
            symbol="ETH",
            decimals=18,
            rpc_url="https://mainnet.base.org",
            explorer_url="https://basescan.org",
            chain_type=ChainType.MAINNET
        ),
        
        # Linea
        "linea": ChainConfig(
            name="Linea",
            chain_id=59144,
            symbol="ETH",
            decimals=18,
            rpc_url="https://rpc.linea.build",
            explorer_url="https://lineascan.build",
            chain_type=ChainType.MAINNET
        ),
        
        # 本地开发链
        "localhost": ChainConfig(
            name="Localhost",
            chain_id=1337,
            symbol="ETH",
            decimals=18,
            rpc_url="http://localhost:8545",
            explorer_url="",
            chain_type=ChainType.DEVNET,
            native_currency="ETH"
        ),
    }
    
    @classmethod
    def get_chain_by_name(cls, name: str) -> Optional[ChainConfig]:
        """根据名称获取链配置"""
        return cls.CHAINS.get(name.lower())
    
    @classmethod
    def get_chain_by_id(cls, chain_id: int) -> Optional[ChainConfig]:
        """根据链ID获取链配置"""
        for chain in cls.CHAINS.values():
            if chain.chain_id == chain_id:
                return chain
        return None
    
    @classmethod
    def get_all_chains(cls) -> List[ChainConfig]:
        """获取所有链配置"""
        return list(cls.CHAINS.values())
    
    @classmethod
    def get_mainnet_chains(cls) -> List[ChainConfig]:
        """获取所有主网链"""
        return [chain for chain in cls.CHAINS.values() if not chain.is_testnet]
    
    @classmethod
    def add_custom_chain(cls, name: str, config: ChainConfig) -> None:
        """添加自定义链配置"""
        cls.CHAINS[name.lower()] = config
    
    @classmethod
    def list_available_chains(cls) -> Dict[str, Dict[str, Any]]:
        """列出所有可用链的信息"""
        chains_info = {}
        for name, chain in cls.CHAINS.items():
            chains_info[name] = {
                "name": chain.name,
                "chain_id": chain.chain_id,
                "symbol": chain.symbol,
                "native_currency": chain.native_currency,
                "is_testnet": chain.is_testnet,
                "explorer_url": chain.explorer_url
            }
        return chains_info


def detect_chain_from_rpc(rpc_url: str) -> Optional[ChainConfig]:
    """从RPC URL自动检测链类型"""
    rpc_lower = rpc_url.lower()
    
    if "infura.io" in rpc_lower:
        return EVMChains.get_chain_by_name("ethereum")
    elif "binance.org" in rpc_lower or "bsc" in rpc_lower:
        return EVMChains.get_chain_by_name("bsc")
    elif "polygon" in rpc_lower or "matic" in rpc_lower:
        return EVMChains.get_chain_by_name("polygon")
    elif "arbitrum" in rpc_lower:
        return EVMChains.get_chain_by_name("arbitrum")
    elif "optimism" in rpc_lower:
        return EVMChains.get_chain_by_name("optimism")
    elif "avax" in rpc_lower or "avalanche" in rpc_lower:
        return EVMChains.get_chain_by_name("avalanche")
    elif "ftm" in rpc_lower or "fantom" in rpc_lower:
        return EVMChains.get_chain_by_name("fantom")
    elif "base" in rpc_lower:
        return EVMChains.get_chain_by_name("base")
    elif "linea" in rpc_lower:
        return EVMChains.get_chain_by_name("linea")
    elif "localhost" in rpc_lower or "127.0.0.1" in rpc_lower:
        return EVMChains.get_chain_by_name("localhost")
    
    return None
