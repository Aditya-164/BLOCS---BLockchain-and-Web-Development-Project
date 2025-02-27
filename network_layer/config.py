import yaml
import os

# Path to the YAML config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")

# Default values if config file or setting is missing
DEFAULT_CONFIG = {
    "BUFFER_SIZE": 1024,  # Default buffer size in bytes
}

# Load configuration from the YAML file
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {CONFIG_PATH}")
    config_data = DEFAULT_CONFIG

# Extract the buffer size, falling back to default if missing
BUFFER_SIZE = config_data.get("BUFFER_SIZE", DEFAULT_CONFIG["BUFFER_SIZE"])
