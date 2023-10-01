import web3
from web3 import Web3
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize web3.py with an Ethereum provider URL
provider_url = os.getenv("ETHEREUM_PROVIDER_URL")  # Set your Ethereum provider URL
w3 = Web3(Web3.HTTPProvider(provider_url))

# Set your contract address
contract_address = "0xYourContractAddress"

# Load your contract ABI
with open("MyNFT.json") as json_file:  # Replace with the path to your contract's ABI JSON file
    contract_abi = json.load(json_file)

# Initialize the contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Your Ethereum wallet private key (for signing transactions)
private_key = os.getenv("PRIVATE_KEY")

# The address you want to mint NFT to
to_address = "0xRecipientAddress"

# The NFT token ID you want to mint
token_id = 1

# Check if the address is the owner of the contract
is_owner = contract.functions.owner().call() == w3.toChecksumAddress(to_address)

if is_owner:
    # Sign and send a transaction to mint the NFT
    nonce = w3.eth.getTransactionCount(w3.toChecksumAddress(private_key))
    transaction = contract.functions.mint(w3.toChecksumAddress(to_address), token_id).buildTransaction({
        "chainId": 1,  # Ethereum mainnet
        "gas": 2000000,  # Set an appropriate gas limit
        "gasPrice": w3.toWei("10", "gwei"),  # Set an appropriate gas price
        "nonce": nonce,
    })
    signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    print(f"Transaction sent: https://etherscan.io/tx/{tx_hash.hex()}")
else:
    print("You are not the owner of the contract.")
