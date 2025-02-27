# Network Layer

# Network Layer Documentation

This module implements a peer-to-peer network infrastructure using PyP2P for decentralized communication.

## Overview
The network layer provides a foundation for creating and managing distributed networks where each node can communicate directly with other nodes without central coordination.

## Components

### Node Class
A standard peer node that can:
- Connect to other peers
- Send and receive messages
- Maintain peer connections
- Handle network events

### BootstrapNode Class
A specialized node that:
- Serves as the network entry point
- Maintains a registry of active peers
- Facilitates peer discovery
- Provides initial network configuration

## Implementation Details
- Uses UDP for peer discovery
- TCP for reliable data transfer
- Implements heartbeat mechanism for connection monitoring
- Handles peer churn (peers joining/leaving network)

## Configuration
The system can be configured through `config.py`:
- Network ports
- Bootstrap node address
- Connection timeouts
- Maximum peer connections

## Example Setup
1. Start a bootstrap node:
```python
from network_layer import BootstrapNode

bootstrap = BootstrapNode(
port=5000,
host='localhost',
max_peers=50
)
bootstrap.start()
```

2. Start regular peer nodes:
```python
from network_layer import Node

peer = Node(
bootstrap_addr=('localhost', 5000),
port=5001
)
peer.connect()
```

## Usage Examples

### Sending Messages
```python
# Send a message to a specific peer
peer.send_message(target_peer_id, "Hello!")

# Broadcast to all connected peers
peer.broadcast("Network announcement")
```

### Event Handling
```python
# Define custom event handlers
@peer.on_message
def handle_message(sender_id, message):
print(f"Received from {sender_id}: {message}")

@peer.on_peer_join
def peer_joined(peer_id):
print(f"New peer joined: {peer_id}")
```

## Error Handling
The system includes robust error handling for:
- Network disconnections
- Invalid messages
- Peer timeouts
- Connection failures

## Testing
Run the test suite:
```bash
python -m pytest tests/network_tests.py
```