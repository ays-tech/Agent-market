# 🚀 Quick Start Guide

Get up and running with Agent Market in 5 minutes!

**Powered by Agno + GroqCloud for blazing fast AI responses! ⚡**

## Step 1: Installation

```bash
# Navigate to the project directory
cd agent-market

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Step 3: Explore Prebuilt Agents

1. Click on **"🏠 Marketplace"** in the sidebar
2. Browse the 6 prebuilt agents:
   - Research Analyst (Web Search)
   - Content Wizard (File Operations)
   - Code Assistant (Calculator + Files)
   - Stock Market Analyst (Finance Data) ⭐ NEW!
   - Crypto Scout (Web Search)
   - Email Helper (Fast & Lightweight)
3. Click **"Try Agent"** to test any agent

## Step 4: Create Your First Agent

### Using No-Code Mode (Easiest)

1. Click **"🧑‍💻 Create Agent"** in the sidebar
2. Make sure **"🧩 No-Code Mode"** is selected
3. Fill in the form:
   ```
   Agent Name: My Assistant
   Your Name: [Your Name]
   Model: llama-3.3-70b-versatile
   Description: A helpful assistant for everyday tasks
   Tools: [Select any tools you want]
   System Prompt: You are a friendly, helpful assistant...
   ```
4. Click **"💾 Save Agent"**
5. Your agent is now in the marketplace!

### Using Developer Mode (Advanced)

1. Click **"🧑‍💻 Create Agent"**
2. Switch to **"💻 Developer Mode"**
3. Edit the JSON:
   ```json
   {
     "name": "My Custom Agent",
     "author": "Your Name",
     "description": "What your agent does",
     "model": "llama-3.3-70b-versatile",
     "tools": ["WebSearchTool", "SummarizeTool"],
     "prompt": "You are a specialized AI assistant that..."
   }
   ```
4. Click **"💾 Save Agent"**

## Step 5: Test Your Agent

1. Click **"💬 Test Agent"** in the sidebar
2. Select your agent from the dropdown
3. Start chatting!
4. Try asking it to use its tools

## Optional: Set Up API Key for Real AI (FREE!)

For actual AI responses (not demo mode):

1. Get a **FREE** API key from [console.groq.com](https://console.groq.com)
2. In the sidebar, expand **"🔑 API Key Settings"**
3. Enter your API key
4. Click **"Save API Key"**

**Or set as environment variable:**
```bash
export GROQ_API_KEY="your-api-key-here"
```

**Why GroqCloud?**
- 🆓 **FREE** tier with generous limits
- ⚡ **Ultra-fast** (up to 750+ tokens/second!)
- 🤖 **Multiple models** (Llama 3.3, Mixtral, Gemma 2)
- 🎯 **Easy to use** - just one API key!

## 🎯 What to Try Next

### Clone and Modify an Agent
1. Go to Marketplace
2. Click **"Clone/Edit"** on any agent
3. Modify it to your needs
4. Save as a new agent

### Save Conversations
1. Chat with an agent
2. Click **"💾 Save Chat"** button
3. Find saved chats in `data/chats/`

### Import Custom Agents
```bash
python examples/import_agent.py examples/custom_agent_example.json
```

## 💡 Pro Tips

- **Start with prebuilt agents** to understand how they work
- **Clone before creating** – it's easier to modify than start from scratch
- **Be specific in prompts** – clear instructions = better agents
- **Choose tools wisely** – match tools to your agent's purpose
- **Test thoroughly** – chat with your agent before considering it done

## 🐛 Troubleshooting

### "No agents found"
- The app creates 6 example agents automatically on first run
- Check if `data/agents.json` exists
- Try restarting the app

### "API Error"
- Running in demo mode (no API key)
- To get real responses, add your FREE GroqCloud API key
- Check if key is valid at [console.groq.com](https://console.groq.com)

### "Import Error"
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### "Port already in use"
- Another Streamlit app is running
- Stop it or use a different port: `streamlit run app.py --server.port 8502`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out [examples/](examples/) for more agent configurations
- Experiment with custom tools
- Share your best agents with the community!

## 🆘 Need Help?

- Check the **FAQ** in the main app (expand at bottom of home page)
- Review the [README.md](README.md)
- Open an issue on GitHub

---

**Happy Building! 🎉**

You're now ready to create, test, and share amazing AI agents!

