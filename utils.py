import socket

def get_local_ip():
    """Gets the local IP address of the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"  # fallback to localhost if it can't determine the IP
    finally:
        s.close()
    return ip
