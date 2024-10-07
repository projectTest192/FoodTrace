from functools import wraps
from fastapi import HTTPException

def check_permission(required_permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户角色
            role = get_current_user_role()
            
            # 检查权限
            if role == 'admin':
                return await func(*args, **kwargs)
                
            if role not in ROLES:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid role"
                )
                
            if required_permission not in ROLES[role]['permissions']:
                raise HTTPException(
                    status_code=403,
                    detail="Permission denied"
                )
                
            return await func(*args, **kwargs)
        return wrapper
    return decorator 