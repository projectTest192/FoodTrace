from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..db.base_class import Base
from ..models.product import Product, Category, ProductIoTData, ProductPrice, ProdTrace, ProductStock
from ..models.user import User, Role, Permission
from ..models.iot import DeviceInfo, IotData, EnvData, TraceEvent, RfidBind
from ..models.shipment import Shipment, ShipTrace, ShipmentItem, ShipmentStatus
from ..models.sale import Sale, SaleItem
from ..models.order import Order, OrderItem, OrderStatus
from ..core.config import settings
from ..core.security import getPassHash
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    """初始化数据库"""
    try:
        # 确保所有模型都被导入和注册
        Base.metadata.create_all(bind=db.get_bind())
        
        # 1. 创建角色
        roles = [
            Role(id=1, name="admin", description="System Administrator"),
            Role(id=2, name="producer", description="Food Producer"),
            Role(id=3, name="distributor", description="Logistics Provider"),
            Role(id=4, name="retailer", description="Retailer"),
            Role(id=5, name="consumer", description="Consumer")
        ]
        
        # 检查并添加不存在的角色
        for role in roles:
            existing_role = db.query(Role).filter(Role.name == role.name).first()
            if not existing_role:
                db.add(role)
        
        db.commit()  # 先提交角色，确保有角色ID
        
        # 2. 创建管理员用户
        admin = User(
            id=f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}",  # 生成ID
            username="theo",
            email="theo@theo.com",
            pwd=getPassHash("test123"),
            is_active=True,
            verified=True,
            role_id=1  # admin role
        )
        
        # 检查管理员是否已存在
        existing_admin = db.query(User).filter(User.email == admin.email).first()
        if not existing_admin:
            db.add(admin)
            print("Admin user created successfully")
        
        # 3. 创建产品类别
        categories = [
            Category(name="Fruits", description="Fresh Fruits"),
            Category(name="Vegetables", description="Fresh Vegetables"),
            Category(name="Meat", description="Fresh Meat"),
            Category(name="Seafood", description="Fresh Seafood"),
            Category(name="Dairy", description="Dairy Products")
        ]
        
        # 检查并添加不存在的类别
        for category in categories:
            existing_category = db.query(Category).filter(Category.name == category.name).first()
            if not existing_category:
                db.add(category)
        
        # 提交所有更改
        db.commit()
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        db.rollback()
        logger.error(f"Base data initialization failed: {e}")
        raise
'''
def init_base_data(db):
    """初始化基础数据"""
    try:
        # 创建基础角色
        roles = {
            "admin": Role(id="ROLE001", name="Admin"),
            "producer": Role(id="ROLE002", name="Producer"),
            "distributor": Role(id="ROLE003", name="Distributor"),
            "retailer": Role(id="ROLE004", name="Retailer"),
            "consumer": Role(id="ROLE005", name="Consumer")
        }
        
        # 创建基础商品分类
        categories = [
            Category(id=1, name="Fresh Produce"),
            Category(id=2, name="Dairy"),
            Category(id=3, name="Meat"),
            Category(id=4, name="Beverages")
        ]
        
        # 添加到数据库
        for role in roles.values():
            if not db.query(Role).filter(Role.name == role.name).first():
                db.add(role)
        
        for category in categories:
            if not db.query(Category).filter(Category.name == category.name).first():
                db.add(category)
        
        db.commit()
        logger.info("Base data initialized successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Base data initialization failed: {e}")
        raise 
        '''