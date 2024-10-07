from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..db.session import get_db
from sqlalchemy.orm import Session
from ..blockchain.ethereum import BlockchainService

router = APIRouter()
blockchain = BlockchainService()

@router.get("/info/{rfid_id}")
def get_rfid_info(rfid_id: str, db: Session = Depends(get_db)) -> Dict[Any, Any]:
    """
    获取RFID绑定的商品信息和区块链数据
    """
    try:
        # 1. 从数据库获取RFID绑定信息
        rfid_bind = db.query(RFIDBind).filter(RFIDBind.rfid_id == rfid_id).first()
        if not rfid_bind:
            raise HTTPException(status_code=404, detail="RFID not found")
            
        # 2. 获取关联的商品信息
        product = db.query(Product).filter(Product.id == rfid_bind.product_id).first()
        
        # 3. 获取区块链溯源信息
        blockchain_data = blockchain.get_product_trace(rfid_id)
        
        return {
            "rfid_id": rfid_id,
            "product": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "manufacturer": product.manufacturer,
                "production_date": product.production_date.isoformat(),
                "expiry_date": product.expiry_date.isoformat()
            },
            "blockchain": blockchain_data,
            "bind_time": rfid_bind.created_at.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 