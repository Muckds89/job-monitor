# Notes on the architecture and orchestration (the job-monitor project in Airflow and Atro CLI)

# 1. Contest
it is a project to demonstrate myself the utility of orchestration and why is the required standard in data engineering. It is to understand the reason behind orchestrating tasks instead of stacking them in sequence. 

In this project we will try to get familiar with the concepts of scheduling, indempodency, deduplication, alerting and containeirisation.

The project is structured to be a simple job-monitor but trying to touch in all the spects of modern orchestration.

the questions I will try to answer:

- my old master process was generating a work list, what is the equivalent in Airflow?
- the restarting way I designed in my old project, what will it be in Airflow? what I should assure in Airflow to restart and relaunch a task safely?
- MY explicit report of failures where it lives in Airflow?
- what does it mean that a DAG is idempodent and my old process was idempodent?
- what does it mean backfill and how did I do it in the old process?


# 2. the parallel with my previous NTM project in Bluesky
* in the old system, the NTM process in bluesky had a monitor.sh script "master" that was monitoring specific folders. When a user wanted to process a new flight , it had to load the tiles in specific input folders. when the monitor script noticed through a diff cat command that the folder contained not processed tiles, it would start the NTM Process by calling a bash script that generated a work list. each command line was a separte bash script call for a single tile. the single tile command was then called to create a .vrt file with adjacent tiles (a buffer in order not to create a cutline in the final product), reprojecting, resampling, masking etc.
** in Airflow ...

# 3. Architecture questions: why and how?

# 4. the advantages of orchestration

