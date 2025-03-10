#!/bin/bash

# 确保在项目根目录
cd "$(dirname "$0")"

echo "Current directory: $(pwd)"

# 删除旧的数据库文件（如果存在）
echo "Cleaning up old database..."
sudo rm -rf backend/app/db/data
mkdir -p backend/app/db/data
chmod -R 777 backend/app/db/data

# 初始化数据库
echo -e "\nInitializing database..."
python backend/app/scripts/init_db.py

# 创建管理员账号
echo -e "\nCreating admin user..."
python backend/app/scripts/init_admin.py

# 检查管理员账号
echo -e "\nChecking admin user..."
python backend/app/scripts/check_admin.py

# 启动后端（确保在backend目录下运行）
cd backend || exit
echo -e "\nStarting backend server..."
python -m uvicorn app.main:app --reload --port 8002 &

# 等待后端启动
sleep 3

# 启动前端
cd ../frontend || exit
echo -e "\nStarting frontend..."
npm start 