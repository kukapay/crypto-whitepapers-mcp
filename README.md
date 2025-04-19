# Crypto Whitepapers MCP Server

An MCP server serving as a structured knowledge base of crypto whitepapers for AI agents to access, analyze, and learn from.

[![Discord](https://img.shields.io/discord/1353556181251133481?cacheSeconds=3600)](https://discord.gg/aRnuu2eJ)
![GitHub License](https://img.shields.io/github/license/kukapay/crypto-whitepapers-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)


## Features

- **Search Whitepapers**: Use DuckDuckGo to find whitepaper PDFs for cryptocurrency projects.
- **Load Whitepapers**: Download and index whitepaper PDFs into the knowledge base.
- **Query Knowledge Base**: Query whitepaper content with optional project filtering.
- **List Projects**: View all projects available in the knowledge base.
- **Claude Desktop Integration**: Access tools and prompts via MCP in Claude Desktop.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for dependency management and running
- Internet access.
- [Claude Desktop](https://claude.ai/download) for MCP integration (optional)

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/crypto-whitepapers-mcp.git
   cd crypto-whitepapers-mcp
   ```

2. **Install Dependencies with uv**:
   ```bash
   uv sync
   ```

5. **Integrate with Claude Desktop** (Optional):
   - Edit the Claude Desktop configuration file:
     - **MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
     - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - Add the following configuration:
     ```json
     {
         "mcpServers": {
             "crypto-whitepapers": {
                 "command": "uv",
                 "args": [
                     "--directory",
                     "/absolute/path/to/crypto-whitepapers-mcp"   
                     "run",
                     "crypto-whitepapers-mcp"
                 ]
             }
         }
     }
     ```
     Replace `/absolute/path/to/crypto-whitepapers-mcp` with the absolute path to the repository.
   - Restart Claude Desktop and verify the server is loaded (look for the hammer icon in the input box).

## Usage

### Tools
The following tools are available via the MCP server:

- **`list_available_projects()`**: Lists all projects in the knowledge base (derived from PDF filenames).
  - Example: `list_available_projects()`
  - Returns: JSON list of project names.
  
- **`search_whitepaper(project_name: str)`**: Searches for a project's whitepaper PDF using DuckDuckGo.
  - Example: `search_whitepaper("bitcoin")`
  - Returns: JSON list of up to 5 results with title, URL, and snippet.

- **`load_whitepaper(project_name: str, url: str)`**: Downloads a whitepaper PDF from a URL and loads it into the knowledge base.
  - Example: `load_whitepaper("bitcoin", "https://bitcoin.org/bitcoin.pdf")`
  - Returns: Success or error message.

- **`ask_whitepapers(query: str, project_name: str = None)`**: Searches the knowledge base for a query, optionally filtered by project.
  - Example: `ask_whitepapers("blockchain technology", "bitcoin")`
  - Returns: Up to 5 matching text snippets.



### Prompts
- **`analyze_tokenomics(project_name: str)`**: Analyzes tokenomics (distribution, supply, incentives) in a project's whitepaper using the `ask_whitepapers` tool.
  - Example: In Claude Desktop, run "Analyze the tokenomics of Ethereum."

### Examples
1. List available projects:
   ```
   List all available projects.
   ```
2. Search for a whitepaper:
   ```
   Search for the Bitcoin whitepaper PDF.
   ```
3. Load a whitepaper:
   ```
   Load the Bitcoin whitepaper from https://bitcoin.org/bitcoin.pdf.
   ```
4. Query the knowledge base:
   ```
   Ask the knowledge base about blockchain technology in the Bitcoin whitepaper.
   ```
   
## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

