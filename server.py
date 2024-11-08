import http.server
import socketserver
import os
from urllib.parse import urlparse
from pyx_parser import parse_pyx  

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)


        if parsed_url.path == '/':
            self.handle_pyx('index.pyx')  
        elif parsed_url.path.endswith(".pyx"):
            self.handle_pyx(parsed_url.path.lstrip('/'))  
        else:
            super().do_GET()

    def handle_pyx(self, file_path):
        try:
            
            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")
                return


            response_content = parse_pyx(file_path)

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            self.wfile.write(response_content.encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error processing file: {str(e)}".encode('utf-8'))

PORT = 8000
Handler = MyRequestHandler
httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
httpd.serve_forever()
