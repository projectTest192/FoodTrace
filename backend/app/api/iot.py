from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db.session import getDb
from ..models import User, DeviceInfo, IotData
from ..schemas.iot import (
    DeviceCreate,
    DeviceInfo,
    IotDataCreate,
    RfidBindInfo
)
from ..services.iot import addSensorData, addRfidBind
from ..core.auth import getCurrentUser

router = APIRouter()

@router.post("/sensor", response_model=IotDataCreate)
async def uploadSensorData(
    data: IotDataCreate,
    db: Session = Depends(getDb),
    currUser: User = Depends(getCurrentUser)
):
    """上传传感器数据"""
    return await addSensorData(db, data)

@router.post("/rfid/bind/{prodId}")
async def bindRfid(
    prodId: int,
    rfidId: str,
    db: Session = Depends(getDb),
    currUser: User = Depends(getCurrentUser)
):
    """RFID绑定"""
    return await addRfidBind(db, prodId, rfidId)