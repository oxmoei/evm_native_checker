# EVM链批量地址余额查询工具 - 使用说明

## 快速开始

### 1. 安装依赖

```bash
# 使用Poetry（推荐）
poetry install --no-root

# 激活虚拟环境
poetry shell
```

### 2. 功能演示

```bash
# 查看功能演示
python demo.py
```

### 3. 查看支持的链

```bash
poetry run evm-native-checker --list-chains
```

### 4. 查询单个地址

```bash
# 查询以太坊地址
poetry run evm-native-checker --address 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe --chain ethereum

# 查询BSC地址
poetry run evm-native-checker --address 0x28C6c06298d514Db089934071355E5743bf21d60 --chain bsc
```

### 5. 批量查询

```bash
# 从文件批量查询（默认只保存有余额的地址）
poetry run evm-native-checker --file addresses.txt --chain polygon

# 导出为CSV格式（只保存有余额的地址）
poetry run evm-native-checker --file addresses.txt --chain bsc --format csv --output results.csv

# 保存所有查询结果（包括无余额的地址）
poetry run evm-native-checker --file addresses.txt --chain polygon --all-results --output all_results.json
```

### 6. 交互式查询（推荐新手）

```bash
# 交互式配置和查询
python check.py
```

## 支持的网络

- **ethereum**: 以太坊主网 (ETH)
- **bsc**: 币安智能链 (BNB)
- **polygon**: Polygon网络 (MATIC)
- **arbitrum**: Arbitrum One (ETH)
- **optimism**: Optimism网络 (ETH)
- **avalanche**: Avalanche C-Chain (AVAX)
- **fantom**: Fantom Opera (FTM)
- **base**: Base网络 (ETH)
- **linea**: Linea网络 (ETH)

## 文件说明

- `check.py`: 交互式查询脚本（推荐新手使用）
- `demo.py`: 功能演示脚本
- `addresses.txt`: 示例地址文件
- `EVM_native_checker/`: 核心包
- `examples/custom_chains.py`: 自定义链配置示例

## 注意事项

1. 首次使用需要配置RPC节点URL
2. 免费RPC节点有请求频率限制
3. 支持所有EVM兼容链
4. 自动识别链类型和代币符号
5. 交互式脚本自动保存有余额的地址，CLI使用 `--all-results` 保存所有结果
