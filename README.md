# Time Block Planner

A command-line tool that transforms your to-do list into a structured time block schedule. Deep work tasks are prioritised first, followed by shallow tasks.

## How to Run

```bash
python main.py
```

## How It Works
1. Enter your available time blocks for the day (e.g. `9:00-12:00, 14:00-17:30`)
2. Enter your tasks with name, estimated duration in minutes, and type (deep/shallow)
3. The planner schedules deep tasks first, then shallow tasks
4. Your schedule is printed to the terminal
5. Tasks are saved to a JSON file and reloaded on your next session

## Example Output

```
09:00 - 11:00 | [DEEP] Boot.dev Personal Project 1
11:00 - 11:15 | [DEEP] IT SecOps Interview Preparation
11:15 - 12:00 | [DEEP] Salesforce Study (continued)
14:00 - 17:30 | [DEEP] Salesforce Study (continued)
```


## Backlog
- Priority ranking (1-3)
- Fixed/mandatory blocks
- Pomodoro timer integration
- Meal break suggestions
- Multi-day project tracking
- Full week planner