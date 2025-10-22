"""
Import Agent Example
This script shows how to programmatically import agents into Agent Market
"""
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import create_agent


def import_agent_from_json(json_file_path):
    """Import an agent from a JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            agent_data = json.load(f)
        
        # Validate required fields
        required_fields = ['name', 'author', 'description', 'model', 'prompt']
        missing = [f for f in required_fields if f not in agent_data]
        
        if missing:
            print(f"❌ Error: Missing required fields: {', '.join(missing)}")
            return None
        
        # Create agent
        created_agent = create_agent(agent_data)
        print(f"✅ Successfully imported agent: {created_agent['name']}")
        print(f"   ID: {created_agent['id']}")
        print(f"   Author: {created_agent['author']}")
        return created_agent
    
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        import_agent_from_json(json_file)
    else:
        # Import the example agent
        example_file = os.path.join(
            os.path.dirname(__file__),
            'custom_agent_example.json'
        )
        print("Importing example agent...")
        import_agent_from_json(example_file)
        print("\nUsage: python import_agent.py <path_to_agent.json>")

