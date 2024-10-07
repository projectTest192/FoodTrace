from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base_class import Base
from .product import Product
from .shipment import Shipment  # 添加这行导入

class DeviceInfo(Base):
    """IoT设备信息"""
    __tablename__ = "device_info"
    __table_args__ = {'extend_existing': True}
    
    id = Column(String(50), primary_key=True)
    deviceId = Column(String, unique=True)  # 设备唯一ID
    name = Column(String)
    type = Column(String)         # temp, humidity, gps
    status = Column(String)       # online, offline
    lastOnline = Column(DateTime)
    productId = Column(String(50), ForeignKey("products.id"))  # 确保这里使用正确的表名和列名
    
    # 关系
    data = relationship("IotData", backref="device")
    product = relationship("Product", backref="devices")

class IotData(Base):
    """IoT设备数据"""
    __tablename__ = "iot_data"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    deviceId = Column(String, ForeignKey("device_info.deviceId"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)  # 存储传感器数据

class EnvData(Base):
    __tablename__ = "env_data_daily"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    deviceId = Column(String, ForeignKey("device_info.deviceId"))
    date = Column(DateTime)
    maxTemp = Column(Float)
    minTemp = Column(Float)
    avgTemp = Column(Float)
    maxHumidity = Column(Float)
    minHumidity = Column(Float)
    avgHumidity = Column(Float)
    alertCount = Column(Integer)
    
    # 关系
    device = relationship("DeviceInfo", backref="env_data")

class TraceEvent(Base):
    """追溯事件模型 - 包括产品状态变化、IoT设备事件等"""
    __tablename__ = "trace_events"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    # 关联信息
    productId = Column(String, ForeignKey("products.id"))  # 修改为 String 类型
    deviceId = Column(String, ForeignKey("device_info.deviceId"), nullable=True)
    shipmentId = Column(String, ForeignKey("shipments.id"), nullable=True)  # 修改为 String 类型
    
    # 事件信息
    eventType = Column(String)    # tempAlert, statusChange, qualityIssue, rfid_scan, sensor_alert
    eventData = Column(JSON)      # 事件详细数据
    location = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    blockchainTxHash = Column(String, nullable=True)
    
    # 关系
    product = relationship("Product", backref="trace_events", overlaps="events,product")
    device = relationship("DeviceInfo", backref="trace_events")
    shipment = relationship("Shipment", backref="trace_events")

class RfidBind(Base):
    """RFID绑定信息模型"""
    __tablename__ = "rfid_binds"

    id = Column(Integer, primary_key=True, index=True)
    rfidTag = Column(String, unique=True, index=True)
    productId = Column(Integer, ForeignKey("products.id"))
    bindTime = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # active, inactive

    # 关联
    product = relationship("Product", backref="rfid_binds") 