# Application configuration settings

# MQTT Settings
MQTT_CONFIG = {
    "broker": "localhost",
    "port": 1883,
    "topic": "shipment/environment",
    "keepalive": 60
}

# Hardware Settings
HARDWARE_CONFIG = {
    "sht35": {
        "bus": 1,
        "address": 0x44
    },
    "gps": {
        "port": "/dev/ttyAMA0",
        "baudrate": 9600
    },
    "nfc": {
        "reset_pin": 20,
        "cs_pin": 4
    }
}

# Flask Settings
FLASK_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False
} 