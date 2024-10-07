from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from ..models.order import OrderStatus

class OrderBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    status: str
    payment_status: Optional[str] = None

class OrderInfo(OrderBase):
    id: int
    order_no: str
    buyer_id: int
    seller_id: int
    total_amount: float
    status: str
    payment_status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    quantity: float
    price: float

class SaleCreate(SaleBase):
    pass

class SaleInfo(SaleBase):
    id: int
    seller_id: int
    buyer_id: int
    sale_time: datetime
    
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemResponse(OrderItemCreate):
    id: int
    order_id: int
    
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    consumer_id: int
    retailer_id: int
    status: OrderStatus
    create_time: datetime
    payment_time: Optional[datetime]
    complete_time: Optional[datetime]
    total_amount: float
    payment_method: str
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True

class RetailerProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image_url: Optional[str]

    class Config:
        from_attributes = True

class RetailerResponse(BaseModel):
    id: int
    name: str
    address: str
    contact_name: str
    contact_phone: str
    outlet_type: str
    service_hours: str

    class Config:
        from_attributes = True 