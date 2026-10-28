"""Offline tests: start the web server on a free port and call it like a browser would."""
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

FAKE_TASK = {
    "Cluster": "arn:aws:ecs:ap-south-1:123456789012:cluster/cloudadhar-cluster",
    "TaskARN": "arn:aws:ecs:ap-south-1:123456789012:task/cloudadhar-cluster/abc123",
    "Family": "from-code-to-cloud",
    "Revision": "2",
    "AvailabilityZone": "ap-south-1a",
    "Limits": {"CPU": 0.25, "Memory": 512},
}
FAKE_CONTAINER = {
    "Image": "123456789012.dkr.ecr.ap-south-1.amazonaws.com/from-code-to-cloud:v2",
    "Networks": [{"IPv4Addresses": ["172.31.5.10"]}],
}


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_app(extra_env):
    port = free_port()
    env = {k: v for k, v in os.environ.items() if k not in ("PLATFORM", "AWS_EXECUTION_ENV", "ECS_CONTAINER_METADATA_URI_V4")}
    env.update(PORT=str(port), **extra_env)
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + "/health", timeout=1)
            break
        except OSError:
            time.sleep(0.1)
    return proc, url


@pytest.fixture(scope="module")
def local_app():
    proc, url = start_app({"APP_VERSION": "v9"})
    yield url
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="module")
def ecs_app():
    class Metadata(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps(FAKE_TASK if self.path.endswith("/task") else FAKE_CONTAINER).encode()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    metadata = HTTPServer(("127.0.0.1", 0), Metadata)
    threading.Thread(target=metadata.serve_forever, daemon=True).start()
    proc, url = start_app({
        "APP_VERSION": "v2",
        "AWS_REGION": "ap-south-1",
        "AWS_EXECUTION_ENV": "AWS_ECS_FARGATE",
        "ECS_CONTAINER_METADATA_URI_V4": f"http://127.0.0.1:{metadata.server_port}/v4/abc",
    })
    yield url
    proc.terminate()
    proc.wait()
    metadata.shutdown()


def test_health(local_app):
    r = urllib.request.urlopen(local_app + "/health")
    assert r.status == 200
    assert json.loads(r.read()) == {"status": "healthy"}


def test_local_page(local_app):
    page = urllib.request.urlopen(local_app + "/").read().decode()
    assert "Application version: v9" in page
    assert "Running on: <code>Local Docker container</code>" in page
    assert "Cluster:" not in page
    assert "{{" not in page


def test_ecs_page_shows_real_task_details(ecs_app):
    page = urllib.request.urlopen(ecs_app + "/").read().decode()
    assert "Application version: v2" in page
    assert "Running on: <code>Amazon ECS on AWS Fargate</code>" in page
    assert "Cluster: <code>cloudadhar-cluster</code>" in page
    assert "Task ID: <code>abc123</code>" in page
    assert "Task definition: <code>from-code-to-cloud:2</code>" in page
    assert "from-code-to-cloud:v2</code>" in page
    assert "Availability Zone: <code>ap-south-1a</code>" in page
    assert "Private IP: <code>172.31.5.10</code>" in page
    assert "CPU / Memory: <code>0.25 vCPU / 512 MB</code>" in page
    assert "AWS Region: <code>ap-south-1</code>" in page


def test_unknown_path_is_404(local_app):
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(local_app + "/nope")
    assert e.value.code == 404


def test_docker_image_only_copies_app_files():
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "COPY app.py index.html ./" in dockerfile
    assert "USER appuser" in dockerfile
