import sys
from pathlib import Path
import redis
import os
import paho.mqtt.client as mqtt
import json

# 添加项目根目录到 Python 路径
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.mqtt_handler import setup_mqtt

# 首先导入数据库相关
from .db.session import engine, SessionLocal
from .db.base import Base
from .db.init_db import init_db
from sqlalchemy.orm import Session

# 然后导入所有模型
from .models.user import User, Role, Permission
from .models.product import Product, Category, ProductIoTData
from .models.shipment import Shipment, ShipmentItem, ShipTrace
from .db.base import *

# 最后导入 API 路由
from .api import auth, user, admin, product, shipment, iot, sale, order

# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    Food traceability system for Oxford Brookes University.
    
    Key features:
    - Product tracking
    - Supply chain management
    - Quality control
    
    User roles:
    - Administrator (System Admin)
    - Producer (Food Producer)
    - Distributor (Logistics)
    - Retailer (Campus Shops)
    - Consumer (OBU Students and Staff)
    """,
    version="2.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 创建数据库表
def setup_database():
    """初始化数据库"""
    try:
        # 确保数据库目录存在
        db_dir = "./app/db/data"
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        print(f"Database directory: {db_dir}")
        
        # 数据库文件路径
        db_file = os.path.join(db_dir, "app.db")
        print(f"Database file: {db_file}")
        print(f"Database exists: {os.path.exists(db_file)}")
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        # 初始化基础数据
        db = SessionLocal()
        try:
            init_db(db)
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {str(e)}")
            raise e
        finally:
            db.close()
            
    except Exception as e:
        print(f"Database setup error: {str(e)}")
        raise e

# Redis连接
redis_client = None
try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
        decode_responses=True
    )
    redis_client.ping()
    print("Redis connection successful")
except Exception as e:
    print(f"Redis error: {e}")
    redis_client = {}

def setup_mqtt_client():
    """设置MQTT客户端"""
    try:
        client = mqtt.Client()

        def on_connect(client, userdata, flags, rc):
            print(f"Connected to MQTT broker with result code: {rc}")
            client.subscribe("foodtrace/+/data")
            client.subscribe("shipment/environment")

        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload)
                
                if msg.topic.startswith("foodtrace/"):
                    device_id = msg.topic.split('/')[1]
                    if isinstance(redis_client, redis.Redis):
                        redis_client.set(
                            f"iot_data:{device_id}",
                            json.dumps(data),
                            ex=3600
                        )
                elif msg.topic == "shipment/environment":
                    shipment_id = data.get("shipment_id")
                    if shipment_id and isinstance(redis_client, redis.Redis):
                        redis_client.set(
                            f"shipment:env:{shipment_id}",
                            json.dumps(data),
                            ex=3600
                        )
                        
            except Exception as e:
                print(f"Error processing MQTT message: {e}")

        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
        client.loop_start()
        print("Connected to MQTT broker successfully")
        return client

    except Exception as e:
        print(f"MQTT setup error: {e}")
        return None

@app.on_event("startup")
def startup_event():
    """应用启动时的初始化操作"""
    try:
        # 初始化数据库
        setup_database()
        
        # 设置MQTT
        app.state.mqtt_client = setup_mqtt_client()
        
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Startup error: {str(e)}")
        raise e

@app.on_event("shutdown")
def shutdown_event():
    """应用关闭时的清理操作"""
    if hasattr(app.state, "mqtt_client") and app.state.mqtt_client:
        app.state.mqtt_client.loop_stop()
        app.state.mqtt_client.disconnect()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)    

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(product.router, prefix="/api", tags=["products"])
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(shipment.router, prefix="/api", tags=["shipments"])
app.include_router(iot.router, prefix="/api/iot", tags=["iot"])
app.include_router(sale.router, prefix="/api/sale", tags=["sale"])
app.include_router(order.router, prefix="/api", tags=["orders"])

# 添加静态文件服务
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to Food Trace System API"}