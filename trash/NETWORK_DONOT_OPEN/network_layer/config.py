import yaml
import os

# Path to the YAML config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")

# Default values if config file or setting is missing
DEFAULT_CONFIG = {
    "MAX_CONNECTIONS": 10,
    "BUFFER_SIZE": 1024,
    "RETRY_COUNT": 3,
}

# Load configuration from the YAML file
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {CONFIG_PATH}")
    config_data = DEFAULT_CONFIG

# Load Max Connections
MAX_CONNECTIONS = config_data.get("MAX_CONNECTIONS", DEFAULT_CONFIG["MAX_CONNECTIONS"])

# Load Buffer Size
BUFFER_SIZE = config_data.get("BUFFER_SIZE", DEFAULT_CONFIG["BUFFER_SIZE"])

# Load Retry Count
RETRY_COUNT = config_data.get("RETRY_COUNT", DEFAULT_CONFIG["RETRY_COUNT"])
