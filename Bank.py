import random

class User:
    def __init__(self, name, email, address, account_type, bank):
        self.bank = bank
        self.account_number = None
        self.name = name
        self.email = email 
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0
    
    def deposit_amount(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f'Deposit: {amount}')
            return f'Deposit successful. New balance: {self.balance}'
        else:
            return 'Invalid deposit amount.'
    
    def withdraw_amount(self, amount):
        if amount > self.balance:
            return 'Withdrawal amount exceeded'
        elif amount > 0:
            self.balance -= amount
            self.transaction_history.append(f'Withdraw: {amount}')
            return f'Withdrawal successful. New balance: {self.balance}'
    
    def check_balance(self):
        return self.balance
    
    def view_transaction_history(self):
        return self.transaction_history
    
    def take_loan(self, amount):
        if self.loan_count >= 2:
            return 'Loan limit exceeded'
        elif amount <= 0:
            return 'Invalid loan amount'
        else:
            self.balance += amount
            self.loan_count += 1
            self.bank.total_loan_amount += amount
            self.transaction_history.append(f'Loan Taken: {amount}')
            return f'Loan of {amount} taken successfully. New balance: {self.balance}'
    
    def transfer_funds(self, amount, recipient_account):
        if amount <= 0:
            return 'Invalid transfer amount'
        elif amount > self.balance:
            return 'Insufficient balance for transfer'
        else:
            self.balance -= amount
            recipient_account.balance += amount
            self.transaction_history.append(f"Transferred amount {amount} to account {recipient_account.account_number}")
            recipient_account.transaction_history.append(f"Received amount {amount} from account {self.account_number}")
            return f'Transfer successful. New balance: {self.balance}'

class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_loan_amount = 0
        self.loan_feature_OnOff = True

    def generate_account_number(self):
        while True:
            account_number = str(random.randint(10000, 30000))
            if account_number not in self.accounts:
                return account_number

    def create_account(self, name, email, address, account_type):
        account_number = self.generate_account_number()
        new_account = User(name, email, address, account_type, self)
        new_account.account_number = account_number
        self.accounts[account_number] = new_account
        return account_number
    
    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            return f'Account {account_number} deleted'
        else:
            return f'Account does not exist'
    
    def list_accounts(self):
        return list(self.accounts.values())
    
    def total_balance(self):
        return sum(account.balance for account in self.accounts.values())
    
    def total_loan(self):
        return self.total_loan_amount
    
    def enable_loan_feature(self, enable):
        self.loan_feature_OnOff = enable
        return f'Loan feature {"enabled" if enable else "disabled"}'

def main():
    bank = Bank()
    while True:
        print("\nWelcome to the Banking Management System")
        print("1. User")
        print("2. Admin")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_menu(bank)
        elif choice == '2':
            admin_menu(bank)
        elif choice == '3':
            break
        else:
            print('Invalid Choice!!')

def user_menu(bank):
    while True:
        print("\nUser Menu")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Take Loan")
        print("7. Transfer Money")
        print("8. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter your address: ")
            account_type = input("Enter account type (Savings/Current): ")
            account_number = bank.create_account(name, email, address, account_type)
            print(f"Account created successfully. Your account number is {account_number}")

        elif choice == '2':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                amount = float(input("Enter amount to deposit: "))
                print(bank.accounts[account_number].deposit_amount(amount))
            else:
                print("Account does not exist.")

        elif choice == '3':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                amount = float(input("Enter amount to withdraw: "))
                print(bank.accounts[account_number].withdraw_amount(amount))
            else:
                print("Account does not exist.")

        elif choice == '4':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                balance = bank.accounts[account_number].check_balance()
                print(f"Available balance: {balance}")
            else:
                print("Account does not exist.")

        elif choice == '5':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                history = bank.accounts[account_number].view_transaction_history()
                for transaction in history:
                    print(transaction)
            else:
                print("Account does not exist.")

        elif choice == '6':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                amount = float(input("Enter loan amount: "))
                print(bank.accounts[account_number].take_loan(amount))
            else:
                print("Account does not exist.")

        elif choice == '7':
            account_number = input("Enter your account number: ")
            if account_number in bank.accounts:
                recipient_account_number = input("Enter recipient's account number: ")
                amount = float(input("Enter amount to transfer: "))
                if recipient_account_number in bank.accounts:
                    print(bank.accounts[account_number].transfer_funds(amount, bank.accounts[recipient_account_number]))
                else:
                    print("Recipient account does not exist.")
            else:
                print("Account does not exist.")

        elif choice == '8':
            break
        else:
            print("Invalid choice")

def admin_menu(bank):
    while True:
        print("\nAdmin Menu")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. View All Accounts")
        print("4. Check Total Available Balance")
        print("5. Check Total Loan Amount")
        print("6. Enable/Disable Loan Feature")
        print("7. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter user's name: ")
            email = input("Enter user's email: ")
            address = input("Enter user's address: ")
            account_type = input("Enter account type (Savings/Current): ")
            account_number = bank.create_account(name, email, address, account_type)
            print(f"Account created successfully. Account number is {account_number}")

        elif choice == '2':
            account_number = input("Enter account number to delete: ")
            result = bank.delete_account(account_number)
            print(result)

        elif choice == '3':
            accounts = bank.list_accounts()
            for account in accounts:
                print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")

        elif choice == '4':
            total_balance = bank.total_balance()
            print(f"Total available balance in the bank: {total_balance}")

        elif choice == '5':
            total_loan = bank.total_loan()
            print(f"Total loan amount: {total_loan}")

        elif choice == '6':
            status = input("Enter 'on' to enable or 'off' to disable: ")
            result = bank.enable_loan_feature(status == 'on')
            print(result)

        elif choice == '7':
            break
        else:
            print("Invalid")

if __name__ == "__main__":
    main()
