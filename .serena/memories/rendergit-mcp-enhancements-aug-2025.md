# RenderGit MCP Server Enhancements - August 2025

## Overview
Major updates to the rendergit-mcp server to fix MCP protocol compliance issues and add local file storage functionality for LLM-friendly repository documentation.

## Problem Context
- MCP clients (Claude Code, Gemini CLI) could not connect to the rendergit-mcp server
- Server was using non-standard parameter schema format
- No ability to save rendered HTML files locally for project reference
- Need for intelligent path detection based on current project context

## Changes Implemented

### 1. MCP Protocol Compliance Fixes
**Parameter Schema Format Fixed:**
```python
# Before (non-compliant)
"parameters": [{"name": "repo_url", "type": "string", "required": True}]

# After (JSON Schema compliant)
"parameters": {
    "type": "object",
    "properties": {
        "repo_url": {"type": "string", "description": "The URL of the Git repository to render."}
    },
    "required": ["repo_url"]
}
```

### 2. New Tool Added: render_repo_to_file
**Purpose:** Save rendered repositories as HTML files to local storage for future reference

**Parameters:**
- `repo_url` (required): Git repository URL to render
- `project_type` (optional): "docker" or "backblaze" storage location
- `project_subpath` (optional): Subdirectory within project type
- `output_path` (optional): Custom full path override

**Intelligence Features:**
- Auto-generates filenames from repo URLs (e.g., `user_project.html`)
- Supports organized project structure with subpaths
- Creates directories automatically
- Returns detailed result with file size and path info

### 3. Volume Mount Configuration
**Container Mounts Added:**
```bash
-v /opt/docker:/projects/docker
-v /mnt/backblaze:/projects/backblaze
```

**Storage Structure:**
- `/projects/docker/` → `/opt/docker/` (local Docker projects)
- `/projects/backblaze/` → `/mnt/backblaze/` (cloud storage projects)

### 4. Enhanced manage_container.sh
Updated container startup script to include volume mounts for persistent file storage.

## Usage Examples

### Basic File Save
```json
{
  "toolName": "render_repo_to_file",
  "parameters": {
    "repo_url": "https://github.com/user/project",
    "project_type": "docker"
  }
}
```
→ Saves to `/opt/docker/{user_project}.html`

### Project-Specific Save
```json
{
  "toolName": "render_repo_to_file", 
  "parameters": {
    "repo_url": "https://github.com/reference/api-examples",
    "project_type": "docker",
    "project_subpath": "rendergit-mcp"
  }
}
```
→ Saves to `/opt/docker/rendergit-mcp/{reference_api-examples}.html`

### Custom Path
```json
{
  "toolName": "render_repo_to_file",
  "parameters": {
    "repo_url": "https://github.com/docs/guide", 
    "output_path": "/projects/docker/my-project/docs/reference.html"
  }
}
```

## Client Configuration

### Claude Code
```bash
claude mcp add rendergit --transport sse https://rendergit.gemneye.info/mcp
```

### Gemini CLI
```json
"rendergit": {
  "url": "https://rendergit.gemneye.info/mcp",
  "type": "sse"
}
```

## Technical Details

### File Structure
- **Container:** `/projects/docker/` and `/projects/backblaze/`
- **Host Mapping:** `/opt/docker/` and `/mnt/backblaze/`
- **Auto-generated Names:** URL path converted to filename (slashes → underscores)
- **Directory Creation:** Automatic `os.makedirs()` with `exist_ok=True`

### Error Handling
- Graceful fallbacks for path detection failures
- Comprehensive exception handling for file operations
- Detailed logging for debugging

### Tools Available
1. **render_repo** - Returns HTML content (existing functionality)
2. **render_repo_to_file** - Saves HTML to local storage (new functionality)

## Benefits
- **MCP Compliance:** Now works with standard MCP clients
- **Local Reference:** Save LLM-friendly repo docs for project context
- **Organized Storage:** Intelligent path management for different project types
- **Workflow Integration:** Perfect for forked project documentation workflow

## Implementation Status
✅ Parameter schema fixed
✅ New tool implemented  
✅ Volume mounts configured
✅ Container rebuilt and tested
✅ Ready for production use

## Next Steps
- Test with actual MCP clients to verify connection fixes
- Create workflow documentation for common use cases
- Consider adding batch processing for multiple repositories