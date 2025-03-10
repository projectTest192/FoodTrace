import serial
import pynmea2

class GPSModule:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
        
    def get_location(self):
        """Get current GPS coordinates"""
        try:
            while True:
                line = self.serial.readline().decode('ascii', errors='replace')
                if line.startswith('$GPGGA'):
                    msg = pynmea2.parse(line)
                    latitude = msg.latitude
                    longitude = msg.longitude
                    return latitude, longitude
                    
        except Exception as e:
            print(f"Error reading GPS: {e}")
            return None, None 