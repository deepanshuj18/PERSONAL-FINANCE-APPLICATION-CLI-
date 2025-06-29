
from auth import register, login
from db import init_db
from finance import add_transaction, view_transactions, update_transaction, delete_transaction
from reports import monthly_report, yearly_report
from budget import set_budget, check_budget_warning
from backup_restore import backup_database, restore_database



def dashboard(user_id):
    while True:
        print("1. Add Transaction\n2. View Transactions\n3. Update Transaction\n4. Delete Transaction")
        print("5. Logout\n6. Monthly Report\n7. Yearly Report")
        print("8. Set Budget\n9. Check Budget Status")
        print("10. Backup Data\n11. Restore Data")

        choice = input("Select option: ").strip()

        if choice == '1':
            t_type = input("Enter type (income/expense): ").strip().lower()
            if t_type == 'income':
                source_income=input("enter source of income: ").strip().lower()
                amount = float(input("Amount: "))
                desc = input("Description (optional): ")
                add_transaction(user_id, t_type, source_income, amount, desc)
            else:
                category = input("Category (e.g., Food, Rent): ").strip()
                amount = float(input("Amount: "))
                desc = input("Description (optional): ")
                add_transaction(user_id, t_type, category, amount, desc)

        elif choice == '2':
            view_transactions(user_id)

        elif choice == '3':
            tid = int(input("Transaction ID to update: "))
            new_amt = float(input("New amount: "))
            update_transaction(user_id, tid, new_amt)

        elif choice == '4':
            tid = int(input("Transaction ID to delete: "))
            delete_transaction(user_id, tid)

        elif choice == '5':
            print("👋 Logging out...")
            break
        elif choice == '6':
            month = input("Enter month (1-12): ").strip()
            year = input("Enter year (e.g., 2025): ").strip()
            monthly_report(user_id, month, year)
        elif choice == '7':
            year = input("Enter year (e.g., 2025): ").strip()
            yearly_report(user_id, year)
        elif choice == '8':
            category = input("Enter category to set budget for: ").strip()
            amount = float(input("Budget Amount: "))
            month = input("Month (1-12): ")
            year = input("Year: ")
            set_budget(user_id, category, amount, month, year)

        elif choice == '9':
            category = input("Enter category to check: ").strip()
            month = input("Month (1-12): ")
            year = input("Year: ")
            check_budget_warning(user_id, category, month, year)
        elif choice == '10':
            backup_database()

        elif choice == '11':
            restore_database()



        else:
            print("❌ Invalid option.")




def main():
    init_db()
    print("=== Personal Finance Management ===")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            username = input("Enter a username: ").strip()
            password = input("Enter a password: ").strip()
            register(username, password)

        elif choice == '2':
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            user_id = login(username, password)
            if user_id:
                dashboard(user_id)

        elif choice == '3':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
