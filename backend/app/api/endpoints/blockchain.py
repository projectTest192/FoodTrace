from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.core.deps import get_current_user
from app.schemas.blockchain import ProductTrace, RFIDWrite, EnvironmentData
from app.core.blockchain import BlockchainClient

router = APIRouter()
blockchain = BlockchainClient()

@router.post("/products/trace", response_model=ProductTrace)
async def create_product_trace(
    product_id: str,
    current_user = Depends(get_current_user)
):
    """创建产品追溯记录"""
    try:
        return await blockchain.create_product_trace(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rfid/write")
async def write_rfid(
    data: RFIDWrite,
    current_user = Depends(get_current_user)
):
    """记录RFID写入"""
    try:
        return await blockchain.record_rfid_write(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/environment/record")
async def record_environment(
    data: EnvironmentData,
    current_user = Depends(get_current_user)
):
    """记录环境数据"""
    try:
        return await blockchain.record_environment(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 