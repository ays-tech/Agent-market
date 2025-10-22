#!/bin/bash

echo "========================================"
echo "  Running Agent Market Tests"
echo "========================================"
echo ""

echo "Running all tests..."
pytest tests/ -v --tb=short

echo ""
echo "========================================"
echo "  Test run complete!"
echo "========================================"

