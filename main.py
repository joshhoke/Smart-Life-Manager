# Smart Life Manager
from datetime import datetime
import json
import os

# Global data
data = {
    "tasks": [],
    "budget": 0.0,
    "expenses": {}  # Expenses by date
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
    print("3. Mood Tracker (coming soon)")
    print("4. Exit")

# == Budget Tracker ==

def budget_menu():
    today = datetime.now().strftime("%Y-%m-%d")
    expenses_today = data["expenses"].get(today, [])


    while True:
        print("\n------------------------------------------")
        print("\n💰 Budget Manager")
        print("1. Set daily budget")
        print("2. Add an expense")
        print("3. View today's spending")
        print("4. Edit an expense")
        print("5. Reset expenses")
        print("6. Go back")
        print("\n------------------------------------------\n\n")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            try:
                new_budget = float(input("Enter daily budget: $"))
                if new_budget < 0:
                    print("🚫 Budget can’t be negative.")
                else:
                    data["budget"] = new_budget
                    save_data()
                    print(f"✅ Budget set to ${data['budget']:.2f}")
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
        
                if today not in data["expenses"]:
                    data["expenses"][today] = []
        
                data["expenses"][today].append(entry)
                save_data()
                print(f"✅ Added {name} (${amount:.2f}) under {category} for {today}")
            except ValueError:
                print("🚫 Invalid amount.")
        elif choice == "3":
            expenses_today = data["expenses"].get(datetime.now().strftime("%Y-%m-%d"), [])
            if not expenses_today:
                print("📭 No expenses logged.")
            else:
                total = sum(item[0] for item in expenses_today)
                print("\n📊 Today's Expenses:")
                for amount, note, category in expenses_today:
                    print(f"- ${amount:.2f} for {note} [{category}]")
                    print(f"\nTotal: ${total:.2f}")
                    print(f"Remaining: ${data['budget'] - total:.2f}")
        elif choice == "4":
                confirm = input("Are you sure you want to reset today's expenses? (y/n): ").lower()
                if confirm == "y":
                    expenses_today.clear()
                    data["expenses"][today] = expenses_today
                    save_data()
                    print("🔄 Expenses reset.")
                else:
                    print("❌ Cancelled.")
        elif choice == "5":
            if not data["expenses"]:
                print("❌ No expenses recorded.")
                continue
            print("📅 Dates with expenses:")
            for i, date in enumerate(data["expenses"], 1):
                print(f"{i}. {date}")
            try:
                date_choice = int(input("Choose a date by number: "))
                dates = list(data["expenses"].keys())
                selected_date = dates[date_choice - 1]
                expenses_on_date = data["expenses"][selected_date]
        
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
        
                    # Apply edits if provided
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
            break
        else:
            print("❌ Invalid option.")

# == Task Manager ==

def task_menu():
    global tasks
    while True:
        print_task_menu()

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            task = input("Enter your task: ")
            data["tasks"].append(task)
            save_data()
            print(f"✅ Task added: {task}")
        elif choice == "2":
            if not data["tasks"]:
                print("📭 No tasks found.")
            else:
                print("\n📋 Your Tasks:")
                for i, task in enumerate(data["tasks"], 1):
                    print(f"{i}. {task}")
        elif choice == "3":
            if not data['tasks']:
                print("❌ No tasks available")
                continue
            for i, task in enumerate(data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Enter task number to delete: "))
                if 1 <= task_num <= len(data["tasks"]):
                    data["tasks"][task_num - 1] += " ✅"
                    print(f"Task marked complete: {data['tasks'][task_num - 1]}")
                    save_data()
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")
        elif choice == "4":
            if not data['tasks']:
                print("❌ No tasks to delete.")
                continue
            for i, task in enumerate(data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Enter task number to delete: "))
                if 1 <= task_num <= len(data["tasks"]):
                    removed = data["tasks"].pop(task_num - 1)
                    save_data()
                    print(f"🗑️ Deleted: {removed}")
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")
        elif choice == "5":
            if not data["tasks"]:
                print("❌ No tasks to edit.")
                continue
            for i, task in enumerate(data["tasks"], 1):
                print(f"{i}. {task}")
            try:
                task_num = int(input("Task number to edit: "))
                if 1 <= task_num <= len(data["tasks"]):
                    new_name = input("Enter new task name: ")
                    data["tasks"][task_num - 1] = new_name
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
    
    while True:
        print_top_menu()

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            task_menu()
        elif choice == "2":
            budget_menu()
        elif choice == "3":
            print("📊 Mood tracking coming soon.")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    load_data()
    main()
