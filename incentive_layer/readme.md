# Ethereum File Storage Deal Management

## Functions

### `propose_deal(client_address, value, client_private_key, file_id, storage_space, duration_hours)`
**Description**: Allows a client to propose a new file storage deal.

**Arguments**:
- `client_address`: The Ethereum address of the client.
- `value`: The amount of Ether to be sent with the transaction.
- `client_private_key`: The private key of the client's Ethereum account.
- `file_id`: The unique identifier for the file being stored.
- `storage_space`: The amount of storage space required for the file, in bytes.
- `duration_hours`: The duration of the storage deal in hours.

**Returns**: The transaction hash of the proposed deal.

---

### `validate_proof(file_id, client_address, client_private_key)`
**Description**: Allows a client to validate the storage provider's proof of storage.

**Arguments**:
- `file_id`: The unique identifier for the file being stored.
- `client_address`: The Ethereum address of the client.
- `client_private_key`: The private key of the client's Ethereum account.

**Returns**: The transaction hash of the validated proof.

---

### `approve_deal(file_id, billing_amount, server_address, server_private_key)`
**Description**: Allows a storage provider to approve a proposed deal.

**Arguments**:
- `file_id`: The unique identifier for the file being stored.
- `billing_amount`: The amount to be billed for the storage deal.
- `server_address`: The Ethereum address of the storage provider.
- `server_private_key`: The private key of the storage provider's Ethereum account.

**Returns**: The transaction hash of the approved deal.

---

### `invalidate_deal(file_id, reason, client_address, client_private_key)`
**Description**: Allows a client to invalidate an active deal.

**Arguments**:
- `file_id`: The unique identifier for the file being stored.
- `reason`: The reason for invalidating the deal.
- `client_address`: The Ethereum address of the client.
- `client_private_key`: The private key of the client's Ethereum account.

**Returns**: The transaction hash of the invalidated deal.

---

### `complete_deal(w3, contract, file_id, client_address, client_private_key)`
**Description**: Allows a client to complete an active deal.

**Arguments**:
- `w3`: The Web3 instance.
- `contract`: The deployed contract instance.
- `file_id`: The unique identifier for the file being stored.
- `client_address`: The Ethereum address of the client.
- `client_private_key`: The private key of the client's Ethereum account.

**Returns**: The transaction receipt of the completed deal.

---

### `get_deal_status(file_id)`
**Description**: Retrieves the current status of a file storage deal.

**Arguments**:
- `file_id`: The unique identifier for the file being stored.

**Returns**: A dictionary containing the deal's status information.

---

## Configuration

The script requires the following configuration variables:
- `client_address`: The Ethereum address of the client.
- `client_private_key`: The private key of the client's Ethereum account.
- `server_address`: The Ethereum address of the storage provider.
- `server_private_key`: The private key of the storage provider's Ethereum account.

**Note**: Replace these values with your own Ethereum addresses and private keys before using the script.
