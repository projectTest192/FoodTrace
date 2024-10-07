from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base
import enum

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE")),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete="CASCADE"))
)

class ROLES:
    ADMIN = "admin"
    PRODUCER = "producer"
    DISTRIBUTOR = "distributor"
    RETAILER = "retailer"
    USER = "user"

class Role(Base):
    """角色"""
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    
    # 关系
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        backref="roles"
    )
    users = relationship("User", back_populates="role")

class Permission(Base):
    """权限"""
    __tablename__ = "permissions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)

class User(Base):
    """用户"""
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, default=lambda: f"USR{datetime.now().strftime('%Y%m%d%H%M%S')}")
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    pwd = Column(String)
    full_name = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 用户信息
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    
    # 企业用户特有字段
    bizLic = Column(String, nullable=True)  # 营业执照
    bizType = Column(String, nullable=True)  # 企业类型
    addr = Column(String, nullable=True)     # 地址
    contName = Column(String, nullable=True)  # 联系人
    contPhone = Column(String, nullable=True) # 联系电话
    extra_info = Column(String, nullable=True)  # 额外信息(JSON)
    
    # 关系
    role = relationship("Role", back_populates="users")
    products = relationship("Product", back_populates="producer")

# 预定义角色和权限
ROLES = {
    'admin': {
        'name': 'Food Safety Manager',
        'description': 'Oxford Brookes University Food Safety Supervisor',
        'permissions': ['*']  # 所有权限
    },
    'producer': {
        'name': 'Campus Food Supplier',
        'description': 'Food and ingredients suppliers for OBU',
        'permissions': [
            'product.create',
            'product.update',
            'quality.create',
            'trace.create',
            'shipment.create'
        ]
    },
    'distributor': {
        'name': 'Campus Food Distributor',
        'description': 'Food distribution and logistics for OBU',
        'permissions': [
            'shipment.create',
            'shipment.update',
            'storage.manage',
            'trace.create',
            'product.read'
        ]
    },
    'retailer': {
        'name': 'Campus Food Outlet',
        'description': 'Campus canteens and food shops in OBU',
        'permissions': [
            'stock.manage',
            'sale.create',
            'food.prepare',
            'trace.create',
            'product.read'
        ]
    },
    'consumer': {
        'name': 'OBU Member',
        'description': 'Oxford Brookes University students and staff',
        'permissions': [
            'food.read',
            'trace.read',
            'feedback.create',
            'retailer.list',    # 查看零售商列表
            'retailer.products', # 查看零售商商品
            'order.create',     # 创建订单
            'order.read'        # 查看订单
        ]
    }
} 