from csv import DictReader
from flask import Flask, request, render_template
import pandas as pd
# import csv

tasks_list = pd.read_csv("tasks_list.csv").to_dict(orient='records') #will be in dataframe (pd), convert to dict shape

# tasks_list = [
#     {"task_name": "go to pet finder", "project": "adopt a cat", "area": "fun and adventure", "when": "04/01/2022", "where": "out", "id": "1"},
#     {"task_name": "buy treats", "project": "train dog", "area": "fun and adventure", "when": "04/01/2022", "where": "out", "id": "2"},
#     {"task_name": "clean bathroom", "project": "maintain home", "area": "wealth", "when": "04/01/2022", "where": "home", "id": "3"},
# ]

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html") # this is where I can list jumping off point, links to edit mode page    

@app.route("/tasks/", methods=["GET", "POST"]) # list of tasks, CREATE
def list_tasks():
    return render_template("tasks.html", tasks_list=tasks_list)

@app.route("/tasks/new", methods=["GET", "POST"])
def add_new_task():
    new_task = {}
    new_task['tasks_name'] = request.form['tasks_name']
    new_task['project'] = request.form['project']
    new_task['area'] = request.form['area']
    new_task['when'] = request.form['when']
    new_task['where'] = request.form['where']
    new_task['id'] = str(len(tasks_list) + 1)
    tasks_list.append(new_task)
    return {"status": 201, "data": tasks_list}

@app.route("/tasks/<id>/", methods=["GET", "PUT", "DELETE"]) #SHOW UPDATE DELETE
def task_page(id):  
    for task in tasks_list:
        print(task['id'])
        if str(task['id']) == str(id): 
            if request.method == "GET":
                return render_template("show.html", tasks_list = task)
            elif request.method == "PUT":
                return "update details of a specific task"
            elif request.method == "DELETE":
                return "delete_task.html" # this doesn't work 
            else:
                return "this task doesn't exist or your route is wrong" # delete_task.html
    tasks_id_list = ""
    for task2 in tasks_list:
        tasks_id_list = tasks_id_list + ", " + str(task2["id"])
    return tasks_id_list + " these are the task ids (debug)"

            
    
@app.route("/tasks/new/", methods=["GET"])  #NEW , SHOW FORM TO CREATE A NEW
def new_task_form():
    return render_template("new.html") #input form for a new task


# @app.route("/tasks/<id>/edit/", methods=["GET"])  # EDIT FORM TO UPDATE
# def edit_task_form():
#     return render_template("update_task.html") #return individual task by id and in edit mode update_task.html

if __name__ == "__main__":
    app.run()