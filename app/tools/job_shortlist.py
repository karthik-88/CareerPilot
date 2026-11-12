from app.tools.job_details import get_job_details

shortlist = []


def add_to_shortlist(job_id):

    # Validate that the job exists
    get_job_details(job_id)

    # Prevent duplicate entries
    if job_id in shortlist:
        return "Job already shortlisted"

    # Add job ID
    shortlist.append(job_id)

    return "Job added successfully"

def view_shortlist():

    results = []

    for job_id in shortlist:
        job = get_job_details(job_id)
        results.append(job)

    return results

def remove_from_shortlist(job_id):
    get_job_details(job_id)

    if job_id not in shortlist:
        return "Job not found in shortlist"

    shortlist.remove(job_id)

    return "Job removed successfully"

