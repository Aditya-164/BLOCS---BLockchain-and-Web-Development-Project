# File Storage Layer Overview for Decentralized Storage System

## 1. Introduction
The File Storage Layer is responsible for the secure and distributed storage of files within the decentralized system. This layer ensures files are sharded, encrypted, replicated, and stored across multiple nodes in the network. It also handles file retrieval, versioning, and data integrity verification through cryptographic techniques.

---

## 2. Overall System Design

### 2.1 Components of the File Storage Layer
The File Storage Layer includes the following components:
- **File Sharding**: The process of splitting files into smaller pieces (shards) for distributed storage.
- **File Encryption**: Ensures data privacy by encrypting files before storage.
- **File Replication**: Involves replicating shards across multiple nodes to improve redundancy and fault tolerance.
- **Metadata Storage**: Stores essential metadata about file shards, encryption keys, and locations in the blockchain.
- **File Retrieval**: The process of reconstructing and delivering a complete file from its distributed shards.
- **Versioning**: Manages multiple versions of files and optimizes storage using delta encoding.
  
### 2.2 File Storage Workflow
1. **File Upload**: The user selects a file to store, which is split into multiple shards. Each shard is encrypted, and replication is applied.
2. **Shards Distribution**: The encrypted shards are distributed across various nodes in the network, with metadata (e.g., shard locations) stored on the blockchain.
3. **Storage Challenge**: Nodes periodically prove that they continue to store the allocated shards through cryptographic proofs.
4. **File Retrieval**: When a user requests a file, the network reconstructs the file by retrieving the shards from storage nodes and decrypting them.
5. **File Versioning**: When updates are made to the file, only the differences (deltas) between versions are stored, and new metadata is recorded.

---

## 3. Internal Implementation Details

### 3.1 File Sharding

#### 3.1.1 Sharding Process
When a user uploads a file to the decentralized storage system, it is split into several smaller pieces called **shards**. This sharding process has the following characteristics:
- **Shard Size**: A configurable size for each shard (e.g., 4 MB or 8 MB), depending on system requirements.
- **Number of Shards**: The file is divided into multiple shards, with the number depending on the file size.
- **Sharding Algorithm**: A sharding algorithm is used to split the file based on fixed-size chunks. Each chunk is then treated as a shard.


---

### 3.2 File Encryption

#### 3.2.1 Encryption Process
Before storage, each shard is encrypted to ensure privacy and security:
- **Encryption Algorithm**: Symmetric encryption (e.g., AES-256) is used to encrypt each shard. The encryption key is unique to the file.
- **Key Management**: Encryption keys are stored securely and are accessible only to the user who owns the file. The keys themselves may also be encrypted using the user’s public key.
- **Encryption per Shard**: Each shard is encrypted individually to prevent data leakage in case a single shard is compromised.

#### 3.2.2 Decryption Process
- When a file is retrieved, shards are decrypted using the corresponding encryption keys before reconstruction.
  
---

### 3.3 File Replication

#### 3.3.1 Replication Strategy
To ensure data durability and availability, each shard is replicated across multiple nodes in the network:
- **Replication Factor**: Each shard is replicated across a configurable number of nodes (e.g., 3 or 5 replicas).
- **Redundancy**: This ensures that even if some nodes go offline or become unresponsive, the file can still be reconstructed from the available shards.
- **Geographical Distribution**: Shards may be stored on nodes located in different geographical regions to enhance availability.

#### 3.3.2 Erasure Coding
- **Erasure Coding** (e.g., **Reed-Solomon coding**) is used to split data into shards and add redundancy. It enables the reconstruction of a file even if some shards are lost or unavailable.
  - For example, if a file is split into 10 shards with a replication factor of 3, even if 2 shards are lost, the file can still be recovered.

#### 3.3.3 Benefits of Replication
- **Fault Tolerance**: Increased redundancy makes the network more resilient to node failures.
- **Improved Availability**: File retrieval is faster, as nodes with replicas can parallelize the delivery of shards.

---

### 3.4 Metadata Storage

#### 3.4.1 Metadata Definition
Metadata contains essential information about the file and its storage. This includes:
- **File Hash**: A unique hash (e.g., SHA-256) representing the original file.
- **Shard Hashes**: A list of hashes for each encrypted shard, ensuring their integrity.
- **Shard Locations**: The network addresses of nodes where the shards are stored.
- **Encryption Keys**: References to the encryption keys used for each shard.
- **Replication Factor**: The number of replicas for each shard.

#### 3.4.2 Blockchain Integration
- File metadata is stored on the blockchain to ensure immutability and easy access by nodes.
- When files are uploaded, metadata transactions are added to the blockchain. This includes shard hashes and storage node details.
- During file retrieval, the blockchain is queried for the shard locations and other relevant metadata.

---

### 3.5 File Retrieval

#### 3.5.1 Retrieval Process
When a user wants to retrieve a file, the following steps occur:
1. **Request Submission**: The user submits a retrieval request to the network.
2. **Metadata Query**: The blockchain is queried for the metadata of the requested file, including shard hashes and storage node addresses.
3. **Shard Requests**: The nodes storing the required shards are identified, and requests are sent to those nodes.
4. **Shard Reconstruction**: Once the shards are retrieved, they are decrypted and combined to reconstruct the original file.
5. **File Delivery**: The reconstructed file is delivered back to the user.

#### 3.5.2 Fault Tolerance in Retrieval
- **Redundant Shards**: If one or more nodes fail to provide the required shards, the system retrieves the necessary replicas from other nodes.
- **Erasure Coding**: Erasure coding ensures that the file can be reconstructed even if some shards are missing.

---

### 3.6 File Versioning

#### 3.6.1 Version Control System
Files stored on the decentralized network are versioned to manage updates and changes efficiently:
- **Version Numbering**: Each time a file is updated, it is assigned a new version number. This allows the system to track changes and retrieve previous versions if necessary.
- **Delta Storage**: Instead of storing full copies of updated files, only the changes (deltas) between versions are stored. This minimizes storage overhead and optimizes file storage for frequently updated files.

#### 3.6.2 Delta Encoding
- **Delta Encoding**: When a file is updated, the difference between the old and new versions is computed and stored. This reduces the amount of data that needs to be stored on the network for each version.
  - For example, if only 5% of a file changes during an update, only that 5% is stored, and the rest of the file remains unchanged.

#### 3.6.3 Metadata Updates
- Each time a file version is updated, new metadata is added to the blockchain, including the new shard hashes and updated encryption keys.
- The blockchain stores a history of version metadata, allowing the retrieval of older versions if required.

---

### 3.7 Data Integrity and Cryptography

#### 3.7.1 Data Integrity Verification
To ensure data integrity, each shard is hashed and stored using cryptographic techniques:
- **Shard Hashing**: A cryptographic hash (e.g., SHA-256) is generated for each shard before it is stored. This hash is included in the file metadata on the blockchain.
- **Merkle Tree**: For efficient verification, shard hashes may be included in a **Merkle tree**. The Merkle root is stored on the blockchain, allowing quick verification of data integrity without having to check every shard individually.

#### 3.7.2 Storage Proofs
- **Proof-of-Storage**: Nodes are periodically required to provide cryptographic proofs that they are storing the allocated shards. These proofs are validated by other nodes in the network to ensure that the data remains available.
- **Challenge-Response**: A node can challenge another to provide a proof of storage by requesting the hash of a random piece of the shard. This ensures that nodes are continuously maintaining the integrity of their storage.

#### 3.7.3 Encryption and Decryption
- **Encryption Keys**: Encryption keys are securely stored, and only the file owner has access to them for decrypting the stored shards during retrieval.
- **Decentralized Key Management**: The system ensures that encryption keys are never stored in plaintext on any single node. Instead, keys may be distributed across nodes using a decentralized key management system.

---

## 4. Conclusion

The File Storage Layer is designed to provide secure, decentralized file storage and retrieval. By using sharding, encryption, replication, and a robust versioning system, it ensures that files are stored efficiently, with high availability and fault tolerance. Integration with the blockchain guarantees the immutability of file metadata and facilitates decentralized control over storage and retrieval processes.


# File structure:
#
# src/
# ├── main.rs
# ├── file_storage_layer.rs
# ├── shard.rs
# ├── metadata.rs
# ├── encryption.rs
# ├── erasure_coding.rs
# ├── distribution.rs
# └── storage_node.rs

# src/main.rs
