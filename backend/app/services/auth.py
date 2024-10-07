from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..models import User, Role
from ..core.security import (
    getPassHash,
    verifyPass,
    createAccessToken,
    verifyToken,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from ..schemas.auth import UserLogin, Token
from ..schemas.user import UserCreate, UserResponse, DistributorCreate, RetailerCreate, ConsumerCreate
from ..core.email import sendVerifyMail
from ..services.email import sendVerifyEmail
from ..services.user import getUserByEmail
from ..db.session import getDb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email: str, db: Session = next(getDb())) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def authenticate_user(email: str, password: str) -> Optional[User]:
    """验证用户"""
    db = next(getDb())
    user = get_user_by_email(email, db)
    if not user:
        return None
    if not verifyPass(password, user.hashed_password):
        return None
    return user

def createUser(db: Session, email: str, password: str):
    hashedPassword = getPassHash(password)
    dbUser = User(email=email, hashedPassword=hashedPassword)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

async def authenticateUser(db: Session, email: str, password: str) -> Optional[User]:
    """验证用户"""
    user = getUserByEmail(db, email)
    if not user:
        return None
    if not verifyPass(password, user.hashed_password):
        return None
    return user

def getUserByEmail(db: Session, email: str):
    """同步函数：通过邮箱查询用户"""
    return db.query(User).filter(User.email == email).first()

def getUserByPhone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def getUserByName(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def getUserByRole(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()

async def createConsumer(db: Session, userData: ConsumerCreate) -> UserResponse:
    """创建消费者用户"""
    # 检查邮箱是否已注册
    if getUserByEmail(db, userData.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 生成验证 token
    token = createAccessToken(
        data={"sub": userData.email, "type": "email_verify"},
        expires_delta=timedelta(minutes=30)
    )
    
    # 创建用户
    db_user = User(
        username=userData.name,
        email=userData.email,
        pwd=getPassHash(userData.pwd),
        role_id=userData.role_id,
        is_active=True,
        verified=False
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # 发送验证邮件
        await sendVerifyEmail(userData.email, token)
        
        # 转换为响应模型
        return UserResponse(
            id=str(db_user.id),  # 确保转换为字符串
            username=db_user.username,
            email=db_user.email,
            role=getRoleName(db_user.role_id),
            verified=db_user.verified,
            is_active=db_user.is_active,
            phone=db_user.phone,
            company=db_user.company
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def createEnterprise(db: Session, user: UserCreate, adminUser: User):
    if adminUser.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    
    if getUserByEmail(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    if user.phone and getUserByPhone(db, user.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )

    hashedPwd = getPassHash(user.pwd)
    dbUser = User(
        username=user.name,  # 使用 name 作为 username
        email=user.email,
        phone=user.phone,
        pwd=hashedPwd,
        role_id=user.role_id,
        bizLic=user.bizLic,
        bizType=user.bizType,
        addr=user.addr,
        contName=user.contName,
        contPhone=user.contPhone,
        verified=True  # 管理员创建的企业用户默认验证通过
    )
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser

def authUser(db: Session, userLogin: UserLogin) -> Optional[User]:
    """用户认证"""
    user = getUserByEmail(db, userLogin.email)
    if not user or not verifyPass(userLogin.password, user.pwd):
        return None
    return user

def verifyUserEmail(db: Session, email: str) -> dict:
    """验证用户邮箱"""
    # 查找用户
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # 检查是否已验证
    if user.verified:
        return {
            "email": email,
            "verified": True,
            "message": "Email already verified"
        }
    
    try:
        # 更新验证状态
        user.verified = True
        db.commit()
        db.refresh(user)
        
        return {
            "email": email,
            "verified": True,
            "message": "Email verified successfully"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

async def verifyEmailToken(token: str) -> str:
    """验证邮箱令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "emailVerify":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的验证令牌"
            )
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的验证令牌"
            )
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的验证令牌"
        )

async def loginUser(db: Session, userLogin: UserLogin):
    """用户登录"""
    # 查找用户
    user = db.query(User).filter(User.email == userLogin.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 验证密码
    if not verifyPass(userLogin.pwd, user.pwd):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # 检查用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
        
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not verified"
        )
    
    # 获取角色信息
    role = user.role.name if user.role else None
    
    # 生成访问令牌
    access_token = createAccessToken(
        data={"sub": user.email, "role": role}
    )
    
    # 返回登录信息
    return {
        "accToken": access_token,
        "tokenType": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,  # 使用 username 而不是 name
            "full_name": user.full_name,  # 添加 full_name
            "email": user.email,
            "role": role,
            "phone": user.phone,
            "company": user.company,
            "verified": user.verified,
            "is_active": user.is_active
        }
    }

def getRoleName(role_id: int) -> str:
    """根据角色ID获取角色名称"""
    role_map = {
        1: "admin",
        2: "producer",
        3: "distributor",
        4: "retailer",
        5: "consumer"
    }
    return role_map.get(role_id, "unknown")

async def regUser(db: Session, user_data: UserCreate) -> User:
    """注册用户"""
    if getUserByEmail(db, user_data.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 根据角色设置状态
    is_consumer = user_data.role_id == 5
    
    # 创建基本用户数据
    user_dict = {
        "username": user_data.name,
        "email": user_data.email,
        "pwd": getPassHash(user_data.pwd),
        "role_id": user_data.role_id,
        "is_active": True,
        "verified": is_consumer
    }
    
    # 如果是企业用户，添加企业相关字段
    if not is_consumer:
        user_dict.update({
            "bizLic": user_data.bizLic,
            "bizType": user_data.bizType,
            "addr": user_data.addr,
            "contName": user_data.contName,
            "contPhone": user_data.contPhone
        })
    
    db_user = User(**user_dict)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

async def createDistributor(db: Session, user: DistributorCreate) -> User:
    """创建经销商账户"""
    if getUserByEmail(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = User(
        username=user.name,  # 将 name 映射到 username
        email=user.email,
        pwd=getPassHash(user.pwd),
        role_id=user.role_id,
        bizLic=user.bizLic,
        bizType="distributor",
        addr=user.addr,
        contName=user.contName,
        contPhone=user.contPhone,
        verified=False,
        is_active=True,
        extra_info={
            "distribution_area": user.distribution_area,
            "vehicle_info": user.vehicle_info
        }
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    await sendVerifyMail(user.email)
    
    return db_user

async def createRetailer(db: Session, user: RetailerCreate) -> User:
    """创建零售商账户"""
    if getUserByEmail(db, user.email):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    db_user = User(
        username=user.name,  # 将 name 映射到 username
        email=user.email,
        pwd=getPassHash(user.pwd),
        role_id=user.role_id,
        bizLic=user.bizLic,
        bizType="retailer",
        addr=user.addr,
        contName=user.contName,
        contPhone=user.contPhone,
        verified=False,
        is_active=True,
        extra_info={
            "outlet_type": user.outlet_type,
            "service_hours": user.service_hours
        }
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    await sendVerifyMail(user.email)
    
    return db_user

async def verifyUserById(db: Session, user_id: str) -> UserResponse:
    """通过ID验证用户"""
    # 查找用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    # 检查是否已验证
    if user.verified:
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=getRoleName(user.role_id),
            verified=True,
            is_active=user.is_active,
            phone=user.phone,
            company=user.company
        )
    
    try:
        # 更新验证状态
        user.verified = True
        db.commit()
        db.refresh(user)
        
        # 返回更新后的用户信息
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=getRoleName(user.role_id),
            verified=True,
            is_active=user.is_active,
            phone=user.phone,
            company=user.company
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        ) 