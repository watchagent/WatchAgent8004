# Watch8004 Quick Start Guide

Welcome to Watch8004! This guide will help you get started with your ERC-8004 compliant AI agent in just a few minutes.

## 🚀 Prerequisites

Before you begin, make sure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **Node.js 16+** installed ([Download](https://nodejs.org/))
- **Git** installed ([Download](https://git-scm.com/))

## 📥 Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/Watch8004.git
cd Watch8004

# Run setup script
./setup.sh
```

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Watch8004.git
cd Watch8004

# Install Python dependencies
pip install -r requirements.txt

# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Install OpenZeppelin contracts
cd contracts
forge install OpenZeppelin/openzeppelin-contracts --no-commit
cd ..

# Setup environment
cp .env.example .env
```

## ⚙️ Configuration

Edit the `.env` file with your settings:

```env
# For local testing (default)
RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
CHAIN_ID=31337

# For testnet deployment
# RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
# PRIVATE_KEY=your_testnet_private_key_here
# CHAIN_ID=11155111
```

## 🏃 Running Watch8004

### Step 1: Start Local Blockchain

In a **separate terminal**, start Anvil (local Ethereum node):

```bash
anvil
```

Keep this terminal running.

### Step 2: Run the Demo

In your **main terminal**:

```bash
python main.py
```

This will:
1. ✅ Deploy ERC-8004 registry contracts
2. ✅ Register Watch8004 agent on-chain
3. ✅ Perform market analysis for BTC
4. ✅ Validate the analysis
5. ✅ Create on-chain validation records
6. ✅ Authorize feedback mechanisms

### Step 3: View the Dashboard

Open `web/index.html` in your browser to see the dashboard:

```bash
# On macOS
open web/index.html

# On Linux
xdg-open web/index.html

# On Windows
start web/index.html
```

## 📊 What Happens in the Demo

The demo showcases a complete ERC-8004 workflow:

1. **Contract Deployment**: Three registries are deployed
   - Identity Registry (ERC-721 based agent identities)
   - Reputation Registry (feedback and ratings)
   - Validation Registry (quality validation)

2. **Agent Registration**: Watch8004 registers itself on-chain
   - Receives unique Agent ID
   - Gets ERC-721 NFT representing identity
   - Publishes capabilities and trust models

3. **Market Analysis**: Agent performs BTC analysis
   - Trend detection
   - Support/resistance levels
   - Risk assessment
   - Trading recommendations

4. **Validation**: Another agent validates the work
   - Quality scoring (0-100)
   - Detailed feedback
   - On-chain validation record

5. **Reputation Building**: Feedback is authorized
   - Clients can rate the agent
   - Reputation score is built over time
   - Trust network is established

## 📁 Generated Files

After running the demo, you'll find:

```
data/
├── btc_analysis.json          # Full market analysis
├── btc_analysis_report.txt    # Formatted report
└── btc_validation.json        # Validation results

contracts/
├── deployment.json            # Contract addresses
└── out/                       # Compiled contracts & ABIs
```

## 🎯 Next Steps

### 1. Customize Your Agent

Edit `agents/watch_agent.py` to add your own capabilities:

```python
class MyCustomAgent(Watch8004Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capabilities.append("my_custom_capability")
    
    def my_custom_function(self, data):
        # Your custom logic here
        pass
```

### 2. Deploy to Testnet

Update `.env` for testnet deployment:

```env
RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_testnet_private_key_here
CHAIN_ID=11155111
```

Get testnet ETH from faucets:
- Sepolia: https://sepoliafaucet.com/
- Base Sepolia: https://www.coinbase.com/faucets/base-sepolia-faucet

### 3. Integrate Real Data

Replace mock data in `analyze_market()` with real API calls:

```python
import requests

def analyze_market(self, symbol: str):
    # Get real market data
    response = requests.get(f'https://api.example.com/market/{symbol}')
    data = response.json()
    
    # Analyze with your logic
    analysis = self.process_market_data(data)
    return analysis
```

### 4. Build Multi-Agent Systems

Create specialized agents that work together:

```python
# Analysis agent
analysis_agent = Watch8004Agent(
    name="AnalysisBot",
    domain="analysis.example.com"
)

# Validation agent
validation_agent = Watch8004Agent(
    name="ValidatorBot",
    domain="validator.example.com"
)

# Agents collaborate trustlessly!
```

## 🔧 Troubleshooting

### "Failed to connect to blockchain"

Make sure Anvil is running:
```bash
anvil
```

### "Contract compilation failed"

Install Solidity compiler:
```bash
foundryup
```

### "Module not found"

Install Python dependencies:
```bash
pip install -r requirements.txt
```

### "Permission denied: ./setup.sh"

Make the script executable:
```bash
chmod +x setup.sh
```

## 📚 Learn More

- **ERC-8004 Specification**: https://eips.ethereum.org/EIPS/eip-8004
- **8004.org**: https://8004.org/
- **A2A Protocol**: https://a2a-protocol.org/
- **Foundry Book**: https://book.getfoundry.sh/

## 🆘 Getting Help

- **GitHub Issues**: Report bugs or request features
- **Discord**: Join our community
- **Documentation**: Check out the full documentation in README.md

## 🎉 Success!

If you see this output, you're all set:

```
✅ Successfully demonstrated Watch8004 ERC-8004 AI Agent!

Key Achievements:
  • Deployed 3 ERC-8004 registry contracts
  • Registered 2 AI agents on-chain
  • Performed market analysis for BTC
  • Validated analysis with 96/100 score
  • Created on-chain validation request and response
  • Authorized feedback mechanism
```

Welcome to the future of trustless AI collaboration! 🤖⛓️
