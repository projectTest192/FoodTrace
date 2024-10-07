from pydantic import BaseModel

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # 替换 orm_mode 