import json
from web3 import Web3
import yaml
import os


class BlockchainConfig:
    def __init__(self, network="sepolia"):        
        # Initialize the Web3 object with the appropriate RPC URL
        rpc_url = DEFAULT_NETWORK_URL
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # if not self.w3.is_connected():
        #     raise ConnectionError(f"Could not connect to the {network} network at {rpc_url}")

        # Load ABI from a specified file path
        abi_path = os.path.join(os.path.dirname(__file__), "abi.json")
        with open(abi_path, "r") as abi_file:
            self.contract_abi = json.load(abi_file)
        
        # Contract address for each network (use separate addresses for production if needed)
        self.contract_address = DEFAULT_CONTRACT_ADDRESS
        
        if not self.contract_address:
            raise ValueError(f"No contract address specified for network '{network}'")

        # Initialize the contract object
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

    def get_w3(self):
        return self.w3

    def get_contract(self):
        return self.contract


# Path to the YAML config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")

# Default values if config file or setting is missing
DEFAULT_CONFIG = {
    "DEFAULT_NETWORK_URL": "https://sepolia.infura.io/v3/4ddbeaf177884a69bdf6073b94008c27",
    "DEFAULT_CONTRACT_ADDRESS": "0xd457540c3f08f7F759206B5eA9a4cBa321dE60DC",
}

# Load configuration from the YAML file
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {CONFIG_PATH}")
    config_data = DEFAULT_CONFIG

# Get the default network URL and contract address
DEFAULT_NETWORK_URL = config_data.get("DEFAULT_NETWORK_URL", DEFAULT_CONFIG["DEFAULT_NETWORK_URL"])
DEFAULT_CONTRACT_ADDRESS = config_data.get("DEFAULT_CONTRACT_ADDRESS", DEFAULT_CONFIG["DEFAULT_CONTRACT_ADDRESS"])


# Usage
# Initialize with 'sepolia' or 'mainnet' or 'goerli' or 'local'
try:
    config = BlockchainConfig()
    w3 = config.get_w3()
    contract = config.get_contract()
except Exception as e:
    print(f"Initialization failed: {e}")