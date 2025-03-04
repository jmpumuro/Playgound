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
        f"The user just completed using the {tool_name} tool. "
        "Please provide a warm, conversational summary of our discussion and why you recommended this tool. "
        "Make it feel personal and empathetic, as if you're checking in with a friend. "
        "Highlight the key insights from the conversation in a natural way. "
        "After the summary, ask the user how they found the exercise and if it was helpful for them."
    )

def get_conversation_summary_prompt() -> str:
    """
    Generate a prompt for summarizing the entire conversation.
    
    Returns:
        A formatted prompt string for generating a conversation summary
    """
    return (
        "Please provide a warm, conversational summary of our discussion. "
        "Instead of using bullet points, weave together the main concerns we discussed, "
        "how the tool was suggested as a potential help, and what insights might have emerged. "
        "Make it feel personal and supportive, as if you're reflecting with a friend. "
        "Keep it concise but warm and empathetic. "
        "After providing the summary, ask the user how they found the exercise and if it was helpful for them."
    ) 