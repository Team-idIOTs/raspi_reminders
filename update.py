import pyrebase
import sys, os
import json
sys.path.append(os.getcwd() + "/../dp_lib/")
sys.path.append(os.getcwd() + "/../")
from config import *
from ReminderScheduler import *
from Task import *


if __name__=="__main__":
    json_path = "reminders.json"

    tasks = {}
    try:
        with open(json_path) as infile:
            data = json.load(infile)
    except FileNotFoundError:
        pass

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    scheduler = ReminderScheduler(user='nkhachan')

    fb_tasks = db.get()
    for task in fb_tasks.each():
        if (task.val()['updated'] == True):
            tasks[task.key()] = task.val()
            task_obj = Task.from_dict(task.val())
            scheduler.schedule_task(task_obj)
            #db.child(task.key()).update({"updated": False})

    with open(json_path, 'w') as outfile:
        json.dump(tasks, outfile)