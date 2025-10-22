"""
Agent Manager - Handles CRUD operations for agents in local storage
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import shutil

DATA_DIR = "data"
AGENTS_FILE = os.path.join(DATA_DIR, "agents.json")
EXAMPLE_AGENTS_FILE = os.path.join(DATA_DIR, "example_agents.json")
CHATS_DIR = os.path.join(DATA_DIR, "chats")


def ensure_data_directory():
    """Ensure data directory and files exist"""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CHATS_DIR, exist_ok=True)
    
    if not os.path.exists(AGENTS_FILE):
        with open(AGENTS_FILE, 'w') as f:
            json.dump([], f)


def load_agents() -> List[Dict]:
    """Load all agents from local storage"""
    ensure_data_directory()
    
    try:
        with open(AGENTS_FILE, 'r') as f:
            agents = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        agents = []
    
    # If no agents exist, load example agents
    if not agents and os.path.exists(EXAMPLE_AGENTS_FILE):
        try:
            with open(EXAMPLE_AGENTS_FILE, 'r') as f:
                agents = json.load(f)
            save_agents(agents)
        except (FileNotFoundError, json.JSONDecodeError):
            agents = []
    
    return agents


def save_agents(agents: List[Dict]):
    """Save agents to local storage"""
    ensure_data_directory()
    with open(AGENTS_FILE, 'w') as f:
        json.dump(agents, f, indent=2)


def create_agent(agent_data: Dict) -> Dict:
    """Create a new agent"""
    agents = load_agents()
    
    # Generate unique ID
    agent_id = f"agent_{len(agents) + 1:03d}"
    while any(a.get('id') == agent_id for a in agents):
        agent_id = f"agent_{int(agent_id.split('_')[1]) + 1:03d}"
    
    # Add metadata
    agent_data['id'] = agent_id
    agent_data['created_at'] = datetime.now().strftime("%Y-%m-%d")
    
    # Add to list and save
    agents.append(agent_data)
    save_agents(agents)
    
    return agent_data


def get_agent(agent_id: str) -> Optional[Dict]:
    """Get a specific agent by ID"""
    agents = load_agents()
    for agent in agents:
        if agent.get('id') == agent_id:
            return agent
    return None


def get_agent_by_name(name: str) -> Optional[Dict]:
    """Get a specific agent by name"""
    agents = load_agents()
    for agent in agents:
        if agent.get('name') == name:
            return agent
    return None


def update_agent(agent_id: str, updated_data: Dict) -> bool:
    """Update an existing agent"""
    agents = load_agents()
    
    for i, agent in enumerate(agents):
        if agent.get('id') == agent_id:
            # Preserve ID and creation date
            updated_data['id'] = agent_id
            updated_data['created_at'] = agent.get('created_at')
            agents[i] = updated_data
            save_agents(agents)
            return True
    
    return False


def delete_agent(agent_id: str) -> bool:
    """Delete an agent"""
    agents = load_agents()
    original_count = len(agents)
    
    agents = [a for a in agents if a.get('id') != agent_id]
    
    if len(agents) < original_count:
        save_agents(agents)
        return True
    
    return False


def search_agents(query: str = "", filters: Dict = None) -> List[Dict]:
    """Search and filter agents"""
    agents = load_agents()
    
    if not query and not filters:
        return agents
    
    results = agents
    
    # Text search
    if query:
        query_lower = query.lower()
        results = [
            a for a in results
            if query_lower in a.get('name', '').lower()
            or query_lower in a.get('description', '').lower()
            or query_lower in a.get('author', '').lower()
            or any(query_lower in tool.lower() for tool in a.get('tools', []))
        ]
    
    # Apply filters
    if filters:
        if 'author' in filters and filters['author']:
            results = [a for a in results if a.get('author') == filters['author']]
        
        if 'model' in filters and filters['model']:
            results = [a for a in results if a.get('model') == filters['model']]
        
        if 'tools' in filters and filters['tools']:
            results = [
                a for a in results
                if any(tool in a.get('tools', []) for tool in filters['tools'])
            ]
    
    return results


def save_chat(agent_name: str, messages: List[Dict]) -> str:
    """Save a chat conversation"""
    ensure_data_directory()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_name.replace(' ', '_')}_{timestamp}.json"
    filepath = os.path.join(CHATS_DIR, filename)
    
    chat_data = {
        'agent': agent_name,
        'timestamp': timestamp,
        'messages': messages
    }
    
    with open(filepath, 'w') as f:
        json.dump(chat_data, f, indent=2)
    
    return filepath

