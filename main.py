import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="atm"
)
cursor = db.cursor()

# ATM Functions
def check_balance(account_number):
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def withdraw(account_number, amount):
    cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        balance = result[0]
        if balance >= amount:
            new_balance = balance - amount
            cursor.execute("UPDATE users SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            db.commit()
            return f"Withdrawn ${amount}. New balance: ${new_balance}"
        else:
            return "Insufficient funds."
    else:
        return "Account not found."

def main():
    while True:
        account_number = int(input("Enter your account number: "))
        pin = int(input("Enter your PIN: "))

        cursor.execute("SELECT * FROM users WHERE account_number = %s AND pin = %s", (account_number, pin))
        result = cursor.fetchone()

        if result:
            while True:
                print("\n1. Check Balance\n2. Withdraw\n3. Exit")
                choice = int(input("Enter your choice: "))

                if choice == 1:
                    balance = check_balance(account_number)
                    print(f"Your balance is: ${balance}")

                elif choice == 2:
                    amount = float(input("Enter the amount to withdraw: "))
                    result = withdraw(account_number, amount)
                    print(result)

                elif choice == 3:
                    print("Thank you for using our ATM. Goodbye!")
                    db.close()
                    return

                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid account number or PIN. Please try again.")

if __name__ == "__main__":
    main()