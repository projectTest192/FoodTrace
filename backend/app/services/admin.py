from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import List

from ..models.user import User, Role
from ..schemas.user import UserCreate, UserInfo
from ..core.security import getPassHash
from .user import getUserByEmail

def getUsers(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """获取用户列表"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

async def createEnt(db: Session, userData: UserCreate, adminId: int) -> User:
    """创建企业用户"""
    admin = db.query(User).filter(User.id == adminId).first()
    if not admin or admin.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    if getUserByEmail(db, userData.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    dbUser = User(
        email=userData.email,
        name=userData.name,
        pwd=getPassHash(userData.password),
        phone=userData.phone,
        role="enterprise",
        active=True,
        verified=True,
        createTime=datetime.utcnow(),
        bizLic=userData.bizLic,
        bizType=userData.bizType,
        addr=userData.addr,
        contName=userData.contName,
        contPhone=userData.contPhone
    )

    try:
        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)
        return dbUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建企业用户失败: {str(e)}"
        )

async def verifyEnt(db: Session, userId: int, adminId: int) -> dict:
    """验证企业用户"""
    admin = db.query(User).filter(User.id == adminId).first()
    if not admin or admin.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )

    dbUser = db.query(User).filter(User.id == userId).first()
    if not dbUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    dbUser.verified = True
    try:
        db.commit()
        db.refresh(dbUser)
        return dbUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证企业用户失败: {str(e)}"
        ) 