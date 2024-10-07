from datetime import datetime, timedelta
import jwt
from ..core.config import settings

def generate_temp_token(product_id: str) -> str:
    """
    生成临时token用于树莓派认证
    """
    expire = datetime.utcnow() + timedelta(minutes=30)  # 30分钟有效期
    
    to_encode = {
        "exp": expire,
        "product_id": product_id,
        "type": "temp_token"
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def verify_temp_token(token: str) -> dict:
    """
    验证临时token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != "temp_token":
            raise ValueError("Invalid token type")
            
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.JWTError:
        raise ValueError("Invalid token") 