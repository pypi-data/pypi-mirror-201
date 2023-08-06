import json
import os

from flasket import endpoint, exceptions
from flasket.clients.gitlab import HookEvents, webhook

from gl_webhooks.controllers import jobs_monitor as ctrl
from gl_webhooks.tasks import jobs_monitor as jobs


@webhook([HookEvents.JOB_HOOK])
def monitor(app, body):
    return ctrl.insert(app.settings, body), 200


@endpoint
def insert(app, body, project_id=0):
    if project_id == 0:
        jobs.insert_jobs_from_all_projects.s(app.settings).apply_async()
    else:
        jobs.insert_jobs_from_project.s(app.settings, project_id).apply_async()
    return {
        "status": 202,
        "title": "Accepted",
    }, 202


@endpoint
def update(app, body):
    jobs.update.s(app.settings).apply_async()
    return {
        "status": 202,
        "title": "Accepted",
    }, 202


@endpoint
def purge(app, body):
    jobs.purge.s().apply_async()
    return {
        "status": 202,
        "title": "Accepted",
    }, 202
