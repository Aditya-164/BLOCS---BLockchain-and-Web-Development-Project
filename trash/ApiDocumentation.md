# BLOCS (Blockchain-based Ledger for Open Cloud Storage)
## Complete Implementation Guide & API Documentation

## Table of Contents
1. [Dependencies](#1-dependencies)
2. [Module Signatures](#2-module-signatures)
3. [Smart Contract Interface](#3-smart-contract-interface)
4. [Network Protocol Definitions](#4-network-protocol-definitions)
5. [Storage Interface](#5-storage-interface)
6. [Security Implementations](#6-security-implementations)
7. [User Guide](#7-user-guide)
8. [UI Integration Guide](#8-ui-integration-guide)
9. [API Documentation](#9-api-documentation)
10. [Development Roadmap](#10-development-roadmap)

## 1. Dependencies

### Workspace Dependencies (`Cargo.toml`)
```toml
[workspace]
members = ["contracts", "core", "network", "storage", "."]

[workspace.dependencies]
tokio = { version = "1.0", features = ["full"] }
async-trait = "0.1"
thiserror = "1.0"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tracing = "0.1"
```

### Core Module Dependencies
```toml
[dependencies]
substrate-primitives = "0.17"
blake2 = "0.10"
sha3 = "0.10"
hmac = "0.12"
rand = "0.8"
uuid = { version = "1.0", features = ["v4"] }
```

### Network Module Dependencies
```toml
[dependencies]
libp2p = { version = "0.53", features = [
    "tcp",
    "websocket",
    "dns",
    "gossipsub",
    "mdns",
    "kad",
    "identify",
    "yamux",
    "noise",
    "macros"
]}
futures = "0.3"
pin-project = "1.0"
```

### Storage Module Dependencies
```toml
[dependencies]
aes-gcm = "0.10"
reed-solomon-erasure = "4.0"
merkle_light = "0.4"
rocksdb = "0.21"
zstd = "0.12"
```

### Contract Module Dependencies
```toml
[dependencies]
ink_lang = "4.0"
ink_storage = "4.0"
ink_prelude = "4.0"
scale = { package = "parity-scale-codec", version = "3.0", default-features = false, features = ["derive"] }
```

## 2. Module Signatures

### Core Types (`core/src/types.rs`)
```rust
pub type Result<T> = std::result::Result<T, Error>;

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("Network error: {0}")]
    Network(String),
    #[error("Storage error: {0}")]
    Storage(String),
    #[error("Contract error: {0}")]
    Contract(String),
    #[error("Validation error: {0}")]
    Validation(String),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FileMetadata {
    // Fields defined earlier
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NodeMetadata {
    pub id: NodeId,
    pub addresses: Vec<Multiaddr>,
    pub storage_stats: StorageStats,
    pub reputation: ReputationMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StorageStats {
    pub total_space: u64,
    pub used_space: u64,
    pub shard_count: u64,
    pub bandwidth_up: u64,
    pub bandwidth_down: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReputationMetrics {
    pub uptime: f64,
    pub reliability: f64,
    pub response_time: u64,
    pub validation_success_rate: f64,
}
```

### Network Interfaces (`network/src/lib.rs`)
```rust
#[async_trait]
pub trait NetworkService: Send + Sync {
    async fn broadcast_shard(&self, shard: ShardLocation) -> Result<()>;
    async fn fetch_shard(&self, shard_id: H256) -> Result<Vec<u8>>;
    async fn find_storage_nodes(&self, count: usize) -> Result<Vec<NodeMetadata>>;
    async fn validate_storage(&self, challenge: Challenge) -> Result<ValidationProof>;
}

#[derive(Debug)]
pub struct NetworkManager {
    behaviour: BlocsBehaviour,
    event_loop: NetworkEventLoop,
    dht: StorageDHT,
}

impl NetworkManager {
    pub async fn new(config: NetworkConfig) -> Result<Self>;
    pub async fn start(&mut self) -> Result<()>;
    pub async fn stop(&mut self) -> Result<()>;
    pub fn connection_count(&self) -> usize;
}
```

### Storage Interfaces (`storage/src/lib.rs`)
```rust
#[async_trait]
pub trait StorageService: Send + Sync {
    async fn store_file(&self, file_path: PathBuf) -> Result<FileMetadata>;
    async fn retrieve_file(&self, file_id: H256) -> Result<Vec<u8>>;
    async fn delete_file(&self, file_id: H256) -> Result<()>;
    async fn list_files(&self) -> Result<Vec<FileMetadata>>;
}

pub trait ShardingService: Send + Sync {
    fn create_shards(&self, data: &[u8]) -> Result<Vec<Shard>>;
    fn merge_shards(&self, shards: Vec<Shard>) -> Result<Vec<u8>>;
    fn validate_shard(&self, shard: &Shard) -> Result<bool>;
}

pub trait EncryptionService: Send + Sync {
    fn encrypt_data(&self, data: &[u8], key: &[u8]) -> Result<Vec<u8>>;
    fn decrypt_data(&self, data: &[u8], key: &[u8]) -> Result<Vec<u8>>;
    fn generate_key(&self) -> Result<Vec<u8>>;
}
```

## 3. Smart Contract Interface

### Storage Contract (`contracts/src/storage_registry.rs`)
```rust
#[ink::contract]
pub mod storage_registry {
    #[ink(storage)]
    pub struct StorageRegistry {
        nodes: ink::StorageMap<AccountId, NodeInfo>,
        files: ink::StorageMap<Hash, FileInfo>,
        stakes: ink::StorageMap<AccountId, Balance>,
    }

    impl StorageRegistry {
        #[ink(constructor)]
        pub fn new(min_stake: Balance) -> Self;

        #[ink(message)]
        pub fn register_node(&mut self, node_info: NodeInfo) -> Result<()>;

        #[ink(message)]
        pub fn update_node_stats(&mut self, stats: NodeStats) -> Result<()>;

        #[ink(message)]
        pub fn stake(&mut self) -> Result<()>;

        #[ink(message)]
        pub fn unstake(&mut self) -> Result<()>;

        #[ink(message)]
        pub fn claim_rewards(&mut self) -> Result<Balance>;
    }
}
```

## 4. Network Protocol Definitions

### Protocol Messages
```rust
#[derive(Debug, Serialize, Deserialize)]
pub enum ProtocolMessage {
    StorageRequest(StorageRequest),
    StorageResponse(StorageResponse),
    ShardTransfer(ShardTransfer),
    ValidationRequest(ValidationRequest),
    ValidationResponse(ValidationResponse),
    NodeAnnouncement(NodeAnnouncement),
    NodeLeave(NodeLeave),
}

#[derive(Debug, Serialize, Deserialize)]
pub struct StorageRequest {
    pub file_id: H256,
    pub size: u64,
    pub redundancy: u8,
    pub payment_proof: PaymentProof,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ValidationRequest {
    pub challenge: Challenge,
    pub proof_request: ProofRequest,
}
```

## 5. Storage Interface

### Sharding Manager
```rust
pub struct ShardingConfig {
    pub shard_size: usize,
    pub redundancy_factor: u8,
    pub encryption_algorithm: EncryptionAlgorithm,
    pub compression_level: u32,
}

pub struct ShardingManager {
    config: ShardingConfig,
    encryption: Box<dyn EncryptionService>,
    compression: Box<dyn CompressionService>,
}

impl ShardingManager {
    pub fn new(config: ShardingConfig) -> Self;
    pub async fn shard_file(&self, path: PathBuf) -> Result<(FileMetadata, Vec<Shard>)>;
    pub async fn reconstruct_file(&self, metadata: FileMetadata, shards: Vec<Shard>) -> Result<Vec<u8>>;
    pub fn validate_shards(&self, shards: &[Shard]) -> Result<bool>;
}
```

## 6. Security Implementations

### Encryption Service
```rust
pub enum EncryptionAlgorithm {
    Aes256Gcm,
    ChaCha20Poly1305,
}

pub trait EncryptionService: Send + Sync {
    fn encrypt(&self, data: &[u8], key: &[u8]) -> Result<Vec<u8>>;
    fn decrypt(&self, data: &[u8], key: &[u8]) -> Result<Vec<u8>>;
    fn generate_key(&self) -> Result<Vec<u8>>;
}

pub struct AesEncryption {
    algorithm: EncryptionAlgorithm,
}

impl EncryptionService for AesEncryption {
    // Implementation details...
}
```

## 7. User Guide

### Command Line Interface
```rust
#[derive(Debug, clap::Parser)]
pub struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Debug, clap::Subcommand)]
pub enum Commands {
    Init(InitCmd),
    Store(StoreCmd),
    Retrieve(RetrieveCmd),
    List(ListCmd),
    Status(StatusCmd),
}

pub struct InitCmd {
    #[arg(long)]
    config: PathBuf,
}
```

### Usage Examples
```bash
# Initialize a new node
blocs init --config node_config.toml

# Store a file
blocs store --file path/to/file.txt

# Retrieve a file
blocs retrieve --file-id <hash> --output path/to/output.txt

# List stored files
blocs list

# Check node status
blocs status
```

## 8. UI Integration Guide

### REST API Interface
```rust
#[derive(Debug, Serialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub error: Option<String>,
}

#[derive(Debug)]
pub struct ApiServer {
    node: Arc<BlocsNode>,
    config: ApiConfig,
}

impl ApiServer {
    pub async fn new(node: Arc<BlocsNode>, config: ApiConfig) -> Self;
    pub async fn start(&self) -> Result<()>;
}

// API Endpoints
pub mod endpoints {
    pub async fn store_file(
        multipart: Multipart,
        node: Arc<BlocsNode>,
    ) -> ApiResponse<FileMetadata>;

    pub async fn retrieve_file(
        file_id: Path<H256>,
        node: Arc<BlocsNode>,
    ) -> ApiResponse<Vec<u8>>;

    pub async fn list_files(
        node: Arc<BlocsNode>,
    ) -> ApiResponse<Vec<FileMetadata>>;

    pub async fn node_status(
        node: Arc<BlocsNode>,
    ) -> ApiResponse<NodeStatus>;
}
```

### WebSocket Events
```rust
#[derive(Debug, Serialize)]
pub enum WsEvent {
    StorageProgress(StorageProgress),
    ValidationEvent(ValidationEvent),
    NodeEvent(NodeEvent),
    NetworkEvent(NetworkEvent),
}

pub struct WsServer {
    events: broadcast::Sender<WsEvent>,
    config: WsConfig,
}
```

## 9. API Documentation

### RESTful API Endpoints

#### File Operations
```
POST   /api/v1/files              # Upload file
GET    /api/v1/files/{id}         # Download file
DELETE /api/v1/files/{id}         # Delete file
GET    /api/v1/files              # List files
```

#### Node Operations
```
GET    /api/v1/node/status        # Node status
POST   /api/v1/node/configure     # Update configuration
GET    /api/v1/node/peers         # List connected peers
```

#### Storage Operations
```
GET    /api/v1/storage/stats      # Storage statistics
POST   /api/v1/storage/validate   # Trigger validation
```

## 10. Development Roadmap

### Phase 1: Core Implementation
- Basic file storage and retrieval
- P2P networking
- DHT implementation
- Basic smart contracts

### Phase 2: Enhanced Features
- Web interface
- Mobile app integration
- Advanced encryption options
- Bandwidth optimization

### Phase 3: Production Readiness
- Performance optimization
- Security auditing
- Documentation
- Community tools

### Future Expansion
1. **Mobile Integration**
   ```rust
   pub trait MobileService {
       fn initialize(&self, config: MobileConfig) -> Result<()>;
       fn background_sync(&self) -> Result<()>;
       fn get_storage_status(&self) -> Result<MobileStorageStatus>;
   }
   ```

2. **Desktop Application**
   ```rust
   pub struct DesktopApp {
       node: Arc<BlocsNode>,
       ui: TauriApp,
       system_tray: SystemTray,
   }
   ```

3. **Browser Extension**
   ```rust
   pub trait BrowserInterface {
       fn connect_node(&self) -> Result<()>;
       fn quick_store(&self, data: &[u8]) -> Result<String>;
       fn quick_retrieve(&self, id: &str) -> Result<Vec<u8>>;
   }
   ```

## Implementation Notes

### Error Handling
```rust
#[derive(Debug, thiserror::Error)]
pub enum BlocsError {
    #[error("Network error: {0}")]
    Network(#[from] NetworkError),
    #[error("Storage error: {0}")]
    Storage(#[from] StorageError),
    #[error("Contract error: {0}")]
    Contract(#[from] ContractError),
    #[error("Validation error: {0}")]
    Validation(#[from] ValidationError),
    #[error("Configuration error: {0}")]
    Config(#[from] ConfigError),
}
```

### Configuration
```rust
#[derive(Debug, Deserialize)]
pub struct NodeConfig {
    pub network: NetworkConfig,
    pub storage: StorageConfig,
    pub contract: ContractConfig,
    pub api: ApiConfig,
}

impl NodeConfig {
    pub fn from_file(path: PathBuf) -> Result<Self>;
    pub fn validate(&self) -> Result<()>;
}
```

### Logging
```rust
#[derive(Debug)]
pub struct Logger {
    pub level: LogLevel,
    pub output: LogOutput,
}

impl Logger {
    pub fn init(config: LogConfig) -> Result<()>;
    pub fn set_level(&mut self, level: LogLevel);
}
```
