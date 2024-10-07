from ..db.redis import redisClient
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
from fastapi import HTTPException, status

from ..models.iot import IotData, DeviceInfo
from ..services.trace import addProdTraceInfo
from ..services.blockchain import blockSVC

# Redis键前缀
TEMP_KEY = "temp:"  # 温度数据
HUMID_KEY = "humid:"  # 湿度数据
GPS_KEY = "gps:"  # GPS数据
ALERT_KEY = "alert:"  # 告警状态

def storeIotData(deviceId: str, data: dict):
    redisClient.hmset(f"iot:{deviceId}", data)

def getIotData(deviceId: str):
    return redisClient.hgetall(f"iot:{deviceId}")

async def addSensorData(
    db: Session,
    prodId: int,
    sensorType: str,
    data: Dict[str, Any]
):
    """添加传感器数据"""
    dbData = IotData(
        prodId=prodId,
        sensorType=sensorType,
        data=data,
        createTime=datetime.utcnow()
    )
    
    try:
        # 保存到数据库
        db.add(dbData)
        db.commit()
        db.refresh(dbData)
        
        # 添加到区块链
        await addProdTraceInfo(db, prodId, {
            "type": "sensor_data",
            "sensor": sensorType,
            "data": data,
            "timestamp": dbData.createTime
        })
        
        return dbData
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加传感器数据失败: {str(e)}"
        )

async def addRfidBind(
    db: Session,
    prodId: int,
    rfidId: str
):
    """RFID绑定"""
    try:
        # 添加到区块链
        await addProdTraceInfo(db, prodId, {
            "type": "rfid_bind",
            "rfid_id": rfidId,
            "timestamp": datetime.utcnow()
        })
        return {"prodId": prodId, "rfidId": rfidId}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RFID绑定失败: {str(e)}"
        )

async def addRealTimeData(deviceId: str, dataType: str, data: Dict[str, Any]):
    """添加实时数据到Redis"""
    timestamp = datetime.utcnow().timestamp()
    
    if dataType == "temp_humid":
        # 温湿度数据(30分钟过期)
        redisClient.zadd(f"{TEMP_KEY}{deviceId}", {str(data["temp"]): timestamp})
        redisClient.zadd(f"{HUMID_KEY}{deviceId}", {str(data["humid"]): timestamp})
        redisClient.expire(f"{TEMP_KEY}{deviceId}", 1800)  # 30分钟
        redisClient.expire(f"{HUMID_KEY}{deviceId}", 1800)
        
        # 检查是否超限
        if data["temp"] > 30 or data["temp"] < 0:
            await addAlertEvent(deviceId, "temperature_alert", data)
            
    elif dataType == "gps":
        # GPS数据(24小时过期)
        redisClient.geoadd(f"{GPS_KEY}{deviceId}", 
                          data["longitude"], 
                          data["latitude"], 
                          timestamp)
        redisClient.expire(f"{GPS_KEY}{deviceId}", 86400)  # 24小时
        
    elif dataType == "alert":
        # 告警状态(无过期时间,手动清除)
        redisClient.hset(f"{ALERT_KEY}{deviceId}", 
                        data["alert_type"],
                        data["alert_msg"])

async def addDailyStats(
    db: Session,
    deviceId: str,
    date: datetime,
    stats: Dict[str, Any]
):
    """添加每日统计数据到数据库"""
    dbStats = IotData(
        deviceId=deviceId,
        dataType="daily_stats",
        data=stats,
        createTime=date
    )
    
    try:
        db.add(dbStats)
        db.commit()
        db.refresh(dbStats)
        
        # 添加到区块链
        await addProdTraceInfo(db, dbStats.prodId, {
            "type": "daily_stats",
            "device_id": deviceId,
            "stats": stats,
            "date": date.isoformat()
        })
        
        return dbStats
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加统计数据失败: {str(e)}"
        )

async def addAlertEvent(
    deviceId: str,
    alertType: str,
    data: Dict[str, Any]
):
    """添加告警事件(数据库+区块链)"""
    # 添加到Redis告警状态
    redisClient.hset(f"{ALERT_KEY}{deviceId}", 
                    alertType,
                    str(data))
                    
    # 添加到区块链
    await addProdTraceInfo(None, data["prodId"], {
        "type": "alert_event",
        "device_id": deviceId,
        "alert_type": alertType,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    })

def getRealTimeData(deviceId: str, dataType: str):
    """获取实时数据"""
    if dataType == "temp":
        return redisClient.zrange(f"{TEMP_KEY}{deviceId}", 0, -1, withscores=True)
    elif dataType == "humid":
        return redisClient.zrange(f"{HUMID_KEY}{deviceId}", 0, -1, withscores=True)
    elif dataType == "gps":
        return redisClient.geopos(f"{GPS_KEY}{deviceId}", "*")
    elif dataType == "alert":
        return redisClient.hgetall(f"{ALERT_KEY}{deviceId}") 