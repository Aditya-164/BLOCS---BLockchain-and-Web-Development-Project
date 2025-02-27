# File Layer Module

## Features

- **Secure File Distribution and Retrieval**: Distribute files securely across multiple shards and reconstruct them when needed.
- **Redundant Encoding**: Utilizes file-level and shard-level Reed-Solomon encoding for data redundancy and error correction.
- **Data Encryption**: Encrypts each shard using a private key to ensure data security.
- **Sharding**: Splits files into multiple shards for efficient storage and transmission.

## Usage

### Distribute a File

Use the `Distribute` function in `file_upload.py` to split and distribute a file.

```python
from file_upload import Distribute

with open('your_file.txt', 'rb') as file_obj:
    private_key = b'your_private_key'
    encrypted_shards, shard_mapping = Distribute(file_obj, private_key, num_shards=5)
```

### Retrieve a File

Use the `Assimilate` function in `file_retrieval.py` to retrieve and reconstruct the original file from shards.

```python
from file_retrieval import Assimilate

original_data = Assimilate(shards, shard_mapping, private_key, shard_parity=2)
```

## Configuration

- **Number of Shards**: Set `num_shards` in `Distribute` to specify the number of shards.
- **Shard Size**: Modify `DEFAULT_SHARD_SIZE` in `config.py` to change the default shard size.
- **Encryption Key**: Use your private key for encryption and decryption.
- **Error Correction Level**: Adjust `DEFAULT_ERROR_CORRECTION` in `config.py` to set the Reed-Solomon error correction level.
- **Configuration File**: Create a `config.yaml` file to override default settings.

### Sample `config.yaml`

```yaml
DEFAULT_SHARD_SIZE: 2048
DEFAULT_ERROR_CORRECTION: 5
```