
from app.data.sample_jobs import jobs


def search_jobs(role, location):
    if not isinstance(role, str) or not role.strip():
        raise ValueError("Role must be a non-empty string")

    if not isinstance(location, str) or not location.strip():
        raise ValueError("Location must be a non-empty string")

    role = role.strip()
    location = location.strip()
    results = []

    for job in jobs:
        role_matches = role.lower() in job["role"].lower()
        location_matches = location.lower() in job["location"].lower()

        if role_matches and location_matches:
            results.append(job)

    return results
