import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

def generate_mock_data(shipment_id):
    return {
        "shipment_id": shipment_id,
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "temperature": round(random.uniform(2.0, 8.0), 2),
            "humidity": round(random.uniform(40, 60), 2),
            "location": {
                "latitude": round(random.uniform(51.7, 51.8), 6),
                "longitude": round(random.uniform(-1.3, -1.2), 6)
            }
        }
    }

def simulate_shipment(shipment_id):
    client = mqtt.Client()
    client.connect("localhost", 1883, 60)
    
    try:
        while True:
            data = generate_mock_data(shipment_id)
            client.publish("food/shipment/environment", json.dumps(data))
            print(f"Published: {json.dumps(data, indent=2)}")
            time.sleep(5)
    except KeyboardInterrupt:
        client.disconnect()

if __name__ == "__main__":
    simulate_shipment(1)  # 模拟shipment_id=1的配送环境数据 