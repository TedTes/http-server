"""
HTTP Server Utilities
Helper functions for URL parsing, MIME types, and HTTP status codes
"""
import re
from urllib.parse import unquote_plus


# HTTP Status Codes and their descriptions
STATUS_CODES = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    503: 'Service Unavailable'
}
# MIME types for common file extensions
MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.txt': 'text/plain',
    '': 'application/octet-stream'
}

def get_status_text(status_code):
    """Get the text description for an HTTP status code"""
    return STATUS_CODES.get(status_code, 'Unknown')

def get_mime_type(filename):
    """Determine MIME type from filename extension"""
    if '.' in filename:
        ext = '.' + filename.rsplit('.', 1)[1].lower()
        return MIME_TYPES.get(ext, 'application/octet-stream')
    return 'application/octet-stream'


def parse_query_string(query_string):
    """
    Parse URL query string into dictionary
    Example: "name=John&age=30" -> {'name': 'John', 'age': '30'}
    """
    params = {}
    if not query_string:
        return params
    
    for pair in query_string.split('&'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            params[unquote_plus(key)] = unquote_plus(value)
        else:
            params[unquote_plus(pair)] = ''
    
    return params



def parse_cookies(cookie_header):
    """Parse Cookie header into dictionary"""
    cookies = {}
    if not cookie_header:
        return cookies
    
    for cookie in cookie_header.split(';'):
        cookie = cookie.strip()
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies[key.strip()] = value.strip()
    
    return cookies


def match_route(pattern, path):
    """
    Match route pattern against URL path and extract parameters
    Pattern: /users/:id -> Path: /users/123 -> {'id': '123'}
    """
    # Convert :param to regex named groups
    regex_pattern = re.sub(r':([a-zA-Z_][a-zA-Z0-9_]*)', r'(?P<\1>[^/]+)', pattern)
    
    # Add start and end anchors
    regex_pattern = f'^{regex_pattern}$'
    
    # Try to match
    match = re.match(regex_pattern, path)
    
    if match:
        return match.groupdict()
    return None


def format_headers(headers_dict):
    """Format headers dictionary into HTTP header string"""
    lines = []
    for key, value in headers_dict.items():
        lines.append(f"{key}: {value}")
    return '\r\n'.join(lines)



def encode_response(status_code, headers, body):
    """Encode complete HTTP response into bytes"""
    # Convert body to bytes if string
    if isinstance(body, str):
        body = body.encode('utf-8')
    
    # Build status line
    status_text = get_status_text(status_code)
    status_line = f"HTTP/1.1 {status_code} {status_text}\r\n"
    
    # Build headers
    header_lines = format_headers(headers)
    
    # Combine: status line + headers + blank line + body
    response = status_line.encode('utf-8')
    response += header_lines.encode('utf-8')
    response += b'\r\n\r\n'
    response += body
    
    return response