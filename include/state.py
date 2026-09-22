import os
import json

def read_state_file(state_file_path):
    """
    Reads the state file and returns the existing jobs as a list of dictionaries.
    If the state file does not exist, returns an empty list.
    """
    if os.path.exists(state_file_path):
        with open(state_file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def compare_new_jobs(state_file_records: list[dict], adapter_records: list[dict])-> list[dict]:
    """
    compares the normalized records from the adapter and compares with the records already seen in the status file.
    returns the new records in the order they appear in adapter_records
    """
    # 1. set lookup is O(1), list would be O(n) per job
    existing_ids = {j["id"] for j in state_file_records}

    # 2. Identify new jobs using set
    new_jobs = [job for job in adapter_records if job["id"] not in existing_ids]

    return new_jobs

def write_json(state_file_path, output):
    """
    write the status file for the retrieved job
    """
    # update the state file with the latest jobs
    with open(state_file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)