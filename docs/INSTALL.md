# Installation Guide - RendergitMCP

This guide provides comprehensive installation instructions for RendergitMCP across different environments and use cases.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **Git**: Latest version (for repository cloning)
- **Memory**: Minimum 512MB RAM (2GB+ recommended)
- **Storage**: 100MB for base installation + space for rendered repositories

### Platform Support
- ✅ **Linux** (Ubuntu 20.04+, RHEL 8+, etc.)
- ✅ **macOS** (10.15+ Catalina)
- ✅ **Windows** (10/11 with WSL2 recommended)
- ✅ **Docker** (Any platform supporting Docker)

## 🚀 Quick Installation

### Option 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/sruckh/rendergit-mcp.git
cd rendergit-mcp

# Install Python dependencies
pip install -r requirements.txt

# Install the original rendergit
pip install git+https://github.com/karpathy/rendergit.git

# Test the installation
python mcp_rendergit_sdk.py --help
```

### Option 2: Using UV (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast Python package installer:

```bash
# Install UV first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/sruckh/rendergit-mcp.git
cd rendergit-mcp

# Install dependencies with UV
uv pip install -r requirements.txt
uv pip install git+https://github.com/karpathy/rendergit.git

# Run the server
python mcp_rendergit_sdk.py
```

### Option 3: Docker Installation

```bash
# Clone repository
git clone https://github.com/sruckh/rendergit-mcp.git
cd rendergit-mcp

# Build Docker image
docker build -t rendergit-mcp .

# Run container
docker run -p 8080:8080 rendergit-mcp
```

## 🔧 Detailed Installation Steps

### 1. Environment Setup

#### Linux (Ubuntu/Debian)
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+ and Git
sudo apt install python3.10 python3.10-venv python3.10-dev git -y

# Install pip
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

#### macOS
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Git
brew install python@3.10 git

# Ensure Python 3.10 is in PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows (WSL2)
```bash
# Install WSL2 with Ubuntu (run in PowerShell as Administrator)
wsl --install -d Ubuntu

# Once in Ubuntu WSL2
sudo apt update && sudo apt install python3.10 python3.10-venv git curl -y
```

### 2. Virtual Environment (Recommended)

```bash
# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows (WSL2):
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install MCP SDK and FastMCP
pip install mcp fastmcp

# Install rendergit dependencies
pip install markdown>=3.8.2 pygments>=2.19.2

# Install original rendergit
pip install git+https://github.com/karpathy/rendergit.git

# Install additional dependencies
pip install aiofiles starlette uvicorn
```

### 4. Verify Installation

```bash
# Test rendergit CLI
rendergit --help

# Test Python imports
python -c "
import mcp
from mcp.server.fastmcp import FastMCP
from rendergit import render_repo_html
print('✅ All dependencies installed correctly')
"

# Test MCP server startup
python mcp_rendergit_sdk.py --transport sse --port 8080 &
sleep 5
curl http://localhost:8080/health
pkill -f mcp_rendergit_sdk.py
```

## 🐳 Docker Installation

### Build from Source

```dockerfile
# Clone repository
git clone https://github.com/sruckh/rendergit-mcp.git
cd rendergit-mcp

# Build image
docker build -t rendergit-mcp:latest .

# Run container
docker run -d \
  --name rendergit-mcp \
  -p 8080:8080 \
  -e RENDERGIT_MAX_SIZE=102400 \
  rendergit-mcp:latest
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  rendergit-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - RENDERGIT_MAX_SIZE=102400
      - RENDERGIT_TIMEOUT=60
    volumes:
      - ./output:/projects
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
# Start with Docker Compose
docker-compose up -d

# Check status
docker-compose logs -f rendergit-mcp
```

## 🔗 MCP Client Integration

### Claude Code Setup

1. **Add MCP Server**:
   ```bash
   claude mcp add rendergit-mcp python /path/to/mcp_rendergit_sdk.py
   ```

2. **Configure Transport**:
   ```json
   {
     "mcpServers": {
       "rendergit-mcp": {
         "command": "python",
         "args": ["/path/to/mcp_rendergit_sdk.py", "--transport", "sse"],
         "env": {}
       }
     }
   }
   ```

3. **Test Integration**:
   ```bash
   # In Claude Code
   Use rendergit to analyze https://github.com/karpathy/nanoGPT
   ```

### Custom MCP Client

```python
# Example Python MCP client
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python", 
        args=["mcp_rendergit_sdk.py", "--transport", "stdio"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Use render_repo tool
            result = await session.call_tool("render_repo", {
                "repo_url": "https://github.com/karpathy/nanoGPT"
            })
            print(f"Rendered HTML length: {len(result.content)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project directory:

```bash
# .env file
RENDERGIT_MAX_SIZE=102400      # Maximum file size (100KB)
RENDERGIT_TIMEOUT=60           # Git clone timeout (seconds)
RENDERGIT_TEMP_DIR=/tmp        # Temporary directory for clones
RENDERGIT_LOG_LEVEL=INFO       # Logging level
RENDERGIT_HOST=0.0.0.0         # Server host
RENDERGIT_PORT=8080            # Server port
```

### Server Configuration

```python
# config.py (optional)
import os

class Config:
    MAX_FILE_SIZE = int(os.getenv('RENDERGIT_MAX_SIZE', 102400))
    CLONE_TIMEOUT = int(os.getenv('RENDERGIT_TIMEOUT', 60))
    TEMP_DIR = os.getenv('RENDERGIT_TEMP_DIR', '/tmp')
    LOG_LEVEL = os.getenv('RENDERGIT_LOG_LEVEL', 'INFO')
    HOST = os.getenv('RENDERGIT_HOST', '0.0.0.0')
    PORT = int(os.getenv('RENDERGIT_PORT', 8080))
```

## 🧪 Testing Installation

### Basic Functionality Test

```bash
# Test script: test_installation.sh
#!/bin/bash

echo "🧪 Testing RendergitMCP Installation"

# Test 1: Python imports
echo "Testing Python imports..."
python -c "
import sys
try:
    from mcp.server.fastmcp import FastMCP
    from rendergit import render_repo_html
    print('✅ Python imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Test 2: Server startup
echo "Testing server startup..."
python mcp_rendergit_sdk.py --transport sse --port 8081 &
SERVER_PID=$!
sleep 3

# Test 3: Health check
echo "Testing health endpoint..."
HEALTH_STATUS=$(curl -s http://localhost:8081/health | jq -r '.status')
if [ "$HEALTH_STATUS" = "healthy" ]; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    kill $SERVER_PID
    exit 1
fi

# Test 4: Server info
echo "Testing server info..."
curl -s http://localhost:8081/info | jq .

# Cleanup
kill $SERVER_PID
echo "✅ All tests passed!"
```

### Advanced Testing

```python
# test_mcp_integration.py
import asyncio
import tempfile
from pathlib import Path

async def test_render_repo():
    """Test repository rendering functionality."""
    
    # Import after installation
    from rendergit import render_repo_html
    
    # Test with a small public repository
    test_repo = "https://github.com/octocat/Hello-World"
    
    try:
        # Test rendering
        html_content = render_repo_html(test_repo, 50000)  # 50KB limit
        
        # Verify content
        assert len(html_content) > 1000, "HTML content too short"
        assert "Hello-World" in html_content, "Repository name not found"
        assert "class=\"highlight\"" in html_content, "Syntax highlighting missing"
        
        print("✅ Repository rendering test passed")
        return True
        
    except Exception as e:
        print(f"❌ Repository rendering test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_render_repo())
    exit(0 if success else 1)
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Error: ModuleNotFoundError: No module named 'mcp'
# Solution:
pip install mcp fastmcp

# Error: ModuleNotFoundError: No module named 'rendergit'
# Solution:
pip install git+https://github.com/karpathy/rendergit.git
```

#### 2. Git Clone Issues
```bash
# Error: fatal: could not read Username for 'https://github.com'
# Solution: Ensure Git is installed and configured
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Permission Issues
```bash
# Error: Permission denied
# Solution: Check file permissions
chmod +x mcp_rendergit_sdk.py

# For Docker
sudo docker run -p 8080:8080 rendergit-mcp
```

#### 4. Port Conflicts
```bash
# Error: Address already in use
# Solution: Use different port
python mcp_rendergit_sdk.py --port 8081

# Or find and kill process using port
lsof -ti:8080 | xargs kill -9
```

### Debug Mode

```bash
# Enable debug logging
export PYTHONPATH=.
export RENDERGIT_LOG_LEVEL=DEBUG
python mcp_rendergit_sdk.py --transport sse --port 8080
```

### Getting Help

If you encounter issues:

1. **Check logs**: Look for error messages in console output
2. **Verify prerequisites**: Ensure all dependencies are installed
3. **Test components**: Run individual tests to isolate issues
4. **Check GitHub Issues**: Search existing issues at https://github.com/sruckh/rendergit-mcp/issues
5. **Create issue**: If problem persists, create a detailed issue report

---

**Installation complete!** 🎉 Your RendergitMCP server is ready to transform repositories into AI-friendly HTML.