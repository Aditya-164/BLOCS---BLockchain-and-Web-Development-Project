# tests/test_sharding.py
import io
import pytest
from file_layer import Distribute, Assimilate
from Crypto.PublicKey import RSA

@pytest.fixture(scope="module")
def rsa_key():
    # Generate RSA key pair for testing
    key = RSA.generate(2048)
    return key.export_key()

def test_distribute_and_assimilate(rsa_key):
    # Sample file data
    test_data = b"Sample test data for sharding and encoding."
    
    # Create file object and distribute it
    file_obj = io.BytesIO(test_data)
    shards, mapping = Distribute(file_obj, rsa_key)
    
    # Check that shards were created
    assert len(shards) > 0
    
    # Reassemble and verify integrity of the data
    reconstructed_data = Assimilate(shards, mapping, rsa_key)
    assert reconstructed_data == test_data

def test_distribute_and_assimilate_num_shards_specific(rsa_key):

    num_shards = 1
    # Sample file data
    test_data = b"python -m unittest discover -s tests"
    
    # Create file object and distribute it
    file_obj = io.BytesIO(test_data)
    shards, mapping = Distribute(file_obj, rsa_key, num_shards=num_shards)

    # Check that shards were created
    assert len(shards) > 0, "No shards were created"
    # Check that the number of shards is as expected
    assert len(shards) == num_shards, f"Expected {num_shards} shards, got {len(shards)} shards"
    
    # Reassemble and verify integrity of the data
    reconstructed_data = Assimilate(shards, mapping, rsa_key)
    assert reconstructed_data == test_data

def test_actual_file(rsa_key):
    # Load a test file
    with open("tests/test_file.txt", "rb") as file:
        test_data = file.read()
        shards, mapping = Distribute(file, rsa_key)
    
    # Create file object and distribute it
    # file_obj = io.BytesIO(test_data)
    
    
    # Check that shards were created
    assert len(shards) > 0
    
    # Reassemble and verify integrity of the data
    reconstructed_data = Assimilate(shards, mapping, rsa_key)
    assert reconstructed_data == test_data

if __name__ == "__main__":
    pytest.main(["-v", "test_file_layer.py"])