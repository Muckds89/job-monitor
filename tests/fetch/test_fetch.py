import json
import os
import requests
import time

today_timestamp = time.strftime("%Y-%m-%d", time.localtime())
folder_path = os.path.join(os.path.dirname(__file__), "new_jobs")
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, f"new_jobs_{today_timestamp}.json")

# 1. Fetch current jobs from REST API
url = "https://api.ashbyhq.com/posting-api/job-board/mapbox"
response = requests.get(url)
data = response.json()
fetched_jobs = data.get("jobs", [])

# 2. Safely read previous state using json
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
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