# Usage Guide - RendergitMCP

This guide provides comprehensive usage examples and API documentation for RendergitMCP across different scenarios and integrations.

## 🚀 Quick Start

### Starting the Server

```bash
# Basic startup (SSE transport, port 8080)
python mcp_rendergit_sdk.py

# Custom configuration
python mcp_rendergit_sdk.py --transport sse --port 8081

# With environment variables
export RENDERGIT_MAX_SIZE=204800  # 200KB max file size
export RENDERGIT_PORT=9000        # Custom port
python mcp_rendergit_sdk.py
```

### Basic Repository Rendering

```bash
# Example with Claude Code
Use rendergit to analyze https://github.com/karpathy/nanoGPT

# The server will:
# 1. Clone the repository
# 2. Process all source files  
# 3. Generate HTML with Human + LLM views
# 4. Return content for analysis
```

## 📚 MCP Tools Reference

### `render_repo`

Renders a Git repository into HTML content returned directly.

#### Parameters
- **`repo_url`** (string, required): GitHub repository URL

#### Returns
- **Type**: String (HTML content)
- **Size**: Varies (typically 50KB - 2MB depending on repository)

#### Example Usage

```python
# Via MCP client
html_content = await session.call_tool("render_repo", {
    "repo_url": "https://github.com/karpathy/nanoGPT"
})

print(f"HTML length: {len(html_content)} characters")
```

#### URL Formats Supported

```python
# All these formats work:
urls = [
    "https://github.com/karpathy/nanoGPT",      # Full URL
    "http://github.com/karpathy/nanoGPT",       # HTTP (converted to HTTPS)
    "github.com/karpathy/nanoGPT",              # Domain included
    "karpathy/nanoGPT",                         # Simplified format
]
```

### `render_repo_to_file`

Renders a Git repository and saves the HTML to a local file with organized storage.

#### Parameters
- **`repo_url`** (string, required): GitHub repository URL
- **`output_path`** (string, optional): Custom output file path
- **`project_type`** (string, optional): Storage location ('docker' or 'backblaze'), default: 'docker'
- **`project_subpath`** (string, optional): Subdirectory within project type

#### Returns
Dictionary with the following structure:
```json
{
    "success": true,
    "output_path": "/projects/docker/ai-repos/karpathy_nanoGPT.html",
    "repo_url": "https://github.com/karpathy/nanoGPT", 
    "file_size": 1847203,
    "message": "Repository rendered and saved to /projects/docker/ai-repos/karpathy_nanoGPT.html"
}
```

#### Example Usage

```python
# Basic usage with auto-generated path
result = await session.call_tool("render_repo_to_file", {
    "repo_url": "https://github.com/karpathy/nanoGPT"
})
print(f"Saved to: {result['output_path']}")

# Custom output path
result = await session.call_tool("render_repo_to_file", {
    "repo_url": "https://github.com/karpathy/nanoGPT",
    "output_path": "/tmp/nanogpt_analysis.html"
})

# Organized storage with project structure
result = await session.call_tool("render_repo_to_file", {
    "repo_url": "https://github.com/transformers/transformers",
    "project_type": "docker",
    "project_subpath": "ai-research/transformers"
})
# Saves to: /projects/docker/ai-research/transformers/transformers_transformers.html
```

#### File Organization

When `output_path` is not specified, files are organized as:
```
/projects/
├── docker/                    # project_type = "docker"
│   ├── {owner}_{repo}.html   # Default location
│   └── ai-research/          # project_subpath = "ai-research"
│       └── transformers/     # project_subpath = "ai-research/transformers"
│           └── {owner}_{repo}.html
└── backblaze/                # project_type = "backblaze"
    └── backups/              # project_subpath = "backups"
        └── {owner}_{repo}.html
```

## 🎯 Usage Scenarios

### 1. Code Analysis for AI

Perfect for feeding repository content to AI models for analysis.

```python
# Render repository for AI analysis
html_content = await render_repo("https://github.com/karpathy/minGPT")

# The HTML contains both views:
# - Human view: Pretty interface with syntax highlighting
# - LLM view: CXML format perfect for Claude/ChatGPT

# Extract CXML content for AI
import re
cxml_match = re.search(r'<textarea id="llm-text"[^>]*>(.*?)</textarea>', html_content, re.DOTALL)
if cxml_match:
    cxml_content = cxml_match.group(1)
    # Feed this to your AI model
```

### 2. Code Review Preparation

Generate comprehensive repository snapshots for review.

```python
# Render multiple repositories for comparison
repos_to_review = [
    "https://github.com/karpathy/nanoGPT",
    "https://github.com/karpathy/minGPT",
    "https://github.com/openai/gpt-2"
]

for repo in repos_to_review:
    result = await render_repo_to_file(repo, {
        "project_type": "docker",
        "project_subpath": "code-review/gpt-models"
    })
    print(f"Review file: {result['output_path']}")
```

### 3. Documentation Generation

Create comprehensive codebase documentation.

```python
# Render for documentation purposes
result = await render_repo_to_file("https://github.com/mycompany/internal-tool", {
    "project_type": "docker", 
    "project_subpath": "documentation/projects"
})

# The HTML file now contains:
# - Complete directory structure
# - All source files with syntax highlighting
# - Markdown documentation rendered as HTML
# - Search functionality via Ctrl+F
```

### 4. Educational Content

Generate learning materials from open source projects.

```python
# Educational repository collection
learning_repos = [
    ("https://github.com/karpathy/nanoGPT", "basics/transformers"),
    ("https://github.com/pytorch/examples", "basics/pytorch"),
    ("https://github.com/huggingface/transformers", "advanced/nlp")
]

for repo_url, subpath in learning_repos:
    await render_repo_to_file(repo_url, {
        "project_type": "docker",
        "project_subpath": f"education/{subpath}"
    })
```

### 5. Competitive Analysis

Analyze competitor or reference implementations.

```python
# Competitor analysis
competitors = [
    "https://github.com/openai/whisper",
    "https://github.com/facebookresearch/llama", 
    "https://github.com/microsoft/DeepSpeed"
]

analysis_results = []
for repo in competitors:
    result = await render_repo_to_file(repo, {
        "project_type": "docker",
        "project_subpath": "analysis/competitors"
    })
    analysis_results.append(result)
```

## 🔧 Advanced Configuration

### Server Configuration

```python
# mcp_server_config.py
import os

# Environment-based configuration
CONFIG = {
    'host': os.getenv('RENDERGIT_HOST', '0.0.0.0'),
    'port': int(os.getenv('RENDERGIT_PORT', 8080)),
    'max_file_size': int(os.getenv('RENDERGIT_MAX_SIZE', 102400)),  # 100KB
    'clone_timeout': int(os.getenv('RENDERGIT_TIMEOUT', 60)),      # 60 seconds
    'temp_dir': os.getenv('RENDERGIT_TEMP_DIR', '/tmp'),
    'log_level': os.getenv('RENDERGIT_LOG_LEVEL', 'INFO'),
}

# Start server with custom config
python mcp_rendergit_sdk.py \
    --host ${CONFIG['host']} \
    --port ${CONFIG['port']} \
    --transport sse
```

### Custom Output Processing

```python
# Process rendered HTML content
async def process_rendered_repo(repo_url: str):
    html_content = await render_repo(repo_url)
    
    # Extract specific information
    import re
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get file count
    file_sections = soup.find_all('section', class_='file-section')
    file_count = len(file_sections)
    
    # Get repository size info
    size_spans = soup.find_all('span', class_='muted')
    total_size = sum(
        float(span.text.replace('(', '').replace(')', '').split()[0]) 
        for span in size_spans if 'KiB' in span.text or 'MiB' in span.text
    )
    
    # Extract programming languages used
    code_blocks = soup.find_all('div', class_='highlight')
    languages = set()
    for block in code_blocks[:10]:  # Check first 10 code blocks
        if 'language-' in str(block):
            lang = re.search(r'language-(\w+)', str(block))
            if lang:
                languages.add(lang.group(1))
    
    return {
        'file_count': file_count,
        'total_size_kb': total_size,
        'languages': list(languages),
        'html_length': len(html_content)
    }

# Usage
stats = await process_rendered_repo("https://github.com/karpathy/nanoGPT")
print(f"Repository stats: {stats}")
```

## 🌐 Integration Examples

### Claude Code Integration

```bash
# 1. Add MCP server to Claude Code
claude mcp add rendergit-mcp python /path/to/mcp_rendergit_sdk.py

# 2. Use in Claude Code conversations
"Analyze the architecture of https://github.com/karpathy/nanoGPT using rendergit"

# 3. Claude Code will automatically:
#    - Call render_repo with the GitHub URL
#    - Receive the HTML content with dual views
#    - Extract the CXML format for AI analysis
#    - Provide insights about the codebase
```

### Custom MCP Client

```python
# custom_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class RendergitClient:
    def __init__(self, server_path: str):
        self.server_params = StdioServerParameters(
            command="python",
            args=[server_path, "--transport", "stdio"]
        )
    
    async def analyze_repository(self, repo_url: str, save_file: bool = False):
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                if save_file:
                    result = await session.call_tool("render_repo_to_file", {
                        "repo_url": repo_url
                    })
                    return result
                else:
                    html_content = await session.call_tool("render_repo", {
                        "repo_url": repo_url
                    })
                    return {"html_content": html_content}

# Usage
async def main():
    client = RendergitClient("mcp_rendergit_sdk.py")
    
    # Get HTML content directly
    result = await client.analyze_repository("https://github.com/karpathy/minGPT")
    print(f"HTML length: {len(result['html_content'])}")
    
    # Save to file
    result = await client.analyze_repository(
        "https://github.com/karpathy/minGPT", 
        save_file=True
    )
    print(f"Saved to: {result['output_path']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### REST API Wrapper

```python
# rest_wrapper.py - Simple REST API wrapper for the MCP server
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from typing import Optional

app = FastAPI(title="RendergitMCP REST API")

class RenderRequest(BaseModel):
    repo_url: str
    save_to_file: bool = False
    project_type: Optional[str] = "docker"
    project_subpath: Optional[str] = None
    output_path: Optional[str] = None

@app.post("/render")
async def render_repository(request: RenderRequest):
    """Render a GitHub repository to HTML."""
    try:
        # Initialize MCP client (implementation depends on your setup)
        from custom_client import RendergitClient
        
        client = RendergitClient("mcp_rendergit_sdk.py")
        
        if request.save_to_file:
            result = await client.analyze_repository(
                request.repo_url, 
                save_file=True
            )
            return {
                "success": True,
                "file_path": result.get("output_path"),
                "file_size": result.get("file_size")
            }
        else:
            result = await client.analyze_repository(request.repo_url)
            return {
                "success": True,
                "html_length": len(result["html_content"]),
                "preview": result["html_content"][:1000] + "..."
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RendergitMCP REST Wrapper"}

# Run with: uvicorn rest_wrapper:app --host 0.0.0.0 --port 8000
```

## 📊 Performance Considerations

### Repository Size Limits

```python
# Typical processing times and sizes:
REPOSITORY_BENCHMARKS = {
    "small": {
        "size_range": "< 1MB",
        "file_count": "< 50 files", 
        "processing_time": "5-15 seconds",
        "examples": ["karpathy/minGPT", "octocat/Hello-World"]
    },
    "medium": {
        "size_range": "1-10MB",
        "file_count": "50-500 files",
        "processing_time": "15-60 seconds", 
        "examples": ["karpathy/nanoGPT", "pytorch/examples"]
    },
    "large": {
        "size_range": "10-50MB",
        "file_count": "500-2000 files",
        "processing_time": "1-5 minutes",
        "examples": ["huggingface/transformers", "pytorch/pytorch"]
    }
}
```

### Optimization Tips

```python
# 1. Use appropriate file size limits
export RENDERGIT_MAX_SIZE=51200  # 50KB per file

# 2. Implement caching for repeated requests
CACHE_DIR = "/tmp/rendergit_cache"
cache_key = hashlib.md5(repo_url.encode()).hexdigest()
cache_file = f"{CACHE_DIR}/{cache_key}.html"

# 3. Batch multiple repositories
async def batch_render_repositories(repo_urls: list):
    tasks = []
    for url in repo_urls:
        task = render_repo_to_file(url, {
            "project_type": "docker",
            "project_subpath": "batch_processed"
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

## 🚨 Error Handling

### Common Error Scenarios

```python
# Handle common errors gracefully
async def safe_render_repo(repo_url: str):
    try:
        result = await render_repo(repo_url)
        return {"success": True, "content": result}
        
    except Exception as e:
        error_type = type(e).__name__
        
        if "not found" in str(e).lower():
            return {
                "success": False,
                "error": "repository_not_found",
                "message": f"Repository {repo_url} not found or is private"
            }
        elif "timeout" in str(e).lower():
            return {
                "success": False,
                "error": "clone_timeout",
                "message": "Repository cloning timed out - it may be too large"
            }
        elif "permission" in str(e).lower():
            return {
                "success": False,
                "error": "permission_denied", 
                "message": "Access denied - repository may be private"
            }
        else:
            return {
                "success": False,
                "error": "unknown_error",
                "message": str(e)
            }

# Usage with error handling
result = await safe_render_repo("https://github.com/invalid/repo")
if not result["success"]:
    print(f"Error: {result['error']} - {result['message']}")
```

## 🔍 Debugging and Monitoring

### Enable Debug Logging

```bash
# Terminal 1: Start server with debug logging
export RENDERGIT_LOG_LEVEL=DEBUG
python mcp_rendergit_sdk.py --transport sse --port 8080

# Terminal 2: Monitor server health
watch -n 5 'curl -s http://localhost:8080/health | jq'

# Terminal 3: Monitor server info
curl -s http://localhost:8080/info | jq
```

### Performance Monitoring

```python
# Monitor server performance
import time
import psutil
import requests

async def monitor_render_performance(repo_url: str):
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    # Make request
    result = await render_repo(repo_url)
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    metrics = {
        "processing_time": end_time - start_time,
        "memory_used": end_memory - start_memory,
        "output_size": len(result),
        "efficiency": len(result) / (end_time - start_time)  # chars/second
    }
    
    print(f"Performance metrics: {metrics}")
    return metrics
```

---

**Ready to explore repositories?** 🚀 Use these examples to get started with RendergitMCP and transform any GitHub repository into AI-friendly, searchable HTML!