from database import connection, cursor, os
from abc import ABC, abstractmethod


# ==========================================
# Customer
# ==========================================
class Customer:

    def __init__(self, customer_id, name, address, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email


# ==========================================
# Abstraction
# ==========================================
class Account(ABC):

    @abstractmethod
    def withdraw(self, account_number, amount):
        pass


# ==========================================
# Bank Account System
# ==========================================
class BankAccountSystem(Account):

    # --------------------------------------
    # Save transaction in database
    # --------------------------------------
    def save_transaction(self, account_number, transaction_type, amount):

        sql = """
        INSERT INTO transactions (account_number, type, amount)
        VALUES (%s, %s, %s)
        """

        values = (account_number, transaction_type, amount)

        cursor.execute(sql, values)
        connection.commit()


    # --------------------------------------
    # Create account
    # --------------------------------------
    def create_account(self, account_number, initial_balance=0):

        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return

        sql = """
        INSERT INTO accounts (account_number, balance)
        VALUES (%s, %s)
        """

        values = (account_number, initial_balance)

        try:
            cursor.execute(sql, values)
            connection.commit()

            print("Account created successfully")

        except:
            print("Account already exists.")


    # --------------------------------------
    # Deposit
    # --------------------------------------
    def deposit(self, account_number, amount):

        if amount <= 0:
            print("Deposit amount must be positive.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_number = %s
        """

        values = (amount, account_number)

        cursor.execute(sql, values)

        if cursor.rowcount == 0:
            print("Account does not exist.")
            return

        connection.commit()

        self.save_transaction(
            account_number,
            "Deposit",
            amount
        )

        print("Deposit successful")


    # --------------------------------------
    # Withdraw
    # --------------------------------------
    def withdraw(self, account_number, amount):

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        try:
            balance = self.get_balance(account_number)

        except ValueError:
            print("Account does not exist.")
            return

        if balance < amount:
            print("Insufficient funds.")
            return

        sql = """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
        """

        values = (amount, account_number)

        cursor.execute(sql, values)
        connection.commit()

        self.save_transaction(
            account_number,
            "Withdraw",
            amount
        )

        print("Withdrawal successful")


    # --------------------------------------
    # Get balance
    # --------------------------------------
    def get_balance(self, account_number):

        sql = """
        SELECT balance
        FROM accounts
        WHERE account_number = %s
        """

        cursor.execute(sql, (account_number,))

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Account does not exist.")

        return result[0]


    # --------------------------------------
    # Delete account
    # --------------------------------------
    def delete_account(self, account_number):

        sql = """
        DELETE FROM accounts
        WHERE account_number = %s
        """

        cursor.execute(sql, (account_number,))

        if cursor.rowcount == 0:
            print("Account does not exist.")
            return

        connection.commit()

        print("Account deleted successfully")


    # --------------------------------------
    # Transfer
    # --------------------------------------
    def transfer(self, from_account, to_account, amount):

        if from_account == to_account:
            print("Cannot transfer to the same account.")
            return

        if amount <= 0:
            print("Transfer amount must be positive.")
            return

        try:
            from_balance = self.get_balance(from_account)
            self.get_balance(to_account)

        except ValueError:
            print("One of the accounts does not exist.")
            return

        if from_balance < amount:
            print("Insufficient funds.")
            return

        try:

            sql1 = """
            UPDATE accounts
            SET balance = balance - %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql1,
                (amount, from_account)
            )

            sql2 = """
            UPDATE accounts
            SET balance = balance + %s
            WHERE account_number = %s
            """

            cursor.execute(
                sql2,
                (amount, to_account)
            )

            connection.commit()

            self.save_transaction(
                from_account,
                "Transfer Out",
                amount
            )

            self.save_transaction(
                to_account,
                "Transfer In",
                amount
            )

            print("Transfer successful")

        except:
            connection.rollback()
            print("Transfer failed.")


    # --------------------------------------
    # Show transactions
    # --------------------------------------
    def show_transactions(self):

        sql = """
        SELECT *
        FROM transactions
        """

        cursor.execute(sql)

        results = cursor.fetchall()

        for transaction in results:
            print(transaction)


# ==========================================
# Savings Account
# ==========================================
class SavingsAccount(BankAccountSystem):

    def withdraw(self, account_number, amount):

        if amount > 500:
            print("Maximum withdrawal is 500 Euro.")
            return

        super().withdraw(
            account_number,
            amount
        )


# ==========================================
# TEST
# ==========================================

bank = BankAccountSystem()
print(os.getenv("DB_USER"))

# Create account
# bank.create_account("111111", 1000)

# Deposit
# bank.deposit("111111", 200)

# Withdraw
# bank.withdraw("111111", 100)

# Balance
# print(bank.get_balance("111111"))

# Transfer
# bank.transfer("111111", "999999", 200)

# Delete
# bank.delete_account("111111")

# Show transactions
# bank.show_transactions()


# ==========================================
# SavingsAccount Test
# ==========================================

# savings = SavingsAccount()

# savings.create_account("222222", 1000)

# savings.withdraw("222222", 300)

# savings.withdraw("222222", 600)