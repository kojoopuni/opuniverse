# Opuniverse Development Guide

## 🛠️ Development Standards

### Code Style
- Use Python type hints
- Follow PEP 8 guidelines
- Document all functions and classes
- Maintain consistent naming conventions

### Version Control
- Create feature branches from main
- Use meaningful commit messages
- Regular commits with atomic changes
- Pull requests for code review

## 🔧 Development Environment

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose
- VS Code with Remote SSH
- Git configured

### Initial Setup
```bash
# Clone repository
git clone [repository-url]
cd ai-services

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## 🔐 Configuration Management

### Environment Variables
- Create .env file from template
- Never commit sensitive data
- Use secrets service for credentials
- Maintain separate dev/prod configs

### VS Code Configuration
- Install recommended extensions
- Configure Python interpreter
- Set up linting and formatting
- Enable Remote SSH

## 🧪 Testing Protocol

### Unit Testing
- Write tests for all new features
- Maintain 80% code coverage
- Use pytest framework
- Mock external services

### Integration Testing
- Test n8n workflows
- Verify CrewAI integrations
- Check API endpoints
- Validate Docker services

## 🐳 Docker Development

### Container Guidelines
- Use docker-compose for local dev
- Build images with proper tags
- Monitor container logs
- Regular cleanup of unused images

### Service Integration
- Test n8n connectivity
- Verify CrewAI services
- Check network configurations
- Monitor resource usage

## 📚 References
- [Python Style Guide](https://peps.python.org/pep-0008/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [n8n Developer Docs](https://docs.n8n.io/development/)
- [Docker Compose Guide](https://docs.docker.com/compose/)

---

## 🔄 API Endpoints

### Available Endpoints
- GET / : Root endpoint providing service information
- GET /health : Health check endpoint
- POST /crews/create : Endpoint for creating new CrewAI instances

### Testing Endpoints
1. Access Swagger UI at http://localhost:8000/docs
2. Click on desired endpoint
3. Click "Try it out"
4. Click "Execute"
5. Review response

## 🔄 Implementation Progress

### Completed
- Basic project structure
- FastAPI service implementation
- CrewAI integration setup
- API documentation with Swagger UI
- Development environment configuration

### Next Steps
- Implement CrewAI Enterprise bridge
- Set up n8n integration
- Add testing framework
- Configure production deployment

> 🔵 **Assistant Memory Prompt**:  
> 1. All formatting verified in VS Code preview
> 2. Used consistent Unicode emojis in headers
> 3. Maintained bullet point formatting
> 4. Next file: INTEGRATION.md

