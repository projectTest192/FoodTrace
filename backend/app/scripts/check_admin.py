import sys
from pathlib import Path

# 获取backend目录的路径
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BACKEND_DIR))

from sqlalchemy.orm import Session
from app.db.session import engine
from app.models.user import User, Role

def check_admin():
    with Session(engine) as db:
        # 检查角色
        roles = db.query(Role).all()
        print("\nRoles in database:")
        for role in roles:
            print(f"- {role.name}: {role.desc}")
        
        # 检查管理员
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if admin:
            print("\nAdmin user exists:")
            print(f"- Name: {admin.name}")
            print(f"- Email: {admin.email}")
            print(f"- Role ID: {admin.roleId}")
            print(f"- Active: {admin.active}")
            print(f"- Verified: {admin.verified}")
        else:
            print("\nWARNING: Admin user not found!")

if __name__ == "__main__":
    check_admin() 