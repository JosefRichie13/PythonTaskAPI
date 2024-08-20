# Backend for a ToDo App using FastAPI, SQLite and Python

This repo has the code for a ToDo App Backend. This app allows you to manage tasks. It exposes the below REST API endpoints 

* POST /addTask

  > This endpoint allows you to add a task .<br><br>
  > The POST Body is
  > ```
  >{
  >"taskname": "<NAME_OF_THE_TASK>",
  >"taskdate": "<DATE_OF_THE_TASK>", // DD-MMM-YYYY format, e.g., 05-Aug-2024
  >"taskstatus": "<TASK_STATUS>" // open or done 
  >}
  > ```
  
* GET /getTasks
  
  > This endpoint allows you to get tasks which are in open or done state. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?taskstatus=<open_OR_done> // Query param must be in small case
  > ```
  
* GET /getTasksByDate

  > This endpoint allows you to get tasks for a date. It requires a query param to be sent and has an optional param as well.<br><br>
  > The required query Parameter is
  > ```
  > ?taskdate="<DATE_OF_THE_TASK>", // DD-MMM-YYYY format, e.g., 05-Aug-2024
  > ```
  > The optional query Parameter is
  > ```
  > ?taskstatus=<open_OR_done> // Query param must be in small case
  > ```

* GET /getTaskID
  
  > This endpoint allows you to get the task ID of a task. It requires 3 query params to be sent.<br><br>
  > The query parameters are
  > ```
  > ?taskname="<NAME_OF_THE_TASK>"
  > ?taskdate="<DATE_OF_THE_TASK>" // DD-MMM-YYYY format, e.g., 05-Aug-2024
  > ?taskstatus="<TASK_STATUS>" // open or done, must be in small case
  > ```

* PUT /updateTask
  
  > This endpoint allows you to update the Task Name, Task Status or Task Date of a Task. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?taskID=<ID_of_theTask>
  > ```
  > The PUT Body is
  > ```
  > {
  >"taskname": "<NAME_OF_THE_TASK>",
  >"taskdate": "<DATE_OF_THE_TASK>", // DD-MMM-YYYY format, e.g., 05-Aug-2024
  >"taskstatus": "<TASK_STATUS>" // open or done 
  >}
  > ```
  
* DELETE /deleteTask

  > This endpoint allows you to delete any task. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?taskID=<ID_of_theTask>
  > ```

To run it in Dev mode, use the FastAPI run command

```console
fastapi dev .\index.py
```

Once the app is started locally, the below URL's will be available 

```
API Endpoint URL : http://127.0.0.1:8000 
Generated API Docs URL : http://127.0.0.1:8000/docs
```
