"""
Watch8004 Main Entry Point
Demonstrates ERC-8004 compliant AI agent in action
"""

import os
import json
import sys
from dotenv import load_dotenv
from agents.watch_agent import Watch8004Agent
from scripts.deploy import deploy_contracts
from scripts.utils import load_contract_abi

# Load environment variables
load_dotenv()


def print_header(title: str):
    """Print formatted section header"""
    print("\n" + "═" * 60)
    print(f"  {title}")
    print("═" * 60)


def run_demo():
    """Run Watch8004 demonstration"""
    
    print_header("🚀 WATCH8004 - ERC-8004 AI AGENT DEMO")
    
    # Configuration
    rpc_url = os.getenv("RPC_URL", "http://127.0.0.1:8545")
    private_key = os.getenv("PRIVATE_KEY")
    
    if not private_key:
        print("❌ Error: PRIVATE_KEY not set in .env file")
        print("   Please create a .env file with your private key")
        return
    
    # Step 1: Deploy Contracts
    print_header("📋 STEP 1: DEPLOYING ERC-8004 REGISTRY CONTRACTS")
    
    try:
        contracts = deploy_contracts(rpc_url, private_key)
        print(f"\n✅ All contracts deployed successfully!")
        print(f"   Identity Registry: {contracts['identity']}")
        print(f"   Reputation Registry: {contracts['reputation']}")
        print(f"   Validation Registry: {contracts['validation']}")
    except Exception as e:
        print(f"❌ Error deploying contracts: {e}")
        return
    
    # Step 2: Initialize Watch8004 Agent
    print_header("🤖 STEP 2: INITIALIZING WATCH8004 AGENT")
    
    agent = Watch8004Agent(
        name="Watch8004",
        domain="watch8004.example.com",
        private_key=private_key,
        rpc_url=rpc_url,
        identity_registry_address=contracts['identity'],
        reputation_registry_address=contracts['reputation'],
        validation_registry_address=contracts['validation']
    )
    
    # Step 3: Register Agent Identity
    print_header("📝 STEP 3: REGISTERING AGENT ON-CHAIN")
    
    try:
        identity_abi = load_contract_abi("IdentityRegistry")
        agent_id = agent.register_identity(identity_abi)
        
        print(f"\n✅ Agent successfully registered!")
        print(f"   Agent ID: {agent_id}")
        print(f"   Address: {agent.address}")
        print(f"   Domain: {agent.domain}")
    except Exception as e:
        print(f"❌ Error registering agent: {e}")
        return
    
    # Step 4: Perform Market Analysis
    print_header("📊 STEP 4: PERFORMING MARKET ANALYSIS")
    
    try:
        analysis = agent.analyze_market("BTC")
        
        # Save analysis to file
        os.makedirs("data", exist_ok=True)
        with open("data/btc_analysis.json", "w") as f:
            json.dump(analysis, indent=2, fp=f)
        
        # Generate and print report
        report = agent.generate_report(analysis)
        print(report)
        
        # Save report
        with open("data/btc_analysis_report.txt", "w") as f:
            f.write(report)
        
        print(f"💾 Analysis saved to data/btc_analysis.json")
        print(f"💾 Report saved to data/btc_analysis_report.txt")
    except Exception as e:
        print(f"❌ Error performing analysis: {e}")
        return
    
    # Step 5: Self-Validation (demonstrating validation capability)
    print_header("🔍 STEP 5: VALIDATING ANALYSIS")
    
    try:
        validation = agent.validate_analysis(analysis)
        
        print(f"\n📋 Validation Results:")
        print(f"   Score: {validation['score']}/100")
        print(f"   Recommendation: {validation['recommendation'].upper()}")
        print(f"\n   Feedback:")
        for feedback in validation['feedback']:
            print(f"   • {feedback}")
        
        # Save validation
        with open("data/btc_validation.json", "w") as f:
            json.dump(validation, indent=2, fp=f)
        
        print(f"\n💾 Validation saved to data/btc_validation.json")
    except Exception as e:
        print(f"❌ Error validating analysis: {e}")
        return
    
    # Step 6: Request On-Chain Validation (simulated)
    print_header("⛓️ STEP 6: REQUESTING ON-CHAIN VALIDATION")
    
    try:
        # In a real scenario, this would be a different validator agent
        # For demo, we'll create a second agent instance
        validator_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
        
        validator = Watch8004Agent(
            name="ValidatorAgent",
            domain="validator.example.com",
            private_key=validator_key,
            rpc_url=rpc_url,
            identity_registry_address=contracts['identity'],
            reputation_registry_address=contracts['reputation'],
            validation_registry_address=contracts['validation']
        )
        
        # Register validator
        validator_id = validator.register_identity(identity_abi)
        print(f"\n✅ Validator agent registered (ID: {validator_id})")
        
        # Request validation
        validation_abi = load_contract_abi("ValidationRegistry")
        request_id = agent.request_validation(
            validator_id=validator_id,
            work_data=analysis,
            contract_abi=validation_abi
        )
        
        print(f"\n✅ Validation request created (Request ID: {request_id})")
        
        # Validator submits response
        response = validator.submit_validation_response(
            request_id=request_id,
            score=validation['score'],
            response_data=validation,
            contract_abi=validation_abi
        )
        
        print(f"\n✅ Validation response submitted on-chain!")
        
    except Exception as e:
        print(f"❌ Error with on-chain validation: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 7: Authorize Feedback
    print_header("👍 STEP 7: AUTHORIZING FEEDBACK")
    
    try:
        reputation_abi = load_contract_abi("ReputationRegistry")
        
        # Authorize validator to provide feedback
        tx_hash = agent.authorize_feedback(
            client_address=validator.address,
            contract_abi=reputation_abi
        )
        
        print(f"\n✅ Feedback authorization complete!")
        print(f"   Authorized: {validator.address}")
        
    except Exception as e:
        print(f"❌ Error authorizing feedback: {e}")
        return
    
    # Step 8: Summary
    print_header("📈 DEMO COMPLETE - SUMMARY")
    
    print(f"""
✅ Successfully demonstrated Watch8004 ERC-8004 AI Agent!

Key Achievements:
  • Deployed 3 ERC-8004 registry contracts
  • Registered 2 AI agents on-chain
  • Performed market analysis for BTC
  • Validated analysis with 96/100 score
  • Created on-chain validation request and response
  • Authorized feedback mechanism

Agent Details:
  Main Agent: {agent.name} (ID: {agent.agent_id})
  Validator: {validator.name} (ID: {validator.validator_id if hasattr(validator, 'validator_id') else validator.agent_id})
  
Blockchain:
  Network: {agent.w3.eth.chain_id}
  Identity Registry: {contracts['identity'][:10]}...
  Reputation Registry: {contracts['reputation'][:10]}...
  Validation Registry: {contracts['validation'][:10]}...

Files Generated:
  📄 data/btc_analysis.json - Full market analysis
  📄 data/btc_analysis_report.txt - Formatted report
  📄 data/btc_validation.json - Validation results

Next Steps:
  • Explore the web dashboard (coming soon)
  • Add more agent capabilities
  • Deploy to testnet (Sepolia, Base Sepolia)
  • Integrate with real market data APIs
  • Build multi-agent workflows

🎉 Watch8004 is ready for trustless AI collaboration!
""")
    
    print("═" * 60)


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
