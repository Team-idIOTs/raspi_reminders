import pyrebase
import sys, os
import json
sys.path.append(os.getcwd() + "/../reminders_lib/")
sys.path.append(os.getcwd() + "/../")
from config import *
from ReminderScheduler import *
from Task import *
import time


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
    storage = firebase.storage()
    scheduler = ReminderScheduler(user='pi')

    fb_tasks = db.get()
    for task in fb_tasks.each():
        if (task.val()['updated'] == True):

            # Add to current list
            tasks[task.key()] = task.val()

            # Create the object
            task_obj = Task.from_dict(task.val())

            # Download the audio file
            storage.child(task_obj.get_audio_name()).download(task_obj.get_audio_name())
            os.system("mv " + task_obj.get_audio_name() + " /home/pi/sounds/")

            # Schedule the cron tasks
            scheduler.schedule_task(task_obj)

            # Revert task's update status
            db.child(task.key()).update({"updated": False})

            # Revert reminder's update status
            for reminder in db.child(task.key()).child('reminders').get().each():
                if (task.val()['updated'] == True):
                    db.child(task.key()).child("reminders").child(reminder.key()).update({"updated":False})

    with open(json_path, 'w') as outfile:
        json.dump(tasks, outfile)
