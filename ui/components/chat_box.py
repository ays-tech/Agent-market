"""
Chat Box Component - Chat interface for testing agents
"""
import streamlit as st
from typing import List, Dict, Optional
from core.runner import AgentRunner


def initialize_chat_session(agent_name: str):
    """Initialize chat session in streamlit session state"""
    session_key = f"chat_history_{agent_name}"
    if session_key not in st.session_state:
        st.session_state[session_key] = []
    return session_key


def render_chat_interface(agent: Dict, show_reasoning: bool = False):
    """Render chat interface for an agent"""
    
    agent_name = agent.get('name', 'Agent')
    session_key = initialize_chat_session(agent_name)
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state[session_key]:
            role = message['role']
            content = message['content']
            
            if role == 'user':
                with st.chat_message("user", avatar="👤"):
                    st.markdown(content)
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(content)
                    
                    # Show reasoning if available and enabled
                    if show_reasoning and 'reasoning' in message:
                        with st.expander("🧠 View Reasoning"):
                            st.code(message['reasoning'], language='text')
    
    # Chat input
    user_input = st.chat_input(f"Message {agent_name}...")
    
    if user_input:
        # Add user message to history
        st.session_state[session_key].append({
            'role': 'user',
            'content': user_input
        })
        
        # Display user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner(f"{agent_name} is thinking..."):
                try:
                    # Create agent runner
                    runner = AgentRunner(agent)
                    
                    # Get response
                    response = runner.run(
                        user_input,
                        chat_history=st.session_state[session_key]
                    )
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add to history
                    st.session_state[session_key].append({
                        'role': 'assistant',
                        'content': response
                    })
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state[session_key].append({
                        'role': 'assistant',
                        'content': error_msg
                    })
        
        # Rerun to update chat
        st.rerun()
    
    return st.session_state[session_key]


def clear_chat_history(agent_name: str):
    """Clear chat history for an agent"""
    session_key = f"chat_history_{agent_name}"
    if session_key in st.session_state:
        st.session_state[session_key] = []


def export_chat_messages(messages: List[Dict]) -> str:
    """Export chat messages to text format"""
    output = []
    for msg in messages:
        role = msg['role'].upper()
        content = msg['content']
        output.append(f"{role}:\n{content}\n")
    
    return '\n'.join(output)

