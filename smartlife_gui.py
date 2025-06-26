import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime
from tkinter import simpledialog


DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"users": {}}
    return {"users": {}}

def save_data():
    data = {
        "tasks": task_listbox.get(0, tk.END),
        "budget": budget_entry.get(),
        "mood": mood_slider.get(),
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def ask_username():
    def submit():
        global username
        username = entry.get().strip()
        if username:
            login.destroy()

    login = tk.Toplevel()
    login.title("Enter Username")
    login.geometry("300x100")
    tk.Label(login, text="Enter your name:").pack(pady=5)
    entry = tk.Entry(login)
    entry.pack()
    tk.Button(login, text="Start", command=submit).pack(pady=5)
    login.grab_set()
    root.wait_window(login)


username = ""
root = tk.Tk()
root.withdraw()
ask_username()
root.deiconify()

root.title("Smart Life Manager")
root.geometry("600x500")

data = load_data()
if username not in data["users"]:
    data["users"][username] = {
        "tasks": [],
        "budget": 0.0,
        "expenses": {},
        "moods": {},
        "completed_today": {},
        "xp": 0,
        "level": 1,
        "streak": 0,
        "last_task_day": ""
    }
user_data = data["users"][username]

nav = tk.Frame(root)
nav.pack()

def show_frame(frame):
    for f in [dashboard_frame, task_frame, budget_frame, mood_frame]:
        f.pack_forget()
    frame.pack(fill="both", expand=True)


#Frames
tk.Button(nav, text="🏠 Dashboard", command=lambda: [show_frame(dashboard_frame), update_dashboard()]).pack(side="left")
tk.Button(nav, text="Tasks", command=lambda: show_frame(task_frame)).pack(side="left")
tk.Button(nav, text="Budget", command=lambda: show_frame(budget_frame)).pack(side="left")
tk.Button(nav, text="Mood", command=lambda: show_frame(mood_frame)).pack(side="left")

dashboard_frame = tk.Frame(root)
task_frame = tk.Frame(root)
budget_frame = tk.Frame(root)
mood_frame = tk.Frame(root)


tk.Label(task_frame, text="📝 Task Manager").pack()
tk.Label(budget_frame, text="💰 Budget Manager").pack()
tk.Label(mood_frame, text="🎭 Mood Tracker").pack()


dashboard_frame.pack()  # Show this first


#Dashboard section
def dashboard_design():
    dashboard_title = tk.Label(dashboard_frame, text="📊 Smart Life Dashboard", font=("Arial", 16, "bold"))
    dashboard_title.pack(pady=10)
    
    user_label = tk.Label(dashboard_frame, text="")
    user_label.pack()
    
    level_label = tk.Label(dashboard_frame, text="")
    level_label.pack()
    
    xp_bar = ttk.Progressbar(dashboard_frame, length=200)
    xp_bar.pack(pady=5)
    
    streak_label = tk.Label(dashboard_frame, text="")
    streak_label.pack()
    
    budget_summary_label = tk.Label(dashboard_frame, text="")
    budget_summary_label.pack()
    
    task_summary_label = tk.Label(dashboard_frame, text="")
    task_summary_label.pack()
    
    mood_summary_label = tk.Label(dashboard_frame, text="")
    mood_summary_label.pack()
dashboard_design()

def update_dashboard():
    today = datetime.now().strftime("%Y-%m-%d")

    user_label.config(text=f"👤 User: {username}")

    xp = user_data["xp"]
    level = user_data["level"]
    xp_goal = level * 100
    xp_bar['value'] = min(xp / xp_goal * 100, 100)
    level_label.config(text=f"🏆 Level {level}  XP: {xp}/{xp_goal}")

    streak_label.config(text=f"🔥 Streak: {user_data['streak']} day(s)")

    expenses = sum(e[0] for e in user_data["expenses"].get(today, []))
    budget_summary_label.config(text=f"💰 Budget Used Today: ${expenses:.2f} / ${user_data['budget']:.2f}")

    completed = user_data["completed_today"].get(today, 0)
    task_summary_label.config(text=f"📝 Tasks Completed Today: {completed}")

    mood = user_data["moods"].get(today)
    if mood:
        emoji = ["😞", "😐", "🙂", "😊", "😄"][mood - 1]
        mood_summary_label.config(text=f"🎭 Mood: {emoji} ({mood})")
    else:
        mood_summary_label.config(text="🎭 Mood: Not logged")




#Task section
# Task list
task_listbox = tk.Listbox(task_frame, width=50, height=6)
task_listbox.pack()

def refresh_tasks():
    task_listbox.delete(0, tk.END)
    for task in user_data["tasks"]:
        task_listbox.insert(tk.END, task)
refresh_tasks()

# Task entry
task_entry = tk.Entry(task_frame, width=40)
task_entry.pack(pady=5)

def add_task():
    task = task_entry.get().strip()
    if task:
        user_data["tasks"].append(task)  # ✅ saves to memory
        save_data()                      # ✅ writes to data.json
        task_entry.delete(0, tk.END)
        refresh_tasks()                  # ✅ updates listbox
        
# Task completion
def complete_task():
    selected = task_listbox.curselection()
    if selected:
        idx = selected[0]
        task = user_data["tasks"][idx]
        if "✅" not in task:
            user_data["tasks"][idx] += " ✅"
            user_data["xp"] += 25

            today = datetime.now().strftime("%Y-%m-%d")
            user_data["completed_today"][today] = user_data["completed_today"].get(today, 0) + 1
            if user_data["completed_today"][today] == 3:
                user_data["xp"] += 75
                messagebox.showinfo("🎉 Daily Goal", "You've completed 3 tasks today! +75 XP")

            save_data()
            update_dashboard()
            refresh_tasks()
            
def delete_task():
    selected = task_listbox.curselection()
    if selected:
        idx = selected[0]
        del user_data["tasks"][idx]
        save_data()
        refresh_tasks()

def edit_task():
    selected = task_listbox.curselection()
    if selected:
        idx = selected[0]
        new_name = simpledialog.askstring("Edit Task", "Enter new task name:")
        if new_name:
            user_data["tasks"][idx] = new_name
            save_data()
            refresh_tasks()
            



tk.Button(task_frame, text="Delete Task", command=delete_task).pack()
tk.Button(task_frame, text="Edit Task", command=edit_task).pack()
tk.Button(task_frame, text="Add Task", command=add_task).pack()
tk.Button(task_frame, text="Complete Task", command=complete_task).pack()










#Budget section
tk.Label(budget_frame, text="Set Budget ($)").pack()
budget_entry = tk.Entry(budget_frame)
budget_entry.pack()

def show_budget():
    try:
        b = float(budget_entry.get())
        budget_label.config(text=f"Budget set: ${b:.2f}")
    except ValueError:
        budget_label.config(text="Invalid budget")

tk.Button(budget_frame, text="Set", command=show_budget).pack()
budget_label = tk.Label(budget_frame, text="")
budget_label.pack()


#Mood section
tk.Label(mood_frame, text="Mood (1–5)").pack()
mood_slider = tk.Scale(mood_frame, from_=1, to=5, orient="horizontal")
mood_slider.pack()




show_frame(dashboard_frame)  # or task_frame
update_dashboard()

dashboard_frame.pack(fill="both", expand=True)

root.mainloop()