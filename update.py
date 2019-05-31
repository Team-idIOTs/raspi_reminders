import pyrebase
import sys, os
import json
from gtts import gTTS
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
    scheduler = ReminderScheduler(user='pi')

    fb_tasks = db.get()
    print(time.time())
    for task in fb_tasks.each():
        if (task.val()['updated'] == True):
            # Add to current list
            tasks[task.key()] = task.val()
            tts = gTTS(task.val()['audio'])
            print(time.time())
            tts.save(task.val()['name'].replace(" ", "") + ".mp3")
            task_obj = Task.from_dict(task.val())
            scheduler.schedule_task(task_obj)
            db.child(task.key()).update({"updated": False})
            for reminder in db.child(task.key()).child('reminders').get().each():
                if (task.val()['updated'] == True):
                    db.child(task.key()).child("reminders").child(reminder.key()).update({"updated":False})

    with open(json_path, 'w') as outfile:
        json.dump(tasks, outfile)
