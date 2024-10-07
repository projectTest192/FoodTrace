from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from typing import List
from pydantic import BaseModel

from ..db.session import getDb
from ..models import User, Role
from ..schemas.auth import UserLogin, Token
from ..schemas.user import UserCreate, UserResponse, DistributorCreate, RetailerCreate, ConsumerCreate
from ..services.auth import (
    authenticateUser,
    getUserByName,
    loginUser,
    createConsumer,
    createEnterprise,
    verifyUserEmail,
    regUser,
    createAccessToken,
    createDistributor,
    createRetailer
)
from ..core.security import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from ..core.auth import getCurrentUser, verifyEmailToken
from ..services.email import sendVerifyEmail
from ..services.user import getUserByEmail

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class LoginRequest(BaseModel):
    email: str
    pwd: str

async def getCurrentUser(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(getDb)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = getUserByName(db, email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register/consumer", response_model=UserResponse)
async def registerConsumer(
    userData: ConsumerCreate,
    db: Session = Depends(getDb)
):
    """注册消费者用户"""
    # 直接调用 service 层的方法，token 生成和邮件发送都在 service 层处理
    return await createConsumer(db, userData)

@router.post("/register/enterprise", response_model=UserResponse)
async def register_enterprise(user: UserCreate, db: Session = Depends(getDb)):
    """企业用户注册"""
    db_user = await createEnterprise(db, user, "producer")
    await sendVerifyEmail(db_user.email)
    return db_user

@router.post("/login", response_model=Token)
async def login(
    userLogin: UserLogin,
    db: Session = Depends(getDb)
):
    """用户登录"""
    return await loginUser(db, userLogin)

@router.post("/register/{role_type}")
async def register(
    role_type: str,  # 现在只接受: consumer, producer, distributor, retailer
    user: UserCreate,
    db: Session = Depends(getDb)
):
    """用户注册"""
    # 验证角色类型
    if role_type not in ['consumer', 'producer', 'distributor', 'retailer']:
        raise HTTPException(
            status_code=400,
            detail="Invalid role type. Must be one of: consumer, producer, distributor, retailer"
        )
    
    return await regUser(db, user)

@router.get("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(getDb)
):
    """验证邮箱"""
    try:
        # 验证 token 并获取邮箱
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email or payload.get("type") != "email_verify":
            raise HTTPException(
                status_code=400,
                detail="Invalid token"
            )
        
        # 更新用户验证状态
        user = getUserByEmail(db, email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        user.verified = True
        db.commit()
        
        return {"message": "Email verified successfully"}
        
    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid token"
        )

@router.post("/register/distributor", response_model=UserResponse)
async def register_distributor(
    user: DistributorCreate,
    db: Session = Depends(getDb)
):
    """经销商注册"""
    return await createDistributor(db, user)

@router.post("/register/retailer", response_model=UserResponse)
async def register_retailer(
    user: RetailerCreate,
    db: Session = Depends(getDb)
):
    """零售商注册"""
    return await createRetailer(db, user)