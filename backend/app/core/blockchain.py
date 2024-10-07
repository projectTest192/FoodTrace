import os
import json
import subprocess
from typing import Dict, Any

class BlockchainClient:
    def __init__(self):
        self.network_path = os.path.join(os.path.dirname(__file__), "../blockchain/network")
        self.env = self._get_env()

    def _get_env(self) -> Dict[str, str]:
        env = os.environ.copy()
        env.update({
            "PATH": f"{self.network_path}/bin:" + env.get("PATH", ""),
            "FABRIC_CFG_PATH": self.network_path,
            "CORE_PEER_TLS_ENABLED": "false",
            "CORE_PEER_LOCALMSPID": "Org1MSP",
            "CORE_PEER_MSPCONFIGPATH": f"{self.network_path}/crypto-config/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp",
            "CORE_PEER_ADDRESS": "localhost:7051"
        })
        return env

    async def execute_chaincode(self, command_type: str, function: str, args: list) -> Dict[str, Any]:
        cmd = self._build_command(command_type, function, args)
        try:
            result = subprocess.run(cmd, env=self.env, cwd=self.network_path,
                                  capture_output=True, text=True, check=True)
            return json.loads(result.stdout) if result.stdout else {}
        except Exception as e:
            raise Exception(f"Chaincode execution failed: {str(e)}")

    def _build_command(self, command_type: str, function: str, args: list) -> list:
        base_cmd = [
            "peer", "chaincode", command_type,
            "-C", "mychannel",
            "-n", "foodtrace",
        ]
        
        if command_type == "invoke":
            base_cmd.extend([
                "-o", "localhost:7050",
                "--peerAddresses", "localhost:7051"
            ])
            
        base_cmd.extend(["-c", json.dumps({"function": function, "Args": args})])
        return base_cmd 