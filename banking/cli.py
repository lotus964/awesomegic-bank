# cli.py

from banking.bank import BankSystem
from banking.transaction import Transaction

class CLI:
    def __init__(self):
        self.bank = BankSystem()

    def run(self):
        print("Welcome to AwesomeGIC Bank! What would you like to do?")
        while True:
            print("[T] Input transactions ")
            print("[I] Define interest rules")
            print("[P] Print statement")
            print("[Q] Quit")
            action = input(">").strip().upper()

            if action == "T":
                self.handle_transactions()
            elif action == "I":
                self.handle_interest_rules()
            elif action == "P":
                self.handle_print_statement()
            elif action == "Q":
                print("Thank you for banking with AwesomeGIC Bank.")
                print("Have a nice day!")
                break
            else:
                print("Invalid selection.")

    def handle_transactions(self):
        print("Please enter transaction details in <Date> <Account> <Type> <Amount> format")
        print("(or enter blank to go back to main menu):")
        while True:
            line = input(">").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 4:
                print("Invalid input format.")
                continue
            date, acc, typ, amt_str = parts
            try:
                amt = float(amt_str)
            except ValueError:
                print("Invalid amount.")
                continue
            success, msg = self.bank.add_transaction(date, acc, typ, amt)
            print(msg)
            if success:
                account = self.bank.list_account_statement(acc)
                print(f"Account: {acc}")
                print("| Date     | Txn Id      | Type | Amount |")
                for txn in account.transactions:
                    print(f"| {txn.date} | {txn.txn_id:<10} | {txn.type}    | {txn.amount:6.2f} |")

    def handle_interest_rules(self):
        print("Please enter interest rules details in <Date> <RuleId> <Rate in %> format")
        print("(or enter blank to go back to main menu):")
        while True:
            line = input(">").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 3:
                print("Invalid input format.")
                continue
            date, rule_id, rate_str = parts
            try:
                rate = float(rate_str)
            except ValueError:
                print("Invalid rate.")
                continue
            success, msg = self.bank.add_interest_rule(date, rule_id, rate)
            print(msg)
            if success:
                rules = self.bank.list_interest_rules()
                print("Interest rules:")
                print("| Date     | RuleId | Rate (%) |")
                for r in rules:
                    print(f"| {r.date} | {r.rule_id:<6} | {r.rate:9.2f} |")

    def handle_print_statement(self):
        print("Please enter account and month to generate the statement <Account> <Year><Month>")
        print("(or enter blank to go back to main menu):")
        while True:
            line = input(">").strip()
            if not line:
                return
            parts = line.split()
            if len(parts) != 2:
                print("Invalid input format.")
                continue
            acc, yyyymm = parts
            acc_data, txns, final = self.bank.get_monthly_statement(acc, yyyymm)
            if not acc_data:
                print("Account not found.")
                continue
            print(f"Account: {acc}")
            print("| Date     | Txn Id      | Type | Amount | Balance |")
            balance = 0.0
            for txn in txns:
                if txn.type == "D":
                    balance += txn.amount
                elif txn.type == "W":
                    balance -= txn.amount
                elif txn.type == "I":
                    balance += txn.amount
                print(f"| {txn.date} | {txn.txn_id:<10} | {txn.type}    | {txn.amount:6.2f} | {balance:7.2f} |")
