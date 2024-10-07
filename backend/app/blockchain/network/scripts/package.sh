#!/bin/bash

# 设置环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

echo "Packaging chaincode..."

# 清理旧的链码包
rm -f foodtrace.tar.gz

# 确保链码目录正确
CHAINCODE_PATH="../chaincode"
if [ ! -f "$CHAINCODE_PATH/foodtrace.go" ]; then
    echo "Error: Cannot find foodtrace.go in $CHAINCODE_PATH"
    exit 1
fi

# 获取当前时间戳作为版本标识
TIMESTAMP=$(date +%Y%m%d%H%M%S)
VERSION="1.1_${TIMESTAMP}"

# 打包链码
peer lifecycle chaincode package foodtrace.tar.gz \
    --path $CHAINCODE_PATH \
    --lang golang \
    --label "foodtrace_${VERSION}"

echo "Chaincode packaged with version: ${VERSION}" 