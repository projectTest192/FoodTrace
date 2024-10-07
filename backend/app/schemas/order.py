from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from ..models.order import OrderStatus

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    retailer_id: str
    items: List[OrderItemCreate]

class OrderItemResponse(OrderItemCreate):
    id: int
    unit_price: float
    
    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    """订单状态更新模型"""
    status: OrderStatus

class OrderResponse(BaseModel):
    """订单响应模型"""
    id: str
    consumer_id: str
    retailer_id: str
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    completed_at: Optional[datetime]
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True 