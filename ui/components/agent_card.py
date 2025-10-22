"""
Agent Card Component - Display agent information in a card format
"""
import streamlit as st
from typing import Dict, Callable


def render_agent_card(agent: Dict, on_try: Callable = None, on_clone: Callable = None, on_delete: Callable = None):
    """Render an agent card with actions"""
    
    with st.container():
        # Use columns for better layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### 🤖 {agent.get('name', 'Unnamed Agent')}")
            st.markdown(f"**👤 Author:** {agent.get('author', 'Unknown')}")
            st.markdown(f"*{agent.get('description', 'No description provided.')}*")
        
        with col2:
            st.markdown(f"**Model:**")
            st.code(agent.get('model', 'N/A'), language=None)
        
        # Tools section
        tools = agent.get('tools', [])
        if tools:
            st.markdown("**🧰 Tools:**")
            tool_badges = ' '.join([f'`{tool}`' for tool in tools])
            st.markdown(tool_badges)
        
        # Metadata
        created_at = agent.get('created_at', 'Unknown')
        st.caption(f"Created: {created_at} | ID: {agent.get('id', 'N/A')}")
        
        # Action buttons
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 1])
        
        with col_btn1:
            if st.button("💬 Try", key=f"try_{agent.get('id')}", use_container_width=True):
                if on_try:
                    on_try(agent)
        
        with col_btn2:
            if st.button("📝 Clone", key=f"clone_{agent.get('id')}", use_container_width=True):
                if on_clone:
                    on_clone(agent)
        
        with col_btn3:
            if st.button("🗑️ Delete", key=f"delete_{agent.get('id')}", use_container_width=True, type="secondary"):
                if on_delete:
                    on_delete(agent)
        
        # Divider
        st.divider()


def render_agent_grid(agents: list, on_try: Callable = None, on_clone: Callable = None, on_delete: Callable = None):
    """Render multiple agents in a grid layout"""
    
    if not agents:
        st.info("No agents found. Create your first agent to get started!")
        return
    
    # Display count
    st.caption(f"Showing {len(agents)} agent(s)")
    
    # Render each agent
    for agent in agents:
        render_agent_card(agent, on_try, on_clone, on_delete)


def render_agent_summary(agent: Dict):
    """Render a compact agent summary"""
    
    with st.container():
        st.markdown(f"### 🤖 {agent.get('name', 'Agent')}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Author:** {agent.get('author', 'Unknown')}")
            st.markdown(f"**Model:** `{agent.get('model', 'N/A')}`")
        
        with col2:
            tools = agent.get('tools', [])
            if tools:
                st.markdown(f"**Tools:** {', '.join(tools)}")
            else:
                st.markdown("**Tools:** None")
        
        # Description in expander
        with st.expander("ℹ️ Description & Prompt"):
            st.markdown(f"**Description:**")
            st.write(agent.get('description', 'No description'))
            st.markdown(f"**System Prompt:**")
            st.code(agent.get('prompt', 'No prompt defined'), language=None)

