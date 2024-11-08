import http.server
import socketserver
import os
from urllib.parse import urlparse
import subprocess
from pyx_parser import parse_pyx  # This is your custom parser function

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        # Serve .pyx files
        if parsed_url.path.endswith(".pyx"):
            self.handle_pyx(parsed_url.path)
        else:
            super().do_GET()

    def handle_pyx(self, path):
        try:
            # Set the path to the pyx file (could be in templates/ directory)
            file_path = os.path.join('templates', path.lstrip('/'))

            # Check if file exists
            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return

            # Parse the .pyx file (you can adjust the parsing behavior as needed)
            response_content = parse_pyx(file_path)

            # Send HTTP response headers
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Send parsed content as response
            self.wfile.write(response_content.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error processing file: {str(e)}".encode('utf-8'))


# Set the port and create the server
PORT = 8000
Handler = MyRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
httpd.serve_forever()
import http.server
import socketserver
import os
from urllib.parse import urlparse
import subprocess
from pyx_parser import parse_pyx  # This is your custom parser function

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        # Serve .pyx files
        if parsed_url.path.endswith(".pyx"):
            self.handle_pyx(parsed_url.path)
        else:
            super().do_GET()

    def handle_pyx(self, path):
        try:
            # Set the path to the pyx file (could be in templates/ directory)
            file_path = os.path.join('templates', path.lstrip('/'))

            # Check if file exists
            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return

            # Parse the .pyx file (you can adjust the parsing behavior as needed)
            response_content = parse_pyx(file_path)

            # Send HTTP response headers
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            # Send parsed content as response
            self.wfile.write(response_content.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error processing file: {str(e)}".encode('utf-8'))


# Set the port and create the server
PORT = 8000
Handler = MyRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
httpd.serve_forever()
