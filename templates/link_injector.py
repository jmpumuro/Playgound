"""Utility functions for handling link injection in chat responses."""

from typing import Optional
from .tool_links import TOOL_LINKS

def inject_tool_link(response: str) -> str:
    """
    Injects the appropriate tool link into the chat response.
    
    Args:
        response (str): The chat response containing tool keywords.
        
    Returns:
        str: The response with injected tool links.
    """
    processed_response = response
    
    for tool_key, tool_info in TOOL_LINKS.items():
        # Check for explicit tool references (when user asks for link)
        keyword = f"<{tool_key}>"
        if keyword in processed_response:
            link_text = f"[ {tool_info['name']}]({tool_info['url']})"
            processed_response = processed_response.replace(keyword, link_text)
            continue
        
        # Don't automatically inject links for tool mentions
        # Only inject when explicitly requested using the <TOOL_NAME> format
    
    return processed_response

def get_tool_link(tool_key: str) -> Optional[dict]:
    """
    Get tool information by key.
    
    Args:
        tool_key (str): The tool identifier (e.g., 'RESONANT_BREATHING')
        
    Returns:
        Optional[dict]: Tool information including name, url, and description if found
    """
    # Try exact match first
    if tool_key in TOOL_LINKS:
        return TOOL_LINKS[tool_key]
    
    # Try case-insensitive match with tool names
    tool_key_lower = tool_key.lower()
    for key, info in TOOL_LINKS.items():
        if (info['name'].lower() == tool_key_lower or 
            tool_key_lower in info['name'].lower() or 
            tool_key_lower.replace("_", " ") in info['name'].lower()):
            return info
    
    return None 