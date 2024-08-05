from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import sqlite3
from create import *

app = FastAPI()

# Defining the body for adding a Task, it needs name of the task, date of the task, status of the task
class addATaskData(BaseModel):
    taskname: str
    taskdate: str
    taskstatus: str


# Adds a task using a POST call
@app.post("/addTask")
def addATask(addATaskBody: addATaskData, response: Response):

    # Taking in the 3 params from the API body.
    # Sanitizing the strings to avoid any XSS vulnerabilities using sanitizeString()
    # Removes any leading/trailing spaces using strip()
    sanitizedName = sanitizeString(addATaskBody.taskname).strip()
    sanitizedStatus = sanitizeString(addATaskBody.taskstatus).strip()
    sanitizedDate = checkDateFormat(addATaskBody.taskdate)

    # Checks the date format, if its incorrect returns a 400
    if sanitizedDate == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status" : addATaskBody.taskdate + " is not a valid date or is not in DD-MMM-YYYY format, e.g., 05-Aug-2024. Please correct the date."}

    # Connects to the DB
    connection = sqlite3.connect("PYTHONTASKAPP.db")
    cur = connection.cursor()

    # Checks if the same task exists on a day
    # If the task exists, it returns 422 and the error message
    queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP WHERE TASKNAME = ? AND TASKDATE = ?"
    valuesToCheckExistingTask = (sanitizedName, addATaskBody.taskdate)
    existingTaskCheck = cur.execute(queryToCheckExistingTask, valuesToCheckExistingTask).fetchall()
    if len(existingTaskCheck) > 0:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"status" : "The task, " + sanitizedName + ", already exists on " + addATaskBody.taskdate + ". Please recheck"}


    # If everything else is good, adds the task to the DB and returns the success status
    queryToAddTask = "INSERT INTO PYTHONTASKAPP (TASKNAME, TASKDATE, TASKSTATUS) VALUES (?, ?, ?)"
    valuesToAddTask = (sanitizedName, addATaskBody.taskdate, sanitizedStatus)
    cur.execute(queryToAddTask, valuesToAddTask)
    connection.commit()
    return {"status" : "Task added" }