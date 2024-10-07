from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.order import Order, OrderItem, OrderStatus
from ..models.user import User
from ..models.product import Product, ProductStock
from ..schemas.sale import OrderCreate
from datetime import datetime

class SaleService:
    def get_retailers(self, db: Session):
        """获取所有零售点列表"""
        retailers = db.query(User).filter(User.role == "retailer").all()
        return [
            {
                "id": retailer.id,
                "name": retailer.name,
                "address": retailer.addr,
                "contact_name": retailer.contName,
                "contact_phone": retailer.contPhone,
                "outlet_type": retailer.extra_info.get("outlet_type", ""),
                "service_hours": retailer.extra_info.get("service_hours", "")
            }
            for retailer in retailers
        ]

    def get_retailer_products(self, db: Session, retailer_id: int):
        """获取零售点的商品列表"""
        # 获取该零售点的库存记录
        stocks = db.query(ProductStock).filter(
            ProductStock.warehouse_id == retailer_id
        ).all()
        
        return [
            {
                "id": stock.product.id,
                "name": stock.product.name,
                "description": stock.product.description,
                "price": stock.product.current_price,
                "stock": stock.quantity,
                "image_url": stock.product.image_url
            }
            for stock in stocks
            if stock.quantity > 0  # 只返回有库存的商品
        ]

    def create_order(self, db: Session, retailer_id: int, order_data: OrderCreate):
        """创建订单"""
        # 计算总金额
        total_amount = sum(item.quantity * item.unit_price for item in order_data.items)
        
        # 创建订单
        db_order = Order(
            consumer_id=order_data.consumer_id,
            retailer_id=retailer_id,
            total_amount=total_amount,
            payment_method=order_data.payment_method
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # 添加订单项目
        for item in order_data.items:
            # 检查库存
            stock = db.query(ProductStock).filter(
                ProductStock.warehouse_id == retailer_id,
                ProductStock.product_id == item.product_id
            ).first()
            
            if not stock or stock.quantity < item.quantity:
                db.rollback()
                raise HTTPException(
                    status_code=400,
                    detail=f"Product {item.product_id} insufficient stock"
                )
            
            # 创建订单项
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            db.add(db_item)
            
            # 更新库存
            stock.quantity -= item.quantity
            
        db.commit()
        return db_order

    def get_retailer_orders(self, db: Session, retailer_id: int, skip: int = 0, limit: int = 100):
        """获取零售点的订单列表"""
        return db.query(Order).filter(
            Order.retailer_id == retailer_id
        ).offset(skip).limit(limit).all()

    def update_order_status(self, db: Session, order_id: int, status: OrderStatus):
        """更新订单状态"""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
            
        order.status = status
        if status == OrderStatus.paid:
            order.payment_time = datetime.utcnow()
        elif status == OrderStatus.completed:
            order.complete_time = datetime.utcnow()
            
        db.commit()
        db.refresh(order)
        return order 