# Smart Life Manager
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

# Global data
data = {
    "users": {},
    "tasks": [],
    "budget": 0.0,
    "expenses": {},  # Expenses by date
    "completed_today": {},
    "moods": {}
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                loaded = json.load(f)
                data.update(loaded)
            except json.JSONDecodeError:
                print("⚠️ Couldn't read data file — starting fresh.")
    else:
        save_data()

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        

# == Printed Task Menu ==

def print_task_menu():
    print("\n📝 Task Manager")
    print("1. Add a task")
    print("2. View all tasks")
    print("3. Mark a task as complete")
    print("4. Delete a task")
    print("5. Edit a task")
    print("6. Go back")

# == Top Main Menu ==

def print_top_menu():
    print("\n🌟 Welcome to the Smart Life Manager")
    print("1. Manage Tasks")
    print("2. Manage Budget")
    print("3. Mood Tracker")
    print("4. Exit")

# == Budget Tracker ==

def budget_menu():
    user_data = data["users"][username]
    today = datetime.now().strftime("%Y-%m-%d")
    expenses_today = user_data["expenses"].get(today, [])

    while True:
        print("\n------------------------------------------")
        print("\n💰 Budget Manager")
        print("1. Set daily budget")
        print("2. Add an expense")
        print("3. View today's spending")
        print("4. Edit an expense")
        print("5. Reset expenses")
        print("6. Show expense graph")
        print("7. Go back")
        print("\n------------------------------------------\n\n")

        choice = input("Choose an option (1–7): ")

        if choice == "1":
            try:
                new_budget = float(input("Enter daily budget: $"))
                if new_budget < 0:
                    print("🚫 Budget can’t be negative.")
                else:
                    user_data["budget"] = new_budget
                    save_data()
                    print(f"✅ Budget set to ${user_data['budget']:.2f}")
            except ValueError:
                print("🚫 Invalid number.")

        elif choice == "2":
            name = input("Expense name: ")
            try:
                amount = float(input("Amount: $"))
                if amount < 0:
                    print("🚫 Amount can’t be negative.")
                    return
                print("📂 Category: [1] Need, [2] Want, [3] Saving")
                category_choice = input("Choose category: ")
                category_map = {"1": "Need", "2": "Want", "3": "Saving"}
                category = category_map.get(category_choice, "Uncategorized")

                today = str(datetime.now().date())
                entry = [amount, name, category]

                if today not in user_data["expenses"]:
                    user_data["expenses"][today] = []

                user_data["expenses"][today].append(entry)
                save_data()
                print(f"✅ Added {name} (${amount:.2f}) under {category} for {today}")
            except ValueError:
                print("🚫 Invalid amount.")

        elif choice == "3":
            expenses_today = user_data["expenses"].get(today, [])
            if not expenses_today:
                print("📭 No expenses logged.")
            else:
                total = sum(item[0] for item in expenses_today)
                print("\n📊 Today's Expenses:")
                for amount, note, category in expenses_today:
                    print(f"- ${amount:.2f} for {note} [{category}]")
                print(f"\nTotal: ${total:.2f}")
                print(f"Remaining: ${user_data['budget'] - total:.2f}")

        elif choice == "4":
            confirm = input("Are you sure you want to reset today's expenses? (y/n): ").lower()
            if confirm == "y":
                expenses_today.clear()
                user_data["expenses"][today] = expenses_today
                save_data()
                print("🔄 Expenses reset.")
            else:
                print("❌ Cancelled.")

        elif choice == "5":
            if not user_data["expenses"]:
                print("❌ No expenses recorded.")
                continue
            print("📅 Dates with expenses:")
            for i, date in enumerate(user_data["expenses"], 1):
                print(f"{i}. {date}")
            try:
                date_choice = int(input("Choose a date by number: "))
                dates = list(user_data["expenses"].keys())
                selected_date = dates[date_choice - 1]
                expenses_on_date = user_data["expenses"][selected_date]

                for j, entry in enumerate(expenses_on_date, 1):
                    amount, name, category = entry
                    print(f"{j}. {name} - ${amount:.2f} [{category}]")

                expense_choice = int(input("Choose expense to edit: "))
                if 1 <= expense_choice <= len(expenses_on_date):
                    new_name = input("New name (leave blank to keep): ")
                    new_amount = input("New amount (leave blank to keep): ")
                    print("📂 Category: [1] Need, [2] Want, [3] Saving, [Enter] to keep")
                    new_cat_input = input("Choose new category or press Enter: ")

                    amount, name, category = expenses_on_date[expense_choice - 1]

                    if new_name:
                        name = new_name
                    if new_amount:
                        try:
                            amt = float(new_amount)
                            if amt >= 0:
                                amount = amt
                            else:
                                print("🚫 Cannot enter negative amounts.")
                                continue
                        except ValueError:
                            print("🚫 Invalid number.")
                            continue
                    if new_cat_input:
                        cat_map = {"1": "Need", "2": "Want", "3": "Saving"}
                        category = cat_map.get(new_cat_input, category)

                    expenses_on_date[expense_choice - 1] = [amount, name, category]
                    save_data()
                    print("✅ Expense updated.")
                else:
                    print("🚫 Invalid selection.")
            except (ValueError, IndexError):
                print("🚫 Invalid input.")
        elif choice == "6":
            try:
                user_expenses = data["users"][username]["expenses"]
                if not user_expenses:
                    print("📭 No expense data to graph.")
                    continue
        
                dates = sorted(user_expenses.keys())
                totals = []
        
                for date in dates:
                    day_entries = user_expenses[date]
                    daily_total = sum(entry[0] for entry in day_entries)
                    totals.append(daily_total)
        
                plt.figure(figsize=(8, 4))
                plt.plot(dates, totals, marker='o', color='green')
                plt.title("Daily Spending")
                plt.xlabel("Date")
                plt.ylabel("Amount ($)")
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.tight_layout()
                plt.show()
        
            except Exception as e:
                print("🚫 Couldn’t generate graph:", e)

        elif choice == "7":
            break
        else:
            print("❌ Invalid option.")

# == Mood Tracker ==

def mood_menu():
    user_data = data["users"][username]
    today = datetime.now().strftime("%Y-%m-%d")

    while True:
        print("\n🎭 Mood Tracker")
        print("1. Log today’s mood")
        print("2. View mood history")
        print("3. Show mood graph")
        print("4. Go back")

        choice = input("Choose an option: ")

        if choice == "1":
            try:
                mood = int(input("How do you feel today (1 = 😞 to 5 = 😄)? "))
                if 1 <= mood <= 5:
                    user_data["moods"][today] = mood
                    save_data()
                    print("✅ Mood recorded.")
                else:
                    print("🚫 Must be between 1 and 5.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "2":
            if not user_data["moods"]:
                print("📭 No mood records yet.")
            else:
                print("📈 Mood History:")
                for date, mood in sorted(user_data["moods"].items()):
                    emoji = ["😞", "😐", "🙂", "😊", "😄"][mood - 1]
                    print(f"{date}: {emoji} ({mood})")
        elif choice == "3":
            if not user_data["moods"]:
                print("📭 No mood data to graph.")
                continue
        
            try:
                mood_dict = user_data["moods"]
                print("📅 Mood Data:", mood_dict)
        
                dates = sorted(mood_dict.keys())
                moods = [mood_dict[date] for date in dates]
        
                if not moods:
                    print("⚠️ No mood values to plot.")
                    continue
        
                plt.figure(figsize=(8, 4))
                plt.plot(dates, moods, marker='o', linestyle='-', color='blue')
                plt.ylim(0.5, 5.5)
                plt.yticks([1, 2, 3, 4, 5], ["😞", "😐", "🙂", "😊", "😄"])
                plt.xticks(rotation=45)
                plt.title("Mood Over Time")
                plt.xlabel("Date")
                plt.ylabel("Mood")
                plt.tight_layout()
                plt.grid(True)
                plt.show()
        
            except Exception as e:
                print("🚫 Failed to plot mood graph:", e)

        elif choice == "4":
            break
        else:
            print("❌ Invalid option.")


# == Task Manager ==

def task_menu():
    user_data = data["users"][username]
    while True:
        print_task_menu()
        choice = input("Choose an option (1–6): ")

        if choice == "1":
            task = input("Enter your task: ")
            user_data["tasks"].append(task)
            save_data()
            print(f"✅ Task added: {task}")

        elif choice == "2":
            if not user_data["tasks"]:
                print("📭 No tasks found.")
            else:
                print("\n📋 Your Tasks:")
                for i, task in enumerate(user_data["tasks"], 1):
                    print(f"{i}. {task}")

        elif choice == "3":
            if not user_data['tasks']:
                print("❌ No tasks available")
                continue
            for i, task in enumerate(user_data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Enter task number to mark complete: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    user_data["tasks"][task_num - 1] += " ✅"
                    today = datetime.now().strftime("%Y-%m-%d")
                    if "completed_today" not in user_data:
                        user_data["completed_today"] = {}
                    user_data["completed_today"][today] = user_data["completed_today"].get(today, 0) + 1
                    if user_data["completed_today"][today] >= 3:
                        print("🏆 Congratulations! You’ve hit your daily goal!")
                    print(f"Task marked complete: {user_data['tasks'][task_num - 1]}")
                    save_data()
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "4":
            if not user_data['tasks']:
                print("❌ No tasks to delete.")
                continue
            for i, task in enumerate(user_data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Enter task number to delete: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    removed = user_data["tasks"].pop(task_num - 1)
                    save_data()
                    print(f"🗑️ Deleted: {removed}")
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "5":
            if not user_data["tasks"]:
                print("❌ No tasks to edit.")
                continue
            for i, task in enumerate(user_data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Task number to edit: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    new_name = input("Enter new task name: ")
                    user_data["tasks"][task_num - 1] = new_name
                    save_data()
                    print("✅ Task updated.")
                else:
                    print("🚫 Invalid task number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "6":
            break
        else:
            print("❌ Invalid option.")




DATA_FILE = "data.json"


def main():
    global username
    
    username = input("Enter your username: ").strip()
    
    if username not in data["users"]:
        print(f"Welcome, {username}! Your data will be created")
        data["users"][username] = {
            "tasks": [],
            "budget": 0.0,
            "expenses": {},
            "moods": {}
        }
        
    print(f"🧑 Welcome, {username}!")
    
    while True:
        print_top_menu()

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            task_menu()
        elif choice == "2":
            budget_menu()
        elif choice == "3":
            mood_menu()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    load_data()
    main()
