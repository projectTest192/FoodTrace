from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RFIDWrite(BaseModel):
    rfid_id: str
    product_id: str
    latitude: float
    longitude: float

class EnvironmentData(BaseModel):
    device_id: str
    product_id: str
    temperature: float
    humidity: float
    latitude: float
    longitude: float

class ProductTrace(BaseModel):
    product_id: str
    rfid_data: Optional[RFIDWrite]
    environment_data: List[EnvironmentData] 