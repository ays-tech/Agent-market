"""
Agent Runner - Executes agent logic via Agno framework
"""
from typing import Dict, List, Optional, Any
from agno.agent import Agent, RunOutput
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from core.groq_integration import get_config, validate_model
import os


# Tool registry mapping to Agno tools
TOOL_REGISTRY = {
    'WebSearchTool': DuckDuckGoTools,
    'SummarizeTool': None,  # Custom implementation
    'FileOpsTool': None,  # Custom implementation
    'MathTool': None,  # Custom implementation
    'YFinanceTool': YFinanceTools,  # Bonus: Stock market tool
}


def get_tool_instances(tool_names: List[str]) -> List[Any]:
    """Get tool instances from names"""
    tools = []
    
    for tool_name in tool_names:
        if tool_name == 'WebSearchTool':
            # Use Agno's built-in DuckDuckGo search
            tools.append(DuckDuckGoTools())
        
        elif tool_name == 'YFinanceTool':
            # Use Agno's finance tools
            tools.append(YFinanceTools())
        
        elif tool_name == 'SummarizeTool':
            # Summarization is handled by the model itself
            # We'll add it to instructions instead
            pass
        
        elif tool_name == 'FileOpsTool':
            # File operations - we'll handle through custom function
            from core.tools.file_ops_agno import get_file_ops_tool
            tools.append(get_file_ops_tool())
        
        elif tool_name == 'MathTool':
            # Math - we'll handle through custom function
            from core.tools.math_tool_agno import get_math_tool
            tools.append(get_math_tool())
    
    return tools


class AgentRunner:
    """Runs an agent with specified configuration using Agno"""
    
    def __init__(self, agent_config: Dict):
        self.config = agent_config
        self.name = agent_config.get('name', 'Agent')
        self.description = agent_config.get('description', '')
        self.model_name = agent_config.get('model', 'llama-3.3-70b-versatile')
        self.system_prompt = agent_config.get('prompt', 'You are a helpful AI assistant.')
        self.tool_names = agent_config.get('tools', [])
        
        # Initialize Agno agent
        self.agent = None
        self._init_agent()
    
    def _init_agent(self):
        """Initialize the Agno agent"""
        groq_config = get_config()
        
        # Check if API key is configured
        if not groq_config.is_configured():
            # Agent will be None in demo mode
            self.agent = None
            return
        
        # Get tools
        tools = get_tool_instances(self.tool_names)
        
        # Build instructions
        instructions = [self.system_prompt]
        
        # Add tool-specific instructions
        if 'SummarizeTool' in self.tool_names:
            instructions.append("When asked to summarize, provide concise summaries of key points.")
        
        # Create Agno agent
        try:
            self.agent = Agent(
                name=self.name,
                model=Groq(id=self.model_name),
                description=self.description,
                instructions=instructions,
                tools=tools if tools else None,
                markdown=True,
            )
        except Exception as e:
            print(f"Error initializing agent: {e}")
            self.agent = None
    
    def run(self, user_input: str, chat_history: Optional[List[Dict]] = None) -> str:
        """Run the agent with user input"""
        
        try:
            # Check if API key is configured
            groq_config = get_config()
            if not groq_config.is_configured() or self.agent is None:
                return self._demo_mode_response(user_input)
            
            # Run the agent
            response: RunOutput = self.agent.run(user_input, stream=False)
            
            # Extract the content from response
            if response and response.content:
                return response.content
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
        
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                return f"❌ **API Key Error**\n\nPlease check your GroqCloud API key.\n\nError: {error_msg}"
            else:
                return f"❌ **Error**: {error_msg}\n\n💡 Make sure your GROQ_API_KEY is valid."
    
    def _demo_mode_response(self, user_input: str) -> str:
        """Generate demo response when no API key"""
        response = f"""🤖 **{self.name}** (Demo Mode)

**Agent Profile:**
{self.description}

**System Instructions:**
{self.system_prompt}

---

📝 **Your message:** 
> {user_input}

---

⚠️ **Demo Mode Active - No Real AI Response**

To get actual AI responses powered by GroqCloud:

1. **Get API Key**: Visit [console.groq.com](https://console.groq.com)
2. **Set API Key**: 
   - Enter in sidebar → API Key Settings
   - Or set environment variable: `GROQ_API_KEY=your_key_here`
3. **Restart Agent**: The agent will automatically use your key

**Current Configuration:**
- **Model**: {self.model_name}
- **Tools**: {', '.join(self.tool_names) if self.tool_names else 'None'}
- **Framework**: Agno + GroqCloud

---

### What This Agent Can Do (With API Key):
"""
        
        if 'WebSearchTool' in self.tool_names:
            response += "\n🔍 **Web Search**: Search DuckDuckGo for current information"
        if 'SummarizeTool' in self.tool_names:
            response += "\n📝 **Summarize**: Condense long texts into key points"
        if 'FileOpsTool' in self.tool_names:
            response += "\n📁 **File Operations**: Read and write files safely"
        if 'MathTool' in self.tool_names:
            response += "\n🧮 **Calculator**: Perform complex mathematical calculations"
        if 'YFinanceTool' in self.tool_names:
            response += "\n💰 **Finance Data**: Get stock prices and market analysis"
        
        response += "\n\n*This is a simulated response. With a real API key, the agent would provide an intelligent, context-aware answer to your query.*"
        
        return response
    
    def get_info(self) -> str:
        """Get agent information"""
        info = f"""**{self.name}**

{self.description}

**Model**: {self.model_name}
**Tools**: {', '.join(self.tool_names) if self.tool_names else 'None'}
**Framework**: Agno + GroqCloud

**System Instructions:**
{self.system_prompt}
"""
        return info
