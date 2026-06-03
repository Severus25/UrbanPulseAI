"""Pytest configuration and pythonpath alignment."""

import os
import sys

# Calculate paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_gateway_path = os.path.join(project_root, "services", "data-gateway")

# Add paths to sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if data_gateway_path not in sys.path:
    sys.path.insert(0, data_gateway_path)

try:
    # Import the app module natively (since services/data-gateway is now in sys.path)
    import app
    import app.main

    # Alias them in sys.modules so imports of services.data_gateway.app.main work
    sys.modules["services.data_gateway.app"] = app
    sys.modules["services.data_gateway.app.main"] = app.main
except Exception as e:
    print(f"Warning: Failed to programmatically alias services.data_gateway: {e}", file=sys.stderr)
