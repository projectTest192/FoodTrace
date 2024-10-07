import redis
import os
from dotenv import load_dotenv
from redis import Redis
from datetime import datetime, timedelta
import aioredis
import logging

load_dotenv()

# 从环境变量获取 Redis 配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# 开发环境使用内存字典模拟 Redis
class DictCache:
    def __init__(self):
        self.cache = {}
        
    def set(self, key, value, ex=None):
        self.cache[key] = value
        
    def get(self, key):
        return self.cache.get(key)
        
    def delete(self, key):
        self.cache.pop(key, None)
        
    def exists(self, key):
        return key in self.cache
        
    def hmset(self, name, mapping):
        if name not in self.cache:
            self.cache[name] = {}
        self.cache[name].update(mapping)
        
    def hgetall(self, name):
        return self.cache.get(name, {})
        
    def ping(self):
        return True

    def zadd(self, key, mapping):
        if key not in self.cache:
            self.cache[key] = {}
        self.cache[key].update(mapping)

    def zremrangebyscore(self, key, min_score, max_score):
        if key in self.cache:
            # 简单实现，实际应该根据分数删除
            self.cache[key] = {}

# 尝试连接 Redis，如果失败则使用内存字典
try:
    redisClient = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASSWORD,
        decode_responses=True
    )
    redisClient.ping()
    print("Redis connection successful")
except (redis.ConnectionError, Exception) as e:
    print(f"Could not connect to Redis: {e}")
    print("Using in-memory cache for development")
    redisClient = DictCache()

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redisClient  # 使用全局的 redisClient
        
    def save_realtime_data(self, device_id: str, data_type: str, value: float):
        """存储实时数据，保留30分钟"""
        key = f"realtime:{data_type}:{device_id}"
        timestamp = datetime.now().timestamp()
        self.redis.zadd(key, {f"{timestamp}:{value}": timestamp})
        # 只保留30分钟的数据
        old_time = (datetime.now() - timedelta(minutes=30)).timestamp()
        self.redis.zremrangebyscore(key, 0, old_time)
    
    def save_gps_location(self, shipment_id: str, lat: float, lng: float):
        """存储GPS位置数据，保留24小时"""
        key = f"gps:shipment:{shipment_id}"
        timestamp = datetime.now().timestamp()
        self.redis.zadd(key, {f"{timestamp}:{lat},{lng}": timestamp})
        # 只保留24小时的数据
        old_time = (datetime.now() - timedelta(hours=24)).timestamp()
        self.redis.zremrangebyscore(key, 0, old_time) 

logger = logging.getLogger(__name__)

async def init_redis_pool():
    try:
        redis = await aioredis.create_redis_pool('redis://localhost')
        return redis
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {str(e)}")
        logger.info("Using in-memory cache for development")
        return None

redis_client = None

async def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = await init_redis_pool()
    return redis_client 