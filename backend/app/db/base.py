from .base_class import Base

# 导入所有模型，确保正确的导入顺序
# 1. 首先导入基础用户模型（因为其他模型都依赖它）
from ..models.user import (
    Role,  # Role 必须在 User 之前，因为 User 依赖 Role
    User,
    Permission
)

# 2. 然后是产品相关模型（依赖于用户模型）
from ..models.product import (
    Category,
    Product,
    ProductPrice,
    ProdTrace,
    ProductStock,
    ProductIoTData
)

# 3. 运输相关模型（必须在 IoT 模型之前）
from ..models.shipment import (
    Shipment,
    ShipTrace,
    ShipmentItem,
    ShipmentStatus
)

# 4. IoT相关模型（依赖于产品和运输模型）
from ..models.iot import (
    DeviceInfo,
    IotData,
    EnvData,
    TraceEvent,  # TraceEvent 依赖 Shipment
    RfidBind
)

# 5. 订单相关模型
from ..models.order import (
    Order,
    OrderItem,
    OrderStatus
)

# 6. 销售相关模型
from ..models.sale import (
    Sale,
    SaleItem
)

# 导出所有模型
__all__ = [
    'Base',
    # User models (必须最先导出)
    'Role', 'User', 'Permission',
    # Product models
    'Category', 'Product', 'ProductPrice', 'ProdTrace', 'ProductStock', 'ProductIoTData',
    # Shipment models (必须在 IoT models 之前)
    'Shipment', 'ShipTrace', 'ShipmentItem', 'ShipmentStatus',
    # IoT models
    'DeviceInfo', 'IotData', 'EnvData', 'TraceEvent', 'RfidBind',
    # Order models
    'Order', 'OrderItem', 'OrderStatus',
    # Sale models
    'Sale', 'SaleItem'
]
