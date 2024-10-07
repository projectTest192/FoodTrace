from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import getDb
from ..services.sale import SaleService
from ..schemas.sale import OrderCreate, OrderResponse
from typing import List
from ..models.order import OrderStatus
from ..models import Sale, SaleItem, Product, Category

router = APIRouter()
sale_service = SaleService()

@router.get("/retailers", response_model=List[dict])
async def get_retailers(
    db: Session = Depends(getDb)
):
    """获取所有零售点列表"""
    return sale_service.get_retailers(db)

@router.get("/retailers/{retailer_id}/products", response_model=List[dict])
async def get_retailer_products(
    retailer_id: int,
    db: Session = Depends(getDb)
):
    """获取零售点的商品列表"""
    return sale_service.get_retailer_products(db, retailer_id)

@router.post("/retailers/{retailer_id}/orders", response_model=OrderResponse)
async def create_order(
    retailer_id: int,
    order: OrderCreate,
    db: Session = Depends(getDb)
):
    """创建订单"""
    return sale_service.create_order(db, retailer_id, order)

@router.get("/retailers/{retailer_id}/orders", response_model=List[OrderResponse])
async def get_retailer_orders(
    retailer_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb)
):
    """获取零售点的订单列表"""
    return sale_service.get_retailer_orders(db, retailer_id, skip, limit)

@router.put("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(getDb)
):
    """更新订单状态"""
    return sale_service.update_order_status(db, order_id, status) 