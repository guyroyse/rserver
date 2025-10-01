# RServer - HTTP Server for Reticulum Networks

A lightweight HTTP/1.1 web server that runs over [Reticulum](https://reticulum.network) mesh networks, enabling decentralized web hosting without internet infrastructure.

## Features

- **HTTP/1.1 Protocol** - Full request/response implementation
- **Static File Serving** - HTML, CSS, JavaScript, images, PDFs, fonts
- **Security** - Directory traversal protection, safe path handling
- **MIME Type Detection** - Automatic Content-Type headers
- **Binary File Support** - Serves all file types correctly
- **Zero Configuration** - Works out of the box
- **Testing Tools** - Built-in MeshCurl client for development

## Getting Started

### Prerequisites

- **Python 3.12 or newer**
- **Reticulum** networking library

### Installation

1. **Install Python**

   Download and install Python 3.12 or newer from [python.org](https://www.python.org/downloads/). Verify installation:
   ```bash
   python --version
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/guyroyse/rserver.git
   cd rserver
   ```

3. **Install Reticulum**
   ```bash
   pip install rns
   ```

### Adding Your Website

Place your website files in the `public/` directory:

```bash
# Create the public directory if it doesn't exist
mkdir public

# Add your files
cp -r /path/to/your/website/* public/
```

Your site should include at least an `index.html` file, which will be served when users request the root path `/`. You can organize your files however you like:

```
public/
├── index.html          # Homepage (required)
├── about.html          # Other pages
├── styles.css          # Stylesheets
├── script.js           # JavaScript
├── images/             # Image directory
│   ├── logo.png
│   └── photo.jpg
└── assets/             # Other assets
    └── document.pdf
```

### Running the Server

1. **Start RServer:**
   ```bash
   python rserver.py
   ```

2. **Note the destination hash** displayed in the output:
   ```
   Server destination: a1b2c3d4e5f6789abcdef0123456789abcdef01234567
   ```

   This hash is the address clients use to connect to your server over the Reticulum network.

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

RServer uses TOML configuration files stored in the `config/` directory. The server will automatically create default configuration files on first run, but you can customize them as needed.

### Server Configuration (`config/server.toml`)

```toml
[server]
public_dir = "public"        # Directory containing your website files
default_file = "index.html"  # Default file to serve for directory requests

[app]
name = "rserver"             # Application name
aspect = "web"               # Application aspect for Reticulum
```

### Identity Files

RServer stores its cryptographic identity in the `config/` directory. This identity is persistent across server restarts and determines the server's destination hash. Do not delete these files unless you want to generate a new server address.

## Testing with MeshCurl

MeshCurl is a command-line HTTP client for Reticulum networks, similar to curl. It's included with RServer for testing and development.

### Basic Usage

```bash
python meshcurl.py <destination_hash> <path>
```

### Examples

```bash
# Request the homepage
python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /

# Request a specific page
python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /about.html

# Request an image
python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 /images/logo.png

# Verbose output (shows request/response details)
python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 -v /

# Different HTTP method
python meshcurl.py a1b2c3d4e5f6789abcdef0123456789abcdef01234567 -X POST /api/data
```

### MeshCurl Options

- `-v` - Verbose output showing request and response headers
- `-X METHOD` - Specify HTTP method (GET, POST, etc.)

## Browsing with MeshBrowser

For a full graphical browsing experience, check out [MeshBrowser](https://github.com/guyroyse/mesh-browser) - a web browser designed specifically for Reticulum networks. MeshBrowser provides a familiar browser interface for accessing RServer and other Reticulum web services.

## How Files Are Served

Files in your `public/` directory map directly to URL paths:

- `public/index.html` → `/` or `/index.html`
- `public/about.html` → `/about.html`
- `public/styles.css` → `/styles.css`
- `public/images/logo.png` → `/images/logo.png`
- `public/docs/guide.pdf` → `/docs/guide.pdf`

### Directory Indexes

When a user requests a directory path (like `/docs/`), RServer will automatically serve the `index.html` file from that directory if it exists:

- Request to `/` → serves `public/index.html`
- Request to `/docs/` → serves `public/docs/index.html`

## HTTP Features

### Supported Methods
- **GET** - File serving (implemented)
- **POST, PUT, DELETE** - Planned for future releases

### Status Codes
- **200 OK** - Successful file serving
- **400 Bad Request** - Malformed HTTP request
- **403 Forbidden** - Directory traversal attempt
- **404 Not Found** - File not found
- **405 Method Not Allowed** - Unsupported HTTP method
- **500 Internal Server Error** - Server error

### MIME Types
Automatic Content-Type detection for common file types:
- **HTML**: `text/html`
- **CSS**: `text/css`
- **JavaScript**: `text/javascript`
- **Images**: `image/png`, `image/jpeg`, `image/gif`, `image/svg+xml`
- **Fonts**: `font/woff2`, `font/woff`, `font/ttf`
- **Documents**: `application/pdf`, `application/json`
- **And many more** - Uses Python's mimetypes module for comprehensive coverage

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