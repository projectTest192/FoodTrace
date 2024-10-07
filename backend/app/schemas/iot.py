from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class DeviceBase(BaseModel):
    deviceId: str
    deviceType: str
    location: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DeviceCreate(DeviceBase):
    """创建设备的请求模型"""
    pass

class DeviceInfo(DeviceBase):
    """设备信息响应模型"""
    id: int
    status: str
    lastActive: Optional[datetime] = None

    class Config:
        from_attributes = True

class IotDataBase(BaseModel):
    deviceId: str
    dataType: str
    value: float
    shipmentId: Optional[int] = None

class IotDataCreate(IotDataBase):
    """创建IoT数据的请求模型"""
    pass

class IotDataInfo(IotDataBase):
    """IoT数据响应模型"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class RfidBindBase(BaseModel):
    rfidTag: str
    productId: int

class RfidBindCreate(RfidBindBase):
    """创建RFID绑定的请求模型"""
    pass

class RfidBindInfo(RfidBindBase):
    """RFID绑定信息响应模型"""
    id: int
    bindTime: datetime
    status: str

    class Config:
        from_attributes = True 