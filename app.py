"""
Demo HTTP Server Application
Example showing how to use the HTTP server
"""

from server import HTTPServer
from response import Response

# Create server instance
app = HTTPServer(host='0.0.0.0', port=8080)


# Route 1: Simple homepage
@app.route('GET', '/')
def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>HTTP Server</title></head>
    <body>
        <h1>🚀 HTTP Server from Scratch!</h1>
        <p>Built with Python sockets, no frameworks!</p>
        <a href="/users">View Users</a>
    </body>
    </html>
    """
    return Response.html(html)


# Route 2: JSON API endpoint
@app.route('GET', '/api/status')
def api_status(request):
    return Response.json({
        'status': 'running',
        'version': '1.0',
        'message': 'Server is healthy'
    })


# Route 3: URL parameters
@app.route('GET', '/users/:id')
def get_user(request):
    user_id = request.params['id']
    return Response.json({
        'id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com'
    })



# Route 4: Query parameters
@app.route('GET', '/search')
def search(request):
    query = request.query_params.get('q', 'nothing')
    page = request.query_params.get('page', '1')
    
    return Response.json({
        'query': query,
        'page': page,
        'results': ['result1', 'result2', 'result3']
    })


# Route 5: POST request with JSON body
@app.route('POST', '/users')
def create_user(request):
    data = request.json()
    
    return Response.json({
        'message': 'User created',
        'user': data
    }, status=201)



# Route 6: Plain text response
@app.route('GET', '/ping')
def ping(request):
    return Response.text('pong')


# Start the server
if __name__ == '__main__':
    app.start()