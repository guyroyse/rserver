"""
RServer configuration management.
"""

import os
import tomllib

# Fixed path (only this one needs to be constant to bootstrap config loading)
CONFIG_PATH = "config/server.toml"

def identity_path():
    """Get the identity file path."""
    config = load_config()
    return config.get("server", {}).get("identity_path", "config/identity")

def public_dir():
    """Get the public directory path."""
    config = load_config()
    return config.get("server", {}).get("public_dir", "public/")

def server_name():
    """Get the server display name."""
    config = load_config()
    return config.get("server", {}).get("name", "RServer Demo")

def default_file():
    """Get the default file name (e.g., index.html)."""
    config = load_config()
    return config.get("server", {}).get("default_file", "index.html")

def announce_interval():
    """Get the announcement interval in seconds."""
    config = load_config()
    return config.get("network", {}).get("announce_interval", 300)

def app_context():
    """Get the application context (app_name, aspect)."""
    config = load_config()
    network = config.get("network", {})
    return network.get("app_name", "rserver"), network.get("aspect", "web")


# Cache for loaded config
_config_cache = None


def load_config():
    """Load configuration from TOML file with defaults."""

    global _config_cache
    
    # Return cached config if already loaded
    if _config_cache is not None:
        return _config_cache
    
    # Create default config file if it doesn't exist
    if not os.path.exists(CONFIG_PATH):
        create_default_config()
    
    # Now read the config file
    try:
        with open(CONFIG_PATH, 'rb') as f:
            _config_cache = tomllib.load(f)
        return _config_cache
    except Exception as e:
        raise ValueError(f"Error reading config file {CONFIG_PATH}: {e}")


def create_default_config():
    """Create a default server.toml file."""
    
    os.makedirs("config", exist_ok=True)
    
    toml_content = """# RServer Configuration

[server]
# Server display name (for discovery)  
name = "RServer Demo"

# Path to server identity file
identity_path = "config/identity"

# File serving settings
public_dir = "public/"        # Directory to serve static content from
directory_listings = true     # Enable directory listings for folders without default file
default_file = "index.html"   # Default file to serve (e.g., index.html, home.html)

[network]
# Application context for destination (should not normally be changed)
app_name = "rserver"
aspect = "web"

# Server announcement interval in seconds
announce_interval = 300
"""
    
    with open(CONFIG_PATH, 'w') as f:
        f.write(toml_content)
    print(f"✓ Created default config file: {CONFIG_PATH}")
