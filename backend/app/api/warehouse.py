from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..db.session import getDb
from ..services.warehouse import WarehouseService
from ..schemas.warehouse import WarehouseCreate, WarehouseUpdate, WarehouseInDB
from typing import List
from ..models import Warehouse, Product, Category  # 如果有引用，使用 Category

router = APIRouter()
warehouse_service = WarehouseService()

@router.post("", response_model=WarehouseInDB)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(getDb)
):
    """创建仓库"""
    return warehouse_service.create_warehouse(db, warehouse)

@router.get("", response_model=List[WarehouseInDB])
def get_warehouses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb)
):
    """获取仓库列表"""
    return warehouse_service.get_warehouses(db, skip=skip, limit=limit)

@router.get("/{warehouse_id}", response_model=WarehouseInDB)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(getDb)
):
    """获取单个仓库"""
    warehouse = warehouse_service.get_warehouse(db, warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse

@router.put("/{warehouse_id}", response_model=WarehouseInDB)
def update_warehouse(
    warehouse_id: int,
    warehouse: WarehouseUpdate,
    db: Session = Depends(getDb)
):
    """更新仓库"""
    return warehouse_service.update_warehouse(db, warehouse_id, warehouse)

@router.delete("/{warehouse_id}")
def delete_warehouse(
    warehouse_id: int,
    db: Session = Depends(getDb)
):
    """删除仓库"""
    warehouse_service.delete_warehouse(db, warehouse_id)
    return {"message": "Warehouse deleted successfully"}

@router.get("/{warehouse_id}/stock")
def get_warehouse_stock(
    warehouse_id: int,
    db: Session = Depends(getDb)
):
    """获取仓库库存"""
    return warehouse_service.get_warehouse_stock(db, warehouse_id) 