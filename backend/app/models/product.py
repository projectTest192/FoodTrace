from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Table, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from decimal import Decimal  # 从Python标准库导入Decimal
from ..db.base_class import Base  # 使用 base_class 中的 Base
from .user import User

class Category(Base):
    """商品分类"""
    __tablename__ = "categories"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    
    # 关系
    products = relationship("Product", back_populates="category")
    children = relationship("Category", backref="parent", remote_side=[id])

class Product(Base):
    """产品基本信息"""
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock = Column(Integer, nullable=False, default=0)
    unit = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String, nullable=True)
    producer_id = Column(String, ForeignKey("users.id"))
    status = Column(String)  # created/active/shipping/retail/sold
    batch_number = Column(String)
    production_date = Column(DateTime)
    expiry_date = Column(DateTime)
    storage_conditions = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
    device_id = Column(String, nullable=True)
    rfid_code = Column(String, nullable=True)
    blockchain_hash = Column(String, nullable=True)
    
    # 关系
    producer = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")
    shipments = relationship("Shipment", back_populates="product")
    prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")
    traces = relationship("ProdTrace", back_populates="product")
    stocks = relationship("ProductStock", back_populates="product")
    iot_data = relationship("ProductIoTData", back_populates="product", uselist=False)

class ProductPrice(Base):
    """产品价格表"""
    __tablename__ = "product_prices"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    product_id = Column(String(50), ForeignKey("products.id", ondelete="CASCADE"))
    retailer_id = Column(String(50), ForeignKey("users.id", ondelete="CASCADE"))
    price = Column(DECIMAL(10, 2), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    product = relationship("Product", back_populates="prices")
    retailer = relationship("User")

class ProdTrace(Base):
    """产品追溯信息"""
    __tablename__ = "product_traces"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    trace_code = Column(String, unique=True, index=True)  # 追溯码
    batch_no = Column(String)      # 批次号
    created_at = Column(DateTime, default=datetime.utcnow)
    trace_data = Column(JSON)      # 追溯数据
    
    # 关系
    product = relationship("Product", back_populates="traces")

class ProductStock(Base):
    """商品库存记录"""
    __tablename__ = "product_stocks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Float)
    batch_no = Column(String, nullable=True)
    production_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    product = relationship("Product", back_populates="stocks")

class ProductIoTData(Base):
    """产品IoT数据"""
    __tablename__ = "product_iot_data"
    
    id = Column(String, primary_key=True, default=lambda: f"IOT{datetime.now().strftime('%Y%m%d%H%M%S')}")
    product_id = Column(String, ForeignKey("products.id", ondelete="CASCADE"))
    device_id = Column(String)
    rfid_id = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    blockchain_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    product = relationship("Product", back_populates="iot_data") 