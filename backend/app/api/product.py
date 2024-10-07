from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, status, Query, Body
from sqlalchemy.orm import Session
from ..db.session import SessionLocal, getDb
from ..models.product import Product, Category, ProductIoTData, ProductPrice
from ..models.shipment import Shipment, ShipTrace
from ..schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    ProductInfo, 
    CategoryCreate, 
    CategoryInDB, 
    ProductFactoryData, 
    TraceCreate,
    TraceInfo,
    ProductResponse,
    IoTDataCreate,
    IoTDataResponse
)
from datetime import datetime
from typing import List, Optional
from ..services.product import ProductService
import shutil
import os
from pathlib import Path
from ..models.user import User
from ..core.auth import getCurrentUser
import time
import random
from decimal import Decimal
import json
import re
from ..services.blockchain import BlockchainService
from sqlalchemy import or_

router = APIRouter(
    prefix="/products",
    tags=["products"]
)
product_service = ProductService()
blockchain_service = BlockchainService()

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 创建上传目录
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

def secure_filename(filename: str) -> str:
    """
    安全化文件名
    """
    # 移除非法字符
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    # 确保文件名不以点开头
    while filename and filename[0] == '.':
        filename = filename[1:]
    # 如果文件名为空，使用默认名称
    if not filename:
        filename = 'file'
    return filename

@router.get("/prodList", response_model=List[ProductResponse])
async def get_products(
    producer_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """获取产品列表"""
    try:
        print(f"Getting products for user: {current_user.email}, role: {current_user.role.name}")  # 调试信息
        
        if producer_id:
            # 获取指定生产商的产品
            products = await product_service.get_producer_products(
                db, 
                producer_id=producer_id,
                skip=skip,
                limit=limit
            )
        else:
            # 获取所有产品
            products = await product_service.get_products(
                db,
                skip=skip,
                limit=limit
            )
            
        if not products:
            return []  # 返回空列表而不是404错误
            
        return products
        
    except Exception as e:
        print(f"Error getting products: {str(e)}")  # 调试信息
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/", response_model=ProductResponse)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    stock: int = Form(...),
    unit: str = Form(...),
    expiry_date: str = Form(...),
    storage_conditions: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """创建产品"""
    try:
        if current_user.role_id != 2:  # 2是生产商角色ID
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only producers can create products"
            )
        
        # 处理图片上传
        image_url = None
        if image:
            # 确保文件名安全
            timestamp = int(time.time())
            safe_filename = f"{timestamp}_{secure_filename(image.filename)}"
            file_path = UPLOAD_DIR / safe_filename
            
            # 保存文件
            try:
                contents = await image.read()
                with open(file_path, "wb") as f:
                    f.write(contents)
                image_url = f"/static/uploads/{safe_filename}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error uploading file: {str(e)}"
                )
        
        # 创建产品数据
        product_data = {
            "name": name,
            "description": description,
            "price": price,
            "category_id": category_id,
            "stock": stock,
            "unit": unit,
            "image_url": image_url,
            "producer_id": current_user.id,
            "status": "created",
            "batch_number": f"BATCH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "production_date": datetime.now(),
            "expiry_date": datetime.fromisoformat(expiry_date.replace('Z', '+00:00')),
            "storage_conditions": storage_conditions
        }
        
        # 打印调试信息
        print(f"Creating product with data: {product_data}")
        
        return await product_service.create_product(db, product_data)
        
    except Exception as e:
        print(f"Error in create_product: {str(e)}")  # 添加错误日志
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/products/{product_id}", response_model=ProductInfo)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """更新产品"""
    if current_user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only producers can update products"
        )
    return await product_service.update_product(db, product_id, product_data)

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """删除产品"""
    if current_user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only producers can delete products"
        )
    await product_service.delete_product(db, product_id)
    return {"message": "Product deleted successfully"}



@router.get("/products/{product_id}/history")
async def get_product_history(product_id: int, db: Session = Depends(getDb)):
    history = await product_service.get_product_history(product_id, db)
    if not history:
        raise HTTPException(status_code=404, detail="Product history not found")
    return history

@router.put("/products/{productId}/status")
async def updateProductStatus(
    productId: int, 
    status: str,  # 限定可选值: "active", "sold", "inactive"
    db: Session = Depends(getDb)
):
    """更新产品状态"""
    dbProduct = db.query(Product).filter(Product.id == productId).first()
    if not dbProduct:
        raise HTTPException(status_code=404, detail="Product not found")
        
    # 验证状态转换是否合法
    valid_transitions = {
        "active": ["sold", "inactive"],
        "sold": ["inactive"],
        "inactive": []
    }
    
    if status not in valid_transitions.get(dbProduct.status, []):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status transition from {dbProduct.status} to {status}"
        )
    
    # 记录状态变更到区块链
    try:
        await addProdTraceInfo(db, productId, {
            "type": "status_change",
            "from": dbProduct.status,
            "to": status,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # 更新数据库状态
        dbProduct.status = status
        db.commit()
        return {"message": "Product status updated successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categories", response_model=CategoryInDB)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(getDb)
):
    """创建商品分类"""
    return product_service.create_category(db, category)

@router.get("/categories", response_model=List[CategoryInDB])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb)
):
    """获取所有分类"""
    return product_service.get_categories(db, skip=skip, limit=limit)

@router.get("/categories/{category_id}", response_model=CategoryInDB)
def get_category(
    category_id: int,
    db: Session = Depends(getDb)
):
    """获取单个分类"""
    category = product_service.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=CategoryInDB)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(getDb)
):
    """更新商品分类"""
    return product_service.update_category(db, category_id, category)

@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(getDb)
):
    """删除商品分类"""
    product_service.delete_category(db, category_id)
    return {"message": "Category deleted successfully"}

@router.post("/stock")
def update_stock(
    product_id: int,
    warehouse_id: int,
    quantity: int,
    operation: str,  # "in" 或 "out"
    db: Session = Depends(getDb)
):
    """更新商品库存"""
    return product_service.update_stock(
        db, product_id, warehouse_id, quantity, operation
    )

@router.get("/stock/{product_id}")
def get_product_stock(
    product_id: int,
    db: Session = Depends(getDb)
):
    """获取商品库存"""
    return product_service.get_product_stock(db, product_id)

@router.get("/public", response_model=List[ProductResponse])
async def get_public_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(getDb)
):
    """获取所有产品（公开接口）"""
    try:
        # 构建查询
        products = db.query(Product).all()  # 简化查询逻辑
        
        if not products:
            return []  # 如果没有产品，返回空列表
            
        return products
        
    except Exception as e:
        print(f"Error getting products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: Session = Depends(getDb)
):
    """获取产品详情（公开接口）"""
    try:
        # 移除多余的空格
        product_id = product_id.strip()
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=404, 
                detail=f"Product {product_id} not found"
            )
        return product
        
    except Exception as e:
        print(f"Error getting product {product_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/{product_id}/iot-data", response_model=IoTDataResponse)
async def receive_iot_data(
    product_id: str,
    iot_data: IoTDataCreate,
    db: Session = Depends(getDb)
):
    """接收产品IoT数据（无需认证）"""
    try:
        print(f"Receiving IoT data for product {product_id}: {iot_data.dict()}")
        
        updated_product = await product_service.update_product_iot_data(
            db=db,
            product_id=product_id,
            iot_data=iot_data.dict()
        )
        
        return updated_product
    except Exception as e:
        print(f"Error processing IoT data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/list", response_model=List[ProductResponse])
async def get_product_list(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """获取商品列表（经销商专用）"""
    try:
        if not current_user.role or current_user.role.name != "distributor":
            raise HTTPException(
                status_code=403,
                detail="Only distributor can access this endpoint"
            )
            
        # 构建查询
        query = db.query(Product)
        
        # 应用过滤条件
        if category_id:
            query = query.filter(Product.category_id == category_id)
            
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%")
                )
            )
        
        # 获取总数
        total = query.count()
        
        # 应用分页
        products = query.offset(skip).limit(limit).all()
        
        # 构建响应
        return {
            "total": total,
            "items": products,
            "page": skip // limit + 1,
            "size": limit
        }
        
    except Exception as e:
        print(f"Error getting product list: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.put("/{product_id}/price")
async def set_product_price(
    product_id: str,
    price_data: dict = Body(...),
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """设置产品价格（零售商专用）"""
    try:
        print(f"Setting price for product {product_id}: {current_user.role.name}")
        if not current_user.role or current_user.role.name != "retailer":
            raise HTTPException(
                status_code=403,
                detail="Only retailer can set product price"
            )
            
        # 获取产品
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        try:
            price = Decimal(str(price_data["price"]))  # 安全地转换价格
        except (KeyError, ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail="Invalid price value"
            )
            
        # 创建或更新价格记录
        price_record = db.query(ProductPrice).filter(
            ProductPrice.product_id == product_id,
            ProductPrice.retailer_id == current_user.id
        ).first()
        
        if not price_record:
            price_record = ProductPrice(
                product_id=product_id,
                retailer_id=current_user.id,
                price=price,
                updated_at=datetime.now()
            )
            db.add(price_record)
        else:
            price_record.price = price
            price_record.updated_at = datetime.now()
            
        db.commit()
        
        return {
            "message": "Price updated successfully",
            "product_id": product_id,
            "price": float(price),
            "retailer_id": current_user.id
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error setting price: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/retailer/{retailer_id}", response_model=List[dict])
async def get_retailer_products(
    retailer_id: str,
    db: Session = Depends(getDb)
):
    """获取指定零售商的商品列表（包含零售商价格）"""
    try:
        # 查询所有有该零售商价格记录的产品
        products = db.query(Product, ProductPrice)\
            .join(ProductPrice, Product.id == ProductPrice.product_id)\
            .filter(ProductPrice.retailer_id == retailer_id)\
            .all()
            
        if not products:
            return []
            
        result = []
        for product, price in products:
            result.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "category_id": product.category_id,
                "producer": product.producer.username if product.producer else None,
                "production_date": product.production_date,
                "expiry_date": product.expiry_date,
                "storage_conditions": product.storage_conditions,
                "status": product.status,
                "price": float(price.price),  # 使用零售商设置的价格
                "image_url": product.image_url
            })
            
        return result
        
    except Exception as e:
        print(f"Error getting retailer products: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/{product_id}/trace", response_model=dict)
async def get_product_trace(
    product_id: str,
    db: Session = Depends(getDb)
):
    """获取产品追溯信息（公开接口）"""
    try:
        # 获取产品基本信息
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
            
        # 获取生产信息
        production_info = {
            "producer": product.producer.username,
            "batch_number": product.batch_number,
            "production_date": product.production_date,
            "expiry_date": product.expiry_date
        }
        
        # 获取IoT数据
        iot_data = db.query(ProductIoTData).filter(
            ProductIoTData.product_id == product_id
        ).first()
        
        # 将 IoT 数据转换为字典
        iot_data_dict = None
        if iot_data:
            iot_data_dict = {
                "id": iot_data.id,
                "product_id": iot_data.product_id,
                "temperature": iot_data.temperature,
                "humidity": iot_data.humidity,
                "latitude": iot_data.latitude,
                "longitude": iot_data.longitude,
                "timestamp": iot_data.created_at,
                "device_id": iot_data.device_id
            }
        
        # 获取物流信息
        shipments = db.query(Shipment)\
            .filter(Shipment.product_id == product_id)\
            .all()
            
        shipping_info = []
        for shipment in shipments:
            ship_data = {
                "shipment_id": shipment.id,
                "distributor": shipment.distributor.username,
                "retailer": shipment.retailer.username,
                "status": shipment.status,
                "created_at": shipment.created_at,
                "delivered_at": shipment.actual_delivery_time
            }
            
            # 获取运输过程中的环境数据
            traces = db.query(ShipTrace)\
                .filter(ShipTrace.shipment_id == shipment.id)\
                .order_by(ShipTrace.created_at)\
                .all()
                
            ship_data["traces"] = [
                {
                    "location": trace.location,
                    "temperature": trace.temperature,
                    "humidity": trace.humidity,
                    "timestamp": trace.created_at
                }
                for trace in traces
            ]
            
            shipping_info.append(ship_data)
        
        # 构建完整的追溯信息
        trace_info = {
            "product_info": {
                "id": product.id,
                "name": product.name,
                "category": product.category.name,
                "storage_conditions": product.storage_conditions
            },
            "production_info": production_info,
            "iot_data": iot_data_dict,  # 使用转换后的字典
            "shipping_info": shipping_info,
            "blockchain_hash": product.blockchain_hash
        }
        
        return trace_info
        
    except Exception as e:
        print(f"Error getting product trace: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 