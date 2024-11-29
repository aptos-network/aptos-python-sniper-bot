import os
import requests
from eth_account import Account
import json

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Replace with your actual Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Make sure to set your private key as an environment variable
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Your Aptos wallet address
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient's address
AMOUNT = 100  # Amount to transfer (in the smallest unit, like tokens)

# Function to sign the transaction
def sign_transaction(private_key, transaction_data):
    account = Account.privateKeyToAccount(private_key)
    signed_txn = account.sign_transaction(transaction_data)
    return signed_txn.rawTransaction

# Function to send the transaction to Aptos API
def send_transaction(private_key, recipient, amount):
    try:
        # Prepare the transaction data (this may vary depending on the API's requirements)
        transaction_data = {
            'sender': WALLET_ADDRESS,
            'recipient': recipient,
            'amount': amount
        }
        
        # Sign the transaction using the private key
        signed_transaction = sign_transaction(private_key, transaction_data)
        
        # Send the signed transaction to the Aptos API
        response = requests.post(f'{APTOS_API_URL}/api/transactions', json={'signedTransaction': signed_transaction.hex()})

        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()
        else:
            print(f"Error sending transaction: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main function to start the bot
def sniper_bot():
    print("Starting sniper bot...")

    # Send the transaction
    result = send_transaction(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT)

    if result:
        print(f"Transaction result: {json.dumps(result, indent=4)}")
    else:
        print("Failed to send transaction.")

if __name__ == '__main__':
    sniper_bot()
