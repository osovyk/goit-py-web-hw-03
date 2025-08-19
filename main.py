from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Type
from app.handler import HttpHandler


def run(host: str = "", port: int = 3000):
    handler: Type[BaseHTTPRequestHandler] = HttpHandler
    httpd = HTTPServer((host, port), handler)
    print(f"Serving on http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run()
