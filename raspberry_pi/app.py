from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt
import json
import time
import threading
from datetime import datetime
import random

# Hardware interfaces
from hardware.sht35_sensor import SHT35Sensor
from hardware.gps_module import GPSModule
from hardware.nfc_controller import NFCController

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
TOPIC = "shipment/environment"

# Initialize hardware
sht35 = SHT35Sensor()
gps = GPSModule()
nfc = NFCController()

# Global state for sensor monitoring
monitoring_active = True

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

def publish_sensor_data():
    """Background task to publish sensor data every 5 minutes"""
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    while monitoring_active:
        try:
            # Get sensor readings
            temp, humidity = sht35.read_sensor()
            lat, lon = gps.get_location()
            
            # Create payload
            payload = {
                "timestamp": datetime.now().isoformat(),
                "temperature": temp,
                "humidity": humidity,
                "location": {
                    "latitude": lat,
                    "longitude": lon
                }
            }
            
            # Publish to MQTT
            mqtt_client.publish(TOPIC, json.dumps(payload))
            
            # Check for anomalies
            if temp > 28.0:  # Temperature threshold
                handle_anomaly("High temperature detected", payload)
                
        except Exception as e:
            print(f"Error publishing sensor data: {e}")
            
        time.sleep(300)  # 5 minutes interval

def handle_anomaly(message, data):
    """Handle detected anomalies"""
    anomaly_payload = {
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }
    # TODO: Send to blockchain logging service
    print(f"Anomaly detected: {anomaly_payload}")

@app.route('/api/write_product_data', methods=['POST'])
def write_product_data():
    """API endpoint to write product data to NFC tag"""
    try:
        product_data = request.json
        
        # Get current sensor readings
        temp, humidity = sht35.read_sensor()
        lat, lon = gps.get_location()
        
        # Combine product data with sensor readings
        iot_data = {
            "product_data": product_data,
            "environmental_data": {
                "temperature": temp,
                "humidity": humidity,
                "location": {
                    "latitude": lat,
                    "longitude": lon
                },
                "timestamp": datetime.now().isoformat()
            }
        }
        
        # Write to NFC tag
        success = nfc.write_tag(iot_data)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Data written to NFC tag",
                "iot_data": iot_data
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to write to NFC tag"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/read_tag', methods=['GET'])
def read_tag():
    """API endpoint to read NFC tag data"""
    try:
        tag_data = nfc.read_tag()
        return jsonify({
            "status": "success",
            "data": tag_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Start sensor monitoring in background thread
    sensor_thread = threading.Thread(target=publish_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    
    # Start Flask application
    app.run(host='0.0.0.0', port=5000)