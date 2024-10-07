from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, JSON, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..db.base_class import Base  # 使用已有的 base_class
from .user import User
from .product import Product

class OrderStatus(str, enum.Enum):
    pending = "pending"     # 已下单
    completed = "completed" # 已完成（已取餐）

class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String(50), primary_key=True)
    consumer_id = Column(String(50), ForeignKey("users.id"))
    retailer_id = Column(String(50), ForeignKey("users.id"))
    total_amount = Column(DECIMAL(10, 2))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # 关系
    consumer = relationship("User", foreign_keys=[consumer_id], backref="consumer_orders")
    retailer = relationship("User", foreign_keys=[retailer_id], backref="retailer_orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    """订单项表"""
    __tablename__ = "order_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    order_id = Column(String(50), ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(String(50), ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(DECIMAL(10, 2))
    
    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product") 