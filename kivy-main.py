from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import json
import os
from datetime import datetime

DATA_FILE = "data.json"
data = {"users": {}}


#Functions to load and save data to and from the json file
def load_data():
    global data
    if os.path.exists(DATA_FILE): 
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"users": {}}
    return data

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

   


def ensure_user_initialized(username):
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


#Classes for the UI

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        if not username:
            return
        ensure_user_initialized(username)
        self.manager.current = "dashboard"
        self.manager.get_screen("dashboard").load_user(username)

class DashboardScreen(Screen):
    def load_user(self, username):
        self.username = username
        user = data["users"][username]
        today = datetime.now().strftime("%Y-%m-%d")

        # XP/Streak/Level updates
        user["xp"] += 1
        if user["xp"] >= user["level"] * 100:
            user["level"] += 1

        last_day = user["last_task_day"]
        if last_day:
            last = datetime.strptime(last_day, "%Y-%m-%d").date()
            now = datetime.now().date()
            if (now - last).days == 1:
                user["streak"] += 1
            elif (now - last).days > 1:
                user["streak"] = 1
        else:
            user["streak"] = 1
        user["last_task_day"] = today
        save_data()

        self.ids.user_label.text = f"Welcome, {username}"
        self.ids.status_label.text = f"Level {user['level']} | XP {user['xp']} | 🔥 Streak: {user['streak']}"
    
    def go_to_tasks(self):
        self.manager.get_screen("tasks").load_user(self.username)
        self.manager.current = "tasks"
    def go_to_budget(self):
        self.manager.get_screen("budget").load_user(self.username)
        self.manager.current = "budget"



class TaskManagerScreen(Screen):
    def on_pre_enter(self):
        self.refresh_tasks()
        
    def load_user(self, username):
        self.username = username
        self.user_data = data["users"][username]
        
    def refresh_tasks(self):
        task_box = self.ids.task_box
        task_box.clear_widgets()
        tasks = self.user_data.get("tasks", [])
        
        if not tasks:
            task_box.add_widget(Label(text = "No tasks yet.", font_size = 18))
            return
        
        for i, task in enumerate(tasks):
            h = BoxLayout(orientation = "horizontal", size_hint_y = None, height = 40)
            h.add_widget(Label(text = f"{i+1}. {task}", font_size = 16))
            done_btn = Button(text = "Done", size_hint_x = None, width = 50, on_press = lambda btn, i=i: self.complete_task(i))
            del_btn = Button(text = "Delete", size_hint_x = None, width = 50, on_press = lambda btn, i=i: self.delete_task(i))
            
            h.add_widget(done_btn)
            h.add_widget(del_btn)
            task_box.add_widget(h)
            
    def add_task(self):
        task_text = self.ids.task_input.text.strip()
        if task_text:
            self.user_data["tasks"].append(task_text)
            self.ids.task_input.text = ""
            save_data()
            self.refresh_tasks()
            
    def complete_task(self, index):
        if "✅" not in self.user_data["tasks"][index]:
            self.user_data["tasks"][index] += " ✅"
            # XP logic
            today = datetime.now().strftime("%Y-%m-%d")
            completed_today = self.user_data["completed_today"].get(today, 0) + 1
            self.user_data["completed_today"][today] = completed_today
            
            if completed_today == 3:
                self.user_data["xp"] += 75
            else:
                self.user_data["xp"] += 25
            
            # Check for level up
            level = self.user_data["level"]
            if self.user_data["xp"] >= level * 100:
                self.user_data["level"] += 1
                print(f"🎉 Leveled up! Now level {self.user_data['level']}")
            
            save_data()
            self.refresh_tasks()

    def delete_task(self, index):
        del self.user_data["tasks"][index]
        save_data()
        self.refresh_tasks()


class BudgetManagerScreen(Screen):
    def load_user(self, username):
        self.username = username
        self.user_data = data["users"][username]
        self.refresh_expenses()
        
    def set_budget(self):
        try:
            value = float(self.ids.budget_input.text.strip())
            self.user_data["budget"] = value
            self.ids.budget_input.text = ""
            save_data()
            self.refresh_expenses()
        except ValueError:
            pass  # Handle UI feedback later
        def add_expense(self):
            name = self.ids.expense_name.text.strip()
        try:
            amount = float(self.ids.expense_amount.text.strip())
        except ValueError:
            return
    def add_expense(self):
        name = self.ids.expense_name.text.strip()
        try:
            amount = float(self.ids.expense_amount.text.strip())
        except ValueError:
            return

        if name and amount >= 0:
            today = datetime.now().strftime("%Y-%m-%d")
            entry = [amount, name, "Uncategorized"]

            if today not in self.user_data["expenses"]:
                self.user_data["expenses"][today] = []

            self.user_data["expenses"][today].append(entry)

            self.ids.expense_name.text = ""
            self.ids.expense_amount.text = ""

            save_data()
            self.refresh_expenses()


    def refresh_expenses(self):
        box = self.ids.expense_box
        box.clear_widgets()
        today = datetime.now().strftime("%Y-%m-%d")
        expenses = self.user_data["expenses"].get(today, [])
        total = sum(item[0] for item in expenses)

        if not expenses:
            box.add_widget(Label(text="No expenses today.", font_size=16))
        else:
            for amount, name, _ in expenses:
                box.add_widget(Label(
                text=f"{name}: ${amount:.2f}",
                font_size=16,
                size_hint_y=None,
                height=30  # 📏 ensures spacing
            ))

        box.add_widget(Label(
            text=f"💸 Spent: ${total:.2f} / ${self.user_data.get('budget', 0.0):.2f}",
            font_size=18,
            size_hint_y=None,
            height=40
        ))



class SmartLifeApp(App):
    def build(self):
        load_data()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TaskManagerScreen(name="tasks"))
        sm.add_widget(BudgetManagerScreen(name="budget"))
        return sm


SmartLifeApp().run()
