import contextlib
import json
import os
import tempfile

from filelock import FileLock

from ..clients.gitlab import gitlab

FINAL_STATES = ["failed", "success", "canceled", "skipped", "manual"]


def atomic_file_action(callback):
    filepath = os.path.join(tempfile.gettempdir(), f"gl-webhooks.jobs-monitor.json")
    lockfile = filepath + ".lock"

    if callback:
        lock = FileLock(lockfile)
    else:
        lock = contextlib.nullcontext()

    with lock:
        data = {}
        with contextlib.suppress(FileNotFoundError) as ctx:
            with open(filepath) as fd:
                data = json.load(fd)

        if callback:
            data = callback(data or {})
            with open(filepath, mode="w") as fd:
                json.dump(data, fd, indent=2, sort_keys=True)

        return data or {}


def insert(settings, body):
    gl = gitlab(settings)

    build_id = str(body["build_id"])
    build_status = body["build_status"]
    project_id = str(body["project_id"])

    def action(data):
        if build_id not in data:
            data[build_id] = {}

        data[build_id]["build_id"] = int(build_id)
        data[build_id]["project_id"] = int(project_id)
        data[build_id]["status"] = build_status
        data[build_id]["web_url"] = body.get("web_url")

        # Get a possible updated status
        if build_status not in FINAL_STATES:
            try:
                job = gl.projects.get(int(project_id), lazy=True).jobs.get(int(build_id))
                data[build_id]["status"] = job.status
                data[build_id]["web_url"] = job.web_url
            except:
                pass

        # Purge final states
        return purge(data)

    data = atomic_file_action(action)
    pending = len([True for v in data.values() if v["status"] == "pending"])
    running = len([True for v in data.values() if v["status"] == "running"])
    created = len([True for v in data.values() if v["status"] == "created"])

    data["pending"] = pending
    data["running"] = running
    data["created"] = created
    return data


def insert_jobs_from_project(settings, project_id):
    gl = gitlab(settings)

    try:
        for job in gl.projects.get(project_id, lazy=True).jobs.list(
            iterator=True,
            scope=["created", "running", "pending"],
        ):
            body = {
                "build_id": job.id,
                "build_status": job.status,
                "project_id": project_id,
                "web_url": job.web_url,
            }
            insert(settings, body)
    except:
        pass


def insert_jobs_from_all_projects(settings):
    gl = gitlab(settings)
    for project in gl.projects.list(iterator=True):
        insert_jobs_from_project(settings, project.id)


def update(settings):
    gl = gitlab(settings)

    def action(data):
        for k, v in data.items():
            try:
                job = gl.projects.get(v["project_id"], lazy=True).jobs.get(v["build_id"])
                v["status"] = job.status
            except:
                pass
        return data

    return atomic_file_action(action)


def purge(data):
    return {k: v for k, v in data.items() if v["status"] not in FINAL_STATES}
