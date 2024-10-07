from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from ..db.session import getDb
from ..services.user import createConsumer, updateUserInfo, updateEntInfo
from ..core.auth import getCurrentUser
from ..core.email import sendVerifyMail

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
async def register(
    user: schemas.ConsumerCreate,
    db: Session = Depends(getDb)
):
    return await createConsumer(db, user)

@router.put("/info", response_model=schemas.User)
def updateInfo(
    userInfo: schemas.UserInfo,
    db: Session = Depends(getDb),
    currentUser = Depends(getCurrentUser)
):
    return updateUserInfo(db, currentUser.id, userInfo)

@router.put("/ent-info", response_model=schemas.User)
def updateEnterprise(
    entInfo: schemas.EntInfo,
    db: Session = Depends(getDb),
    currentUser = Depends(getCurrentUser)
):
    return updateEntInfo(db, currentUser.id, entInfo)

@router.post("/testmail")
async def testMail(email: str):
    """测试邮件发送功能"""
    result = await sendVerifyMail(email)
    if result:
        return {"msg": "邮件发送成功"}
    return {"msg": "邮件发送失败"}

@router.get("/users")
async def get_users(db: Session = Depends(getDb)):
    """获取所有用户"""
    users = db.query(schemas.User).all()
    return users