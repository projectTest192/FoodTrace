#!/bin/bash

# 进入backend目录
cd backend

# 删除旧的数据库文件（如果存在）
rm -f backend/app/db/data/app.db

# 初始化数据库
python app/scripts/init_db.py

# 初始化管理员账号
python app/scripts/init_admin.py

# 返回到项目根目录
cd ..
