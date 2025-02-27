import yaml
import os

# Path to the YAML config file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config.yaml")

# Default values if config file or setting is missing
DEFAULT_CONFIG = {
    "DEFAULT_SHARD_SIZE": 1024,  # Fallback shard size in bytes
    "DEFAULT_ERROR_CORRECTION": 10,  # Default error correction level
    "DEFAULT_PROOF_HASH_ALGO": "sha256" # Default proof hash algorithm
}

# Load configuration from the YAML file
try:
    with open(CONFIG_PATH, "r") as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"Configuration file not found: {CONFIG_PATH}")
    config_data = DEFAULT_CONFIG

# Extract the shard size, falling back to default if missing
DEFAULT_SHARD_SIZE = config_data.get("DEFAULT_SHARD_SIZE", DEFAULT_CONFIG["DEFAULT_SHARD_SIZE"])
# Extract the error correction level, falling back to default if missing
DEFAULT_ERROR_CORRECTION = config_data.get("DEFAULT_ERROR_CORRECTION", DEFAULT_CONFIG["DEFAULT_ERROR_CORRECTION"])
# Extract the proof hash algorithm, falling back to default if missing
DEFAULT_PROOF_HASH_ALGO = config_data.get("DEFAULT_PROOF_HASH_ALGO", DEFAULT_CONFIG["DEFAULT_PROOF_HASH_ALGO"])