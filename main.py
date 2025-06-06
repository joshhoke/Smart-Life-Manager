# Smart Life Manager - Day 1 Menu

tasks = []
budget = 0.0
expenses = []

def main():
    
    
    
    def budget_menu():
        global budget, expenses
    
        while True:
            print("\n💰 Budget Manager")
            print("1. Set daily budget")
            print("2. Add an expense")
            print("3. View today's spending")
            print("4. Reset expenses")
            print("5. Go back")
    
            choice = input("Choose an option (1–4): ")
    
            if choice == "1":
                try:
                    budget = float(input("Enter your daily budget: $"))
                    print(f"✅ Daily budget set to ${budget:.2f}")
                except ValueError:
                    print("🚫 Please enter a valid number.")
            elif choice == "2":
                try:
                    amount = float(input("Enter expense amount: $"))
                    note = input("What was it for? ")
                    expenses.append((amount, note))
                    print(f"🧾 Expense added: ${amount:.2f} for '{note}'")
                except ValueError:
                    print("🚫 Please enter a valid number.")
            elif choice == "3":
                if not expenses:
                    print("📭 No expenses logged.")
                else:
                    total = sum(item[0] for item in expenses)
                    print("\n📊 Today's Expenses:")
                    for amount, note in expenses:
                        print(f"- ${amount:.2f} for {note}")
                    print(f"\nTotal: ${total:.2f}")
                    print(f"Remaining: ${budget - total:.2f}")
            elif choice == "4":
                confirm = input("Are you sure you want to reset today's expenses? (y/n): ").lower()
                if confirm == "y":
                    expenses.clear()
                    print("🔄 Expenses reset.")
                else:
                    print("❌ Cancelled.")
            elif choice == "5":
                break
            else:
                print("❌ Invalid option.")

    def task_menu():
        global tasks
        while True:
            print("\n📝 Task Manager")
            print("1. Add a task")
            print("2. View all tasks")
            print("3. Mark a task as complete")
            print("4. Delete a task")
            print("5. Go back")
    
            choice = input("Choose an option (1–4): ")
    
            if choice == "1":
                task = input("Enter your task: ")
                tasks.append(task)
                print(f"✅ Task added: {task}")
            elif choice == "2":
                if not tasks:
                    print("📭 No tasks found.")
                else:
                    print("\n📋 Your Tasks:")
                    for i, task in enumerate(tasks, 1):
                        print(f"{i}. {task}")
            elif choice == "3":
                if not tasks:
                    print("❌ No tasks available")
                    continue
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                try:
                    task_num = int(input("Enter task number to delete: "))
                    if 1 <= task_num <= len(tasks):
                        tasks[task_num - 1] += " ✅"
                        print(f"Task marked complete: {tasks[task_num - 1]}")
                    else:
                        print("🚫 Invalid number.")
                except ValueError:
                    print("🚫 Please enter a number.")
            elif choice == "4":
                if not tasks:
                    print("❌ No tasks to delete.")
                    continue
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
                try:
                    task_num = int(input("Enter task number to delete: "))
                    if 1 <= task_num <= len(tasks):
                        removed = tasks.pop(task_num - 1)
                        print(f"🗑️ Deleted: {removed}")
                    else:
                        print("🚫 Invalid number.")
                except ValueError:
                    print("🚫 Please enter a number.")
            elif choice == "5":
                break
            else:
                print("❌ Invalid option.")
    


    while True:
        print("\n🌟 Welcome to the Smart Life Manager")
        print("1. Manage Tasks")
        print("2. Manage Budget")
        print("3. Mood Tracker (coming soon)")
        print("4. Exit")

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
    main()
