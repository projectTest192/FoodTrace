from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "Food Trace System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 数据库配置 - 使用相对路径
    DATABASE_URL: str = "sqlite:///./app/db/data/app.db"
    
    # Redis配置 - 用于存储MQTT数据
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None  # 修改为Optional
    
    # MQTT配置
    MQTT_BROKER: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USERNAME: Optional[str] = None  # 修改为Optional
    MQTT_PASSWORD: Optional[str] = None  # 修改为Optional
    
    # 邮件配置
    MAIL_USERNAME: str = "qiezi360@gmail.com"
    MAIL_PASSWORD: str = "pkmo vepa rbzs waoq"  # 应用专用密码
    MAIL_FROM: str = "qiezi360@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False
    MAIL_FROM_NAME: str = "Food Trace System"
    
    # 区块链配置
    BLOCKCHAIN_NODE_URL: str = "http://localhost:8545"  # 或者使用测试网络
    BLOCKCHAIN_PRIVATE_KEY: str = ""  # 部署时设置
    CONTRACT_ADDRESS: str = ""  # 部署合约后设置
    
    # Hyperledger Fabric 配置
    FABRIC_API_URL: str = "http://localhost:4000"  # Fabric API 网关地址
    FABRIC_ORG: str = "Org1"
    FABRIC_CHANNEL: str = "mychannel"
    FABRIC_CHAINCODE: str = "foodtrace"
    FABRIC_BIN_PATH: str = str(Path(__file__).parent.parent / "blockchain/network/bin")
    FABRIC_CFG_PATH: str = str(Path(__file__).parent.parent / "blockchain/network")
    
    # 树莓派配置
    RASPBERRY_PI_URL: str = "http://localhost:5000"  # 树莓派服务地址
    
    # API服务地址
    API_URL: str = "http://localhost:8002"
    
    # 静态文件配置
    STATIC_DIR: Path = Path(__file__).parent.parent / "static"
    UPLOAD_DIR: Path = STATIC_DIR / "uploads"
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # 允许额外的字段

# 创建全局设置对象
settings = Settings()

# 设置数据库 URI
settings.SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL 

# 确保必要的目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 