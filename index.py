from typing import Union

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
import sqlite3
from helpers import *
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def landingPage():
    return FileResponse("PythonTaskApp.html")

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



# Gets all Tasks, Tasks in Open status or Tasks in Done status. Taskstatus is an optional param
@app.get("/getTasks")
def getTasks(response: Response, taskstatus: Union[str, None] = None):

    # Connects to the DB
    getConnection = sqlite3.connect("PYTHONTASKAPP.db")
    getCur = getConnection.cursor()

    # Gets all the tasks
    if taskstatus == "":
        queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP"
        taskCheck = getCur.execute(queryToCheckExistingTask).fetchall()
        return taskCheck
    # Gets tasks which are in open or done State
    elif taskstatus == "open" or taskstatus == "done":
        queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP WHERE TASKSTATUS = ?"
        valuesToCheckExistingTask = [taskstatus]
        taskCheck = getCur.execute(queryToCheckExistingTask, valuesToCheckExistingTask).fetchall()
        return taskCheck
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status" : "The provided query parameter is not supported" }



# Gets all Tasks of a date. Taskdate is a mandatory param, Taskstatus is an optional param
@app.get("/getTasksByDate")
def getTasksByDate(response: Response, taskdate: str, taskstatus: Union[str, None] = None):

    # Connects to the DB
    getConnection = sqlite3.connect("PYTHONTASKAPP.db")
    getCur = getConnection.cursor()

    # Checks the date format, if its incorrect returns a 400
    if checkDateFormat(taskdate) == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status" : taskdate + " is not a valid date or is not in DD-MMM-YYYY format, e.g., 05-Aug-2024. Please correct the date."}

    # Gets the tasks which are in open or done state for the given date
    if taskstatus == "open" or taskstatus == "done":
        queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP WHERE TASKDATE = ? AND TASKSTATUS = ?"
        valuesToCheckExistingTask = (taskdate, taskstatus)
        taskCheck = getCur.execute(queryToCheckExistingTask, valuesToCheckExistingTask).fetchall()
        # This if block, checks if there are any tasks for the day
        if len(taskCheck) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status": "No task is scheduled on " + taskdate}
        return taskCheck
    # Gets all the tasks for the given date
    elif taskdate != 0:
        queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP WHERE TASKDATE = ?"
        valuesToCheckExistingTask = [taskdate]
        taskCheck = getCur.execute(queryToCheckExistingTask, valuesToCheckExistingTask).fetchall()
        # This if block, checks if there are any tasks for the day
        if len(taskCheck) == 0:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"status": "No task is scheduled on " + taskdate}
        return taskCheck
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status" : "No task is scheduled on " + taskdate + " with the status " + taskstatus}



# Gets all Task ID of Task
@app.get("/getTaskID")
def getTasks(response: Response, taskname: str, taskdate: str, taskstatus: str):

    # Connects to the DB
    getConnection = sqlite3.connect("PYTHONTASKAPP.db")
    getCur = getConnection.cursor()

    queryToCheckExistingTaskID = "SELECT ROWID FROM PYTHONTASKAPP WHERE TASKNAME = ? AND TASKDATE = ? AND TASKSTATUS = ?"
    valuesToCheckExistingTaskID = (taskname, taskdate, taskstatus)
    taskID = getCur.execute(queryToCheckExistingTaskID, valuesToCheckExistingTaskID).fetchone()

    if taskID is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No suck task found, please recheck"}
    else:
        return {"status": taskID}



# Defining the body for updating a Task, it needs name of the task, date of the task, status of the task
class updateATaskData(BaseModel):
    taskname: str
    taskdate: str
    taskstatus: str

# Updates a task using a PUT call
@app.put("/updateTask")
def updateTask(updateATaskBody: updateATaskData, taskID: str, response: Response):

    sanitizedName = sanitizeString(updateATaskBody.taskname).strip()
    sanitizedStatus = sanitizeString(updateATaskBody.taskstatus).strip()
    sanitizedDate = checkDateFormat(updateATaskBody.taskdate)

    if sanitizedDate == False:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status" : updateATaskBody.taskdate + " is not a valid date or is not in DD-MMM-YYYY format, e.g., 05-Aug-2024. Please correct the date."}

    putConnection = sqlite3.connect("PYTHONTASKAPP.db")
    cur = putConnection.cursor()

    # Checks if the task exists and if it does not, returns a 404
    queryToCheckTheUpdate = "SELECT * FROM PYTHONTASKAPP WHERE ROWID = ?"
    valuesToCheckTheUpdate = [taskID]
    checkTheUpdate = cur.execute(queryToCheckTheUpdate, valuesToCheckTheUpdate).fetchone()

    if checkTheUpdate is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No suck task found, please recheck"}
    else:
    # If the task exists, check if we are updating to an already existing task, if yes, return 422
        queryToCheckExistingTask = "SELECT * FROM PYTHONTASKAPP WHERE TASKNAME = ? AND TASKDATE = ? AND TASKSTATUS = ?"
        valuesToCheckExistingTask = (sanitizedName, updateATaskBody.taskdate, sanitizedStatus)
        existingTaskCheck = cur.execute(queryToCheckExistingTask, valuesToCheckExistingTask).fetchall()
        if len(existingTaskCheck) > 0:
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            return {
                "status": "The task, " + sanitizedName + ", already exists on " + updateATaskBody.taskdate + ", with the status "+ sanitizedStatus +". Please recheck"}

        # Update the task, if it exists and if we are not updating to an already existing task
        queryToUpdateExistingTask = "UPDATE PYTHONTASKAPP SET TASKNAME = ?, TASKDATE = ?, TASKSTATUS = ? WHERE ROWID = ?"
        valuesToUpdateExistingTask = (sanitizedName, updateATaskBody.taskdate, sanitizedStatus, taskID)
        cur.execute(queryToUpdateExistingTask, valuesToUpdateExistingTask)
        putConnection.commit()
        return {"status" : "Task updated"}



# Deletes a task using a DELETE call
@app.delete("/deleteTask")
def deleteTask(taskID: str, response: Response):

    # Connects to the DB
    delConnection = sqlite3.connect("PYTHONTASKAPP.db")
    delCur = delConnection.cursor()

    # Checks if the task exists
    queryToCheckTask = "SELECT * FROM PYTHONTASKAPP WHERE ROWID = ?"
    valuesToCheckTask = [taskID]
    checkDelResult = delCur.execute(queryToCheckTask, valuesToCheckTask).fetchall()

    # If the task exists, delete it or else return 404
    if len(checkDelResult) > 0:
        queryToDeleteTask = "DELETE FROM PYTHONTASKAPP WHERE ROWID = ?"
        delCur.execute(queryToDeleteTask, valuesToCheckTask)
        delConnection.commit()
        return {"status": "Task with ID " + taskID + " is deleted"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No task with ID "+taskID+" found, please recheck"}