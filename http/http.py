"""
RServer HTTP-like request handling.
"""

import os
import mimetypes
import config
from .request_parser import parse_http_request
from .response_builder import build_response


def http_handler(data):
    """Handle incoming data from Link layer."""

    try:
        # Decode the request
        request_data = data.decode('utf-8')
        print(f"✓ Received:")
        print(request_data)
        
        # Parse and handle the HTTP request
        response = handle_request(request_data)
        
        # Return response (already bytes)
        return response
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return response_500_internal_error(str(e))


def handle_request(request_data):
    """Parse HTTP-like request and generate response."""

    try:
        method, path, version, headers, body = parse_http_request(request_data)
    except ValueError as e:
        return response_400_bad_request(str(e))
    
    print(f"✓ {method} {path}")
    
    # For now, just return a simple response
    if method == "GET":
        return handle_get_request(path, headers)
    else:
        return response_405_method_not_allowed("Method Not Supported")


def handle_get_request(path, headers):
    """Handle GET requests by serving files from public directory."""
    # Resolve path to actual file
    file_path = resolve_file_path(path)
    
    # Security check - block paths with .. 
    if not is_safe_path(path):
        return response_403_forbidden("Access denied")
    
    # Check if file exists
    if not os.path.exists(file_path):
        return response_404_not_found("File not found")
    
    # Read and serve the file
    try:
        content_type = detect_mime_type(file_path)
        
        # Read all files as binary
        with open(file_path, 'rb') as f:
            content = f.read()
        
        return response_200_ok(content, content_type)
    except Exception as e:
        return response_500_internal_error(f"Error reading file: {e}")


def resolve_file_path(url_path):
    """Resolve URL path to filesystem path."""

    # Find path relative to public directory
    file_path = os.path.join(config.public_dir(), url_path.lstrip('/'))
    
    # If path is a directory append default file
    if os.path.exists(file_path) and os.path.isdir(file_path):
        file_path = os.path.join(file_path, config.default_file())
    
    return file_path


def is_safe_path(path):
    """Check if path is safe (no directory traversal)."""
    # Block any path containing ..
    if ".." in path:
        return False
    return True


def detect_mime_type(file_path):
    """Detect MIME type based on file extension."""
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Default to text/html if unknown
    if mime_type is None:
        return "text/html"
    
    return mime_type


def response_200_ok(content, content_type, headers=None):
    """Return a 200 OK response."""
    return build_response(200, "OK", content, content_type, headers)


def response_400_bad_request(message):
    """Return a 400 Bad Request response."""
    return build_response(400, "Bad Request", message.encode('utf-8'), "text/plain")


def response_403_forbidden(message):
    """Return a 403 Forbidden response."""
    return build_response(403, "Forbidden", message.encode('utf-8'), "text/plain")


def response_404_not_found(message):
    """Return a 404 Not Found response."""
    return build_response(404, "Not Found", message.encode('utf-8'), "text/plain")


def response_405_method_not_allowed(message):
    """Return a 405 Method Not Allowed response."""
    return build_response(405, "Method Not Allowed", message.encode('utf-8'), "text/plain")


def response_500_internal_error(message):
    """Return a 500 Internal Server Error response."""
    return build_response(500, "Internal Server Error", message.encode('utf-8'), "text/plain")


