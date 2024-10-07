import paho.mqtt.client as mqtt
from ..core.config import settings
import json
import redis
from datetime import datetime

# Redis 连接
try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
except:
    print("Using in-memory cache for development")
    redis_client = {}

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("foodtrace/+/data")  # 订阅所有设备的数据主题

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        device_id = msg.topic.split('/')[1]
        
        # 添加时间戳
        data['timestamp'] = datetime.now().isoformat()
        
        # 存储到Redis
        if isinstance(redis_client, redis.Redis):
            redis_client.set(
                f"iot_data:{device_id}", 
                json.dumps(data),
                ex=3600  # 1小时过期
            )
        else:
            redis_client[f"iot_data:{device_id}"] = data
            
    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# 创建MQTT客户端
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# 连接MQTT服务器
try:
    mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
    mqtt_client.loop_start()
except:
    print("MQTT connection failed, using mock data") 