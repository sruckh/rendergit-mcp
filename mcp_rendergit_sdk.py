#!/usr/bin/env python3
"""
MCP-compliant rendergit server using official MCP Python SDK.
Supports SSE transport for Claude Code compatibility.
"""
import asyncio
import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP, Context
from rendergit import render_repo_html
from starlette.requests import Request
from starlette.responses import JSONResponse

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create MCP server
mcp = FastMCP("rendergit-mcp")


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Health check endpoint for monitoring and load balancing."""
    return JSONResponse({
        "status": "healthy",
        "service": "rendergit-mcp",
        "version": "2.0.0",
        "transport": "sse"
    })


@mcp.custom_route("/info", methods=["GET"])
async def server_info(request: Request):
    """Server information endpoint."""
    return JSONResponse({
        "service": "rendergit-mcp", 
        "description": "MCP server for rendering Git repositories as LLM-friendly HTML",
        "version": "2.0.0",
        "health": "/health",
        "mcp_endpoint": "/",
        "tools": ["render_repo", "render_repo_to_file"]
    })


@mcp.tool()
async def render_repo(repo_url: str, ctx: Context) -> str:
    """
    Renders a Git repository into a single HTML file optimized for LLM context.
    
    Args:
        repo_url: The URL of the Git repository to render.
        
    Returns:
        HTML content of the rendered repository.
    """
    await ctx.info(f"Rendering repository: {repo_url}")
    
    try:
        html_content = render_repo_html(repo_url, 100 * 1024)
        await ctx.info(f"Successfully rendered {len(html_content)} characters")
        return html_content
        
    except Exception as e:
        await ctx.error(f"Failed to render repository: {str(e)}")
        raise


@mcp.tool()
async def render_repo_to_file(
    repo_url: str,
    ctx: Context,
    output_path: str = None,
    project_type: str = "docker",
    project_subpath: str = ""
) -> dict:
    """
    Renders a Git repository into a single HTML file and saves it to local storage.
    
    Args:
        repo_url: The URL of the Git repository to render.
        output_path: Optional custom output path. If not provided, will auto-generate.
        project_type: Project storage location: 'docker' or 'backblaze'.
        project_subpath: Optional subdirectory within the project type.
        
    Returns:
        Dictionary with success status, file path, and metadata.
    """
    await ctx.info(f"Rendering repository to file: {repo_url}")
    
    try:
        # Render the repository
        html_content = render_repo_html(repo_url, 100 * 1024)
        
        # Generate output path if not provided
        if not output_path:
            parsed_url = urlparse(repo_url)
            repo_name = parsed_url.path.strip('/').replace('/', '_')
            
            # Build the base path with optional subpath
            if project_subpath.strip():
                base_path = f"/projects/{project_type}/{project_subpath.strip()}"
            else:
                # Default to current project directory name
                # If CWD is /opt/docker/rendergit-mcp, use 'rendergit-mcp' as subpath
                current_dir_name = os.path.basename(os.getcwd())
                base_path = f"/projects/{project_type}/{current_dir_name}"
                
            output_path = f"{base_path}/{repo_name}.html"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write HTML to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        result = {
            "success": True,
            "output_path": output_path,
            "repo_url": repo_url,
            "file_size": len(html_content),
            "message": f"Repository rendered and saved to {output_path}"
        }
        
        await ctx.info(f"Successfully saved to {output_path} ({len(html_content)} bytes)")
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to render repository to file: {str(e)}")
        raise


def main():
    """Entry point for the MCP server."""
    # Parse command line arguments for transport type
    transport = "sse"  # Use SSE transport with /sse endpoint
    port = 8080
    
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv[1:], 1):
            if arg == "--transport" and i + 1 < len(sys.argv):
                transport = sys.argv[i + 1]
            elif arg == "--port" and i + 1 < len(sys.argv):
                port = int(sys.argv[i + 1])
    
    # Configure FastMCP settings before running
    mcp.settings.host = "0.0.0.0"  # Allow external connections
    mcp.settings.port = port
    
    logging.info(f"Starting rendergit MCP server with {transport} transport on {mcp.settings.host}:{mcp.settings.port}")
    
    # Run the server with specified transport
    mcp.run(transport=transport)


if __name__ == '__main__':
    main()