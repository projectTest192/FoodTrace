from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime, timedelta

from ..db.session import getDb
from ..models import User, Shipment
from ..schemas.shipment import ShipCreate, ShipInfo, ShipTraceInfo, ShipmentCreate, ShipmentUpdate, ShipmentResponse, EnvironmentData, ShipmentStatusUpdate
from ..services.shipment import createShip, getShips, getShipById, ShipmentService
from ..services.trace import addShipTraceInfo
from ..core.auth import getCurrentUser
from ..models.shipment import ShipmentStatus
from ..core.mqtt_handler import redis_client

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"]
)
shipment_service = ShipmentService()

@router.post("/", response_model=ShipmentResponse)
async def create_shipment(
    shipment: ShipmentCreate,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """创建配送单"""
    print(f"Current user role: {current_user.role.name}")  # 调试信息
    print(f"Current user role type: {type(current_user.role)}")  # 调试信息
    
    # 修改判断逻辑
    if not current_user.role or current_user.role.name != "distributor":
        raise HTTPException(
            status_code=403, 
            detail="Only distributor can create shipment"
        )
    
    try:
        # 生成配送单号
        shipment_id = f"SH{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建配送单
        db_shipment = Shipment(
            id=shipment_id,
            product_id=shipment.product_id,
            retailer_id=shipment.retailer_id,
            distributor_id=current_user.id,
            quantity=shipment.quantity,
            status=ShipmentStatus.in_transit,  # 直接设置为运输中
            expected_delivery_time=shipment.expected_delivery_date or (datetime.now() + timedelta(days=1)),
            created_at=datetime.now()
        )
        
        db.add(db_shipment)
        db.commit()
        db.refresh(db_shipment)
        
        return db_shipment
        
    except Exception as e:
        db.rollback()
        print(f"Error creating shipment: {str(e)}")  # 添加错误日志
        raise HTTPException(
            status_code=500,
            detail=f"Could not create shipment: {str(e)}"
        )

@router.get("", response_model=List[ShipmentResponse])
async def get_shipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb)
):
    """获取配送单列表"""
    return shipment_service.get_shipments(db, skip=skip, limit=limit)

@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: int,
    db: Session = Depends(getDb)
):
    """获取配送单详情"""
    return shipment_service.get_shipment(db, shipment_id)

@router.put("/{shipment_id}/status", response_model=ShipmentResponse)
async def update_shipment_status(
    shipment_id: str,
    status_update: ShipmentStatusUpdate,
    db: Session = Depends(getDb)
):
    """更新配送状态"""
    try:
        return await shipment_service.update_status(db, shipment_id, status_update.status)
    except Exception as e:
        print(f"Error updating shipment status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/{shipment_id}/temperature")
async def log_temperature(
    shipment_id: int,
    temperature: float,
    db: Session = Depends(getDb)
):
    """记录配送温度"""
    return shipment_service.update_temperature_log(db, shipment_id, temperature)

@router.post("/{shipId}/trace", response_model=ShipTraceInfo)
async def addShipmentTrace(
    shipId: int,
    traceInfo: dict,
    db: Session = Depends(getDb),
    currUser: User = Depends(getCurrentUser)
):
    """添加物流追溯信息"""
    return await addShipTraceInfo(db, shipId, traceInfo)

@router.post("/{shipment_id}/start")
async def start_shipment(
    shipment_id: int,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """开始配送"""
    return await shipment_service.start_shipment(db, shipment_id)

@router.post("/{shipment_id}/complete")
async def complete_shipment(
    shipment_id: int,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """确认收货"""
    if current_user.role != "retailer":
        raise HTTPException(
            status_code=403,
            detail="Only retailer can confirm delivery"
        )
    
    return await shipment_service.complete_shipment(db, shipment_id)

@router.post("/{shipment_id}/environment")
async def record_environment(
    shipment_id: int,
    data: EnvironmentData,
    db: Session = Depends(getDb)
):
    """记录环境数据"""
    return await shipment_service.record_environment_data(db, shipment_id, data)

@router.get("/{shipment_id}/environment")
async def get_shipment_environment(shipment_id: str):
    """获取配送环境数据"""
    try:
        # 从Redis获取数据
        redis_key = f"shipment:env:{shipment_id}"
        data = redis_client.get(redis_key)
        
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No environment data found"
            )
            
        return json.loads(data)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 

@router.get("/all", response_model=List[ShipmentResponse])
async def get_all_shipments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb)
):
    """获取所有配送单（公开接口）"""
    try:
        return shipment_service.get_all_shipments(db, skip=skip, limit=limit)
    except Exception as e:
        print(f"Error getting all shipments: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )