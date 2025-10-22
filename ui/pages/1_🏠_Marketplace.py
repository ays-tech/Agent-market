"""
Marketplace Page - Browse, search, and explore AI agents
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.agent_manager import load_agents, search_agents
from ui.components.agent_card import render_agent_grid
from core.grok_integration import get_available_models

# Page configuration
st.set_page_config(
    page_title="Agent Marketplace",
    page_icon="🏠",
    layout="wide"
)

# Header
st.title("🏠 Agent Marketplace")
st.markdown("Browse, test, and clone AI agents from the marketplace")
st.divider()

# Search and filter section
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input(
        "🔍 Search agents",
        placeholder="Search by name, author, description, or tools...",
        label_visibility="collapsed"
    )

with col2:
    # Get unique authors
    all_agents = load_agents()
    authors = sorted(list(set(agent.get('author', 'Unknown') for agent in all_agents)))
    author_filter = st.selectbox(
        "Filter by author",
        options=['All Authors'] + authors
    )

with col3:
    # Get available models
    models = list(get_available_models().keys())
    model_filter = st.selectbox(
        "Filter by model",
        options=['All Models'] + models
    )

# Apply filters
filters = {}
if author_filter != 'All Authors':
    filters['author'] = author_filter
if model_filter != 'All Models':
    filters['model'] = model_filter

# Search agents
agents = search_agents(query=search_query, filters=filters if filters else None)

# Sort options
col_sort, col_count = st.columns([1, 3])
with col_sort:
    sort_by = st.selectbox(
        "Sort by",
        options=['Newest First', 'Name (A-Z)', 'Name (Z-A)', 'Author'],
        label_visibility="collapsed"
    )

# Apply sorting
if sort_by == 'Name (A-Z)':
    agents = sorted(agents, key=lambda x: x.get('name', '').lower())
elif sort_by == 'Name (Z-A)':
    agents = sorted(agents, key=lambda x: x.get('name', '').lower(), reverse=True)
elif sort_by == 'Author':
    agents = sorted(agents, key=lambda x: x.get('author', '').lower())
elif sort_by == 'Newest First':
    agents = sorted(agents, key=lambda x: x.get('created_at', ''), reverse=True)

st.divider()

# Callback functions for agent cards
def on_try_agent(agent):
    """Handle try agent button click"""
    st.session_state['selected_agent'] = agent
    st.session_state['selected_agent_id'] = agent.get('id')
    st.switch_page("ui/pages/3_💬_Test_Agent.py")

def on_clone_agent(agent):
    """Handle clone agent button click"""
    st.session_state['clone_agent'] = agent
    st.switch_page("ui/pages/2_🧑‍💻_Create_Agent.py")

# Display agents
render_agent_grid(agents, on_try=on_try_agent, on_clone=on_clone_agent)

# Stats in sidebar
with st.sidebar:
    st.markdown("### 📊 Marketplace Stats")
    st.metric("Total Agents", len(all_agents))
    st.metric("Search Results", len(agents))
    
    # Tool usage stats
    st.markdown("### 🧰 Popular Tools")
    tool_counts = {}
    for agent in all_agents:
        for tool in agent.get('tools', []):
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
    
    for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
        st.markdown(f"- **{tool}**: {count} agent(s)")
    
    st.divider()
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("➕ Create New Agent", use_container_width=True):
        st.switch_page("ui/pages/2_🧑‍💻_Create_Agent.py")
    
    if st.button("🔄 Refresh Marketplace", use_container_width=True):
        st.rerun()

