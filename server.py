"""
HTTP Server
Core TCP server that handles socket connections and HTTP processing
"""

import socket
import threading
from parser import parse_request
from response import Response
from router import Router


class HTTPServer:
    """
    HTTP Server using raw TCP sockets
    
    Handles incoming connections, parses HTTP, routes requests,
    and sends responses back to clients
    """

    def __init__(self, host='0.0.0.0', port=8080):
        """
        Initialize HTTP Server
        
        Args:
            host (str): Host to bind to (0.0.0.0 = all interfaces)
            port (int): Port to listen on
        """
        self.host = host
        self.port = port
        self.router = Router()
        self.running = False

    
    def route(self, method, pattern):
        """
        Decorator to register route handlers
        
        Usage:
            @app.route('GET', '/users/:id')
            def get_user(request):
                return Response.json({'id': request.params['id']})
        """
        def decorator(handler):
            self.router.add_route(method, pattern,handler)
            return handler
       
        return decorator
    

    def  handle_client(self, client_socket, address):
        """
        Handle individual client connection
        
        Args:
            client_socket: Socket connection to client
            address: Client address tuple (ip, port)
        """

        try:
            # Receive data from client (max 4096 bytes)
            raw_data = client_socket.recv(4096)
            
            if not raw_data:
                return  # Client closed connection

            
            # Parse HTTP request
            request = parse_request(raw_data)


            if request is None:
                # Bad request - send 400 error
                response = Response(400, "Bad Request")
                client_socket.sendall(response.to_bytes())
                return
            
            # Find matching route
            handler, params = self.router.match(request.method, request.path)


            if handler is None:
                # No route found - send 404
                response = Response(404, "Not Found")
            else:
                # Inject URL params into request
                request.params = params
                
                try:
                    # Call the handler function
                    response = handler(request)
                except Exception as e:
                    # Handler crashed - send 500 error
                    print(f"Error in handler: {e}")
                    response = Response(500, "Internal Server Error")

            client_socket.sendall(response.to_bytes())
            
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        
        finally:
            # Always close the connection
            client_socket.close()
    
    def start(self):
        """Start the HTTP server"""
        # Create TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow reusing address (useful for quick restarts)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to host and port
        server_socket.bind((self.host, self.port))
        
        # Listen for connections (backlog of 5)
        server_socket.listen(5)

        self.running = True
        print(f"🚀 HTTP Server running on http://{self.host}:{self.port}")
        print("Press Ctrl+C to stop")
        
        try:
            while self.running:
                # Accept incoming connection
                client_socket, address = server_socket.accept()
                print(f"📡 Connection from {address[0]}:{address[1]}")
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            self.running = False
        
        finally:
            server_socket.close()
            print("✅ Server stopped")