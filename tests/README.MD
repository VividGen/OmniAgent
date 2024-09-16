# OmniAgent Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/VividGen/OmniAgent.svg)](https://github.com/VividGen/OmniAgent/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/VividGen/OmniAgent.svg)](https://github.com/VividGen/OmniAgent/issues)

OmniAgent is an enterprise-grade AI orchestration framework that revolutionizes Web3 development by seamlessly bridging artificial intelligence with blockchain technologies. Build powerful on-chain AI agents in hours instead of months.

## 🚀 Key Features

- **Modular Architecture**: Three-layer design with Interpreter, Classifier, and specialized Executors
- **Intelligent Task Routing**: Smart classification system powered by Google Gemma and domain-specific models
- **Plug-and-Play Model Integration**: Easy integration with various AI models
- **Cross-Chain Compatibility**: Seamless interaction with multiple blockchain networks
- **Specialized Executors**:
  - DeFi Operations
  - Token/NFT Management
  - Web3 Knowledge Integration
  - Social Data Analysis

## 🏗️ Architecture

```
┌─────────────────┐
│    User Input   │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Interpreter   │ ─── Task Understanding & Parameter Extraction
└────────┬────────┘
         ▼
┌─────────────────┐
│   Classifier    │ ─── Intelligent Task Routing
└────────┬────────┘
         ▼
┌─────────────────┐
│    Executor     │ ─── Specialized Task Execution
└────────┬────────┘
         ▼
┌─────────────────┐
│      Web3       │ ─── Blockchain & Protocol Interaction
└─────────────────┘
```

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/VividGen/OmniAgent.git

# Configure environment
cp .env.example .env

# Start
docker-compose up -d
```

## 📦 Quick Start

```javascript
const { OmniAgent } = require('omniagent');

// Initialize OmniAgent
const agent = new OmniAgent({
  model: 'gemma',
  executors: ['defi', 'token', 'social']
});

// Execute a task
const result = await agent.execute({
  task: 'Token swap',
  params: {
    fromToken: 'ETH',
    toToken: 'USDC',
    amount: '1.0'
  }
});
```

## 💡 Use Cases

- **DeFi Operations**: Token swaps, liquidity provision, yield farming
- **Asset Management**: NFT trading, token transfers, portfolio analysis
- **Market Intelligence**: Price tracking, trend analysis, social sentiment
- **Cross-Chain Operations**: Bridge transfers, cross-chain swaps
- **Smart Contract Interaction**: Contract deployment, function calls

## 🔧 Configuration

```javascript
{
  "interpreter": {
    "model": "gemma",
    "temperature": 0.7  },
  "classifier": {
    "model": "codegemma",
    "threshold": 0.85
  },
  "executors": {
    "defi": {
      "networks": ["ethereum", "polygon"],
      "protocols": ["uniswap", "aave"]
    },
    "token": {
      "supportedTokens": ["ERC20", "ERC721", "ERC1155"]
    }
  }
}
```

## 📚 Documentation

Comprehensive documentation is available at our documentation site.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Google Gemma and CodeGemma teams for their excellent models
- The Web3 community for continuous support and feedback
- All contributors who have helped shape OmniAgent
