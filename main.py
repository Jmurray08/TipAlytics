from src.database import initialize_db
from src.shift_logger import log_shift

def menu():
    print("=== Inn Tracker ===\n")
    while True:
        print("Options:")
        print("1. Add a new shift")
        print("2. Exit")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            log_shift()
        elif choice == "2":
            print("Thank you for your entries!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.\n")

if __name__ == "__main__":
    initialize_db()
    menu()
