import html
import json
import os
import socket
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


PORT = int(os.getenv("PORT", "8080"))
TEMPLATE = Path(__file__).with_name("index.html").read_text(encoding="utf-8")

# ECS sets this inside every task. It's a local URL that returns real details about the running task.
METADATA_URI = os.getenv("ECS_CONTAINER_METADATA_URI_V4")
_task_details = None


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=2) as response:
        return json.loads(response.read())


def ecs_details():
    """Read the ECS task metadata endpoint once. Returns {} when not running on ECS."""
    global _task_details
    if _task_details is not None:
        return _task_details
    if not METADATA_URI:
        _task_details = {}
        return _task_details
    try:
        task = fetch_json(METADATA_URI + "/task")
        container = fetch_json(METADATA_URI)
    except (OSError, ValueError):
        return {}

    ips = [ip for net in container.get("Networks", []) for ip in net.get("IPv4Addresses", [])]
    limits = task.get("Limits", {})
    _task_details = {
        "Cluster": task.get("Cluster", "").split("/")[-1],
        "Task ID": task.get("TaskARN", "").split("/")[-1],
        "Task definition": f"{task.get('Family', '')}:{task.get('Revision', '')}",
        "Image": container.get("Image", ""),
        "Availability Zone": task.get("AvailabilityZone", ""),
        "Private IP": ", ".join(ips),
        "CPU / Memory": f"{limits.get('CPU', '?')} vCPU / {limits.get('Memory', '?')} MB",
    }
    return _task_details


def platform_name(details):
    if os.getenv("PLATFORM"):
        return os.getenv("PLATFORM")
    if os.getenv("AWS_EXECUTION_ENV") == "AWS_ECS_FARGATE":
        return "Amazon ECS on AWS Fargate"
    if details:
        return "Amazon ECS"
    return "Local Docker container"


def runtime_rows():
    details = ecs_details()
    rows = {"Running on": platform_name(details)}
    rows.update(details)
    rows["Container hostname"] = socket.gethostname()
    rows["AWS Region"] = os.getenv("AWS_REGION", "not on AWS")
    return "\n".join(
        f"      <p>{html.escape(name)}: <code>{html.escape(str(value))}</code></p>"
        for name, value in rows.items() if value
    )


class RequestHandler(BaseHTTPRequestHandler):
    def send_content(self, status, content_type, body):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/health":
            self.send_content(200, "application/json", json.dumps({"status": "healthy"}))
            return

        if self.path != "/":
            self.send_content(404, "text/plain", "Not found")
            return

        page = TEMPLATE.replace("{{APP_VERSION}}", html.escape(os.getenv("APP_VERSION", "v1")))
        page = page.replace("{{RUNTIME}}", runtime_rows())
        self.send_content(200, "text/html; charset=utf-8", page)

    def log_message(self, message_format, *args):
        print(json.dumps({"client": self.client_address[0], "request": message_format % args}), flush=True)


if __name__ == "__main__":
    print(f"App listening on port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), RequestHandler).serve_forever()
