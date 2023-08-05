import contextlib
import json
import os
import tempfile
from multiprocessing.managers import SharedMemoryManager

import gitlab
from filelock import FileLock
from flasket import endpoint
from flasket.clients.gitlab import HookEvents, webhook


# TODO: Move to controller
def action_jobs_file(app, callback):
    # Get a unique ID from app.config
    key = app.config["UNIQUE_KEY"]
    filepath = os.path.join(tempfile.gettempdir(), f"gl-webhooks.jobs.{key}.json")
    lockfile = filepath + ".lock"

    with FileLock(lockfile):
        data = {}
        with contextlib.suppress(FileNotFoundError) as ctx:
            with open(filepath) as fd:
                data = json.load(fd)

        if callback:
            data = callback(data or {})
            with open(filepath, mode="w") as fd:
                json.dump(data, fd, indent=2, sort_keys=True)

        return data or {}


@endpoint
def monitor_purge(app, body):
    cfg = app.settings["gitlab"]

    gl = gitlab.Gitlab(cfg["url"], private_token=cfg["token"])

    def action(data):
        # purge finished states
        data = {k: v for k, v in data.items() if v["status"] not in ["failed", "success", "canceled"]}
        for k, v in data.items():
            try:
                job = gl.projects.get(v["project_id"], lazy=True).jobs.get(v["build_id"])
                v["status"] = job.status
            except:
                pass
        data = {k: v for k, v in data.items() if v["status"] not in ["failed", "success", "canceled"]}
        return data

    data = action_jobs_file(app, action)
    return data, 200


@webhook([HookEvents.JOB_HOOK])
def monitor(app, body):
    build_id = str(body["build_id"])
    build_status = body["build_status"]

    def action(data):
        if build_id not in data:
            data[build_id] = {}

        data[build_id]["build_id"] = int(build_id)
        data[build_id]["project_id"] = int(body["project_id"])

        last_status = data[build_id].get("status", "absent")

        if build_status in ["created"]:
            # purge finished states
            data[build_id]["status"] = build_status
            data = {k: v for k, v in data.items() if v["status"] not in ["failed", "success", "canceled"]}
        elif build_status in ["pending"] and last_status in ["absent", "created"]:
            data[build_id]["status"] = build_status
        elif build_status in ["running"] and last_status in ["absent", "created", "pending"]:
            data[build_id]["status"] = build_status
        elif build_status in ["failed", "success", "canceled"]:
            data[build_id]["status"] = build_status
        return data

    data = action_jobs_file(app, action)
    pending = len([True for v in data.values() if v["status"] == "pending"])
    running = len([True for v in data.values() if v["status"] == "running"])

    data["pending"] = pending
    data["running"] = running

    return data, 200
