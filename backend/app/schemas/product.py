from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile
from .base import BaseSchema

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryInDB(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductBase(BaseSchema):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    stock: int
    unit: str

class ProductCreate(BaseModel):
    """产品创建请求模型"""
    name: str
    description: str
    category_id: int
    price: float
    stock: int
    unit: str
    storage_conditions: str
    expiry_date: datetime

class ProductUpdate(BaseModel):
    """更新产品请求模型"""
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    unit: Optional[str] = None

class ProductInfo(BaseModel):
    """产品详细信息"""
    id: str
    name: str
    description: str
    manufacturer: str
    category: str
    price: float
    stock: int
    unit: str
    created_at: datetime
    trace_info: Optional[dict] = None

class ProductFactoryData(BaseModel):
    rfid_code: str
    iot_data: Dict[str, Any]

class ProductStockUpdate(BaseModel):
    quantity: float
    operation: str  # "in" or "out"

class TraceCreate(BaseModel):
    trace_code: str
    batch_no: str
    trace_data: Dict[str, Any]

class TraceInfo(TraceCreate):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    """产品响应模型"""
    id: str  # 改为字符串类型
    name: str
    description: Optional[str] = None
    category_id: int
    producer_id: str  # 改为字符串类型
    price: float
    stock: int
    unit: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class IoTDataCreate(BaseModel):
    """IoT数据创建请求模型"""
    device_id: str
    rfid_id: str
    temperature: float
    humidity: float
    latitude: float
    longitude: float

class IoTDataResponse(IoTDataCreate):
    """IoT数据响应模型"""
    id: str
    product_id: str
    blockchain_hash: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True 