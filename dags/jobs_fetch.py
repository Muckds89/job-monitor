import json
import os
import requests
import time
from pendulum import datetime
from airflow.sdk import dag, task

@task
def fetch_jobs():
    today_timestamp = time.strftime("%Y-%m-%d", time.localtime())
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "include/jobs")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"new_jobs_{today_timestamp}.json")
    state_file_path = os.path.join(folder_path, "state.json")



    # 1. Fetch current jobs from REST API
    url = "https://api.ashbyhq.com/posting-api/job-board/mapbox"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    if "jobs" not in data:
        raise Exception(f"Unexpected response from API: {data}")
    fetched_jobs = data.get("jobs", [])

    # 2. Safely read previous state using json
    if os.path.exists(state_file_path):
        with open(state_file_path, "r", encoding="utf-8") as f:
            existing_jobs = json.load(f)
    else:
        existing_jobs = []

    # 3. Create set of existing IDs for fast O(1) deduplication
    existing_ids = {j["id"] for j in existing_jobs}

    # 4. Identify new jobs using sets
    new_jobs = [job for job in fetched_jobs if job["id"] not in existing_ids]

    print(f"Total jobs fetched today: {len(fetched_jobs)}")
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
        json.dump(fetched_jobs, f, indent=2)

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
    new_jobs = fetch_jobs()
    # You can add more tasks here to process new_jobs if needed

fetch_jobs_dag = fetch_jobs_dag()