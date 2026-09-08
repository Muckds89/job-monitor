import json
import os
import requests
import time
from pendulum import datetime
from airflow.sdk import dag, task
from include.source_config import load_config
from include.sources import PARSERS
import sys

@task
def fetch_jobs(source: str = "example_source"):

    # 1. Fetch jobs from the API
    parser = PARSERS[source["ats"]] 
    response = requests.get(source["api_url"], headers=source.get("headers", {}))
    today_timestamp = time.strftime("%Y-%m-%d", time.localtime())
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "include/jobs")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"new_jobs_{source['ats']}_{today_timestamp}.json")
    state_file_path = os.path.join(folder_path, f"state_{source['ats']}.json")
    response.raise_for_status()    
    cleaned_data = parser(response, source)

    # 2. Safely read previous state using json
    if os.path.exists(state_file_path):
        with open(state_file_path, "r", encoding="utf-8") as f:
            existing_jobs = json.load(f)
    else:
        existing_jobs = []

    # 3. Create set of existing IDs for fast O(1) deduplication
    existing_ids = {j["id"] for j in existing_jobs}

    # 4. Identify new jobs using sets
    new_jobs = [job for job in cleaned_data if job["id"] not in existing_ids]

    print(f"Total jobs fetched today: {len(cleaned_data)}")
    print(f"New jobs detected: {len(new_jobs)}")

    # 5. Update state and write clean JSON to disk
    if new_jobs:
        updated_jobs = existing_jobs + new_jobs
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(updated_jobs, f, indent=2)
        print(f"Saved {len(new_jobs)} new jobs to {file_path}")
    else:
        print("No new jobs found.")

    # update the state file with the latest jobs
    with open(state_file_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2)

    return new_jobs

# Define the basic parameters of the DAG, like schedule and start_date
@dag(
    start_date=datetime(2026, 9, 5),
    schedule="@daily",
    doc_md=__doc__,
    default_args={"owner": "Muckds", "retries": 3},
    tags=["example"],
)
def fetch_jobs_dag():
    sources = load_config()
    fetch_jobs.expand(source=sources)
    # You can add more tasks here to process new_jobs if needed

fetch_jobs_dag = fetch_jobs_dag()