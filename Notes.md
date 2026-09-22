# Notes on Architecture and Orchestration (Job Monitor with Airflow & Astro CLI)

## 1. Context
This project demonstrates the practical utility of orchestration and why it is the industry standard in Data Engineering. The goal is to understand the core architectural advantages of orchestrating tasks instead of chaining custom scripts in sequence.

In this project, I explore fundamental concepts:
- **Scheduling & Triggering**
- **Idempotency & Deduplication**
- **Alerting & Failure Management**
- **Containerization (Docker / Astro CLI)**

The target system is a lightweight **Job Monitor** that polls public ATS endpoints (Ashby, Lever, Greenhouse) daily, computes the diff against historical data, and sends alerts for new job posts.

---

## 2. Parallelism: Previous NTM Project (Bluesky) vs. Airflow

### The NTM System (Past)
- **Monitoring:** A `monitor.sh` script continuously checked input folders. When new flight tiles were uploaded, a `diff` command detected unprocessed tiles.
- **Task Generation:** A master Bash script generated a list of parameterized command-line calls. Each line invoked a script processing a single tile (creating a `.vrt` with adjacent buffer tiles, reprojecting, resampling, and masking).
- **State Tracking:** Checked directly on the filesystem based on output files presence.
- **Technology Stack:** Pure Bash/Shell scripts. While functional for local execution, relying solely on Bash for pipeline orchestration leads to fragile error handling, lack of centralized visibility, and maintenance bottlenecks.

### The Job Monitor in Airflow (Present)
- **Data Ingestion:** We poll target ATS endpoints (e.g., Ashby's public REST API at `https://api.ashbyhq.com/posting-api/job-board/<company>`) using Python `requests`.
- **Payload Structure:** The response is a JSON payload. We extract the list of jobs from the `jobs` key. We raise the response status and then we check inside the payload for 'jobs' key. However, in case the 'job' key is there but the value is a null list (maybe the ATS servise changed internally and write in 'job_posting' key) we need to raise an error. In case of an empty 'jobs' value list instead, we need to validate against the previous status as if there is a sudden drop of number of jobs that indicate a potential issue. an empty job list could be legit in case there are no job posting. **Identification & Diffing:** Each job contains a unique `id` (e.g., UUID string). New job postings are identified by computing the set difference between today's IDs and yesterday's stored IDs:
  `new_jobs = set(today_ids) - set(yesterday_ids)`. There are 2 different approches to finding new job posts, one is to have a snapshot of today's job post, while the alternative is to retrieve the subset of all the ids which were never seen. The project opted for the latter, so if a job gets canceled and republished shortly after ( a practice known a "ghost jobs", where companies keep the opening indefinitive hopen to show they are hiring while they don't have the headcount). The aim is to get genuine new job. The downside of this approach is to ignore genuine republications (maybe because the company couldn't find ideals candidates), but in my experience that is a small minority and the general practice is indefinite openings.
- **Technology Stack:** Python & Apache Airflow. Python is the industry standard for modern data orchestration because it provides native data structures (`set`, `dict`), robust networking libraries (`requests`), and seamless integration with Airflow's scheduling, retry mechanisms, and observability features.
- **Normalisation**. different ATS response give different payload service. the task was designed to normailise response for each  type of response. for example Ashby and bamboohr might have the same identifier 'id' but different fields names for the same concept (ashby use 'title' while bamboohr uses 'jobOpeningName'). Morevover, the same response might be incoherent with location information contained in different place on two different job ids.
A discarted solution is to hardcode a dictionary for each filed with key value depending on the ats type. that will be to costly to maintain with several dictinaries to maintan (one for each field).
The opted solution was to build a data mapper (or adapter) to translate the json raw data to something normalise that the application can use with a clear and coherent internal structure. the process:
-- **Define the destination model**: given the large number of fields contained in a json response for each ATS, the best approach is to filter the fields on the strictly necessary for the application needs: deduplication needs only an id, the daily report needs the necessary information in an email to check if the new job is a valid opportunity for the potential user, and finally its status to decide if the application has already seen that job on previous run or not. In this way the fields could start as simply id, location, title, url. We can always add new fields later on.
The fields need to satisfy the following condition : stability, consistency across the ATS, and usefulness for the final user.
The custom 'first_seen' field to log when the job is seen for the first time downstream. The adaptor returns what seen in the source, the status comparison will be managed downstream. This will keep the adaptor component stateless, making it modular and replacable according "separation of concerns" between translating the source and managing the status in data engineering.

---

## 3. Architecture Questions: Why and How?

### Q1: What is the equivalent of the old master process in Airflow?
In Airflow, the master process is represented by the **DAG definition file** combined with **Dynamic Task Mapping** (`.expand()`). Instead of running a loop inside a single Bash script, Airflow dynamically instantiates independent Task Instances for each parameter (e.g., one task per target company or job board).

### Q2: How does restarting work in Airflow, and what makes a task safe to re-run?
Airflow provides native **Retries** and manual **Clear Task** operations via its Web UI. 
To make a re-run safe, the task must be **idempotent**. This means that executing the task once or multiple times with the same input produces the exact same side-effects (e.g., updating a database using `UPSERT` instead of `INSERT`, or ensuring email alerts are only sent for unnotified IDs).

### Q3: Where does explicit reporting of failures live?
In Airflow, failure reporting is handled at three levels:
1. **Visual UI:** Task instances turn red (`FAILED`) on the Grid and Graph views.
2. **Centralized Logging:** Detailed logs per task instance are accessible directly from the UI.
3. **Alerting Callbacks:** Native hooks like `on_failure_callback` can automatically trigger notifications (Slack, Email, PagerDuty).

### Q4: What does Idempotency mean, and was the old system idempotent?
- **Definition:** An operation is idempotent if running it multiple times with the same parameters yields the exact same result without unintended side-effects.
- **Comparison:** The old NTM script was partially idempotent if it checked for existing output files before processing. However, if interrupted mid-execution, it could leave partially processed `.vrt` or temporary files. In Airflow, tasks should be designed to clean up or overwrite their state cleanly on execution.

### Q5: What is Backfill, and how was it done manually vs. in Airflow?
- **Definition:** Backfill is the process of running a pipeline retroactively for past historical execution dates.
- **Old Way:** Manually looping over historical dates via terminal CLI parameters (e.g., `for date in dates; do ./script.sh $date; done`).
- **Airflow Way:** Airflow natively tracks the `logical_date` (or `execution_date`). You can trigger historical backfills natively via the CLI (`astro dev run dags backfill`) or UI, isolated by date context.

## 4. the advantages of orchestration

- **Concept of logical date e Run after** logical date (in the past called execution date) is the start of the temporal window we are analysing and run after  is the effective date when the task is triggered. Airflow make sure that we have the full picture for our temporal analysis and all the data are in the response.
- **Concept of Idempotency** Normal functioning in Airflows means that the task will be executed on the same logical date (retries, backfill or manual execution). This means we need to assure the task can give the same result every time it runs for the same logiacal date. If the task fails during execution and Airflow start again, the result has to be the same. This is why we set up a status file which get a blank write at each runs. If we used an append like open(state_file_path, "a"), this would have produced a duplication, giving a different result for a different run on the same input data.
- **Concept of Backfill** Even though it is not the case in this project, we might have a task that have access to a source which is indexable in time and have the possibility to 'Backfill' historic windows logical dates. In this project we don't have access to historical data but just 'current' data. However this is a powerful instrument in orchestration and Airflow that would give us the chance to analyse data back in time for specific time windows. However, in case one wants to analyse data back in time it has to be mindful to use the parameters 'catchup'. Not doing so, would end up Airflow firing many executions simultanuosly.
- **Concept of Deduplication** we eliminate instances that means the same thing. To decide what two information are the same thing is the hard part in a pipeline. In this project, we decide the job id is what defines uniqueness.
