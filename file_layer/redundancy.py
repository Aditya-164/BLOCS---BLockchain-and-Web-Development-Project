from reedsolo import RSCodec
from .config import DEFAULT_ERROR_CORRECTION

# Create Reed-Solomon codec
rs = RSCodec(DEFAULT_ERROR_CORRECTION)

def encode_file(data: bytes) -> bytes:
    """Encode the entire file with Reed-Solomon"""
    return rs.encode(data)

def encode_shard(shard: bytes) -> bytes:
    """Encode each shard with Reed-Solomon encoding """
    return rs.encode(shard)

def decode_file(shards: list[bytes]) -> bytes:
    """Decode an entire file from Reed-Solomon encoded shards."""
    return rs.decode(b''.join(shards))[0]

def decode_shard(shard_data: bytes) -> bytes:
    """Decode a single shard using Reed-Solomon encoding."""
    return rs.decode(shard_data)[0]
