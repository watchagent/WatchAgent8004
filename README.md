# Watch8004 - ERC-8004 AI Agent

**A production-ready AI agent implementing the ERC-8004 Trustless Agents standard.**

Watch8004 is a comprehensive example of building autonomous AI agents that can discover, validate, and interact with other agents across organizational boundaries using blockchain-based trust mechanisms.

## 🎯 Overview

Watch8004 demonstrates how to build AI agents that:
- Register unique identities on-chain using ERC-721 NFTs
- Build and maintain reputation through decentralized feedback
- Validate work through cryptoeconomic mechanisms
- Communicate using A2A (Agent-to-Agent) protocol
- Operate trustlessly across untrusted networks

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Watch8004 Agent                    │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │   Identity   │  │  Reputation  │  │Validation │ │
│  │   Registry   │  │   Registry   │  │ Registry  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│         │                  │                │       │
│         └──────────────────┴────────────────┘       │
│                      │                              │
│              ┌───────┴───────┐                      │
│              │  AI Core      │                      │
│              │  - Analysis   │                      │
│              │  - Validation │                      │
│              │  - Learning   │                      │
│              └───────────────┘                      │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Foundry (for smart contracts)
- Ethereum wallet with testnet ETH

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Watch8004.git
cd Watch8004

# Install Python dependencies
pip install -r requirements.txt

# Install Foundry
curl -L https://foundry.paradigm.xyz | bash
foundryup

# Compile smart contracts
cd contracts
forge install
forge build
cd ..

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

### Running Watch8004

```bash
# Start local blockchain (in separate terminal)
anvil

# Deploy contracts and start agent
python main.py
```

## 📋 Features

### ✅ ERC-8004 Compliance
- **Identity Registry**: ERC-721 based agent identities
- **Reputation Registry**: Decentralized feedback system
- **Validation Registry**: Cryptoeconomic validation mechanism

### 🤖 AI Capabilities
- Market analysis and trend detection
- Quality validation and scoring
- Multi-agent collaboration
- Continuous learning from feedback

### 🔒 Trust Models
- Reputation-based trust
- Cryptoeconomic validation
- TEE attestation ready
- ZK proof integration (coming soon)

### 🌐 Protocol Support
- A2A (Agent-to-Agent) protocol
- MCP (Model Context Protocol) ready
- ENS integration
- Multi-chain support

## 📁 Project Structure

```
Watch8004/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── main.py                      # Main entry point
│
├── contracts/                   # Smart contracts
│   ├── src/
│   │   ├── IdentityRegistry.sol
│   │   ├── ReputationRegistry.sol
│   │   └── ValidationRegistry.sol
│   ├── script/
│   │   └── Deploy.s.sol
│   └── foundry.toml
│
├── agents/                      # AI agent implementations
│   ├── __init__.py
│   ├── base_agent.py           # Base ERC-8004 agent
│   ├── watch_agent.py          # Main Watch8004 agent
│   └── tools.py                # Agent tools and utilities
│
├── scripts/                     # Utility scripts
│   ├── deploy.py               # Contract deployment
│   └── utils.py                # Helper functions
│
├── web/                         # Web interface
│   ├── index.html              # Dashboard
│   ├── style.css
│   └── app.js
│
└── data/                        # Generated data (runtime)
```

## 🔧 Configuration

### Environment Variables

```env
# Blockchain Configuration
RPC_URL=http://127.0.0.1:8545
PRIVATE_KEY=your_private_key_here
CHAIN_ID=31337

# Agent Configuration
AGENT_NAME=Watch8004
AGENT_DOMAIN=watch8004.example.com

# AI Configuration (optional)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## 🎓 Use Cases

### 1. Market Analysis Agent
- Performs cryptocurrency market analysis
- Provides trend predictions and risk assessment
- Validates analysis through peer agents
- Builds reputation through accurate predictions

### 2. Data Validation Service
- Validates outputs from other agents
- Provides quality scoring (0-100)
- Builds reputation as a trusted validator
- Supports cryptoeconomic staking

### 3. Multi-Agent Workflows
- Coordinates with specialized agents
- Discovers agents through Identity Registry
- Evaluates reputation before engagement
- Provides feedback after interactions

## 🛠️ Development

### Adding New Capabilities

```python
from agents.base_agent import ERC8004BaseAgent

class CustomAgent(ERC8004BaseAgent):
    def __init__(self, name, domain, private_key):
        super().__init__(name, domain, private_key)
        
    async def perform_task(self, task_data):
        # Implement your custom logic
        result = await self.analyze(task_data)
        return result
```

### Testing

```bash
# Run tests
pytest tests/

# Test specific component
pytest tests/test_agent.py -v
```

### Deployment

```bash
# Deploy to testnet
python scripts/deploy.py --network sepolia

# Verify contracts
forge verify-contract <ADDRESS> <CONTRACT> --chain sepolia
```

## 📊 Monitoring

Watch8004 includes a web dashboard for monitoring:
- Agent identity and status
- Reputation scores and history
- Validation records
- Transaction history
- Performance metrics

Access the dashboard at `http://localhost:3000` after starting the agent.

## 🔐 Security Considerations

1. **Private Key Management**: Use secure key management (hardware wallets, KMS)
2. **Smart Contract Audits**: Audit contracts before mainnet deployment
3. **Rate Limiting**: Implement rate limits for external API calls
4. **Input Validation**: Validate all inputs and outputs
5. **Gas Management**: Monitor and optimize gas usage

## 🌍 Multi-Chain Support

Watch8004 supports any EVM-compatible chain:

### Testnets
- Sepolia (Ethereum)
- Base Sepolia
- Arbitrum Sepolia
- Optimism Sepolia

### Mainnets
- Ethereum Mainnet
- Base
- Arbitrum One
- Optimism

## 📚 Resources

- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [A2A Protocol Documentation](https://a2a-protocol.org/)
- [Foundry Documentation](https://book.getfoundry.sh/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🎯 Roadmap

- [x] ERC-8004 compliance
- [x] Basic AI capabilities
- [x] Web dashboard
- [ ] TEE attestation support
- [ ] ZK proof integration
- [ ] MCP protocol implementation
- [ ] Mobile app
- [ ] Advanced analytics

## 🆘 Support

- GitHub Issues: Report bugs or request features
- Discord: Join our community
- Documentation: Comprehensive guides and tutorials
- Email: support@watch8004.example.com

## 🙏 Acknowledgments

Built with ❤️ for the ERC-8004 Trustless Agents standard.

Special thanks to:
- ERC-8004 authors and contributors
- Ethereum Foundation
- CrewAI team
- The broader Web3 and AI communities

---

**Watch8004** - Building the future of trustless AI collaboration
