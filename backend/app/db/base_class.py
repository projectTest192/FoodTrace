from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from .model_registry import Base

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)

# 导出基类
__all__ = ['Base'] 