from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Dict

from ..db.session import getDb
from ..core.auth import getCurrentUser, getCurrentAdmin, getCurrentActiveUser
from ..schemas.user import UserCreate, UserInfo, UserUpdate, UserResponse
from ..services.admin import createEnt, verifyEnt, getUsers
from ..models import User, Role, Product, Category
from ..services.auth import verifyUserById

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
async def getUsers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDb),
    currAdmin: User = Depends(getCurrentAdmin)
):
    """管理员获取所有用户列表"""
    if currAdmin.role_id != 1:  # 1 是管理员角色ID
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role_id": user.role_id,
            "is_active": user.is_active,
            "verified": user.verified,
            "created_at": user.created_at,
            "role": user.role.name if user.role else None,  # 只返回角色名称
            "phone": user.phone,
            "company": user.company,
            "bizLic": user.bizLic,
            "bizType": user.bizType,
            "addr": user.addr,
            "contName": user.contName,
            "contPhone": user.contPhone
        } for user in users
    ]

@router.post("/enterprise", response_model=UserInfo)
async def createEnterprise(
    userData: UserCreate,
    db: Session = Depends(getDb),
    currUser: User = Depends(getCurrentUser)
):
    """创建企业用户"""
    return await createEnt(db, userData, currUser.id)

@router.post("/verify/{userId}")
async def verifyEnterprise(
    userId: int,
    db: Session = Depends(getDb),
    currUser: User = Depends(getCurrentUser)
):
    """验证企业用户"""
    return await verifyEnt(db, userId, currUser.id)

@router.put("/users/{user_id}/verify", response_model=UserResponse)
async def verifyUser(
    user_id: str,
    db: Session = Depends(getDb),
    current_admin: User = Depends(getCurrentAdmin)
):
    """管理员验证用户"""
    if not current_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要管理员权限"
        )
    
    try:
        verified_user = await verifyUserById(db, user_id)
        return verified_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 