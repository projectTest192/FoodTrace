#!/bin/bash

# 设置环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

echo "Installing new version of chaincode..."

# 安装新版本链码
peer lifecycle chaincode install foodtrace.tar.gz

# 获取最新安装的包ID
PACKAGE_ID=$(peer lifecycle chaincode queryinstalled | grep foodtrace | tail -n1 | awk '{print $3}' | sed 's/,//')
echo "Package ID: $PACKAGE_ID"

# 获取当前sequence
CURRENT_SEQUENCE=$(peer lifecycle chaincode querycommitted -C mychannel -n foodtrace --output json | jq -r '.sequence')
NEW_SEQUENCE=$((CURRENT_SEQUENCE + 1))
echo "Current sequence: $CURRENT_SEQUENCE"
echo "New sequence: $NEW_SEQUENCE"

# 批准链码定义
peer lifecycle chaincode approveformyorg \
    -o localhost:7050 \
    --channelID mychannel \
    --name foodtrace \
    --version "1.1" \
    --package-id $PACKAGE_ID \
    --sequence $NEW_SEQUENCE

# 提交链码定义
peer lifecycle chaincode commit \
    -o localhost:7050 \
    --channelID mychannel \
    --name foodtrace \
    --version "1.1" \
    --sequence $NEW_SEQUENCE

echo "Chaincode upgraded successfully"