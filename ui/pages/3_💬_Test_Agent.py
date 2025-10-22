"""
Test Agent Page - Chat with and test AI agents
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.agent_manager import load_agents, save_chat
from ui.components.agent_card import render_agent_summary
from ui.components.chat_box import render_chat_interface, clear_chat_history, export_chat_messages

# Page configuration
st.set_page_config(
    page_title="Test Agent",
    page_icon="💬",
    layout="wide"
)

# Header
st.title("💬 Test Agent")
st.markdown("Chat with AI agents and test their capabilities")
st.divider()

# Load agents
agents = load_agents()

if not agents:
    st.warning("⚠️ No agents found. Create an agent first!")
    if st.button("➕ Create Agent"):
        st.switch_page("ui/pages/2_🧑‍💻_Create_Agent.py")
    st.stop()

# Agent selector
selected_agent = st.session_state.get('selected_agent', None)

# If no agent selected, show dropdown
if not selected_agent:
    agent_names = [agent.get('name', 'Unnamed') for agent in agents]
    selected_name = st.selectbox(
        "Select an agent to test",
        options=agent_names,
        index=0
    )
    
    # Get selected agent
    selected_agent = next(
        (agent for agent in agents if agent.get('name') == selected_name),
        agents[0]
    )
else:
    # Show selected agent with option to change
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"💬 Chatting with: **{selected_agent.get('name')}**")
    with col2:
        if st.button("🔄 Change Agent", use_container_width=True):
            st.session_state['selected_agent'] = None
            st.rerun()

# Display agent info
with st.expander("ℹ️ Agent Information", expanded=False):
    render_agent_summary(selected_agent)

st.divider()

# Chat controls
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    show_reasoning = st.checkbox(
        "🧠 Show Reasoning",
        value=False,
        help="Display the agent's thought process"
    )

with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat_history(selected_agent.get('name'))
        st.success("Chat cleared!")
        st.rerun()

with col3:
    # Get current chat history
    session_key = f"chat_history_{selected_agent.get('name')}"
    if session_key in st.session_state and st.session_state[session_key]:
        if st.button("💾 Save Chat", use_container_width=True):
            try:
                filepath = save_chat(
                    selected_agent.get('name'),
                    st.session_state[session_key]
                )
                st.success(f"✅ Chat saved to: {filepath}")
            except Exception as e:
                st.error(f"❌ Error saving chat: {str(e)}")

st.divider()

# Chat interface
render_chat_interface(selected_agent, show_reasoning=show_reasoning)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 Current Agent")
    st.markdown(f"**Name:** {selected_agent.get('name')}")
    st.markdown(f"**Author:** {selected_agent.get('author')}")
    st.markdown(f"**Model:** `{selected_agent.get('model')}`")
    
    tools = selected_agent.get('tools', [])
    if tools:
        st.markdown(f"**Tools:** {len(tools)}")
        for tool in tools:
            st.markdown(f"- {tool}")
    else:
        st.markdown("**Tools:** None")
    
    st.divider()
    
    # Chat stats
    st.markdown("### 📊 Chat Stats")
    session_key = f"chat_history_{selected_agent.get('name')}"
    if session_key in st.session_state:
        messages = st.session_state[session_key]
        user_msgs = len([m for m in messages if m['role'] == 'user'])
        agent_msgs = len([m for m in messages if m['role'] == 'assistant'])
        
        st.metric("User Messages", user_msgs)
        st.metric("Agent Responses", agent_msgs)
    else:
        st.caption("No messages yet")
    
    st.divider()
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🏠 Marketplace", use_container_width=True):
        st.switch_page("ui/pages/1_🏠_Marketplace.py")
    
    if st.button("📝 Clone Agent", use_container_width=True):
        st.session_state['clone_agent'] = selected_agent
        st.switch_page("ui/pages/2_🧑‍💻_Create_Agent.py")
    
    st.divider()
    
    # Tips
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Ask clear, specific questions
    - Try using the agent's tools
    - Save interesting conversations
    - Clone and modify agents
    """)

