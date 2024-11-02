from http.server import SimpleHTTPRequestHandler
import socketserver
from file_handler import upload_file, list_files_for_download, serve_file
from utils import get_local_ip
import os

PORT = 8000
DIRECTORY = "shared_files"
TEMPLATE_PATH = r"templates\index.html"

# Ensure the directory exists
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

class FileServerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Display the main page with upload form and file list
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(list_files_for_download(DIRECTORY, TEMPLATE_PATH).encode("utf-8"))
        elif self.path.startswith('/files/'):
            # Serve a file for download
            serve_file(self, DIRECTORY, self.path)

    def do_POST(self):
        # Handle file upload
        upload_file(self, DIRECTORY)

# Start the server with the local IP
if __name__ == "__main__":
    local_ip = get_local_ip()
    handler = FileServerHandler
    httpd = socketserver.TCPServer(("", PORT), handler)

    print(f"Serving at http://{local_ip}:{PORT}")
    print("Press Ctrl+C to stop the server.")
    
    httpd.serve_forever()
