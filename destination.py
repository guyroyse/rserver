"""
RServer destination management.
"""

import RNS
import config


def create_destination(identity):
    """Create a Reticulum destination for the web server."""
    app_name, aspect = config.app_context()
    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,      # Accept incoming connections
        RNS.Destination.SINGLE,  # Single instance
        app_name, aspect         # Application context from config
    )
    
    return destination