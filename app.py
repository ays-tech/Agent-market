"""
Agent Market - Create, Modify & Explore AI Agents
A local, open-source agent marketplace powered by LangChain and Grok Cloud
"""
import streamlit as st
import os
from core.agent_manager import ensure_data_directory, load_agents
from core.groq_integration import get_config, set_api_key

# Page configuration
st.set_page_config(
    page_title="Agent Market",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure data directory exists
ensure_data_directory()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        width: 100%;
    }
    
    .agent-card {
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/bot.png", width=150)
    st.markdown("# 🤖 Agent Market")
    st.markdown("### Your Local AI Agent Hub")
    st.divider()
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    st.page_link("app.py", label="🏡 Home")
    st.page_link("pages/1_🏠_Marketplace.py", label="🏠 Marketplace")
    st.page_link("pages/2_🧑‍💻_Create_Agent.py", label="🧑‍💻 Create Agent")
    st.page_link("pages/3_💬_Test_Agent.py", label="💬 Test Agent")
    
    st.divider()
    
    # Configuration
    st.markdown("### ⚙️ Configuration")
    
    # API Key input
    with st.expander("🔑 API Key Settings"):
        config = get_config()
        
        st.markdown(config.get_api_key_status())
        
        api_key_input = st.text_input(
            "GroqCloud API Key",
            type="password",
            placeholder="Enter your GroqCloud API key",
            help="Get your FREE API key from https://console.groq.com"
        )
        
        if st.button("Save API Key"):
            if api_key_input:
                set_api_key(api_key_input)
                st.success("✅ API Key saved!")
                st.rerun()
            else:
                st.error("Please enter an API key")
        
        st.caption("💡 You can also set the GROQ_API_KEY environment variable")
        st.caption("🆓 GroqCloud offers FREE API access with generous limits!")
    
    # User profile (optional)
    with st.expander("👤 User Profile"):
        username = st.text_input(
            "Your Name",
            value=st.session_state.get('username', ''),
            placeholder="Enter your name"
        )
        if username:
            st.session_state['username'] = username
    
    st.divider()
    
    # Quick stats
    st.markdown("### 📊 Quick Stats")
    agents = load_agents()
    st.metric("Total Agents", len(agents))
    
    # Count by author
    authors = set(agent.get('author') for agent in agents)
    st.metric("Authors", len(authors))
    
    # Count tools
    all_tools = set()
    for agent in agents:
        all_tools.update(agent.get('tools', []))
    st.metric("Unique Tools", len(all_tools))
    
    st.divider()
    
    # About
    st.markdown("### ℹ️ About")
    st.caption("Agent Market v2.0")
    st.caption("Build, test, and share AI agents locally")
    st.caption("Powered by Agno & GroqCloud ⚡")

# Main content
st.markdown("""
<div class="main-header">
    <h1>🤖 Welcome to Agent Market</h1>
    <p>Your Local AI Agent Marketplace</p>
</div>
""", unsafe_allow_html=True)

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏠 Marketplace")
    st.markdown("""
    Browse and explore AI agents created by the community.
    - Search & filter agents
    - View agent details
    - Clone and modify
    - Test before using
    """)
    if st.button("🏠 Go to Marketplace", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🏠_Marketplace.py")

with col2:
    st.markdown("### 🧑‍💻 Create Agents")
    st.markdown("""
    Build your own AI agents with ease for free from your local machine. 
    - No-code builder
    - Developer mode
    - Choose tools & models
    - Custom prompts
    """)
    if st.button("🧑‍💻 Create Agent", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🧑‍💻_Create_Agent.py")

with col3:
    st.markdown("### 💬 Test Agents")
    st.markdown("""
    Chat with agents and test their capabilities.
    - Interactive chat
    - Real-time responses
    - Save conversations
    - View reasoning
    """)
    if st.button("💬 Test Agent", use_container_width=True, type="primary"):
        st.switch_page("pages/3_💬_Test_Agent.py")

st.divider()

# Recent agents
st.markdown("## 🌟 Featured Agents")

if agents:
    # Show top 3 agents
    featured = agents[:3]
    
    cols = st.columns(3)
    for idx, agent in enumerate(featured):
        with cols[idx]:
            with st.container():
                st.markdown(f"### {agent.get('name')}")
                st.caption(f"by {agent.get('author')}")
                st.markdown(f"*{agent.get('description', '')[:100]}...*")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("Try", key=f"try_{idx}", use_container_width=True):
                        st.session_state['selected_agent'] = agent
                        st.switch_page("pages/3_💬_Test_Agent.py")
                with col_b:
                    if st.button("Clone", key=f"clone_{idx}", use_container_width=True):
                        st.session_state['clone_agent'] = agent
                        st.switch_page("pages/2_🧑‍💻_Create_Agent.py")
else:
    st.info("No agents yet. Create your first agent to get started!")

st.divider()

# Getting started
st.markdown("## 🚀 Getting Started")

with st.expander("📖 Quick Start Guide"):
    st.markdown("""
    ### Welcome to Agent Market! Here's how to get started:
    
    #### 1️⃣ Set Up Your API Key (FREE!)
    - Get a FREE API key from [console.groq.com](https://console.groq.com)
    - Enter it in the sidebar under "API Key Settings"
    - Or set the `GROQ_API_KEY` environment variable
    - GroqCloud offers generous free tier with fast inference!
    
    #### 2️⃣ Explore the Marketplace
    - Browse existing agents
    - Search by name, author, or tools
    - Click "Try Agent" to test any agent
    - Click "Clone/Edit" to modify an agent
    
    #### 3️⃣ Create Your First Agent
    - Go to "Create Agent" page
    - Choose **No-Code Mode** for simplicity
    - Or use **Developer Mode** for JSON configuration
    - Fill in the details:
        - Name your agent
        - Add a description
        - Choose tools (web search, summarize, etc.)
        - Write a system prompt
    - Save and test!
    
    #### 4️⃣ Test and Iterate
    - Chat with your agent in the Test page
    - Save interesting conversations
    - Clone and modify agents to improve them
    - Share your creations!
    
    ### 💡 Tips
    - Start by trying the prebuilt agents
    - Clone an existing agent to learn
    - Write clear, detailed system prompts
    - Choose appropriate tools for your use case
    - Test thoroughly before publishing
    
    ### 🛠️ Available Tools
    - **Web Search**: Find current information online
    - **Summarize**: Condense long texts
    - **File Operations**: Read and write files
    - **Calculator**: Perform math calculations
    
    ### 📚 Learn More
    - Check out the README for detailed documentation
    - Visit the GitHub repository for updates
    - Join the community to share your agents
    """)

with st.expander("❓ FAQ"):
    st.markdown("""
    **Q: Do I need an API key to use Agent Market?**
    A: For demo mode and exploring the marketplace, no. To get real AI responses from agents, you'll need a FREE GroqCloud API key.
    
    **Q: Where is my data stored?**
    A: All data is stored locally in the `data/` folder. Your agents are in `agents.json` and chats are saved in `data/chats/`.
    
    **Q: Can I share my agents?**
    A: Currently, agents are stored locally. You can share the JSON configuration with others manually.
    
    **Q: What models are available?**
    A: Agent Market supports multiple models from GroqCloud: Llama 3.3 70B, Llama 3.1, Mixtral, and Gemma 2 - all FREE!
    
    **Q: Why GroqCloud?**
    A: GroqCloud offers extremely fast inference (up to 750 tokens/second!), generous free tier, and multiple state-of-the-art models.
    
    **Q: How do I delete an agent?**
    A: Currently, you can manually edit the `data/agents.json` file to remove agents. A delete feature will be added in future versions.
    
    **Q: Can I add custom tools?**
    A: Yes! You can create custom tools by adding Python files to the `core/tools/` directory and registering them in the tool registry.
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #666;">
    <p>🤖 <strong>Agent Market</strong> - The HuggingFace of AI Agents, but Local</p>
    <p>Built with ❤️ using Streamlit, Agno & GroqCloud ⚡</p>
    <p>Powered by <strong>ultra-fast</strong> inference on Groq's LPU™ architecture</p>
</div>
""", unsafe_allow_html=True)

