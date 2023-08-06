import os

from celery import shared_task

from ..controllers import jobs_monitor as ctrl


@shared_task(ignore_result=True)
def insert_jobs_from_all_projects(settings):
    ctrl.insert_jobs_from_all_projects(settings)


@shared_task(ignore_result=True)
def insert_jobs_from_project(settings, project_id):
    ctrl.insert_jobs_from_project(settings, project_id)


@shared_task(ignore_result=True)
def update(settings):
    ctrl.update(settings)


@shared_task(ignore_result=True)
def purge():
    ctrl.atomic_file_action(ctrl.purge)
