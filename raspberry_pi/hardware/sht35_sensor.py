import smbus2
import time

class SHT35Sensor:
    def __init__(self, bus=1, address=0x44):
        self.bus = smbus2.SMBus(bus)
        self.address = address

    def read_sensor(self):
        """Read temperature and humidity from SHT35"""
        try:
            # Send measurement command
            self.bus.write_i2c_block_data(self.address, 0x2C, [0x06])
            time.sleep(0.5)
            
            # Read data
            data = self.bus.read_i2c_block_data(self.address, 0x00, 6)
            
            # Convert the data
            temp_raw = data[0] * 256 + data[1]
            humidity_raw = data[3] * 256 + data[4]
            
            temperature = -45 + (175 * temp_raw / 65535.0)
            humidity = 100 * humidity_raw / 65535.0
            
            return temperature, humidity
            
        except Exception as e:
            print(f"Error reading SHT35: {e}")
            return None, None 