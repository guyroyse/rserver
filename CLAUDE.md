# RServer - Reticulum Web Server

## Project Context

RServer is part of the **MeshWeb** project - a universal browser/server system for decentralized protocols. RServer specifically implements HTTP-like web serving over Reticulum networks.

## What RServer Does

- **Serves static web content** (HTML, CSS, JS, images, PDFs, etc.) over Reticulum networks
- **Implements HTTP/1.1-like semantics** using Reticulum Links (not LXMF)
- **File-based serving** - serves files from a configurable public directory
- **Handles routing** - supports paths like `/`, `/about.html`, `/images/logo.png`
- **MIME type detection** - automatic Content-Type headers for all file types
- **Binary file support** - serves images, fonts, PDFs, and other binary content
- **Security features** - prevents directory traversal attacks
- **Error handling** - proper HTTP status codes (200, 404, 403, 500, etc.)

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

### Current Implementation

**Modular Architecture:**
```
rserver/
├── http/                    # HTTP protocol handling
│   ├── http.py             # Main HTTP request handler
│   ├── request_parser.py   # HTTP request parsing
│   └── response_builder.py # HTTP response construction
├── reticulum/              # Reticulum networking
│   ├── identity.py         # Cryptographic identity management
│   ├── destination.py      # Network destination creation
│   └── link.py             # Link connection handling
├── config.py               # TOML configuration
├── content.py              # Public directory management
├── rserver.py              # Main server orchestrator
└── meshcurl.py             # HTTP client for testing

```

**Key Features Implemented:**
- **HTTP/1.1 request parsing** - method, path, headers, body
- **MIME type detection** - uses Python mimetypes module
- **Binary file serving** - all files read as binary for universal support
- **Security checks** - blocks directory traversal with ".."
- **Error responses** - 400, 403, 404, 405, 500 with proper HTTP format
- **Directory index** - serves index.html for directory requests
- **Configuration** - TOML config files for identity, paths, defaults

## User Experience Goals

### For Developers (Server Operators)
```bash
# Start the server
python rserver.py
# Output: "✓ Server destination: a1b2c3d4e5f6789abcdef..."

# Test with meshcurl (like curl for Reticulum)
python meshcurl.py a1b2c3d4e5f6... /
python meshcurl.py a1b2c3d4e5f6... /styles.css
python meshcurl.py a1b2c3d4e5f6... /guy-head.png
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

## Development Status

**✅ Completed:**
1. **Core serving** - Static HTML/CSS/JS/image files working
2. **Error handling** - 404s, 403s, 500s with proper HTTP responses
3. **MIME types** - Automatic Content-Type detection for all file types
4. **Binary file support** - Images, PDFs, fonts served correctly
5. **HTTP protocol** - Full HTTP/1.1 request/response implementation
6. **Security** - Directory traversal protection
7. **Testing tool** - MeshCurl for development and debugging

**🚧 Future Enhancements:**
- **Discovery mechanism** - Auto-announce for browser discovery
- **Directory listings** - Show folder contents when no index.html
- **Custom error pages** - Serve HTML error pages instead of plain text
- **Configuration** - Command line options for port, directory, etc.
- **Performance** - Caching, compression, keep-alive connections

## Why This Matters

RServer demonstrates **native Reticulum applications** rather than tunneling existing protocols. It shows how to build responsive, interactive apps directly on Reticulum's primitives - exactly what the ecosystem needs for broader adoption.
- Prefer putting called code after calling code.
- Always end source code files with a blank empty line.