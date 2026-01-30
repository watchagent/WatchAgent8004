"""
Utility Functions for Watch8004
Helper functions for contract interaction and data management
"""

import json
import os
from typing import List, Dict


def load_contract_abi(contract_name: str) -> List[Dict]:
    """
    Load contract ABI from file
    
    Args:
        contract_name: Name of the contract
        
    Returns:
        Contract ABI as list of dicts
    """
    abi_path = f"contracts/out/{contract_name}.abi.json"
    
    if not os.path.exists(abi_path):
        raise FileNotFoundError(
            f"ABI file not found: {abi_path}\n"
            f"Please compile contracts first using: cd contracts && forge build"
        )
    
    with open(abi_path, "r") as f:
        return json.load(f)


def load_deployment_info() -> Dict:
    """
    Load deployment information
    
    Returns:
        Deployment info dict
    """
    deployment_path = "contracts/deployment.json"
    
    if not os.path.exists(deployment_path):
        raise FileNotFoundError(
            f"Deployment file not found: {deployment_path}\n"
            f"Please deploy contracts first using: python scripts/deploy.py"
        )
    
    with open(deployment_path, "r") as f:
        return json.load(f)


def format_address(address: str, length: int = 10) -> str:
    """
    Format Ethereum address for display
    
    Args:
        address: Full Ethereum address
        length: Number of characters to show from each end
        
    Returns:
        Formatted address string
    """
    if len(address) < length * 2:
        return address
    
    return f"{address[:length]}...{address[-length:]}"


def format_transaction_hash(tx_hash: str, length: int = 10) -> str:
    """
    Format transaction hash for display
    
    Args:
        tx_hash: Transaction hash
        length: Number of characters to show from each end
        
    Returns:
        Formatted hash string
    """
    return format_address(tx_hash, length)


def save_json(data: Dict, filepath: str, pretty: bool = True):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        filepath: Output file path
        pretty: Whether to pretty-print JSON
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w") as f:
        if pretty:
            json.dump(data, f, indent=2)
        else:
            json.dump(data, f)


def load_json(filepath: str) -> Dict:
    """
    Load data from JSON file
    
    Args:
        filepath: Input file path
        
    Returns:
        Loaded data
    """
    with open(filepath, "r") as f:
        return json.load(f)


def validate_private_key(private_key: str) -> bool:
    """
    Validate Ethereum private key format
    
    Args:
        private_key: Private key string
        
    Returns:
        True if valid, False otherwise
    """
    if not private_key:
        return False
    
    # Remove 0x prefix if present
    if private_key.startswith("0x"):
        private_key = private_key[2:]
    
    # Check length (should be 64 hex characters)
    if len(private_key) != 64:
        return False
    
    # Check if all characters are valid hex
    try:
        int(private_key, 16)
        return True
    except ValueError:
        return False


def calculate_gas_cost(gas_used: int, gas_price: int) -> float:
    """
    Calculate gas cost in ETH
    
    Args:
        gas_used: Amount of gas used
        gas_price: Gas price in Wei
        
    Returns:
        Cost in ETH
    """
    return (gas_used * gas_price) / 10**18


def wei_to_eth(wei: int) -> float:
    """
    Convert Wei to ETH
    
    Args:
        wei: Amount in Wei
        
    Returns:
        Amount in ETH
    """
    return wei / 10**18


def eth_to_wei(eth: float) -> int:
    """
    Convert ETH to Wei
    
    Args:
        eth: Amount in ETH
        
    Returns:
        Amount in Wei
    """
    return int(eth * 10**18)
