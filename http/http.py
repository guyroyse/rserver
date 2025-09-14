"""
RServer HTTP-like request handling.
"""

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
        
        # Return response as bytes
        return response.encode('utf-8')
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return response_500_internal_error(str(e)).encode('utf-8')


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
    
    return response_200_ok(html_content, "text/html")


def response_200_ok(content, content_type="text/html", headers=None):
    """Return a 200 OK response."""
    return build_response(200, "OK", content, content_type, headers)


def response_400_bad_request(message):
    """Return a 400 Bad Request response."""
    return build_response(400, "Bad Request", message, "text/plain")


def response_405_method_not_allowed(message):
    """Return a 405 Method Not Allowed response."""
    return build_response(405, "Method Not Allowed", message, "text/plain")


def response_500_internal_error(message):
    """Return a 500 Internal Server Error response."""
    return build_response(500, "Internal Server Error", message, "text/plain")
