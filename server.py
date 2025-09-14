"""
RServer HTTP-like request handling.
"""

import config
from link import start_link_server


def start_server(destination):
    """Start the RServer."""
    start_link_server(destination, handle_data)
    print(f"✓ HTTP server started")

def handle_data(data):
    """Handle incoming data from Link layer."""
    try:
        # Decode the request
        request_data = data.decode('utf-8')
        print(f"✓ Received: {request_data[:50]}...")
        
        # Parse and handle the HTTP request
        response = handle_request(request_data)
        
        # Return response as bytes
        return response.encode('utf-8')
        
    except Exception as e:
        print(f"✗ Error: {e}")
        # Return error response
        error_response = "HTTP/1.1 500 Internal Server Error\r\n\r\nServer Error"
        return error_response.encode('utf-8')

def handle_request(request_data):
    """Parse HTTP-like request and generate response."""
    lines = request_data.strip().split('\r\n')
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\nEmpty Request"
    
    # Parse request line: "GET /path HTTP/1.1"
    request_line = lines[0].split()
    if len(request_line) < 2:
        return "HTTP/1.1 400 Bad Request\r\n\r\nInvalid Request Line"
    
    method = request_line[0]
    path = request_line[1]
    
    print(f"✓ {method} {path}")
    
    # For now, just return a simple response
    if method == "GET":
        return handle_get_request(path)
    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Supported"

def handle_get_request(path):
    """Handle GET requests."""
    # Simple response for now
    html_content = f"""<!DOCTYPE html>
<html>
<head><title>RServer Response</title></head>
<body>
    <h1>Hello from RServer!</h1>
    <p>You requested: {path}</p>
    <p>This is a basic response from the Reticulum web server.</p>
</body>
</html>"""
    
    response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html\r
Content-Length: {len(html_content)}\r
\r
{html_content}"""
    
    return response