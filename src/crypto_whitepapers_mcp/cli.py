import os
import json
import urllib.request
from typing import AsyncIterator, Dict
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP, Context
from mcp.types import Prompt, PromptMessage, TextContent, GetPromptResult
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.fastembed import FastEmbedEmbedder
from duckduckgo_search import DDGS

# Configuration
WHITEPAPERS_DIR = "./whitepapers"
VECTOR_DB_URI = "tmp/whitepapers_db"
VECTOR_DB_TABLE = "crypto_whitepapers"

# Initialize MCP server
mcp = FastMCP(
  "Crypto Whitepapers", 
  dependencies=["mcp[cli]", "agno", "lancedb", "pdf2text", "duckduckgo-search", "fastembed"]
)

# Initialize embedder
embedder = FastEmbedEmbedder()

# Initialize vector_db
vector_db = LanceDb(
  uri=VECTOR_DB_URI, 
  table_name=VECTOR_DB_TABLE, 
  embedder=embedder, 
  search_type=SearchType.vector
)

# Initialize knowledge base
knowledge_base = PDFKnowledgeBase(
    path=WHITEPAPERS_DIR,
    vector_db=vector_db
)

# Tools
@mcp.tool()
def search_whitepaper(project_name: str, ctx: Context = None) -> str:
    """Search for a cryptocurrency project's whitepaper PDF using DuckDuckGo.

    Parameters:
        project_name (str): The name of the cryptocurrency project (e.g., 'bitcoin', 'ethereum').

    Returns:
        str: A JSON-formatted list of search results with title, URL, and snippet.
    """
    try:
        with DDGS() as ddgs:
            query = f"{project_name} whitepaper filetype:pdf"
            results = ddgs.text(keywords=query, max_results=5)
        formatted_results = [
            {"title": r["title"], "url": r["href"], "snippet": r["body"]}
            for r in results
        ]
        return json.dumps(formatted_results, indent=2)
    except Exception as e:
        return f"Error searching for {project_name} whitepaper: {str(e)}"

@mcp.tool()
def load_whitepaper(project_name: str, url: str, ctx: Context = None) -> str:
    """Load a whitepaper PDF from a URL into the knowledge base.

    Parameters:
        project_name (str): The name of the cryptocurrency project (e.g., 'bitcoin', 'ethereum').
        url (str): The URL of the whitepaper PDF to download and load.

    Returns:
        str: A message indicating success or failure.
    """
    try:
        # Sanitize project name for filename
        safe_project_name = project_name.lower().replace(" ", "_")
        file_path = os.path.join(WHITEPAPERS_DIR, f"{safe_project_name}.pdf")
        
        # Download PDF
        urllib.request.urlretrieve(url, file_path)
        
        # Load into knowledge base
        knowledge_base.load()
        
        return f"Successfully loaded {project_name} whitepaper from {url}"
    except Exception as e:
        return f"Error loading {project_name} whitepaper: {str(e)}"

@mcp.tool()
def ask_whitepapers(query: str, project_name: str = None, ctx: Context = None) -> str:
    """Search the knowledge base for information related to a query, optionally filtered by project.

    Parameters:
        query (str): The search query to find relevant whitepaper content.
        project_name (str, optional): The name of the cryptocurrency project to filter results (e.g., 'bitcoin'). If None, searches all whitepapers.

    Returns:
        str: A string containing up to 5 matching results from the knowledge base.
    """
    
    # Apply filter if project_name is provided
    filters = [{"source": f"{project_name.lower()}.pdf"}] if project_name else None
    
    results = knowledge_base.search(
        query=query,
        num_documents=5,
        filters=filters
    )
    
    if not results:
        return f"No matches found for query '{query}'" + (f" in {project_name} whitepaper" if project_name else "")
    
    return "\n\n".join([r.content for r in results])

@mcp.tool()
def list_available_projects(ctx: Context) -> str:
    """List all cryptocurrency projects available in the knowledge base.

    Parameters:
        None

    Returns:
        str: A JSON-formatted list of project names derived from PDF filenames.
    """
    try:
        projects = [
            os.path.splitext(f)[0]
            for f in os.listdir(WHITEPAPERS_DIR)
            if f.endswith(".pdf")
        ]
        return json.dumps(projects, indent=2)
    except Exception as e:
        return f"Error listing projects: {str(e)}"

# Prompts
@mcp.prompt()
def analyze_tokenomics(project_name: str) -> GetPromptResult:
    """Analyze the tokenomics described in a cryptocurrency whitepaper"""
    return GetPromptResult(
        description="Analyze tokenomics of a cryptocurrency",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Analyze the tokenomics (token distribution, supply, incentives) described in the {project_name} whitepaper. "
                         f"Use the 'ask_whitepapers' tool to search the knowledge base for relevant information."
                )
            )
        ]
    )

# Main execution
def main() -> None:
    mcp.run()
