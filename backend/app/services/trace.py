from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import Dict, Any, List

from .blockchain import blockSVC
from .product import ProductService
from .shipment import getShipById
from ..models.product import ProdTrace
from ..models.shipment import ShipTrace, Shipment

productSvc = ProductService()

async def addProdTraceInfo(
    db: Session, 
    prodId: int,
    traceInfo: Dict[str, Any]
) -> ProdTrace:
    """添加产品追溯信息"""
    # 检查产品是否存在
    product = productSvc.getProdById(db, prodId)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # 添加区块
    block = blockSVC.addBlock({
        "type": "product",
        "prodId": prodId,
        "info": traceInfo,
        "timestamp": datetime.utcnow()
    })
    
    # 保存追溯记录
    dbTrace = ProdTrace(
        prodId=prodId,
        blockId=block.blockId,
        traceInfo=traceInfo,
        createTime=block.timestamp
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

async def addShipTraceInfo(
    db: Session, 
    shipment_id: str, 
    trace_data: Dict[str, Any]
) -> bool:
    """添加运输追踪信息"""
    try:
        # 1. 获取运输单
        shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
        if not shipment:
            return False
            
        # 2. 准备区块链数据
        blockchain_data = {
            "shipment_id": shipment_id,
            "product_id": shipment.product_id,
            "timestamp": datetime.now().isoformat(),
            "location": trace_data.get("location"),
            "temperature": trace_data.get("temperature"),
            "humidity": trace_data.get("humidity"),
            "status": trace_data.get("status", "in_transit")
        }
        
        # 3. 上传到区块链
        await blockSVC.upload_product_data(blockchain_data)
        
        # 4. 更新运输单状态
        shipment.current_location = trace_data.get("location")
        shipment.status = trace_data.get("status", "in_transit")
        db.commit()
        
        return True
    except Exception as e:
        print(f"Error adding trace info: {e}")
        db.rollback()
        return False 