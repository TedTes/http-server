"""
HTTP Router
Handles URL routing and maps paths to handler functions
"""

from utils import match_route


class Router:
    """
    Router class for registering and matching routes
    
    Routes are stored as:
    {
        'GET': [('/users', handler1), ('/users/:id', handler2)],
        'POST': [('/users', handler3)]
    }
    """
    def __init__(self):
        """Initialize empty route registry"""
        self.routes = {}
    
    def add_route(self, method, pattern, handler):
        """
        Register a route handler
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            pattern (str): URL pattern (/users/:id)
            handler (function): Function to handle the request
        """

        method = method.upper()
        
        if method not in self.routes:
            self.routes[method] = []
        
        self.routes[method].append((pattern, handler))

    
    def match(self, method, path):
        """
        Find matching route and extract parameters
        
        Args:
            method (str): HTTP method
            path (str): Request path
        
        Returns:
            tuple: (handler, params) or (None, None) if no match
        """
        method = method.upper()
        
        # No routes for this method
        if method not in self.routes:
            return (None, None)
        
        # Try each route pattern
        for pattern, handler in self.routes[method]:
            params = match_route(pattern, path)
            if params is not None:
                return (handler, params)
        
        # No match found
        return (None, None)