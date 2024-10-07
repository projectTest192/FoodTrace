from datetime import datetime
import json
import subprocess
from typing import Optional, Dict, Any, List
from pathlib import Path
from ..core.config import settings

class BlockchainService:
    def __init__(self):
        # 设置Fabric环境变量
        self.env = {
            "PATH": f"{settings.FABRIC_BIN_PATH}:$PATH",
            "FABRIC_CFG_PATH": settings.FABRIC_CFG_PATH,
            "CORE_PEER_TLS_ENABLED": "false",
            "CORE_PEER_LOCALMSPID": "Org1MSP",
            "CORE_PEER_MSPCONFIGPATH": f"{settings.FABRIC_CFG_PATH}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp",
            "CORE_PEER_ADDRESS": "localhost:7051"
        }

    def _run_command(self, command: str) -> str:
        """执行shell命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                env=self.env,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e.stderr}")
            raise

    async def upload_product_data(self, data: Dict[str, Any]) -> bool:
        """上传产品数据到区块链"""
        try:
            # 构建chaincode调用命令
            command = (
                f"peer chaincode invoke -o localhost:7050 "
                f"-C mychannel -n foodtrace "
                f"--peerAddresses localhost:7051 "
                f'-c \'{{"function":"CreateProduct","Args":["{data["product_id"]}", "{json.dumps(data)}"]}}\''
            )
            
            self._run_command(command)
            return True
        except Exception as e:
            print(f"Error uploading to blockchain: {e}")
            return False

    async def get_product_trace(self, product_id: str) -> Dict[str, Any]:
        """获取产品溯源信息"""
        try:
            # 构建查询命令
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProduct","{product_id}"]}}\''
            )
            
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error querying blockchain: {e}")
            return {}

    async def update_product_status(self, product_id: str, status: str, data: Dict[str, Any]) -> bool:
        """更新产品状态"""
        try:
            command = (
                f"peer chaincode invoke -o localhost:7050 "
                f"-C mychannel -n foodtrace "
                f"--peerAddresses localhost:7051 "
                f'-c \'{{"function":"SetProductStatus","Args":["{product_id}","{status}","{json.dumps(data)}"]}}\''
            )
            
            self._run_command(command)
            return True
        except Exception as e:
            print(f"Error updating product status: {e}")
            return False

    async def get_all_products(self) -> List[Dict]:
        """获取所有产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetAllProducts"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    async def get_product(self, product_id: str) -> Dict:
        """查询单个产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProduct","{product_id}"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting product: {e}")
            return {}

    async def get_active_products(self) -> List[Dict]:
        """查询活跃产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetActiveProducts"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting active products: {e}")
            return []

    async def get_product_history(self, product_id: str) -> List[Dict]:
        """查询产品历史记录"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProductHistory","{product_id}"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting product history: {e}")
            return []

    async def get_products_by_status(self, status: str) -> List[Dict]:
        """根据状态查询产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProductsByStatus","{status}"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting products by status: {e}")
            return []

    async def get_products_by_producer(self, producer_id: str) -> List[Dict]:
        """查询生产者的产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProductsByProducer","{producer_id}"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting products by producer: {e}")
            return []

    async def get_products_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """查询日期范围内的产品"""
        try:
            command = (
                f"peer chaincode query "
                f"-C mychannel -n foodtrace "
                f'-c \'{{"Args":["GetProductsByDateRange","{start_date}","{end_date}"]}}\''
            )
            result = self._run_command(command)
            return json.loads(result)
        except Exception as e:
            print(f"Error getting products by date range: {e}")
            return []

    async def create_product(self, data: Dict[str, Any]) -> bool:
        """创建新产品"""
        try:
            command = (
                f"peer chaincode invoke -o localhost:7050 "
                f"-C mychannel -n foodtrace "
                f"--peerAddresses localhost:7051 "
                f'-c \'{{"function":"CreateProduct","Args":["{data["product_id"]}", "{json.dumps(data)}"]}}\''
            )
            self._run_command(command)
            return True
        except Exception as e:
            print(f"Error creating product: {e}")
            return False

# 创建服务实例
blockSVC = BlockchainService() 