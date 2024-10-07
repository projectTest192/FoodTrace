from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from decimal import Decimal

from ..db.session import getDb
from ..models.user import User
from ..models.product import Product, ProductPrice
from ..models.order import Order, OrderItem, OrderStatus
from ..schemas.order import OrderCreate, OrderResponse, OrderItemCreate, OrderStatusUpdate
from ..core.auth import getCurrentUser

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """创建订单"""
    try:
        # 验证零售商
        retailer = db.query(User).filter(User.id == order.retailer_id).first()
        if not retailer or retailer.role.name != "retailer":
            raise HTTPException(
                status_code=404,
                detail="Retailer not found"
            )
            
        # 计算总金额
        total_amount = Decimal('0.0')
        order_items = []
        
        for item in order.items:
            # 获取产品
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product {item.product_id} not found"
                )
                
            # 获取零售商价格
            price_record = db.query(ProductPrice).filter(
                ProductPrice.product_id == item.product_id,
                ProductPrice.retailer_id == order.retailer_id
            ).first()
            
            if not price_record:
                raise HTTPException(
                    status_code=400,
                    detail=f"No price set for product {item.product_id}"
                )
                
            # 检查库存
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient stock for product {item.product_id}"
                )
                
            # 计算商品总价
            item_total = Decimal(str(price_record.price)) * Decimal(str(item.quantity))
            total_amount += item_total
            
            # 创建订单项
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=price_record.price
                )
            )
            
            # 更新库存
            product.stock -= item.quantity
            
        # 创建订单
        db_order = Order(
            id=f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            consumer_id=current_user.id,
            retailer_id=order.retailer_id,
            total_amount=total_amount,
            status="pending",
            created_at=datetime.now(),
            items=order_items
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        return db_order
        
    except Exception as e:
        db.rollback()
        print(f"Error creating order: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/my-orders", response_model=List[OrderResponse])
async def get_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """获取当前用户的订单"""
    try:
        print(f"Getting orders for user: {current_user.id}")
        orders = db.query(Order)\
            .filter(Order.consumer_id == current_user.id)\
            .offset(skip)\
            .limit(limit)\
            .all()
            
        return orders
    except Exception as e:
        print(f"Error getting orders: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: str,
    status_update: OrderStatusUpdate,
    db: Session = Depends(getDb),
    current_user: User = Depends(getCurrentUser)
):
    """更新订单状态（确认取餐）"""
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )
            
        # 验证权限（只有消费者本人或零售商可以更新状态）
        if current_user.id != order.consumer_id and current_user.id != order.retailer_id:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
            
        # 只能将订单标记为已完成
        if status_update.status != OrderStatus.completed:
            raise HTTPException(
                status_code=400,
                detail="Invalid status update"
            )
            
        # 更新状态
        order.status = status_update.status
        order.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(order)
        
        return order
        
    except Exception as e:
        db.rollback()
        print(f"Error updating order status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 