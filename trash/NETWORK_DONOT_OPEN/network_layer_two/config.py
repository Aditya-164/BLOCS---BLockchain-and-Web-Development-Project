import yaml
import os

# Path to the YAML config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")

# Default values if config file or setting is missing
DEFAULT_CONFIG = {
    "DEFAULT_INTERFACE": "eth0",  # Default network interface
    "DEBUG": 0,  # Debug mode flag
}

# Load configuration from the YAML file
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {CONFIG_PATH}")
    config_data = DEFAULT_CONFIG

# Extract the network interface, falling back to default if missing
DEFAULT_INTERFACE = config_data.get("DEFAULT_INTERFACE", DEFAULT_CONFIG["DEFAULT_INTERFACE"])

# Extract the debug setting, falling back to default if missing
DEBUG = config_data.get("DEBUG", DEFAULT_CONFIG["DEBUG"])