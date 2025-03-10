from PN532 import *

class NFCController:
    def __init__(self):
        self.pn532 = PN532_SPI(debug=False, reset=20, cs=4)
        self.pn532.begin()
        self.pn532.SAM_configuration()

    def write_tag(self, data):
        """Write data to NFC tag"""
        try:
            # Wait for tag
            uid = self.pn532.read_passive_target(timeout=2)
            if uid is None:
                return False
                
            # Convert data to bytes
            data_bytes = json.dumps(data).encode()
            
            # Write to tag
            self.pn532.ntag2xx_write_block(1, data_bytes)
            return True
            
        except Exception as e:
            print(f"Error writing to NFC tag: {e}")
            return False
            
    def read_tag(self):
        """Read data from NFC tag"""
        try:
            # Wait for tag
            uid = self.pn532.read_passive_target(timeout=2)
            if uid is None:
                return None
                
            # Read data
            data = self.pn532.ntag2xx_read_block(1)
            return json.loads(data.decode())
            
        except Exception as e:
            print(f"Error reading NFC tag: {e}")
            return None 