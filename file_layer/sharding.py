from typing import List

def split_data(data: bytes, shard_size: int) -> List[bytes]:
    """Split data into chunks of shard_size."""
    return [data[i:i + shard_size] for i in range(0, len(data), shard_size)]

def merge_data(shards: List[bytes]) -> bytes:
    """Combine shards to form the original data."""
    return b''.join(shards)
