from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt



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
            print("⚠️ Login aborted: No username entered.")
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
        self.ids.status_label.text = f"Level {user['level']} | XP {user['xp']} | Streak: {user['streak']}"
    
    def go_to_tasks(self):
        self.manager.get_screen("tasks").load_user(self.username)
        self.manager.current = "tasks"
    def go_to_budget(self):
        self.manager.get_screen("budget").load_user(self.username)
        self.manager.current = "budget"
    def go_to_mood(self):
        self.manager.get_screen("mood").load_user(self.username)
        self.manager.current = "mood"


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
            h = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        
            label = Label(text=f"{i+1}. {task}", font_size=16, size_hint_x=0.6)
        
            done_btn = Button(text="[DONE]", size_hint_x=0.15, on_press=lambda btn, i=i: self.complete_task(i))
            edit_btn = Button(text="[EDIT]", size_hint_x=0.15, on_press=lambda btn, i=i: self.edit_task(i))
            del_btn = Button(text="[DEL]", size_hint_x=0.15, on_press=lambda btn, i=i: self.delete_task(i))
        
            h.add_widget(label)
            h.add_widget(done_btn)
            h.add_widget(edit_btn)
            h.add_widget(del_btn)
        
            task_box.add_widget(h)
    
    def edit_task(self, index):
    
        current = self.user_data["tasks"][index].replace(" [DONE]", "")
    
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
    
        task_input = TextInput(text=current, multiline=False, hint_text="Edit task")
    
        save_btn = Button(text="Save", size_hint_y=None, height=40)
        cancel_btn = Button(text="Cancel", size_hint_y=None, height=40)
    
        btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btns.add_widget(save_btn)
        btns.add_widget(cancel_btn)
    
        layout.add_widget(Label(text="Edit Task", size_hint_y=None, height=30))
        layout.add_widget(task_input)
        layout.add_widget(btns)
    
        popup = Popup(title="Edit Task", content=layout, size_hint=(0.75, 0.4), auto_dismiss=False)
    
        def save_changes(instance):
            new_text = task_input.text.strip()
            if new_text:
                was_done = "[DONE]" in self.user_data["tasks"][index]
                self.user_data["tasks"][index] = new_text + (" [DONE]" if was_done else "")
                save_data()
                self.refresh_tasks()
                popup.dismiss()
    
        save_btn.bind(on_press=save_changes)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
    
        popup.open()

    def add_task(self):
        task_text = self.ids.task_input.text.strip()
        if task_text:
            self.user_data["tasks"].append(task_text)
            self.ids.task_input.text = ""
            save_data()
            self.refresh_tasks()
            
    def complete_task(self, index):
        task = self.user_data["tasks"][index]
        today = datetime.now().strftime("%Y-%m-%d")
        completed_today = self.user_data["completed_today"].get(today, 0)
    
        if "[DONE]" in task:
            # Uncheck the task
            self.user_data["tasks"][index] = task.replace(" [DONE]", "")
            if completed_today > 0:
                self.user_data["completed_today"][today] = completed_today - 1
    
            # Optional: Subtract XP (or just don't award it again)
            # To keep it safe, no XP subtraction is applied
    
        else:
            # Check the task as done
            self.user_data["tasks"][index] += " [DONE]"
            completed_today += 1
            self.user_data["completed_today"][today] = completed_today
    
            if completed_today == 3:
                self.user_data["xp"] += 75
            else:
                self.user_data["xp"] += 25
    
            # Check level up
            if self.user_data["xp"] >= self.user_data["level"] * 100:
                self.user_data["level"] += 1
                print(f"Level up! Now level {self.user_data['level']}")
    
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
    
    def show_expense_graph(self):
        try:
            import matplotlib.pyplot as plt
        
            expenses_by_day = self.user_data.get("expenses", {})
            if not expenses_by_day:
                print("📭 No expense data to graph.")
                return
        
            # Sort by date
            sorted_dates = sorted(expenses_by_day.keys())
            totals = []
        
            for date in sorted_dates:
                total = sum(item[0] for item in expenses_by_day[date])
                totals.append(total)
        
            plt.figure(figsize=(8, 4))
            plt.plot(sorted_dates, totals, marker='o', linestyle='-', color='green')
            plt.title("Total Spent Per Day")
            plt.xlabel("Date")
            plt.ylabel("Amount ($)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        
        except Exception as e:
            print("🚫 Failed to generate total-spending graph:", e)



    def refresh_expenses(self):
        box = self.ids.expense_box
        box.clear_widgets()
        today = datetime.now().strftime("%Y-%m-%d")
        expenses = self.user_data["expenses"].get(today, [])
        total = sum(item[0] for item in expenses)

        if not expenses:
            box.add_widget(Label(text="No expenses today.", font_size=16))
        else:
            for i, (amount, name, _) in enumerate(expenses):
                row = BoxLayout(size_hint_y=None, height=40, spacing=10)
            
                label = Label(
                    text=f"{name}: ${amount:.2f}",
                    font_size=16,
                    size_hint_x=0.6
                )
            
                edit_btn = Button(
                    text="[EDIT]",
                    size_hint_x=0.2,
                    on_press=lambda btn, i=i: self.edit_expense(i)
                )
            
                del_btn = Button(
                    text="[DEL]",
                    size_hint_x=0.2,
                    on_press=lambda btn, i=i: self.delete_expense(i)
                )
            
                row.add_widget(label)
                row.add_widget(edit_btn)
                row.add_widget(del_btn)
            
                box.add_widget(row)

            

        box.add_widget(Label(
            text=f"Spent: ${total:.2f} / ${self.user_data.get('budget', 0.0):.2f}",
            font_size=18,
            size_hint_y=None,
            height=40
        ))
        
    def edit_expense(self, index):
        today = datetime.now().strftime("%Y-%m-%d")
        current = self.user_data["expenses"][today][index]
        current_amount, current_name, current_category = current
    
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
    
        name_input = TextInput(text=current_name, multiline=False, hint_text="Name")
        amount_input = TextInput(text=str(current_amount), multiline=False, hint_text="Amount", input_filter='float')
    
        save_btn = Button(text="Save", size_hint_y=None, height=40)
        cancel_btn = Button(text="Cancel", size_hint_y=None, height=40)
    
        btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btns.add_widget(save_btn)
        btns.add_widget(cancel_btn)
    
        layout.add_widget(Label(text="Edit Expense", size_hint_y=None, height=30))
        layout.add_widget(name_input)
        layout.add_widget(amount_input)
        layout.add_widget(btns)
    
        popup = Popup(title="Edit Expense", content=layout, size_hint=(0.75, 0.5), auto_dismiss=False)
    
        def save_changes(instance):
            try:
                new_name = name_input.text.strip()
                new_amount = float(amount_input.text.strip())
                self.user_data["expenses"][today][index] = [new_amount, new_name, current_category]
                save_data()
                self.refresh_expenses()
                popup.dismiss()
            except ValueError:
                print("❌ Invalid amount")
    
        save_btn.bind(on_press=save_changes)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
    
        popup.open()
        
    def delete_expense(self, index):
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.user_data["expenses"] and 0 <= index < len(self.user_data["expenses"][today]):
            del self.user_data["expenses"][today][index]
            save_data()
            self.refresh_expenses()



class MoodTrackerScreen(Screen):
    def load_user(self, username):
        self.username = username
        self.user_data = data["users"][username]
        self.refresh_moods()
    
    def log_mood(self):
        try:
            mood = int(self.ids.mood_input.text.strip())
            if not 1 <= mood <= 5:
                return
        except ValueError:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.user_data["moods"][today] = mood
        self.ids.mood_input.text = ""
        save_data()
        self.refresh_moods()
    
    def refresh_moods(self):
        box = self.ids.mood_box
        box.clear_widgets()
        moods = self.user_data.get("moods", {})
        emojis = ["😞", "😐", "🙂", "😊", "😄"]

        if not moods:
            box.add_widget(Label(text="No mood records yet.", font_size=16, size_hint_y=None, height=30))
            return

        for date in sorted(moods):
            mood = moods[date]
            emoji = emojis[mood - 1]
            box.add_widget(Label(
                text=f"{date}: {emoji} ({mood})",
                font_size=16,
                size_hint_y=None,
                height=30
            ))
    
    def show_mood_graph(self):
        moods = self.user_data.get("moods", {})
        if not moods:
            print("📭 No mood data to graph.")
            return
    
        dates = sorted(moods.keys())
        values = [moods[d] for d in dates]
        emoji_labels = ["😞", "😐", "🙂", "😊", "😄"]

        try:
            plt.figure(figsize=(8, 4))
            plt.plot(dates, values, marker='o', linestyle='-', color='blue')
            plt.title("Mood Over Time")
            plt.xlabel("Date")
            plt.ylabel("Mood")
            plt.ylim(0.5, 5.5)
            plt.yticks([1, 2, 3, 4, 5], emoji_labels)
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print("🚫 Failed to generate mood graph:", e)

    

class SmartLifeApp(App):
    def build(self):
        load_data()
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TaskManagerScreen(name="tasks"))
        sm.add_widget(BudgetManagerScreen(name="budget"))
        sm.add_widget(MoodTrackerScreen(name="mood"))
        return sm


if __name__ == "__main__":
    import traceback
    try:
        SmartLifeApp().run()
    except Exception as e:
        print("❌ An unexpected error occurred:")
        traceback.print_exc()

        # Write the error to a file so it’s preserved even if the window closes
        with open("error_log.txt", "w") as f:
            traceback.print_exc(file=f)

        # Pause so user sees it if launched by double-click
        input("\nPress Enter to exit...")
