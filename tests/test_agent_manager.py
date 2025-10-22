"""
Test cases for Agent Manager - CRUD operations
"""
import pytest
import json
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import (
    create_agent,
    get_agent,
    get_agent_by_name,
    update_agent,
    delete_agent,
    search_agents,
    load_agents,
    save_agents
)


@pytest.fixture
def temp_data_dir(tmp_path, monkeypatch):
    """Create a temporary data directory for testing"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    chats_dir = data_dir / "chats"
    chats_dir.mkdir()
    
    # Create empty agents.json
    agents_file = data_dir / "agents.json"
    agents_file.write_text("[]")
    
    # Create empty example_agents.json
    example_file = data_dir / "example_agents.json"
    example_file.write_text("[]")
    
    # Patch the module-level constants
    import core.agent_manager as am
    monkeypatch.setattr(am, 'DATA_DIR', str(data_dir))
    monkeypatch.setattr(am, 'AGENTS_FILE', str(agents_file))
    monkeypatch.setattr(am, 'EXAMPLE_AGENTS_FILE', str(example_file))
    monkeypatch.setattr(am, 'CHATS_DIR', str(chats_dir))
    
    yield data_dir


class TestAgentManager:
    """Test suite for Agent Manager"""
    
    def test_create_agent(self, temp_data_dir):
        """Test creating a new agent"""
        agent_data = {
            'name': 'Test Agent',
            'author': 'Test Author',
            'description': 'A test agent',
            'model': 'llama-3.3-70b-versatile',
            'tools': ['WebSearchTool'],
            'prompt': 'You are a test agent'
        }
        
        created_agent = create_agent(agent_data)
        
        assert created_agent['name'] == 'Test Agent'
        assert created_agent['author'] == 'Test Author'
        assert 'id' in created_agent
        assert 'created_at' in created_agent
        assert created_agent['id'].startswith('agent_')
    
    def test_create_multiple_agents(self, temp_data_dir):
        """Test creating multiple agents"""
        agent1 = create_agent({
            'name': 'Agent 1',
            'author': 'Author 1',
            'description': 'First agent',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Agent 1'
        })
        
        agent2 = create_agent({
            'name': 'Agent 2',
            'author': 'Author 2',
            'description': 'Second agent',
            'model': 'llama-3.1-8b-instant',
            'tools': ['WebSearchTool'],
            'prompt': 'Agent 2'
        })
        
        assert agent1['id'] != agent2['id']
        
        agents = load_agents()
        assert len(agents) == 2
    
    def test_get_agent(self, temp_data_dir):
        """Test retrieving an agent by ID"""
        created = create_agent({
            'name': 'Retrieve Test',
            'author': 'Test',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        retrieved = get_agent(created['id'])
        
        assert retrieved is not None
        assert retrieved['id'] == created['id']
        assert retrieved['name'] == 'Retrieve Test'
    
    def test_get_agent_by_name(self, temp_data_dir):
        """Test retrieving an agent by name"""
        create_agent({
            'name': 'Unique Name Agent',
            'author': 'Test',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        retrieved = get_agent_by_name('Unique Name Agent')
        
        assert retrieved is not None
        assert retrieved['name'] == 'Unique Name Agent'
    
    def test_update_agent(self, temp_data_dir):
        """Test updating an agent"""
        created = create_agent({
            'name': 'Original Name',
            'author': 'Test',
            'description': 'Original description',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Original prompt'
        })
        
        updated_data = {
            'name': 'Updated Name',
            'author': 'Test',
            'description': 'Updated description',
            'model': 'llama-3.1-8b-instant',
            'tools': ['WebSearchTool', 'MathTool'],
            'prompt': 'Updated prompt'
        }
        
        success = update_agent(created['id'], updated_data)
        
        assert success is True
        
        updated = get_agent(created['id'])
        assert updated['name'] == 'Updated Name'
        assert updated['description'] == 'Updated description'
        assert updated['model'] == 'llama-3.1-8b-instant'
        assert 'WebSearchTool' in updated['tools']
        assert updated['id'] == created['id']  # ID should not change
    
    def test_delete_agent(self, temp_data_dir):
        """Test deleting an agent"""
        created = create_agent({
            'name': 'To Delete',
            'author': 'Test',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        success = delete_agent(created['id'])
        
        assert success is True
        
        retrieved = get_agent(created['id'])
        assert retrieved is None
    
    def test_delete_nonexistent_agent(self, temp_data_dir):
        """Test deleting an agent that doesn't exist"""
        success = delete_agent('nonexistent_id')
        assert success is False
    
    def test_search_agents_by_name(self, temp_data_dir):
        """Test searching agents by name"""
        create_agent({
            'name': 'Python Expert',
            'author': 'Test',
            'description': 'Expert in Python',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        create_agent({
            'name': 'JavaScript Expert',
            'author': 'Test',
            'description': 'Expert in JavaScript',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        results = search_agents(query='Python')
        
        assert len(results) == 1
        assert results[0]['name'] == 'Python Expert'
    
    def test_search_agents_by_author(self, temp_data_dir):
        """Test searching agents by author"""
        create_agent({
            'name': 'Agent 1',
            'author': 'Alice',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        create_agent({
            'name': 'Agent 2',
            'author': 'Bob',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': [],
            'prompt': 'Test'
        })
        
        results = search_agents(query='Alice')
        
        assert len(results) == 1
        assert results[0]['author'] == 'Alice'
    
    def test_search_agents_with_filters(self, temp_data_dir):
        """Test searching agents with filters"""
        create_agent({
            'name': 'Agent 1',
            'author': 'Alice',
            'description': 'Test',
            'model': 'llama-3.3-70b-versatile',
            'tools': ['WebSearchTool'],
            'prompt': 'Test'
        })
        
        create_agent({
            'name': 'Agent 2',
            'author': 'Bob',
            'description': 'Test',
            'model': 'llama-3.1-8b-instant',
            'tools': ['MathTool'],
            'prompt': 'Test'
        })
        
        # Filter by model
        results = search_agents(filters={'model': 'llama-3.1-8b-instant'})
        assert len(results) == 1
        assert results[0]['name'] == 'Agent 2'
        
        # Filter by author
        results = search_agents(filters={'author': 'Alice'})
        assert len(results) == 1
        assert results[0]['name'] == 'Agent 1'
        
        # Filter by tools
        results = search_agents(filters={'tools': ['WebSearchTool']})
        assert len(results) == 1
        assert results[0]['name'] == 'Agent 1'
    
    def test_load_empty_agents(self, temp_data_dir):
        """Test loading agents when file is empty"""
        agents = load_agents()
        assert isinstance(agents, list)
        # May be empty or may load example agents
    
    def test_save_and_load_agents(self, temp_data_dir):
        """Test saving and loading agents"""
        test_agents = [
            {
                'id': 'agent_001',
                'name': 'Test Agent 1',
                'author': 'Test',
                'description': 'Test',
                'model': 'llama-3.3-70b-versatile',
                'tools': [],
                'prompt': 'Test',
                'created_at': '2025-10-22'
            },
            {
                'id': 'agent_002',
                'name': 'Test Agent 2',
                'author': 'Test',
                'description': 'Test',
                'model': 'llama-3.1-8b-instant',
                'tools': ['WebSearchTool'],
                'prompt': 'Test',
                'created_at': '2025-10-22'
            }
        ]
        
        save_agents(test_agents)
        loaded_agents = load_agents()
        
        assert len(loaded_agents) == 2
        assert loaded_agents[0]['name'] == 'Test Agent 1'
        assert loaded_agents[1]['name'] == 'Test Agent 2'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

