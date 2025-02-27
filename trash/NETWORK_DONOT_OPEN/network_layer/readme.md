# Network Layer Module

## Overview

The `network_layer` module provides a framework to create a decentralized network with peer-to-peer communication capabilities. It includes a `Node` class for general peer nodes and a `BootstrapNode` class that serves as a discovery point for new nodes joining the network. The module supports sending and broadcasting data packets across nodes and includes features for error handling, retry logic, and detailed logging.

---

## Directory Structure

The `network_layer` directory is organized as follows:

```
network_layer/
├── __init__.py            # Initializes the package
├── config.py              # Configuration settings for the network
├── node.py                # Node class for general nodes in the network
├── bootstrap_node.py      # BootstrapNode class for initial discovery nodes
├── handlers.py            # Data packet and handler definitions
├── logger.py              # Logger setup for logging network activity
├── readme.md              # Documentation
└── utils.py               # Utility functions for creating and connecting sockets
```

---

## Configuration

The `config.py` file includes settings used across the module:

- `MAX_CONNECTIONS`: Maximum number of simultaneous connections allowed per node.
- `BUFFER_SIZE`: Buffer size for data transmission.
- `TIMEOUT`: Timeout in seconds for network connections.
- `RETRY_COUNT`: Number of times a node retries connection to a peer on failure.

---

## Classes and Methods

### Node Class

The `Node` class represents a general peer in the network. Nodes can connect to a `BootstrapNode` to discover peers and communicate with them directly.

#### Constructor
```python
Node(node_id: int, host: str, port: int, bootstrap_address: tuple = None)
```

- `node_id` (int): Unique identifier for the node.
- `host` (str): Host address of the node.
- `port` (int): Port on which the node listens.
- `bootstrap_address` (tuple): Optional, address `(host, port)` of the `BootstrapNode` for peer discovery.

#### Key Methods
- `start_node()`: Starts the node and connects to the bootstrap server if provided.
- `send_data(peer, data)`: Sends a data packet to a specific peer identified by `(peer_id, peer_host, peer_port)`.
- `broadcast_data(data)`: Broadcasts a data packet to all connected peers.
- `handle_data(packet)`: Processes received data packets. This can be customized as needed.
- `shutdown()`: Shuts down the node, closes sockets, and stops listening for connections.
- `get_peers()`: Returns a list of connected peers as `(peer_id, peer_host, peer_port)` tuples.

### BootstrapNode Class

The `BootstrapNode` class inherits from `Node` and functions as a central discovery point, storing a list of connected peers and sharing it with new nodes joining the network.

#### Constructor
```python
BootstrapNode(node_id: int, host: str, port: int)
```

- `node_id` (int): Unique identifier for the bootstrap node.
- `host` (str): Host address of the bootstrap node.
- `port` (int): Port on which the bootstrap node listens.

#### Key Methods
- `start_bootstrap_node()`: Starts the bootstrap node to listen for incoming peer connections.
- `shutdown()`: Shuts down the bootstrap node, closing all connections and logging the shutdown.

---

## Usage Examples

### 1. Starting a Bootstrap Node

To initialize and start a bootstrap node:
```python
from network_layer.bootstrap_node import BootstrapNode

bootstrap_node = BootstrapNode(node_id=1, host="localhost", port=8000)
bootstrap_node.start_bootstrap_node()
```

This will create a central discovery point that new nodes can connect to and retrieve a list of active peers.

### 2. Starting a General Node

To initialize and start a general node, passing the bootstrap address to enable peer discovery:
```python
from network_layer.node import Node

node = Node(node_id=2, host="localhost", port=8001, bootstrap_address=("localhost", 8000))
node.start_node()
```

When this node starts, it connects to the bootstrap node, retrieves the list of peers, and attempts to establish connections with them.

### 3. Sending and Broadcasting Data

To send a data packet to a specific peer:
```python
# Assuming peer = (peer_id, peer_host, peer_port)
node.send_data(peer=("3", "localhost", 8002), data="Hello, Peer 3!")
```

To broadcast a message to all connected peers:
```python
node.broadcast_data(data="Hello, everyone!")
```

### 4. Handling Data Packets

The `Node` class has a `handle_data` method that can be customized to define how each node should handle incoming data. By default, this method uses `DataHandler` to print received data. You can override `handle_data` as needed:
```python
def custom_handle_data(self, packet):
    print(f"Custom handler: Node {self.node_id} received packet: {packet}")

node.handle_data = custom_handle_data.__get__(node, Node)  # Bind custom handler
```

### 5. Shutting Down a Node

To gracefully shut down a node:
```python
node.shutdown()
```

This will close the socket, terminate active connections, and log the shutdown.

---

## Logging

The module uses Python’s `logging` module to track events, errors, and network activity. Logs are saved in `network.log` and provide information about:
- Node start and shutdown events.
- Peer connections and disconnections.
- Data packet transmissions.
- Connection failures and retry attempts.

The logging setup can be customized in `logger.py`:
```python
# Example of logging setup in logger.py
import logging

logging.basicConfig(
    filename="network.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger("NetworkLayer")
```

---

## Error Handling and Retry Logic

The module includes error handling for various network operations:
- **Graceful Cleanup**: Nodes automatically close sockets and terminate threads on errors.
- **Retry Logic**: Nodes retry connecting to peers up to `RETRY_COUNT` times in case of failures.
- **Logging Errors**: Errors are logged with appropriate log levels (`WARNING` for retries, `ERROR` for unrecoverable failures).

For instance, if a connection to a peer fails, the module will retry and log each attempt, only logging an error if all retries are exhausted.

---

## Example Workflow

1. **Start Bootstrap Node**: Initialize and start the bootstrap node to enable peer discovery.
2. **Start General Nodes**: Create general nodes, passing the bootstrap node’s address for peer discovery.
3. **Exchange Data**: Nodes can send data to specific peers or broadcast to all peers.
4. **Shutdown**: Gracefully shut down nodes when no longer needed.



