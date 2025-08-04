import pytest
from unittest.mock import patch
from banking.cli import CLI

def test_e2e_transaction_deposit_and_withdrawal(capsys):
    # Simulate full CLI interaction: deposit, withdrawal, quit
    user_inputs = [
        "T",                       # Enter transaction menu
        "20230601 AC001 D 200.00",
        "20230610 AC001 W 50.00",
        "",                        # Return to main menu
        "Q"                        # Quit
    ]

    with patch("builtins.input", side_effect=user_inputs):
        cli = CLI()
        cli.run()

    output = capsys.readouterr().out
    assert "Account: AC001" in output
    assert "| 20230601" in output
    assert "| 20230610" in output
    assert "Thank you for banking with AwesomeGIC Bank." in output


def test_e2e_interest_definition_and_statement(capsys):
    user_inputs = [
        "T",                         # Enter transaction menu
        "20230601 AC002 D 1000.00",
        "",                          # Back to main menu
        "I",                         # Define interest rules
        "20230601 RULE01 12.00",
        "",                          # Back to main menu
        "P",                         # Print statement
        "AC002 202306",
        "",                          # Back to main menu
        "Q"
    ]

    with patch("builtins.input", side_effect=user_inputs):
        cli = CLI()
        cli.run()

    output = capsys.readouterr().out
    assert "Account: AC002" in output
    assert "RULE01" in output
    assert "| 20230630 |" in output  # interest credited
    assert "I" in output             # interest transaction
    assert "Thank you for banking with AwesomeGIC Bank." in output


def test_e2e_invalid_inputs_and_validation(capsys):
    user_inputs = [
        "T",
        "invalid input line",
        "20230601 AC003 W 50.00",   # invalid - withdrawal first
        "20230601 AC003 D -10.00",  # invalid - negative deposit
        "",                         # back
        "I",
        "invalid rule line",
        "20230601 R1 0",            # invalid interest rate
        "",                         # back
        "Q"
    ]

    with patch("builtins.input", side_effect=user_inputs):
        cli = CLI()
        cli.run()

    output = capsys.readouterr().out
    assert "Invalid input format" in output
    assert "First transaction cannot be withdrawal" in output
    assert "Amount must be positive" in output
    assert "Rate must be between 0 and 100" in output
    assert "Thank you for banking with AwesomeGIC Bank." in output
