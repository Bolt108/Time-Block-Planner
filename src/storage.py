#Saving to JSON (step 5):

import json
import os

def save_tasks(task_dict, username):
    os.makedirs("data", exist_ok=True)
    filename = f"data/{username}_tasks.json"
    with open(filename, "w") as f:
        json.dump(task_dict, f, indent=4)
    print(f"\nTasks saved to {filename}")

def retrieve_tasks(path=""):
    task_dict = {}
    with open(path, "r") as f:
        task_dict = json.load(f)
    return task_dict
   