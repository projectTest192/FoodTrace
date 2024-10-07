from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
from .base import BaseSchema

class UserBase(BaseSchema):
    """用户基础模型"""
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(BaseModel):
    """用户创建模型"""
    name: str  # 这个会被映射到 username
    email: str
    pwd: str
    role_id: int
    bizLic: Optional[str] = None
    bizType: Optional[str] = None
    addr: Optional[str] = None
    contName: Optional[str] = None
    contPhone: Optional[str] = None

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    """用户更新模型"""
    pwd: Optional[str] = None  # 改为 pwd
    name: Optional[str] = None
    phone: Optional[str] = None
    bizLic: Optional[str] = None
    bizType: Optional[str] = None
    addr: Optional[str] = None
    contName: Optional[str] = None
    contPhone: Optional[str] = None

class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: str  # 改为接受字符串类型的ID
    pwd: str  # 改为 pwd
    active: bool
    verified: bool
    created_at: datetime
    updated_at: datetime
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: str  # 改为字符串类型，因为我们的用户ID是 'USR' 开头的字符串
    username: str
    email: EmailStr
    role: str
    verified: bool
    is_active: bool
    phone: Optional[str] = None
    company: Optional[str] = None
    
    class Config:
        from_attributes = True

class ConsumerCreate(BaseSchema):
    """消费者创建模型"""
    name: str  # 这个会被映射到 User.username
    email: str
    pwd: str
    role_id: int = 5  # 默认为消费者角色ID

    class Config:
        from_attributes = True

class ProducerCreate(UserCreate):
    """生产商创建模型"""
    role_id: int = 2
    bizLic: str
    addr: str
    contName: str
    contPhone: str

class DistributorCreate(UserCreate):
    """经销商创建模型"""
    role_id: int = 3
    bizLic: str
    addr: str
    contName: str
    contPhone: str
    distribution_area: List[str]
    vehicle_info: Dict[str, str]

class RetailerCreate(UserCreate):
    """零售商创建模型"""
    role_id: int = 4
    bizLic: str
    addr: str
    contName: str
    contPhone: str
    outlet_type: str
    service_hours: str

class EnterpriseCreate(UserCreate):
    """企业用户创建请求模型"""
    regTime: datetime = None

class AdminCreate(UserCreate):
    """管理员创建请求模型"""
    role: str = "admin"

class UserInfo(BaseSchema):
    """用户信息返回模型"""
    id: int
    name: str
    email: str
    role_id: int
    active: bool
    verified: bool
    bizType: Optional[str] = None
    bizLic: Optional[str] = None
    addr: Optional[str] = None
    contName: Optional[str] = None
    contPhone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EntInfo(BaseModel):
    """企业信息更新模型"""
    bizLic: Optional[str] = None      # 营业执照
    bizType: Optional[str] = None     # 企业类型
    addr: Optional[str] = None        # 地址
    contName: Optional[str] = None    # 联系人
    contPhone: Optional[str] = None   # 联系电话
    regTime: Optional[datetime] = None # 注册时间

    class Config:
        from_attributes = True

class User(UserBase):
    """用户信息返回模型"""
    id: int
    role: str
    active: bool = True
    verified: bool = False
    createTime: datetime
    lastLogin: Optional[datetime] = None
    
    # 用户详细信息
    avatar: Optional[str] = None
    addr: Optional[str] = None
    phone: Optional[str] = None
    birthDate: Optional[datetime] = None
    gender: Optional[str] = None
    
    # 企业用户特有字段
    bizLic: Optional[str] = None
    contName: Optional[str] = None
    contPhone: Optional[str] = None
    bizType: Optional[str] = None
    regTime: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    token: str
    type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class EnterpriseProfile(BaseModel):
    # 企业用户特有字段
    businessLicense: str
    address: str
    contactPerson: str
    contactPhone: str
    # ... 其他企业信息字段