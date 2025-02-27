import hashlib
import hmac

from .config import DEFAULT_PROOF_HASH_ALGO

def generate_proof(data: bytes, salt: bytes, key: bytes) -> str:
    """Generate a proof of data integrity using HMAC."""
    return hmac.new(key, data + salt, getattr(hashlib, DEFAULT_PROOF_HASH_ALGO)).hexdigest()

def verify_proof(expected_proof: str, proof: str) -> bool:
    """Verify a proof of data integrity."""
    return hmac.compare_digest(expected_proof, proof)