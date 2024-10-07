from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum, JSON, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base
from .user import User
import enum

class ShipmentStatus(str, enum.Enum):
    """配送状态"""
    in_transit = "in_transit"  # 运输中
    delivered = "delivered"    # 已送达

class Shipment(Base):
    """配送单"""
    __tablename__ = "shipments"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String(50), primary_key=True)
    distributor_id = Column(String(50), ForeignKey("users.id"))
    retailer_id = Column(String(50), ForeignKey("users.id"))
    product_id = Column(String(50), ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(String(20))
    delivery_address = Column(String(200), nullable=True)
    expected_delivery_time = Column(DateTime, nullable=True)
    actual_delivery_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    shipping_data = Column(JSON, nullable=True)
    
    # 关系
    distributor = relationship("User", foreign_keys=[distributor_id])
    retailer = relationship("User", foreign_keys=[retailer_id])
    product = relationship("Product", back_populates="shipments")
    items = relationship("ShipmentItem", back_populates="shipment")
    traces = relationship("ShipTrace", back_populates="shipment")

class ShipmentItem(Base):
    """配送单商品"""
    __tablename__ = "shipment_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    shipment_id = Column(String(50), ForeignKey("shipments.id", ondelete="CASCADE"))
    product_id = Column(String(50), ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Float)
    
    # 关系
    shipment = relationship("Shipment", back_populates="items")
    product = relationship("Product")

class ShipTrace(Base):
    """配送追踪记录"""
    __tablename__ = "shipment_traces"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    shipment_id = Column(String(50), ForeignKey("shipments.id", ondelete="CASCADE"))
    location = Column(String(200))
    temperature = Column(Float)
    humidity = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    shipment = relationship("Shipment", back_populates="traces") 