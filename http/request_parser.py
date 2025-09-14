"""
HTTP request parsing for RServer.
"""


def parse_http_request(request_text):
    """Parse HTTP request text into components.
    
    Returns:
        tuple: (method, path, version, headers, body)
    """
    lines = request_text.split('\r\n')
    
    if not lines:
        raise ValueError("Empty request")
    
    # Parse request line: "GET /path HTTP/1.1"
    request_line = lines[0].split(' ')
    if len(request_line) < 3:
        raise ValueError("Invalid request line")
    
    method = request_line[0]
    path = request_line[1]
    version = request_line[2]
    
    # Parse headers
    headers = {}
    body_start = len(lines)  # Default: no body
    
    for i, line in enumerate(lines[1:], 1):
        if line == '':  # Empty line = end of headers
            body_start = i + 1
            break
        
        if ':' not in line:
            continue  # Skip malformed header lines
            
        key, value = line.split(':', 1)
        headers[key.strip().lower()] = value.strip()
    
    # Body (if any)
    body = '\r\n'.join(lines[body_start:]) if body_start < len(lines) else ''
    
    return method, path, version, headers, body