import mimetypes
from . import BASE_DIR, env
from .storage import read_all

STATIC_DIR = BASE_DIR / "static"


def render(handler, page_template: str, context: dict | None = None, status: int = 200):
    ctx = {"current_path": handler.path}
    if context:
        ctx.update(context)
    tpl = env.get_template(f"pages/{page_template}")
    html = tpl.render(**ctx)
    handler.send_response(status)
    handler.send_header("Content-type", "text/html; charset=utf-8")
    handler.end_headers()
    handler.wfile.write(html.encode("utf-8"))


def send_static(handler, path_str: str) -> bool:
    rel = path_str.lstrip("/")
    if rel.startswith("static/"):
        candidate = (BASE_DIR / rel).resolve()
    else:
        candidate = (STATIC_DIR / rel).resolve()

    if not (
        candidate.exists()
        and candidate.is_file()
        and str(candidate).startswith(str(BASE_DIR))
    ):
        return False

    mt = mimetypes.guess_type(str(candidate))[0] or "application/octet-stream"
    handler.send_response(200)
    handler.send_header("Content-type", mt)
    handler.end_headers()
    with open(candidate, "rb") as f:
        handler.wfile.write(f.read())
    return True


def render_read(handler):
    data = read_all()
    items = sorted(data.items(), key=lambda kv: kv[0], reverse=True)
    return render(handler, "read.html", {"items": items})
