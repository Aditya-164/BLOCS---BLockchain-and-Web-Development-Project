# BLOCS (Blockchain-based Ledger for Open Cloud Storage)
## System Implementation Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Module Implementation Details](#4-module-implementation-details)
5. [Smart Contract Implementation](#5-smart-contract-implementation)
6. [Network Protocol](#6-network-protocol)
7. [Storage System](#7-storage-system)
8. [Security Implementation](#8-security-implementation)
9. [Testing Strategy](#9-testing-strategy)
10. [Deployment Guide](#10-deployment-guide)

## 1. Project Overview

BLOCS is a decentralized cloud storage system that leverages blockchain technology for transparency and incentivization while using a peer-to-peer network for actual storage operations.

### Key Features
- Decentralized file storage and retrieval
- Blockchain-based incentive system
- File sharding and encryption
- Proof-of-Storage consensus
- DHT-based shard tracking
- Zero-knowledge proofs for privacy

### Technology Stack
- Rust (Core implementation)
- Polkadot/Substrate (Smart contracts)
- libp2p (P2P networking)
- ink! (Smart contract development)
- SQLite (Local metadata storage)

## 2. System Architecture

### High-Level Components
```
                                    ┌─────────────────┐
                                    │   Polkadot      │
                                    │  Smart Contract │
                                    └────────┬────────┘
                                            │
┌─────────────┐    ┌─────────────┐    ┌────┴─────┐
│  Storage    │◄───┤    Node     ├────►  Network  │
│   Layer     │    │   Manager   │    │  Layer   │
└─────────────┘    └─────────────┘    └────┬─────┘
                                           │
                                    ┌──────┴──────┐
                                    │     DHT     │
                                    └─────────────┘
```

### Component Interactions
1. Node Manager coordinates all operations
2. Storage Layer handles file operations
3. Network Layer manages P2P communications
4. DHT tracks shard locations
5. Smart Contracts manage incentives

## 3. Directory Structure

```
blocs/
├── Cargo.toml                 # Workspace configuration
├── README.md                  # Project documentation
├── contracts/                 # Smart contract implementations
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs            # Contract wrapper
│       ├── incentives.rs     # Token economy
│       └── storage_registry.rs# Node registry
├── core/                      # Core functionality
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs            # Core exports
│       ├── config.rs         # Configuration
│       ├── types.rs          # Type definitions
│       └── error.rs          # Error handling
├── network/                   # P2P networking
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs            # Network exports
│       ├── behaviour.rs      # Network behavior
│       ├── protocol.rs       # Custom protocols
│       └── dht.rs            # DHT implementation
├── storage/                   # Storage management
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs            # Storage exports
│       ├── encryption.rs     # Data encryption
│       ├── sharding.rs       # File sharding
│       └── validation.rs     # PoS validation
└── src/                      # Main application
    ├── main.rs               # Entry point
    ├── node.rs               # Node implementation
    └── cli.rs                # CLI interface
```

## 4. Module Implementation Details

### Core Module

#### Types (`core/src/types.rs`)
```rust
pub struct FileMetadata {
    pub file_id: H256,
    pub name: String,
    pub size: u64,
    pub owner: H256,
    pub shard_locations: Vec<ShardLocation>,
    pub encryption_key: Vec<u8>,
    pub timestamp: u64,
    pub redundancy_factor: u8,
}

pub struct ShardLocation {
    pub shard_id: H256,
    pub node_id: String,
    pub merkle_proof: Vec<H256>,
    pub last_validated: u64,
}

pub struct StorageNode {
    pub id: String,
    pub available_space: u64,
    pub reliability_score: f64,
    pub uptime: u64,
    pub bandwidth: u64,
}
```

#### Configuration (`core/src/config.rs`)
```rust
pub struct Config {
    pub node_id: String,
    pub listen_addresses: Vec<Multiaddr>,
    pub storage_path: PathBuf,
    pub max_storage: u64,
    pub min_redundancy: u8,
    pub contract_address: H256,
    pub bootstrap_nodes: Vec<Multiaddr>,
}

impl Config {
    pub fn from_file(path: PathBuf) -> Result<Self, ConfigError> {
        // Configuration loading implementation
    }
}
```

### Network Module

#### Behavior (`network/src/behaviour.rs`)
```rust
#[derive(NetworkBehaviour)]
pub struct BlocsBehaviour {
    pub gossipsub: Gossipsub,
    pub kademlia: Kademlia,
    pub mdns: Mdns,
    pub identify: Identify,
}

impl BlocsBehaviour {
    pub async fn new(config: &Config) -> Result<Self, NetworkError> {
        // Network behavior initialization
    }

    pub fn broadcast_shard_location(&mut self, location: ShardLocation) {
        // Shard location broadcasting
    }
}
```

#### DHT Implementation (`network/src/dht.rs`)
```rust
pub struct StorageDHT {
    kademlia: Kademlia,
    local_store: HashMap<H256, Vec<ShardLocation>>,
}

impl StorageDHT {
    pub async fn put_shard_location(
        &mut self,
        file_id: H256,
        location: ShardLocation,
    ) -> Result<(), DhtError> {
        // DHT storage implementation
    }

    pub async fn get_shard_locations(
        &self,
        file_id: H256,
    ) -> Result<Vec<ShardLocation>, DhtError> {
        // Shard location retrieval
    }
}
```

### Storage Module

#### Sharding (`storage/src/sharding.rs`)
```rust
pub struct ShardingManager {
    shard_size: usize,
    redundancy_factor: u8,
    storage_path: PathBuf,
}

impl ShardingManager {
    pub async fn shard_file(
        &self,
        file_path: PathBuf,
        encryption_key: &[u8],
    ) -> Result<(FileMetadata, Vec<Vec<u8>>), StorageError> {
        // File sharding implementation
        // 1. Read file
        // 2. Encrypt data
        // 3. Split into shards
        // 4. Generate merkle proofs
        // 5. Create metadata
    }

    pub async fn reconstruct_file(
        &self,
        metadata: FileMetadata,
        shards: Vec<Vec<u8>>,
    ) -> Result<Vec<u8>, StorageError> {
        // File reconstruction implementation
    }
}
```

## 5. Smart Contract Implementation

### Incentive Contract (`contracts/src/incentives.rs`)
```rust
#[ink::contract]
mod storage_incentives {
    #[ink(storage)]
    pub struct StorageIncentives {
        storage_providers: ink::StorageMap<AccountId, Balance>,
        storage_users: ink::StorageMap<AccountId, Balance>,
        price_per_byte: Balance,
        minimum_stake: Balance,
    }

    impl StorageIncentives {
        #[ink(message)]
        pub fn store_file(&mut self, size: Balance) -> Result<(), Error> {
            // Payment handling for storage
        }

        #[ink(message)]
        pub fn claim_rewards(&mut self) -> Result<Balance, Error> {
            // Reward distribution
        }

        #[ink(message)]
        pub fn slash_provider(&mut self, provider: AccountId) -> Result<(), Error> {
            // Penalty implementation
        }
    }
}
```

## 6. Network Protocol

### Protocol Specification

#### Message Types
```rust
pub enum BlocsMessage {
    StorageRequest {
        file_id: H256,
        size: u64,
        redundancy: u8,
    },
    StorageResponse {
        accepted: bool,
        available_space: u64,
    },
    ShardTransfer {
        shard_id: H256,
        data: Vec<u8>,
        proof: Vec<H256>,
    },
    ValidationChallenge {
        shard_id: H256,
        challenge_data: Vec<u8>,
    },
    ValidationResponse {
        shard_id: H256,
        proof: Vec<u8>,
    },
}
```

### DHT Protocol
1. Key-Value store for shard locations
2. Regular validation of stored data
3. Automatic replication on node failure

## 7. Storage System

### Encryption Strategy
- AES-256-GCM for symmetric encryption
- RSA for key exchange
- Per-file encryption keys

### Sharding Algorithm
1. Calculate optimal shard size
2. Generate erasure coding
3. Distribute shards based on node reliability

### Proof-of-Storage Implementation
```rust
pub struct StorageProof {
    pub shard_id: H256,
    pub merkle_root: H256,
    pub proof_path: Vec<H256>,
    pub challenge_response: Vec<u8>,
}

impl StorageProof {
    pub fn validate(&self, challenge: &[u8]) -> bool {
        // Proof validation implementation
    }
}
```

## 8. Security Implementation

### Zero-Knowledge Proofs
```rust
pub struct ZkProof {
    pub proof: Vec<u8>,
    pub public_inputs: Vec<u8>,
}

impl ZkProof {
    pub fn generate(
        shard: &[u8],
        challenge: &[u8],
    ) -> Result<Self, SecurityError> {
        // ZKP generation
    }

    pub fn verify(&self) -> bool {
        // ZKP verification
    }
}
```

## 9. Testing Strategy

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_file_sharding() {
        // Sharding test implementation
    }

    #[tokio::test]
    async fn test_storage_proof() {
        // PoS test implementation
    }
}
```

### Integration Tests
```rust
#[tokio::test]
async fn test_complete_storage_cycle() {
    // 1. Initialize nodes
    // 2. Store file
    // 3. Verify storage
    // 4. Retrieve file
    // 5. Validate data
}
```

## 10. Deployment Guide

### Node Setup
1. Install dependencies
2. Configure node
3. Initialize storage
4. Connect to network

### Configuration Example
```toml
[node]
id = "node1"
storage_path = "/data/blocs"
max_storage = "1000000000"  # 1GB
min_redundancy = 3

[network]
listen_addresses = ["/ip4/0.0.0.0/tcp/4001"]
bootstrap_nodes = [
    "/ip4/104.131.131.82/tcp/4001/p2p/QmaCpDMGvV2BGHeYERUEnRQAwe3N8SzbUtfsmvsqQLuvuJ"
]

[contract]
address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"
```

### Performance Considerations
1. Shard size optimization
2. Network bandwidth management
3. Storage allocation strategy
4. DHT query optimization

## Key Design Decisions

1. **Modular Architecture**
   - Separate concerns for maintainability
   - Clear interfaces between components
   - Easy to test and extend

2. **Storage Strategy**
   - Fixed shard size for simplicity
   - Reed-Solomon erasure coding
   - Merkle trees for validation

3. **Network Protocol**
   - Custom protocol over libp2p
   - DHT for shard tracking
   - Gossip for network updates

4. **Security**
   - Client-side encryption
   - Zero-knowledge proofs
   - Regular validation challenges

5. **Incentive Model**
   - Token rewards for storage
   - Slashing for violations
   - Reputation system

## Future Improvements

1. **Scalability**
   - Implement sharding for the DHT
   - Optimize network protocols
   - Add caching layer

2. **Features**
   - Streaming support
   - Deduplication
   - Compression

3. **Security**
   - Quantum-resistant encryption
   - Enhanced privacy features
   - Additional validation methods

