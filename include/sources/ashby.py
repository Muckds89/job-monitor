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

    
    Qui dentro decidi tu:
      - dove sta la lista nella risposta, e cosa fai se non c'e'
      - come si chiamano i campi in questa sorgente
      - come costruisci l'url se la sorgente non te lo da'
      - come appiattisci la sede quando e' annidata o sporca
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
            "id": job.get("id"),
            "title": job.get("title"),
            "url": job.get("jobUrl"),
            "location": job.get("location")
        }
        cleaned_data.append(cleaned_job)


    return cleaned_data