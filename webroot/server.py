import socket
import os

IP = '0.0.0.0'
PORT = 80


# We will store forbidden files and redirect rules:
FORBIDDEN_FILES = ['secret.html', 'private.txt']  # Add any files you consider forbidden
REDIRECTION_DICTIONARY = {
    'page1.html': 'page2.html'
}

# Default root file
DEFAULT_FILE = 'index.html'


def get_file_data(filename):
    """ Get data from file in binary mode """
    with open(filename, 'rb') as f:
        return f.read()


def get_content_type(filename):
    """ Return the correct Content-Type based on the file extension """
    _, ext = os.path.splitext(filename.lower())
    if ext in ['.html', '.txt']:
        return "text/html; charset=utf-8"
    elif ext == '.jpg':
        return "image/jpeg"
    elif ext == '.js':
        return "text/javascript; charset=UTF-8"
    elif ext == '.css':
        return "text/css"
    else:
        # If we don't recognize the type, default to text/html
        return "text/html; charset=utf-8"


def send_response(client_socket, status_code, status_message, body=b'', content_type=None):
    """ Send an HTTP response to the client """
    headers = f"HTTP/1.0 {status_code} {status_message}\r\n"
    if content_type:
        headers += f"Content-Type: {content_type}\r\n"
    headers += f"Content-Length: {len(body)}\r\n"
    headers += "\r\n"
    response = headers.encode('utf-8') + body
    client_socket.sendall(response)


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate a proper HTTP response and send to the client.
    Implement steps 8-10:
    - If resource == '', return index.html if exists.
    - Check if resource is in REDIRECTION_DICTIONARY (302 redirect).
    - Check if resource is forbidden (403).
    - If not found (404).
    - Otherwise (200) with appropriate Content-Type.
    """

    # Step 8: If resource is empty or '/', serve index.html
    if resource == '' or resource == '/':
        resource = DEFAULT_FILE

    # Remove leading slash if present
    if resource.startswith('/'):
        resource = resource[1:]

    # Step 10: Check if resource requires redirection
    if resource in REDIRECTION_DICTIONARY:
        # 302 Redirect
        new_location = REDIRECTION_DICTIONARY[resource]
        headers = (
            f"HTTP/1.0 302 Found\r\n"
            f"Location: /{new_location}\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        client_socket.sendall(headers.encode('utf-8'))
        return

    # Step 10: Check if resource is forbidden
    if resource in FORBIDDEN_FILES:
        # 403 Forbidden
        send_response(client_socket, "403", "Forbidden")
        return

    # Check if file exists
    if not os.path.isfile(resource):
        # 404 Not Found
        send_response(client_socket, "404", "Not Found")
        return

    # If file exists, read its content
    file_data = get_file_data(resource)
    content_type = get_content_type(resource)
    # 200 OK
    send_response(client_socket, "200", "OK", body=file_data, content_type=content_type)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns:
    - TRUE/FALSE: Whether it is a valid request we can understand
    - requested_resource: The requested URL (without leading '/')

    Now, if we don't understand the request (method not GET or bad version),
    we will return a signal that will lead us to return a 500 Internal Server Error.
    """
    lines = request.split('\r\n')
    if len(lines) < 1:
        return False, '', True  # not even a proper request line

    request_line = lines[0]
    parts = request_line.split(' ')
    if len(parts) != 3:
        return False, '', True  # invalid request line format

    method, requested_resource, version = parts

    # Check if method is GET
    if method != 'GET':
        # Not a GET request => return as not understood (will lead to 500 error)
        return False, '', True

    # Check HTTP version format
    if not version.startswith('HTTP/'):
        # Invalid version => return as not understood (500)
        return False, '', True

    # If requested_resource starts with '/'
    if requested_resource.startswith('/'):
        requested_resource = requested_resource[1:]

    # This is a valid GET request
    return True, requested_resource, False


def handle_client(client_socket):
    """
    Handles client requests:
    - receives the request
    - validates it
    - if valid GET request, handle it
    - If not understood request, return 500 Internal Server Error
    """
    print('Client connected')
    try:
        client_request = client_socket.recv(1024).decode('utf-8', errors='replace')
        if not client_request:
            print("Empty request received. Closing connection.")
            return

        valid_http, resource, internal_error = validate_http_request(client_request)
        if internal_error:
            # According to step 10, return a 500 Internal Server Error instead of closing.
            send_response(client_socket, "500", "Internal Server Error")
        elif valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
        else:
            # If not valid but not flagged as internal error, might be a scenario not previously described.
            # Just return 500 Internal Server Error as a fallback.
            send_response(client_socket, "500", "Internal Server Error")

    finally:
        print('Closing connection')
        client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen(10)
    print("Listening for connections on port %d" % PORT)

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received from', client_address)
        handle_client(client_socket)


if __name__ == "__main__":
    main()
