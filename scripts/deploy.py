"""
Smart Contract Deployment Script
Deploys ERC-8004 registry contracts
"""

import json
import os
from web3 import Web3
from eth_account import Account
from solcx import compile_standard, install_solc


def compile_contract(contract_name: str) -> dict:
    """
    Compile Solidity contract
    
    Args:
        contract_name: Name of the contract (e.g., "IdentityRegistry")
        
    Returns:
        Compiled contract data
    """
    contract_path = f"contracts/src/{contract_name}.sol"
    
    if not os.path.exists(contract_path):
        raise FileNotFoundError(f"Contract not found: {contract_path}")
    
    with open(contract_path, "r") as f:
        contract_source = f.read()
    
    # Install solc if needed
    try:
        install_solc("0.8.20")
    except:
        pass
    
    # Compile
    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                f"{contract_name}.sol": {"content": contract_source}
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version="0.8.20",
    )
    
    # Extract bytecode and ABI
    contract_data = compiled["contracts"][f"{contract_name}.sol"][contract_name]
    
    return {
        "abi": contract_data["abi"],
        "bytecode": contract_data["evm"]["bytecode"]["object"]
    }


def deploy_contract(
    w3: Web3,
    account: Account,
    contract_data: dict,
    contract_name: str
) -> str:
    """
    Deploy a smart contract
    
    Args:
        w3: Web3 instance
        account: Ethereum account
        contract_data: Compiled contract data
        contract_name: Name of contract
        
    Returns:
        Deployed contract address
    """
    print(f"   Deploying {contract_name}...")
    
    # Create contract instance
    contract = w3.eth.contract(
        abi=contract_data["abi"],
        bytecode=contract_data["bytecode"]
    )
    
    # Build deployment transaction
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Estimate gas
    try:
        gas_estimate = contract.constructor().estimate_gas({
            'from': account.address
        })
        gas_limit = int(gas_estimate * 1.2)  # Add 20% buffer
    except:
        gas_limit = 3000000  # Fallback
    
    txn = contract.constructor().build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': gas_limit,
        'gasPrice': w3.eth.gas_price
    })
    
    # Sign and send transaction
    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    # Wait for receipt
    print(f"   Transaction sent: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt['status'] == 1:
        print(f"   ✅ {contract_name} deployed at: {receipt['contractAddress']}")
        return receipt['contractAddress']
    else:
        raise Exception(f"Deployment failed for {contract_name}")


def save_contract_abi(contract_name: str, abi: list):
    """
    Save contract ABI to file
    
    Args:
        contract_name: Name of contract
        abi: Contract ABI
    """
    os.makedirs("contracts/out", exist_ok=True)
    
    with open(f"contracts/out/{contract_name}.abi.json", "w") as f:
        json.dump(abi, f, indent=2)


def deploy_contracts(
    rpc_url: str = "http://127.0.0.1:8545",
    private_key: str = None
) -> dict:
    """
    Deploy all ERC-8004 registry contracts
    
    Args:
        rpc_url: Blockchain RPC URL
        private_key: Deployer private key
        
    Returns:
        Dict with deployed contract addresses
    """
    # Setup Web3
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # if not w3.is_connected():
    #     raise Exception("Failed to connect to blockchain")
    
    # Setup account
    if not private_key:
        # Use default Anvil account for testing
        private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    
    account = Account.from_key(private_key)
    
    print(f"\n   Connected to blockchain (Chain ID: {w3.eth.chain_id})")
    print(f"   Deployer address: {account.address}")
    print(f"   Balance: {w3.eth.get_balance(account.address) / 10**18:.4f} ETH")
    
    deployed = {}
    
    # Deploy Identity Registry
    print(f"\n1️⃣  Identity Registry")
    try:
        identity_data = compile_contract("IdentityRegistry")
        identity_address = deploy_contract(w3, account, identity_data, "IdentityRegistry")
        save_contract_abi("IdentityRegistry", identity_data["abi"])
        deployed['identity'] = identity_address
    except Exception as e:
        print(f"   ❌ Error: {e}")
        raise
    
    # Deploy Reputation Registry
    print(f"\n2️⃣  Reputation Registry")
    try:
        reputation_data = compile_contract("ReputationRegistry")
        reputation_address = deploy_contract(w3, account, reputation_data, "ReputationRegistry")
        save_contract_abi("ReputationRegistry", reputation_data["abi"])
        deployed['reputation'] = reputation_address
    except Exception as e:
        print(f"   ❌ Error: {e}")
        raise
    
    # Deploy Validation Registry
    print(f"\n3️⃣  Validation Registry")
    try:
        validation_data = compile_contract("ValidationRegistry")
        validation_address = deploy_contract(w3, account, validation_data, "ValidationRegistry")
        save_contract_abi("ValidationRegistry", validation_data["abi"])
        deployed['validation'] = validation_address
    except Exception as e:
        print(f"   ❌ Error: {e}")
        raise
    
    # Save deployment info
    deployment_info = {
        "network": {
            "rpc_url": rpc_url,
            "chain_id": w3.eth.chain_id
        },
        "deployer": account.address,
        "contracts": deployed
    }
    
    with open("contracts/deployment.json", "w") as f:
        json.dump(deployment_info, f, indent=2)
    
    print(f"\n   💾 Deployment info saved to contracts/deployment.json")
    
    return deployed


if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    
    load_dotenv()
    
    rpc_url = os.getenv("RPC_URL", "http://127.0.0.1:8545")
    private_key = os.getenv("PRIVATE_KEY")
    
    try:
        contracts = deploy_contracts(rpc_url, private_key)
        print(f"\n✅ All contracts deployed successfully!")
        for name, address in contracts.items():
            print(f"   {name.capitalize()}: {address}")
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        sys.exit(1)
