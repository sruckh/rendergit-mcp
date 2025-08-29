# Project Goals - RendergitMCP

## 🎯 Primary Objective

Transform [Andrej Karpathy's rendergit](https://github.com/karpathy/rendergit) into a production-ready **Model Context Protocol (MCP) server** that seamlessly integrates with Claude Code and other MCP-compatible clients.

## 🚀 Core Functionality

### Repository Processing
- ✅ **Flexible URL Support**: Accept various GitHub URL formats
  - Full URLs: `https://github.com/owner/repo`
  - Simplified: `owner/repo` (no protocol needed)
  - Domain included: `github.com/owner/repo`

- ✅ **Dual Output Modes**:
  - **HTML Response**: Direct HTML content for immediate use
  - **File Storage**: Save rendered HTML to organized file structure

- ✅ **LLM-Optimized Output**: Generate CXML text format perfect for AI analysis
  - Human-readable view with syntax highlighting
  - Raw CXML format for copying to Claude/ChatGPT
  - Conversation context integration

## 🛠 Technical Requirements

### MCP Server Implementation
- ✅ **FastMCP Framework**: Use official MCP Python SDK
- ✅ **SSE Transport**: Server-Sent Events for Claude Code compatibility  
- ✅ **Health Monitoring**: Built-in health checks and server info endpoints
- ✅ **Error Handling**: Robust error handling with meaningful messages

### Integration Capabilities
- ✅ **Context7 MCP**: Leverage for current documentation when needed
- ✅ **Fetch Integration**: Retrieve data from external websites
- ✅ **Serena Memory**: Access project memories for additional context
- ✅ **Claude Flow Agents**: Launch specialized agents for complex tasks

### File Organization
- ✅ **Structured Storage**: Organize output in `/projects/{type}/{subpath}/` structure
- ✅ **Auto-naming**: Generate meaningful filenames from repository paths
- ✅ **Path Flexibility**: Support custom output paths when specified

## 📋 Success Criteria

### Functional Requirements
1. **URL Processing**: Handle all GitHub URL formats correctly
2. **Content Generation**: Produce both Human and LLM views
3. **File Management**: Save files to organized directory structure
4. **Error Recovery**: Gracefully handle network issues, missing repos, large files

### Performance Requirements
1. **Response Time**: Process typical repositories in under 30 seconds
2. **Memory Efficiency**: Handle repositories up to 100MB without issues
3. **Concurrent Requests**: Support multiple simultaneous rendering requests

### Integration Requirements
1. **Claude Code**: Seamless integration with Claude Code MCP client
2. **Transport Compatibility**: Support both SSE and stdio transports
3. **API Consistency**: Maintain consistent MCP tool interface

## 🔄 Development Workflow

### Repository Management
- **GitHub Repository**: `sruckh/rendergit-mcp`
- **Version Control**: Always use SSH for GitHub operations
- **Branching**: Feature branches for major changes
- **Documentation**: Keep documentation synchronized with code

### Quality Assurance
- **Testing**: Comprehensive test coverage for all MCP tools
- **Code Review**: All changes reviewed before merge
- **Documentation**: Update docs with feature changes
- **Performance**: Monitor and optimize rendering performance

### Deployment
- **Docker Support**: Containerized deployment ready
- **Configuration**: Environment-based configuration
- **Monitoring**: Health endpoints for production monitoring
- **Logging**: Comprehensive logging for debugging

## 🎯 Future Enhancements

### Advanced Features
- **Caching**: Cache rendered repositories for faster repeat access
- **Incremental Updates**: Support for updating cached repositories
- **Private Repositories**: Support for private repos with authentication
- **Multiple Formats**: Additional output formats (PDF, Markdown, etc.)

### Integration Expansion
- **GitLab Support**: Extend to GitLab repositories
- **Bitbucket Support**: Support for Bitbucket repositories
- **Local Repositories**: Render local Git repositories
- **Archive Support**: Process repository archives (ZIP, tar.gz)

### Performance Optimization
- **Streaming**: Stream large repository processing
- **Parallel Processing**: Parallel file processing for faster rendering
- **Compression**: Compress output for faster network transfer
- **CDN Integration**: CDN support for cached content delivery

## 📊 Success Metrics

### Usage Metrics
- **Adoption Rate**: Number of Claude Code users integrating the server
- **Repository Coverage**: Types and sizes of repositories processed
- **Performance Benchmarks**: Processing time vs. repository size

### Quality Metrics
- **Error Rate**: Percentage of failed repository processing attempts
- **User Satisfaction**: Feedback on output quality and usefulness
- **Integration Success**: Successful MCP client integrations

---

**Status**: ✅ **Core objectives achieved** - MCP server operational with dual-view rendering, flexible URL support, and Claude Code integration ready.
