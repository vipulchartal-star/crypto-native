#!/usr/bin/env python3

import os
import subprocess
import threading
import time
from pathlib import Path

from flask import Flask, jsonify, send_file, url_for


ROOT_DIR = Path(__file__).resolve().parent
WORK_ROOT = Path(os.environ.get("WORK_ROOT", "/tmp/render-apk-builder"))
ARTIFACTS_DIR = WORK_ROOT / "artifacts"
BUILD_SCRIPT = ROOT_DIR / "build_android.sh"

app = Flask(__name__)
build_lock = threading.Lock()
latest_artifact = {"path": None, "built_at": None}


def artifact_payload(path: Path) -> dict:
    return {
        "artifact": path.name,
        "download_url": url_for("download_artifact", name=path.name, _external=True),
        "size_bytes": path.stat().st_size,
        "built_at": latest_artifact["built_at"],
    }


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "render-apk-builder"})


@app.post("/build")
def build():
    if not build_lock.acquire(blocking=False):
        return jsonify({"ok": False, "error": "build already running"}), 409

    try:
        started = time.time()
        result = subprocess.run(
            [str(BUILD_SCRIPT)],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=3600,
            env=os.environ.copy(),
        )
        if result.returncode != 0:
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": "build failed",
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    }
                ),
                500,
            )

        artifact_path = Path(result.stdout.strip().splitlines()[-1])
        latest_artifact["path"] = artifact_path
        latest_artifact["built_at"] = int(started)
        payload = artifact_payload(artifact_path)
        payload["ok"] = True
        payload["stdout"] = result.stdout
        return jsonify(payload)
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "build timed out"}), 504
    finally:
        build_lock.release()


@app.get("/latest")
def latest():
    path = latest_artifact["path"]
    if path is None or not path.exists():
        return jsonify({"ok": False, "error": "no artifact built yet"}), 404
    payload = artifact_payload(path)
    payload["ok"] = True
    return jsonify(payload)


@app.get("/artifacts/<name>")
def download_artifact(name: str):
    artifact_path = ARTIFACTS_DIR / name
    if not artifact_path.exists():
        return jsonify({"ok": False, "error": "artifact not found"}), 404
    return send_file(artifact_path, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
