"""
Create Agent Page - Build new agents with no-code or dev mode
"""
import streamlit as st
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import create_agent, update_agent
from core.groq_integration import get_model_names
from ui.components.tool_selector import render_tool_selector

# Page configuration
st.set_page_config(
    page_title="Create Agent",
    page_icon="🧑‍💻",
    layout="wide"
)

# Header
st.title("🧑‍💻 Create Your AI Agent")
st.markdown("Build a custom AI agent with no-code builder or developer mode")
st.divider()

# Check if cloning an existing agent
clone_agent = st.session_state.get('clone_agent', None)
if clone_agent:
    st.info(f"📝 Cloning agent: **{clone_agent.get('name')}**")
    # Clear the clone data after displaying
    if st.button("Clear Clone Data"):
        st.session_state['clone_agent'] = None
        st.rerun()

# Mode selector
col1, col2 = st.columns(2)
with col1:
    mode = st.radio(
        "Select Mode",
        options=['🧩 No-Code Mode', '💻 Developer Mode'],
        horizontal=True
    )

st.divider()

# No-Code Mode
if mode == '🧩 No-Code Mode':
    st.markdown("### 🧩 No-Code Agent Builder")
    st.caption("Create an agent using a simple form - no coding required!")
    
    with st.form("agent_builder_form"):
        # Agent details
        col1, col2 = st.columns(2)
        
        with col1:
            agent_name = st.text_input(
                "Agent Name *",
                value=clone_agent.get('name', '') if clone_agent else '',
                placeholder="e.g., Research Analyst",
                help="Choose a descriptive name for your agent"
            )
            
            author = st.text_input(
                "Your Name *",
                value=clone_agent.get('author', '') if clone_agent else '',
                placeholder="e.g., John Doe",
                help="Your name or username"
            )
        
        with col2:
            models = get_model_names()
            default_model = clone_agent.get('model', models[0]) if clone_agent else models[0]
            model_index = models.index(default_model) if default_model in models else 0
            
            selected_model = st.selectbox(
                "Model *",
                options=models,
                index=model_index,
                help="Choose the AI model for your agent"
            )
        
        # Description
        description = st.text_area(
            "Description *",
            value=clone_agent.get('description', '') if clone_agent else '',
            placeholder="Describe what your agent does and what it's good at...",
            height=100,
            help="A clear description helps users understand your agent's purpose"
        )
        
        # Tools
        selected_tools = render_tool_selector(
            clone_agent.get('tools', []) if clone_agent else []
        )
        
        # System prompt
        st.markdown("**System Prompt / Personality ***")
        system_prompt = st.text_area(
            "System Prompt",
            value=clone_agent.get('prompt', '') if clone_agent else '',
            placeholder="You are a professional assistant that helps with...",
            height=150,
            help="Define your agent's personality, behavior, and expertise",
            label_visibility="collapsed"
        )
        
        # Submit button
        st.divider()
        submitted = st.form_submit_button(
            "💾 Save Agent",
            use_container_width=True,
            type="primary"
        )
    
    # Handle form submission outside the form
    if submitted:
        # Validation
        if not agent_name or not author or not description or not system_prompt:
            st.error("❌ Please fill in all required fields (marked with *)")
        else:
            # Create agent data
            agent_data = {
                'name': agent_name,
                'author': author,
                'description': description,
                'model': selected_model,
                'tools': selected_tools,
                'prompt': system_prompt
            }
            
            try:
                # Save agent
                created_agent = create_agent(agent_data)
                st.success(f"✅ Agent '{agent_name}' successfully created!")
                st.balloons()
                
                # Show agent info
                with st.expander("View Agent Details"):
                    st.json(created_agent)
                
                # Clear clone data
                if 'clone_agent' in st.session_state:
                    st.session_state['clone_agent'] = None
                
                # Store created agent for navigation
                st.session_state['last_created_agent'] = created_agent
                
                # Navigation buttons (outside form)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💬 Test This Agent", key="nocode_test", use_container_width=True):
                        st.session_state['selected_agent'] = created_agent
                        st.switch_page("pages/3_💬_Test_Agent.py")
                with col2:
                    if st.button("🏠 Go to Marketplace", key="nocode_market", use_container_width=True):
                        st.switch_page("pages/1_🏠_Marketplace.py")
            
            except Exception as e:
                st.error(f"❌ Error creating agent: {str(e)}")

# Developer Mode
else:
    st.markdown("### 💻 Developer Mode")
    st.caption("Create an agent using JSON configuration - for advanced users")
    
    # Template
    template = {
        "name": "Research Analyst",
        "author": "YourName",
        "description": "Analyzes trends and provides insights",
        "model": "grok-beta",
        "tools": ["WebSearchTool", "SummarizeTool"],
        "prompt": "You are a professional research analyst with expertise in gathering and analyzing information..."
    }
    
    # If cloning, use clone data as template
    if clone_agent:
        template = {
            'name': clone_agent.get('name', ''),
            'author': clone_agent.get('author', ''),
            'description': clone_agent.get('description', ''),
            'model': clone_agent.get('model', ''),
            'tools': clone_agent.get('tools', []),
            'prompt': clone_agent.get('prompt', '')
        }
    
    # JSON editor
    agent_json = st.text_area(
        "Agent Configuration (JSON)",
        value=json.dumps(template, indent=2),
        height=400,
        help="Edit the JSON to configure your agent"
    )
    
    # Validate and save
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("💾 Save Agent", use_container_width=True, type="primary"):
            try:
                # Parse JSON
                agent_data = json.loads(agent_json)
                
                # Validate required fields
                required_fields = ['name', 'author', 'description', 'model', 'prompt']
                missing_fields = [f for f in required_fields if f not in agent_data]
                
                if missing_fields:
                    st.error(f"❌ Missing required fields: {', '.join(missing_fields)}")
                else:
                    # Save agent
                    created_agent = create_agent(agent_data)
                    st.success(f"✅ Agent '{agent_data['name']}' successfully created!")
                    st.balloons()
                    
                    # Clear clone data
                    if 'clone_agent' in st.session_state:
                        st.session_state['clone_agent'] = None
                    
                    # Store for navigation
                    st.session_state['last_created_agent'] = created_agent
                    
                    # Navigation buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💬 Test Agent", key="dev_test", use_container_width=True):
                            st.session_state['selected_agent'] = created_agent
                            st.switch_page("pages/3_💬_Test_Agent.py")
                    with col2:
                        if st.button("🏠 Marketplace", key="dev_market", use_container_width=True):
                            st.switch_page("pages/1_🏠_Marketplace.py")
            
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Help section
    with st.expander("📚 JSON Schema Reference"):
        st.markdown("""
        ### Required Fields
        - `name` (string): Agent name
        - `author` (string): Your name
        - `description` (string): What the agent does
        - `model` (string): AI model to use
        - `prompt` (string): System prompt defining behavior
        
        ### Optional Fields
        - `tools` (array): List of tools (WebSearchTool, SummarizeTool, FileOpsTool, MathTool)
        
        ### Available Models (GroqCloud)
        - `llama-3.3-70b-versatile` (Recommended - Most capable)
        - `llama-3.1-70b-versatile`
        - `llama-3.1-8b-instant` (Fast)
        - `mixtral-8x7b-32768`
        - `gemma2-9b-it`
        
        ### Available Tools
        - `WebSearchTool`: Search the web (DuckDuckGo)
        - `SummarizeTool`: Summarize text
        - `FileOpsTool`: File operations
        - `MathTool`: Math calculations
        - `YFinanceTool`: Stock market data (Bonus!)
        """)

# Sidebar info
with st.sidebar:
    st.markdown("### ⚡ Quick Actions")
    if st.button("🏡 Home", use_container_width=True, key="sidebar_home"):
        st.switch_page("app.py")
    
    if st.button("🏠 Marketplace", use_container_width=True, key="sidebar_market"):
        st.switch_page("pages/1_🏠_Marketplace.py")
    
    st.divider()
    
    st.markdown("### ℹ️ About Agent Builder")
    st.markdown("""
    **No-Code Mode** 🧩
    - Simple form interface
    - Perfect for beginners
    - Visual tool selection
    
    **Developer Mode** 💻
    - JSON configuration
    - Full control
    - For advanced users
    """)
    
    st.divider()
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Give your agent a clear, descriptive name
    - Write a detailed system prompt
    - Choose tools that match your agent's purpose
    - Test your agent after creation
    """)

