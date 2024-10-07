import subprocess
import json
from typing import List, Optional

class BlockchainClient:
    def __init__(self):
        self.network_path = "app/blockchain/network"

    async def _execute_command(self, command: str) -> str:
        process = await asyncio.create_subprocess_shell(
            f"cd {self.network_path} && {command}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Command failed: {stderr.decode()}")
        return stdout.decode()

    async def create_product(self, *args) -> None:
        args_str = ",".join([f'"{arg}"' for arg in args])
        command = f'./scripts/query.sh CreateProduct {args_str}'
        await self._execute_command(command)

    async def set_product_status(self, chain_id: str, status: str) -> None:
        command = f'./scripts/query.sh SetProductStatus "{chain_id}" "{status}"'
        await self._execute_command(command)

    async def get_product_history(self, chain_id: str) -> List[dict]:
        command = f'./scripts/query.sh GetProductHistory "{chain_id}"'
        result = await self._execute_command(command)
        return json.loads(result) 