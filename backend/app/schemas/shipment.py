from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from ..models.shipment import ShipmentStatus
from enum import Enum

class ShipmentStatus(str, Enum):
    in_transit = "in_transit"  # 运输中
    delivered = "delivered"    # 已送达

class ShipmentBase(BaseModel):
    shipment_no: str
    distributor_id: int
    receiver_id: int

class ShipmentCreate(BaseModel):
    """简化的配送单创建模型"""
    product_id: str
    retailer_id: str
    quantity: int
    expected_delivery_date: Optional[datetime] = None

class ShipmentUpdate(BaseModel):
    status: Optional[str] = None
    delivered_at: Optional[datetime] = None

class ShipmentItemBase(BaseModel):
    product_id: int
    quantity: float

class ShipmentItemCreate(ShipmentItemBase):
    pass

class ShipmentItemInfo(ShipmentItemBase):
    id: int
    shipment_id: int

    class Config:
        from_attributes = True

class ShipTraceBase(BaseModel):
    location: str
    temperature: float
    humidity: float

class ShipTraceCreate(ShipTraceBase):
    shipment_id: int

class ShipTraceInfo(ShipTraceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ShipmentInfo(ShipmentBase):
    id: int
    status: str
    created_at: datetime
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    items: List[ShipmentItemInfo]
    traces: List[ShipTraceInfo]

    class Config:
        from_attributes = True

class ShipBase(BaseModel):
    """物流基础模型"""
    prodId: int
    fromAddr: str
    toAddr: str
    carrier: str

class ShipCreate(ShipBase):
    """物流创建模型"""
    pass

class ShipUpdate(ShipBase):
    """物流更新模型"""
    pass

class ShipInfo(ShipBase):
    """物流信息模型"""
    id: int
    userId: int
    createTime: datetime
    status: str
    traceInfo: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class ShipmentItemResponse(ShipmentItemCreate):
    id: int
    shipment_id: int

    class Config:
        from_attributes = True

class ShipmentResponse(BaseModel):
    """配送单响应模型"""
    id: str
    product_id: str
    retailer_id: str
    distributor_id: str
    quantity: int
    status: ShipmentStatus
    created_at: datetime
    expected_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    environment_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class EnvironmentData(BaseModel):
    """环境数据模型"""
    temperature: float
    humidity: float
    latitude: float
    longitude: float
    timestamp: datetime

class ShipmentStatusUpdate(BaseModel):
    """配送状态更新模型"""
    status: ShipmentStatus

class ShipmentResponse(BaseModel):
    """配送单响应模型"""
    id: str
    product_id: str
    retailer_id: str
    distributor_id: str
    quantity: int
    status: ShipmentStatus
    created_at: datetime
    expected_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    environment_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True 