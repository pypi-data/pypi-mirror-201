import contextlib
import json
import os
import tempfile
from multiprocessing.managers import SharedMemoryManager

import gitlab
from filelock import FileLock
from flasket import endpoint
from flasket.clients.gitlab import HookEvents, webhook

FINAL_STATES = ["failed", "success", "canceled", "skipped", "manual"]


# TODO: Move to controller
def atomic_file_action(app, callback):
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


# TODO: Move to controller
def purge_jobs(data):
    data = {k: v for k, v in data.items() if v["status"] not in FINAL_STATES}
    return data


# TODO: Move to controller
def insert_job(app, body):
    build_id = str(body["build_id"])
    build_status = body["build_status"]
    project_id = str(body["project_id"])

    cfg = app.settings["gitlab"]
    gl = gitlab.Gitlab(cfg["url"], private_token=cfg["token"])

    def action(data):
        if build_id not in data:
            data[build_id] = {}

        data[build_id]["build_id"] = int(build_id)
        data[build_id]["project_id"] = int(project_id)
        data[build_id]["status"] = build_status

        # Get a possible updated status
        if build_status not in FINAL_STATES:
            try:
                job = gl.projects.get(int(project_id), lazy=True).jobs.get(int(build_id))
                data[build_id]["status"] = job.status
            except:
                pass

        # Purge final states
        return purge_jobs(data)

    data = atomic_file_action(app, action)
    pending = len([True for v in data.values() if v["status"] == "pending"])
    running = len([True for v in data.values() if v["status"] == "running"])
    created = len([True for v in data.values() if v["status"] == "created"])

    data["pending"] = pending
    data["running"] = running
    data["created"] = created

    return data, 200


@endpoint
def monitor_purge(app, body):
    data = atomic_file_action(app, purge_jobs)
    return data, 200


@endpoint
def monitor_insert(app, body, project_id):
    data = {}

    cfg = app.settings["gitlab"]
    gl = gitlab.Gitlab(cfg["url"], private_token=cfg["token"])

    for job in gl.projects.get(project_id, lazy=True).jobs.list(iterator=True, scope=["running", "pending", "created"]):
        body = {
            "build_id": job.id,
            "build_status": job.status,
            "project_id": project_id,
        }
        data, _ = insert_job(app, body)

    if data:
        return data, 200
    else:
        return {}, 204


@endpoint
def monitor_update(app, body):
    cfg = app.settings["gitlab"]
    gl = gitlab.Gitlab(cfg["url"], private_token=cfg["token"])

    def action(data):
        for k, v in data.items():
            try:
                job = gl.projects.get(v["project_id"], lazy=True).jobs.get(v["build_id"])
                v["status"] = job.status
            except:
                pass
        return data

    data = atomic_file_action(app, action)
    return data, 200


@webhook([HookEvents.JOB_HOOK])
def monitor(app, body):
    return insert_job(app, body)
