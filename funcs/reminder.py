import os
import json
from datetime import datetime, timedelta

REMINDERS_FILE = "reminders.json"

def load_reminders():
    if not os.path.exists(REMINDERS_FILE):
        return []
    with open(REMINDERS_FILE, "r") as file:
        reminders = json.load(file)
    return reminders

def save_reminders(reminders):
    with open(REMINDERS_FILE, "w") as file:
        json.dump(reminders, file)

def set_reminder(reminder_text, time):
    reminders = load_reminders()
    reminder_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    reminders.append({"text": reminder_text, "time": time})
    save_reminders(reminders)
    return f"Reminder set for {reminder_time.strftime('%Y-%m-%d %H:%M:%S')} - '{reminder_text}'."

def view_reminders():
    reminders = load_reminders()
    if not reminders:
        return "You have no upcoming reminders."

    reminders.sort(key=lambda x: datetime.strptime(x["time"], "%Y-%m-%d %H:%M:%S"))
    reminder_list = [f"{datetime.strptime(r['time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')} - {r['text']}" for r in reminders]
    return "\n".join(reminder_list)

def clear_reminders():
    os.remove(REMINDERS_FILE)
    return "All reminders have been cleared."
