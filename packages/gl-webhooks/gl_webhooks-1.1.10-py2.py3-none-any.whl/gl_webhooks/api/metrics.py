"""
/api/metrics endpoint
"""

from flasket import endpoint

from .webhooks.gitlab import jobs


@endpoint
def get(app, **_kwargs):
    """/api/metrics endpoint"""
    # Not returning anything is actually enough to at least have an up{job} metric
    retval = """
# HELP gl_webhooks_service_status Static value to imply service is up
# TYPE gl_webhooks_service_status gauge
gl_webhooks_service_status 1
"""

    # Metrics for api webhooks/gitlab/jobs.py
    data = jobs.atomic_file_action(app, None)
    pending = len([True for v in data.values() if v["status"] == "pending"])
    running = len([True for v in data.values() if v["status"] == "running"])
    created = len([True for v in data.values() if v["status"] == "created"])
    retval += """
# HELP gl_webhooks_jobs_count Count of jobs
# TYPE gl_webhooks_jobs_count gauge
"""
    retval += 'gl_webhooks_jobs_count{state="pending"} ' + str(pending) + "\n"
    retval += 'gl_webhooks_jobs_count{state="running"} ' + str(running) + "\n"
    retval += 'gl_webhooks_jobs_count{state="created"} ' + str(created) + "\n"

    return retval
