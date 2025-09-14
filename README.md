# RServer - HTTP Server for Reticulum Networks

A lightweight HTTP/1.1 web server that runs over [Reticulum](https://reticulum.network) mesh networks, enabling decentralized web hosting without internet infrastructure.

## Features

- 🌐 **HTTP/1.1 Protocol** - Full request/response implementation
- 📁 **Static File Serving** - HTML, CSS, JavaScript, images, PDFs, fonts
- 🔒 **Security** - Directory traversal protection, safe path handling
- 🎯 **MIME Type Detection** - Automatic Content-Type headers
- 📱 **Binary File Support** - Serves all file types correctly
- ⚡ **Zero Configuration** - Works out of the box
- 🔧 **Testing Tools** - Built-in MeshCurl client for development

## Quick Start

### Prerequisites

- Python 3.7+
- [Reticulum](https://github.com/markqvist/Reticulum) installed

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd rserver

# Install Reticulum if not already installed
pip install rns
```

### Running the Server

1. **Start RServer:**
   ```bash
   python rserver.py
   ```

2. **Note the destination hash** from the output:
   ```
   ✓ Server destination: a1b2c3d4e5f6789abcdef0123456789abcdef01234567
   ```

3. **Test with MeshCurl:**
   ```bash
   # Request the homepage
   python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /

   # Request specific files
   python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /styles.css
   python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /guy-head.png
   ```

## Project Structure

```
rserver/
├── public/                 # Web content directory
│   ├── index.html         # Default homepage
│   ├── styles.css         # Stylesheet
│   ├── script.js          # JavaScript
│   └── guy-head.png       # Example image
├── http/                  # HTTP protocol implementation
│   ├── http.py           # Request handler
│   ├── request_parser.py # HTTP request parsing
│   └── response_builder.py # HTTP response building
├── reticulum/            # Reticulum networking
│   ├── identity.py       # Identity management
│   ├── destination.py    # Destination setup
│   └── link.py           # Link handling
├── config/               # Configuration files
│   └── server.toml       # Server configuration
├── rserver.py           # Main server
└── meshcurl.py          # HTTP client for testing
```

## Configuration

RServer uses TOML configuration files stored in the `config/` directory:

```toml
# config/server.toml
[server]
public_dir = "public"
default_file = "index.html"

[app]
name = "rserver"
aspect = "web"
```

## MeshCurl Usage

MeshCurl is a curl-like HTTP client for Reticulum networks:

```bash
# Basic usage
python meshcurl.py <destination_hash> [path]

# Examples
python meshcurl.py abc123def456... /                    # Homepage
python meshcurl.py abc123def456... /about.html          # Specific page
python meshcurl.py abc123def456... -v /                 # Verbose output
python meshcurl.py abc123def456... -X POST /api/data    # Different HTTP method
```

## Adding Content

1. **Add files to the `public/` directory:**
   ```bash
   cp mypage.html public/
   cp -r images/ public/
   ```

2. **Files are immediately available:**
   - `public/mypage.html` → `http://destination/mypage.html`
   - `public/images/logo.png` → `http://destination/images/logo.png`

3. **Directory indexes:**
   - `public/docs/` → serves `public/docs/index.html` if it exists
   - Root `/` → serves `public/index.html`

## HTTP Features

### Supported Methods
- ✅ GET (file serving)
- ❌ POST, PUT, DELETE (planned)

### Status Codes
- **200 OK** - Successful file serving
- **400 Bad Request** - Malformed HTTP request
- **403 Forbidden** - Directory traversal attempt
- **404 Not Found** - File not found
- **405 Method Not Allowed** - Unsupported HTTP method
- **500 Internal Server Error** - Server error

### MIME Types
Automatic detection for common file types:
- **HTML**: `text/html`
- **CSS**: `text/css`
- **JavaScript**: `text/javascript`
- **Images**: `image/png`, `image/jpeg`, `image/gif`
- **Fonts**: `font/woff2`, `font/woff`
- **PDFs**: `application/pdf`
- **And many more...**

## Security Features

- **Directory Traversal Protection** - Blocks paths containing `..`
- **Safe Path Resolution** - All paths confined to public directory
- **Input Validation** - HTTP request parsing with error handling
- **No Execute** - Static file serving only, no code execution

## How It Works

1. **Reticulum Integration**: RServer creates a Reticulum destination and listens for Link connections
2. **HTTP Protocol**: Incoming requests are parsed as HTTP/1.1 and responses follow HTTP standards
3. **File Serving**: Files are read from the public directory and served with appropriate MIME types
4. **Binary Support**: All files are handled as binary data for universal compatibility

## Development

### Architecture
- **Modular Design** - Separate packages for HTTP, Reticulum, and configuration
- **Clean Separation** - Protocol handling separate from file serving logic
- **Extensible** - Easy to add new HTTP methods, authentication, etc.

### Testing
```bash
# Start server in one terminal
python rserver.py

# Test in another terminal
python meshcurl.py <destination> /
python meshcurl.py <destination> /nonexistent  # Test 404
```

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Related Projects

- [Reticulum](https://reticulum.network) - The underlying mesh networking protocol
- [MeshWeb](https://github.com/your-org/meshweb) - Universal browser for decentralized protocols