from typing import List, Dict
from .encryption import decrypt_data
from .redundancy import decode_file, decode_shard
from .metadata import get_hash

def Assimilate(shards: List[bytes], mapping: Dict[str, int], private_key: bytes) -> bytes:
    # Reorder shards based on mapping
    ordered_shards = [shards[mapping[get_hash(shard)]] for shard in shards]
    
    # Decrypt each shard
    decrypted_shards = [decrypt_data(shard, private_key) for shard in ordered_shards]
    
    # Decode each shard individually
    decoded_shards = [decode_shard(shard) for shard in decrypted_shards]
    
    # Decode the entire file to reconstruct original data
    original_data = decode_file(decoded_shards)
    return original_data
