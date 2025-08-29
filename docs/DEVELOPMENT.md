# Development Guide - RendergitMCP

This guide provides comprehensive development information for contributors to the RendergitMCP project.

## 🏗 Project Architecture

### System Overview

```
RendergitMCP Architecture
┌─────────────────────────────────────────────────┐
│                MCP Client                       │
│            (Claude Code, etc.)                  │
└─────────────┬───────────────────────────────────┘
              │ MCP Protocol (SSE/stdio)
┌─────────────▼───────────────────────────────────┐
│              MCP Server                         │
│         (mcp_rendergit_sdk.py)                  │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │   FastMCP       │  │    Health/Info      │   │
│  │   Framework     │  │    Endpoints        │   │
│  └─────────────────┘  └─────────────────────┘   │
└─────────────┬───────────────────────────────────┘
              │ Function calls
┌─────────────▼───────────────────────────────────┐
│            Rendergit Library                    │
│         (karpathy/rendergit)                    │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │  Git Clone      │  │   HTML Generation   │   │
│  │  Operations     │  │   (Pygments +       │   │
│  │                 │  │    Markdown)        │   │
│  └─────────────────┘  └─────────────────────┘   │
└─────────────┬───────────────────────────────────┘
              │ File operations
┌─────────────▼───────────────────────────────────┐
│              File System                        │
│                                                 │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │ Temp Clone      │  │   Output HTML       │   │
│  │ Directory       │  │   Files             │   │
│  └─────────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### Core Components

#### 1. MCP Server Layer (`mcp_rendergit_sdk.py`)
- **FastMCP Framework**: Handles MCP protocol communication
- **Tool Definitions**: `render_repo` and `render_repo_to_file` tools
- **Transport Support**: SSE (Server-Sent Events) and stdio transports
- **Health Monitoring**: `/health` and `/info` endpoints
- **Error Handling**: Comprehensive exception handling and logging

#### 2. Business Logic Layer
- **URL Processing**: Normalize various GitHub URL formats
- **Path Generation**: Auto-generate organized output paths
- **File Management**: Directory creation and file writing operations
- **Context Handling**: MCP context for progress reporting

#### 3. Rendergit Integration Layer
- **Clone Operations**: Shallow git clones for efficiency
- **Content Processing**: File filtering and processing
- **HTML Generation**: Dual-view HTML with syntax highlighting
- **CXML Export**: LLM-friendly text format generation

### Data Flow

```
1. MCP Client Request
   ↓
2. URL Normalization & Validation
   ↓
3. Rendergit Library Call
   ↓ 
4. Git Clone (shallow, temporary)
   ↓
5. File Scanning & Processing
   ↓
6. HTML Generation (Human + LLM views)
   ↓
7. File Storage (if requested)
   ↓
8. Response to MCP Client
```

## 🛠 Development Environment Setup

### Prerequisites

```bash
# System requirements
Python 3.10+
Git 2.0+
Docker (optional, for containerized development)

# Development tools
pip install black isort flake8 mypy pytest pytest-asyncio
```

### Development Installation

```bash
# 1. Clone repository
git clone https://github.com/sruckh/rendergit-mcp.git
cd rendergit-mcp

# 2. Create development environment
python -m venv venv-dev
source venv-dev/bin/activate  # Linux/macOS
# venv-dev\Scripts\activate   # Windows

# 3. Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Create this for dev dependencies

# 4. Install in editable mode
pip install -e .

# 5. Install original rendergit
pip install git+https://github.com/karpathy/rendergit.git
```

### Development Dependencies (`requirements-dev.txt`)

```txt
# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0
httpx>=0.24.0  # For testing HTTP endpoints

# Code Quality
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.0.0

# Development Tools
pre-commit>=3.0.0
watchdog>=3.0.0  # For file watching during development

# Documentation
mkdocs>=1.5.0
mkdocs-material>=9.0.0
```

### Pre-commit Setup

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

```bash
# Install pre-commit hooks
pre-commit install
```

## 🧪 Testing Framework

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_mcp_server.py       # MCP server tests
├── test_tools.py            # Tool functionality tests
├── test_integration.py      # End-to-end integration tests
├── test_performance.py      # Performance and benchmarking tests
└── fixtures/                # Test data and fixtures
    ├── sample_repos.py
    └── mock_responses.py
```

### Test Configuration (`conftest.py`)

```python
# tests/conftest.py
import asyncio
import tempfile
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch

@pytest.fixture
def sample_repo_url():
    """Sample repository URL for testing."""
    return "https://github.com/octocat/Hello-World"

@pytest.fixture
def temp_output_dir():
    """Temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
async def mcp_server():
    """MCP server instance for testing."""
    from mcp_rendergit_sdk import mcp
    
    # Configure for testing
    mcp.settings.host = "127.0.0.1"
    mcp.settings.port = 8888
    
    # Start server in background
    server_task = asyncio.create_task(mcp.run_async())
    await asyncio.sleep(0.1)  # Give server time to start
    
    yield mcp
    
    # Cleanup
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

@pytest.fixture
def mock_rendergit():
    """Mock rendergit library for testing."""
    with patch('mcp_rendergit_sdk.render_repo_html') as mock:
        mock.return_value = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Repository</title></head>
        <body>
            <div id="human-view">Human view content</div>
            <textarea id="llm-text">LLM view content</textarea>
        </body>
        </html>
        """
        yield mock
```

### Unit Tests

```python
# tests/test_tools.py
import pytest
from mcp.server.fastmcp import Context
from unittest.mock import AsyncMock

from mcp_rendergit_sdk import render_repo, render_repo_to_file

class TestRenderRepo:
    """Test the render_repo MCP tool."""
    
    @pytest.mark.asyncio
    async def test_render_repo_success(self, mock_rendergit):
        """Test successful repository rendering."""
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/octocat/Hello-World"
        
        result = await render_repo(repo_url, ctx)
        
        assert result is not None
        assert len(result) > 0
        assert "Test Repository" in result
        ctx.info.assert_called()
        
    @pytest.mark.asyncio
    async def test_render_repo_invalid_url(self, mock_rendergit):
        """Test rendering with invalid repository URL."""
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/invalid/nonexistent"
        
        # Mock rendergit to raise exception
        mock_rendergit.side_effect = Exception("Repository not found")
        
        with pytest.raises(Exception, match="Repository not found"):
            await render_repo(repo_url, ctx)
        
        ctx.error.assert_called()

class TestRenderRepoToFile:
    """Test the render_repo_to_file MCP tool."""
    
    @pytest.mark.asyncio
    async def test_render_to_file_success(self, mock_rendergit, temp_output_dir):
        """Test successful rendering to file."""
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/octocat/Hello-World"
        output_path = str(temp_output_dir / "test.html")
        
        result = await render_repo_to_file(
            repo_url, ctx, output_path=output_path
        )
        
        assert result["success"] is True
        assert result["output_path"] == output_path
        assert result["file_size"] > 0
        
        # Verify file was created
        assert Path(output_path).exists()
        
    @pytest.mark.asyncio
    async def test_render_to_file_auto_path(self, mock_rendergit, tmp_path):
        """Test auto-generated output path."""
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/octocat/Hello-World"
        
        # Mock the projects directory
        with patch('os.makedirs'), patch('builtins.open', create=True):
            result = await render_repo_to_file(repo_url, ctx)
            
            expected_filename = "github.com_octocat_Hello-World.html"
            assert expected_filename in result["output_path"]
            assert result["success"] is True
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class TestMCPIntegration:
    """Integration tests for MCP server functionality."""
    
    @pytest.mark.asyncio
    async def test_mcp_client_connection(self):
        """Test MCP client can connect to server."""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_rendergit_sdk.py", "--transport", "stdio"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test listing tools
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools]
                
                assert "render_repo" in tool_names
                assert "render_repo_to_file" in tool_names
    
    @pytest.mark.asyncio
    async def test_end_to_end_rendering(self, mock_rendergit):
        """Test complete rendering workflow."""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_rendergit_sdk.py", "--transport", "stdio"]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test render_repo tool
                result = await session.call_tool("render_repo", {
                    "repo_url": "https://github.com/octocat/Hello-World"
                })
                
                assert result.content is not None
                assert len(result.content) > 0

class TestHealthEndpoints:
    """Test HTTP health endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, mcp_server):
        """Test /health endpoint returns healthy status."""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8888/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["service"] == "rendergit-mcp"
    
    @pytest.mark.asyncio
    async def test_info_endpoint(self, mcp_server):
        """Test /info endpoint returns server information."""
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8888/info")
            
            assert response.status_code == 200
            data = response.json()
            assert data["service"] == "rendergit-mcp"
            assert "tools" in data
            assert len(data["tools"]) == 2
```

### Performance Tests

```python
# tests/test_performance.py
import pytest
import time
import psutil
from unittest.mock import patch

class TestPerformance:
    """Performance benchmarking tests."""
    
    @pytest.mark.asyncio
    async def test_rendering_performance(self, mock_rendergit):
        """Test rendering performance stays within acceptable limits."""
        from mcp_rendergit_sdk import render_repo
        from mcp.server.fastmcp import Context
        
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/octocat/Hello-World"
        
        # Measure performance
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        result = await render_repo(repo_url, ctx)
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        # Performance assertions
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory
        
        assert execution_time < 5.0, f"Rendering took {execution_time}s, expected <5s"
        assert memory_used < 50 * 1024 * 1024, f"Used {memory_used}B memory, expected <50MB"
        assert len(result) > 1000, "Output seems too small"
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, mock_rendergit):
        """Test server handles concurrent requests efficiently."""
        import asyncio
        from mcp_rendergit_sdk import render_repo
        from mcp.server.fastmcp import Context
        
        ctx = AsyncMock(spec=Context)
        repo_url = "https://github.com/octocat/Hello-World"
        
        # Run multiple concurrent requests
        start_time = time.time()
        
        tasks = [render_repo(repo_url, ctx) for _ in range(5)]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        # All requests should complete
        assert len(results) == 5
        assert all(len(result) > 1000 for result in results)
        
        # Should be faster than sequential execution
        total_time = end_time - start_time
        assert total_time < 10.0, f"Concurrent requests took {total_time}s"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_rendergit_sdk --cov-report=html

# Run specific test categories
pytest tests/test_tools.py -v
pytest tests/test_integration.py -v
pytest tests/test_performance.py -v

# Run tests with different verbosity
pytest -v  # verbose
pytest -s  # show prints

# Run tests and generate reports
pytest --html=reports/report.html --self-contained-html
```

## 🔍 Code Quality and Standards

### Code Style

```python
# .flake8
[flake8]
max-line-length = 88
ignore = E203, W503
exclude = .git,__pycache__,docs/source/conf.py,old,build,dist,venv

# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py310']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Code Formatting Commands

```bash
# Format code with black
black mcp_rendergit_sdk.py tests/

# Sort imports with isort
isort mcp_rendergit_sdk.py tests/

# Check code style with flake8
flake8 mcp_rendergit_sdk.py tests/

# Type checking with mypy
mypy mcp_rendergit_sdk.py

# Run all quality checks
black --check mcp_rendergit_sdk.py tests/
isort --check-only mcp_rendergit_sdk.py tests/
flake8 mcp_rendergit_sdk.py tests/
mypy mcp_rendergit_sdk.py
```

## 🚀 Deployment and Release

### Docker Development

```dockerfile
# Dockerfile.dev - Development version with debugging tools
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

# Install rendergit
RUN pip install git+https://github.com/karpathy/rendergit.git

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Development command with file watching
CMD ["python", "-m", "watchdog.auto_restart", "--", "python", "mcp_rendergit_sdk.py"]
```

```bash
# Build and run development container
docker build -f Dockerfile.dev -t rendergit-mcp:dev .
docker run -p 8080:8080 -v $(pwd):/app rendergit-mcp:dev
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt -r requirements-dev.txt
        pip install git+https://github.com/karpathy/rendergit.git
    
    - name: Run code quality checks
      run: |
        black --check .
        isort --check-only .
        flake8 .
        mypy mcp_rendergit_sdk.py
    
    - name: Run tests
      run: |
        pytest --cov=mcp_rendergit_sdk --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Build Docker image
      run: |
        docker build -t rendergit-mcp:latest .
        docker tag rendergit-mcp:latest rendergit-mcp:${{ github.sha }}
    
    - name: Test Docker image
      run: |
        docker run -d -p 8080:8080 --name test-server rendergit-mcp:latest
        sleep 5
        curl -f http://localhost:8080/health
        docker stop test-server
```

### Release Process

```bash
# 1. Update version
# Edit version in mcp_rendergit_sdk.py and other relevant files

# 2. Create release branch
git checkout -b release/v1.0.0

# 3. Update CHANGELOG.md
# Add release notes and changes

# 4. Run full test suite
pytest --cov=mcp_rendergit_sdk

# 5. Build and test Docker image
docker build -t rendergit-mcp:v1.0.0 .
docker run -d -p 8080:8080 rendergit-mcp:v1.0.0
curl http://localhost:8080/health

# 6. Create pull request to main
gh pr create --title "Release v1.0.0" --body "Release version 1.0.0"

# 7. After merge, create git tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# 8. Create GitHub release
gh release create v1.0.0 --title "RendergitMCP v1.0.0" --notes-file CHANGELOG.md
```

## 🐛 Debugging and Troubleshooting

### Debug Mode

```bash
# Enable debug logging
export RENDERGIT_LOG_LEVEL=DEBUG
python mcp_rendergit_sdk.py --transport sse --port 8080

# Or with Python debugger
python -m pdb mcp_rendergit_sdk.py

# Or with debugpy for VS Code
python -m debugpy --listen 5678 --wait-for-client mcp_rendergit_sdk.py
```

### Common Development Issues

#### 1. Import Errors
```python
# Issue: Cannot import rendergit
# Solution: Ensure rendergit is installed
pip install git+https://github.com/karpathy/rendergit.git

# Issue: Cannot import MCP modules
# Solution: Install MCP SDK
pip install mcp fastmcp
```

#### 2. Test Failures
```bash
# Issue: Tests fail due to missing fixtures
# Solution: Check test configuration
pytest --collect-only  # See what tests are discovered
pytest -v tests/test_tools.py::test_specific_function

# Issue: Async tests not running
# Solution: Install pytest-asyncio
pip install pytest-asyncio
```

#### 3. Docker Issues
```bash
# Issue: Docker build fails
# Solution: Check Dockerfile syntax and dependencies
docker build --no-cache -t rendergit-mcp .

# Issue: Container exits immediately
# Solution: Check logs
docker run rendergit-mcp
docker logs <container-id>
```

### Performance Debugging

```python
# profile_server.py - Performance profiling
import cProfile
import pstats
from mcp_rendergit_sdk import render_repo

def profile_render():
    """Profile repository rendering performance."""
    import asyncio
    from mcp.server.fastmcp import Context
    from unittest.mock import AsyncMock
    
    ctx = AsyncMock(spec=Context)
    
    async def run_render():
        await render_repo("https://github.com/octocat/Hello-World", ctx)
    
    asyncio.run(run_render())

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    profile_render()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(20)
```

## 📝 Contributing Guidelines

### Contribution Workflow

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/rendergit-mcp.git
   cd rendergit-mcp
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Changes**
   ```bash
   pytest
   black --check .
   isort --check-only .
   flake8 .
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Use descriptive title and description
   - Reference relevant issues
   - Include test coverage information

### Code Review Checklist

- [ ] Code follows style guidelines (black, isort, flake8)
- [ ] Type hints are present (mypy passes)
- [ ] Tests are added for new functionality
- [ ] Tests pass locally and in CI
- [ ] Documentation is updated
- [ ] Backward compatibility is maintained
- [ ] Performance impact is considered
- [ ] Security implications are reviewed

---

**Ready to contribute?** 🚀 Follow this guide to set up your development environment and start improving RendergitMCP!