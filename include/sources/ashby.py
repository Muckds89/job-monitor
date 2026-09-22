# include/sources/ashby.py

import os
import json
import time


def parse(response, source):
    """
    response: the object returned by requests.get(url) for this source
    source:   the configuration dictionary for this company

    Returns: a list of dictionaries in the normalized format,
             i.e., id, title, url, location.

    Inside this function, you can decide:
        - where the list of jobs is located in the response, and what to do if it's not present
        - what the field names are in this source
        - how to construct the URL if the source doesn't provide it
        - how to flatten the location if it's nested or messy

     """

    # retrieve the ats from the source configuration

    data = response.json()
    if "jobs" not in data:
        raise Exception(f"Unexpected response from API: {data}")
    fetched_jobs = data.get("jobs", [])

    # normalize the data into a list of dictionaries with the required fields
    cleaned_data = []
    for job in fetched_jobs:
        cleaned_job = {
            "id": str(job.get("id")),
            "title": job.get("title"),
            "url": job.get("jobUrl"),
            "location": job.get("location")
        }
        cleaned_data.append(cleaned_job)


    return cleaned_data