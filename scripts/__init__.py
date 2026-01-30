"""
Watch8004 Scripts Module
Deployment and utility scripts
"""

from scripts.deploy import deploy_contracts
from scripts.utils import load_contract_abi, load_deployment_info

__all__ = ["deploy_contracts", "load_contract_abi", "load_deployment_info"]
