
AwesomeGIC Bank Application
===========================

Overview
--------
AwesomeGIC Bank is a simple banking application that allows users to:
- Manage multiple bank accounts
- Record deposit and withdrawal transactions
- Define interest rules that apply from certain dates
- Calculate monthly interest based on balances and interest rules
- Generate monthly account statements

Design & Assumptions
--------------------
- Each Account maintains its own transaction history and balance.
- Transactions are deposits ('D'), withdrawals ('W'), or interest ('I').
- Withdrawals cannot cause negative balance; the first transaction cannot be a withdrawal.
- Interest is applied monthly based on rules defined with a date and rate.
- Interest transactions do not have transaction IDs.
- Interest calculations assume a 365-day year.
- Dates are in YYYYMMDD format; statements use YYYYMM.
- Bank class manages all accounts and interest rules.
- CLI allows interactive operations for transactions, interest rules, and statements.
- Decimal arithmetic with rounding HALF_UP is used to ensure financial accuracy.

Environment
-----------
- OS: Windows 10/11, Linux (Ubuntu 20.04+), or MacOS (latest)
- Python version: 3.10 or above recommended
- Libraries: Uses only Python standard libraries (decimal, typing, datetime)
- No external packages required

Setup and Installation
----------------------
1. Ensure Python 3.10+ is installed and added to your PATH.
   To verify, run:
       python --version

2. Clone or download the AwesomeGIC Bank source code to your local machine.

3. (Optional) It is recommended to create a virtual environment:
       python -m venv venv
       On Windows: venv\Scripts\activate
       On Linux/Mac: source venv/bin/activate

4. No external dependencies to install; all libraries used are standard.

Running the Application
-----------------------
1. Navigate to the project root directory (where `cli.py` resides).

2. Run the CLI application:
      python banking/cli.py

3. Follow the on-screen prompts to:
   - Input transactions (Date Account Type Amount)
   - Define interest rules (Date RuleId Rate%)
   - Print statements for accounts
   - Quit the application
   - Enter space bar to go main menu

Example Transaction Input: Enter T or t
    20230626 AC001 W 100.00 - expected result :Error: First transaction cannot be withdrawal
    20230626 AC001 D 100.00 - expected result :Transaction 20230626-01 added successfully.
    20230626 AC001 W 100.00 - expected result :after Deposit withdrawal transaction will inserted.
    Then system responds by displaying the statement of the account:
      Account: AC001
      | Date     | Txn Id      | Type | Amount | Balance |
      | 20230626 | 20230626-01 | D    |  100.00 |   100.00 |
      | 20230626 | 20230626-02 | W    |  100.00 |     0.00 |

-Enter blank to go back to main menu and enter transaction type  I or i for intrest rule
 Upon selecting Define interest rule option, application prompts user to define interest rules:
 Please enter interest rules details in <Date> <RuleId> <Rate in %> format 
(or enter blank to go back to main menu):
Example Interest Rule Input:
    20230615 RULE03 2.20

    Some constraints to note:
      * Date should be in YYYYMMdd format
      * RuleId is string, free format
      * Interest rate should be greater than 0 and less than 100
      * If there's any existing rules on the same day, the latest one is kept
   Then system responds by listing all interest rules orderd by date:
    (assuming there are already RULE01 and RULE02 in the system) 
 
            Interest rules:
            | Date     | RuleId | Rate (%) |
            | 20230101 | RULE01 |     1.95 |
            | 20230520 | RULE02 |     1.90 |
            | 20230615 | RULE03 |     2.20 |
 -Enter blank to go back to main menu and enter transaction type  P or p for print statement option 
- Upon selecting Print statement option, application prompts user to select which account to print the statement for:
      Please enter account and month to generate the statement <Account> <Year><Month>
      When user enters the account
      ```
      AC001 202306
      ```

      System then responds with the following account statement, which shows all the transactions and interest for that month (transaction type for interest is I):
      ```
      Account: AC001
      | Date     | Txn Id      | Type | Amount | Balance |
      | 20230601 | 20230601-01 | D    | 150.00 |  250.00 |
      | 20230626 | 20230626-01 | W    |  20.00 |  230.00 |
      | 20230626 | 20230626-02 | W    | 100.00 |  130.00 |
      | 20230630 |             | I    |   0.39 |  130.39 |
      ```
   - How to apply the interest rule:
      -Interest is applied on end of day balance
      ```
      | Period              | Num of days | EOD Balance | Rate Id | Rate | Annualized Interest      |
      | 20230601 - 20230614 | 14          | 250         | RULE02  | 1.90 | 250 * 1.90% * 14 = 66.50 |
      | 20230615 - 20230625 | 11          | 250         | RULE03  | 2.20 | 250 * 2.20% * 11 = 60.50 |
      | 20230626 - 20230630 |  5          | 130         | RULE03  | 2.20 | 130 * 2.20% *  5 = 14.30 |
      (this table is provided to help you get an idea how the calculation is done, it should not be displayed in the output)
      ```
      * Therefore total interest is: (66.50 + 60.50 + 14.30) / 365 = 0.3871 => 0.39
      * The interest is credited at the last day of the month

4. To exit, choose option 'Q'  or q at the main menu.
      System responds with:
      ```
      Thank you for banking with AwesomeGIC Bank.
      Have a nice day!

Testing in local environment (Windows)
----------------
- Tests are located in the `testing/` directory.
- Run all tests with:
      pytest testing/test_e2e.py or python -m pytest testing\test_e2e.py
- Run with Seprate files 
     pytest testing/test_cli.py or python -m pytest testing\test_cli.py
     pytest testing/test_account.py or python -m pytest testing\test_account.py
     pytest testing/test_interest_rule.py or python -m pytest testing\test_interest_rule.py
     pytest testing/test_transaction.py or python -m pytest testing\test_transaction.py
     pytest testing/test_account.py or python -m pytest testing\test_account.py
- To List all testcases run the below command in Windows
      python -m pytest --collect-only 
- pytest must be installed separately if you want to run tests:
      pip install pytest

- How to Execute the Job
   - GitHub will automatically detect the new workflow and run the job on every push or pull request to main.
   - To see the job execution status:
   - Go to your repo on GitHub.
   - Click on the Actions tab.
   - Select the workflow run to see logs and results.
-To Check job status
  Go to your GitHub repository.
  Click on the "Actions" tab near the top of the repo page.
  You’ll see a list of workflow runs:
       Each entry shows:
      The workflow name (e.g., "CI", "Build", "Test").
      The commit message.
      Click on a workflow run to see detailed status:


Notes
-----
- Dates must follow YYYYMMDD or YYYYMM formats strictly.
- Amounts must be positive decimals.
- Withdrawal cannot be first transaction and cannot cause negative balance.
- Interest rates must be > 0 and < 100.
Please refer to the local test_execution_status file for the result. 

Contact
-------
For questions or support, contact: senlotus204@gmail.com

Thank you for using AwesomeGIC Bank!
