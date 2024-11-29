# aptos-python-sniper-bot

A Python-based sniper bot for interacting with the **Aptos blockchain**. This bot allows you to send token transactions to any recipient on the Aptos network by signing transactions with your private key. It uses the **Aptos API** for submitting transactions and can be customized to automate token transfers.

## Features:
- **Sign and Send Transactions**: Sign transactions locally using your private key and send them to the Aptos network.
- **Configurable**: Easily set your Aptos wallet address, recipient address, and transfer amount.
- **Secure**: Private key management via environment variables to ensure security.

## Setup:
1. Set your `APTOS_PRIVATE_KEY` and `APTOS_WALLET_ADDRESS` as environment variables.
2. Install the required dependencies:
   ```bash
   pip install requests eth-account

3. Run the bot to send a token transfer to a specified recipient:

    python sniper_bot.py

Requirements:

    Python 3.x
    requests, eth-account libraries

Example Usage:

python sniper_bot.py
