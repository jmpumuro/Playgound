"""
This module contains the summary prompt templates used in the stress reduction chat component.
"""

def get_tool_summary_prompt(tool_name: str) -> str:
    """
    Generate a summary prompt for tool usage.
    
    Args:
        tool_name: The name of the tool that was used
        
    Returns:
        A formatted prompt string for generating a summary
    """
    return (
        f"After using the {tool_name} tool: Briefly summarize why you recommended it, validate their experiences, "
        "and highlight key insights. Ask how they found the exercise and encourage regular brief practice, "
        "noting how consistency builds improvement over time."
    )

def get_conversation_summary_prompt() -> str:
    """
    Generate a prompt for summarizing the entire conversation.
    
    Returns:
        A formatted prompt string for generating a conversation summary
    """
    return (
        "Briefly summarize our discussion, connecting their concerns with suggested tools and insights. "
        "Validate feelings, acknowledge progress, and keep it warm and encouraging. "
        "Ask about their experience and suggest incorporating this practice into their routine, "
        "mentioning specific benefits of consistency for their situation."
    ) 