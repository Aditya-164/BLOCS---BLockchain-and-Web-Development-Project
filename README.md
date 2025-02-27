# README for Decentralized P2P File Storage Network (BLOCS)

## Overview

**BLOCS (Blockchain-based Ledger for Open Cloud Storage)** is a decentralized peer-to-peer (P2P) cloud storage system. It leverages blockchain technology, Proof-of-Storage (PoS) consensus, and a token-based economy to create a distributed, secure, and privacy-preserving network where users can store and retrieve files without relying on centralized cloud providers. The project includes secure file sharding, encryption, a transparent storage ledger, and an incentive layer for participants.

## Table of Contents
1. [Features](#features)
2. [System Components](#system-components)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Architecture](#architecture)
6. [Security Considerations](#security-considerations)
7. [Advantages](#advantages)
8. [Future Work](#future-work)

## Features

- **Decentralized File Storage**: Data is divided into encrypted fragments (shards) and distributed across multiple nodes, enhancing privacy and fault tolerance.
- **Proof-of-Storage Consensus**: Ensures that nodes are genuinely holding data without revealing the data itself.
- **Token Economy**: Nodes earn tokens as rewards for storing data and are penalized for failure to provide storage.
- **End-to-End Encryption**: Files are encrypted client-side, ensuring privacy and control over data access.
- **Zero-Knowledge Proofs (ZKPs)**: Used to validate storage without exposing file contents.

## System Components

The system comprises four major layers:

### 1. Blockchain Layer
A blockchain ledger stores storage transactions, ensuring transparency, immutability, and secure file ownership tracking. Key operations include:
- **Storage Registration**: Nodes announce available storage capacity.
- **Storage Proofs**: Periodic challenges require nodes to prove data possession.
- **Rewards and Penalties**: Nodes earn tokens for validated storage; penalties apply for non-compliance.

### 2. Storage Layer
Responsible for data distribution and retrieval:
- **File Sharding and Encryption**: Files are encrypted and split into shards, which are distributed across the network.
- **Redundancy and Availability**: Techniques such as replication ensure data remains accessible even if nodes go offline.

### 3. Incentive Layer
A token-based economy incentivizes nodes to participate:
- **Earning Tokens**: Nodes storing data earn tokens.
- **Storage Payments**: Users pay tokens to upload data.
- **Smart Contracts**: Automated management of token rewards and penalties.

### 4. File Management
Handles file upload, metadata storage, and retrieval:
- **File Upload**: Files are split, encrypted, and distributed, with metadata stored on the blockchain.
- **File Retrieval**: Shards are retrieved from peers, decrypted, and reassembled.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/BLOCS.git
   cd BLOCS
   ```

2. **Install Dependencies**
   The project requires Python 3.x and the following packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Ethereum Client**
   Ensure a connection to an Ethereum client like Ganache or a test network, as BLOCS uses smart contracts for token transactions.

## Usage

### Running the CLI

1. **Start Genesis Node** (for the first node only):
   ```bash
   python setup.py
   ```
   When prompted:
   - Choose "yes" for Genesis node.
   - Enter port (e.g., 5050).
   - Provide your Ethereum client address and private key.

2. **Join Network as a Peer Node**:
   ```bash
   python setup.py
   ```
   When prompted:
   - Choose "no" for Genesis node.
   - Enter port.
   - Enter the Genesis node's IP.
   - Provide your Ethereum client address and private key.

3. **Commands**:
   - **Upload File**:
     ```bash
     upload
     ```
     Provide the file path and desired duration (in timesteps) for storage.
   - **Download File**:
     ```bash
     download
     ```
     Provide details for all uploaded files on network.
   - **List Files**:
     ```bash
     list
     ```
   - **List Peers**:
     ```bash
     peers
     ```
   - **Exit**:
     ```bash
     exit
     ```

### Key File Operations

- **Distribute File**: Uploads, shreds, encrypts, and stores a file across the network.
- **Retrieve File**: Gathers shards from peers and reassembles the original file.

## Architecture

1. **Decentralized Storage Layer**: Distributes encrypted file shards across the network.
2. **Blockchain Layer**: Uses Proof-of-Storage consensus for transparency, security, and token distribution.
3. **File Retrieval**: Queries blockchain metadata for shard locations, retrieves shards from nodes, and reconstructs the file.

### Proof-of-Storage Protocol

The protocol enables nodes to prove file possession by generating and verifying cryptographic proofs (Zero-Knowledge Proofs). These proofs occur at regular intervals and secure token rewards or apply penalties based on proof validity.

## Security Considerations

1. **End-to-End Encryption**: Files are encrypted on the client side, ensuring only the owner has access.
2. **Zero-Knowledge Proofs (ZKPs)**: Enable nodes to prove data storage without exposing file contents.
3. **Token Penalties**: Nodes failing to respond to proof requests may face token slashing, ensuring network reliability.

## Advantages

- **Decentralization**: Eliminates single points of failure.
- **Security**: Strong encryption and sharding protect user data.
- **Transparency**: Immutable blockchain ledger records all actions.
- **Incentive Model**: Token rewards encourage active participation.
- **Privacy**: End-to-end encryption ensures data confidentiality.

## Future Work

- **Scalability**: Incorporating off-chain solutions for high transaction volume.
- **Data Availability**: Enhancing retrieval processes for large-scale deployment.
- **Governance**: Potential integration of decentralized governance models.
- **Redundancy**: Implementing additional fault tolerance mechanisms.
