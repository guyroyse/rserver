# RServer - Reticulum Web Server

## Project Context

RServer is part of the **MeshWeb** project - a universal browser/server system for decentralized protocols. RServer specifically implements HTTP-like web serving over Reticulum networks.

## What RServer Does

- **Serves static web content** (HTML, CSS, JS, images) over Reticulum networks
- **Implements HTTP-like semantics** using Reticulum Links (not LXMF)
- **Auto-announces** itself on the network for browser discovery
- **File-based serving** - point it at a directory, it serves the contents
- **Handles routing** - supports paths like `/`, `/about.html`, `/images/logo.png`
- **MIME type detection** for proper Content-Type headers

## Architecture Decisions

### Protocol Choice: Reticulum Links
- **Not raw packets** (no reliability)
- **Not LXMF** (message-oriented, async, store-and-forward overhead)
- **Reticulum Links** - TCP-like reliable connections, perfect for request/response
- Links provide automatic acknowledgments, retries, and ordered delivery

### Protocol Design
```
Request Format:
- Method (GET, POST, etc.)
- Path (/index.html, /images/logo.png)
- Headers (optional)

Response Format:  
- Status code (200, 404, etc.)
- Content-Type (text/html, image/png, etc.)
- Body (file contents)
```

### Key Features for Demo
- **Simple command line**: `rserver ./my-website/`
- **Auto-discovery**: Announces itself so browsers can find it
- **Web-standard files**: Serves regular HTML/CSS/JS
- **404 handling**: Graceful error responses
- **Directory listing**: When browsing folders (optional)

## Technical Implementation

### Core Components
1. **Reticulum destination** creation and announcement
2. **Link request handler** for incoming browser connections  
3. **File system interface** for serving static content
4. **MIME type detection** for Content-Type headers
5. **Basic routing logic** for path resolution

### Python Structure
```python
import RNS
import RNS.Destination

class ReticServer:
    def __init__(self, content_dir):
        # Create Reticulum destination
        # Register link request handler
        # Start announcing server availability
        
    def handle_request(self, path, source):
        # Load file from content_dir + path
        # Return content + mime type  
        # Handle 404s gracefully
```

## User Experience Goals

### For Developers (Server Operators)
```bash
pip install meshweb
rserver ./my-website/
# Output: "Server running at reticulum://a1b2c3d4e5f6.../index.html"
```

### For End Users (Browser Users)
- Server appears in browser's discovery/directory
- Pages load like regular websites
- All over mesh networks (LoRa, WiFi, etc.)

## Demo Scenarios

1. **Basic file serving** - HTML page with CSS and images
2. **Multi-hop networking** - Server on different network segment
3. **Offline operation** - Works without internet
4. **Live development** - Edit files, refresh browser

## Future Extensibility

While starting with static files, architecture should support:
- **Dynamic content** (server-side scripting)
- **File uploads** (POST requests)
- **Authentication** (user login)
- **Real-time features** (WebSocket-like over Links)

## Development Priority

1. **Core serving** - Static HTML/CSS/JS files
2. **Discovery** - Announce mechanism  
3. **Error handling** - 404s, permission issues
4. **MIME types** - Proper Content-Type detection
5. **Command line** - Simple developer interface

## Why This Matters

RServer demonstrates **native Reticulum applications** rather than tunneling existing protocols. It shows how to build responsive, interactive apps directly on Reticulum's primitives - exactly what the ecosystem needs for broader adoption.
- Prefer putting called code after calling code.
- Always end source code files with a blank empty line.