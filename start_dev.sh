#!/bin/bash

# 确保在项目根目录
cd "$(dirname "$0")"

# 启动SMTP调试服务器（后台运行）
echo "启动SMTP调试服务器..."
python -m smtpd -n -c DebuggingServer localhost:1025 &
SMTP_PID=$!

# 删除旧的数据库文件（如果存在）
echo "清理旧数据库..."
rm -rf backend/app/db/data
mkdir -p backend/app/db/data
chmod -R 777 backend/app/db/data

# 初始化数据库
echo -e "\n初始化数据库..."
python backend/app/scripts/init_db.py

# 创建管理员账号
echo -e "\n创建管理员账号..."
python backend/app/scripts/init_admin.py

# 检查管理员账号
echo -e "\n检查管理员账号..."
python backend/app/scripts/check_admin.py

# 启动后端
cd backend || exit
echo -e "\n启动后端服务器..."
python -m uvicorn app.main:app --reload --port 8002 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
cd ../frontend || exit
echo -e "\n启动前端..."
npm start &
FRONTEND_PID=$!

# 等待用户按Ctrl+C
echo -e "\n所有服务已启动。按Ctrl+C停止..."
wait

# 清理进程
kill $SMTP_PID
kill $BACKEND_PID
kill $FRONTEND_PID 