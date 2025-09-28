import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

def test_app_import():
    import server
    assert hasattr(server, 'app')