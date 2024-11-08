import http.server
import socketserver
import os
from urllib.parse import urlparse
from pyx_parser import parse_pyx  # Ensure pyx_parser.py is in the same directory

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        # Serve a default .pyx file if the root path is requested
        if parsed_url.path == '/':
            self.handle_pyx('index.pyx')  # Assuming index.pyx is in the root
        elif parsed_url.path.endswith(".pyx"):
            self.handle_pyx(parsed_url.path.lstrip('/'))  # Serve .pyx files from root
        else:
            super().do_GET()

    def handle_pyx(self, file_path):
        try:
            # Check if the file exists in the root directory
            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return

            # Parse the .pyx file
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
httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
httpd.serve_forever()
