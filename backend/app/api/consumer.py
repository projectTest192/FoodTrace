from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session import sessionLocal
from ..models.product import Product

router = APIRouter()

def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/browse/")
async def browseProducts(skip: int = 0, limit: int = 10, db: Session = Depends(getDb)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products 