# Task Manager Cloud API

This is a task manager REST API I made for Task 6 of the SOA and Cloud Computing course (TIES4560) at the University of Jyväskylä, October 2025. It runs as 4 Google Cloud Functions in Python 3.11 and saves the tasks in Firestore. There is also a small web page (`index.html`) to use the API, which I hosted on Google Cloud Storage.

## What is inside

| File | What it does |
|---|---|
| `main.py` | The 4 Cloud Functions |
| `index.html` | The web page to create, list and delete tasks and to see the statistics |
| `requirements.txt` | The Python packages |
| `stats_function.py` | My first version of the statistics function, before I moved it into `main.py` |
| `event_function.py`, `scheduled_function.py` | An event function and a scheduled function I tried, but I did not deploy them |

## API

| Function | Method | What it does |
|---|---|---|
| `create-task` | POST | Creates a task from a JSON body with `title` and an optional `description` |
| `get-tasks` | GET | Returns all tasks and the count |
| `delete-task` | DELETE | Deletes a task, for example `delete-task?id=1` |
| `get-task-stats` | GET | Returns the total, completed and pending tasks. This was the bonus part |

Every task is saved in the Firestore collection `tasks`, with `id`, `title`, `description`, `completed` and `created_at`.

The first version on 17 October 2025 kept the tasks in memory. Then on 18 October I changed it to save them in Firestore.

## How to run

Step 1: Log in and set your Google Cloud project:

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

Step 2: Deploy the functions from this folder. For example, for `create-task`:

```bash
gcloud functions deploy create-task --runtime python311 --trigger-http --allow-unauthenticated --region europe-west1 --source . --entry-point create_task
```

Do the same for `get-tasks` (entry point `get_tasks`), `delete-task` (`delete_task`) and `get-task-stats` (`get_task_stats`).

Step 3: Put your project ID in `API_BASE` in `index.html` and open the page. You can also test the API with curl:

```bash
curl https://europe-west1-YOUR_PROJECT_ID.cloudfunctions.net/get-tasks
```

## Limits

- The task counts in `get-task-stats` come from Firestore, but the API calls, response time and success rate are fixed sample numbers.
- The functions accept calls without login and allow every origin (CORS), as it was a course demo.
- Currently, there is no way to edit a task.
