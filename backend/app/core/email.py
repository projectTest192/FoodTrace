from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List, Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import timedelta, datetime
from ..core.security import SECRET_KEY, ALGORITHM
from ..core.config import settings
from pydantic import EmailStr

load_dotenv()

 
templates_dir = Path(__file__).parent.parent / "templates"
templates_dir.mkdir(exist_ok=True)

# Email configuration from environment variables
email_conf = ConnectionConfig(
    MAIL_USERNAME="qiezi360@gmail.com",  # 直接硬编码测试
    MAIL_PASSWORD="pkmo vepa rbzs waoq",  # 直接硬编码测试
    MAIL_FROM="qiezi360@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=templates_dir,
    MAIL_FROM_NAME="Food Trace System"
)

# 本地开发环境配置
DEV_SMTP_PORT = 1025  # Python smtp调试服务器端口
DEV_SMTP_HOST = "localhost"

# 创建FastMail实例
mail = FastMail(email_conf)

async def sendVerifyMail(email: str, token: str):
    """发送验证邮件"""
    try:
        # 创建邮件内容
        verifyLink = f"http://localhost:3000/verify-email?token={token}"  # 使用token而不是email
        htmlContent = f"""
        <h2>Welcome to Food Trace System</h2>
        <p>Please click the following link to verify your email:</p>
        <p><a href="{verifyLink}">{verifyLink}</a></p>
        <br>
        <p>If this is not your action, please ignore this email.</p>
        """

        # 创建邮件消息
        msg = MessageSchema(
            subject="验证您的食品溯源系统账号",
            recipients=[email],
            body=htmlContent,
            subtype="html"
        )

        # 发送邮件
        await mail.send_message(msg)
        print(f"验证邮件已发送至: {email}")
        return True

    except Exception as e:
        print(f"发送邮件时出错: {str(e)}")
        return False

async def sendResetMail(email: str, resetToken: str):
    """发送重置密码邮件"""
    try:
        resetLink = f"http://localhost:3000/reset-pwd?token={resetToken}"
        htmlContent = f"""
        <h2>重置您的密码</h2>
        <p>您请求重置密码，请点击以下链接：</p>
        <p><a href="{resetLink}">{resetLink}</a></p>
        <br>
        <p>如果不是您本人的操作，请忽略此邮件。</p>
        """

        msg = MessageSchema(
            subject="重置您的食品溯源系统密码",
            recipients=[email],
            body=htmlContent,
            subtype="html"
        )

        await mail.send_message(msg)
        
        print(f"密码重置邮件已发送至: {email}")
        return True

    except Exception as e:
        print(f"发送邮件时出错: {str(e)}")
        return False

# 如果需要实际发送邮件，取消下面的注释
"""
async def sendVerifyEmail(email: str):
    try:
        message = MessageSchema(
            subject="验证您的邮箱",
            recipients=[email],
            body=f"请点击以下链接验证您的邮箱：\n"
                 f"http://localhost:3000/verify-email?email={email}",
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
"""

# 临时禁用邮件配置
async def sendVerificationEmail(email: str, token: str):
    # 临时打印验证链接而不是发送邮件
    print(f"""
    Would send email to: {email}
    Verification link: http://localhost:3000/verify-email?token={token}
    """)
    return True 

async def sendEmail(
    to_email: str,
    subject: str,
    body: str,
    html: bool = True
) -> bool:
    """发送邮件的基础函数"""
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[to_email],
            body=body,
            subtype="html" if html else "plain"
        )
        
        # 开发环境只打印不发送
        if os.getenv("ENV") == "dev":
            print(f"\nWould send email to: {to_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body}")
            return True
            
        await mail.send_message(message)
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        if os.getenv("ENV") != "dev":
            raise e
        return False 
