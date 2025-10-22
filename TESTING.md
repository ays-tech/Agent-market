# 🧪 Testing Guide - Agent Market

## Quick Start

### Run All Tests

**Windows:**
```bash
run_tests.bat
```

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

**Or using pytest directly:**
```bash
pytest tests/ -v
```

---

## Test Files

### 1. `tests/test_agent_manager.py`
Tests for CRUD operations on agents.

**Run only this test:**
```bash
pytest tests/test_agent_manager.py -v
```

**Test Coverage:**
- ✅ Create agent
- ✅ Create multiple agents
- ✅ Get agent by ID
- ✅ Get agent by name
- ✅ Update agent
- ✅ Delete agent
- ✅ Search agents (by name, author, tools)
- ✅ Filter agents (by model, author, tools)
- ✅ Load and save agents

### 2. `tests/test_tools.py`
Tests for custom Agno tools.

**Run only this test:**
```bash
pytest tests/test_tools.py -v
```

**Test Coverage:**
- ✅ File Operations Tool
  - Read files
  - Write files
  - List directories
  - Security (path traversal, absolute paths)
- ✅ Math Calculator Tool
  - Basic arithmetic
  - Functions (sqrt, sin, cos, etc.)
  - Constants (pi, e)
  - Complex expressions
  - Error handling

---

## Running Specific Tests

### Run a specific test class:
```bash
pytest tests/test_agent_manager.py::TestAgentManager -v
```

### Run a specific test method:
```bash
pytest tests/test_agent_manager.py::TestAgentManager::test_create_agent -v
```

### Run tests matching a pattern:
```bash
pytest tests/ -k "search" -v
```

---

## Pytest Options

### Verbose output:
```bash
pytest tests/ -v
```

### Show print statements:
```bash
pytest tests/ -v -s
```

### Stop at first failure:
```bash
pytest tests/ -x
```

### Show test coverage:
```bash
pytest tests/ --cov=core --cov-report=html
```

### Run with detailed output:
```bash
pytest tests/ -vv
```

---

## Test Results Explanation

### ✅ PASSED
Test completed successfully

### ❌ FAILED
Test failed - check the output for details

### ⚠️ SKIPPED
Test was skipped (not applicable or requires setup)

### 🔄 XFAIL
Expected failure (known issue)

---

## Example Output

```
======================================
Running Agent Market Tests
======================================

tests/test_agent_manager.py::TestAgentManager::test_create_agent PASSED         [10%]
tests/test_agent_manager.py::TestAgentManager::test_create_multiple_agents PASSED [20%]
tests/test_agent_manager.py::TestAgentManager::test_get_agent PASSED            [30%]
tests/test_agent_manager.py::TestAgentManager::test_update_agent PASSED         [40%]
tests/test_agent_manager.py::TestAgentManager::test_delete_agent PASSED         [50%]
tests/test_tools.py::TestFileOpsTool::test_read_file PASSED                     [60%]
tests/test_tools.py::TestFileOpsTool::test_write_file PASSED                    [70%]
tests/test_tools.py::TestMathTool::test_basic_arithmetic PASSED                 [80%]
tests/test_tools.py::TestMathTool::test_sqrt_function PASSED                    [90%]
tests/test_tools.py::TestMathTool::test_complex_expression PASSED               [100%]

======================== 10 passed in 2.34s ========================
```

---

## Writing New Tests

### Test File Template:
```python
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.your_module import your_function

class TestYourFeature:
    """Test suite for your feature"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        result = your_function()
        assert result == expected_value
```

### Best Practices:
1. One test file per module
2. Use descriptive test names
3. Test both success and failure cases
4. Use fixtures for setup/teardown
5. Keep tests independent
6. Assert expected behavior

---

## Troubleshooting

### ImportError: No module named 'pytest'
```bash
pip install pytest
```

### Tests not found
Make sure you're in the project root directory:
```bash
cd "C:\Users\USER\Desktop\ai agent platform builder"
pytest tests/ -v
```

### Path issues
The tests automatically add the parent directory to the path:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

## CI/CD Integration

### GitHub Actions Example:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

---

## Test Coverage Goals

- ✅ Agent Manager: 90%+ coverage
- ✅ Tools: 80%+ coverage
- 🎯 Overall: 85%+ coverage

Run with coverage report:
```bash
pip install pytest-cov
pytest tests/ --cov=core --cov-report=term-missing
```

---

Happy Testing! 🧪✨

