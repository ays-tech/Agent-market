"""
Tool Selector Component - UI for selecting agent tools
"""
import streamlit as st
from typing import List


# Available tools with descriptions
AVAILABLE_TOOLS = {
    'WebSearchTool': {
        'name': 'Web Search',
        'icon': '🔍',
        'description': 'Search the web for current information, news, and data'
    },
    'SummarizeTool': {
        'name': 'Summarize',
        'icon': '📝',
        'description': 'Summarize long texts, articles, and documents'
    },
    'FileOpsTool': {
        'name': 'File Operations',
        'icon': '📁',
        'description': 'Read, write, and manage files'
    },
    'MathTool': {
        'name': 'Calculator',
        'icon': '🧮',
        'description': 'Perform mathematical calculations and evaluate expressions'
    },
    'YFinanceTool': {
        'name': 'Stock Market Data',
        'icon': '💰',
        'description': 'Get real-time stock prices, company info, and financial data'
    }
}


def render_tool_selector(selected_tools: List[str] = None) -> List[str]:
    """Render tool selector and return selected tools"""
    
    if selected_tools is None:
        selected_tools = []
    
    st.markdown("**🧰 Select Tools:**")
    st.caption("Choose which tools this agent can use")
    
    selected = []
    
    # Create columns for better layout
    cols = st.columns(2)
    
    for idx, (tool_key, tool_info) in enumerate(AVAILABLE_TOOLS.items()):
        col = cols[idx % 2]
        
        with col:
            is_selected = st.checkbox(
                f"{tool_info['icon']} {tool_info['name']}",
                value=tool_key in selected_tools,
                key=f"tool_{tool_key}",
                help=tool_info['description']
            )
            
            if is_selected:
                selected.append(tool_key)
    
    return selected


def render_tool_badges(tools: List[str]):
    """Render tool badges"""
    if not tools:
        st.caption("No tools selected")
        return
    
    badges = []
    for tool in tools:
        if tool in AVAILABLE_TOOLS:
            tool_info = AVAILABLE_TOOLS[tool]
            badges.append(f"{tool_info['icon']} {tool_info['name']}")
        else:
            badges.append(tool)
    
    st.markdown(' • '.join(badges))


def get_tool_info(tool_key: str) -> dict:
    """Get information about a tool"""
    return AVAILABLE_TOOLS.get(tool_key, {
        'name': tool_key,
        'icon': '🔧',
        'description': 'Unknown tool'
    })

