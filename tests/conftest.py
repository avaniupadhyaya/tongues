# conftest.py — pytest configuration for Tongues app
# Place this file in the tests/ directory

import pytest
import sys
import os

# Ensure the parent directory (tongues-python/) is on the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
