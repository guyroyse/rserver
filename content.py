"""
RServer content management.
"""

import os
import config


def ensure_public_directory():
    """Create public directory and default index.html if directory didn't exist. Returns True if created."""
    
    public_dir = config.public_dir()
    
    # Create the public directory and index.html if they don't exist
    if not os.path.exists(public_dir):
        create_public_directory(public_dir)        
        create_default_index(public_dir)
        return True
    
    return False


def create_public_directory(public_dir):
    """Create the public directory."""

    os.makedirs(public_dir, exist_ok=True)


def create_default_index(public_dir):
    """Create the default file."""
    
    default_filename = config.default_file()
    index_path = os.path.join(public_dir, default_filename)
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RServer - Hello World</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .info {
            background: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #2196F3;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello World!</h1>
        <p class="subtitle">Welcome to RServer</p>
        
        <div class="info">
            <strong>🎉 Success!</strong> You're viewing this page over the Reticulum network.
        </div>
        
        <p>This is a simple HTML page served by RServer, demonstrating HTTP-like web serving over Reticulum Links.</p>
        
        <p><strong>What's happening:</strong></p>
        <ul>
            <li>Your browser connected to this RServer over Reticulum</li>
            <li>The server loaded this file from the public directory</li>
            <li>Content was delivered using reliable Reticulum Links</li>
            <li>No internet connection required!</li>
        </ul>
    </div>
</body>
</html>"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)