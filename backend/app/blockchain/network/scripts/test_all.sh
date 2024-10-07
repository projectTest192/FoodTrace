#!/bin/bash

# 设置环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}
export CORE_PEER_TLS_ENABLED=false
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

# 测试场景1：创建新产品
echo "===== 测试场景1：创建新产品 ====="
echo "创建食品A..."
peer chaincode invoke -o localhost:7050 -C mychannel -n foodtrace \
    --peerAddresses localhost:7051 \
    -c '{"function":"CreateProduct","Args":[
        "PROD001",
        "foodA",
        "Fresh food A",
        "producerA",
        "2024-03-15",
        "DEV001",
        "RF001",
        "4.5",
        "45.2",
        "31.2304",
        "121.4737"
    ]}'

sleep 5

echo "创建食品B..."
peer chaincode invoke -o localhost:7050 -C mychannel -n foodtrace \
    --peerAddresses localhost:7051 \
    -c '{"function":"CreateProduct","Args":[
        "PROD002",
        "foodB",
        "Fresh food B",
        "producerB",
        "2024-03-16",
        "DEV001",
        "RF002",
        "4.8",
        "46.1",
        "31.2305",
        "121.4738"
    ]}'

sleep 5

# 测试场景2：查询产品
echo -e "\n===== 测试场景2：查询产品 ====="
echo "查询所有产品..."
peer chaincode query -C mychannel -n foodtrace \
    -c '{"Args":["GetAllProducts"]}'

sleep 2

# 测试场景3：状态管理
echo -e "\n===== 测试场景3：状态管理 ====="
echo "标记食品A为已售出..."
peer chaincode invoke -o localhost:7050 -C mychannel -n foodtrace \
    --peerAddresses localhost:7051 \
    -c '{"function":"SetProductStatus","Args":["PROD001","sold"]}'

sleep 5

echo "查看活跃产品..."
peer chaincode query -C mychannel -n foodtrace \
    -c '{"Args":["GetActiveProducts"]}'

# 测试按状态查询
echo "Testing GetProductsByStatus..."
peer chaincode query -C mychannel -n foodtrace -c '{"Args":["GetProductsByStatus", "active"]}'

# 测试按生产商查询
echo "Testing GetProductsByProducer..."
peer chaincode query -C mychannel -n foodtrace -c '{"Args":["GetProductsByProducer", "producerA"]}'

# 测试按日期范围查询
echo "Testing GetProductsByDateRange..."
peer chaincode query -C mychannel -n foodtrace -c '{"Args":["GetProductsByDateRange", "2024-01-01", "2024-12-31"]}'

echo -e "\n===== 测试完成 =====" 