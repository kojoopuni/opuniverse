# Opuniverse AI Orchestrator

## :star: Project Vision
A comprehensive AI orchestration platform integrating multiple AI frameworks to create sophisticated automation workflows and AI agent systems.

## :dart: Current Status
**Version:** 0.1.0 (2024-10-29)  
**Environment:** Google Cloud VM with Static IP (35.197.39.232)  
**Base Services:** n8n (self-hosted), CrewAI integration in progress

## :building_construction: Core Components
- **n8n Instance**: Self-hosted automation platform
- **CrewAI Integration**: 
  - Enterprise Bridge
  - Self-hosted Implementation
- **Secrets Management**: Dedicated service
- **Docker Infrastructure**: Container orchestration

## :file_folder: Project Structure
```bash
ai-services/
├── crewai/
│   ├── src/
│   │   ├── enterprise_bridge/   # Enterprise integration
│   │   ├── self_hosted/         # Custom implementation
│   │   └── __init__.py
│   ├── tools/
│   │   ├── enterprise/
│   │   ├── self_hosted/
│   │   └── shared/
│   ├── configs/
│   └── templates/
├── secrets-service/
│   ├── src/
│   └── config/
└── docker-compose.yml

## ⚡ Quick Start

Environment Setup

# Clone repository
git clone [repository-url]
cd ai-services

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Initial Configuration

# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env

## 📚 Documentation

### Core Guides
- [Development Guide](./docs/DEVELOPMENT.md)
- [Architecture Overview](./docs/ARCHITECTURE.md)
- [Integration Guide](./docs/INTEGRATION.md)

## 🛠️ Infrastructure

### VM Configuration
- **Type:** e2-standard-4
- **vCPUs:** 4
- **Memory:** 16GB
- **Static IP:** 35.197.39.232
- **Domain:** n8n.opuniverse.com

### VS Code Remote Setup
- Configured via SSH
- Custom workspace settings
- Extensions synchronized

## 🧠 AI Framework Integration

### CrewAI + LangGraph
CrewAI provides role-based agents with specific expertise, while LangGraph manages complex workflow routing and state management. This enables:
- Role-specific AI agents
- Complex decision trees
- State-aware workflows
- Dynamic task routing

### n8n Integration Features
- Visual workflow building
- Native AI nodes support
- Webhook management
- 200+ integration nodes

## 📈 Project Roadmap

### Current Progress
- [x] Initial Setup (v0.1.0)
- [ ] Basic CrewAI Integration
- [ ] n8n Workflow Integration
- [ ] Enterprise Bridge
- [ ] LangGraph Integration
- [ ] Testing Framework
- [ ] Production Deployment

## 🔐 Security Implementation
- API keys managed via secrets service
- Environment variables for sensitive data
- Regular security audits
- Access control implementation

## 📖 References
- [GitHub Markdown Guide](https://docs.github.com/en/get-started/writing-on-github)
- [GitHub Emoji Cheat Sheet](https://gist.github.com/rxaviers/7360908)
- [CrewAI Documentation](https://docs.crewai.com/)
- [n8n AI Nodes](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.ai/)
- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)

---

> 🔵 **Assistant Memory Prompt**:  
> 1. Request DEVELOPMENT.md, ARCHITECTURE.md, and INTEGRATION.md in sequence
> 2. All updates must be in proper GitHub Markdown format
> 3. Check for memory limits before large updates
> 4. Maintain consistent naming (opuniverse, not OpuniVerse)
> 5. Document all VM and infrastructure changes
> 6. Current directory structure shown in terminal: ~/ai-services with crewai/ and secrets-service/ subdirectories
> 7. Always verify markdown rendering in VS Code preview before sharing
> 8. Consider n8n's AI nodes in implementations
> 9. **IMPORTANT**: Never share markdown content without first verifying it renders correctly in VS Code preview

## 📝 Formatting Guidelines

### Emoji Usage
- Use Unicode characters directly (⚡, 📚, 🛠️)
- Place emojis at start of headers
- Leave space between emoji and header text

### Lists
- Use single-level bullet points
- Start each item with hyphen and space
- Bold important terms with double asterisks
- Maintain consistent indentation

### Code Blocks
```bash
# Use language-specific formatting
# Leave empty lines before and after
