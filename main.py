# Smart Life Manager
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.progress import Progress, BarColumn, TextColumn
data = {
    "users": {},

}

DATA_FILE = "data.json"

def open_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                loaded = json.load(f)
                data.update(loaded)
            except json.JSONDecodeError:
                print("⚠️ Data file corrupt. Starting fresh.")
                data = {"users": {}}

def save_data(user_data):
    #print("📦 Saving this to file:", json.dumps(data, indent=2))  # print it out first
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
def ensure_user_initialized(username):
    if "users" not in data:
        data["users"] = {}

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



# Global data
console = Console()
data = {
    "users": {},

}
#first func of data.py was originally here


def main():
    
    username = input("Enter your name: ").strip()
    usnRef = username

    open_data()
    ensure_user_initialized(username)
    level_system(username)
    
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = data['users'][username]

    #Give EXP
    user_data["xp"] += 1
    
    #Level up if enough
    if user_data["xp"] >= user_data["level"] * 100:
        user_data["level"] += 1
        print(f"You leveled up! You're now level {user_data['level']}!")
    
    #Update streak
    
    last_day = user_data["last_task_day"]
    if last_day:
        last = datetime.strptime(last_day, "%Y-%m-%d").date()
        now = datetime.now().date()
        if (now - last).days == 1:
            user_data["streak"] += 1
        elif (now - last).days > 1:
            user_data["streak"] =1
            
    else:
        user_data["streak"] = 1
        
    user_data["last_task_day"] = today


    

    while True:
        display_dashboard(username)
        choice = input("Choose an option (1–4): ")
        if choice == "1":
            task_menu(user_data)
        elif choice == "2":
            budget_menu(user_data, username)
        elif choice == "3":
            mood_menu(user_data)
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice.")


def display_dashboard(username):
    user_data = data["users"][username]
    today = datetime.now().strftime("%Y-%m-%d")

    console.print(f"[bold cyan]\\n📊 DAILY DASHBOARD — {today}[/bold cyan]")
    console.print(f"👤 [yellow]{username}[/yellow]")

    # XP Bar
    xp = user_data["xp"]
    level = user_data["level"]
    next_xp = level * 100
    percent = int((xp / next_xp) * 100)
    
    with Progress(
        TextColumn("[bold green]🏆 Level {task.fields[level]}[/bold green]"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=True,
    ) as progress:
        bar = progress.add_task("", level=level, total=next_xp, completed=xp)

    # Streak
    console.print(f"🔥 [bold red]Streak:[/bold red] {user_data['streak']} day(s)")

    # Tasks
    todays_tasks = user_data.get("tasks", [])
    if todays_tasks:
        console.print("📝 [bold]Tasks:[/bold]")
        for task in todays_tasks:
            check = "✅" if "✅" in task else "⬜"
            console.print(f"   {check} {task}")
    else:
        console.print("📝 No tasks added today.")

    # Budget
    total_spent = sum(exp[0] for exp in user_data["expenses"].get(today, []))
    budget = user_data["budget"]
    console.print(f"💰 [bold]Budget:[/bold] Used ${total_spent:.2f} / ${budget:.2f}")

    # Mood
    mood = user_data["moods"].get(today)
    if mood:
        emoji = ["😞", "😐", "🙂", "😊", "😄"][mood - 1]
        console.print(f"🎭 Mood: {emoji} ({mood}) [green]Logged[/green]")
    else:
        console.print("🎭 Mood: [yellow]Not logged today.[/yellow]")
        
    console.print(Panel.fit(
        f"[bold cyan]🌟 SMART LIFE MANAGER[/bold cyan]\n"
        f"[yellow]👤 {username}[/yellow] | "
        f"[green]Level {user_data['level']}[/green] | "
        f"[magenta]XP: {user_data['xp']}[/magenta] | "
        f"[red]🔥 Streak: {user_data['streak']} days[/red]",
        border_style="blue",
        box=box.ROUNDED
    ))
    print("1. Manage Tasks")
    print("2. Manage Budget")
    print("3. Mood Tracker")
    print("4. Exit")



def level_system(username):
    today = datetime.now().strftime("%Y-%m-%d")
    user_data = data['users'][username]
    
    #Give EXP
    user_data["xp"] += 1
    
    #Level up if enough
    if user_data["xp"] >= user_data["level"] * 100:
        user_data["level"] += 1
        print(f"You leveled up! You're now level {user_data['level']}!")
    
    #Update streak
    
    last_day = user_data["last_task_day"]
    if last_day:
        last = datetime.strptime(last_day, "%Y-%m-%d").date()
        now = datetime.now().date()
        if (now - last).days == 1:
            user_data["streak"] += 1
        elif (now - last).days > 1:
            user_data["streak"] =1
            
    else:
        user_data["streak"] = 1
        
    user_data["last_task_day"] = today


def load_dadta():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                loaded = json.load(f)
                data.update(loaded)
            except json.JSONDecodeError:
                print("⚠️ Couldn't read data file — starting fresh.")
    else:
        save_data(user_data)

def save_dadta(user_data):
    #print("📦 Saving this to file:", json.dumps(data, indent=2))  # print it out first
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
    
def ensure_udser_initialized(username):
    if "users" not in data:
        data["users"] = {}

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

# == Printed Task Menu ==

def print_task_menu():
    console.print(Panel.fit(
        "[bold yellow]📝 TASK MANAGER[/bold yellow]\n\n"
        "[cyan]1.[/cyan] Add a task\n"
        "[cyan]2.[/cyan] View all tasks\n"
        "[cyan]3.[/cyan] Mark a task as complete\n"
        "[cyan]4.[/cyan] Delete a task\n"
        "[cyan]5.[/cyan] Edit a task\n"
        "[cyan]6.[/cyan] Go back",
        title="📋 Options",
        border_style="bright_blue",
        box=box.ROUNDED
    ))


# == Top Main Menu ==

def print_top_menu(user_data, username):
    console.print(Panel.fit(
        f"[bold cyan]🌟 SMART LIFE MANAGER[/bold cyan]\n"
        f"[yellow]👤 {username}[/yellow] | "
        f"[green]Level {user_data['level']}[/green] | "
        f"[magenta]XP: {user_data['xp']}[/magenta] | "
        f"[red]🔥 Streak: {user_data['streak']} days[/red]",
        border_style="blue",
        box=box.ROUNDED
    ))
    print("1. Manage Tasks")
    print("2. Manage Budget")
    print("3. Mood Tracker")
    print("4. Exit")

# == Budget Tracker ==

def budget_menu(user_data, username):
    today = datetime.now().strftime("%Y-%m-%d")
    expenses_today = user_data["expenses"].get(today, [])

    while True:
        console.print(Panel.fit(
            "[bold yellow]💰 BUDGET MANAGER[/bold yellow]\n\n"
            "[cyan]1.[/cyan] Set daily budget\n"
            "[cyan]2.[/cyan] Add an expense\n"
            "[cyan]3.[/cyan] View today’s spending\n"
            "[cyan]4.[/cyan] Edit an expense\n"
            "[cyan]5.[/cyan] Reset expenses\n"
            "[cyan]6.[/cyan] Graph expenses\n"
            "[cyan]7.[/cyan] Go back",
            title="💼 Options",
            border_style="bright_blue",
            box=box.ROUNDED
        ))

        choice = input("Choose an option (1–7): ")

        if choice == "1":
            try:
                new_budget = float(input("Enter daily budget: $"))
                if new_budget < 0:
                    print("🚫 Budget can’t be negative.")
                else:
                    user_data["budget"] = new_budget
                    save_data(user_data)
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
                save_data(user_data)
                print(f"✅ Added {name} (${amount:.2f}) under {category} for {today}")
            except ValueError:
                print("🚫 Invalid amount.")

        elif choice == "3":
            expenses_today = user_data["expenses"].get(today, [])
            if not expenses_today:
                console.print("📭 [bold yellow]No expenses logged for today.[/bold yellow]")
            else:
                total = sum(item[0] for item in expenses_today)
                remaining = user_data["budget"] - total
            
                table = Table(title="📊 Today's Expenses", box=box.ROUNDED, style="white")
                table.add_column("Amount", justify="right", style="cyan", no_wrap=True)
                table.add_column("Note", style="magenta")
                table.add_column("Category", style="green")
            
                for amount, note, category in expenses_today:
                    table.add_row(f"${amount:.2f}", note, category)
            
                console.print(table)
            
                console.print(f"💸 [bold cyan]Total:[/bold cyan] ${total:.2f}")
                console.print(f"💼 [bold green]Remaining Budget:[/bold green] ${remaining:.2f}")


        elif choice == "4":
            confirm = input("Are you sure you want to reset today's expenses? (y/n): ").lower()
            if confirm == "y":
                expenses_today.clear()
                user_data["expenses"][today] = expenses_today
                save_data(user_data)
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
                    save_data(user_data)
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

def mood_menu(user_data):
    today = datetime.now().strftime("%Y-%m-%d")

    while True:
        console.print(Panel.fit(
            "[bold yellow]🎭 MOOD TRACKER[/bold yellow]\n\n"
            "[cyan]1.[/cyan] Log today’s mood\n"
            "[cyan]2.[/cyan] View mood history\n"
            "[cyan]3.[/cyan] Show mood graph 📈\n"
            "[cyan]4.[/cyan] Go back",
            title="📈 Options",
            border_style="bright_magenta",
            box=box.ROUNDED
        ))


        choice = input("Choose an option: ")

        if choice == "1":
            try:
                mood = int(input("How do you feel today (1 = 😞 to 5 = 😄)? "))
                if 1 <= mood <= 5:
                    user_data["moods"][today] = mood
                    save_data(user_data)
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

def task_menu(user_data):
    while True:
        print_task_menu()
        choice = input("Choose an option (1–6): ")

        if choice == "1":
            task = input("Enter your task: ")
            user_data["tasks"].append(task)
            save_data(user_data)
            print(f"✅ Task added: {task}")

        elif choice == "2":
            if not user_data["tasks"]:
                print("📭 No tasks found.")
            else:
                table = Table(title="📋 Your Tasks", box=box.SQUARE)
                table.add_column("No.", justify="right", style="cyan")
                table.add_column("Task", style="white")
                
                for i, task in enumerate(user_data["tasks"], 1):
                    table.add_row(str(i), task)
                
                console.print(table)



        elif choice == "3":  # Complete task
            if not user_data["tasks"]:
                print("❌ No tasks available")
                continue
            table = Table(title="📋 Your Tasks", box=box.SQUARE)
            table.add_column("No.", justify="right", style="cyan")
            table.add_column("Task", style="white")
                
            for i, task in enumerate(user_data["tasks"], 1):
                table.add_row(str(i), task)
            try:
                task_num = int(input("Enter task number to mark complete: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    user_data["tasks"][task_num - 1] += " ✅"
                    today = datetime.now().strftime("%Y-%m-%d")
                    completed_today = user_data["completed_today"].get(today, 0) + 1
                    user_data["completed_today"][today] = completed_today

                    if completed_today == 3:
                        print("🏆 You’ve completed 3 tasks today! +75 XP")
                        user_data["xp"] += 75
                    else:
                        user_data["xp"] += 25
                        print(f"✅ Task completed. +25 XP")

                    save_data(user_data)
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "4":
            if not user_data['tasks']:
                print("❌ No tasks to delete.")
                continue
            table = Table(title="📋 Your Tasks", box=box.SQUARE)
            table.add_column("No.", justify="right", style="cyan")
            table.add_column("Task", style="white")
            
            for i, task in enumerate(user_data["tasks"], 1):
                table.add_row(str(i), task)
            
            console.print(table)

            try:
                task_num = int(input("Enter task number to delete: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    removed = user_data["tasks"].pop(task_num - 1)
                    save_data(user_data)
                    print(f"🗑️ Deleted: {removed}")
                else:
                    print("🚫 Invalid number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "5":
            if not user_data["tasks"]:
                print("❌ No tasks to edit.")
                continue
            table = Table(title="📋 Your Tasks", box=box.SQUARE)
            table.add_column("No.", justify="right", style="cyan")
            table.add_column("Task", style="white")
            
            for i, task in enumerate(user_data["tasks"], 1):
                table.add_row(str(i), task)
            try:
                task_num = int(input("Task number to edit: "))
                if 1 <= task_num <= len(user_data["tasks"]):
                    new_name = input("Enter new task name: ")
                    user_data["tasks"][task_num - 1] = new_name
                    save_data(user_data)
                    print("✅ Task updated.")
                else:
                    print("🚫 Invalid task number.")
            except ValueError:
                print("🚫 Please enter a number.")

        elif choice == "6":
            break
        else:
            print("❌ Invalid option.")







main()





