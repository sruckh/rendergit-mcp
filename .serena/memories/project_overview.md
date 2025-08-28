# RenderGit MCP Project Overview

## Purpose
This project aims to create an MCP (Model Context Protocol) server that provides rendergit functionality for LLM interactions. The goal is to:

1. Take GitHub URLs (e.g., "sruckh/ig_phantom" without the full "https://github.com/" prefix)
2. Use rendergit to obtain LLM View: Raw CXML text format output
3. Make this output available as conversation context for LLMs like Claude/ChatGPT

## Current State
- **Status**: The core functionality is implemented in `mcp_rendergit.py`. It's a Flask server that exposes a `/render` endpoint that takes a `repo_url` and returns the rendered HTML.
- **Repository**: Based on https://github.com/karpathy/rendergit functionality
- **Framework**: Uses Claude Flow orchestration and SPARC methodology

## Project Structure
- `.claude/` - Claude Code configuration files
- `.claude-flow/` - Claude Flow metrics and coordination data
- `.hive-mind/` - Hive mind configuration for agent coordination
- `.roo/` - Roo framework rules and configurations
- `.swarm/` - Swarm coordination database and state
- `coordination/` - Task coordination and orchestration
- `memory/` - Session and agent memory storage
- `CLAUDE.md` - Development environment configuration and guidelines
- `GOALS.md` - Project goals and requirements
- `claude-flow.config.json` - Claude Flow feature configuration
- `mcp_rendergit.py` - The main MCP server file.

## Tech Stack
- **Backend**: Python with Flask
- **Runtime**: Node.js v20.19.3, Python 3.13.2
- **Package Manager**: npm v11.4.2
- **Framework**: Claude Flow for agent orchestration
- **Protocol**: MCP (Model Context Protocol) server implementation
- **Coordination**: SPARC methodology with TDD approach
- **Development**: Linux environment with concurrent execution patterns

## Key Features Enabled
- Auto topology selection
- Parallel execution
- Neural training
- Smart auto-spawning
- Self-healing workflows
- Cross-session memory
- GitHub integration
