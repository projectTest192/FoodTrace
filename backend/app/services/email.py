from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from ..core.config import settings
from ..core.email import email_conf, sendVerifyMail, sendResetMail


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,  # 使用 STARTTLS
    MAIL_SSL_TLS=False,  # 不使用 SSL/TLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False  # 临时禁用证书验证
)

fastmail = FastMail(conf)

async def sendVerifyEmail(email: str, token: str):
    """发送验证邮件的服务层函数"""
    try:
        print(f"准备发送邮件到: {email}")
        return await sendVerifyMail(email, token)
    except Exception as e:
        print(f"发送邮件失败: {str(e)}")
        raise e

async def sendAlertEmail(emails: List[str], alert_type: str, alert_data: dict):
    """发送告警邮件"""
    subject = f"系统告警 - {alert_type}"
    body = f"""
    <h2>系统检测到异常</h2>
    <p>告警类型: {alert_type}</p>
    <p>告警详情:</p>
    <pre>{alert_data}</pre>
    """
    
    message = MessageSchema(
        subject=subject,
        recipients=emails,
        body=body,
        subtype="html"
    )
    
    await fastmail.send_message(message)
    return True 