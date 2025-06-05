# Smart Life Manager - Day 1 Menu

def main():
    while True:
        print("\n🌟 Welcome to the Smart Life Manager")
        print("1. Manage Tasks")
        print("2. Manage Budget (coming soon)")
        print("3. Mood Tracker (coming soon)")
        print("4. Exit")

        choice = input("Choose an option (1–4): ")

        if choice == "1":
            print("🔧 Task Manager is under construction.")
        elif choice == "2":
            print("💰 Budget feature coming soon.")
        elif choice == "3":
            print("📊 Mood tracking coming soon.")
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
