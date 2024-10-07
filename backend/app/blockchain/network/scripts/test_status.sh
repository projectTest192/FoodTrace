#!/bin/bash

# 设置环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

# 测试产品状态管理
echo "===== 测试产品状态管理 ====="

echo "1. 查看所有产品的当前状态..."
peer chaincode query -C mychannel -n foodtrace \
    -c '{"Args":["GetAllProducts"]}'

echo -e "\n2. 标记产品为已售出..."
peer chaincode invoke -o localhost:7050 -C mychannel -n foodtrace \
    --peerAddresses localhost:7051 \
    -c '{"function":"SetProductStatus","Args":["PROD001","sold"]}'

sleep 5

echo -e "\n3. 查看活跃产品..."
peer chaincode query -C mychannel -n foodtrace \
    -c '{"Args":["GetActiveProducts"]}'

echo -e "\n===== 测试完成 =====" 