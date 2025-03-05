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
        "Please provide a warm, deeply empathetic summary of our discussion and why you recommended this tool. "
        "Make it feel personal and supportive, as if you're checking in with a caring friend. "
        "Acknowledge any challenges they shared and validate their experiences with genuine understanding. "
        "Highlight the key insights from the conversation in a natural, conversational way. "
        "Express appreciation for their willingness to engage with the tool and their commitment to their well-being. "
        "After the summary, ask how they found the exercise and if it was helpful, then gently encourage them to "
        "continue practicing regularly, emphasizing that consistent practice can lead to meaningful improvements "
        "over time. Suggest a realistic timeframe for practice that feels manageable (e.g., 'even 5 minutes daily')."
    )

def get_conversation_summary_prompt() -> str:
    """
    Generate a prompt for summarizing the entire conversation.
    
    Returns:
        A formatted prompt string for generating a conversation summary
    """
    return (
        "Please provide a warm, deeply empathetic summary of our discussion. "
        "Instead of using bullet points, compassionately weave together the main concerns we discussed, "
        "how the tool was suggested as a potential help, and what insights might have emerged. "
        "Validate their feelings and experiences with genuine understanding and care. "
        "Acknowledge any progress made, no matter how small, and celebrate their courage in addressing their concerns. "
        "Make it feel personal and supportive, as if you're reflecting with a trusted friend who truly cares. "
        "Keep it concise but warm, empathetic, and encouraging. "
        "After providing the summary, ask how they found the exercise and if it was helpful, then "
        "gently encourage them to make this practice a regular part of their self-care routine, explaining "
        "that consistent practice, even for just a few minutes daily, can build resilience and promote well-being over time. "
        "Offer a specific, encouraging note about how continuing this practice might benefit them based on what you've learned about their situation."
    ) 