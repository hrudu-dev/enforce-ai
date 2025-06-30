# Contributing to EnforceAI

🎉 **Thank you for your interest in contributing to EnforceAI!** 🎉

We welcome contributions from the community and are excited to see what you'll bring to this project. This guide will help you get started with contributing to EnforceAI.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to conduct@enforce-ai.com.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- AWS Account (for testing)
- Basic understanding of compliance frameworks (GDPR, FISMA, etc.)

### First Steps

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/enforce-ai.git
   cd enforce-ai
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/original-org/enforce-ai.git
   ```

## 🛠️ Development Setup

### Environment Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Configure your AWS credentials
aws configure

# Set up local database (if needed)
python scripts/setup_db.py
```

### Running the Application

```bash
# Run the demo application
streamlit run demo_app.py

# Run with development settings
ENVIRONMENT=development streamlit run demo_app.py

# Run tests
pytest
```

## 🎯 How to Contribute

### Types of Contributions

We welcome several types of contributions:

#### 🐛 Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Add relevant logs or screenshots

#### ✨ Feature Requests
- Use the feature request template
- Explain the use case
- Describe the expected behavior
- Consider implementation complexity

#### 📝 Documentation
- Fix typos or unclear explanations
- Add examples or tutorials
- Improve API documentation
- Translate documentation

#### 🔧 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring

### Finding Issues to Work On

- **Good First Issues**: Look for issues labeled `good first issue`
- **Help Wanted**: Issues labeled `help wanted` need community support
- **Bug Fixes**: Issues labeled `bug` are great for getting started
- **Features**: Issues labeled `enhancement` for new functionality

## 🔄 Pull Request Process

### Before You Start

1. **Check existing issues** to avoid duplicate work
2. **Create an issue** if one doesn't exist
3. **Discuss your approach** in the issue comments
4. **Get approval** from maintainers for large changes

### Creating a Pull Request

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Write tests** for your changes

4. **Update documentation** if needed

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add new compliance framework support"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process

1. **Automated checks** must pass (CI/CD, linting, tests)
2. **Code review** by at least one maintainer
3. **Testing** in development environment
4. **Approval** and merge by maintainers

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

```python
# Good
def analyze_compliance(resource_data: Dict[str, Any], framework: str) -> ComplianceResult:
    """
    Analyze resource compliance against specified framework.
    
    Args:
        resource_data: AWS resource information
        framework: Compliance framework name (GDPR, FISMA, etc.)
        
    Returns:
        ComplianceResult object with analysis results
        
    Raises:
        ValueError: If framework is not supported
    """
    if framework not in SUPPORTED_FRAMEWORKS:
        raise ValueError(f"Unsupported framework: {framework}")
    
    return ComplianceResult(
        status=check_compliance(resource_data, framework),
        violations=find_violations(resource_data, framework),
        recommendations=generate_recommendations(resource_data, framework)
    )
```

### Code Formatting

We use automated formatting tools:

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .
```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: type(scope): description

# Examples:
feat(agents): add new compliance agent for ISO 27001
fix(scanner): resolve EC2 instance scanning timeout
docs(readme): update installation instructions
test(policy): add unit tests for policy enforcement
refactor(core): simplify agent orchestration logic
```

### File Structure

```
enforce-ai/
├── agents/                 # AI agents
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class
│   ├── compliance_agent.py
│   ├── audit_agent.py
│   └── policy_agent.py
├── policies/              # Compliance frameworks
│   ├── __init__.py
│   ├── frameworks.py
│   └── custom/
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── aws_helpers.py
│   └── logging.py
├── tests/                 # Test files
│   ├── unit/
│   ├── integration/
│   └── fixtures/
└── docs/                  # Documentation
    ├── api.md
    └── deployment.md
```

## 🧪 Testing Guidelines

### Test Structure

```python
# tests/unit/test_compliance_agent.py
import pytest
from unittest.mock import Mock, patch
from agents.compliance_agent import ComplianceAgent

class TestComplianceAgent:
    """Test suite for ComplianceAgent"""
    
    @pytest.fixture
    def compliance_agent(self):
        """Create ComplianceAgent instance for testing"""
        return ComplianceAgent()
    
    @pytest.fixture
    def mock_resource(self):
        """Mock AWS resource data"""
        return {
            'resource_id': 'i-1234567890abcdef0',
            'resource_type': 'EC2',
            'encrypted': False
        }
    
    def test_analyze_compliance_gdpr(self, compliance_agent, mock_resource):
        """Test GDPR compliance analysis"""
        result = compliance_agent.analyze_compliance(mock_resource, 'GDPR')
        
        assert result['status'] == 'NON_COMPLIANT'
        assert 'encryption' in result['violations'][0].lower()
    
    @patch('boto3.client')
    def test_bedrock_integration(self, mock_boto_client, compliance_agent):
        """Test Amazon Bedrock integration"""
        mock_bedrock = Mock()
        mock_boto_client.return_value = mock_bedrock
        
        # Test implementation
        pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_compliance_agent.py

# Run with coverage
pytest --cov=agents --cov-report=html

# Run integration tests
pytest tests/integration/

# Run tests with specific markers
pytest -m "not slow"
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows
- **Performance Tests**: Test system performance
- **Security Tests**: Test security vulnerabilities

## 📚 Documentation

### Documentation Standards

- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Include type hints for all functions
- **Examples**: Provide usage examples
- **API Documentation**: Auto-generated from docstrings

### Writing Documentation

```python
def enforce_policy(self, resource: Dict[str, Any], framework: str) -> PolicyResult:
    """
    Enforce compliance policy on AWS resource.
    
    This method analyzes the provided resource against the specified
    compliance framework and returns enforcement results including
    violations and recommended actions.
    
    Args:
        resource: AWS resource data containing:
            - resource_id (str): Unique resource identifier
            - resource_type (str): Type of AWS resource (EC2, RDS, etc.)
            - Additional resource-specific attributes
        framework: Compliance framework name. Supported frameworks:
            - 'GDPR': General Data Protection Regulation
            - 'FISMA': Federal Information Security Management Act
            - 'EU_AI_ACT': European Union AI Act
            - 'ISO_42001': ISO/IEC 42001 AI Management
    
    Returns:
        PolicyResult: Object containing:
            - status (str): Compliance status ('COMPLIANT', 'NON_COMPLIANT')
            - violations (List[str]): List of policy violations found
            - recommendations (List[str]): Recommended remediation actions
            - risk_level (str): Risk assessment ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')
    
    Raises:
        ValueError: If framework is not supported
        AWSError: If AWS API calls fail
        
    Example:
        >>> agent = PolicyAgent()
        >>> resource = {
        ...     'resource_id': 'i-1234567890abcdef0',
        ...     'resource_type': 'EC2',
        ...     'encrypted': False
        ... }
        >>> result = agent.enforce_policy(resource, 'GDPR')
        >>> print(result.status)
        'NON_COMPLIANT'
    """
```

## 🌟 Recognition

### Contributors

We recognize contributors in several ways:

- **Contributors file**: Listed in CONTRIBUTORS.md
- **Release notes**: Mentioned in release announcements
- **Social media**: Highlighted on our social channels
- **Swag**: EnforceAI merchandise for significant contributions

### Contribution Levels

- **First-time Contributor**: Welcome package and recognition
- **Regular Contributor**: Special badge and priority support
- **Core Contributor**: Invitation to maintainer discussions
- **Maintainer**: Full repository access and decision-making power

## 💬 Community

### Communication Channels

- **GitHub Discussions**: General discussions and Q&A
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time chat and community support
- **Email**: contribute@enforce-ai.com for private matters

### Community Guidelines

1. **Be respectful** and inclusive
2. **Help others** learn and grow
3. **Share knowledge** and experiences
4. **Provide constructive feedback**
5. **Follow the code of conduct**

### Getting Help

- **Documentation**: Check docs/ directory first
- **Search Issues**: Look for existing solutions
- **Ask Questions**: Use GitHub Discussions
- **Join Discord**: Get real-time help from community

## 🎉 Thank You!

Every contribution, no matter how small, makes EnforceAI better. We appreciate:

- 🐛 Bug reports and fixes
- 💡 Feature suggestions and implementations
- 📝 Documentation improvements
- 🧪 Test additions and improvements
- 💬 Community support and discussions
- ⭐ Stars and sharing the project

**Happy Contributing!** 🚀

---

*For questions about contributing, please reach out to contribute@enforce-ai.com or join our Discord community.*