# Development Guidelines for RenderGit MCP

## Critical Development Rules

### 🚨 MANDATORY: Concurrent Execution Patterns
1. **ALL operations MUST be concurrent/parallel in a single message**
2. **NEVER save working files, text/mds and tests to the root folder**
3. **ALWAYS organize files in appropriate subdirectories**
4. **USE CLAUDE CODE'S TASK TOOL** for spawning agents concurrently

### File Organization Structure
- `/src` - Source code files
- `/tests` - Test files  
- `/docs` - Documentation and markdown files
- `/config` - Configuration files
- `/scripts` - Utility scripts
- `/examples` - Example code

## SPARC Methodology Workflow
1. **Specification** - Requirements analysis (`sparc run spec-pseudocode`)
2. **Pseudocode** - Algorithm design (`sparc run spec-pseudocode`) 
3. **Architecture** - System design (`sparc run architect`)
4. **Refinement** - TDD implementation (`sparc tdd`)
5. **Completion** - Integration (`sparc run integration`)

## Code Style & Best Practices
- **Modular Design**: Keep files under 500 lines
- **Environment Safety**: Never hardcode secrets or sensitive data
- **Test-First Development**: Write tests before implementation
- **Clean Architecture**: Maintain separation of concerns
- **Documentation**: Keep documentation current and comprehensive

## Agent Coordination Protocol
Every agent spawned via Task tool MUST follow this protocol:

### Before Work:
```bash
npx claude-flow@alpha hooks pre-task --description "[task]"
npx claude-flow@alpha hooks session-restore --session-id "swarm-[id]"
```

### During Work:
```bash
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "swarm/[agent]/[step]"
npx claude-flow@alpha hooks notify --message "[what was done]"
```

### After Work:
```bash
npx claude-flow@alpha hooks post-task --task-id "[task]"
npx claude-flow@alpha hooks session-end --export-metrics true
```

## Performance Benefits
- 84.8% SWE-Bench solve rate
- 32.3% token reduction
- 2.8-4.4x speed improvement  
- 27+ neural models available

## Integration with MCP Servers
- Claude Flow coordinates strategy
- Claude Code's Task tool executes with real agents
- MCP tools only handle coordination setup
- Use hooks for real-time coordination between agents