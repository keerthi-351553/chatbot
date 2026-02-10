# search_tool.py
import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return a list of callable tools for ToolNode.
    """
    if not os.environ.get("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not set")

    tools = [
        TavilySearchResults(max_results=2)
    ]
    return tools

def create_tool_node(tools):
    """
    Create a ToolNode using the wrapper functions.
    """
    return ToolNode(tools)
