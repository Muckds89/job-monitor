[![CI](https://github.com/Muckds89/job-monitor/actions/workflows/tests.yml/badge.svg)](https://github.com/Muckds89/job-monitor/actions/workflows/tests.yml) 

# Overview

Scheduled Airflow pipeline that polls applicant tracking system APIs and reports new job postings

# Domain

**ATS** ATS stands for Application Tracking System, a service widely use today to manage, process and aquire applications for job posts

# Tech Stack

- **Airflow** a pipeline orchestration stack which allows to monitor, concatenate and organise tasks (DAGS) in a orderly manner thanks to a master process represanted by the **DAG definition file** combined with **Dynamic Task Mapping** (`.expand()`).
- **ASTRO CLI**
- **Docker**
- **Python**


# How it works

# Project structure

# Run it locally

# Run the tests

## Install only development dependencies (without airflow)

```bash
pip install -r requirements-dev.txt
python -m pytest --ignore=tests/dags
```

# Adding a source

- ***First step** in include/config.json append a new company dictionary to the "companies" list of dictionaries, for example:
```json
 {
    "company": "IQGeo",
    "api_url": "https://iqgeo.bamboohr.com/careers/list",
    "ats": "bamboohr"
}
```
- **Second step** build an adapter .py file to normalise the response from the ATS in include/sources

- **Third step** write a test in tests/ and test it with pytest manually. Also ther eis an automated CI workflow that triggers for every push/pull_request.

# Design decisions


# Status/ Next steps

In progress