from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

from ..db.session import getDb
from ..models.user import User
from .security import SECRET_KEY, ALGORITHM
from ..services.user import getUserByEmail

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def getCurrentUser(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(getDb)
) -> User:
    """获取当前用户"""
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
        
    user = getUserByEmail(db, email)
    if user is None:
        raise credentials_exception
    return user

async def getCurrentActiveUser(current_user = Depends(getCurrentUser)):
    """获取当前活跃用户"""
    if not current_user.active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user 

async def getCurrentAdmin(
    current_user: User = Depends(getCurrentUser)
) -> User:
    """获取当前管理员用户"""
    if not current_user or current_user.role_id != 1:  # 假设 role_id 1 是管理员
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要管理员权限"
        )
    return current_user

def verifyEmailToken(token: str) -> str:
    """验证邮箱token并返回邮箱地址"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Invalid token: email not found")
            
        token_type: str = payload.get("type")
        if token_type != "email_verify":
            raise ValueError("Invalid token type")
            
        return email
        
    except JWTError:
        raise ValueError("Invalid token format") 