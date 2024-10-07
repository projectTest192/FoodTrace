from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os

# 确保数据目录存在
DB_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DB_DIR, exist_ok=True)

# 数据库URL
DB_FILE = os.path.join(DB_DIR, "app.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

print(f"Database directory: {DB_DIR}")
print(f"Database file: {DB_FILE}")
print(f"Database exists: {os.path.exists(DB_FILE)}")

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    # 启用外键支持
    isolation_level='SERIALIZABLE'
)

# SQLite不支持ALTER TABLE，所以我们需要在连接时启用外键
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA synchronous=OFF")
    cursor.execute("PRAGMA journal_mode=MEMORY")
    cursor.close()

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# 创建基类
Base = declarative_base()

# 依赖项
def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 导出这些变量供其他模块使用
__all__ = ['engine', 'SessionLocal', 'getDb', 'Base', 'DB_FILE']