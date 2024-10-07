#!/bin/bash

MODE=$1

if [ "$MODE" == "down" ]; then
    # 停止网络
    docker-compose down --volumes --remove-orphans
    # 清理容器
    docker rm -f $(docker ps -aq) 2>/dev/null || true
    # 清理网络
    docker network prune -f
    # 清理数据
    rm -rf config/* crypto-config/* data/*
    rm -f core.yaml
    # 清理链码相关文件
    cd ../chaincode
    rm -f go.mod go.sum
    rm -rf vendor
    cd ../network
elif [ "$MODE" == "up" ]; then
    # 启动网络
    ./start.sh
else
    echo "Usage: $0 [up|down]"
    exit 1
fi 