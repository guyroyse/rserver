"""
HTTP response building for RServer.
"""


def build_response(status_code, status_text, content, content_type="text/html", headers=None):
    """Build a complete HTTP response.
    
    Args:
        status_code: HTTP status code (200, 404, etc.)
        status_text: HTTP status text ("OK", "Not Found", etc.)
        content: Response body content
        content_type: MIME type for Content-Type header
        headers: Additional headers as dict
    
    Returns:
        str: Complete HTTP response
    """
    if headers is None:
        headers = {}
    
    # Start with status line
    response_lines = [f"HTTP/1.1 {status_code} {status_text}"]
    
    # Add Content-Type and Content-Length
    response_lines.append(f"Content-Type: {content_type}")
    response_lines.append(f"Content-Length: {len(content.encode('utf-8'))}")
    
    # Add additional headers
    for key, value in headers.items():
        response_lines.append(f"{key}: {value}")
    
    # Empty line separates headers from body
    response_lines.append("")
    
    # Add body
    response_lines.append(content)
    
    return "\r\n".join(response_lines)
