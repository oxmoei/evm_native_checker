#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自定义链配置示例
展示如何添加和使用自定义的EVM链配置
"""

from EVM_native_checker import EVMChains, ChainConfig, ChainType, EthereumBalanceChecker


def add_custom_chains():
    """添加自定义链配置示例"""
    
    # 添加自定义链配置
    custom_chains = {
        # 添加一个新的测试网
        "my_testnet": ChainConfig(
            name="My Test Network",
            chain_id=9999,
            symbol="MTN",
            decimals=18,
            rpc_url="https://testnet.mychain.com",
            explorer_url="https://testnet-explorer.mychain.com",
            chain_type=ChainType.TESTNET,
            is_testnet=True,
            native_currency="MTN"
        ),
        
        # 添加一个私有链
        "private_chain": ChainConfig(
            name="Private Chain",
            chain_id=1337,
            symbol="PRV",
            decimals=18,
            rpc_url="http://192.168.1.100:8545",
            explorer_url="",
            chain_type=ChainType.DEVNET,
            native_currency="PRV"
        ),
        
        # 添加一个Layer2网络
        "my_layer2": ChainConfig(
            name="My Layer2 Network",
            chain_id=12345,
            symbol="L2T",
            decimals=18,
            rpc_url="https://rpc.mylayer2.com",
            explorer_url="https://explorer.mylayer2.com",
            chain_type=ChainType.MAINNET,
            native_currency="L2T"
        )
    }
    
    # 注册自定义链
    for name, config in custom_chains.items():
        EVMChains.add_custom_chain(name, config)
        print(f"✅ 已添加自定义链: {name} ({config.name})")
    
    return custom_chains


def use_custom_chain():
    """使用自定义链的示例"""
    
    # 添加自定义链
    add_custom_chains()
    
    # 使用自定义链查询余额
    try:
        # 使用自定义链名称
        checker = EthereumBalanceChecker(chain_name="my_testnet")
        
        # 查询地址余额
        address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"
        result = checker.get_balance(address)
        
        print(f"查询结果: {result}")
        
    except Exception as e:
        print(f"查询失败: {e}")


def list_all_chains():
    """列出所有可用的链（包括自定义链）"""
    
    # 添加自定义链
    add_custom_chains()
    
    # 列出所有链
    print("📋 所有可用链:")
    chains = EVMChains.list_available_chains()
    
    for name, info in chains.items():
        chain_type = "测试网" if info['is_testnet'] else "主网"
        print(f"  {name}: {info['name']} ({info['symbol']}) - {chain_type} - Chain ID: {info['chain_id']}")


if __name__ == "__main__":
    print("🔧 自定义链配置示例")
    print("="*50)
    
    # 列出所有链
    list_all_chains()
    
    print("\n" + "="*50)
    print("使用自定义链查询余额:")
    use_custom_chain()
