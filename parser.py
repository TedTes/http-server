"""
HTTP Request Parser
Parses raw HTTP request bytes into Request objects
"""

from request import Request

def parse_request(raw_data):
    """
    Parse raw HTTP request bytes into a Request object
    
    Args:
        raw_data (bytes): Raw HTTP request data
    
    Returns:
        Request: Parsed request object
        None: If parsing fails
    """
    try:
      request_text = raw_data.decode('utf-8')
    except UnicodeDecodeError: 
        return None
    
    lines = request_text.split('\r\n')

    if  not lines:
        return None
    
    parts = lines[0].split(' ');

    if  len(parts) != 3:
       return  None
    
    method , path, version = parts

    headers = {}

    i = 1

    while  i < len(lines) and  lines[i] != '':
        line = lines[i]
        if  ':' in line:

            key , value = line.split(':',1)
            headers[key.strip()] = value.strip()
        i+=1
    
    
    body_start = i + 1

    if body_start < len(lines):
        body = '\r\n'.join(lines[body_start:])
        body.encode('utf-8')
    else: 
        body = b''

    return Request(method, path, version, headers, body)