"""
EVM链批量地址余额查询工具

一个用于批量查询多种EVM兼容链原生代币余额的Python工具包。
"""

__version__ = "0.1.0"
__author__ = "ylx"
__email__ = "cryptostar@163.com"

from .checker import EthereumBalanceChecker
from .utils import quick_check_balance
from .chains import EVMChains, ChainConfig, ChainType, detect_chain_from_rpc

__all__ = ["EthereumBalanceChecker", "quick_check_balance", "EVMChains", "ChainConfig", "ChainType", "detect_chain_from_rpc"]
