"""Offline tests: start the web server on a free port and call it like a browser would."""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def server():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    env = dict(os.environ, PORT=str(port), APP_VERSION="v9", PLATFORM="Test runner", AWS_REGION="ap-south-1")
    proc = subprocess.Popen([sys.executable, "app.py"], cwd=ROOT, env=env, stdout=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            urllib.request.urlopen(url + "/health", timeout=1)
            break
        except OSError:
            time.sleep(0.1)
    yield url
    proc.terminate()
    proc.wait()


def test_health(server):
    r = urllib.request.urlopen(server + "/health")
    assert r.status == 200
    assert json.loads(r.read()) == {"status": "healthy"}


def test_home_page_shows_runtime_details(server):
    page = urllib.request.urlopen(server + "/").read().decode()
    assert "Application version: v9" in page
    assert "Test runner" in page
    assert "ap-south-1" in page
    assert "{{" not in page


def test_unknown_path_is_404(server):
    with pytest.raises(urllib.error.HTTPError) as e:
        urllib.request.urlopen(server + "/nope")
    assert e.value.code == 404


def test_docker_image_only_copies_app_files():
    dockerfile = (ROOT / "Dockerfile").read_text()
    assert "COPY app.py index.html ./" in dockerfile
    assert "USER cloudadhar" in dockerfile
