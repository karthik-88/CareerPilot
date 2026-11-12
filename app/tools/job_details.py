
from app.data.sample_jobs import jobs


def get_job_details(job_id):
    if not isinstance(job_id, int) or isinstance(job_id, bool) or job_id <= 0:
        raise ValueError("Job ID must be a positive integer")
    for job in jobs:
        if job["id"] == job_id:
            return job

    raise ValueError(f"Job with ID {job_id} not found")