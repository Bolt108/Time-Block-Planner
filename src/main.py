from datetime import datetime, timedelta
from planner import schedule_tasks, print_schedule
from storage import save_tasks, retrieve_tasks
from pathlib import Path
welcome = """
Welcome to the TIME BLOCK PLANNER!

This tool will help you transform your endless to-do list into a time block planner. It will prioritise your deep tasks and batch your shallow tasks.
The difference between a deep and shallow task is that a deep task requires a lot of brainpower and concentration to complete while a shallow task is more like a chore and is light in brain cycles used.

The steps are as follows:
1) You will be asked to enter the available time blocks you have in your day (e.g. "9:00-12:00, 13:00-17:00")
2) You will then enter your tasks with name, along with duration, and deep/shallow type
3) The program will schedule deep tasks first into available blocks, then shallow
4) The program will print a clean schedule to the terminal
5) Your tasks will be saved to a JSON file
"""

def get_available_time_blocks() -> list[str]:
    available_time_blocks_string = input("Please enter your available time blocks with a '-' for each time range in 24-hour format and separated by a comma and space: ")
    available_time_blocks_list = available_time_blocks_string.replace(" ", "").split(',')
    return available_time_blocks_list

# Helper to parse string into a clean datetime.time object
def parse_to_time(t_str):
    fmt = "%H:%M" if ":" in t_str else "%H"
    return datetime.strptime(t_str, fmt).time()

def available_time_blocks_str_to_timedelta(available_time_blocks_str_list: list) -> list[dict]:
    processed_ranges = []

    for time_str in available_time_blocks_str_list:
        start_str, end_str = time_str.split('-')
            
        start_time = parse_to_time(start_str)
        end_time = parse_to_time(end_str)
        
        # Calculate duration by anchoring to a dummy date (since time objects can't be subtracted)
        dummy_date = datetime.today()
        start_dt = datetime.combine(dummy_date, start_time)
        end_dt = datetime.combine(dummy_date, end_time)
        
        # Extract duration as timedelta and convert to total minutes
        duration_td = end_dt - start_dt
        duration_minutes = int(duration_td.total_seconds() / 60)
        duration_hours = duration_minutes/60
        
        processed_ranges.append({
            "start_clock": start_time,
            "end_clock": end_time,
            "duration_minutes": duration_minutes,
            "duration_hours": duration_hours
        })
    
    return processed_ranges


def get_task_list(curr_task_dict=None):
    task_dict = {} if curr_task_dict is None else curr_task_dict
    any_tasks = input("\nDo you have any tasks? (y/n) ")
    while any_tasks == 'y':
        task_name = input("\nWhat is the task name? ")
        task_duration_minutes = int(input("\nHow long will the task take to complete in minutes? "))
        task_depth_type = input("\nIs this a deep task or shallow task? Enter 'deep' or 'shallow': ").strip().lower()
        task_dict[task_name] = {'duration_minutes': task_duration_minutes, 'depth_type': task_depth_type}
        any_tasks = input("\nDo you have any more tasks? (y/n) ")

    return task_dict

def main():
    username = input("\n\nDear User, by what name/username would you like to be referred to? ")
    user_tasks_file_path = ""
    curr_task_dict = {}
    folder_path = Path('data')
    if folder_path.exists():
        for item in folder_path.iterdir():
            if username in str(item):
                user_tasks_file_path = item
                break
    if user_tasks_file_path == "":
        print(f"\nAlrighty {username}, here we gooooo.....")
        print(welcome)
    available_time_blocks_str = get_available_time_blocks()
    available_time_blocks_list_dict = available_time_blocks_str_to_timedelta(available_time_blocks_str)
    print("\nAlright here are the available time blocks in your day: ")
    for time_block in available_time_blocks_list_dict:
        print(f"Time: {time_block['start_clock']} to {time_block['end_clock']} | Duration: {time_block['duration_minutes']} minutes")
    time_blocks_correct = input("\nAre these time blocks correct? (y/n) ")
    while time_blocks_correct != 'n' and time_blocks_correct != 'y':
        print("Please only enter 'y' or 'n'")
        time_blocks_correct = input("\nAre these time blocks correct? (y/n) ")

    while time_blocks_correct != 'y':
        available_time_blocks_str = get_available_time_blocks()
        available_time_blocks_list_dict = available_time_blocks_str_to_timedelta(available_time_blocks_str)
        for time_block in available_time_blocks_list_dict:
            print(f"Time: {time_block['start_clock']} to {time_block['end_clock']} | Duration: {time_block['duration_minutes']} minutes")
        time_blocks_correct = input("\nAre these time blocks correct? (y/n) ")

    if user_tasks_file_path != "":
        curr_task_dict = retrieve_tasks(str(user_tasks_file_path))
        print(f"\nWelcome back {username}! Here are your saved tasks:")
        for name, info in curr_task_dict.items():
            print(f"  - {name}: {info['duration_minutes']} mins [{info['depth_type']}]")
    task_dict = get_task_list(curr_task_dict)
    scheduled = schedule_tasks(available_time_blocks_list_dict, task_dict)
    print_schedule(scheduled)
    save_tasks(task_dict, username)
    print(f"\nHave a productive day, {username}! Your schedule is set.")

main()