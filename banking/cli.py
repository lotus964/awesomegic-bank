from banking.bank import Bank
from decimal import Decimal, InvalidOperation

class CLI:
    def __init__(self):
        self.bank = Bank()

    def run(self):
        print("Welcome to AwesomeGIC Bank! What would you like to do?")
        while True:
            print("[T] Input transactions")
            print("[I] Define interest rules")
            print("[P] Print statement")
            print("[Q] Quit")
            choice = input(">").strip().upper()
            if choice == 'T':
                self.handle_transactions()
            elif choice == 'I':
                self.handle_interest_rules()
            elif choice == 'P':
                self.handle_print_statement()
            elif choice == 'Q':
                print("Thank you for banking with AwesomeGIC Bank.")
                print("Have a nice day!")
                break
            else:
                print("Invalid option. Please select T, I, P or Q.")



def handle_transactions(self):
    print("Please enter transaction details in <Date> <Account> <Type> <Amount> format")
    print("(or enter blank to go back to main menu):")
    while True:
        line = input(">").strip()
        if line == "":
            break
        parts = line.split()
        if len(parts) != 4:
            print("Invalid input format. Try again.")
            continue
        date, account_id, txn_type, amount_str = parts
        try:
            amount = Decimal(amount_str)
        except InvalidOperation:
            print("Invalid amount format. Try again.")
            continue
        try:
            txn = self.bank.add_transaction(date, account_id, txn_type, amount)
            self.print_account_statement(account_id)
        except Exception as e:
            print(e)


    def handle_interest_rules(self):
        print("Please enter interest rules details in <Date> <RuleId> <Rate in %> format")
        print("(or enter blank to go back to main menu):")
        while True:
            line = input(">").strip()
            if line == "":
                break
            parts = line.split()
            if len(parts) != 3:
                print("Invalid input format. Try again.")
                continue
            date, rule_id, rate_str = parts
            try:
                rate = Decimal(rate_str)
            except InvalidOperation:
                print("Invalid rate format. Try again.")
                continue
            try:
                self.bank.add_interest_rule(date, rule_id, rate)
                self.print_interest_rules()
            except Exception as e:
                print(f"Error: {e}")

    def handle_print_statement(self):
        print("Please enter account and month to generate the statement <Account> <Year><Month>")
        print("(or enter blank to go back to main menu):")
        while True:
            line = input(">").strip()
            if line == "":
                break
            parts = line.split()
            if len(parts) != 2:
                print("Invalid input format. Try again.")
                continue
            account_id, year_month = parts
            try:
                # Calculate interest for the month first
                self.bank.calculate_monthly_interest(account_id, year_month)
                # Print statement
                self.print_account_statement(account_id, year_month)
            except Exception as e:
                print(f"Error: {e}")

    def print_account_statement(self, account_id: str, year_month: str = None):
        if year_month:
            transactions = self.bank.get_account_statement(account_id, year_month)
        else:
            # Print all transactions of the account
            account = self.bank.accounts.get(account_id)
            if not account:
                print(f"Account {account_id} not found")
                return
            transactions = account.transactions

        print(f"Account: {account_id}")
        print("| Date     | Txn Id      | Type | Amount | Balance |")
        balance = Decimal('0.00')
        for txn in sorted(transactions, key=lambda t: (t.date, t.txn_id or "")):
            if txn.txn_type == 'D' or txn.txn_type == 'I':
                balance += txn.amount
            elif txn.txn_type == 'W':
                balance -= txn.amount
            balance = balance.quantize(Decimal('0.01'))
            print(f"| {txn.date} | {txn.txn_id:<11} | {txn.txn_type}    | {txn.amount:7.2f} | {balance:8.2f} |")

    def print_interest_rules(self):
        rules = self.bank.get_interest_rules()
        print("Interest rules:")
        print("| Date     | RuleId | Rate (%) |")
        for r in rules:
            print(f"| {r.date} | {r.rule_id} | {r.rate:8.2f} |")
