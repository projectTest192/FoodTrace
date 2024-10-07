from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .base import BaseSchema

class UserLogin(BaseSchema):
    """用户登录模型"""
    email: str
    pwd: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    """令牌数据模型"""
    email: Optional[str] = None
    role: Optional[str] = None

class Token(BaseSchema):
    """令牌模型"""
    accToken: str
    tokenType: str
    user: dict 