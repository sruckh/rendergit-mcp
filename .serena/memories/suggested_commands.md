# Suggested Commands for RenderGit MCP Development

## Claude Flow Commands

### SPARC Methodology
- `npx claude-flow sparc modes` - List available SPARC modes
- `npx claude-flow sparc run <mode> "<task>"` - Execute specific SPARC mode
- `npx claude-flow sparc tdd "<feature>"` - Run complete TDD workflow
- `npx claude-flow sparc info <mode>` - Get detailed mode information

### Batch Operations
- `npx claude-flow sparc batch <modes> "<task>"` - Parallel execution of multiple modes
- `npx claude-flow sparc pipeline "<task>"` - Full pipeline processing
- `npx claude-flow sparc concurrent <mode> "<tasks-file>"` - Multi-task processing

### Build and Test Commands
- `npm run build` - Build the project (when package.json is created)
- `npm run test` - Run tests
- `npm run lint` - Run linting
- `npm run typecheck` - Type checking

## MCP Server Setup
- `claude mcp add claude-flow npx claude-flow@alpha mcp start` - Add Claude Flow MCP server
- Check `.mcp.json` for configured MCP servers

## Application execution
- `python3 mcp_rendergit.py` - Run the Flask server

## System Commands (Linux)
- `ls -la` - List files with details
- `find . -name "*.py"` - Find Python files
- `find . -name "*.js"` - Find JavaScript files  
- `find . -name "*.ts"` - Find TypeScript files
- `grep -r "pattern" .` - Search for patterns recursively
- `cd /opt/docker/rendergit-mcp` - Navigate to project root

## Git Operations
- `git status` - Check repository status
- `git add .` - Stage all changes
- `git commit -m "message"` - Commit with message
- `git push` - Push to remote repository

## Environment Tools
- `python3 --version` - Check Python version (3.13.2)
- `node --version` - Check Node.js version (v20.19.3)
- `npm --version` - Check npm version (11.4.2)
- `which python3` - Find Python executable path
- `which node` - Find Node.js executable path

## Claude Flow Agent Commands
These commands are used within the SPARC methodology for agent coordination and execution.