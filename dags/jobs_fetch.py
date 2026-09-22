import os
import requests
import time
from pendulum import datetime
from airflow.sdk import dag, task
from include.source_config import load_config
from include.sources import PARSERS
from include.state import read_state_file, compare_new_jobs, write_json 

@task
def fetch_jobs(source):

    # 1. Fetch jobs from the API
    parser = PARSERS[source["ats"]] 
    response = requests.get(source["api_url"], headers=source.get("headers", {}))
    response.raise_for_status()    
    today_timestamp = time.strftime("%Y-%m-%d", time.localtime())
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "include/jobs")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"new_jobs_{source['company']}_{today_timestamp}.json")
    state_file_path = os.path.join(folder_path, f"state_{source['company']}.json")
    cleaned_data = parser(response, source)

    # 2. Safely read previous state using json
    existing_jobs = read_state_file(state_file_path)

    # 3. Identify new jobs using sets
    new_jobs = compare_new_jobs(existing_jobs,cleaned_data)

    print(f"Total jobs fetched today: {len(cleaned_data)}")
    print(f"New jobs detected: {len(new_jobs)}")

    # 4. Update report for new jobsS and write clean JSON to disk
    if not new_jobs:
        print("No new jobs found.")
    # write the new_jobs file report
    write_json(file_path,new_jobs)

    # 5. update the state file with the latest jobs
    write_json(state_file_path,cleaned_data)

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