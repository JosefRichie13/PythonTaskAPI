# Backend for a ToDo App using FastAPI, SQLite and Python

This repo has the code for a ToDo App Backend. It exposes the below REST API endpoints 

* POST /addTask
* GET /getTasks
* GET /getTasksByDate
* GET /getTaskID
* PUT /updateTask
* DELETE /deleteTask

To run it in Dev mode, use the FastAPI run command

```console
fastapi dev .\index.py
```

Once the app is started locally, the below URL's will be available 

```
API Endpoint URL : http://127.0.0.1:8000 
Generated API Docs URL : http://127.0.0.1:8000/docs
```
