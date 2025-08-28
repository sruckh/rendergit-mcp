#!/usr/bin/env python3
"""
MCP-compliant rendergit server using Flask and proper MCP protocol.
Based on official MCP TypeScript SDK patterns.
"""
import json
import logging
import os
import uuid
from pathlib import Path
from urllib.parse import urlparse
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS
from rendergit import render_repo_html

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = Flask(__name__)
CORS(app, expose_headers=['Mcp-Session-Id'], allow_headers=['Content-Type', 'mcp-session-id'])

# Store active SSE connections
active_connections = {}

def mcp_error_response(code: int, message: str, id=None):
    """Create MCP-compliant error response"""
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": id
    }

def mcp_result_response(result, id):
    """Create MCP-compliant result response"""
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": id
    }

def sse_event(data):
    """Format data as Server-Sent Event"""
    return f"data: {json.dumps(data)}\n\n"

@app.route('/sse', methods=['GET'])
def sse_endpoint():
    """SSE endpoint for MCP server-to-client communication"""
    session_id = str(uuid.uuid4())
    
    def sse_stream():
        try:
            # Send initialization message with server capabilities
            server_info = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        }
                    },
                    "serverInfo": {
                        "name": "rendergit-mcp",
                        "version": "0.3.0"
                    }
                }
            }
            yield sse_event(server_info)
            
            # Keep connection alive
            while True:
                try:
                    # Check for any messages queued for this session
                    if session_id in active_connections:
                        connection = active_connections[session_id]
                        if connection.get('messages'):
                            for message in connection['messages']:
                                yield sse_event(message)
                            connection['messages'] = []
                    
                    # Keep-alive ping
                    import time
                    time.sleep(15)
                    yield ": keep-alive\n\n"
                except GeneratorExit:
                    break
        except Exception as e:
            logging.error(f"SSE stream error: {e}")
        finally:
            if session_id in active_connections:
                del active_connections[session_id]
            logging.info(f"SSE connection {session_id} closed")
    
    active_connections[session_id] = {'messages': []}
    logging.info(f"SSE connection established: {session_id}")
    
    response = Response(
        stream_with_context(sse_stream()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )
    response.headers['Mcp-Session-Id'] = session_id
    return response

@app.route('/messages', methods=['POST'])
def messages_endpoint():
    """Handle MCP messages from client"""
    try:
        data = request.get_json()
        if not data:
            return Response(
                json.dumps(mcp_error_response(-32700, "Parse error")),
                status=400,
                mimetype='application/json'
            )
        
        # Handle different MCP method calls
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        
        if method == 'initialize':
            # MCP initialization
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {
                        "listChanged": True
                    }
                },
                "serverInfo": {
                    "name": "rendergit-mcp",
                    "version": "0.3.0"
                }
            }
            return Response(
                json.dumps(mcp_result_response(result, request_id)),
                mimetype='application/json'
            )
        
        elif method == 'tools/list':
            # List available tools
            tools = [
                {
                    "name": "render_repo",
                    "description": "Renders a Git repository into a single HTML file optimized for LLM context and returns the HTML content.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo_url": {
                                "type": "string",
                                "description": "The URL of the Git repository to render."
                            }
                        },
                        "required": ["repo_url"]
                    }
                },
                {
                    "name": "render_repo_to_file",
                    "description": "Renders a Git repository into a single HTML file and saves it to local storage for future reference.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "repo_url": {
                                "type": "string",
                                "description": "The URL of the Git repository to render."
                            },
                            "output_path": {
                                "type": "string",
                                "description": "Optional custom output path. If not provided, will auto-generate based on repo name."
                            },
                            "project_type": {
                                "type": "string",
                                "enum": ["docker", "backblaze"],
                                "description": "Project storage location: 'docker' for /projects/docker or 'backblaze' for /projects/backblaze",
                                "default": "docker"
                            },
                            "project_subpath": {
                                "type": "string",
                                "description": "Optional subdirectory within the project type (e.g., 'rendergit-mcp' to save to /projects/docker/rendergit-mcp/)"
                            }
                        },
                        "required": ["repo_url"]
                    }
                }
            ]
            
            result = {"tools": tools}
            return Response(
                json.dumps(mcp_result_response(result, request_id)),
                mimetype='application/json'
            )
        
        elif method == 'tools/call':
            # Execute a tool
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            try:
                if tool_name == "render_repo":
                    repo_url = arguments.get('repo_url')
                    if not repo_url:
                        return Response(
                            json.dumps(mcp_error_response(-32602, "Missing repo_url parameter", request_id)),
                            status=400,
                            mimetype='application/json'
                        )
                    
                    logging.info(f"Executing render_repo for {repo_url}")
                    html_content = render_repo_html(repo_url, 100 * 1024)
                    
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": html_content
                            }
                        ]
                    }
                    return Response(
                        json.dumps(mcp_result_response(result, request_id)),
                        mimetype='application/json'
                    )
                
                elif tool_name == "render_repo_to_file":
                    repo_url = arguments.get('repo_url')
                    if not repo_url:
                        return Response(
                            json.dumps(mcp_error_response(-32602, "Missing repo_url parameter", request_id)),
                            status=400,
                            mimetype='application/json'
                        )
                    
                    output_path = arguments.get('output_path')
                    project_type = arguments.get('project_type', 'docker')
                    project_subpath = arguments.get('project_subpath', '')
                    
                    logging.info(f"Executing render_repo_to_file for {repo_url}")
                    html_content = render_repo_html(repo_url, 100 * 1024)
                    
                    # Generate output path if not provided
                    if not output_path:
                        parsed_url = urlparse(repo_url)
                        repo_name = parsed_url.path.strip('/').replace('/', '_')
                        
                        # Build the base path with optional subpath
                        if project_subpath.strip():
                            base_path = f"/projects/{project_type}/{project_subpath.strip()}"
                        else:
                            base_path = f"/projects/{project_type}"
                        
                        output_path = f"{base_path}/{repo_name}.html"
                    
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    
                    # Write HTML to file
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({
                                    "success": True,
                                    "output_path": output_path,
                                    "repo_url": repo_url,
                                    "file_size": len(html_content),
                                    "message": f"Repository rendered and saved to {output_path}"
                                }, indent=2)
                            }
                        ]
                    }
                    return Response(
                        json.dumps(mcp_result_response(result, request_id)),
                        mimetype='application/json'
                    )
                
                else:
                    return Response(
                        json.dumps(mcp_error_response(-32601, f"Unknown tool: {tool_name}", request_id)),
                        status=400,
                        mimetype='application/json'
                    )
                    
            except Exception as e:
                logging.error(f"Tool execution error: {e}", exc_info=True)
                return Response(
                    json.dumps(mcp_error_response(-32603, f"Internal error: {str(e)}", request_id)),
                    status=500,
                    mimetype='application/json'
                )
        
        else:
            return Response(
                json.dumps(mcp_error_response(-32601, f"Unknown method: {method}", request_id)),
                status=400,
                mimetype='application/json'
            )
    
    except Exception as e:
        logging.error(f"Message handling error: {e}", exc_info=True)
        return Response(
            json.dumps(mcp_error_response(-32603, "Internal server error")),
            status=500,
            mimetype='application/json'
        )

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "server": "rendergit-mcp", "version": "0.3.0"}

if __name__ == '__main__':
    logging.info("Starting MCP-compliant rendergit server")
    app.run(host='0.0.0.0', port=8080, debug=False)