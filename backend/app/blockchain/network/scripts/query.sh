#!/bin/bash

# 设置环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

# 获取查询参数
QUERY_FUNC=$1
shift  # 移除第一个参数，剩下的都是函数参数

# 构建参数数组
ARGS=()
for arg in "$@"; do
    ARGS+=("$arg")
done

# 显示帮助信息
if [ -z "$QUERY_FUNC" ]; then
    echo "Usage: ./query.sh <function_name> [args...]"
    echo "Available functions:"
    echo "  GetAllProducts            - 查询所有产品"
    echo "  GetProduct <prodId>       - 查询单个产品"
    echo "  GetActiveProducts         - 查询活跃产品"
    echo "  GetProductHistory <prodId> - 查询产品历史记录"
    echo "  GetProductsByStatus       - 查询产品状态"
    echo "  GetProductsByProducer     - 查询生产者产品"
    echo "  GetProductsByDateRange    - 查询产品日期范围"
    echo ""
    echo "Examples:"
    echo "  ./query.sh GetAllProducts"
    echo "  ./query.sh GetProduct PROD001"
    echo "  ./query.sh GetActiveProducts"
    echo "  ./query.sh GetProductHistory PROD001"
    echo "  ./query.sh GetProductsByStatus active"
    echo "  ./query.sh GetProductsByProducer producerA"
    echo "  ./query.sh GetProductsByDateRange 2024-01-01 2024-12-31"
    exit 1
fi

# 构建查询命令
QUERY_STRING="{\"Args\":[\"$QUERY_FUNC\""
for arg in "${ARGS[@]}"; do
    QUERY_STRING="$QUERY_STRING,\"$arg\""
done
QUERY_STRING="$QUERY_STRING]}"

# 执行查询
echo "Executing query: $QUERY_STRING"
peer chaincode query -C mychannel -n foodtrace -c "$QUERY_STRING"