import hashlib
from typing import List, Dict

def get_hash(data: bytes) -> str:
    """Generate a smaller hash using a double-hashing technique."""
    # First, compute SHA-256 hash
    sha256_hash = hashlib.sha256(data).digest()
    # Second, compute MD5 hash of the SHA-256 output to get a smaller hash
    final_hash = hashlib.md5(sha256_hash).hexdigest()  # Use SHA-1 instead of MD5 if desired
    return final_hash

def create_shard_mapping(shards: List[bytes]) -> Dict[str, int]:
    """Create a mapping of double-hashed shard keys to their sequence number."""
    return {get_hash(shard): idx for idx, shard in enumerate(shards)}
