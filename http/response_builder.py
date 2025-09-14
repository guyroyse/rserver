"""
HTTP response building for RServer.
"""


def build_response(status_code, status_text, content, content_type, headers=None):
    """Build a complete HTTP response.
    
    Args:
        status_code: HTTP status code (200, 404, etc.)
        status_text: HTTP status text ("OK", "Not Found", etc.)
        content: Response body content as bytes
        content_type: MIME type for Content-Type header
        headers: Additional headers as dict
    
    Returns:
        bytes: Complete HTTP response as bytes
    """
    if headers is None:
        headers = {}
    
    # Start with status line
    response_lines = [f"HTTP/1.1 {status_code} {status_text}"]
    
    # Add Content-Type and Content-Length
    response_lines.append(f"Content-Type: {content_type}")
    response_lines.append(f"Content-Length: {len(content)}")
    
    # Add additional headers
    for key, value in headers.items():
        response_lines.append(f"{key}: {value}")
    
    # Headers section as bytes
    headers_bytes = "\r\n".join(response_lines).encode('utf-8')
    headers_bytes += b"\r\n\r\n"  # Empty line + body separator
    
    # Combine headers + body
    return headers_bytes + content
