# MCP Server Configuration

## Current MCP Servers
Based on `.mcp.json` configuration, the following MCP servers are available:

### Claude Flow MCP Server
- **Command**: `npx claude-flow@alpha mcp start`
- **Type**: stdio
- **Purpose**: Agent orchestration, SPARC methodology, swarm coordination
- **Features**: 
  - Auto topology selection
  - Parallel execution
  - Neural training
  - Smart auto-spawning
  - Self-healing workflows
  - Cross-session memory
  - GitHub integration

### Ruv Swarm MCP Server  
- **Command**: `npx ruv-swarm@latest mcp start`
- **Type**: stdio
- **Purpose**: Advanced swarm coordination and distributed systems
- **Features**: 
  - Distributed consensus protocols
  - Byzantine fault tolerance
  - CRDT synchronization
  - Performance benchmarking

## Configuration Files

### MCP Server Configuration (`.mcp.json`)
```json
{
  "mcpServers": {
    "claude-flow": {
      "command": "npx",
      "args": ["claude-flow@alpha", "mcp", "start"],
      "type": "stdio"
    },
    "ruv-swarm": {
      "command": "npx", 
      "args": ["ruv-swarm@latest", "mcp", "start"],
      "type": "stdio"
    }
  }
}
```

### Claude Flow Configuration (`claude-flow.config.json`)
- **Max Agents**: 10
- **Default Topology**: hierarchical
- **Execution Strategy**: parallel
- **Token Optimization**: enabled
- **Cache**: enabled
- **Telemetry Level**: detailed

## Setup Instructions
1. Add Claude Flow MCP server: `claude mcp add claude-flow npx claude-flow@alpha mcp start`
2. Verify servers are configured in `.mcp.json`
3. Test server connectivity and functionality
4. Use MCP tools for coordination setup only
5. Use Claude Code's Task tool for actual agent execution

## Tool Categories

### Claude Flow MCP Tools
- Coordination: `swarm_init`, `agent_spawn`, `task_orchestrate`
- Monitoring: `swarm_status`, `agent_list`, `agent_metrics`, `task_status`, `task_results`
- Memory & Neural: `memory_usage`, `neural_status`, `neural_train`, `neural_patterns`
- GitHub Integration: `github_swarm`, `repo_analyze`, `pr_enhance`, `issue_triage`, `code_review`
- System: `benchmark_run`, `features_detect`, `swarm_monitor`

### Ruv Swarm MCP Tools
- Distributed consensus and coordination
- Performance benchmarking
- Neural processing capabilities
- Memory management
- Autonomous agent systems