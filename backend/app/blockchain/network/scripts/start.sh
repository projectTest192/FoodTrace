#!/bin/bash

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# 检查必要的二进制文件
for binary in cryptogen configtxgen peer; do
    if [ ! -f "./bin/$binary" ]; then
        echo "Missing required binary: $binary"
        echo "Please run the Fabric binary installation script first."
        exit 1
    fi
done

# 添加环境变量
export PATH=${PWD}/bin:$PATH
export FABRIC_CFG_PATH=${PWD}

# 清理旧文件和容器
echo "Cleaning up old files and containers..."
docker-compose down --volumes --remove-orphans
rm -rf config/*
rm -rf crypto-config/*
rm -rf data/*

# 创建必要的目录
mkdir -p config
mkdir -p crypto-config
mkdir -p data/peer0.org1.example.com

# 获取 core.yaml
if [ ! -f "core.yaml" ]; then
    echo "Getting core.yaml..."
    CONTAINER_ID=$(docker create hyperledger/fabric-peer:2.4)
    docker cp ${CONTAINER_ID}:/etc/hyperledger/fabric/core.yaml .
    docker rm ${CONTAINER_ID}
fi

echo "Generating certificates..."
./bin/cryptogen generate --config=./crypto-config.yaml --output="crypto-config"

# 创建必要的 MSP 目录结构
for org in org1.example.com; do
    for peer in peer0; do
        PEER_PATH="./crypto-config/peerOrganizations/${org}/peers/${peer}.${org}"
        ADMIN_PATH="./crypto-config/peerOrganizations/${org}/users/Admin@${org}"
        
        # 创建目录
        mkdir -p ${PEER_PATH}/msp/{admincerts,cacerts,keystore,signcerts,tlscacerts}
        mkdir -p ${PEER_PATH}/tls
        
        # 复制 MSP 证书
        cp ${ADMIN_PATH}/msp/signcerts/Admin@${org}-cert.pem ${PEER_PATH}/msp/admincerts/
        cp ./crypto-config/peerOrganizations/${org}/ca/ca.${org}-cert.pem ${PEER_PATH}/msp/cacerts/
        cp ./crypto-config/peerOrganizations/${org}/tlsca/tlsca.${org}-cert.pem ${PEER_PATH}/msp/tlscacerts/
        
        # 复制 TLS 证书
        cp ./crypto-config/peerOrganizations/${org}/tlsca/tlsca.${org}-cert.pem ${PEER_PATH}/tls/ca.crt
        cp ${ADMIN_PATH}/tls/client.crt ${PEER_PATH}/tls/server.crt
        cp ${ADMIN_PATH}/tls/client.key ${PEER_PATH}/tls/server.key
        
        # 复制私钥
        cp ${ADMIN_PATH}/msp/keystore/priv_sk ${PEER_PATH}/msp/keystore/
        
        # 复制签名证书
        cp ${ADMIN_PATH}/msp/signcerts/Admin@${org}-cert.pem ${PEER_PATH}/msp/signcerts/peer.${org}-cert.pem
        
        # 创建 config.yaml
        cat > ${PEER_PATH}/msp/config.yaml << EOF
NodeOUs:
  Enable: true
  ClientOUIdentifier:
    Certificate: cacerts/ca.${org}-cert.pem
    OrganizationalUnitIdentifier: client
  PeerOUIdentifier:
    Certificate: cacerts/ca.${org}-cert.pem
    OrganizationalUnitIdentifier: peer
  AdminOUIdentifier:
    Certificate: cacerts/ca.${org}-cert.pem
    OrganizationalUnitIdentifier: admin
  OrdererOUIdentifier:
    Certificate: cacerts/ca.${org}-cert.pem
    OrganizationalUnitIdentifier: orderer
EOF
    done
done

# 设置权限
chmod -R 755 crypto-config

echo "Generating genesis block..."
./bin/configtxgen -profile TwoOrgsOrdererGenesis -channelID system-channel -outputBlock ./config/genesis.block

echo "Generating channel transaction..."
./bin/configtxgen -profile TwoOrgsChannel -outputCreateChannelTx ./config/channel.tx -channelID mychannel

echo "Starting network..."
docker-compose up -d peer0.org1.example.com orderer.example.com

# 等待容器启动
echo "Waiting for containers to start..."
for i in {1..30}; do
    if docker ps | grep "orderer.example.com" && docker ps | grep "peer0.org1.example.com"; then
        echo "Containers are running"
        break
    fi
    echo "Waiting for containers... ($i/30)"
    sleep 2
done

# 检查容器是否真正启动
if ! docker ps | grep "orderer.example.com" || ! docker ps | grep "peer0.org1.example.com"; then
    echo "Error: Containers failed to start"
    docker-compose logs
    exit 1
fi

# 等待网络服务就绪
echo "Waiting for network services..."
sleep 10

# 设置环境变量
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_MSPCONFIGPATH=${PWD}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051

# 创建通道
echo "Creating channel..."
peer channel create -o localhost:7050 -c mychannel -f ./config/channel.tx --outputBlock ./config/mychannel.block

# 加入通道
echo "Joining channel..."
peer channel join -b ./config/mychannel.block

# 准备链码
echo "Preparing chaincode..."
cd ../chaincode
rm -f go.mod go.sum
rm -rf vendor

# 创建 go.mod
cat > go.mod << EOF
module foodtrace

go 1.21

require github.com/hyperledger/fabric-contract-api-go v1.2.1
EOF

# 更新依赖
go mod tidy

# 返回到 network 目录
cd ../network

# 打包链码
echo "Packaging chaincode..."
peer lifecycle chaincode package foodtrace.tar.gz \
    --path ../chaincode \
    --lang golang \
    --label foodtrace_1.0

# 安装链码前先检查环境
echo "Checking peer status..."
peer node status || {
    echo "Error: Peer is not running properly"
    exit 1
}

# 安装链码
echo "Installing chaincode..."
peer lifecycle chaincode install foodtrace.tar.gz

# 获取包ID并验证
echo "Getting chaincode package ID..."
PACKAGE_ID=$(peer lifecycle chaincode queryinstalled 2>&1 | grep "foodtrace_1.0" | sed -n 's/^Package ID: \(.*\), Label: foodtrace_1.0$/\1/p')
if [ -z "$PACKAGE_ID" ]; then
    echo "Error: Failed to get package ID"
    exit 1
fi
echo "Package ID: ${PACKAGE_ID}"

# 批准链码
echo "Approving chaincode..."
peer lifecycle chaincode approveformyorg \
    -o localhost:7050 \
    --channelID mychannel \
    --name foodtrace \
    --version 1.0 \
    --package-id ${PACKAGE_ID} \
    --sequence 1 \
    --init-required

# 检查批准状态
echo "Checking commit readiness..."
peer lifecycle chaincode checkcommitreadiness \
    --channelID mychannel \
    --name foodtrace \
    --version 1.0 \
    --sequence 1 \
    --init-required \
    --output json

# 提交链码定义
echo "Committing chaincode..."
peer lifecycle chaincode commit \
    -o localhost:7050 \
    --channelID mychannel \
    --name foodtrace \
    --version 1.0 \
    --sequence 1 \
    --init-required \
    --peerAddresses localhost:7051

# 等待链码启动
echo "Waiting for chaincode to start..."
sleep 10

# 检查链码定义
echo "Checking chaincode definition..."
peer lifecycle chaincode querycommitted \
    --channelID mychannel \
    --name foodtrace \
    --output json || {
    echo "Error: Chaincode not committed properly"
    exit 1
}

# 初始化链码
echo "Initializing chaincode..."
peer chaincode invoke \
    -o localhost:7050 \
    --channelID mychannel \
    --name foodtrace \
    --isInit \
    -c '{"function":"Init","Args":[]}' \
    --peerAddresses localhost:7051

# 等待一下让初始化完成
sleep 10

# 验证初始化是否成功
echo "Verifying initialization..."
peer chaincode query \
    -C mychannel \
    -n foodtrace \
    -c '{"Args":["GetAllProducts"]}'

# 等待链码容器启动
echo "Waiting for chaincode container to start..."
for i in {1..30}; do
    if docker ps | grep dev-peer0.org1.example.com-foodtrace; then
        echo "Chaincode container is running"
        break
    fi
    echo "Waiting for chaincode container... ($i/30)"
    sleep 2
done

# 最终验证
if ! docker ps | grep dev-peer0.org1.example.com-foodtrace; then
    echo "Error: Chaincode container failed to start"
    exit 1
fi

echo "Network setup complete!"