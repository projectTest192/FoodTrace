from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json
import asyncio
import subprocess
import httpx

from ..models.product import (
    Product, 
    ProdTrace, 
    Category, 
    ProductPrice, 
    ProductStock,
    ProductIoTData
)
from ..models.user import User
from ..schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    CategoryCreate,
    ProductFactoryData,
    ProductResponse,
    ProductInfo,
    IoTDataCreate,
    IoTDataResponse
)
# 暂时注释掉区块链相关的导入，因为我们现在不使用区块链
# from ..blockchain.models import BlockData
# from ..blockchain.client import BlockchainClient
from ..db.session import getDb
from ..utils.token import generate_temp_token
from ..core.config import settings

class ProductService:
    def __init__(self):
        # self.blockchain = BlockchainClient()  # 暂时注释掉
        pass

    def getProdById(self, db: Session, prodId: int) -> Product:
        """获取单个产品"""
        prod = db.query(Product).filter(Product.id == prodId).first()
        if not prod:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="产品不存在"
            )
        return prod

    def getProds(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        """获取产品列表"""
        return db.query(Product).offset(skip).limit(limit).all()

    def createProd(self, db: Session, prodData: ProductCreate, userId: int) -> Product:
        """创建产品"""
        dbProd = Product(
            name=prodData.name,
            desc=prodData.desc,
            producerId=userId,
            category=prodData.category,
            price=prodData.price,
            stock=prodData.stock,
            prodDate=prodData.prodDate,
            expDate=prodData.expDate,
            batchNum=prodData.batchNum,
            status="inProd"
        )
        
        try:
            db.add(dbProd)
            db.commit()
            db.refresh(dbProd)
            return dbProd
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"创建产品失败: {str(e)}"
            )

    def updateProd(self, db: Session, prodId: int, prodData: ProductUpdate) -> Product:
        """更新产品"""
        dbProd = self.getProdById(db, prodId)
        
        updateData = prodData.dict(exclude_unset=True)
        for field, value in updateData.items():
            setattr(dbProd, field, value)
        
        try:
            db.commit()
            db.refresh(dbProd)
            return dbProd
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"更新产品失败: {str(e)}"
            )

    def addProdTrace(self, db: Session, prodId: int, traceData: Dict[str, Any]) -> ProdTrace:
        """添加产品追溯信息"""
        dbTrace = ProdTrace(
            prodId=prodId,
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

    async def create_product(self, db: Session, product_data: dict) -> ProductResponse:
        """创建产品"""
        try:
            # 打印输入数据
            print(f"Input product_data: {product_data}")
            
            # 生成产品ID
            product_id = f"PROD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 创建产品实例
            db_product = Product(
                id=product_id,
                name=product_data["name"],
                description=product_data["description"],
                category_id=product_data["category_id"],
                producer_id=product_data["producer_id"],
                price=product_data["price"],
                stock=int(product_data["stock"]),  # 确保转换为整数
                unit=str(product_data["unit"]),    # 确保转换为字符串
                status=product_data["status"],
                batch_number=product_data["batch_number"],
                production_date=product_data["production_date"],
                expiry_date=product_data["expiry_date"],
                storage_conditions=product_data["storage_conditions"],
                image_url=product_data.get("image_url"),
                created_at=datetime.utcnow()
            )
            
            # 打印产品实例数据
            print(f"Product instance before save: stock={db_product.stock}, unit={db_product.unit}")
            
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            
            # 打印保存后的数据
            print(f"Product after save: stock={db_product.stock}, unit={db_product.unit}")
            
            # 创建响应对象
            response = ProductResponse(
                id=str(db_product.id),
                name=db_product.name,
                description=db_product.description,
                category_id=db_product.category_id,
                producer_id=str(db_product.producer_id),
                price=db_product.price,
                stock=db_product.stock,
                unit=db_product.unit,
                created_at=db_product.created_at,
                updated_at=db_product.updated_at
            )
            
            # 打印响应数据
            print(f"Response data: {response.dict()}")
            
            return response
            
        except Exception as e:
            db.rollback()
            print(f"Error in create_product: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def send_to_raspberry_pi(self, data: dict):
        """发送数据到树莓派"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.RASPBERRY_PI_URL}/write-rfid",
                    json=data,
                    timeout=10.0
                )
                return response.json()
        except Exception as e:
            print(f"Error sending data to Raspberry Pi: {e}")
            raise

    async def bind_factory_data(self, db: Session, product_id: int, data: ProductFactoryData) -> Product:
        """绑定出厂数据(RFID和IoT)"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
            
        product.rfid_code = data.rfid_code
        product.status = "active"
        
        # 创建追溯记录
        trace = ProdTrace(
            product_id=product_id,
            trace_code=f"TR{datetime.now().strftime('%Y%m%d%H%M%S')}",
            batch_no=product.batch_number,
            trace_data={
                "type": "factory_data",
                "rfid": data.rfid_code,
                "iot": data.iot_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        db.add(trace)
        db.commit()
        db.refresh(product)
        return product

    async def save_factory_data(self, db: Session, product_id: int, factory_data: dict):
        """保存产品出厂数据"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product.rfid_code = factory_data["rfidId"]
        product.device_id = factory_data["deviceId"]
        product.factory_data = factory_data
        
        db.commit()
        db.refresh(product)
        return product

    async def upload_to_blockchain(self, factory_data: dict) -> bool:
        """上传到区块链（预留）"""
        try:
            # TODO: 实际的区块链上传
            print(f"[Blockchain] Would upload: {json.dumps(factory_data, indent=2)}")
            return True
        except Exception as e:
            print(f"[Blockchain] Error: {str(e)}")
            return False

    async def update_product(self, db: Session, product_id: int, update_data: dict):
        db_product = self.get_product(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")

        # 更新基本信息
        for field, value in update_data.items():
            if hasattr(db_product, field) and value is not None:
                setattr(db_product, field, value)

        # 如果有新价格，创建新的价格记录
        if "price" in update_data:
            # 结束旧价格记录
            current_price = db.query(ProductPrice).filter(
                ProductPrice.product_id == product_id,
                ProductPrice.end_date == None
            ).first()
            if current_price:
                current_price.end_date = datetime.utcnow()

            # 创建新价格记录
            new_price = ProductPrice(
                product_id=product_id,
                price=update_data["price"],
                start_date=datetime.utcnow()
            )
            db.add(new_price)

        db.commit()
        db.refresh(db_product)
        return db_product

    def get_products(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Product).offset(skip).limit(limit).all()

    async def get_product(self, db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def get_product_history(self, product_id: int, db: Session) -> List[dict]:
        """获取产品历史记录
        直接从区块链获取历史记录
        """
        product = self.get_product(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        try:
            # 执行区块链查询命令
            process = await asyncio.create_subprocess_shell(
                f'cd app/blockchain/network && ./scripts/query.sh GetProductHistory "{product.chain_id}"',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Query failed: {stderr.decode()}")
            
            # 解析返回的JSON数据
            history = json.loads(stdout.decode())
            return history
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get history: {str(e)}"
            )

    def create_category(self, db: Session, category_data: CategoryCreate):
        """创建商品分类"""
        db_category = Category(**category_data.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def get_categories(self, db: Session, skip: int = 0, limit: int = 100):
        """获取分类列表"""
        return db.query(Category).offset(skip).limit(limit).all()

    def get_category(self, db: Session, category_id: int):
        """获取单个分类"""
        return db.query(Category).filter(Category.id == category_id).first()

    def update_category(self, db: Session, category_id: int, category: CategoryCreate):
        db_category = self.get_category(db, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        for field, value in category.dict().items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        return db_category

    def delete_category(self, db: Session, category_id: int):
        db_category = self.get_category(db, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # 检查是否有商品使用此分类
        if db_category.products:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete category with associated products"
            )
        
        db.delete(db_category)
        db.commit()

    def delete_product(self, db: Session, product_id: int):
        db_product = self.get_product(db, product_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # 检查是否可以删除（例如：已售出的商品不能删除）
        if db_product.status != "active":
            raise HTTPException(
                status_code=400,
                detail=f"Cannot delete product with status: {db_product.status}"
            )
        
        db.delete(db_product)
        db.commit()

    async def update_stock(self, db: Session, product_id: int, quantity: float, operation: str):
        """更新商品库存"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        stock = ProductStock(
            product_id=product_id,
            quantity=quantity,
            batch_no=product.batch_no,
            production_date=product.production_date,
            expiry_date=product.production_date + timedelta(days=product.shelf_life)
        )
        
        if operation == "in":
            product.quantity += quantity
        elif operation == "out":
            if product.quantity < quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")
            product.quantity -= quantity
        
        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock

    async def get_product_stock(self, db: Session, product_id: int):
        """获取商品库存"""
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        stocks = db.query(ProductStock).filter(
            ProductStock.product_id == product_id
        ).order_by(ProductStock.updated_at.desc()).all()
        
        return {
            "current_quantity": product.quantity,
            "stock_records": stocks
        }

    async def getProds(self, db: Session, skip: int = 0, limit: int = 100):
        """获取产品列表"""
        return db.query(Product).offset(skip).limit(limit).all()

    async def updateProd(self, db: Session, prod_id: int, prod_data: ProductUpdate) -> Product:
        """更新产品"""
        db_product = await self.getProd(db, prod_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        for field, value in prod_data.dict(exclude_unset=True).items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product

    async def deleteProd(self, db: Session, prod_id: int):
        """删除产品"""
        db_product = await self.getProd(db, prod_id)
        if not db_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(db_product)
        db.commit()

    async def bind_iot_data(self, db: Session, product_id: str, iot_data: dict):
        """绑定IoT数据到产品"""
        try:
            # 1. 查找产品
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            # 2. 创建IoT数据记录
            iot_record = ProductIoTData(
                id=f"IOT{datetime.now().strftime('%Y%m%d%H%M%S')}",
                product_id=product_id,
                device_id=iot_data["device_id"],
                rfid_id=iot_data["rfid_id"],
                temperature=iot_data["temperature"],
                humidity=iot_data["humidity"],
                latitude=iot_data["latitude"],
                longitude=iot_data["longitude"]
            )
            
            # 3. 更新产品状态
            product.rfid_code = iot_data["rfid_id"]
            product.device_id = iot_data["device_id"]
            product.status = "active"
            
            db.add(iot_record)
            db.commit()
            
            return product
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def createProduct(
        db: Session, 
        product: ProductCreate, 
        current_user: User
    ) -> ProductResponse:
        """创建产品"""
        if current_user.role_id != 2:  # 确保是生产商
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only manufacturers can create products"
            )
        
        # 生成产品ID
        product_id = f"PROD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        db_product = Product(
            id=product_id,
            name=product.name,
            description=product.description,
            category_id=product.category_id,
            producer_id=current_user.id,
            price=product.price,
            stock=product.stock,  # 确保设置库存
            unit=product.unit,    # 确保设置单位
            status="created",
            batch_number=f"BATCH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            production_date=datetime.utcnow(),
            expiry_date=product.expiry_date,
            storage_conditions=product.storage_conditions,
            created_at=datetime.utcnow()
        )
        
        try:
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            
            return ProductResponse(
                id=str(db_product.id),
                name=db_product.name,
                description=db_product.description,
                category_id=db_product.category_id,
                producer_id=str(db_product.producer_id),
                price=db_product.price,
                stock=db_product.stock,  # 返回库存
                unit=db_product.unit,    # 返回单位
                created_at=db_product.created_at,
                updated_at=db_product.updated_at
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_producer_products(
        self,
        db: Session,
        producer_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductResponse]:
        """获取指定生产商的产品列表"""
        try:
            products = db.query(Product)\
                .filter(Product.producer_id == producer_id)\
                .offset(skip)\
                .limit(limit)\
                .all()
                
            return [
                ProductResponse(
                    id=str(product.id),
                    name=product.name,
                    description=product.description,
                    category_id=product.category_id,
                    producer_id=str(product.producer_id),
                    price=product.price,
                    stock=product.stock,
                    unit=product.unit,
                    created_at=product.created_at,
                    updated_at=product.updated_at
                )
                for product in products
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting producer products: {str(e)}"
            )

    async def get_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProductResponse]:
        """获取所有产品列表"""
        try:
            products = db.query(Product)\
                .offset(skip)\
                .limit(limit)\
                .all()
                
            return [
                ProductResponse(
                    id=str(product.id),
                    name=product.name,
                    description=product.description,
                    category_id=product.category_id,
                    producer_id=str(product.producer_id),
                    price=product.price,
                    stock=product.stock,
                    unit=product.unit,
                    created_at=product.created_at,
                    updated_at=product.updated_at
                )
                for product in products
            ]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error getting products: {str(e)}"
            )

    async def update_product_iot_data(
        self,
        db: Session,
        product_id: str,
        iot_data: dict
    ) -> IoTDataResponse:
        """更新产品IoT数据"""
        try:
            # 查找产品
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found"
                )
            
            # 创建IoT数据记录
            iot_record = ProductIoTData(
                id=f"IOT{datetime.now().strftime('%Y%m%d%H%M%S')}",
                product_id=product_id,
                device_id=iot_data["device_id"],
                rfid_id=iot_data["rfid_id"],
                temperature=iot_data["temperature"],
                humidity=iot_data["humidity"],
                latitude=iot_data["latitude"],
                longitude=iot_data["longitude"],
                created_at=datetime.utcnow()
            )
            
            # 更新产品状态
            product.status = "active"
            product.device_id = iot_data["device_id"]
            product.rfid_code = iot_data["rfid_id"]
            
            # 保存更改
            db.add(iot_record)
            db.commit()
            db.refresh(iot_record)
            
            return IoTDataResponse(
                id=iot_record.id,
                product_id=iot_record.product_id,
                device_id=iot_record.device_id,
                rfid_id=iot_record.rfid_id,
                temperature=iot_record.temperature,
                humidity=iot_record.humidity,
                latitude=iot_record.latitude,
                longitude=iot_record.longitude,
                blockchain_hash=iot_record.blockchain_hash,
                created_at=iot_record.created_at
            )
            
        except Exception as e:
            db.rollback()
            print(f"Error updating IoT data: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            ) 