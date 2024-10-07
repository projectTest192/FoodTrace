import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.user import User, Role
from app.models.product import Product
from app.models.shipment import Shipment
from app.models.iot import DeviceInfo
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    db = SessionLocal()
    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
        
        # 初始化基础角色
        roles = [
            {"name": "admin", "description": "System Administrator"},
            {"name": "consumer", "description": "Normal Consumer"},
            {"name": "producer", "description": "Food Producer"},
            {"name": "distributor", "description": "Food Distributor"},
            {"name": "retailer", "description": "Food Retailer"}
        ]
        
        for role_data in roles:
            role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not role:
                role = Role(**role_data)
                db.add(role)
        
        db.commit()
        logger.info("Basic roles initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise e
    finally:
        db.close()

def main():
    # 使用 session.py 中定义的路径
    from app.db.session import DB_FILE, DB_DIR
    
    print(f"Database directory: {DB_DIR}")
    print(f"Database file: {DB_FILE}")
    
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    exists = os.path.exists(DB_FILE)
    print(f"Database exists: {exists}")
    
    if not exists:
        print("Initializing database...")
        try:
            init_db()
            print("Database initialization completed")
        except Exception as e:
            print(f"Failed to initialize database: {str(e)}")

if __name__ == "__main__":
    main() 