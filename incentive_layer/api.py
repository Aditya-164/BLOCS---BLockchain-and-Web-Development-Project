from .config import contract, w3
import time
import random
import string
from web3 import Web3
# import json
# from eth_typing import HexStr
# from eth_utils import to_bytes

# function from client to propose a deal


def propose_deal(client_address, value, client_private_key, file_id, storage_space, duration_hours):
    try:
        file_id = w3.keccak(text=file_id)
        # print(type(file_id))
        block_number = w3.eth.block_number
        print(f"Current block number: {block_number}")

        # block = w3.eth.get_block('latest')
        # print(f"Block number: {block.number}")
        # print(f"Block timestamp: {block.timestamp}")
        # Build transaction
        # gas_estimate = contract.functions.proposeDeal(file_id, storage_space, duration_hours).estimate_gas({
        #     'from': client_address
        # })
        transaction = contract.functions.proposeDeal(file_id, storage_space, duration_hours).build_transaction({
            'value': value,
            'from': client_address,
            'gas': 6721975,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(client_address)
        })
        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=client_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt['status'] == 1:
            return w3.to_hex(tx_hash)
        else:
            raise Exception(f"Transaction failed: {tx_receipt}")
    except Exception as e:
        print(f"Error while proposing deal: {str(e)}")
        raise

# Client function


def validate_proof(file_id, client_address, client_private_key):
    try:
        # Estimate gas first to check if the transaction will fail
        file_id = w3.keccak(text=file_id)
        # gas_estimate = contract.functions.validateProof(file_id).estimate_gas({
        #     'from': client_address
        # })
        print(f"FROM VALIDAPI{client_address}")
        # Build transaction with estimated gas
        transaction = contract.functions.validateProof(file_id).build_transaction({
            'from': client_address,
            'gas': 6721975,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(client_address)
        })

        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=client_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt['status'] == 1:
            return w3.to_hex(tx_hash)
        else:
            raise Exception(f"Transaction failed: {tx_receipt}")

    except Exception as e:
        print(
            f"[validate_proof]: Error while executing validate_proof {str(e)}")
        raise

# Server calls approve deal to check if billing_amount == promised_amount


def approve_deal(file_id, billing_amount, server_address, server_private_key):
    try:
        # block_number = w3.eth.block_number
        # print(f"Current block number: {block_number}")
        file_id = w3.keccak(text=file_id)
        block = w3.eth.get_block('latest')
        gas_estimate = contract.functions.approveDeal(file_id, billing_amount).estimate_gas({
            'from': server_address
        })
        transaction = contract.functions.approveDeal(file_id, billing_amount).build_transaction({
            'from': server_address,
            'gas': 6721975,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(server_address)
        })
        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=server_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt['status'] == 1:
            return w3.to_hex(tx_hash)
        else:
            raise Exception(f"Transaction failed: {tx_receipt}")

    except Exception as e:
        print(f"Error while approving deal: {str(e)}")
        raise


# Client calls to invalidate the deal, due to no response or intentional
def invalidate_deal(file_id, reason, client_address, client_private_key):
    try:
        # gas_estimate = contract.functions.invalidateDeal(file_id, reason).estimate_gas({
        #     'from': my_address
        # })
        file_id = w3.keccak(text=file_id)
        print(f"FROM INVALIDAPI{client_address}")

        transaction = contract.functions.invalidateDeal(file_id, reason).build_transaction({
            'from': client_address,
            'gas': 6721975,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(client_address)
        })
        signed_txn = w3.eth.account.sign_transaction(
            transaction, private_key=client_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        if tx_receipt['status'] == 1:
            return w3.to_hex(tx_hash)
        else:
            raise Exception(f"Transaction failed: {tx_receipt}")
    except Exception as e:
        print(f"Error while invalidating deal: {str(e)}")
        raise


def complete_deal(file_id, client_address, client_private_key) -> dict:
    try:
        file_id = w3.keccak(text=file_id)
        tx = contract.functions.completeDeal(file_id).build_transaction({
            'from': client_address,
            'gas': 6721975,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(client_address),
        })

        signed_tx = w3.eth.account.sign_transaction(
            tx, private_key=client_private_key)  # Replace with your private key
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        deal_completed_event = contract.events.DealCompleted().process_receipt(tx_receipt)
        if deal_completed_event:
            print(f"Deal completed for file ID: {file_id}")

        return tx_receipt

    except Exception as e:
        print(f"Error completing deal: {str(e)}")
        raise

# anyone can call this function


def get_deal_status(file_id):
    file_id = w3.keccak(text=file_id)
    deal = contract.functions.files(file_id).call()
    return {
        "client": deal[0],
        "storageProvider": deal[1],
        "startTime": deal[2],
        "duration": deal[3],
        "storageSpace": deal[4],
        "totalAmount": deal[5],
        "remainingAmount": deal[6],
        "lastValidationTime": deal[7],
        "isActive": deal[8],
        "isApproved": deal[9]
    }

"""
client_address = '0xaE0e33E28AEE05144711F5000bC763e3145323ea'
client_private_key = '0x8cde6b6f4acffa0093bb703f9aee6e4384b4f89235fe959c7e1633973932c280'

server_address = '0xE70EB10De1E4F50050D6169D0985d93E92b3A322'
server_private_key = '0x93f9a5010d72cc1cbf7e72229f605312791b594b1f181e7d1804979389af201c'


propose_deal(client_address, 20, client_private_key, 'DEALOFTHEYEAR', 10, 2)

# Approve a deal (no Ether involved)
approve_deal('DEALOFTHEYEAR', 20, server_address, server_private_key)

# Validate proof (no Ether involved)
validate_proof('DEALOFTHEYEAR', client_address, client_private_key)


# Invalidate a deal (no Ether involved)
# invalidate_deal('DEALOFTHEYEAR', 'Reason for invalidation', client_address, client_private_key)

# Complete a deal (no Ether involved)
complete_deal(w3, contract, 'DEALOFTHEYEAR', client_address, client_private_key)

# Get the deal status (no Ether involved)
deal_status = get_deal_status('DEALOFTHEYEAR')
"""
