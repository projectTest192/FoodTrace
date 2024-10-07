from sqlalchemy.orm import registry

# 创建一个全局的模型注册表
mapper_registry = registry()
Base = mapper_registry.generate_base()

# 导出基类
__all__ = ['Base'] 