
# HTTP Server

This project implements a simple HTTP server that supports basic functionality, including serving static files, handling HTTP GET requests, and supporting various HTTP status codes such as `200 OK`, `404 Not Found`, `403 Forbidden`, `302 Found`, and `500 Internal Server Error`. The server is implemented in Python using the `socket` module.

## Features

1. Handles HTTP GET requests.
2. Serves static files such as HTML, CSS, JavaScript, and images.
3. Supports Content-Type headers for different file types.
4. Handles the following HTTP status codes:
   - `200 OK`: File successfully served.
   - `404 Not Found`: File does not exist.
   - `403 Forbidden`: Access to certain files is restricted.
   - `302 Found`: Redirects to another resource.
   - `500 Internal Server Error`: For invalid or unrecognized requests.
5. Automatically serves `index.html` when the root (`/`) is requested.

## Prerequisites

1. Python 3.x installed on your machine.
2. A directory named `webroot` containing the static files to serve (e.g., HTML, CSS, JS, images).
3. Ensure the following files and folders are present in the `webroot` directory:
   - `index.html`
   - Subdirectories for `css`, `images`, `js`, and any other required files.

## Setup

1. Clone the repository or download the script.

## Usage

### Starting the Server

1. Open a terminal and navigate to the directory containing the server script.
2. Run the server using the command:
   ```
   python server.py
   ```
3. The server will start listening on `0.0.0.0:80`.

### Connecting to the Server

#### Using a Web Browser

1. Open a web browser.
2. Navigate to the server's address:
   ```
   http://127.0.0.1/<resource_name>
   ```
   Replace `<resource_name>` with the name of the file you want to access. For example:
   - To request the root (i.e., `index.html`):
     ```
     http://127.0.0.1/
     ```
   - To access a file (e.g., `page1.html`):
     ```
     http://127.0.0.1/page1.html
     ```
   - To access an image (e.g., `abstract.jpg`):
     ```
     http://127.0.0.1/images/abstract.jpg
     ```


## Troubleshooting

1. **Port Already in Use**:
   If port 80 is already in use, modify the `PORT` variable in the script to a different port (e.g., 8080). Update the URLs accordingly (e.g., `http://127.0.0.1:8080`).
