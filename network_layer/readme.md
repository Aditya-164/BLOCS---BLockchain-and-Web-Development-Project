# Network Layer Module

## Features

This Python module implements a simple peer-to-peer (P2P) network framework using TCP/IP connections. The network is based on a decentralized architecture where each node can communicate with other nodes directly without the need for a central server.

## How it Works

The network is built around the concept of a "Genesis Node" - a single node that every other node in the network knows the IP address and port of. When a new node wants to join the network, it first connects to the Genesis Node to discover other existing nodes.

The general flow of joining the network is as follows:

1. The new node (called the "Candidate Node") connects to the Genesis Node.
2. The Candidate Node asks the Genesis Node for the address of a random node already in the network.
3. The Genesis Node responds with the address of a random existing node.
4. The Candidate Node then connects to the random node and asks for the list of all nodes in the network.
5. The random node sends the Candidate Node the list of all known nodes in the network.
6. The Candidate Node then connects to all the nodes in the list and joins the network.
7. The Candidate Node then broadcasts a message to the network, informing all other nodes that it has joined.

## Network Setup

The module provides three main methods for setting up the network:

1. `start()`: Start the node on a specific port
2. `join_network()`: Join the network by connecting to the Genesis Node 
3. `stop()`: Stop the node and close all connections

## Message Communication

The module provides three main methods for communication between nodes:

1. `broadcast()`: Send a message to all nodes in the network
2. `send()`: Send a direct message to a specific node
3. `reply()`: Reply to a received message

The `Node` class also provides a handler method `handle_message()` that can be overridden to process incoming messages

### Message Format

Messages are sent in JSON format with the following structure:

```json
{
    "id": "fbc019f3a87787f904b54875f62e2193445f0e0f4e82f6978d77dbe29d7a9894",
    "title": "#BROADCAST",
    "message": "Hello world",
    "time": 1617555967.1199386,
    "sender_ip": "192.168.1.100",
    "sender_port": 5050
}
```

## Usage

### Creating a Genesis Node

```python
from Network import Network

genesis_node = Network("localhost")  # Use "localhost" for local testing, or the actual IP address
genesis_node.start(5050)  # Start the server on port 5050

# The Genesis Node is now running and ready to accept connections
```

### Joining the Network

```python
from Network import Network

new_node = Network("localhost")
new_node.start(5051)  # Start the server on a different port
new_node.join_network()  # Join the network
```

### Sending Messages

#### Broadcasting Messages

```python
# Send a broadcast message to all nodes
node.broadcast("Hello, P2P network!")
```

#### Sending Direct Messages

```python
# Create a message
message = node.short_json_msg("#DIRECT_MESSAGE", "Hello specific node!")

# Send the message and wait for response (hasResponse=1)
response = node.send(connection, message, hasResponse=1)

# Send message without waiting for response
node.send(connection, message, hasResponse=0)
```

#### Replying to Messages

```python
# Reply to a received message
def handle_message(self, conn, message):
    # Process the received message
    response = self.short_json_msg("#REPLY", "Message received!")
    self.reply(conn, response)
```

### Example: Interactive Chat Node

Here's an example of how to create an interactive chat node that can send and receive messages:

```python
from Network import Network
import threading

class ChatNode:
    def __init__(self, ip="localhost", port=5050):
        self.network = Network(ip)
        self.network.start(port)
        
        if port != 5050:  # If not genesis node
            self.network.join_network()
        
        # Start listening for messages in a separate thread
        self.listen_thread = threading.Thread(target=self.listen_for_messages)
        self.listen_thread.daemon = True
        self.listen_thread.start()
    
    def listen_for_messages(self):
        while True:
            # Handle incoming messages
            pass
    
    def send_message(self, message):
        self.network.broadcast(message)
    
    def send_direct_message(self, recipient_conn, message):
        msg = self.network.short_json_msg("#DIRECT_MESSAGE", message)
        response = self.network.send(recipient_conn, msg, hasResponse=1)
        return response

# Usage
if __name__ == "__main__":
    # Create a chat node
    node = ChatNode(port=5051)
    
    # Main loop for sending messages
    while True:
        message = input("Enter message: ")
        if message.lower() == 'quit':
            break
        node.send_message(message)
```

## Message Types

The module supports several types of messages:

1. `#BROADCAST`: Send to all nodes in the network
2. `#NODE_CON_ADDR`: Used when establishing connections
3. `#DIRECT_MESSAGE`: Send to a specific node
4. `#REPLY`: Used for responses
5. `#GIVE_NODES_IN_NETWORK`: Request network node list
6. `#JOINED_IN_NETWORK`: Broadcast when a new node joins

### Creating Custom Messages

```python
# Create a custom message
message = node.short_json_msg(
    title="#CUSTOM_MESSAGE",
    message="Your message content"
)
```
