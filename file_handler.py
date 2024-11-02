import os
from urllib.parse import unquote
from http.server import SimpleHTTPRequestHandler

def load_template(filename):
    """Loads an HTML template from the templates directory."""
    with open(filename, 'r') as file:
        return file.read()

def list_files_for_download(directory, template_path):
    """Generates HTML for listing available files for download based on a template."""
    html_template = load_template(template_path)
    
    file_links = ""
    for filename in os.listdir(directory):
        file_links += f'<li><a href="/files/{filename}" download>{filename}</a></li>'
    
    # Insert the file links into the HTML template
    html_content = html_template.replace('<!-- File links will be dynamically inserted here -->', file_links)
    return html_content

def serve_file(handler, directory, path):
    """Serves a specific file for download."""
    filename = unquote(path[len('/files/'):])
    handler.path = os.path.join(directory, filename)
    return SimpleHTTPRequestHandler.do_GET(handler)

def upload_file(handler, directory):
    """Handles file upload and saves it in the specified directory."""
    content_length = int(handler.headers['Content-Length'])
    field_data = handler.rfile.read(content_length)
    
    filename = handler.headers.get("Filename")  # Expecting a custom header with filename
    if filename:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'wb') as f:
            f.write(field_data)
        
        handler.send_response(200)
        handler.send_header("Content-type", "text/plain")
        handler.end_headers()
        handler.wfile.write(b"File uploaded successfully")
    else:
        handler.send_response(400)
        handler.send_header("Content-type", "text/plain")
        handler.end_headers()
        handler.wfile.write(b"Filename not provided")
