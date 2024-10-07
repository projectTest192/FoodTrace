from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, status
from .. import models, schemas
from ..core.security import getPassHash, verifyPass
from ..core.email import sendEmail
from typing import List, Optional

def getUserByEmail(db: Session, email: str) -> Optional[models.User]:
    """通过邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()

def getUserById(db: Session, userId: int) -> Optional[models.User]:
    """通过ID获取用户"""
    return db.query(models.User).filter(models.User.id == userId).first()

def getUserByPhone(db: Session, phone: str) -> Optional[models.User]:
    """通过手机号获取用户"""
    return db.query(models.User).filter(models.User.phone == phone).first()

def getUserByName(db: Session, name: str) -> Optional[models.User]:
    """通过用户名获取用户"""
    return db.query(models.User).filter(models.User.name == name).first()

def getUsers(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """获取用户列表"""
    return db.query(models.User).offset(skip).limit(limit).all()

def authUser(db: Session, name: str, pwd: str) -> Optional[models.User]:
    """用户认证"""
    user = getUserByName(db, name)
    if not user or not verifyPass(pwd, user.pwd):
        return None
    return user

def createUser(db: Session, userData: schemas.UserCreate, roleName: str) -> models.User:
    """创建新用户"""
    if getUserByEmail(db, userData.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    if userData.phone and getUserByPhone(db, userData.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )
    
    role = db.query(models.Role).filter(models.Role.name == roleName).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"角色 {roleName} 不存在"
        )
    
    dbUser = models.User(
        email=userData.email,
        name=userData.name,
        pwd=getPassHash(userData.password),
        phone=userData.phone,
        roleId=role.id,
        active=True,
        verified=False,
        createTime=datetime.utcnow()
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
            detail=f"创建用户失败: {str(e)}"
        )

def updateUser(db: Session, userId: int, userUpdate: schemas.UserUpdate) -> models.User:
    """更新用户信息"""
    dbUser = getUserById(db, userId)
    if not dbUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    updateData = userUpdate.dict(exclude_unset=True)
    for field, value in updateData.items():
        setattr(dbUser, field, value)
    
    try:
        db.commit()
        db.refresh(dbUser)
        return dbUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户失败: {str(e)}"
        )

def updateEntInfo(db: Session, userId: int, entInfo: schemas.EntInfo) -> models.User:
    """更新企业信息"""
    dbUser = getUserById(db, userId)
    if not dbUser or dbUser.role == "consumer":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="企业用户不存在"
        )
    
    updateData = entInfo.dict(exclude_unset=True)
    for field, value in updateData.items():
        setattr(dbUser, field, value)
    
    try:
        db.commit()
        db.refresh(dbUser)
        return dbUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新企业信息失败: {str(e)}"
        )

def verifyUserEmail(db: Session, email: str) -> models.User:
    """验证用户邮箱"""
    user = getUserByEmail(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    user.verified = True
    try:
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"验证邮箱失败: {str(e)}"
        )

async def sendVerifyEmail(userEmail: str, token: str):
    """发送验证邮件"""
    subject = "验证您的邮箱"
    body = f"""
    <h2>欢迎注册食品溯源系统</h2>
    <p>请点击以下链接验证您的邮箱：</p>
    <p><a href="http://localhost:3000/verify-email?token={token}">验证邮箱</a></p>
    <p>如果不是您本人的操作，请忽略此邮件。</p>
    """
    return await sendEmail(userEmail, subject, body)

def updateUserInfo(db: Session, userId: int, userInfo: schemas.UserInfo):
    dbUser = db.query(models.User).filter(models.User.id == userId).first()
    if not dbUser:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新用户信息
    for key, value in userInfo.dict(exclude_unset=True).items():
        setattr(dbUser, key, value)
    
    db.commit()
    db.refresh(dbUser)
    return dbUser

async def createConsumer(db: Session, userCreate: schemas.ConsumerCreate):
    # 检查邮箱
    if getUserByEmail(db, userCreate.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查手机号
    if userCreate.phone and getUserByPhone(db, userCreate.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )

    # 创建用户
    hashedPwd = getPassHash(userCreate.pwd)
    dbUser = models.User(
        name=userCreate.name,
        email=userCreate.email,
        phone=userCreate.phone,
        pwd=hashedPwd,
        role="consumer",
        createTime=datetime.utcnow()
    )
    
    try:
        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)
        
        # 发送验证邮件
        await sendVerifyEmail(userCreate.email, "sample_token")
        
        return dbUser
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建用户失败: {str(e)}"
        )

def create_user(db: Session, user: schemas.UserCreate, role_name: str) -> models.User:
    """创建新用户"""
    # 检查邮箱是否已存在
    if getUserByEmail(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 获取对应角色
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role {role_name} not found"
        )
    
    # 创建用户
    db_user = models.User(
        email=user.email,
        name=user.name,
        pwd=getPassHash(user.password),
        phone=user.phone,
        roleId=role.id,
        active=True,
        verified=False
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User:
    """更新用户信息"""
    db_user = getUserById(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_user_email(db: Session, email: str) -> models.User:
    """验证用户邮箱"""
    user = getUserByEmail(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.verified = True
    db.commit()
    db.refresh(user)
    return user 