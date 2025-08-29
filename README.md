# RendergitMCP - MCP Server for Repository Rendering

> Transform any GitHub repository into LLM-friendly HTML with a single MCP call.

**RendergitMCP** is a Model Context Protocol (MCP) server that brings [Andrej Karpathy's rendergit](https://github.com/karpathy/rendergit) functionality to Claude Code and other MCP-compatible clients. It flattens GitHub repositories into single HTML files optimized for AI analysis and human code review.

## 🚀 Features

### Dual View Modes
- **👤 Human View**: Beautiful interface with syntax highlighting, sidebar navigation, and responsive design
- **🤖 LLM View**: Raw CXML text format - perfect for copying to Claude/ChatGPT for code analysis

### Smart Repository Processing  
- **Syntax highlighting** for code files via Pygments
- **Markdown rendering** for README files and documentation
- **Smart filtering** - automatically skips binaries and oversized files
- **Directory tree** overview with file size information
- **Search-friendly** - use Ctrl+F to find anything across all files
- **Responsive design** that works on mobile devices

### MCP Integration
- **Two MCP tools**: `render_repo` (returns HTML) and `render_repo_to_file` (saves to disk)
- **SSE Transport**: Compatible with Claude Code's Server-Sent Events transport
- **Health monitoring**: Built-in health check and server info endpoints
- **Flexible output**: Save to custom paths or auto-generated locations

## 🛠 Installation

### Prerequisites
- Python 3.10 or higher
- Git installed and accessible from command line
- MCP-compatible client (like Claude Code)

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sruckh/rendergit-mcp.git
   cd rendergit-mcp
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or use uv for faster installation
   uv pip install -r requirements.txt
   ```

3. **Install rendergit**:
   ```bash
   pip install git+https://github.com/karpathy/rendergit.git
   ```

### Docker Setup

```bash
# Build the container
docker build -t rendergit-mcp .

# Run the server
docker run -p 8080:8080 rendergit-mcp
```

## 📋 MCP Tools

### `render_repo`
Renders a Git repository into HTML content returned directly.

**Parameters:**
- `repo_url` (string): GitHub repository URL

**Returns:** HTML content as string

**Example:**
```python
# Via MCP client
result = mcp_client.call_tool("render_repo", {
    "repo_url": "https://github.com/karpathy/nanoGPT"
})
```

### `render_repo_to_file`
Renders a Git repository and saves the HTML to a local file.

**Parameters:**
- `repo_url` (string): GitHub repository URL
- `output_path` (string, optional): Custom output path
- `project_type` (string, optional): Storage location ('docker' or 'backblaze'), default 'docker'
- `project_subpath` (string, optional): Subdirectory within project type

**Returns:** Dictionary with success status, file path, and metadata

**Example:**
```python
# Via MCP client
result = mcp_client.call_tool("render_repo_to_file", {
    "repo_url": "https://github.com/karpathy/nanoGPT",
    "project_type": "docker",
    "project_subpath": "ai-repos"
})
```

## 🔧 Usage Examples

### Basic Repository Rendering

```bash
# Start the MCP server
python mcp_rendergit_sdk.py --transport sse --port 8080
```

Then from your MCP client (like Claude Code):

```python
# Render repository to HTML string
html_content = render_repo("https://github.com/karpathy/nanoGPT")

# Render and save to file
result = render_repo_to_file(
    "https://github.com/karpathy/nanoGPT",
    output_path="/tmp/nanogpt.html"
)
print(f"Saved to: {result['output_path']}")
print(f"File size: {result['file_size']} bytes")
```

### Simplified Repository URLs

The server accepts various URL formats:
- `https://github.com/owner/repo` (full URL)
- `github.com/owner/repo` (without protocol)  
- `owner/repo` (simplified format)

### Output File Organization

When using `render_repo_to_file` without specifying `output_path`:
- Files are saved to `/projects/{project_type}/{project_subpath}/`
- Filename format: `{owner}_{repo}.html`
- Example: `/projects/docker/ai-repos/karpathy_nanoGPT.html`

## 🏗 Architecture

### Core Components

- **`mcp_rendergit_sdk.py`**: Main MCP server using FastMCP framework
- **`rendergit` integration**: Uses Karpathy's original rendergit library
- **SSE Transport**: Server-Sent Events for Claude Code compatibility
- **Health monitoring**: `/health` and `/info` endpoints

### File Structure

```
rendergit-mcp/
├── mcp_rendergit_sdk.py    # Main MCP server
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── docs/                   # Documentation
│   ├── INSTALL.md         # Installation guide
│   ├── USAGE.md           # Usage examples
│   └── DEVELOPMENT.md     # Development guide
└── vendor/                 # Vendored dependencies
```

## 🔄 Integration with Claude Code

1. **Add MCP server to Claude Code**:
   ```bash
   claude mcp add rendergit-mcp python /path/to/mcp_rendergit_sdk.py
   ```

2. **Use in conversations**:
   ```
   Use rendergit to analyze https://github.com/karpathy/nanoGPT
   ```

3. **The server will**:
   - Clone the repository
   - Process all source files
   - Generate HTML with dual Human/LLM views
   - Return content for AI analysis

## 🧪 Development

### Running Tests

```bash
python -m pytest tests/
```

### Development Mode

```bash
# Install in development mode
pip install -e .

# Run with debug logging
python mcp_rendergit_sdk.py --transport sse --port 8080
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📊 Performance

- **Fast cloning**: Uses shallow clones (`--depth 1`) for speed
- **Smart filtering**: Automatically skips binary files and large files
- **Efficient rendering**: Processes files in memory without temporary storage
- **Responsive output**: Handles repositories up to 100MB efficiently

## 🔧 Configuration

### Environment Variables

- `RENDERGIT_MAX_SIZE`: Maximum file size to process (default: 100KB)
- `RENDERGIT_TIMEOUT`: Git clone timeout (default: 60s)
- `RENDERGIT_TEMP_DIR`: Temporary directory for clones

### Server Options

- `--transport`: Transport type (sse, stdio)
- `--port`: Server port (default: 8080)
- `--host`: Server host (default: 0.0.0.0)

## 🐛 Troubleshooting

### Common Issues

1. **Git clone failures**: Ensure Git is installed and repository is accessible
2. **Large repositories**: Some repositories may exceed processing limits
3. **Network timeouts**: Check internet connectivity and repository availability

### Debug Mode

```bash
# Enable debug logging
export PYTHONPATH=.
python -m logging.DEBUG mcp_rendergit_sdk.py
```

## 📝 License

This project builds on [Andrej Karpathy's rendergit](https://github.com/karpathy/rendergit) (0BSD License).

MCP integration code is available under MIT License.

## 🙏 Acknowledgments

- **Andrej Karpathy** for the original rendergit tool
- **Anthropic** for the MCP protocol and Claude Code integration
- **FastMCP** team for the excellent MCP Python framework

## 🔗 Links

- **Original rendergit**: https://github.com/karpathy/rendergit
- **MCP Protocol**: https://github.com/modelcontextprotocol/specification
- **Claude Code**: https://claude.ai/code
- **FastMCP**: https://github.com/jlowin/fastmcp

---

**Ready to transform repositories into AI-friendly HTML?** Install RendergitMCP and start analyzing codebases with a single MCP call! 🚀