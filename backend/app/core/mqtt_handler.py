import json
from fastapi import FastAPI
from redis import Redis
import paho.mqtt.client as mqtt
from .config import settings

# Redis配置
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
    decode_responses=True
)

def setup_mqtt(app: FastAPI):
    """设置MQTT客户端"""
    mqtt_client = mqtt.Client()
    
    @mqtt_client.on_connect
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT broker")
        client.subscribe("shipment/environment")
    
    @mqtt_client.on_message
    def on_message(client, userdata, msg):
        try:
            # 解析数据
            data = json.loads(msg.payload)
            shipment_id = data.get("shipment_id")
            
            if shipment_id:
                # 存储到Redis
                redis_key = f"shipment:env:{shipment_id}"
                redis_client.set(redis_key, json.dumps(data))
                redis_client.expire(redis_key, 3600)  # 1小时过期
                
                print(f"Stored environment data for shipment {shipment_id}")
            
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    try:
        # 连接MQTT代理
        mqtt_client.connect(settings.MQTT_BROKER, settings.MQTT_PORT, 60)
        mqtt_client.loop_start()
        
        # 保存client实例到app的state中
        app.state.mqtt_client = mqtt_client
        
        @app.on_event("shutdown")
        def shutdown_event():
            mqtt_client.loop_stop()
            mqtt_client.disconnect()
            
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return None

    return mqtt_client 