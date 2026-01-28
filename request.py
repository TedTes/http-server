"""
HTTP Request Object
Represents a parsed HTTP request with all its components
"""

import json
from utils import parse_query_string, parse_cookies


class Request:
    """
    HTTP Request object containing all request data
    
    Attributes:
        method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
        path (str): URL path without query string
        version (str): HTTP version (e.g., 'HTTP/1.1')
        headers (dict): Request headers (case-insensitive)
        query_params (dict): Parsed query string parameters
        body (bytes): Raw request body
        params (dict): URL parameters from route pattern
        cookies (dict): Parsed cookies
    """
    def __init__(self, method, path, version, headers, body=b''):
        """
        Initialize Request object
        
        Args:
            method (str): HTTP method
            path (str): Full path including query string
            version (str): HTTP version
            headers (dict): Request headers
            body (bytes): Raw request body (default empty)
        """
        self.method = method.upper()
        self.version = version
        self.headers = headers
        self.body = body
        self.params = {}
        if '?' in path:
            self.path, query_string = path.split('?', 1)
            self.query_params = parse_query_string(query_string)
        else:
            self.path = path
            self.query_params = {}
        cookie_header = self.headers.get('Cookie', '')
        self.cookies = parse_cookies(cookie_header)
    
    def get_header(self, name, default=None):
        """Get header value (case-insensitive)"""
        # Make headers case-insensitive
        for key, value in self.headers.items():
            if key.lower() == name.lower():
                return value
        return default
    
    def json(self):
        """Parse request body as JSON"""
        try:
            return json.loads(self.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    
    def __repr__(self):
        """String representation of Request for debugging"""
        return f"<Request {self.method} {self.path}>"
