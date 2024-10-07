import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.session import SessionLocal
from app.models.user import User, Role
from app.core.security import getPassHash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_admin():
    db = SessionLocal()
    try:
        # 1. 首先创建角色
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            admin_role = Role(
                name="admin",
                desc="System Administrator"
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        
        # 2. 检查管理员是否已存在
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            # 3. 创建管理员用户
            admin = User(
                name="theo",
                email="theo@theo.com",
                phone="13888888888",
                pwd=getPassHash("theo123"),
                roleId=admin_role.id,
                active=True,
                verified=True
            )
            db.add(admin)
            db.commit()
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
            
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise e
    finally:
        db.close()

def main():
    print(f"\nInitializing admin user in database: {SessionLocal().bind.engine.url.database}\n")
    try:
        init_admin()
        print("Admin user initialized successfully")
    except Exception as e:
        print(f"Failed to initialize admin: {str(e)}")

if __name__ == "__main__":
    main() 