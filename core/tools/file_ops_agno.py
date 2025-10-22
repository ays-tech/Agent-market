"""
File Operations Tool - Agno compatible
"""
import os
from typing import Optional


def get_file_ops_tool():
    """Get file operations tool for Agno"""
    
    def file_operations(command: str) -> str:
        """
        Execute file operations.
        
        Args:
            command: Command in format 'read:filepath' or 'write:filepath:content' or 'list:directory'
        
        Returns:
            Result of the file operation
        """
        try:
            parts = command.split(':', 2)
            operation = parts[0].lower()
            
            if operation == 'read':
                if len(parts) < 2:
                    return "Error: Please specify a file path. Format: 'read:filepath'"
                
                filepath = parts[1].strip()
                
                if not _is_safe_path(filepath):
                    return "Error: Access denied. Only files in the current workspace are accessible."
                
                if not os.path.exists(filepath):
                    return f"Error: File '{filepath}' not found."
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return f"📄 Contents of {filepath}:\n\n{content}"
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            
            elif operation == 'write':
                if len(parts) < 3:
                    return "Error: Format: 'write:filepath:content'"
                
                filepath = parts[1].strip()
                content = parts[2]
                
                if not _is_safe_path(filepath):
                    return "Error: Access denied."
                
                try:
                    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return f"✅ Successfully wrote to {filepath}"
                except Exception as e:
                    return f"Error writing file: {str(e)}"
            
            elif operation == 'list':
                directory = parts[1].strip() if len(parts) > 1 else '.'
                
                if not _is_safe_path(directory):
                    return "Error: Access denied."
                
                if not os.path.exists(directory):
                    return f"Error: Directory '{directory}' not found."
                
                try:
                    items = os.listdir(directory)
                    files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
                    dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
                    
                    result = f"📁 Contents of {directory}:\n\n"
                    if dirs:
                        result += "Directories:\n" + '\n'.join(f"  📁 {d}" for d in sorted(dirs)) + "\n\n"
                    if files:
                        result += "Files:\n" + '\n'.join(f"  📄 {f}" for f in sorted(files))
                    
                    return result if (dirs or files) else "Directory is empty."
                except Exception as e:
                    return f"Error listing directory: {str(e)}"
            
            else:
                return f"Error: Unknown operation '{operation}'. Use 'read', 'write', or 'list'."
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _is_safe_path(path: str) -> bool:
        """Check if path is safe to access"""
        if os.path.isabs(path):
            return False
        if '..' in path:
            return False
        return True
    
    # Return as a callable tool
    return file_operations

