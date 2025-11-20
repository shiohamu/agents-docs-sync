import os
import sys

# Ensure the repository root is in sys.path for all Python imports
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
