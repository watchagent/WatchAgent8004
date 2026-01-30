"""
ERC-8004 Base Agent Implementation
Provides core functionality for ERC-8004 compliant AI agents
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from web3 import Web3
from eth_account import Account
import requests


class ERC8004BaseAgent:
    """Base class for ERC-8004 compliant AI agents"""
    
    def __init__(
        self,
        name: str,
        domain: str,
        private_key: str,
        rpc_url: str = "http://127.0.0.1:8545",
        identity_registry_address: Optional[str] = None,
        reputation_registry_address: Optional[str] = None,
        validation_registry_address: Optional[str] = None
    ):
        """
        Initialize ERC-8004 Base Agent
        
        Args:
            name: Agent name
            domain: Agent domain (unique identifier)
            private_key: Ethereum private key
            rpc_url: Blockchain RPC endpoint
            identity_registry_address: Identity Registry contract address
            reputation_registry_address: Reputation Registry contract address
            validation_registry_address: Validation Registry contract address
        """
        self.name = name
        self.domain = domain
        self.private_key = private_key
        
        # Web3 setup
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        
        # Contract addresses
        self.identity_registry_address = identity_registry_address
        self.reputation_registry_address = reputation_registry_address
        self.validation_registry_address = validation_registry_address
        
        # Agent state
        self.agent_id = None
        self.registration_uri = None
        self.capabilities = []
        self.trust_models = ["reputation", "validation"]
        
        print(f"✅ Agent '{self.name}' initialized")
        print(f"   Address: {self.address}")
        print(f"   Domain: {self.domain}")
    
    def create_registration_file(self) -> Dict[str, Any]:
        """
        Create ERC-8004 compliant registration file
        
        Returns:
            Dict containing agent registration data
        """
        registration = {
            "version": "registration-v1",
            "name": self.name,
            "description": f"{self.name} - ERC-8004 Compliant AI Agent",
            "wallet": f"eip155:1:{self.address}",
            "domain": self.domain,
            "endpoints": {
                "a2a": {
                    "enabled": True,
                    "endpoint": f"https://{self.domain}/a2a"
                },
                "mcp": {
                    "enabled": False,
                    "endpoint": ""
                }
            },
            "capabilities": self.capabilities,
            "trustModels": self.trust_models,
            "evmChains": [
                {
                    "name": "Local",
                    "chainId": self.w3.eth.chain_id,
                    "registries": {
                        "identity": self.identity_registry_address,
                        "reputation": self.reputation_registry_address,
                        "validation": self.validation_registry_address
                    }
                }
            ]
        }
        
        return registration
    
    def compute_hash(self, data: Any) -> str:
        """
        Compute SHA-256 hash of data
        
        Args:
            data: Data to hash (will be JSON serialized)
            
        Returns:
            Hex string of hash
        """
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data, sort_keys=True)
        
        return hashlib.sha256(data.encode()).hexdigest()
    
    def register_identity(self, contract_abi: List[Dict]) -> int:
        """
        Register agent identity on-chain
        
        Args:
            contract_abi: Identity Registry contract ABI
            
        Returns:
            Agent ID
        """
        if not self.identity_registry_address:
            raise ValueError("Identity Registry address not set")
        
        # Create registration file
        registration_data = self.create_registration_file()
        registration_uri = f"ipfs://mock/{self.domain}/registration.json"
        
        # Create contract instance
        contract = self.w3.eth.contract(
            address=self.identity_registry_address,
            abi=contract_abi
        )
        
        # Build transaction
        nonce = self.w3.eth.get_transaction_count(self.address)
        
        txn = contract.functions.registerAgent(
            self.name,
            self.domain,
            registration_uri
        ).build_transaction({
            'from': self.address,
            'nonce': nonce,
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Parse agent ID from logs
        logs = contract.events.AgentRegistered().process_receipt(receipt)
        self.agent_id = logs[0]['args']['agentId']
        self.registration_uri = registration_uri
        
        print(f"✅ Agent registered on-chain")
        print(f"   Agent ID: {self.agent_id}")
        print(f"   Transaction: {tx_hash.hex()}")
        
        return self.agent_id
    
    def authorize_feedback(
        self,
        client_address: str,
        contract_abi: List[Dict]
    ) -> str:
        """
        Authorize a client to submit feedback
        
        Args:
            client_address: Address to authorize
            contract_abi: Reputation Registry contract ABI
            
        Returns:
            Transaction hash
        """
        if not self.reputation_registry_address:
            raise ValueError("Reputation Registry address not set")
        
        if not self.agent_id:
            raise ValueError("Agent not registered")
        
        contract = self.w3.eth.contract(
            address=self.reputation_registry_address,
            abi=contract_abi
        )
        
        nonce = self.w3.eth.get_transaction_count(self.address)
        
        txn = contract.functions.authorizeFeedback(
            self.agent_id,
            client_address
        ).build_transaction({
            'from': self.address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"✅ Feedback authorized for {client_address}")
        print(f"   Transaction: {tx_hash.hex()}")
        
        return tx_hash.hex()
    
    def request_validation(
        self,
        validator_id: int,
        work_data: Dict,
        contract_abi: List[Dict]
    ) -> int:
        """
        Request validation from another agent
        
        Args:
            validator_id: ID of validator agent
            work_data: Data to be validated
            contract_abi: Validation Registry contract ABI
            
        Returns:
            Request ID
        """
        if not self.validation_registry_address:
            raise ValueError("Validation Registry address not set")
        
        if not self.agent_id:
            raise ValueError("Agent not registered")
        
        # Compute hash of work
        work_hash = self.compute_hash(work_data)
        work_uri = f"ipfs://mock/{self.domain}/work/{work_hash[:8]}.json"
        
        contract = self.w3.eth.contract(
            address=self.validation_registry_address,
            abi=contract_abi
        )
        
        nonce = self.w3.eth.get_transaction_count(self.address)
        
        txn = contract.functions.requestValidation(
            self.agent_id,
            validator_id,
            work_uri,
            bytes.fromhex(work_hash)
        ).build_transaction({
            'from': self.address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Parse request ID from logs
        logs = contract.events.ValidationRequested().process_receipt(receipt)
        request_id = logs[0]['args']['requestId']
        
        print(f"✅ Validation requested from agent {validator_id}")
        print(f"   Request ID: {request_id}")
        print(f"   Transaction: {tx_hash.hex()}")
        
        return request_id
    
    def submit_validation_response(
        self,
        request_id: int,
        score: int,
        response_data: Dict,
        contract_abi: List[Dict]
    ) -> str:
        """
        Submit validation response
        
        Args:
            request_id: Validation request ID
            score: Validation score (0-100)
            response_data: Validation response data
            contract_abi: Validation Registry contract ABI
            
        Returns:
            Transaction hash
        """
        if not self.validation_registry_address:
            raise ValueError("Validation Registry address not set")
        
        # Compute hash of response
        response_hash = self.compute_hash(response_data)
        response_uri = f"ipfs://mock/{self.domain}/validation/{response_hash[:8]}.json"
        
        contract = self.w3.eth.contract(
            address=self.validation_registry_address,
            abi=contract_abi
        )
        
        nonce = self.w3.eth.get_transaction_count(self.address)
        
        txn = contract.functions.submitValidationResponse(
            request_id,
            score,
            response_uri,
            bytes.fromhex(response_hash)
        ).build_transaction({
            'from': self.address,
            'nonce': nonce,
            'gas': 300000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"✅ Validation response submitted")
        print(f"   Request ID: {request_id}")
        print(f"   Score: {score}/100")
        print(f"   Transaction: {tx_hash.hex()}")
        
        return tx_hash.hex()
    
    def get_reputation_score(self, contract_abi: List[Dict]) -> int:
        """
        Get average reputation score
        
        Args:
            contract_abi: Reputation Registry contract ABI
            
        Returns:
            Average reputation score (0-100)
        """
        if not self.reputation_registry_address or not self.agent_id:
            return 0
        
        contract = self.w3.eth.contract(
            address=self.reputation_registry_address,
            abi=contract_abi
        )
        
        score = contract.functions.getAverageScore(self.agent_id).call()
        return score
    
    def get_validation_score(self, contract_abi: List[Dict]) -> int:
        """
        Get average validation score
        
        Args:
            contract_abi: Validation Registry contract ABI
            
        Returns:
            Average validation score (0-100)
        """
        if not self.validation_registry_address or not self.agent_id:
            return 0
        
        contract = self.w3.eth.contract(
            address=self.validation_registry_address,
            abi=contract_abi
        )
        
        score = contract.functions.getAverageValidationScore(self.agent_id).call()
        return score
