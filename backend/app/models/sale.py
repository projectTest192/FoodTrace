from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base
import enum

class Sale(Base):
    """销售记录"""
    __tablename__ = "sales"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String(50), primary_key=True)
    retailer_id = Column(Integer, ForeignKey("users.id"))
    sale_date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    status = Column(String, default="completed")
    
    # 关系
    items = relationship("SaleItem", back_populates="sale")
    retailer = relationship("User")

class SaleItem(Base):
    """销售项目"""
    __tablename__ = "sale_items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    # 关系
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product") 