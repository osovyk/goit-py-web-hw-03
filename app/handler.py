import urllib.parse
from http.server import BaseHTTPRequestHandler

from .storage import append_message
from .views import render, render_read, send_static


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr = urllib.parse.urlparse(self.path)

        if pr.path == "/":
            return render(self, "index.html")

        if pr.path in ("/message", "/message.html"):
            return render(self, "message.html")

        if pr.path == "/read":
            return render_read(self)

        if send_static(self, pr.path):
            return None

        return render(self, "error.html", status=404)

    def do_POST(self):
        pr = urllib.parse.urlparse(self.path)
        if pr.path != "/message":
            return render(self, "error.html", status=404)

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        parsed = urllib.parse.unquote_plus(raw.decode("utf-8"))
        pairs = [p for p in parsed.split("&") if "=" in p]
        data = dict(p.split("=", 1) for p in pairs)

        username = (data.get("username") or "").strip()
        message = (data.get("message") or "").strip()
        if username or message:
            append_message(username, message)

        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()
        return None
