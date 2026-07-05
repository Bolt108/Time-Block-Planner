from datetime import datetime, timedelta
"""
The scheduling algorithm in plain English:

Sort tasks: deep first, then shallow
For each task, find a time block with enough remaining minutes
Assign a start time, calculate end time, reduce the block's remaining time
If a task is longer than any single block, split it across blocks
Print the final schedule
A data structure to track scheduled slots:

scheduled = [
    {
        "task_name": "Boot.dev Personal Project 1",
        "depth_type": "deep",
        "start": datetime_object,
        "end": datetime_object
    }
]
"""
#The scheduler function skeleton:

def schedule_tasks(time_blocks, task_dict):
    # Sort: deep tasks first
    sorted_tasks = sorted(task_dict.items(), key=lambda x: x[1]['depth_type'] != 'deep')
    
    scheduled = []
    
    # Track remaining minutes per block
    # Use datetime objects so you can do arithmetic
    blocks = []
    for block in time_blocks:
        dummy = datetime.today().date()
        blocks.append({
            "current": datetime.combine(dummy, block["start_clock"]),
            "end": datetime.combine(dummy, block["end_clock"]),
        })
    
    for task_name, task_info in sorted_tasks:
        minutes_remaining = task_info["duration_minutes"]
        
        for block in blocks:
            if minutes_remaining <= 0:
                break
            available = int((block["end"] - block["current"]).total_seconds() / 60)
            if available <= 0:
                continue
            
            chunk = min(minutes_remaining, available)
            slot_start = block["current"]
            slot_end = slot_start + timedelta(minutes=chunk)
            
            scheduled.append({
                "task_name": task_name,
                "depth_type": task_info["depth_type"],
                "start": slot_start,
                "end": slot_end,
                "note": "continued" if chunk < task_info["duration_minutes"] and slot_start != datetime.combine(datetime.today().date(), time_blocks[0]["start_clock"]) else ""
            })
            
            block["current"] = slot_end
            minutes_remaining -= chunk
        
        if minutes_remaining > 0:
            print(f"Warning: '{task_name}' could not be fully scheduled. This task will require multiple days to complete. {minutes_remaining} minutes unscheduled.")
    
    return scheduled

# Printing the schedule:

def print_schedule(scheduled):
    print("\n--- YOUR TIME BLOCK SCHEDULE ---\n")
    for slot in scheduled:
        label = f"[{slot['depth_type'].upper()}]"
        note = f" ({slot['note']})" if slot['note'] else ""
        print(f"{slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')} | {label} {slot['task_name']}{note}")


