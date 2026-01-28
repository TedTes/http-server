"""
HTTP Response Builder
Provides easy ways to create HTTP responses
"""

import json
from utils import get_status_text, get_mime_type


class Response:
    """
    HTTP Response object for building responses
    
    Attributes:
        status_code (int): HTTP status code (200, 404, etc.)
        headers (dict): Response headers
        body (bytes): Response body content
    """
    def __init__(self, status_code=200, body='', headers=None):
        """
        Initialize Response object
        
        Args:
            status_code (int): HTTP status code (default 200)
            body (str or bytes): Response body
            headers (dict): Custom headers
        """
        self.status_code = status_code
        self.headers = headers or {}
        
        # Convert body to bytes if string
        if isinstance(body, str):
            self.body = body.encode('utf-8')
        else:
            self.body = body
        
        # Auto-set Content-Length
        self.headers['Content-Length'] = str(len(self.body))

    def to_bytes(self):
        """Convert response to raw HTTP bytes"""
        # Status line
        status_text = get_status_text(self.status_code)
        status_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n"
        
        # Headers
        header_lines = []
        for key, value in self.headers.items():
            header_lines.append(f"{key}: {value}\r\n")
        
        # Combine all parts
        response = status_line.encode('utf-8')
        response += ''.join(header_lines).encode('utf-8')
        response += b'\r\n'  # Blank line separates headers from body
        response += self.body
        
        return response
        
    @staticmethod
    def json(data, status=200):
        """Create a JSON response"""
        body = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        return Response(status, body, headers)
    

    @staticmethod
    def html(content, status=200):
        """Create an HTML response"""
        headers = {'Content-Type': 'text/html; charset=utf-8'}
        return Response(status, content, headers)

    @staticmethod
    def text(content, status=200):
        """Create a plain text response"""
        headers = {'Content-Type': 'text/plain; charset=utf-8'}
        return Response(status, content, headers)
    
    @staticmethod
    def redirect(location, status=302):
        """Create a redirect response"""
        headers = {'Location': location}
        return Response(status, '', headers)
    