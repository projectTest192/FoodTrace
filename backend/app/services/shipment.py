from ..db.redis import redisClient
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Optional, Dict, Any

from ..models.shipment import Shipment, ShipTrace, ShipmentItem, ShipmentStatus
from ..schemas.shipment import ShipCreate, ShipUpdate, ShipmentCreate, ShipmentUpdate, EnvironmentData
# 暂时注释掉区块链相关的导入
# from ..blockchain.models import BlockData
from ..models.product import ProductStock

def storeShipmentData(shipmentId: int, data: dict):
    redisClient.hmset(f"shipment:{shipmentId}", data)

def getShipmentData(shipmentId: int):
    return redisClient.hgetall(f"shipment:{shipmentId}")

def getShipById(db: Session, shipId: int) -> Optional[Shipment]:
    """获取单个物流记录"""
    return db.query(Shipment).filter(Shipment.id == shipId).first()

def getShips(db: Session, skip: int = 0, limit: int = 100) -> List[Shipment]:
    """获取物流列表"""
    return db.query(Shipment).offset(skip).limit(limit).all()

async def createShip(db: Session, shipData: dict, userId: int) -> Shipment:
    """创建物流记录"""
    dbShip = Shipment(
        prodId=shipData.prodId,
        fromAddr=shipData.fromAddr,
        toAddr=shipData.toAddr,
        carrier=shipData.carrier,
        userId=userId,
        createTime=datetime.utcnow()
    )
    
    try:
        db.add(dbShip)
        db.commit()
        db.refresh(dbShip)
        return dbShip
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建物流记录失败: {str(e)}"
        )

async def addShipTrace(db: Session, shipId: int, traceData: Dict[str, Any]) -> ShipTrace:
    """添加物流追溯信息"""
    dbTrace = ShipTrace(
        shipId=shipId,
        blockId="",  # 暂时使用空字符串
        traceInfo=traceData,
        createTime=datetime.utcnow()
    )
    
    try:
        db.add(dbTrace)
        db.commit()
        db.refresh(dbTrace)
        return dbTrace
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加追溯信息失败: {str(e)}"
        )

async def create_shipment(db: Session, shipData: ShipCreate, userId: int) -> Shipment:
    """创建物流信息"""
    dbShip = Shipment(
        prodId=shipData.prodId,
        fromAddr=shipData.fromAddr,
        toAddr=shipData.toAddr,
        carrier=shipData.carrier,
        userId=userId,
        createTime=datetime.utcnow()
    )
    
    try:
        db.add(dbShip)
        db.commit()
        db.refresh(dbShip)
        return dbShip
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建物流失败: {str(e)}"
        )

async def get_shipment(db: Session, shipId: int) -> Shipment:
    """获取单个物流信息"""
    ship = db.query(Shipment).filter(Shipment.id == shipId).first()
    if not ship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流信息不存在"
        )
    return ship

async def update_shipment(db: Session, shipId: int, shipData: ShipUpdate) -> Shipment:
    """更新物流信息"""
    ship = db.query(Shipment).filter(Shipment.id == shipId).first()
    if not ship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物流信息不存在"
        )
    
    ship.prodId = shipData.prodId
    ship.fromAddr = shipData.fromAddr
    ship.toAddr = shipData.toAddr
    ship.carrier = shipData.carrier
    
    try:
        db.add(ship)
        db.commit()
        db.refresh(ship)
        return ship
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新物流失败: {str(e)}"
        )

class ShipmentService:
    async def create_shipment(
        self, 
        db: Session, 
        shipment: ShipmentCreate, 
        distributor_id: int
    ):
        """创建配送单"""
        db_shipment = Shipment(
            distributor_id=distributor_id,
            retailer_id=shipment.to_warehouse_id,
            status=ShipmentStatus.created,
            from_address=shipment.from_warehouse.address,
            to_address=shipment.to_warehouse.address,
            contact_name=shipment.contact_name,
            contact_phone=shipment.contact_phone
        )
        db.add(db_shipment)
        db.flush()

        # 创建配送项目
        for item in shipment.items:
            db_item = ShipmentItem(
                shipment_id=db_shipment.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(db_item)

        db.commit()
        db.refresh(db_shipment)
        return db_shipment

    async def start_shipment(self, db: Session, shipment_id: int):
        """开始配送"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        if shipment.status != ShipmentStatus.created:
            raise HTTPException(status_code=400, detail="Invalid status transition")
        
        shipment.status = ShipmentStatus.in_transit
        shipment.start_time = datetime.utcnow()
        
        db.commit()
        db.refresh(shipment)
        return shipment

    async def complete_shipment(self, db: Session, shipment_id: int):
        """完成配送"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        if shipment.status != ShipmentStatus.in_transit:
            raise HTTPException(status_code=400, detail="Invalid status transition")
        
        # 1. 更新状态
        shipment.status = ShipmentStatus.delivered
        shipment.complete_time = datetime.utcnow()
        
        # 2. 增加目标仓库库存
        for item in shipment.items:
            stock = db.query(ProductStock).filter(
                ProductStock.product_id == item.product_id,
                ProductStock.warehouse_id == shipment.retailer_id
            ).first()
            
            if not stock:
                stock = ProductStock(
                    product_id=item.product_id,
                    warehouse_id=shipment.retailer_id,
                    quantity=0
                )
                db.add(stock)
            
            stock.quantity += item.quantity
        
        db.commit()
        db.refresh(shipment)
        return shipment

    async def update_environment_data(
        self, 
        db: Session, 
        shipment_id: int, 
        data: dict
    ):
        """更新环境数据"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        if not shipment.environment_data:
            shipment.environment_data = []
        
        shipment.environment_data.append({
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        })
        
        db.commit()
        return {"status": "success"}

    def update_shipment_status(self, db: Session, shipment_id: int, status: ShipmentStatus):
        """更新配送状态"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
            
        shipment.status = status
        if status == ShipmentStatus.delivered:
            shipment.complete_time = datetime.utcnow()
            
        db.commit()
        db.refresh(shipment)
        return shipment

    def update_temperature_log(self, db: Session, shipment_id: int, temperature: float):
        """更新温度记录"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
            
        if not shipment.temperature_log:
            shipment.temperature_log = []
            
        shipment.temperature_log.append({
            "temperature": temperature,
            "time": datetime.utcnow().isoformat()
        })
        
        db.commit()
        return shipment

    async def record_environment_data(self, db: Session, shipment_id: int, data: EnvironmentData):
        """记录环境数据"""
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        if not shipment.environment_data:
            shipment.environment_data = []
        
        shipment.environment_data.append(data.dict())
        
        db.commit()
        return {"status": "success"} 

    async def update_status(self, db: Session, shipment_id: str, new_status: ShipmentStatus):
        """更新配送状态"""
        try:
            # 获取配送单
            shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
            if not shipment:
                raise HTTPException(
                    status_code=404,
                    detail=f"Shipment {shipment_id} not found"
                )
            
            # 更新状态
            shipment.status = new_status
            
            # 如果状态是已送达，更新送达时间
            if new_status == ShipmentStatus.delivered:
                shipment.actual_delivery_time = datetime.now()
            
            db.commit()
            db.refresh(shipment)
            
            return shipment
            
        except Exception as e:
            db.rollback()
            print(f"Error updating shipment status: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Could not update shipment status: {str(e)}"
            )

    def get_all_shipments(self, db: Session, skip: int = 0, limit: int = 100):
        """获取所有配送单"""
        try:
            return db.query(Shipment)\
                    .order_by(Shipment.created_at.desc())\
                    .offset(skip)\
                    .limit(limit)\
                    .all()
        except Exception as e:
            print(f"Error getting shipments: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Could not get shipments: {str(e)}"
            )