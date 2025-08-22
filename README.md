# EVM链批量地址余额查询工具

这是一个用于批量查询多种EVM兼容链地址原生代币余额的Python工具。

## 功能特性

- 🔍 批量查询多个EVM地址的原生代币余额
- 🌐 支持多种EVM兼容链（以太坊、BSC、Polygon、Arbitrum、Optimism等）
- 📁 支持从文件读取地址列表
- ✅ 自动验证地址格式
- 💾 将查询结果保存为JSON或CSV格式（默认只保存有余额的地址）
- 📊 提供详细的查询统计信息
- ⚡ 支持自定义RPC节点
- 🛡️ 内置错误处理和重试机制
- 🔧 支持链类型自动检测
- 🎨 美化的日志输出，支持颜色和图标

## 安装依赖

### 使用Poetry（推荐）

```bash
# 安装Poetry（如果还没有安装）
curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install --no-root
```



## 使用方法

### 1. 准备地址文件

创建一个文本文件（如 `addresses.txt`），每行一个EVM地址：

```
0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
0x28C6c06298d514Db089934071355E5743bf21d60
0xA090e606E30bD747d4E6245a1517EbE430F0057e
```

### 2. 配置链和RPC节点

#### 使用预定义链（推荐）

```bash
# 查看支持的链
poetry run eth-balance-checker --list-chains

# 使用特定链
poetry run eth-balance-checker --chain ethereum --file addresses.txt
poetry run eth-balance-checker --chain bsc --file addresses.txt
poetry run eth-balance-checker --chain polygon --file addresses.txt
```

#### 使用自定义RPC节点

```bash
# 自定义RPC节点
poetry run evm-native-checker --rpc https://mainnet.infura.io/v3/YOUR-PROJECT-ID --file addresses.txt
```

#### 支持的链

- **Ethereum**: 以太坊主网 (ETH)
- **BSC**: 币安智能链 (BNB)
- **Polygon**: Polygon网络 (MATIC)
- **Arbitrum**: Arbitrum One (ETH)
- **Optimism**: Optimism网络 (ETH)
- **Avalanche**: Avalanche C-Chain (AVAX)
- **Fantom**: Fantom Opera (FTM)
- **Base**: Base网络 (ETH)
- **Linea**: Linea网络 (ETH)

### 3. 运行脚本

#### 使用CLI工具（推荐）

```bash
# 查看支持的链
poetry run evm-native-checker --list-chains

# 查询单个地址
poetry run evm-native-checker --address 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe --chain ethereum

# 批量查询（指定链）
poetry run evm-native-checker --file addresses.txt --chain bsc

# 批量查询（自定义RPC）
poetry run evm-native-checker --file addresses.txt --rpc https://mainnet.infura.io/v3/YOUR-PROJECT-ID

# 导出为CSV格式（只保存有余额的地址）
poetry run evm-native-checker --file addresses.txt --chain polygon --format csv --output results.csv

# 保存所有查询结果（包括无余额的地址）
poetry run evm-native-checker --file addresses.txt --chain polygon --all-results --output all_results.json
```

#### 使用Python脚本（交互式）

```bash
poetry run python check.py
```

脚本会引导您完成以下配置：
1. **RPC节点配置**：选择预定义链或输入自定义RPC URL
2. **链选择**：从支持的链列表中选择
3. **查询延迟**：设置请求间隔时间
4. **文件路径**：指定地址文件和输出文件路径

或者指定自定义RPC节点：

```bash
poetry run python check.py "https://mainnet.infura.io/v3/YOUR-PROJECT-ID"
```

### 4. 交互式配置

脚本会引导您完成以下配置：

1. **RPC节点配置**：
   - 选择预定义链配置
   - 或输入自定义RPC URL

2. **链选择**：
   - 从支持的链列表中选择
   - 支持数字选择或链名称输入

3. **查询延迟配置**：
   - 设置请求间隔时间
   - 建议值：0.1-0.5秒

4. **文件路径配置**：
   - 地址文件路径（默认：addresses.txt）
   - 输出文件路径（默认：balance_results.json）
   - 自动保存有余额的地址（无需询问）

## 输出格式

查询结果将保存为JSON或CSV格式，默认只保存有余额的地址。包含以下信息：

```json
[
  {
    "address": "0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe",
    "balance_wei": "1000000000000000000",
    "balance_native": 1.0,
    "symbol": "ETH",
    "status": "success"
  },
  {
    "address": "0x28C6c06298d514Db089934071355E5743bf21d60",
    "balance_wei": "5000000000000000000",
    "balance_native": 5.0,
    "symbol": "BNB",
    "status": "success"
  },
  {
    "address": "0x1234567890123456789012345678901234567890",
    "balance_wei": 0,
    "balance_native": 0,
    "symbol": "ETH",
    "status": "invalid_address",
    "error": "无效的EVM地址格式"
  }
]
```

## 注意事项

1. **RPC节点限制**：免费RPC节点通常有请求频率限制，脚本内置了延迟机制
2. **地址格式**：支持带0x前缀和不带前缀的地址格式
3. **错误处理**：脚本会自动处理无效地址和网络错误
4. **文件编码**：建议使用UTF-8编码保存地址文件
5. **多链支持**：支持所有EVM兼容链，自动识别链类型和代币符号
6. **链配置**：可以自定义添加新的链配置
7. **智能过滤**：自动保存有余额的地址，减少输出文件大小

## 示例输出

```
🚀 EVM链批量地址余额查询工具
============================================================
  支持多种EVM兼容链的原生代币余额查询
============================================================

🔧 RPC节点配置
------------------------------
请选择配置方式:
1. 使用预定义链配置
2. 输入自定义RPC URL

📋 可用的链
------------------------------
  🌐 主网:
    • 1. ethereum: Ethereum (ETH)
    • 2. bsc: BNB Smart Chain (BNB)
    • 3. polygon: Polygon (MATIC)

✅ 成功连接到 BNB Smart Chain (BNB)
ℹ️ RPC URL: https://bsc-dataseed1.binance.org

⏱️ 查询延迟配置
--------------------
ℹ️ 延迟时间用于避免触发RPC节点的频率限制
ℹ️ 建议值: 0.1-0.5秒

🔍 开始批量查询
------------------------------
ℹ️ 总计 5 个地址，延迟 0.2 秒
[██████████████████████████████] 5/5 (100.0%) - 0x28C6c06298d514Db089934071355E5743bf21d60

📊 查询结果摘要
==================================================
  总地址数: 5
  查询成功: 4
  无效地址: 1
  查询错误: 0
  总BNB余额: 1234.567890 BNB
==================================================

💰 有余额的地址
------------------------------
  💰 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe: 1000.000000 BNB
  💰 0x28C6c06298d514Db089934071355E5743bf21d60: 234.567890 BNB

💾 结果已保存到: balance_results.json

============================================================
  🎉 批量查询完成！
============================================================
```

## 开发

### 代码格式化

```bash
# 格式化代码
poetry run black .

# 检查代码风格
poetry run flake8 .
```

### 日志美化演示

```bash
# 查看美化后的输出效果
poetry run python demo_logger.py
```

### 构建和发布

```bash
# 构建包
poetry build

# 发布到PyPI（需要配置）
poetry publish
```

## 故障排除

### 连接问题
- 检查RPC节点URL是否正确
- 确认网络连接正常
- 验证API密钥是否有效

### 权限问题
- 确保有读取地址文件的权限
- 确保有写入输出文件的权限

### 性能优化
- 对于大量地址，可以调整延迟时间
- 考虑使用付费RPC节点以获得更好的性能

### Poetry相关问题
- 确保已正确安装Poetry
- 检查pyproject.toml文件格式是否正确
- 尝试删除poetry.lock文件并重新安装依赖
